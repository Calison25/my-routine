from datetime import date
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.application.advance_cycle import AdvanceCycleUseCase
from app.application.get_next_workout import GetNextWorkoutUseCase, NextWorkoutOutput
from app.application.get_workout_calendar import CalendarDay, GetWorkoutCalendarUseCase
from app.application.register_workout import RegisterWorkoutUseCase
from app.application.set_cycle_position import SetCyclePositionUseCase
from app.domain.workout_cycle_state import WorkoutCycleState
from app.domain.workout_log import WorkoutLog
from app.domain.workout_program import WorkoutSlotCategory
from app.main import app
from app.presentation.routers.workouts import (
    get_advance_cycle_use_case,
    get_get_workout_calendar_use_case,
    get_next_workout_use_case,
    get_register_workout_use_case,
    get_set_cycle_position_use_case,
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
    assert "test-uuid-1234" in body["data"]["ids"]


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


# --- today-program tests ---


@pytest.fixture
def mock_next_workout_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=GetNextWorkoutUseCase)
    use_case.execute.return_value = NextWorkoutOutput(
        slot_label="A",
        slot_order=0,
        slot_id="slot-1",
        program_name="Push Pull Legs",
        categories=[
            WorkoutSlotCategory(id="cat-1", category_id=1, muscle_group_id=3),
            WorkoutSlotCategory(id="cat-2", category_id=1, muscle_group_id=4),
        ],
    )
    return use_case


@pytest.fixture
def mock_next_workout_use_case_none() -> AsyncMock:
    use_case = AsyncMock(spec=GetNextWorkoutUseCase)
    use_case.execute.return_value = None
    return use_case


@pytest.fixture
def client_with_next_workout_mock(mock_next_workout_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_next_workout_use_case] = lambda: mock_next_workout_use_case
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_next_workout_none_mock(mock_next_workout_use_case_none: AsyncMock) -> None:
    app.dependency_overrides[get_next_workout_use_case] = lambda: mock_next_workout_use_case_none
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_today_program_returns_200_with_slot(
    mock_next_workout_use_case: AsyncMock, client_with_next_workout_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workouts/today-program")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    data = body["data"]
    assert data["slot_label"] == "A"
    assert data["slot_order"] == 0
    assert data["program_name"] == "Push Pull Legs"
    assert len(data["categories"]) == 2
    assert data["categories"][0]["category_id"] == 1
    assert data["categories"][0]["muscle_group_id"] == 3


@pytest.mark.anyio
async def test_get_today_program_returns_null_when_no_program(
    mock_next_workout_use_case_none: AsyncMock, client_with_next_workout_none_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/workouts/today-program")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"] is None


# --- skip-today tests ---


@pytest.fixture
def mock_advance_cycle_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=AdvanceCycleUseCase)
    use_case.execute.return_value = WorkoutCycleState(current_slot_order=1, program_id="prog-1")
    return use_case


@pytest.fixture
def client_with_advance_cycle_mock(mock_advance_cycle_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_advance_cycle_use_case] = lambda: mock_advance_cycle_use_case
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_skip_today_returns_200(
    mock_advance_cycle_use_case: AsyncMock, client_with_advance_cycle_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/workouts/skip-today")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"]["current_slot_order"] == 1
    mock_advance_cycle_use_case.execute.assert_awaited_once()


# --- cycle-position tests ---


@pytest.fixture
def mock_set_cycle_position_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=SetCyclePositionUseCase)
    use_case.execute.return_value = WorkoutCycleState(current_slot_order=2, program_id="prog-1")
    return use_case


@pytest.fixture
def client_with_set_cycle_position_mock(mock_set_cycle_position_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_set_cycle_position_use_case] = (
        lambda: mock_set_cycle_position_use_case
    )
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_set_cycle_position_returns_200(
    mock_set_cycle_position_use_case: AsyncMock, client_with_set_cycle_position_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.put(
            "/api/workouts/cycle-position",
            json={"slot_order": 2},
        )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"]["current_slot_order"] == 2
    mock_set_cycle_position_use_case.execute.assert_awaited_once_with(2)
