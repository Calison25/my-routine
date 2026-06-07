from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.workout_cycle_repository import WorkoutCycleRepository
from app.domain.workout_cycle_state import WorkoutCycleState
from app.infrastructure.database.models import WorkoutCycleStateModel


class SqlAlchemyWorkoutCycleRepository(WorkoutCycleRepository):
    _SINGLETON_ID = 1

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_state(self) -> WorkoutCycleState:
        stmt = select(WorkoutCycleStateModel).where(
            WorkoutCycleStateModel.id == self._SINGLETON_ID
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return WorkoutCycleState()
        return WorkoutCycleState(
            current_slot_order=model.current_slot_order,
            program_id=str(model.program_id) if model.program_id else None,
        )

    async def save_state(self, state: WorkoutCycleState) -> None:
        stmt = select(WorkoutCycleStateModel).where(
            WorkoutCycleStateModel.id == self._SINGLETON_ID
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = WorkoutCycleStateModel(
                id=self._SINGLETON_ID,
                current_slot_order=state.current_slot_order,
                program_id=state.program_id,
                updated_at=datetime.now(timezone.utc),
            )
            self._session.add(model)
        else:
            model.current_slot_order = state.current_slot_order
            model.program_id = state.program_id
            model.updated_at = datetime.now(timezone.utc)

        await self._session.flush()

    async def reset_for_program(self, program_id: str) -> WorkoutCycleState:
        state = WorkoutCycleState(current_slot_order=0, program_id=program_id)
        await self.save_state(state)
        return state
