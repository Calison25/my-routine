from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING, Any

from app.domain.workout_log import WorkoutLog

if TYPE_CHECKING:
    from app.application.list_workouts_by_date import WorkoutDetail


class WorkoutLogRepository(ABC):
    @abstractmethod
    async def create(self, log: WorkoutLog) -> WorkoutLog: ...

    @abstractmethod
    async def create_batch(self, logs: list[WorkoutLog]) -> list[WorkoutLog]: ...

    @abstractmethod
    async def get_by_date_range(
        self, start: date, end: date
    ) -> list[WorkoutLog]: ...

    @abstractmethod
    async def get_by_date(self, target_date: date) -> list[WorkoutLog]: ...

    @abstractmethod
    async def get_by_date_with_details(
        self, target_date: date
    ) -> list[Any]: ...
