from app.domain.training_category import TrainingCategory
from app.domain.training_category_repository import TrainingCategoryRepository


class ListTrainingCategoriesUseCase:
    def __init__(self, repository: TrainingCategoryRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[TrainingCategory]:
        return await self._repository.list_all()
