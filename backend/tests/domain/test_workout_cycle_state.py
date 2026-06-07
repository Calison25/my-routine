import pytest

from app.domain.workout_cycle_state import WorkoutCycleState


def test_next_slot_order_advances_circularly() -> None:
    state = WorkoutCycleState(current_slot_order=0)
    assert state.next_slot_order(total_slots=3) == 1

    state = WorkoutCycleState(current_slot_order=1)
    assert state.next_slot_order(total_slots=3) == 2


def test_next_slot_order_wraps_around() -> None:
    state = WorkoutCycleState(current_slot_order=2)
    assert state.next_slot_order(total_slots=3) == 0


def test_advance_updates_current_slot_order() -> None:
    state = WorkoutCycleState(current_slot_order=0)
    state.advance(total_slots=3)
    assert state.current_slot_order == 1


def test_next_slot_order_raises_when_no_slots() -> None:
    state = WorkoutCycleState(current_slot_order=0)
    with pytest.raises(ValueError, match="Programa não tem slots"):
        state.next_slot_order(total_slots=0)
