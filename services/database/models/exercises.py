import uuid

from sqlalchemy import Column, UUID, String, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped

from utils.clients.database.mixin_model import MixinModel


class ExercisesModel(MixinModel):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = Column(String(length=250), nullable=False)
    max_score: Mapped[int] = Column(Integer, nullable=True)
    min_score: Mapped[int] = Column(Integer, nullable=True)
    description: Mapped[str] = Column(Text, nullable=False)
    order_index: Mapped[int] = Column(Integer, nullable=False, default=0)
    estimated_time: Mapped[str] = Column(String(length=50), nullable=True)

    course_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )
