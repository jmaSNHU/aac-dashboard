# breed.py
# db model class for breed table

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from model.base import Base

class Breed(Base):
    __tablename__ = "breed"

    # maps the fields to columns of the breed table
    id: Mapped[int] = mapped_column(primary_key=True)
    breed_name: Mapped[str] = mapped_column(String(100))

    # relationship / navigation links
    animals: Mapped[List["Animal"]] = relationship(back_populates="breed")

    # string representation using the breed_name field
    def __repr__(self) -> str:
        return f"{self.breed_name!r}"