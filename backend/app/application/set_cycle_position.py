from app.domain.workout_cycle_repository import WorkoutCycleRepository
from app.domain.workout_cycle_state import WorkoutCycleState
from app.domain.workout_program_repository import WorkoutProgramRepository


class SetCyclePositionUseCase:
    def __init__(
        self,
        program_repository: WorkoutProgramRepository,
        cycle_repository: WorkoutCycleRepository,
    ) -> None:
        self._program_repository = program_repository
        self._cycle_repository = cycle_repository

    async def execute(self, slot_order: int) -> WorkoutCycleState:
        program = await self._program_repository.get_active()
        if not program:
            raise ValueError("Nenhum programa ativo")
        if slot_order < 0 or slot_order >= len(program.slots):
            raise ValueError("Posição inválida")
        state = await self._cycle_repository.get_state()
        state.current_slot_order = slot_order
        await self._cycle_repository.save_state(state)
        return state
