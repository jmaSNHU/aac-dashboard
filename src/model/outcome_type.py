# outcome_type.py
# db model class for outcome_type table

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from model.base import Base

class OutcomeType(Base):
    __tablename__ = "outcome_type"

    # maps the fields to columns of the breed table
    id: Mapped[int] = mapped_column(primary_key=True)
    outcome_type: Mapped[str] = mapped_column(String(25))

    # relationship / navigation links
    animals: Mapped[List["Animal"]] = relationship(back_populates="outcome_type")

    # string representation using the outcome_type field
    def __repr__(self) -> str:
        return f"{self.outcome_type!r}"