from unittest.mock import AsyncMock

import pytest

from app.application.create_workout_program import (
    CreateWorkoutProgramInput,
    CreateWorkoutProgramUseCase,
    SlotCategoryInput,
    SlotInput,
)
from app.domain.workout_cycle_repository import WorkoutCycleRepository
from app.domain.workout_program import WorkoutProgram
from app.domain.workout_program_repository import WorkoutProgramRepository


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock(spec=WorkoutProgramRepository)
    repo.create.side_effect = lambda program: program
    return repo


@pytest.fixture
def mock_cycle_repo() -> AsyncMock:
    return AsyncMock(spec=WorkoutCycleRepository)


def _make_input(
    name: str = "Programa A",
    slots: list[SlotInput] | None = None,
) -> CreateWorkoutProgramInput:
    if slots is None:
        slots = [
            SlotInput(
                slot_label="Treino A",
                categories=[SlotCategoryInput(category_id=1, muscle_group_id=1)],
            ),
            SlotInput(
                slot_label="Treino B",
                categories=[SlotCategoryInput(category_id=2)],
            ),
        ]
    return CreateWorkoutProgramInput(name=name, slots=slots)


@pytest.mark.anyio
async def test_execute_deactivates_all_before_creating(
    mock_repo: AsyncMock,
) -> None:
    use_case = CreateWorkoutProgramUseCase(repository=mock_repo)
    await use_case.execute(_make_input())

    mock_repo.deactivate_all.assert_awaited_once()
    mock_repo.create.assert_awaited_once()

    # deactivate_all deve ser chamado antes de create
    deactivate_order = mock_repo.deactivate_all.await_args_list
    create_order = mock_repo.create.await_args_list
    assert len(deactivate_order) == 1
    assert len(create_order) == 1


@pytest.mark.anyio
async def test_execute_creates_program_with_slots(
    mock_repo: AsyncMock,
) -> None:
    input_data = _make_input()
    use_case = CreateWorkoutProgramUseCase(repository=mock_repo)
    result = await use_case.execute(input_data)

    assert isinstance(result, WorkoutProgram)
    assert result.name == "Programa A"
    assert result.is_active is True
    assert len(result.slots) == 2
    assert result.slots[0].slot_label == "Treino A"
    assert result.slots[0].slot_order == 0
    assert result.slots[1].slot_label == "Treino B"
    assert result.slots[1].slot_order == 1
    assert result.slots[0].categories[0].category_id == 1
    assert result.slots[0].categories[0].muscle_group_id == 1
    assert result.slots[1].categories[0].muscle_group_id is None


@pytest.mark.anyio
async def test_execute_raises_error_for_empty_name(
    mock_repo: AsyncMock,
) -> None:
    input_data = _make_input(name="  ")
    use_case = CreateWorkoutProgramUseCase(repository=mock_repo)

    with pytest.raises(ValueError, match="Nome do programa não pode ser vazio"):
        await use_case.execute(input_data)

    mock_repo.create.assert_not_awaited()


@pytest.mark.anyio
async def test_execute_raises_error_for_empty_slots(
    mock_repo: AsyncMock,
) -> None:
    input_data = _make_input(slots=[])
    use_case = CreateWorkoutProgramUseCase(repository=mock_repo)

    with pytest.raises(ValueError, match="Programa deve ter ao menos um slot"):
        await use_case.execute(input_data)

    mock_repo.create.assert_not_awaited()


@pytest.mark.anyio
async def test_execute_resets_cycle_for_new_program(
    mock_repo: AsyncMock,
    mock_cycle_repo: AsyncMock,
) -> None:
    use_case = CreateWorkoutProgramUseCase(
        repository=mock_repo, cycle_repository=mock_cycle_repo
    )
    result = await use_case.execute(_make_input())

    mock_cycle_repo.reset_for_program.assert_awaited_once_with(result.id)
