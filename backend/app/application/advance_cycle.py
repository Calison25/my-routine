from app.domain.workout_cycle_repository import WorkoutCycleRepository
from app.domain.workout_cycle_state import WorkoutCycleState
from app.domain.workout_program_repository import WorkoutProgramRepository


class AdvanceCycleUseCase:
    def __init__(
        self,
        program_repository: WorkoutProgramRepository,
        cycle_repository: WorkoutCycleRepository,
    ) -> None:
        self._program_repository = program_repository
        self._cycle_repository = cycle_repository

    async def execute(self) -> WorkoutCycleState:
        program = await self._program_repository.get_active()
        if not program:
            raise ValueError("Nenhum programa ativo")
        state = await self._cycle_repository.get_state()
        state.advance(len(program.slots))
        await self._cycle_repository.save_state(state)
        return state
