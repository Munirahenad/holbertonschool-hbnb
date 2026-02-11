class InMemoryRepository:
    """
    Simple in-memory repository.

    Storage format:
      {
        "User": { "<id>": obj, ... },
        "Place": { "<id>": obj, ... },
        ...
      }
    """

    def __init__(self):
        self._storage = {}

    def _bucket(self, model_name):
        if model_name not in self._storage:
            self._storage[model_name] = {}
        return self._storage[model_name]

    def add(self, model_name, obj):
        bucket = self._bucket(model_name)
        bucket[obj.id] = obj
        return obj

    def get(self, model_name, obj_id):
        return self._bucket(model_name).get(obj_id)

    def all(self, model_name):
        return list(self._bucket(model_name).values())

    def update(self, model_name, obj_id, **fields):
        obj = self.get(model_name, obj_id)
        if not obj:
            return None

        for k, v in fields.items():
            if hasattr(obj, k):
                setattr(obj, k, v)

        if hasattr(obj, "touch") and callable(getattr(obj, "touch")):
            obj.touch()

        return obj

    def delete(self, model_name, obj_id):
        bucket = self._bucket(model_name)
        return bucket.pop(obj_id, None)

    def exists(self, model_name, obj_id):
        return self.get(model_name, obj_id) is not None
