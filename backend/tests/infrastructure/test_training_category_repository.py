from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.training_category import TrainingCategory
from app.infrastructure.database.models import TrainingCategoryModel
from app.infrastructure.database.training_category_repository_impl import (
    SqlAlchemyTrainingCategoryRepository,
)


class TestSqlAlchemyTrainingCategoryRepository:
    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def repository(
        self, mock_session: AsyncMock
    ) -> SqlAlchemyTrainingCategoryRepository:
        return SqlAlchemyTrainingCategoryRepository(session=mock_session)

    async def test_list_all_returns_categories(
        self, repository: SqlAlchemyTrainingCategoryRepository, mock_session: AsyncMock
    ) -> None:
        model_1 = MagicMock(spec=TrainingCategoryModel)
        model_1.id = 1
        model_1.name = "Musculação"
        model_2 = MagicMock(spec=TrainingCategoryModel)
        model_2.id = 2
        model_2.name = "Cardio"

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_1, model_2]
        mock_session.execute.return_value = mock_result

        categories = await repository.list_all()

        assert len(categories) == 2
        assert isinstance(categories[0], TrainingCategory)
        assert categories[0].id == 1
        assert categories[0].name == "Musculação"
        assert categories[1].id == 2
        assert categories[1].name == "Cardio"

    async def test_list_all_empty_returns_empty_list(
        self, repository: SqlAlchemyTrainingCategoryRepository, mock_session: AsyncMock
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        categories = await repository.list_all()

        assert categories == []
