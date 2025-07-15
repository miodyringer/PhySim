import pygame

from PySimEngine.Entity import Entity
from PySimEngine.Game import Game


class Circle(Entity):
    def __init__(self, x, y, radius, color, velocity):
        super().__init__(x, y)
        self.radius = radius
        self.color = color
        self.velocity = pygame.Vector2(velocity)

    def update(self, delta_time, game: Game):
        self.position += self.velocity * delta_time
        screen_rect = game.display_surface.get_rect()
        if self.position.x - self.radius < 0 or self.position.x + self.radius > screen_rect.width:
            self.velocity.x *= -1
        if self.position.y - self.radius < 0 or self.position.y + self.radius > screen_rect.height:
            self.velocity.y *= -1

    def render(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)