from dataclasses import dataclass
from typing import Optional

from app.domain.workout_cycle_repository import WorkoutCycleRepository
from app.domain.workout_program import WorkoutSlotCategory
from app.domain.workout_program_repository import WorkoutProgramRepository


@dataclass(frozen=True)
class NextWorkoutOutput:
    slot_id: str
    slot_label: str
    slot_order: int
    categories: list[WorkoutSlotCategory]
    program_name: str


class GetNextWorkoutUseCase:
    def __init__(
        self,
        program_repository: WorkoutProgramRepository,
        cycle_repository: WorkoutCycleRepository,
    ) -> None:
        self._program_repository = program_repository
        self._cycle_repository = cycle_repository

    async def execute(self) -> Optional[NextWorkoutOutput]:
        program = await self._program_repository.get_active()
        if not program:
            return None
        state = await self._cycle_repository.get_state()
        safe_index = state.current_slot_order % len(program.slots)
        slot = program.slots[safe_index]
        return NextWorkoutOutput(
            slot_id=slot.id,
            slot_label=slot.slot_label,
            slot_order=slot.slot_order,
            categories=slot.categories,
            program_name=program.name,
        )
