from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.create_workout_program import (
    CreateWorkoutProgramInput,
    CreateWorkoutProgramUseCase,
    SlotCategoryInput,
    SlotInput,
)
from app.application.get_active_program import GetActiveProgramUseCase
from app.domain.workout_program import WorkoutProgram
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.workout_program_repository_impl import (
    SqlAlchemyWorkoutProgramRepository,
)
from app.presentation.response import error_response, success_response

router = APIRouter(prefix="/api/programs", tags=["programs"])


# --------------- Pydantic schemas ---------------


class SlotCategoryRequest(BaseModel):
    category_id: int
    muscle_group_id: Optional[int] = None


class SlotRequest(BaseModel):
    slot_label: str
    categories: list[SlotCategoryRequest]


class CreateProgramRequest(BaseModel):
    name: str
    slots: list[SlotRequest]


# --------------- Dependencies ---------------


async def _get_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyWorkoutProgramRepository:
    return SqlAlchemyWorkoutProgramRepository(session)


async def get_create_program_use_case(
    repo: SqlAlchemyWorkoutProgramRepository = Depends(_get_repository),
) -> CreateWorkoutProgramUseCase:
    return CreateWorkoutProgramUseCase(repo)


async def get_active_program_use_case(
    repo: SqlAlchemyWorkoutProgramRepository = Depends(_get_repository),
) -> GetActiveProgramUseCase:
    return GetActiveProgramUseCase(repo)


# --------------- Helpers ---------------


def _serialize_program(program: WorkoutProgram) -> dict:
    return {
        "id": program.id,
        "name": program.name,
        "is_active": program.is_active,
        "created_at": program.created_at.isoformat() if program.created_at else None,
        "slots": [
            {
                "id": slot.id,
                "slot_label": slot.slot_label,
                "slot_order": slot.slot_order,
                "categories": [
                    {
                        "id": cat.id,
                        "category_id": cat.category_id,
                        "muscle_group_id": cat.muscle_group_id,
                    }
                    for cat in slot.categories
                ],
            }
            for slot in program.slots
        ],
    }


# --------------- Endpoints ---------------


@router.post("/", status_code=201)
async def create_program(
    request: CreateProgramRequest,
    use_case: CreateWorkoutProgramUseCase = Depends(get_create_program_use_case),
) -> dict:
    try:
        input_data = CreateWorkoutProgramInput(
            name=request.name,
            slots=[
                SlotInput(
                    slot_label=s.slot_label,
                    categories=[
                        SlotCategoryInput(
                            category_id=c.category_id,
                            muscle_group_id=c.muscle_group_id,
                        )
                        for c in s.categories
                    ],
                )
                for s in request.slots
            ],
        )
        program = await use_case.execute(input_data)
        return success_response(_serialize_program(program))
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content=error_response(str(exc)),
        )


@router.get("/active")
async def get_active_program(
    use_case: GetActiveProgramUseCase = Depends(get_active_program_use_case),
) -> dict:
    program = await use_case.execute()
    if program is None:
        return success_response(None)
    return success_response(_serialize_program(program))


@router.get("/")
async def list_programs(
    repo: SqlAlchemyWorkoutProgramRepository = Depends(_get_repository),
) -> dict:
    programs = await repo.list_all()
    return success_response([_serialize_program(p) for p in programs])
