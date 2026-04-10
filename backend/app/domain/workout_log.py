import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.domain.training_category import CategoryID


@dataclass
class WorkoutLog:
    date: date
    category_id: int
    done: bool
    muscle_group_id: Optional[int] = None
    duration_minutes: Optional[int] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def validate(self) -> None:
        if self.category_id == CategoryID.MUSCULACAO and self.muscle_group_id is None:
            raise ValueError("Grupo muscular é obrigatório para Musculação")
        if self.category_id != CategoryID.MUSCULACAO and self.muscle_group_id is not None:
            raise ValueError("Grupo muscular só é permitido para Musculação")
        if self.duration_minutes is not None and self.duration_minutes <= 0:
            raise ValueError("Duração deve ser maior que zero")
