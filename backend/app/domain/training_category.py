from dataclasses import dataclass
from enum import IntEnum


class CategoryID(IntEnum):
    MUSCULACAO = 1
    CARDIO = 2
    PILATES = 3


@dataclass(frozen=True)
class TrainingCategory:
    id: int
    name: str

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Nome da categoria não pode ser vazio")
