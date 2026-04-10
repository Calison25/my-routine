from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.application.register_workout import RegisterWorkoutUseCase
from app.domain.training_category import CategoryID
from app.domain.workout_log import WorkoutLog
from app.domain.workout_log_repository import WorkoutLogRepository


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock(spec=WorkoutLogRepository)
    repo.create.side_effect = lambda log: log
    return repo


@pytest.mark.anyio
async def test_execute_with_valid_musculacao_creates_workout(
    mock_repo: AsyncMock,
) -> None:
    workout = WorkoutLog(
        date=date(2026, 4, 9),
        category_id=CategoryID.MUSCULACAO,
        muscle_group_id=1,
        done=True,
        duration_minutes=60,
    )

    use_case = RegisterWorkoutUseCase(repository=mock_repo)
    result = await use_case.execute(workout)

    assert isinstance(result, WorkoutLog)
    assert result.id is not None
    mock_repo.create.assert_awaited_once()
    created_log: WorkoutLog = mock_repo.create.call_args[0][0]
    assert created_log.category_id == CategoryID.MUSCULACAO
    assert created_log.muscle_group_id == 1
    assert created_log.done is True


@pytest.mark.anyio
async def test_execute_with_valid_cardio_creates_workout(
    mock_repo: AsyncMock,
) -> None:
    workout = WorkoutLog(
        date=date(2026, 4, 9),
        category_id=CategoryID.CARDIO,
        muscle_group_id=None,
        done=True,
        duration_minutes=30,
    )

    use_case = RegisterWorkoutUseCase(repository=mock_repo)
    result = await use_case.execute(workout)

    assert isinstance(result, WorkoutLog)
    assert result.id is not None
    mock_repo.create.assert_awaited_once()


@pytest.mark.anyio
async def test_execute_musculacao_without_muscle_group_raises_error(
    mock_repo: AsyncMock,
) -> None:
    workout = WorkoutLog(
        date=date(2026, 4, 9),
        category_id=CategoryID.MUSCULACAO,
        muscle_group_id=None,
        done=True,
    )

    use_case = RegisterWorkoutUseCase(repository=mock_repo)

    with pytest.raises(ValueError, match="Grupo muscular é obrigatório"):
        await use_case.execute(workout)

    mock_repo.create.assert_not_awaited()


@pytest.mark.anyio
async def test_execute_with_invalid_duration_raises_error(
    mock_repo: AsyncMock,
) -> None:
    workout = WorkoutLog(
        date=date(2026, 4, 9),
        category_id=CategoryID.CARDIO,
        muscle_group_id=None,
        done=True,
        duration_minutes=-5,
    )

    use_case = RegisterWorkoutUseCase(repository=mock_repo)

    with pytest.raises(ValueError, match="Duração deve ser maior que zero"):
        await use_case.execute(workout)

    mock_repo.create.assert_not_awaited()
