from PhySimEngine.Entity import Entity


class EntityManager:
    """Manages all entities, handling safe addition and removal."""
    def __init__(self):
        self.entities = []
        self.to_add = []
        self.to_remove = []

    def add(self, entity: Entity):
        """
        Adds an entity to the queue.
        :param entity: The entity to add.
        """
        self.to_add.append(entity)

    def remove(self, entity: Entity):
        """
        Removes an entity from the queue.
        :param entity: The entity to remove.
        """
        self.to_remove.append(entity)

    def get_entities(self) -> list[Entity]:
        """
        Returns all entities in the queue.
        Returns: List of all entities.
        """
        return self.entities[:]

    def apply_changes(self):
        """Safely adds or removes queued entities between frames."""
        if self.to_add:
            self.entities.extend(self.to_add)
            self.to_add.clear()
        if self.to_remove:
            self.entities = [e for e in self.entities if e not in self.to_remove]
            self.to_remove.clear()