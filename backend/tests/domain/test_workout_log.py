from datetime import date

import pytest

from app.domain.training_category import CategoryID
from app.domain.workout_log import WorkoutLog


class TestWorkoutLog:
    def test_create_valid_musculacao_workout(self) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.MUSCULACAO,
            done=True,
            muscle_group_id=1,
        )

        log.validate()
        assert log.date == date(2026, 4, 9)
        assert log.category_id == CategoryID.MUSCULACAO
        assert log.done is True
        assert log.muscle_group_id == 1
        assert log.id is not None

    def test_create_valid_cardio_workout(self) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.CARDIO,
            done=True,
        )

        log.validate()
        assert log.category_id == CategoryID.CARDIO
        assert log.muscle_group_id is None

    def test_musculacao_without_muscle_group_raises_error(self) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.MUSCULACAO,
            done=True,
            muscle_group_id=None,
        )

        with pytest.raises(
            ValueError, match="Grupo muscular é obrigatório para Musculação"
        ):
            log.validate()

    def test_cardio_with_muscle_group_raises_error(self) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.CARDIO,
            done=True,
            muscle_group_id=1,
        )

        with pytest.raises(
            ValueError, match="Grupo muscular só é permitido para Musculação"
        ):
            log.validate()

    def test_negative_duration_raises_error(self) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.CARDIO,
            done=True,
            duration_minutes=-5,
        )

        with pytest.raises(ValueError, match="Duração deve ser maior que zero"):
            log.validate()

        log_zero = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.CARDIO,
            done=True,
            duration_minutes=0,
        )

        with pytest.raises(ValueError, match="Duração deve ser maior que zero"):
            log_zero.validate()

    def test_valid_workout_with_duration(self) -> None:
        log = WorkoutLog(
            date=date(2026, 4, 9),
            category_id=CategoryID.CARDIO,
            done=True,
            duration_minutes=45,
        )

        log.validate()
        assert log.duration_minutes == 45
