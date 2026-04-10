from abc import ABC, abstractmethod

from app.domain.muscle_group import MuscleGroup


class MuscleGroupRepository(ABC):
    @abstractmethod
    async def list_by_category(self, category_id: int) -> list[MuscleGroup]: ...
