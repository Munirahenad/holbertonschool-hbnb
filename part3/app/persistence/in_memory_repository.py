#!/usr/bin/python3
"""In-memory repository (temporary fallback)."""

from app.persistence.repository import Repository


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[getattr(obj, "id")] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def delete(self, obj_id):
        if obj_id not in self._storage:
            return False
        del self._storage[obj_id]
        return True

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None
