import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.domain.workout_program import WorkoutProgram, WorkoutSlot, WorkoutSlotCategory
from app.infrastructure.database.models import (
    WorkoutProgramModel,
    WorkoutProgramSlotModel,
    WorkoutSlotCategoryModel,
)
from app.infrastructure.database.workout_program_repository_impl import (
    SqlAlchemyWorkoutProgramRepository,
)


class TestSqlAlchemyWorkoutProgramRepository:
    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def repository(
        self, mock_session: AsyncMock
    ) -> SqlAlchemyWorkoutProgramRepository:
        return SqlAlchemyWorkoutProgramRepository(session=mock_session)

    async def test_create_program_persists_with_slots_and_categories(
        self,
        repository: SqlAlchemyWorkoutProgramRepository,
        mock_session: AsyncMock,
    ) -> None:
        program = WorkoutProgram(
            name="Treino ABC",
            is_active=True,
            slots=[
                WorkoutSlot(
                    program_id="ignored",
                    slot_label="A",
                    slot_order=0,
                    categories=[
                        WorkoutSlotCategory(category_id=1, muscle_group_id=1),
                        WorkoutSlotCategory(category_id=1, muscle_group_id=2),
                    ],
                ),
                WorkoutSlot(
                    program_id="ignored",
                    slot_label="B",
                    slot_order=1,
                    categories=[
                        WorkoutSlotCategory(category_id=2),
                    ],
                ),
            ],
        )

        captured_model: list[WorkoutProgramModel] = []

        def fake_add(model: WorkoutProgramModel) -> None:
            captured_model.append(model)

        async def fake_flush() -> None:
            pass

        refreshed_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        async def fake_refresh(model: object, attribute_names: list[str] | None = None) -> None:
            pass

        mock_session.add = MagicMock(side_effect=fake_add)
        mock_session.flush = AsyncMock(side_effect=fake_flush)
        mock_session.refresh = AsyncMock(side_effect=fake_refresh)

        result = await repository.create(program)

        assert isinstance(result, WorkoutProgram)
        mock_session.add.assert_called_once()
        mock_session.flush.assert_awaited_once()
        mock_session.refresh.assert_awaited_once()

        added_model = captured_model[0]
        assert isinstance(added_model, WorkoutProgramModel)
        assert added_model.name == "Treino ABC"
        assert added_model.is_active is True
        assert len(added_model.slots) == 2
        assert added_model.slots[0].slot_label == "A"
        assert added_model.slots[0].slot_order == 0
        assert len(added_model.slots[0].categories) == 2
        assert added_model.slots[1].slot_label == "B"
        assert len(added_model.slots[1].categories) == 1

        assert result.name == "Treino ABC"
        assert result.is_active is True
        assert len(result.slots) == 2

    async def test_get_active_returns_active_program(
        self,
        repository: SqlAlchemyWorkoutProgramRepository,
        mock_session: AsyncMock,
    ) -> None:
        program_id = uuid.uuid4()
        slot_id = uuid.uuid4()
        cat_entry_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        cat_model = MagicMock(spec=WorkoutSlotCategoryModel)
        cat_model.id = cat_entry_id
        cat_model.slot_id = slot_id
        cat_model.category_id = 1
        cat_model.muscle_group_id = 3

        slot_model = MagicMock(spec=WorkoutProgramSlotModel)
        slot_model.id = slot_id
        slot_model.program_id = program_id
        slot_model.slot_label = "A"
        slot_model.slot_order = 0
        slot_model.categories = [cat_model]

        program_model = MagicMock(spec=WorkoutProgramModel)
        program_model.id = program_id
        program_model.name = "Treino Ativo"
        program_model.is_active = True
        program_model.created_at = now
        program_model.slots = [slot_model]

        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = program_model
        mock_session.execute.return_value = mock_result

        result = await repository.get_active()

        assert result is not None
        assert isinstance(result, WorkoutProgram)
        assert result.id == str(program_id)
        assert result.name == "Treino Ativo"
        assert result.is_active is True
        assert len(result.slots) == 1
        assert result.slots[0].slot_label == "A"
        assert len(result.slots[0].categories) == 1
        assert result.slots[0].categories[0].category_id == 1
        assert result.slots[0].categories[0].muscle_group_id == 3

    async def test_get_active_returns_none_when_no_active(
        self,
        repository: SqlAlchemyWorkoutProgramRepository,
        mock_session: AsyncMock,
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repository.get_active()

        assert result is None

    async def test_deactivate_all_clears_active_flag(
        self,
        repository: SqlAlchemyWorkoutProgramRepository,
        mock_session: AsyncMock,
    ) -> None:
        mock_session.execute = AsyncMock()

        await repository.deactivate_all()

        mock_session.execute.assert_awaited_once()
        stmt = mock_session.execute.call_args[0][0]
        compiled = stmt.compile(compile_kwargs={"literal_binds": True})
        sql_text = str(compiled)
        assert "workout_programs" in sql_text
        assert "is_active" in sql_text
