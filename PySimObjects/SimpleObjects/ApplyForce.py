from abc import abstractmethod, ABC
import pygame

class ApplyForce(ABC):
    @abstractmethod
    def get_applied_force(self, target_entity: 'Entity') -> pygame.Vector2:
        """Calculates and returns the force exerted on a target entity."""
        pass

    @abstractmethod
    def get_force_origin(self) -> pygame.Vector2:
        """Returns the point from which the force originates."""
        pass