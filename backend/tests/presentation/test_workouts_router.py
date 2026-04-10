from datetime import date
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.application.get_workout_calendar import CalendarDay, GetWorkoutCalendarUseCase
from app.application.register_workout import RegisterWorkoutUseCase
from app.domain.workout_log import WorkoutLog
from app.main import app
from app.presentation.routers.workouts import (
    get_get_workout_calendar_use_case,
    get_register_workout_use_case,
)


@pytest.fixture
def mock_register_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=RegisterWorkoutUseCase)
    use_case.execute.return_value = WorkoutLog(
        id="test-uuid-1234",
        date=date(2026, 4, 9),
        category_id=2,
        done=True,
        duration_minutes=30,
    )
    return use_case


@pytest.fixture
def mock_register_use_case_error() -> AsyncMock:
    use_case = AsyncMock(spec=RegisterWorkoutUseCase)
    use_case.execute.side_effect = ValueError("Grupo muscular é obrigatório para Musculação")
    return use_case


@pytest.fixture
def mock_calendar_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=GetWorkoutCalendarUseCase)
    use_case.execute.return_value = [
        CalendarDay(date=date(2026, 4, 1), done=False, count=0),
        CalendarDay(date=date(2026, 4, 2), done=True, count=1),
    ]
    return use_case


@pytest.fixture
def client_with_register_mock(mock_register_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_register_workout_use_case] = lambda: mock_register_use_case
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_register_error_mock(mock_register_use_case_error: AsyncMock) -> None:
    app.dependency_overrides[get_register_workout_use_case] = lambda: mock_register_use_case_error
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_calendar_mock(mock_calendar_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_get_workout_calendar_use_case] = lambda: mock_calendar_use_case
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_workout_returns_201(
    mock_register_use_case: AsyncMock, client_with_register_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/workouts",
            json={
                "date": "2026-04-09",
                "category_id": 2,
                "done": True,
                "duration_minutes": 30,
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert "data" in body
    assert body["data"]["id"] == "test-uuid-1234"


@pytest.mark.anyio
async def test_create_workout_invalid_returns_400(
    mock_register_use_case_error: AsyncMock, client_with_register_error_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/workouts",
            json={
                "date": "2026-04-09",
                "category_id": 1,
                "done": True,
            },
        )

    assert response.status_code == 400
    body = response.json()
    assert "error" in body


@pytest.mark.anyio
async def test_get_calendar_returns_200(
    mock_calendar_use_case: AsyncMock, client_with_calendar_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workouts/calendar?month=4&year=2026")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert "days" in body["data"]
    assert len(body["data"]["days"]) == 2
    assert body["data"]["days"][0]["date"] == "2026-04-01"
    assert body["data"]["days"][0]["done"] is False
    assert body["data"]["days"][0]["count"] == 0


@pytest.mark.anyio
async def test_get_calendar_missing_params_returns_422() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workouts/calendar")

    assert response.status_code == 422
