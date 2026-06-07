from dataclasses import dataclass
from typing import Optional

from app.domain.workout_cycle_repository import WorkoutCycleRepository
from app.domain.workout_program import (
    WorkoutProgram,
    WorkoutSlot,
    WorkoutSlotCategory,
)
from app.domain.workout_program_repository import WorkoutProgramRepository


@dataclass(frozen=True)
class SlotCategoryInput:
    category_id: int
    muscle_group_id: Optional[int] = None


@dataclass(frozen=True)
class SlotInput:
    slot_label: str
    categories: list[SlotCategoryInput]


@dataclass(frozen=True)
class CreateWorkoutProgramInput:
    name: str
    slots: list[SlotInput]


class CreateWorkoutProgramUseCase:
    def __init__(
        self,
        repository: WorkoutProgramRepository,
        cycle_repository: Optional[WorkoutCycleRepository] = None,
    ) -> None:
        self._repository = repository
        self._cycle_repository = cycle_repository

    async def execute(self, input_data: CreateWorkoutProgramInput) -> WorkoutProgram:
        await self._repository.deactivate_all()

        slots = [
            WorkoutSlot(
                program_id="",
                slot_label=s.slot_label,
                slot_order=i,
                categories=[
                    WorkoutSlotCategory(
                        category_id=c.category_id,
                        muscle_group_id=c.muscle_group_id,
                    )
                    for c in s.categories
                ],
            )
            for i, s in enumerate(input_data.slots)
        ]

        program = WorkoutProgram(name=input_data.name, slots=slots, is_active=True)
        program.validate()

        created = await self._repository.create(program)

        if self._cycle_repository:
            await self._cycle_repository.reset_for_program(created.id)

        return created
