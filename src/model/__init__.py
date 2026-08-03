# model/__init__.py
# model aggregate

from model.animal import Animal
from model.animal_type import AnimalType
from model.breed import Breed
from model.outcome_type import OutcomeType
from model.sex_upon_outcome import SexUponOutcome

# imports alls models so SQLAlchemy can register them with the Base type
__all__ = ["Animal", "AnimalType", "Breed", "OutcomeType", "SexUponOutcome"]
