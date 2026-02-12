#!/usr/bin/python3
"""User module"""

from __future__ import annotations

import re
from typing import Any, List, Optional, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .place import Place
    from .review import Review


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """
    User entity representing system users.
    
    Attributes:
        first_name (str): User's first name (required, max 50)
        last_name (str): User's last name (required, max 50)
        email (str): User's email address (required, valid format)
        password (str): User's password (required, min 8 chars)
        is_admin (bool): Admin privileges flag (default False)
        places (List[Place]): Places owned by user
        reviews (List[Review]): Reviews written by user
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_admin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize a new User."""
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self._places: List[Place] = []
        self._reviews: List[Review] = []

    # ============= Properties with Validation =============

    @property
    def first_name(self) -> str:
        """Get first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Set first name with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("first_name is required")
        if len(value) > 50:
            raise ValueError("first_name must be at most 50 characters")
        self._first_name = value.strip()

    @property
    def last_name(self) -> str:
        """Get last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Set last name with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("last_name is required")
        if len(value) > 50:
            raise ValueError("last_name must be at most 50 characters")
        self._last_name = value.strip()

    @property
    def email(self) -> str:
        """Get email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set email with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required")
        if not _EMAIL_RE.match(value.strip()):
            raise ValueError("email must be a valid email address")
        self._email = value.strip().lower()

    @property
    def password(self) -> str:
        """Get password."""
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Set password with validation."""
        if not value or len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        # Note: In production, hash the password!
        self._password = value

    @property
    def is_admin(self) -> bool:
        """Get admin status."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value: bool) -> None:
        """Set admin status."""
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self._is_admin = value

    # ============= Relationship Properties =============

    @property
    def places(self) -> List[Place]:
        """Get places owned by user."""
        return self._places.copy()

    @property
    def reviews(self) -> List[Review]:
        """Get reviews written by user."""
        return self._reviews.copy()

    # ============= Relationship Methods =============

    def add_place(self, place: Place) -> None:
        """Add a place owned by user."""
        if place not in self._places:
            self._places.append(place)
            self.save()

    def remove_place(self, place: Place) -> None:
        """Remove a place owned by user."""
        if place in self._places:
            self._places.remove(place)
            self.save()

    def add_review(self, review: Review) -> None:
        """Add a review written by user."""
        if review not in self._reviews:
            self._reviews.append(review)
            self.save()

    def remove_review(self, review: Review) -> None:
        """Remove a review written by user."""
        if review in self._reviews:
            self._reviews.remove(review)
            self.save()

    # ============= Business Methods (UML Compliance) =============

    def register(self) -> None:
        """Register user account. (+register() in UML)"""
        self.save()

    def update_profile(self, data: dict) -> None:
        """Update user profile. (+updateProfile() in UML)"""
        self.update(data)

    def delete(self) -> None:
        """Delete user account. (+delete() in UML)"""
        # Will be handled by facade/repository
        pass

    def is_admin_user(self) -> bool:
        """Check if user is admin. (+isAdmin(): Boolean in UML)"""
        return self.is_admin

    def get_full_name(self) -> str:
        """Get user's full name. (+getFullName(): String in UML)"""
        return f"{self.first_name} {self.last_name}"

    # ============= Validation =============

    def validate(self) -> bool:
        """Validate user data. (+validate() in UML)"""
        try:
            # Trigger all validators
            _ = self.first_name
            _ = self.last_name
            _ = self.email
            _ = self.password
            _ = self.is_admin
            return True
        except (ValueError, AttributeError):
            return False

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            # Password is intentionally NOT included for security
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        """String representation."""
        return f"[User] {self.email}"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<User id={self._id} email={self.email}>"
