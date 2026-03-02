#!/usr/bin/python3
"""SQLAlchemy repository implementation (Task 5)."""

from app.extensions import db
from app.persistence.repository import Repository


class SQLAlchemyRepository(Repository):
    """Generic repository for SQLAlchemy persistence."""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)

    def get_all(self):
        return db.session.query(self.model).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False

        db.session.delete(obj)
        db.session.commit()
        return True

    def get_by_attribute(self, attr_name, attr_value):
        if not hasattr(self.model, attr_name):
            return None

        return (
            db.session.query(self.model)
            .filter(getattr(self.model, attr_name) == attr_value)
            .first()
        )
