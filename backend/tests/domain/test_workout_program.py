import pytest

from app.domain.workout_program import (
    WorkoutProgram,
    WorkoutSlot,
    WorkoutSlotCategory,
)


class TestWorkoutProgram:
    def test_validate_program_with_empty_name_raises_error(self) -> None:
        slot = WorkoutSlot(
            program_id="prog-1",
            slot_label="A",
            slot_order=1,
            categories=[WorkoutSlotCategory(category_id=1)],
        )
        program = WorkoutProgram(name="", slots=[slot])

        with pytest.raises(
            ValueError, match="Nome do programa não pode ser vazio"
        ):
            program.validate()

        program_spaces = WorkoutProgram(name="   ", slots=[slot])

        with pytest.raises(
            ValueError, match="Nome do programa não pode ser vazio"
        ):
            program_spaces.validate()

    def test_validate_program_with_no_slots_raises_error(self) -> None:
        program = WorkoutProgram(name="Treino Push/Pull", slots=[])

        with pytest.raises(
            ValueError, match="Programa deve ter ao menos um slot"
        ):
            program.validate()

    def test_validate_slot_with_no_categories_raises_error(self) -> None:
        slot = WorkoutSlot(
            program_id="prog-1",
            slot_label="A",
            slot_order=1,
            categories=[],
        )
        program = WorkoutProgram(name="Treino Push/Pull", slots=[slot])

        with pytest.raises(
            ValueError, match="Slot deve ter ao menos uma categoria"
        ):
            program.validate()

    def test_activate_sets_is_active_true(self) -> None:
        program = WorkoutProgram(name="Treino ABC", is_active=False)

        program.activate()

        assert program.is_active is True

    def test_deactivate_sets_is_active_false(self) -> None:
        program = WorkoutProgram(name="Treino ABC", is_active=True)

        program.deactivate()

        assert program.is_active is False

    def test_valid_program_does_not_raise(self) -> None:
        slot = WorkoutSlot(
            program_id="prog-1",
            slot_label="A",
            slot_order=1,
            categories=[
                WorkoutSlotCategory(category_id=1, muscle_group_id=3),
                WorkoutSlotCategory(category_id=2),
            ],
        )
        program = WorkoutProgram(
            name="Treino Push/Pull/Legs",
            slots=[slot],
        )

        program.validate()

        assert program.name == "Treino Push/Pull/Legs"
        assert program.is_active is False
        assert program.id is not None
        assert program.created_at is None
        assert len(program.slots) == 1
        assert program.slots[0].slot_label == "A"
        assert len(program.slots[0].categories) == 2
