from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.application.get_workout_calendar import (
    CalendarDay,
    GetWorkoutCalendarUseCase,
)
from app.domain.training_category import CategoryID
from app.domain.workout_log import WorkoutLog
from app.domain.workout_log_repository import WorkoutLogRepository


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock(spec=WorkoutLogRepository)


@pytest.mark.anyio
async def test_execute_returns_all_days_of_month(mock_repo: AsyncMock) -> None:
    mock_repo.get_by_date_range.return_value = []

    use_case = GetWorkoutCalendarUseCase(repository=mock_repo)
    result = await use_case.execute(month=4, year=2026)

    assert len(result) == 30  # April has 30 days
    assert result[0].date == date(2026, 4, 1)
    assert result[-1].date == date(2026, 4, 30)


@pytest.mark.anyio
async def test_execute_day_with_done_workout_is_done(mock_repo: AsyncMock) -> None:
    mock_repo.get_by_date_range.return_value = [
        WorkoutLog(
            id="abc-123",
            date=date(2026, 4, 5),
            category_id=CategoryID.MUSCULACAO,
            muscle_group_id=1,
            done=True,
            duration_minutes=60,
        ),
    ]

    use_case = GetWorkoutCalendarUseCase(repository=mock_repo)
    result = await use_case.execute(month=4, year=2026)

    day_5 = result[4]  # index 4 = day 5
    assert day_5.date == date(2026, 4, 5)
    assert day_5.done is True
    assert day_5.count == 1


@pytest.mark.anyio
async def test_execute_day_without_workout_is_not_done(mock_repo: AsyncMock) -> None:
    mock_repo.get_by_date_range.return_value = []

    use_case = GetWorkoutCalendarUseCase(repository=mock_repo)
    result = await use_case.execute(month=4, year=2026)

    day_1 = result[0]
    assert day_1.done is False
    assert day_1.count == 0


@pytest.mark.anyio
async def test_execute_invalid_month_raises_error(mock_repo: AsyncMock) -> None:
    use_case = GetWorkoutCalendarUseCase(repository=mock_repo)

    with pytest.raises(ValueError, match="Mês deve estar entre 1 e 12"):
        await use_case.execute(month=13, year=2026)

    with pytest.raises(ValueError, match="Mês deve estar entre 1 e 12"):
        await use_case.execute(month=0, year=2026)
