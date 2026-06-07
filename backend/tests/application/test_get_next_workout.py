from unittest.mock import AsyncMock

import pytest

from app.application.get_next_workout import GetNextWorkoutUseCase, NextWorkoutOutput
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


@pytest.mark.anyio
async def test_execute_returns_none_when_no_active_program(
    mock_program_repo: AsyncMock,
    mock_cycle_repo: AsyncMock,
) -> None:
    mock_program_repo.get_active.return_value = None

    use_case = GetNextWorkoutUseCase(
        program_repository=mock_program_repo,
        cycle_repository=mock_cycle_repo,
    )
    result = await use_case.execute()

    assert result is None
    mock_cycle_repo.get_state.assert_not_awaited()


@pytest.mark.anyio
async def test_execute_returns_current_slot(
    mock_program_repo: AsyncMock,
    mock_cycle_repo: AsyncMock,
) -> None:
    categories = [WorkoutSlotCategory(category_id=1, muscle_group_id=2)]
    slot_a = WorkoutSlot(
        program_id="prog-1",
        slot_label="Treino A",
        slot_order=0,
        categories=categories,
    )
    slot_b = WorkoutSlot(
        program_id="prog-1",
        slot_label="Treino B",
        slot_order=1,
        categories=[WorkoutSlotCategory(category_id=2)],
    )
    program = WorkoutProgram(
        name="PPL",
        slots=[slot_a, slot_b],
        is_active=True,
        id="prog-1",
    )

    mock_program_repo.get_active.return_value = program
    mock_cycle_repo.get_state.return_value = WorkoutCycleState(
        current_slot_order=0, program_id="prog-1"
    )

    use_case = GetNextWorkoutUseCase(
        program_repository=mock_program_repo,
        cycle_repository=mock_cycle_repo,
    )
    result = await use_case.execute()

    assert result is not None
    assert isinstance(result, NextWorkoutOutput)
    assert result.slot_label == "Treino A"
    assert result.slot_order == 0
    assert result.categories == categories
    assert result.program_name == "PPL"
