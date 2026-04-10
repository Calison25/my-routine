from app.domain.workout_log import WorkoutLog
from app.domain.workout_log_repository import WorkoutLogRepository


class RegisterWorkoutUseCase:
    def __init__(self, repository: WorkoutLogRepository) -> None:
        self._repository = repository

    async def execute(self, log: WorkoutLog) -> WorkoutLog:
        log.validate()
        return await self._repository.create(log)
