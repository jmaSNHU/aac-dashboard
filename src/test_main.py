from model.base import Base
from database import engine, SessionLocal
import model

def init_db():
    """Build all registered database structures."""
    print("Building schema metadata structures...")
    Base.metadata.create_all(bind=engine)

def main():
    init_db();

    db = SessionLocal()
    try:
        queried_animal = db.query(model.Animal).filter_by(id="100").first()
        print(f"Animal: {queried_animal}")
        print(f"Breed: {queried_animal.breed}")
    except Exception as e:
        print(f"An exception has occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
