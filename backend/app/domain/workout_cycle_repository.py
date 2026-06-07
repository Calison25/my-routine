from abc import ABC, abstractmethod

from app.domain.workout_cycle_state import WorkoutCycleState


class WorkoutCycleRepository(ABC):
    @abstractmethod
    async def get_state(self) -> WorkoutCycleState: ...

    @abstractmethod
    async def save_state(self, state: WorkoutCycleState) -> None: ...

    @abstractmethod
    async def reset_for_program(self, program_id: str) -> WorkoutCycleState: ...
