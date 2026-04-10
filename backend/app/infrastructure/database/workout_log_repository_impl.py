import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.list_workouts_by_date import WorkoutDetail
from app.domain.workout_log import WorkoutLog
from app.domain.workout_log_repository import WorkoutLogRepository
from app.infrastructure.database.models import WorkoutLogModel


class SqlAlchemyWorkoutLogRepository(WorkoutLogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, log: WorkoutLog) -> WorkoutLog:
        model = WorkoutLogModel(
            id=uuid.UUID(log.id),
            date=log.date,
            category_id=log.category_id,
            muscle_group_id=log.muscle_group_id,
            done=log.done,
            duration_minutes=log.duration_minutes,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def create_batch(self, logs: list[WorkoutLog]) -> list[WorkoutLog]:
        models = [
            WorkoutLogModel(
                id=uuid.UUID(log.id),
                date=log.date,
                category_id=log.category_id,
                muscle_group_id=log.muscle_group_id,
                done=log.done,
                duration_minutes=log.duration_minutes,
            )
            for log in logs
        ]
        self._session.add_all(models)
        await self._session.flush()
        for model in models:
            await self._session.refresh(model)
        return [self._to_domain(m) for m in models]

    async def get_by_date_range(
        self, start: date, end: date
    ) -> list[WorkoutLog]:
        stmt = select(WorkoutLogModel).where(
            WorkoutLogModel.date.between(start, end)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def get_by_date(self, target_date: date) -> list[WorkoutLog]:
        stmt = select(WorkoutLogModel).where(
            WorkoutLogModel.date == target_date
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def get_by_date_with_details(
        self, target_date: date
    ) -> list[WorkoutDetail]:
        stmt = (
            select(WorkoutLogModel)
            .where(WorkoutLogModel.date == target_date)
            .options(
                selectinload(WorkoutLogModel.category),
                selectinload(WorkoutLogModel.muscle_group),
            )
            .order_by(WorkoutLogModel.created_at)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_detail(m) for m in models]

    @staticmethod
    def _to_domain(model: WorkoutLogModel) -> WorkoutLog:
        return WorkoutLog(
            id=str(model.id),
            date=model.date,
            category_id=model.category_id,
            muscle_group_id=model.muscle_group_id,
            done=model.done,
            duration_minutes=model.duration_minutes,
        )

    @staticmethod
    def _to_detail(model: WorkoutLogModel) -> WorkoutDetail:
        return WorkoutDetail(
            id=str(model.id),
            date=model.date,
            category_id=model.category_id,
            category_name=model.category.name,
            muscle_group_id=model.muscle_group_id,
            muscle_group_name=model.muscle_group.name if model.muscle_group else None,
            done=model.done,
            duration_minutes=model.duration_minutes,
        )
