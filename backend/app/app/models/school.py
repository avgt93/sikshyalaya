from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class School(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=128), nullable=False)
    address = Column(String(length=64))
    department = relationship("Department", back_populates="school")
    __tablename__ = "school" # noqa