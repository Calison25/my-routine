import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TrainingCategoryModel(Base):
    __tablename__ = "training_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    muscle_groups: Mapped[list["MuscleGroupModel"]] = relationship(
        back_populates="category"
    )
    workout_logs: Mapped[list["WorkoutLogModel"]] = relationship(
        back_populates="category"
    )


class MuscleGroupModel(Base):
    __tablename__ = "muscle_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_categories.id"), nullable=False
    )

    category: Mapped["TrainingCategoryModel"] = relationship(
        back_populates="muscle_groups"
    )
    workout_logs: Mapped[list["WorkoutLogModel"]] = relationship(
        back_populates="muscle_group"
    )


class WorkoutLogModel(Base):
    __tablename__ = "workout_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_categories.id"), nullable=False
    )
    muscle_group_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("muscle_groups.id"), nullable=True
    )
    done: Mapped[bool] = mapped_column(Boolean, nullable=False)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    category: Mapped["TrainingCategoryModel"] = relationship(
        back_populates="workout_logs"
    )
    muscle_group: Mapped["MuscleGroupModel | None"] = relationship(
        back_populates="workout_logs"
    )
