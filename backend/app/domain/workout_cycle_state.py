from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkoutCycleState:
    current_slot_order: int = 0
    program_id: Optional[str] = None

    def next_slot_order(self, total_slots: int) -> int:
        if total_slots == 0:
            raise ValueError("Programa não tem slots")
        return (self.current_slot_order + 1) % total_slots

    def advance(self, total_slots: int) -> None:
        self.current_slot_order = self.next_slot_order(total_slots)
