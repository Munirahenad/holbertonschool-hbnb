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
        text: str,
        user: User,
        place: Place,
        **kwargs,
    ):
        """Initialize a new Review."""
        super().__init__(**kwargs)
        self.rating = rating
        self.text = text
        self.user = user
        self.place = place

        if user:
            user.add_review(self)
        if place:
            place.add_review(self)

    @property
    def rating(self) -> int:
        """Get rating."""
        return self._rating

    @rating.setter
    def rating(self, value: int):
        try:
            value = int(value)
            if value < 1 or value > 5:
                raise ValueError("rating must be between 1 and 5")
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer")
        self._rating = value

    @property
    def text(self) -> str:
        """Get review text."""
        return self._text

    @text.setter
    def text(self, value: str):
        if not value or not value.strip():
            raise ValueError("text is required")
        if len(value) > 500:
            raise ValueError("text must be under 500 characters")
        self._text = value.strip()

    @property
    def user(self) -> User:
        """Get user who wrote review."""
        return self._user

    @user.setter
    def user(self, value: User):
        if value is None:
            raise ValueError("user is required")
        self._user = value

    @property
    def place(self) -> Place:
        """Get place being reviewed."""
        return self._place

    @place.setter
    def place(self, value: Place):
        if value is None:
            raise ValueError("place is required")
        self._place = value

    def create(self) -> None:
        """Create review."""
        self.save()

    def update(self, data: dict) -> None:
        """Update review."""
        super().update(data)

    def delete(self) -> None:
        """Delete review."""
        pass

    @staticmethod
    def list_by_place(place_id: str) -> list:
        """List reviews by place."""
        return []

    def validate_rating(self) -> bool:
        """Validate rating."""
        return 1 <= self.rating <= 5

    def validate_text(self) -> bool:
        """Validate review text."""
        return len(self.text) <= 500

    def validate(self) -> bool:
        """Validate review data."""
        try:
            _ = self.rating
            _ = self.text
            _ = self.user
            _ = self.place
            return True
        except (ValueError, AttributeError):
            return False

    def to_dict(self) -> dict:
        """Convert review to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "rating": self.rating,
            "text": self.text,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None,
        })
        return base_dict

    def __str__(self) -> str:
        """String representation."""
        return f"[Review] {self.rating}/5 by {self.user.email if self.user else 'Unknown'}"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<Review id={self._id} rating={self.rating}>"
