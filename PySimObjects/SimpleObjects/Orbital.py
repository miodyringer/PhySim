from abc import abstractmethod, ABC
import pygame

# Import necessary base components
from PySimEngine.Entity import Entity
from PySimObjects.SimpleObjects.Movable import Movable
from PySimObjects.SimpleObjects.Collision import Collision # Assuming 'Collision' is your Collidable
from PySimObjects.SimpleObjects.Mass import Mass # Assuming 'Mass' is your HasMass
from PySimObjects.SimpleObjects.RecieveForce import ReceiveForce # Assuming 'RecieveForce' is your ReceivesForce
from PySimObjects.SimpleObjects.Shape import Shape # For Collision's __init__

class Orbital(Entity, Movable, Collision, Mass, ReceiveForce, ABC):
    """
    An abstract base class for entities that are movable, collidable,
    have mass, and can receive forces.
    """
    def __init__(self, x: int, y: int, velocity: pygame.Vector2, mass: float, shape: Shape, restitution: float = 0.8):
        Entity.__init__(self, x, y)
        Movable.__init__(self, velocity)
        Collision.__init__(self, shape)
        Mass.__init__(self, mass)
        ReceiveForce.__init__(self)

        self.acceleration = pygame.Vector2(0, 0)
        self.force_accumulated = pygame.Vector2(0, 0)
        self.pending_velocity_change = pygame.Vector2(0, 0)
        self.pending_position_correction = pygame.Vector2(0, 0)
        self.restitution = restitution

    @abstractmethod
    def calculate_physics(self, delta_time: float, game):
        pass

    @abstractmethod
    def update(self, delta_time: float, game):
        pass

    @abstractmethod
    def render(self, surface):
        pass

    def apply_movement(self, delta_time: float):
        """
        This method is part of Movable but its core logic is integrated into apply_physics_update.
        :param delta_time: The time between frames.
        """
        pass

    @abstractmethod
    def get_collision_shape(self) -> Shape:
        """Returns the shape object used for detailed collision detection."""
        pass

    @abstractmethod
    def resolve_collision(self, other: 'Collision'):
        """
        Handles the collision response with another collidable object.
        :param other: Collision object.
        """
        pass

    def get_mass(self) -> float:
        """Returns the mass of the entity."""
        return self.mass

    def apply_force(self, force: pygame.Vector2, delta_time: float):
        """
        Applies a given force to the entity, accumulating it for the current frame.
        :param force: Force to be applied.
        :param delta_time: The time between frames.
        """
        self.force_accumulated += force