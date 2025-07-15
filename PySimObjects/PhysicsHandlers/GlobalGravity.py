# PySimObjects/PhysicsHandlers/GlobalGravity.py
import pygame
from PySimObjects.SimpleObjects.Mass import Mass

class GlobalGravity:
    """
    Handles gravitational forces between objects based on their mass and distance.
    Uses Newton's Law of Universal Gravitation: F = G * (m1 * m2) / r^2
    """
    def __init__(self, gravitational_constant: float):
        """
        Initializes the global gravity handler.
        :param gravitational_constant: The gravitational constant (G) for the simulation.
                                       Adjust this value to control the strength of gravity in your pixel world.
        """
        self.G = gravitational_constant

    def calculate_gravitational_force(self, body1_pos: pygame.Vector2, body1_mass: float,
                                      body2_pos: pygame.Vector2, body2_mass: float) -> pygame.Vector2:
        """
        Calculates the gravitational force exerted by body2 on body1.
        :param body1_pos: Position of the first body.
        :param body1_mass: Mass of the first body.
        :param body2_pos: Position of the second body.
        :param body2_mass: Mass of the second body.
        :return: A pygame.Vector2 representing the force on body1.
        """
        if body1_mass <= 0 or body2_mass <= 0:
            return pygame.Vector2(0, 0)

        direction_vector = body2_pos - body1_pos
        distance_squared = direction_vector.magnitude_squared()

        if distance_squared < 100:
            distance_squared = 100
        distance = direction_vector.magnitude()

        if distance == 0:
            return pygame.Vector2(0, 0)

        force_magnitude = (self.G * body1_mass * body2_mass) / distance_squared
        force_direction = direction_vector.normalize()

        return force_direction * force_magnitude