from datetime import datetime
from typing import Optional
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.application.create_workout_program import CreateWorkoutProgramUseCase
from app.application.get_active_program import GetActiveProgramUseCase
from app.domain.workout_program import (
    WorkoutProgram,
    WorkoutSlot,
    WorkoutSlotCategory,
)
from app.infrastructure.database.workout_program_repository_impl import (
    SqlAlchemyWorkoutProgramRepository,
)
from app.main import app
from app.presentation.routers.programs import (
    _get_repository,
    get_active_program_use_case,
    get_create_program_use_case,
)


def _make_program(
    program_id: str = "prog-uuid-1234",
    name: str = "Treino ABC",
    is_active: bool = True,
) -> WorkoutProgram:
    return WorkoutProgram(
        id=program_id,
        name=name,
        is_active=is_active,
        created_at=datetime(2026, 4, 11, 10, 0, 0),
        slots=[
            WorkoutSlot(
                id="slot-uuid-1",
                program_id=program_id,
                slot_label="Dia A",
                slot_order=0,
                categories=[
                    WorkoutSlotCategory(
                        id="cat-uuid-1",
                        category_id=1,
                        muscle_group_id=1,
                    ),
                ],
            ),
        ],
    )


_VALID_PAYLOAD = {
    "name": "Treino ABC",
    "slots": [
        {
            "slot_label": "Dia A",
            "categories": [{"category_id": 1, "muscle_group_id": 1}],
        },
    ],
}


# --------------- fixtures ---------------


@pytest.fixture
def mock_create_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=CreateWorkoutProgramUseCase)
    use_case.execute.return_value = _make_program()
    return use_case


@pytest.fixture
def mock_create_use_case_error() -> AsyncMock:
    use_case = AsyncMock(spec=CreateWorkoutProgramUseCase)
    use_case.execute.side_effect = ValueError("Nome do programa não pode ser vazio")
    return use_case


@pytest.fixture
def mock_active_program_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=GetActiveProgramUseCase)
    use_case.execute.return_value = _make_program()
    return use_case


@pytest.fixture
def mock_active_program_none_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=GetActiveProgramUseCase)
    use_case.execute.return_value = None
    return use_case


@pytest.fixture
def mock_repository() -> AsyncMock:
    repo = AsyncMock(spec=SqlAlchemyWorkoutProgramRepository)
    repo.list_all.return_value = [
        _make_program(),
        _make_program(program_id="prog-uuid-5678", name="Treino XYZ", is_active=False),
    ]
    return repo


@pytest.fixture
def client_with_create_mock(mock_create_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_create_program_use_case] = lambda: mock_create_use_case
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_create_error_mock(mock_create_use_case_error: AsyncMock) -> None:
    app.dependency_overrides[get_create_program_use_case] = lambda: mock_create_use_case_error
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_active_mock(mock_active_program_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_active_program_use_case] = lambda: mock_active_program_use_case
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_active_none_mock(mock_active_program_none_use_case: AsyncMock) -> None:
    app.dependency_overrides[get_active_program_use_case] = lambda: mock_active_program_none_use_case
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_list_mock(mock_repository: AsyncMock) -> None:
    app.dependency_overrides[_get_repository] = lambda: mock_repository
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


# --------------- tests ---------------


@pytest.mark.anyio
async def test_create_program_returns_201(
    mock_create_use_case: AsyncMock, client_with_create_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/programs/", json=_VALID_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert "data" in body
    assert body["data"]["id"] == "prog-uuid-1234"
    assert body["data"]["name"] == "Treino ABC"
    assert body["data"]["is_active"] is True
    assert len(body["data"]["slots"]) == 1


@pytest.mark.anyio
async def test_create_program_invalid_returns_400(
    mock_create_use_case_error: AsyncMock, client_with_create_error_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/programs/",
            json={"name": "", "slots": []},
        )

    assert response.status_code == 400
    body = response.json()
    assert "error" in body


@pytest.mark.anyio
async def test_get_active_program_returns_200(
    mock_active_program_use_case: AsyncMock, client_with_active_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/programs/active")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"]["id"] == "prog-uuid-1234"
    assert body["data"]["is_active"] is True


@pytest.mark.anyio
async def test_get_active_program_returns_null_when_none(
    mock_active_program_none_use_case: AsyncMock, client_with_active_none_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/programs/active")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"] is None


@pytest.mark.anyio
async def test_list_programs_returns_200(
    mock_repository: AsyncMock, client_with_list_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/programs/")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert len(body["data"]) == 2
    assert body["data"][0]["name"] == "Treino ABC"
    assert body["data"][1]["name"] == "Treino XYZ"
