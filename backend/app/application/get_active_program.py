from typing import Optional

from app.domain.workout_program import WorkoutProgram
from app.domain.workout_program_repository import WorkoutProgramRepository


class GetActiveProgramUseCase:
    def __init__(self, repository: WorkoutProgramRepository) -> None:
        self._repository = repository

    async def execute(self) -> Optional[WorkoutProgram]:
        return await self._repository.get_active()
