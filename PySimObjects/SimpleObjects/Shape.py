from abc import abstractmethod, ABC
import pygame

class Shape(ABC):
    @abstractmethod
    def render_shape(self, surface: pygame.Surface, position: pygame.Vector2, color):
        """Renders the shape on the given surface."""
        pass

    @abstractmethod
    def intersects(self, other: 'Shape', self_pos: pygame.Vector2, other_pos: pygame.Vector2) -> bool:
        """Checks for intersection with another shape."""
        pass