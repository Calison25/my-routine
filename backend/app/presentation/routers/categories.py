from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.list_training_categories import ListTrainingCategoriesUseCase
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.training_category_repository_impl import (
    SqlAlchemyTrainingCategoryRepository,
)
from app.presentation.response import success_response

router = APIRouter(prefix="/api", tags=["categories"])


async def get_list_categories_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> ListTrainingCategoriesUseCase:
    repository = SqlAlchemyTrainingCategoryRepository(session)
    return ListTrainingCategoriesUseCase(repository)


@router.get("/categories")
async def list_categories(
    use_case: ListTrainingCategoriesUseCase = Depends(get_list_categories_use_case),
) -> dict:
    categories = await use_case.execute()
    return success_response(
        [{"id": c.id, "name": c.name} for c in categories]
    )
