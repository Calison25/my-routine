from dataclasses import dataclass

from app.domain.training_category import CategoryID


@dataclass(frozen=True)
class MuscleGroup:
    id: int
    name: str
    category_id: int

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Nome do grupo muscular não pode ser vazio")
        if self.category_id != CategoryID.MUSCULACAO:
            raise ValueError(
                "Grupo muscular só pode pertencer à categoria Musculação"
            )
