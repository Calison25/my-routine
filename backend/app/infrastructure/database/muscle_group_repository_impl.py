from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.muscle_group import MuscleGroup
from app.domain.muscle_group_repository import MuscleGroupRepository
from app.infrastructure.database.models import MuscleGroupModel


class SqlAlchemyMuscleGroupRepository(MuscleGroupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_category(self, category_id: int) -> list[MuscleGroup]:
        stmt = select(MuscleGroupModel).where(
            MuscleGroupModel.category_id == category_id
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [
            MuscleGroup(
                id=model.id,
                name=model.name,
                category_id=model.category_id,
            )
            for model in models
        ]
