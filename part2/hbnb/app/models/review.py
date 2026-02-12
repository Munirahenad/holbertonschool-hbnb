#!/usr/bin/python3
"""Review module"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .place import Place


class Review(BaseModel):
    """Review entity representing user reviews and ratings."""

    def __init__(
        self,
        rating: int,
        comment: str,
        user: User,
        place: Place,
        **kwargs,
    ):
        """Initialize a new Review."""
        super().__init__(**kwargs)
        self.rating = rating
        self.comment = comment
        self.user = user
        self.place = place

        if user:
            user.add_review(self)
        if place:
            place.add_review(self)

    # ============= Properties with Validation =============

    @property
    def rating(self) -> int:
        """Get rating."""
        return self._rating

    @rating.setter
    def rating(self, value: int):
        """Set rating with validation (1-5)."""
        try:
            value = int(value)
            if value < 1 or value > 5:
                raise ValueError("rating must be between 1 and 5")
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer")
        self._rating = value

    @property
    def comment(self) -> str:
        """Get comment."""
        return self._comment

    @comment.setter
    def comment(self, value: str):
        """Set comment with validation."""
        if len(value) > 500:
            raise ValueError("comment must be under 500 characters")
        self._comment = value.strip() if value else ""

    @property
    def user(self) -> User:
        """Get user who wrote review."""
        return self._user

    @user.setter
    def user(self, value: User):
        """Set user with validation."""
        if value is None:
            raise ValueError("user is required")
        self._user = value

    @property
    def place(self) -> Place:
        """Get place being reviewed."""
        return self._place

    @place.setter
    def place(self, value: Place):
        """Set place with validation."""
        if value is None:
            raise ValueError("place is required")
        self._place = value

    # ============= Business Methods (UML Compliance) =============

    def create(self) -> None:
        """Create review. (+create() in UML)"""
        self.save()

    def update(self, data: dict) -> None:
        """Update review. (+update() in UML)"""
        super().update(data)

    def delete(self) -> None:
        """Delete review. (+delete() in UML)"""
        pass

    @staticmethod
    def list_by_place(place_id: str) -> list:
        """List reviews by place. (+listByPlace(place_id): List in UML)"""
        # This will be implemented by facade/repository
        return []

    # ============= Validation =============

    def validate_rating(self) -> bool:
        """Validate rating. (+validateRating() in UML)"""
        return 1 <= self.rating <= 5

    def validate_comment(self) -> bool:
        """Validate comment. (+validateComment() in UML)"""
        return len(self.comment) <= 500

    def validate(self) -> bool:
        """Validate review data. (+validate() in UML)"""
        try:
            _ = self.rating
            _ = self.comment
            _ = self.user
            _ = self.place
            return True
        except (ValueError, AttributeError):
            return False

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert review to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "rating": self.rating,
            "comment": self.comment,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        """String representation."""
        return f"[Review] {self.rating}/5 by {self.user.email if self.user else 'Unknown'}"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<Review id={self._id} rating={self.rating}>"
