import uuid
from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.workout_log import WorkoutLog
from app.infrastructure.database.models import WorkoutLogModel
from app.infrastructure.database.workout_log_repository_impl import (
    SqlAlchemyWorkoutLogRepository,
)


class TestSqlAlchemyWorkoutLogRepository:
    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def repository(
        self, mock_session: AsyncMock
    ) -> SqlAlchemyWorkoutLogRepository:
        return SqlAlchemyWorkoutLogRepository(session=mock_session)

    async def test_create_workout_log(
        self, repository: SqlAlchemyWorkoutLogRepository, mock_session: AsyncMock
    ) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=2,
            done=True,
            duration_minutes=30,
        )

        generated_id = uuid.uuid4()

        async def fake_flush() -> None:
            pass

        async def fake_refresh(model: object) -> None:
            model.id = generated_id  # type: ignore[attr-defined]

        mock_session.add = MagicMock()
        mock_session.flush = AsyncMock(side_effect=fake_flush)
        mock_session.refresh = AsyncMock(side_effect=fake_refresh)

        result = await repository.create(log)

        assert isinstance(result, WorkoutLog)
        assert result.id == str(generated_id)
        assert result.date == date(2026, 4, 9)
        assert result.category_id == 2
        assert result.done is True
        assert result.duration_minutes == 30
        mock_session.add.assert_called_once()

    async def test_get_by_date_range_returns_logs(
        self, repository: SqlAlchemyWorkoutLogRepository, mock_session: AsyncMock
    ) -> None:
        log_id = uuid.uuid4()
        model = MagicMock(spec=WorkoutLogModel)
        model.id = log_id
        model.date = date(2026, 4, 8)
        model.category_id = 1
        model.muscle_group_id = 1
        model.done = True
        model.duration_minutes = 60

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model]
        mock_session.execute.return_value = mock_result

        logs = await repository.get_by_date_range(
            start=date(2026, 4, 1), end=date(2026, 4, 10)
        )

        assert len(logs) == 1
        assert isinstance(logs[0], WorkoutLog)
        assert logs[0].id == str(log_id)
        assert logs[0].date == date(2026, 4, 8)
        assert logs[0].category_id == 1
        assert logs[0].muscle_group_id == 1

    async def test_get_by_date_returns_logs(
        self, repository: SqlAlchemyWorkoutLogRepository, mock_session: AsyncMock
    ) -> None:
        log_id = uuid.uuid4()
        model = MagicMock(spec=WorkoutLogModel)
        model.id = log_id
        model.date = date(2026, 4, 9)
        model.category_id = 2
        model.muscle_group_id = None
        model.done = False
        model.duration_minutes = None

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model]
        mock_session.execute.return_value = mock_result

        logs = await repository.get_by_date(target_date=date(2026, 4, 9))

        assert len(logs) == 1
        assert isinstance(logs[0], WorkoutLog)
        assert logs[0].id == str(log_id)
        assert logs[0].done is False
        assert logs[0].duration_minutes is None
