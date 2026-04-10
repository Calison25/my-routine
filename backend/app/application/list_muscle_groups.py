from app.domain.muscle_group import MuscleGroup
from app.domain.muscle_group_repository import MuscleGroupRepository


class ListMuscleGroupsUseCase:
    def __init__(self, repository: MuscleGroupRepository) -> None:
        self._repository = repository

    async def execute(self, category_id: int) -> list[MuscleGroup]:
        return await self._repository.list_by_category(category_id)
