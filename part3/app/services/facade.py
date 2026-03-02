#!/usr/bin/python3
"""HBnB Facade (Task 5)."""

from app.persistence.in_memory_repository import InMemoryRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    """
    Task 5:
    - Provide SQLAlchemyRepository.
    - Refactor user operations to use SQLAlchemyRepository when user_model is available.
    - No database initialization here (handled in Task 6).
    """

    def __init__(self, user_model=None, user_repo=None):
        if user_repo is not None:
            self.user_repo = user_repo
        elif user_model is not None:
            self.user_repo = SQLAlchemyRepository(user_model)
        else:
            self.user_repo = InMemoryRepository()

    # ------------------ USERS ------------------
    def create_user(self, user_obj):
        return self.user_repo.add(user_obj)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)
