from model.base import Base
from database import engine, SessionLocal
import model
from sqlalchemy.orm import Session

class AnimalShelter:
    def __init__(self, t_model, db: Session):
        self.t_model = t_model
        self.db = db

    def create(self, input_data: dict):
        data = self.t_model(**input_data)
        self.db.add(data)
        self.db.commit()
        # refresh model object to get ID
        self.db.refresh(data)
        return data

    def read_by_id(self, t_id: int):
        return self.db.query(self.t_model).filter(self.t_model.id == t_id).first()

    def read(self, filters: dict = None):
        if filters:
            return self.db.query(self.t_model).filter_by(**filters).all()
        else:
            return self.db.query(self.t_model).all()

    def update(self, t_id: int, update_data: dict):
        data = self.get(t_id)
        if data:
            for key, value in update_data.items():
                setattr(data, key, value)
            self.db.commit()
            self.db.refresh()
        return data

    def delete(self, t_id):
        data = self.get(t_id)
        if data:
            self.db.delete(data)
            self.db.commit()
        return data

