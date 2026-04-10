import calendar
from dataclasses import dataclass
from datetime import date

from app.domain.workout_log_repository import WorkoutLogRepository


@dataclass(frozen=True)
class CalendarDay:
    date: date
    done: bool
    count: int


class GetWorkoutCalendarUseCase:
    def __init__(self, repository: WorkoutLogRepository) -> None:
        self._repository = repository

    async def execute(self, month: int, year: int) -> list[CalendarDay]:
        if month < 1 or month > 12:
            raise ValueError("Mês deve estar entre 1 e 12")
        if year < 1:
            raise ValueError("Ano deve ser positivo")

        _, last_day = calendar.monthrange(year, month)
        start = date(year, month, 1)
        end = date(year, month, last_day)

        logs = await self._repository.get_by_date_range(start, end)

        logs_by_date: dict[date, list[object]] = {}
        for log in logs:
            logs_by_date.setdefault(log.date, []).append(log)

        days: list[CalendarDay] = []
        for day_num in range(1, last_day + 1):
            current_date = date(year, month, day_num)
            day_logs = logs_by_date.get(current_date, [])
            done = any(getattr(log, "done", False) for log in day_logs)
            days.append(
                CalendarDay(
                    date=current_date,
                    done=done,
                    count=len(day_logs),
                )
            )

        return days
