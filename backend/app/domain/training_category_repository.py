from abc import ABC, abstractmethod

from app.domain.training_category import TrainingCategory


class TrainingCategoryRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[TrainingCategory]: ...
