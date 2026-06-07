from unittest.mock import AsyncMock

import pytest

from app.application.get_active_program import GetActiveProgramUseCase
from app.domain.workout_program import WorkoutProgram, WorkoutSlot, WorkoutSlotCategory
from app.domain.workout_program_repository import WorkoutProgramRepository


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock(spec=WorkoutProgramRepository)


@pytest.mark.anyio
async def test_execute_returns_active_program(mock_repo: AsyncMock) -> None:
    program = WorkoutProgram(
        name="Programa A",
        slots=[
            WorkoutSlot(
                program_id="any",
                slot_label="Treino A",
                slot_order=1,
                categories=[WorkoutSlotCategory(category_id=1)],
            )
        ],
        is_active=True,
    )
    mock_repo.get_active.return_value = program

    use_case = GetActiveProgramUseCase(repository=mock_repo)
    result = await use_case.execute()

    assert result is not None
    assert isinstance(result, WorkoutProgram)
    assert result.is_active is True
    assert result.name == "Programa A"
    mock_repo.get_active.assert_awaited_once()


@pytest.mark.anyio
async def test_execute_returns_none_when_no_active_program(
    mock_repo: AsyncMock,
) -> None:
    mock_repo.get_active.return_value = None

    use_case = GetActiveProgramUseCase(repository=mock_repo)
    result = await use_case.execute()

    assert result is None
    mock_repo.get_active.assert_awaited_once()
