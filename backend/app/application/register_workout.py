from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from app.domain.workout_log import WorkoutLog
from app.domain.workout_log_repository import WorkoutLogRepository

if TYPE_CHECKING:
    from app.application.advance_cycle import AdvanceCycleUseCase


class RegisterWorkoutUseCase:
    def __init__(
        self,
        repository: WorkoutLogRepository,
        advance_cycle: Optional[AdvanceCycleUseCase] = None,
    ) -> None:
        self._repository = repository
        self._advance_cycle = advance_cycle

    async def execute(self, log: WorkoutLog) -> WorkoutLog:
        log.validate()
        result = await self._repository.create(log)
        if log.done and log.program_slot_id and self._advance_cycle is not None:
            try:
                await self._advance_cycle.execute()
            except ValueError:
                pass  # sem programa ativo
        return result
