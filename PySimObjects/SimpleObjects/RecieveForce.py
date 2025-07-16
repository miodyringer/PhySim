from abc import ABC, abstractmethod
import pygame


class ReceiveForce(ABC):
    @abstractmethod
    def apply_force(self, force: pygame.Vector2, delta_time: float):
        """Applies the calculated force to the object."""
        pass