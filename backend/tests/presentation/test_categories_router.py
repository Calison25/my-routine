from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.application.list_training_categories import ListTrainingCategoriesUseCase
from app.domain.training_category import TrainingCategory
from app.infrastructure.database.connection import get_db_session
from app.main import app
from app.presentation.routers.categories import get_list_categories_use_case


@pytest.fixture
def mock_use_case() -> AsyncMock:
    use_case = AsyncMock(spec=ListTrainingCategoriesUseCase)
    use_case.execute.return_value = [
        TrainingCategory(id=1, name="Musculação"),
        TrainingCategory(id=2, name="Cardio"),
    ]
    return use_case


@pytest.fixture
def client_with_mock(mock_use_case: AsyncMock) -> AsyncClient:
    app.dependency_overrides[get_list_categories_use_case] = lambda: mock_use_case
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_list_categories_returns_200(
    mock_use_case: AsyncMock, client_with_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/categories")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_list_categories_returns_data_format(
    mock_use_case: AsyncMock, client_with_mock: None
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/categories")

    body = response.json()
    assert "data" in body
    assert len(body["data"]) == 2
    assert body["data"][0] == {"id": 1, "name": "Musculação"}
    assert body["data"][1] == {"id": 2, "name": "Cardio"}
