import pygame
from PySimEngine.Entity import Entity
from PySimObjects.SimpleObjects.ApplyForce import ApplyForce


class ForceField(Entity, ApplyForce):
    """
    An entity that applies a constant force in a specific direction
    to other objects within a defined radius.
    """

    def __init__(self, x: int, y: int, radius: float, strength: float,
                 direction_vector: pygame.Vector2, color: tuple = (150, 255, 150)):
        Entity.__init__(self, x, y)

        self.radius = radius
        self.strength = strength

        self.direction = direction_vector.normalize() if direction_vector.length() > 0 else pygame.Vector2(0, 0)
        self.color = color

    def get_applied_force(self, target_entity: 'Entity') -> pygame.Vector2:
        distance = self.position.distance_to(target_entity.position)

        if distance > self.radius:
            return pygame.Vector2(0, 0)

        return self.direction * self.strength

    def get_force_origin(self) -> pygame.Vector2:
        return self.position

    def calculate_physics(self, delta_time: float, game):
        pass

    def update(self, delta_time: float, game):
        pass

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (self.color[0], self.color[1], self.color[2], 50),
                           self.position, int(self.radius), 1)

        pygame.draw.circle(surface, self.color, self.position, 15)

        arrow_start = self.position
        arrow_end = self.position + self.direction * 30
        pygame.draw.line(surface, (255, 255, 255), arrow_start, arrow_end, 3)

        head_size = 8
        angle = self.direction.angle_to(pygame.Vector2(1, 0))

        p1 = arrow_end + pygame.Vector2(head_size, 0).rotate(-angle + 150)
        p2 = arrow_end + pygame.Vector2(head_size, 0).rotate(-angle - 150)
        pygame.draw.polygon(surface, (255, 255, 255), [arrow_end, p1, p2])