from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.training_category import TrainingCategory
from app.domain.training_category_repository import TrainingCategoryRepository
from app.infrastructure.database.models import TrainingCategoryModel


class SqlAlchemyTrainingCategoryRepository(TrainingCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[TrainingCategory]:
        result = await self._session.execute(select(TrainingCategoryModel))
        models = result.scalars().all()
        return [
            TrainingCategory(id=model.id, name=model.name)
            for model in models
        ]
