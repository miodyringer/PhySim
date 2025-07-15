import pygame

from PySimEngine.Entity import Entity
from PySimEngine.Game import Game


class Orbital(Entity):

    orbitals = []
    G = 6000

    def __init__(self, x, y, mass, color, velocity):
        super().__init__(x, y)
        self.radius = (mass / 3.14) ** 0.5
        self.mass = mass
        self.color = color
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        Orbital.orbitals.append(self)

    def apply_force(self, force_vector: pygame.Vector2):
        self.force += force_vector

    def update(self, delta_time, game: Game):
        if self.mass == 0:
            return

        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time
        self.force = pygame.Vector2(0, 0)

    def render(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    @staticmethod
    def update_all_physics():
        for orbital in Orbital.orbitals:
            orbital.force = pygame.Vector2(0, 0)

        for i in range(len(Orbital.orbitals)):
            for j in range(i + 1, len(Orbital.orbitals)):
                body1 = Orbital.orbitals[i]
                body2 = Orbital.orbitals[j]

                direction_vector = body2.position - body1.position
                distance = direction_vector.length()

                if distance < (body1.radius + body2.radius):
                    # You could handle collisions here, or just skip force calculation
                    continue

                direction_unit_vector = direction_vector.normalize()

                force_magnitude = Orbital.G * (body1.mass * body2.mass) / (distance * distance)

                force_vector = direction_unit_vector * force_magnitude

                body1.apply_force(force_vector)
                body2.apply_force(-force_vector)

    @classmethod
    def remove_orbital(cls, orbital_to_remove):
        if orbital_to_remove in cls.orbitals:
            cls.orbitals.remove(orbital_to_remove)