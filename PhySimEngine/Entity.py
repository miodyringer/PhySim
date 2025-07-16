from abc import abstractmethod, ABC

import pygame

class Entity(ABC):
    """Abstract base class for all game objects."""
    def __init__(self, x: int, y: int):
        self.position: pygame.Vector2 = pygame.Vector2(x, y)

    @abstractmethod
    def calculate_physics(self, delta_time: float, scenario: 'Scenario'):
        """
        Precalculates the physics of the entity based on the delta time.
        :param delta_time: Time in seconds since the last frame.
        :param scenario: The main scenario instance, providing access to managers (input, entities).
        """
        pass

    @abstractmethod
    def update(self, delta_time: float, scenario: 'Scenario'):
        """
        Update logic for the entity.
        :param delta_time: Time in seconds since the last frame.
        :param scenario: The main scenario instance, providing access to managers (input, entities).
        """
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Render logic for the entity.
        :param surface: The surface to render to.
        """
        pass