#!/usr/bin/python3
"""Amenity module"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .place import Place


class Amenity(BaseModel):
    """Amenity entity representing features and services available at places."""

    def __init__(
        self,
        name: str,
        description: str = "",
        **kwargs,
    ):
        """Initialize a new Amenity."""
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self._places: List[Place] = []

    # ============= Properties with Validation =============

    @property
    def name(self) -> str:
        """Get name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set name with validation."""
        if not value or not value.strip():
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be at most 50 characters")
        self._name = value.strip()

    @property
    def description(self) -> str:
        """Get description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set description with validation."""
        if len(value) > 200:
            raise ValueError("description must be at most 200 characters")
        self._description = value.strip() if value else ""

    # ============= Relationship Properties =============

    @property
    def places(self) -> List[Place]:
        """Get places that have this amenity."""
        return self._places.copy()

    # ============= Relationship Methods =============

    def add_place(self, place: Place):
        """Add a place that offers this amenity."""
        if place not in self._places:
            self._places.append(place)
            self.save()

    def remove_place(self, place: Place):
        """Remove a place from this amenity."""
        if place in self._places:
            self._places.remove(place)
            self.save()

    # ============= Business Methods (UML Compliance) =============

    def create(self) -> None:
        """Create amenity. (+create() in UML)"""
        self.save()

    def update(self, data: dict) -> None:
        """Update amenity. (+update() in UML)"""
        super().update(data)

    def delete(self) -> None:
        """Delete amenity. (+delete() in UML)"""
        pass

    @staticmethod
    def list() -> list:
        """List all amenities. (+list() in UML)"""
        # This will be implemented by facade/repository
        return []

    def get_name(self) -> str:
        """Get amenity name. (+getName(): String in UML)"""
        return self.name

    def get_description(self) -> str:
        """Get amenity description. (+getDescription(): String in UML)"""
        return self.description

    # ============= Validation =============

    def validate(self) -> bool:
        """Validate amenity data. (+validate() in UML)"""
        try:
            _ = self.name
            return True
        except (ValueError, AttributeError):
            return False

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert amenity to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "description": self.description,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        """String representation."""
        return f"[Amenity] {self.name}"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<Amenity id={self._id} name={self.name}>"
