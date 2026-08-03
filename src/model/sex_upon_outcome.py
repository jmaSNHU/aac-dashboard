# sex_upon_outcome.py
# db model class for sex_upon_outcome table

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from model.base import Base

class SexUponOutcome(Base):
    __tablename__ = "sex_upon_outcome"

    # maps the fields to columns of the breed table
    id: Mapped[int] = mapped_column(primary_key=True)
    sex: Mapped[str] = mapped_column(String(25))

    # relationship / navigation links
    animals: Mapped[List["Animal"]] = relationship(back_populates="sex_upon_outcome")

    # string representation using the outcome_type field
    def __repr__(self) -> str:
        return f"{self.sex!r}"