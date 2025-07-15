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
    An abstract base class for entities that participate in orbital mechanics,
    are movable, collidable, have mass, and can receive forces.
    It integrates Entity with various physics capabilities.
    """
    def __init__(self, x: float, y: float, velocity: pygame.Vector2, mass: float, shape: Shape, restitution: float = 0.8):
        # Initialize Entity first, as it's the root game object
        Entity.__init__(self, x, y)
        # Initialize other parent abstract classes
        Movable.__init__(self, velocity)
        Collision.__init__(self, shape)
        Mass.__init__(self, mass)
        ReceiveForce.__init__(self) # Assuming it has an __init__ or does nothing

        # Orbital-specific physics attributes
        self.acceleration = pygame.Vector2(0, 0)
        self._net_force_accumulated = pygame.Vector2(0, 0) # Accumulates forces each frame
        self._pending_velocity_change = pygame.Vector2(0, 0) # For collision impulses
        self._pending_position_correction = pygame.Vector2(0, 0) # For collision separation
        self.restitution = restitution # Coefficient of restitution for collisions

    # --- Implementations of abstract methods from Entity ---
    @abstractmethod
    def calculate_physics(self, delta_time: float, game):
        """
        Phase 1: Calculates forces, detects potential collisions, and determines desired state changes
        for the entity based on its current state. No state changes are applied here yet.
        """
        pass

    @abstractmethod
    def update(self, delta_time: float, game):
        """
        Phase 2: Applies the calculated physics changes (e.g., updates velocity, position)
        to the entity's actual state. Collision resolution also typically happens here.
        """
        pass

    @abstractmethod
    def render(self, surface):
        """Renders the orbital body."""
        pass

    # --- Implementations of abstract methods from Movable ---
    # The actual movement application logic is handled in apply_physics_update
    def apply_movement(self, delta_time: float):
        """This method is part of Movable but its core logic is integrated into apply_physics_update."""
        pass

    # --- Implementations of abstract methods from Collision ---
    @abstractmethod
    def get_collision_shape(self) -> Shape:
        """Returns the shape object used for detailed collision detection."""
        pass

    @abstractmethod
    def resolve_collision(self, other: 'Collision'):
        """Handles the collision response with another collidable object."""
        pass

    # --- Implementations of abstract methods from Mass ---
    def get_mass(self) -> float:
        """Returns the mass of the entity."""
        return self.mass

    # --- Implementations of abstract methods from ReceiveForce ---
    def apply_force(self, force: pygame.Vector2, delta_time: float):
        """Applies a given force to the entity, accumulating it for the current frame."""
        self._net_force_accumulated += force