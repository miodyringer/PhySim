import random

import pygame

from PySimEngine.Entity import Entity
from PySimEngine.Game import Game
from PySimObjects.Circle import Circle


class Cube(Entity):
    def __init__(self, x, y, size, color):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = 300

    def update(self, delta_time, game: Game):
        movement = pygame.Vector2(0, 0)
        if game.input_manager.is_held(pygame.K_w): movement.y -= 1
        if game.input_manager.is_held(pygame.K_s): movement.y += 1
        if game.input_manager.is_held(pygame.K_a): movement.x -= 1
        if game.input_manager.is_held(pygame.K_d): movement.x += 1

        if movement.length() > 0:
            self.position += movement.normalize() * self.speed * delta_time

        if game.input_manager.is_pressed(pygame.K_k):
            rand_pos = (random.randint(50, 750), random.randint(50, 550))
            rand_vel = (random.randint(-150, 150), random.randint(-150, 150))
            rand_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            new_circle = Circle(rand_pos[0], rand_pos[1], 15, rand_color, rand_vel)
            game.entity_manager.add(new_circle)

        self.rect.topleft = self.position

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)