from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, func, update, or_, and_, desc

from src.constants.base import EmailStatus, FeedbackKind, FeedbackStatus
from src.models.feedback import Feedback
from src.repositories.base import BaseSQLRepository
from src.schemas.feedback import FeedbackQueryParams


class FeedbackRepository(BaseSQLRepository):

    async def create(self, **data) -> Feedback:
        feedback = Feedback(**data)
        self.session.add(feedback)
        await self.session.flush()
        return feedback

    async def get_by_id(self, feedback_id: UUID) -> Feedback | None:
        return await self.session.get(Feedback, feedback_id)

    async def get_all(self, params: FeedbackQueryParams) -> tuple[list[Feedback], int]:
        conditions = []
        if params.kind:
            conditions.append(Feedback.kind == params.kind)
        if params.status:
            conditions.append(Feedback.status == params.status)
        if params.search:
            pattern = f"%{params.search.strip()}%"
            conditions.append(or_(
                Feedback.name.ilike(pattern),
                Feedback.email.ilike(pattern),
                Feedback.message.ilike(pattern),
                Feedback.contact.ilike(pattern),
            ))

        stmt = (
            select(Feedback)
            .where(*conditions)
            .order_by(desc(Feedback.created_at))
            .limit(params.limit)
            .offset(params.offset)
        )
        items = (await self.session.execute(stmt)).scalars().all()
        total = (await self.session.execute(
            select(func.count()).select_from(Feedback).where(*conditions)
        )).scalar_one()
        return list(items), total

    async def stats(self) -> dict:
        def count(*where):
            return select(func.count()).select_from(Feedback).where(*where).scalar_subquery()

        row = (await self.session.execute(select(
            count().label("total"),
            count(Feedback.status == FeedbackStatus.new).label("new"),
            count(Feedback.kind == FeedbackKind.order).label("orders"),
            count(Feedback.kind == FeedbackKind.training).label("trainings"),
            count(Feedback.kind == FeedbackKind.question).label("questions"),
            count(Feedback.email_status == EmailStatus.failed).label("email_failed"),
        ))).one()
        return dict(row._mapping)

    async def update(self, feedback_id: UUID, **values) -> Feedback | None:
        if values:
            await self.session.execute(
                update(Feedback).where(Feedback.id == feedback_id).values(**values)
            )
        feedback = await self.get_by_id(feedback_id)
        if feedback:
            await self.session.refresh(feedback)
        return feedback

    async def delete(self, feedback_id: UUID) -> bool:
        feedback = await self.get_by_id(feedback_id)
        if not feedback:
            return False
        await self.session.delete(feedback)
        return True

    # --- Очередь отправки писем ---

    async def claim_for_email(self, feedback_id: UUID) -> Feedback | None:
        """
        Атомарно «забирает» обращение на отправку: pending/failed → sending.
        Защищает от двойной отправки фоновой задачей и воркером повторов.
        """
        stmt = (
            update(Feedback)
            .where(
                Feedback.id == feedback_id,
                Feedback.email_status.in_([EmailStatus.pending, EmailStatus.failed]),
            )
            .values(
                email_status=EmailStatus.sending,
                email_attempts=Feedback.email_attempts + 1,
                updated_at=datetime.now(timezone.utc),
            )
            .returning(Feedback.id)
        )
        claimed = (await self.session.execute(stmt)).scalar_one_or_none()
        if claimed is None:
            return None
        feedback = await self.get_by_id(feedback_id)
        await self.session.refresh(feedback)
        return feedback

    async def get_retry_ids(self, max_attempts: int, limit: int = 20) -> list[UUID]:
        """
        Обращения, письмо по которым нужно (пере)отправить:
        - pending старше 30 секунд (фоновая задача не отработала, например, из-за рестарта);
        - failed с оставшимися попытками (с растущей паузой между попытками);
        - «зависшие» в sending дольше 10 минут.
        """
        now = datetime.now(timezone.utc)
        stmt = (
            select(Feedback.id)
            .where(
                Feedback.email_attempts < max_attempts,
                Feedback.created_at > now - timedelta(days=3),
                or_(
                    and_(Feedback.email_status == EmailStatus.pending,
                         Feedback.created_at < now - timedelta(seconds=30)),
                    and_(Feedback.email_status == EmailStatus.failed,
                         Feedback.updated_at < now - func.make_interval(0, 0, 0, 0, 0,
                                                                        Feedback.email_attempts * Feedback.email_attempts)),
                    and_(Feedback.email_status == EmailStatus.sending,
                         Feedback.updated_at < now - timedelta(minutes=10)),
                ),
            )
            .order_by(Feedback.created_at)
            .limit(limit)
        )
        return list((await self.session.execute(stmt)).scalars().all())

    async def release_stuck(self, feedback_id: UUID) -> None:
        """ Возвращает зависшее в sending обращение в очередь """
        await self.session.execute(
            update(Feedback)
            .where(Feedback.id == feedback_id, Feedback.email_status == EmailStatus.sending)
            .values(email_status=EmailStatus.failed)
        )
