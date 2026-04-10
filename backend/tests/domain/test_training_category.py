import pytest

from app.domain.training_category import CategoryID, TrainingCategory


class TestTrainingCategory:
    def test_create_valid_category(self) -> None:
        category = TrainingCategory(id=1, name="Musculação")

        assert category.id == 1
        assert category.name == "Musculação"
        category.validate()

    def test_category_with_empty_name_raises_error(self) -> None:
        category = TrainingCategory(id=1, name="")

        with pytest.raises(ValueError, match="Nome da categoria não pode ser vazio"):
            category.validate()

        category_spaces = TrainingCategory(id=2, name="   ")

        with pytest.raises(ValueError, match="Nome da categoria não pode ser vazio"):
            category_spaces.validate()

    def test_category_ids_are_defined(self) -> None:
        assert CategoryID.MUSCULACAO == 1
        assert CategoryID.CARDIO == 2
        assert CategoryID.PILATES == 3
