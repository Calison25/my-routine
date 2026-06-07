import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class WorkoutSlotCategory:
    category_id: int
    muscle_group_id: Optional[int] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class WorkoutSlot:
    program_id: str
    slot_label: str
    slot_order: int
    categories: list[WorkoutSlotCategory] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def validate(self) -> None:
        if not self.categories:
            raise ValueError("Slot deve ter ao menos uma categoria")


@dataclass
class WorkoutProgram:
    name: str
    slots: list[WorkoutSlot] = field(default_factory=list)
    is_active: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[datetime] = None

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Nome do programa não pode ser vazio")
        if not self.slots:
            raise ValueError("Programa deve ter ao menos um slot")
        for slot in self.slots:
            slot.validate()

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
