from PySimEngine.Entity import Entity


class EntityManager:
    """Manages all entities, handling safe addition and removal."""
    def __init__(self):
        self._entities = []
        self._to_add = []
        self._to_remove = []

    def add(self, entity: Entity):
        self._to_add.append(entity)

    def remove(self, entity: Entity):
        self._to_remove.append(entity)

    def get_entities(self) -> list[Entity]:
        return self._entities[:]

    def apply_changes(self):
        """Safely adds and removes entities between frames."""
        if self._to_add:
            self._entities.extend(self._to_add)
            self._to_add.clear()
        if self._to_remove:
            self._entities = [e for e in self._entities if e not in self._to_remove]
            self._to_remove.clear()