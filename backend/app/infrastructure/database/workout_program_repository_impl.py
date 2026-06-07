import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.workout_program import WorkoutProgram, WorkoutSlot, WorkoutSlotCategory
from app.domain.workout_program_repository import WorkoutProgramRepository
from app.infrastructure.database.models import (
    WorkoutProgramModel,
    WorkoutProgramSlotModel,
    WorkoutSlotCategoryModel,
)


class SqlAlchemyWorkoutProgramRepository(WorkoutProgramRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, program: WorkoutProgram) -> WorkoutProgram:
        model = WorkoutProgramModel(
            id=uuid.UUID(program.id),
            name=program.name,
            is_active=program.is_active,
            slots=[
                WorkoutProgramSlotModel(
                    id=uuid.UUID(slot.id),
                    slot_label=slot.slot_label,
                    slot_order=slot.slot_order,
                    categories=[
                        WorkoutSlotCategoryModel(
                            id=uuid.UUID(cat.id),
                            category_id=cat.category_id,
                            muscle_group_id=cat.muscle_group_id,
                        )
                        for cat in slot.categories
                    ],
                )
                for slot in program.slots
            ],
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model, attribute_names=["id", "name", "is_active", "created_at", "slots"])
        return self._to_domain(model)

    async def get_active(self) -> Optional[WorkoutProgram]:
        stmt = (
            select(WorkoutProgramModel)
            .where(WorkoutProgramModel.is_active.is_(True))
            .options(
                selectinload(WorkoutProgramModel.slots).selectinload(
                    WorkoutProgramSlotModel.categories
                ),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_domain(model)

    async def get_by_id(self, program_id: str) -> Optional[WorkoutProgram]:
        stmt = (
            select(WorkoutProgramModel)
            .where(WorkoutProgramModel.id == uuid.UUID(program_id))
            .options(
                selectinload(WorkoutProgramModel.slots).selectinload(
                    WorkoutProgramSlotModel.categories
                ),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_domain(model)

    async def deactivate_all(self) -> None:
        stmt = (
            update(WorkoutProgramModel)
            .where(WorkoutProgramModel.is_active.is_(True))
            .values(is_active=False)
        )
        await self._session.execute(stmt)

    async def list_all(self) -> list[WorkoutProgram]:
        stmt = (
            select(WorkoutProgramModel)
            .options(
                selectinload(WorkoutProgramModel.slots).selectinload(
                    WorkoutProgramSlotModel.categories
                ),
            )
            .order_by(WorkoutProgramModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    @staticmethod
    def _to_domain(model: WorkoutProgramModel) -> WorkoutProgram:
        return WorkoutProgram(
            id=str(model.id),
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
            slots=[
                WorkoutSlot(
                    id=str(slot.id),
                    program_id=str(model.id),
                    slot_label=slot.slot_label,
                    slot_order=slot.slot_order,
                    categories=[
                        WorkoutSlotCategory(
                            id=str(cat.id),
                            category_id=cat.category_id,
                            muscle_group_id=cat.muscle_group_id,
                        )
                        for cat in slot.categories
                    ],
                )
                for slot in model.slots
            ],
        )
