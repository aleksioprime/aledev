from sqlalchemy import desc, nulls_first, select
from sqlalchemy.orm import selectinload

from src.constants.base import LangEnum
from src.models.achievement import Achievement
from src.models.experience import Experience
from src.models.mentoring import MentoringMetric, MentoringPage
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


def _translation(translations, lang: str):
    """Перевод на нужном языке, иначе русский, иначе любой"""
    by_lang = {t.lang.value if hasattr(t.lang, "value") else t.lang: t for t in translations}
    return by_lang.get(lang) or by_lang.get(LangEnum.ru.value) or next(iter(by_lang.values()), None)


class PortfolioExportService:
    """Собирает данные портфолио из базы и отдаёт документ Word"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def build_docx(self, lang: str) -> bytes:
        async with self.uow:
            session = self.uow.session
            experiences = (await session.execute(
                select(Experience).order_by(nulls_first(desc(Experience.end_date)), desc(Experience.start_date))
            )).scalars().unique().all()
            # На сайте показываются избранные проекты — их же выгружаем
            projects = (await session.execute(
                select(Project).where(Project.is_favorite.is_(True)).order_by(Project.order)
            )).scalars().unique().all()
            achievements = (await session.execute(
                select(Achievement)
                .where(Achievement.is_published.is_(True))
                .order_by(Achievement.year.desc().nullslast(), Achievement.order)
            )).scalars().unique().all()
            page = (await session.execute(
                select(MentoringPage)
                .where(MentoringPage.slug == "mentoring", MentoringPage.is_published.is_(True))
                .options(
                    selectinload(MentoringPage.translations),
                    selectinload(MentoringPage.metrics).selectinload(MentoringMetric.translations),
                )
            )).scalars().unique().one_or_none()

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
            if page is not None:
                page_tr = _translation(page.translations, lang)
                data.mentoring_lead = page_tr.lead if page_tr else None
                for metric in sorted(page.metrics, key=lambda m: m.order):
                    metric_tr = _translation(metric.translations, lang)
                    data.metrics.append(ExportMetric(value=metric.value, label=metric_tr.label if metric_tr else metric.key))

        return build_portfolio_docx(data)
