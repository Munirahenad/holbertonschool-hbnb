from persistence.repository import InMemoryRepository

class HBnBFacade:
    """
    Facade layer:
    API layer should talk to this class (not directly to repository).

    Part 2: uses InMemoryRepository
    Part 3: will be replaced with SQLAlchemy-backed repository
    """

    def __init__(self):
        self.repo = InMemoryRepository()
