#!/usr/bin/python3
"""Place module"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .review import Review
    from .amenity import Amenity


class Place(BaseModel):
    """Place entity representing rental properties."""

    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self._reviews: List[Review] = []
        self._amenities: List[Amenity] = []

        if owner:
            owner.add_place(self)

    # ============= Properties with Validation =============

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Title is required")
        if len(value) > 100:
            raise ValueError("Title must be under 100 characters")
        self._title = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if len(value) > 1000:
            raise ValueError("Description must be under 1000 characters")
        self._description = value.strip() if value else ""

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError("Price must be greater than 0")
            if value > 1000000:
                raise ValueError("Price must be under 1,000,000")
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        self._price = round(value, 2)

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        try:
            value = float(value)
            if not (-90 <= value <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number")
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        try:
            value = float(value)
            if not (-180 <= value <= 180):
                raise ValueError("Longitude must be between -180 and 180")
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number")
        self._longitude = value

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, value: User):
        if value is None:
            raise ValueError("Owner ID is required")
        self._owner = value

    # ============= Relationship Properties =============

    @property
    def reviews(self) -> List[Review]:
        return self._reviews.copy()

    @property
    def amenities(self) -> List[Amenity]:
        return self._amenities.copy()

    # ============= Relationship Methods =============

    def add_review(self, review: Review):
        if review not in self._reviews:
            self._reviews.append(review)
            self.save()

    def add_amenity(self, amenity: Amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)
            self.save()
            amenity.add_place(self)

    def remove_amenity(self, amenity: Amenity):
        """Remove amenity from place (اختياري لكن موجود في كودك)"""
        if amenity in self._amenities:
            self._amenities.remove(amenity)
            self.save()
            amenity.remove_place(self)

    # ============= Business Methods =============

    def create(self):
        self.save()

    def update(self, data: dict):
        super().update(data)

    def delete(self):
        pass

    def list_reviews(self) -> List[Review]:
        return self.reviews

    def get_amenities(self) -> List[Amenity]:
        return self.amenities

    def get_average_rating(self) -> float:
        if not self._reviews:
            return 0.0
        total = sum(r.rating for r in self._reviews)
        return round(total / len(self._reviews), 1)

    # ============= Validation =============

    def validate(self) -> bool:
        try:
            _ = self.title
            _ = self.price
            _ = self.latitude
            _ = self.longitude
            _ = self.owner
            return True
        except (ValueError, AttributeError):
            return False

    # ============= Serialization =============

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "amenity_ids": [a.id for a in self._amenities],
            "average_rating": self.get_average_rating(),
        })
        return base_dict

    def __str__(self) -> str:
        return f"[Place] {self.title}"
