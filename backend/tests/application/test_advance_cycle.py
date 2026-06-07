from unittest.mock import AsyncMock

import pytest

from app.application.advance_cycle import AdvanceCycleUseCase
from app.domain.workout_cycle_state import WorkoutCycleState
from app.domain.workout_program import (
    WorkoutProgram,
    WorkoutSlot,
    WorkoutSlotCategory,
)
from app.domain.workout_program_repository import WorkoutProgramRepository
from app.domain.workout_cycle_repository import WorkoutCycleRepository


@pytest.fixture
def mock_program_repo() -> AsyncMock:
    return AsyncMock(spec=WorkoutProgramRepository)


@pytest.fixture
def mock_cycle_repo() -> AsyncMock:
    return AsyncMock(spec=WorkoutCycleRepository)


def _make_program(num_slots: int = 3) -> WorkoutProgram:
    slots = [
        WorkoutSlot(
            program_id="prog-1",
            slot_label=f"Treino {chr(65 + i)}",
            slot_order=i,
            categories=[WorkoutSlotCategory(category_id=1)],
        )
        for i in range(num_slots)
    ]
    return WorkoutProgram(
        name="PPL", slots=slots, is_active=True, id="prog-1"
    )


@pytest.mark.anyio
async def test_execute_advances_cycle_and_saves(
    mock_program_repo: AsyncMock,
    mock_cycle_repo: AsyncMock,
) -> None:
    mock_program_repo.get_active.return_value = _make_program(3)
    state = WorkoutCycleState(current_slot_order=0, program_id="prog-1")
    mock_cycle_repo.get_state.return_value = state

    use_case = AdvanceCycleUseCase(
        program_repository=mock_program_repo,
        cycle_repository=mock_cycle_repo,
    )
    result = await use_case.execute()

    assert result.current_slot_order == 1
    mock_cycle_repo.save_state.assert_awaited_once_with(state)


@pytest.mark.anyio
async def test_execute_raises_error_without_active_program(
    mock_program_repo: AsyncMock,
    mock_cycle_repo: AsyncMock,
) -> None:
    mock_program_repo.get_active.return_value = None

    use_case = AdvanceCycleUseCase(
        program_repository=mock_program_repo,
        cycle_repository=mock_cycle_repo,
    )

    with pytest.raises(ValueError, match="Nenhum programa ativo"):
        await use_case.execute()

    mock_cycle_repo.get_state.assert_not_awaited()
    mock_cycle_repo.save_state.assert_not_awaited()
