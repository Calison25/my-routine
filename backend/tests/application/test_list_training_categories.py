from unittest.mock import AsyncMock

import pytest

from app.application.list_training_categories import ListTrainingCategoriesUseCase
from app.domain.training_category import TrainingCategory
from app.domain.training_category_repository import TrainingCategoryRepository


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock(spec=TrainingCategoryRepository)


@pytest.mark.anyio
async def test_execute_returns_categories_as_dtos(mock_repo: AsyncMock) -> None:
    categories = [
        TrainingCategory(id=1, name="Musculação"),
        TrainingCategory(id=2, name="Cardio"),
    ]
    mock_repo.list_all.return_value = categories

    use_case = ListTrainingCategoriesUseCase(repository=mock_repo)
    result = await use_case.execute()

    assert result == categories
    mock_repo.list_all.assert_awaited_once()


@pytest.mark.anyio
async def test_execute_empty_returns_empty_list(mock_repo: AsyncMock) -> None:
    mock_repo.list_all.return_value = []

    use_case = ListTrainingCategoriesUseCase(repository=mock_repo)
    result = await use_case.execute()

    assert result == []
    mock_repo.list_all.assert_awaited_once()
