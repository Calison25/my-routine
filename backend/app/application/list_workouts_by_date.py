from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.workout_log_repository import WorkoutLogRepository


@dataclass(frozen=True)
class WorkoutDetail:
    id: str
    date: date
    category_id: int
    category_name: str
    muscle_group_id: Optional[int]
    muscle_group_name: Optional[str]
    done: bool
    duration_minutes: Optional[int]


class ListWorkoutsByDateUseCase:
    def __init__(self, repository: WorkoutLogRepository) -> None:
        self._repository = repository

    async def execute(self, target_date: date) -> list[WorkoutDetail]:
        logs = await self._repository.get_by_date_with_details(target_date)
        return logs
