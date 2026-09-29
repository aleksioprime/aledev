from sqlalchemy import desc, nulls_first, select

from src.constants.base import LangEnum
from src.models.achievement import Achievement
from src.models.experience import Experience
from src.models.project import Project
from src.repositories.uow import UnitOfWork
from src.utils.portfolio_docx import (
    ExportAchievement,
    ExportExperience,
    ExportMetric,
    ExportProject,
    PortfolioExportData,
    build_portfolio_docx,
)

# Контент секции наставничества задаётся статически (совпадает с лендингом)
_MENTORING_STATIC = {
    "ru": {
        "lead": (
            "Опыт руководства кафедрой дизайна и технологии Международной гимназии «Сколково»: учебные программы по ИИ, программированию и робототехнике, инженерная лаборатория и десятки ученических проектов - от роботов до нейросетей."
        ),
        "metrics": [
            ("30+", "проектов учеников"),
            ("20+", "призёров и победителей конкурсов"),
            ("10+", "учебных программ"),
        ],
    },
    "en": {
        "lead": (
            "Experience heading the Design & Technology department at the Skolkovo International Gymnasium: "
            "curricula in AI, programming and robotics, an engineering lab and dozens of student projects - "
            "from robots to neural networks."
        ),
        "metrics": [
            ("30+", "student projects"),
            ("20+", "competition prize winners"),
            ("10+", "curricula"),
        ],
    },
}


def _translation(translations, lang: str):
    """Перевод на нужном языке, иначе русский, иначе любой"""
    by_lang = {t.lang.value if hasattr(t.lang, "value") else t.lang: t for t in translations}
    return by_lang.get(lang) or by_lang.get(LangEnum.ru.value) or next(iter(by_lang.values()), None)


class PortfolioExportService:
    """Собирает данные портфолио из базы и отдаёт документ Word"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def build_docx(self, lang: str) -> bytes:
        """
        Собирает документ Word на выбранном языке
        """
        async with self.uow:
            session = self.uow.session
            experiences = (await session.execute(
                select(Experience).order_by(nulls_first(desc(Experience.end_date)), desc(Experience.start_date))
            )).scalars().unique().all()
            # На сайте показываются избранные проекты - их же выгружаем
            projects = (await session.execute(
                select(Project).where(Project.is_favorite.is_(True)).order_by(Project.order)
            )).scalars().unique().all()
            achievements = (await session.execute(
                select(Achievement)
                .where(Achievement.is_published.is_(True))
                .order_by(Achievement.year.desc().nullslast(), Achievement.order)
            )).scalars().unique().all()

            data = PortfolioExportData(lang=lang)
            for exp in experiences:
                tr = _translation(exp.translations, lang)
                if tr is None:
                    continue
                data.experiences.append(ExportExperience(
                    start_date=exp.start_date, end_date=exp.end_date, is_current=exp.is_current,
                    position=tr.position, company=tr.company,
                    responsibilities=tr.responsibilities, description=tr.description,
                ))
            for project in projects:
                tr = _translation(project.translations, lang)
                if tr is None:
                    continue
                data.projects.append(ExportProject(
                    title=tr.title, short_description=tr.short_description,
                    description=tr.description, stack=project.stack,
                ))
            for item in achievements:
                tr = _translation(item.translations, lang)
                if tr is None:
                    continue
                data.achievements.append(ExportAchievement(
                    title=tr.title, category=item.category, scope=item.scope, year=item.year,
                    organization=tr.organization, result=tr.result,
                    description=tr.short_description or tr.description,
                ))
            mentoring_content = _MENTORING_STATIC.get(lang) or _MENTORING_STATIC["ru"]
            data.mentoring_lead = mentoring_content["lead"]
            data.metrics = [
                ExportMetric(value=value, label=label) for value, label in mentoring_content["metrics"]
            ]

        return build_portfolio_docx(data)
