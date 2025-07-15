from abc import abstractmethod, ABC
import pygame

class Movable(ABC):
    def __init__(self, velocity: pygame.Vector2):
        self.velocity = velocity

    @abstractmethod
    def apply_movement(self, delta_time: float):
        """Applies movement based on velocity and delta_time."""
        pass