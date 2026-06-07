import os

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.list_muscle_groups import ListMuscleGroupsUseCase
from app.application.list_training_categories import ListTrainingCategoriesUseCase
from app.infrastructure.ai.claude_program_generator import ProgramGeneratorService
from app.infrastructure.ai.whisper_transcription_service import (
    AudioTranscriptionService,
)
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.muscle_group_repository_impl import (
    SqlAlchemyMuscleGroupRepository,
)
from app.infrastructure.database.training_category_repository_impl import (
    SqlAlchemyTrainingCategoryRepository,
)
from app.presentation.response import error_response, success_response

router = APIRouter(prefix="/api/ai", tags=["ai"])


class GenerateProgramRequest(BaseModel):
    transcription: str


async def get_transcription_service() -> AudioTranscriptionService:
    api_key = os.getenv("OPENAI_API_KEY", "")
    return AudioTranscriptionService(api_key=api_key)


async def get_program_generator_service() -> ProgramGeneratorService:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    return ProgramGeneratorService(api_key=api_key)


async def get_categories_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> ListTrainingCategoriesUseCase:
    repository = SqlAlchemyTrainingCategoryRepository(session)
    return ListTrainingCategoriesUseCase(repository)


async def get_muscle_groups_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> ListMuscleGroupsUseCase:
    repository = SqlAlchemyMuscleGroupRepository(session)
    return ListMuscleGroupsUseCase(repository)


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    service: AudioTranscriptionService = Depends(get_transcription_service),
) -> dict:
    try:
        audio_bytes = await file.read()
        filename = file.filename or "audio.webm"
        text = await service.transcribe(audio_bytes, filename)
        return success_response({"text": text})
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=error_response(f"Erro na transcrição: {exc}"),
        )


@router.post("/generate-program")
async def generate_program(
    body: GenerateProgramRequest,
    generator: ProgramGeneratorService = Depends(get_program_generator_service),
    categories_use_case: ListTrainingCategoriesUseCase = Depends(
        get_categories_use_case
    ),
    muscle_groups_use_case: ListMuscleGroupsUseCase = Depends(
        get_muscle_groups_use_case
    ),
) -> dict:
    try:
        categories = await categories_use_case.execute()
        categories_data = [{"id": c.id, "name": c.name} for c in categories]

        all_muscle_groups: list[dict[str, object]] = []
        for cat in categories:
            groups = await muscle_groups_use_case.execute(cat.id)
            for g in groups:
                all_muscle_groups.append(
                    {"id": g.id, "name": g.name, "category_id": g.category_id}
                )

        program = await generator.generate(
            transcription=body.transcription,
            categories=categories_data,
            muscle_groups=all_muscle_groups,
        )
        return success_response(program)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=error_response(f"Erro ao gerar programa: {exc}"),
        )
