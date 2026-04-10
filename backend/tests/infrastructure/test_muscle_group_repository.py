from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.muscle_group import MuscleGroup
from app.infrastructure.database.models import MuscleGroupModel
from app.infrastructure.database.muscle_group_repository_impl import (
    SqlAlchemyMuscleGroupRepository,
)


class TestSqlAlchemyMuscleGroupRepository:
    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def repository(
        self, mock_session: AsyncMock
    ) -> SqlAlchemyMuscleGroupRepository:
        return SqlAlchemyMuscleGroupRepository(session=mock_session)

    async def test_list_by_category_returns_muscle_groups(
        self, repository: SqlAlchemyMuscleGroupRepository, mock_session: AsyncMock
    ) -> None:
        model_1 = MagicMock(spec=MuscleGroupModel)
        model_1.id = 1
        model_1.name = "Peito"
        model_1.category_id = 1
        model_2 = MagicMock(spec=MuscleGroupModel)
        model_2.id = 2
        model_2.name = "Costas"
        model_2.category_id = 1

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_1, model_2]
        mock_session.execute.return_value = mock_result

        groups = await repository.list_by_category(category_id=1)

        assert len(groups) == 2
        assert isinstance(groups[0], MuscleGroup)
        assert groups[0].id == 1
        assert groups[0].name == "Peito"
        assert groups[0].category_id == 1
        assert groups[1].id == 2
        assert groups[1].name == "Costas"

    async def test_list_by_category_empty_returns_empty_list(
        self, repository: SqlAlchemyMuscleGroupRepository, mock_session: AsyncMock
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        groups = await repository.list_by_category(category_id=99)

        assert groups == []
