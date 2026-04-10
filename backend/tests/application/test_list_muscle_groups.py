from unittest.mock import AsyncMock

import pytest

from app.application.list_muscle_groups import ListMuscleGroupsUseCase
from app.domain.muscle_group import MuscleGroup
from app.domain.muscle_group_repository import MuscleGroupRepository
from app.domain.training_category import CategoryID


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock(spec=MuscleGroupRepository)


@pytest.mark.anyio
async def test_execute_with_musculacao_returns_groups(mock_repo: AsyncMock) -> None:
    groups = [
        MuscleGroup(id=1, name="Peito", category_id=CategoryID.MUSCULACAO),
        MuscleGroup(id=2, name="Costas", category_id=CategoryID.MUSCULACAO),
    ]
    mock_repo.list_by_category.return_value = groups

    use_case = ListMuscleGroupsUseCase(repository=mock_repo)
    result = await use_case.execute(category_id=CategoryID.MUSCULACAO)

    assert result == groups
    mock_repo.list_by_category.assert_awaited_once_with(CategoryID.MUSCULACAO)


@pytest.mark.anyio
async def test_execute_with_cardio_returns_empty(mock_repo: AsyncMock) -> None:
    mock_repo.list_by_category.return_value = []

    use_case = ListMuscleGroupsUseCase(repository=mock_repo)
    result = await use_case.execute(category_id=CategoryID.CARDIO)

    assert result == []
    mock_repo.list_by_category.assert_awaited_once_with(CategoryID.CARDIO)
