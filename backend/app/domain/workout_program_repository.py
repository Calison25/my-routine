from abc import ABC, abstractmethod
from typing import Optional

from app.domain.workout_program import WorkoutProgram


class WorkoutProgramRepository(ABC):
    @abstractmethod
    async def create(self, program: WorkoutProgram) -> WorkoutProgram: ...

    @abstractmethod
    async def get_active(self) -> Optional[WorkoutProgram]: ...

    @abstractmethod
    async def get_by_id(self, program_id: str) -> Optional[WorkoutProgram]: ...

    @abstractmethod
    async def deactivate_all(self) -> None: ...

    @abstractmethod
    async def list_all(self) -> list[WorkoutProgram]: ...
