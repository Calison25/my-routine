from unittest.mock import AsyncMock

import pytest

from app.application.set_cycle_position import SetCyclePositionUseCase
from app.domain.workout_cycle_state import WorkoutCycleState
from app.domain.workout_program import WorkoutProgram, WorkoutSlot, WorkoutSlotCategory


def _make_program(num_slots: int = 3) -> WorkoutProgram:
    slots = [
        WorkoutSlot(
            program_id="prog-1",
            slot_label=chr(65 + i),
            slot_order=i,
            categories=[WorkoutSlotCategory(category_id=1, muscle_group_id=i + 1)],
        )
        for i in range(num_slots)
    ]
    return WorkoutProgram(id="prog-1", name="PPL", slots=slots, is_active=True)


@pytest.fixture
def program_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_active.return_value = _make_program(3)
    return repo


@pytest.fixture
def cycle_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_state.return_value = WorkoutCycleState(current_slot_order=0, program_id="prog-1")
    return repo


@pytest.mark.anyio
async def test_set_cycle_position_updates_position(
    program_repo: AsyncMock, cycle_repo: AsyncMock
) -> None:
    use_case = SetCyclePositionUseCase(program_repo, cycle_repo)

    state = await use_case.execute(slot_order=2)

    assert state.current_slot_order == 2
    cycle_repo.save_state.assert_awaited_once()
    saved_state = cycle_repo.save_state.call_args[0][0]
    assert saved_state.current_slot_order == 2


@pytest.mark.anyio
async def test_set_cycle_position_raises_for_invalid_position(
    program_repo: AsyncMock, cycle_repo: AsyncMock
) -> None:
    use_case = SetCyclePositionUseCase(program_repo, cycle_repo)

    with pytest.raises(ValueError, match="Posição inválida"):
        await use_case.execute(slot_order=5)

    with pytest.raises(ValueError, match="Posição inválida"):
        await use_case.execute(slot_order=-1)

    cycle_repo.save_state.assert_not_awaited()


@pytest.mark.anyio
async def test_set_cycle_position_raises_without_program(
    cycle_repo: AsyncMock,
) -> None:
    program_repo = AsyncMock()
    program_repo.get_active.return_value = None
    use_case = SetCyclePositionUseCase(program_repo, cycle_repo)

    with pytest.raises(ValueError, match="Nenhum programa ativo"):
        await use_case.execute(slot_order=0)
