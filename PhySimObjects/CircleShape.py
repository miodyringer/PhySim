import pygame
from PhySimObjects.SimpleObjects.Shape import Shape

class CircleShape(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def render_shape(self, surface: pygame.Surface, position: pygame.Vector2, color):
        pygame.draw.circle(surface, color, (int(position.x), int(position.y)), int(self.radius))

    def intersects(self, other: 'Shape', self_pos: pygame.Vector2, other_pos: pygame.Vector2) -> bool:
        if isinstance(other, CircleShape):
            distance = self_pos.distance_to(other_pos)
            return distance < (self.radius + other.radius)
        return False
