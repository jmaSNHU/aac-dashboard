from model.base import Base
from database import engine, SessionLocal
import model
from crud_module import AnimalShelter
from sqlalchemy import select

def init_db():
    """Build all registered database structures."""
    print("Building schema metadata structures...")
    Base.metadata.create_all(bind=engine)

def main():
    init_db()

    db = SessionLocal()

    try:
        queried_animal = db.query(model.Animal).filter_by(id="100").first()
        print(f"Animal: {queried_animal}")
        print(f"Breed: {queried_animal.breed}")

        stmt = select(model.Animal).where(
            model.Animal.breed.has(
                model.Breed.breed_name
                .in_(["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"])),
            model.Animal.age_upon_outcome_in_weeks >= 26.00,
            model.Animal.age_upon_outcome_in_weeks <= 156.00,
            model.Animal.sex_upon_outcome.has(
                model.SexUponOutcome.sex == "Intact Female"
            )
        )
        animals_list = db.scalars(stmt).all()
        print(f"animal list count: {len(animals_list)}")

    except Exception as e:
        print(f"An exception has occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
