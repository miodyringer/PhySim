from abc import abstractmethod, ABC

import pygame

class Entity(ABC):
    """Abstract base class for all game objects."""
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)

    @abstractmethod
    def calculate_physics(self, delta_time: float, game):
        pass

    @abstractmethod
    def update(self, delta_time, game):
        """
        Update logic for the entity.
        :param delta_time: Time in seconds since the last frame.
        :param game: The main game instance, providing access to managers (input, entities).
        """
        pass

    @abstractmethod
    def render(self, surface):
        pass