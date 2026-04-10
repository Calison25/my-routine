from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.get_workout_calendar import GetWorkoutCalendarUseCase
from app.application.list_workouts_by_date import ListWorkoutsByDateUseCase
from app.application.register_workout import RegisterWorkoutUseCase
from app.domain.workout_log import WorkoutLog
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.workout_log_repository_impl import (
    SqlAlchemyWorkoutLogRepository,
)
from app.presentation.response import error_response, success_response

router = APIRouter(prefix="/api", tags=["workouts"])


class CreateWorkoutRequest(BaseModel):
    date: date
    category_id: int
    muscle_group_ids: Optional[list[int]] = None
    done: bool
    duration_minutes: Optional[int] = None


async def _get_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyWorkoutLogRepository:
    return SqlAlchemyWorkoutLogRepository(session)


async def get_register_workout_use_case(
    repo: SqlAlchemyWorkoutLogRepository = Depends(_get_repository),
) -> RegisterWorkoutUseCase:
    return RegisterWorkoutUseCase(repo)


async def get_get_workout_calendar_use_case(
    repo: SqlAlchemyWorkoutLogRepository = Depends(_get_repository),
) -> GetWorkoutCalendarUseCase:
    return GetWorkoutCalendarUseCase(repo)


async def get_list_workouts_use_case(
    repo: SqlAlchemyWorkoutLogRepository = Depends(_get_repository),
) -> ListWorkoutsByDateUseCase:
    return ListWorkoutsByDateUseCase(repo)


@router.post("/workouts", status_code=201)
async def create_workout(
    request: CreateWorkoutRequest,
    use_case: RegisterWorkoutUseCase = Depends(get_register_workout_use_case),
) -> dict:
    try:
        ids: list[str] = []
        group_ids = request.muscle_group_ids or [None]

        for gid in group_ids:
            log = WorkoutLog(
                date=request.date,
                category_id=request.category_id,
                muscle_group_id=gid,
                done=request.done,
                duration_minutes=request.duration_minutes,
            )
            created = await use_case.execute(log)
            ids.append(created.id)

        return success_response({"ids": ids})
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content=error_response(str(exc)),
        )


@router.get("/workouts")
async def list_workouts(
    target_date: date,
    use_case: ListWorkoutsByDateUseCase = Depends(get_list_workouts_use_case),
) -> dict:
    details = await use_case.execute(target_date)
    return success_response([
        {
            "id": d.id,
            "date": d.date.isoformat(),
            "category_id": d.category_id,
            "category_name": d.category_name,
            "muscle_group_id": d.muscle_group_id,
            "muscle_group_name": d.muscle_group_name,
            "done": d.done,
            "duration_minutes": d.duration_minutes,
        }
        for d in details
    ])


@router.get("/workouts/calendar")
async def get_workout_calendar(
    month: int,
    year: int,
    use_case: GetWorkoutCalendarUseCase = Depends(get_get_workout_calendar_use_case),
) -> dict:
    try:
        days = await use_case.execute(month, year)
        return success_response(
            {
                "days": [
                    {
                        "date": d.date.isoformat(),
                        "done": d.done,
                        "count": d.count,
                    }
                    for d in days
                ]
            }
        )
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content=error_response(str(exc)),
        )
