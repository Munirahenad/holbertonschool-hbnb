#!/usr/bin/python3
"""BaseModel module - Base class for all HBnB entities"""
 
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class BaseModel:
    """
    Base class for all HBnB entities.
    
    Provides:
    - id: UUID4 string (unique identifier)
    - created_at: UTC datetime of creation
    - updated_at: UTC datetime of last update
    - save(): Update timestamp
    - update(): Update attributes with validation
    - to_dict(): Convert to dictionary
    - validate(): Override in subclasses
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize BaseModel with UUID and timestamps."""
        now = datetime.now(timezone.utc)

        self._id: str = kwargs.get("id", str(uuid.uuid4()))
        self._created_at: datetime = kwargs.get("created_at", now)
        self._updated_at: datetime = kwargs.get("updated_at", now)

    # ============= Getters (UML compatibility) =============
    
    def get_id(self) -> str:
        """Get entity ID (UUID4)."""
        return self._id
    
    def get_created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at
    
    def get_updated_at(self) -> datetime:
        """Get last update timestamp."""
        return self._updated_at

    # ============= Properties (Pythonic convenience) =============
    
    @property
    def id(self) -> str:
        """ID property."""
        return self._id
    
    @property
    def created_at(self) -> datetime:
        """Creation timestamp property."""
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        """Last update timestamp property."""
        return self._updated_at

    # ============= Core Methods =============
    
    def save(self) -> None:
        """
        Update the updated_at timestamp.
        Matches UML: +updateTimestamp() void
        """
        self._updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entity to dictionary representation.
        Matches UML: +toDict() Dictionary
        """
        return {
            "id": self._id,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }

    def validate(self) -> bool:
        """
        Validate entity state.
        Override in subclasses for custom validation.
        Matches UML: +validate() bool
        """
        return True

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update allowed attributes from dictionary.
        
        Protected fields (id, created_at, updated_at) cannot be updated.
        After update, validates and saves.
        
        Args:
            data: Dictionary of attributes to update
        """
        # Protected fields that cannot be updated
        protected = {
            "id", "_id", 
            "created_at", "_created_at", 
            "updated_at", "_updated_at"
        }
        
        for key, value in data.items():
            if key in protected or key.startswith("_"):
                continue
                
            # Try with underscore first (private attribute)
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
            # Then try without underscore
            elif hasattr(self, key):
                setattr(self, key, value)
        
        if self.validate():
            self.save()

    def __str__(self) -> str:
        """String representation."""
        return f"[{self.__class__.__name__}] ({self._id})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"<{self.__class__.__name__} id={self._id}>"
