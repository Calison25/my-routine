from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.list_muscle_groups import ListMuscleGroupsUseCase
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.muscle_group_repository_impl import (
    SqlAlchemyMuscleGroupRepository,
)
from app.presentation.response import success_response

router = APIRouter(prefix="/api", tags=["muscle_groups"])


async def get_list_muscle_groups_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> ListMuscleGroupsUseCase:
    repository = SqlAlchemyMuscleGroupRepository(session)
    return ListMuscleGroupsUseCase(repository)


@router.get("/categories/{category_id}/muscle-groups")
async def list_muscle_groups(
    category_id: int,
    use_case: ListMuscleGroupsUseCase = Depends(get_list_muscle_groups_use_case),
) -> dict:
    groups = await use_case.execute(category_id)
    return success_response(
        [{"id": g.id, "name": g.name, "categoryId": g.category_id} for g in groups]
    )
