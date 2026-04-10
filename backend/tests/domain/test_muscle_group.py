import pytest

from app.domain.muscle_group import MuscleGroup
from app.domain.training_category import CategoryID


class TestMuscleGroup:
    def test_create_valid_muscle_group(self) -> None:
        group = MuscleGroup(id=1, name="Peito", category_id=CategoryID.MUSCULACAO)

        assert group.id == 1
        assert group.name == "Peito"
        assert group.category_id == CategoryID.MUSCULACAO
        group.validate()

    def test_muscle_group_with_empty_name_raises_error(self) -> None:
        group = MuscleGroup(id=1, name="", category_id=CategoryID.MUSCULACAO)

        with pytest.raises(ValueError, match="Nome do grupo muscular não pode ser vazio"):
            group.validate()

        group_spaces = MuscleGroup(id=2, name="   ", category_id=CategoryID.MUSCULACAO)

        with pytest.raises(ValueError, match="Nome do grupo muscular não pode ser vazio"):
            group_spaces.validate()

    def test_muscle_group_with_wrong_category_raises_error(self) -> None:
        group = MuscleGroup(id=1, name="Peito", category_id=CategoryID.CARDIO)

        with pytest.raises(
            ValueError,
            match="Grupo muscular só pode pertencer à categoria Musculação",
        ):
            group.validate()

    def test_muscle_group_belongs_to_musculacao(self) -> None:
        group = MuscleGroup(id=1, name="Costas", category_id=CategoryID.MUSCULACAO)

        group.validate()
        assert group.category_id == CategoryID.MUSCULACAO
