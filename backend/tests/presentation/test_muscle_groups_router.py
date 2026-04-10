from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.application.list_muscle_groups import ListMuscleGroupsUseCase
from app.domain.muscle_group import MuscleGroup
from app.main import app
from app.presentation.routers.muscle_groups import get_list_muscle_groups_use_case


@pytest.fixture
def mock_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=ListMuscleGroupsUseCase)
    use_case.execute.return_value = [
        MuscleGroup(id=1, name="Peito", category_id=1),
        MuscleGroup(id=2, name="Costas", category_id=1),
    ]
    return use_case


@pytest.fixture
def mock_empty_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=ListMuscleGroupsUseCase)
    use_case.execute.return_value = []
    return use_case


@pytest.fixture
def client_with_mock(mock_use_case: AsyncMock) -> AsyncClient:
    app.dependency_overrides[get_list_muscle_groups_use_case] = lambda: mock_use_case
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_empty_mock(mock_empty_use_case: AsyncMock) -> AsyncClient:
    app.dependency_overrides[get_list_muscle_groups_use_case] = lambda: mock_empty_use_case
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_list_muscle_groups_returns_200(
    mock_use_case: AsyncMock, client_with_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/categories/1/muscle-groups")

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert len(body["data"]) == 2
    assert body["data"][0] == {"id": 1, "name": "Peito", "categoryId": 1}


@pytest.mark.anyio
async def test_list_muscle_groups_empty_returns_empty_data(
    mock_empty_use_case: AsyncMock, client_with_empty_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/categories/1/muscle-groups")

    assert response.status_code == 200
    body = response.json()
    assert body == {"data": []}
