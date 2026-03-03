#!/usr/bin/python3
"""SQLAlchemy repository implementation (Tasks 5, 6 & 7)."""

from app.extensions import db
from app.persistence.repository import Repository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


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


# ==================== TASK 6: UserRepository ====================

class UserRepository(SQLAlchemyRepository):
    """User-specific repository with custom queries."""
    
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Get a user by email address.
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: User object or None if not found
        """
        return self.model.query.filter_by(email=email).first()


# ==================== TASK 7: PlaceRepository ====================

class PlaceRepository(SQLAlchemyRepository):
    """Place-specific repository."""
    
    def __init__(self):
        super().__init__(Place)


# ==================== TASK 7: ReviewRepository ====================

class ReviewRepository(SQLAlchemyRepository):
    """Review-specific repository."""
    
    def __init__(self):
        super().__init__(Review)


# ==================== TASK 7: AmenityRepository ====================

class AmenityRepository(SQLAlchemyRepository):
    """Amenity-specific repository."""
    
    def __init__(self):
        super().__init__(Amenity)
