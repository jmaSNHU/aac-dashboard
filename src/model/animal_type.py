# animal_type.py
# db model class for animal_type


from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from model.base import Base


class AnimalType(Base):
    __tablename__ = "animal_type"

    # map the fields to columns of the animal_type table
    id: Mapped[int] = mapped_column(primary_key=True)
    animal_type: Mapped[str] = mapped_column(String(25))

    # relationship / navigation links
    animals: Mapped[List["Animal"]] = relationship(back_populates="animal_type")

    # string representation using the animal_type field
    def __repr__(self) -> str:
        return f"{self.animal_type!r}"