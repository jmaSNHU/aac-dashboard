# animal.py
# db model class for animal table

import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, ForeignKey, Float
from model.base import Base

class Animal(Base):
    __tablename__ = "animal"

    # map the fields to columns of the animal table
    # primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    age_upon_outcome: Mapped[str] = mapped_column(String(50))
    animal_id: Mapped[str] = mapped_column(String(50))
    # foreign key for animal_type
    animal_type_id: Mapped[int] = mapped_column(ForeignKey("animal_type.id"))
    # navigation links
    animal_type: Mapped["AnimalType"] = relationship(back_populates="animals")
    # foreign key for breed
    breed_id: Mapped[int] = mapped_column(ForeignKey("breed.id"))
    # navigation links
    breed: Mapped["Breed"] = relationship(back_populates="animals")
    color: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[str] = mapped_column(String(50))
    datetime: Mapped[str] = mapped_column(String(50))
    month_year: Mapped[datetime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String(50))
    outcome_subtype: Mapped[str] = mapped_column(String(50))
    # foreign key for outcome_type
    outcome_type_id: Mapped[int] = mapped_column(ForeignKey("outcome_type.id"))
    # navigation link
    outcome_type: Mapped["OutcomeType"] = relationship(back_populates="animals")
    # foreign key for sex_upon_outcome
    sex_upon_outcome_id: Mapped[int] = mapped_column(ForeignKey("sex_upon_outcome.id"))
    # navigation link
    sex_upon_outcome: Mapped["SexUponOutcome"] = relationship(back_populates="animals")
    location_lat: Mapped[float] = mapped_column(Float)
    location_long: Mapped[float] = mapped_column(Float)
    age_upon_outcome_in_weeks: Mapped[float] = mapped_column(Float)

    # string representation of an animal object
    # TODO: delete
    def __repr__(self) -> str:
        return f"{self.name!r}"
