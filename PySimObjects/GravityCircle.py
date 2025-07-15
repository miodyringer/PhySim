import pygame

from PySimEngine.Entity import Entity
from PySimEngine.Scenario import Scenario
from PySimObjects.SimpleObjects.Movable import Movable
from PySimObjects.SimpleObjects.Collision import Collision
from PySimObjects.SimpleObjects.Mass import Mass
from PySimObjects.SimpleObjects.RecieveForce import ReceiveForce
from PySimObjects.CircleShape import CircleShape
from PySimObjects.PhysicsHandlers.LocalGravity import LocalGravity


class GravityCircle(Entity, Movable, Collision, Mass, ReceiveForce):
    """
    A circle entity that is movable, can collide, has mass, receives forces (like gravity),
    and is affected by a LocalGravity handler.
    """
    def __init__(self, x: float, y: float, radius: float, color: tuple,
                 initial_velocity: pygame.Vector2, mass: float = 1.0,
                 restitution: float = 0.8):
        Entity.__init__(self, x, y)
        Movable.__init__(self, initial_velocity)
        Mass.__init__(self, mass)
        ReceiveForce.__init__(self)

        self.restitution = restitution

        self._shape = CircleShape(radius)
        Collision.__init__(self, self._shape)

        self.color = color
        self.radius = radius

        self._net_force_accumulated = pygame.Vector2(0, 0)
        self._pending_velocity_change = pygame.Vector2(0, 0)
        self._pending_position_correction = pygame.Vector2(0, 0)


    def apply_force(self, force: pygame.Vector2, delta_time: float):
        """Applies a force to the circle, accumulating it for the current frame's physics calculation."""
        self._net_force_accumulated += force

    def apply_movement(self, delta_time: float):
        """This method from Movable is mostly handled by apply_physics_update directly for PhysicsBody."""
        pass

    def get_collision_shape(self) -> CircleShape:
        """Returns the circle's shape for collision detection."""
        return self._shape

    def resolve_collision(self, other: 'Collision'):
        """
        Calculates collision resolution (position correction and velocity impulse)
        and stores them in pending variables. Does NOT apply changes immediately.
        """
        if isinstance(other, GravityCircle):
            other_circle = other
            distance = self.position.distance_to(other_circle.position)
            combined_radii = self.radius + other_circle.radius

            if distance < combined_radii and distance != 0:
                overlap = combined_radii - distance
                direction = (self.position - other_circle.position).normalize()

                self._pending_position_correction += direction * (overlap / 2)
                other_circle._pending_position_correction -= direction * (overlap / 2)

                relative_velocity = self.velocity - other_circle.velocity
                velocity_along_normal = relative_velocity.dot(direction)

                if velocity_along_normal < 0:
                    e = min(self.restitution, other_circle.restitution)
                    j = -(1 + e) * velocity_along_normal
                    j /= (1 / self.mass) + (1 / other_circle.mass)

                    impulse = j * direction
                    self._pending_velocity_change += impulse / self.mass
                    other_circle._pending_velocity_change -= impulse / other_circle.mass

    def get_mass(self) -> float:
        """Returns the mass of the circle."""
        return self.mass


    def calculate_physics(self, delta_time: float, scenario: Scenario):
        """
        Phase 1: Accumulates forces and calculates collision effects.
        Does NOT modify position or velocity directly.
        """

        if hasattr(scenario, 'local_gravity_handler') and isinstance(scenario.local_gravity_handler, LocalGravity):
            gravity_force = self.get_mass() * scenario.local_gravity_handler.gravity_vector
            self.apply_force(gravity_force, delta_time)

        self._pending_velocity_change = pygame.Vector2(0, 0)
        self._pending_position_correction = pygame.Vector2(0, 0)

        for other_entity in scenario.entity_manager.get_entities():
            if other_entity is not self and isinstance(other_entity, Collision):
                if self.get_collision_shape().intersects(other_entity.get_collision_shape(), self.position, other_entity.position):
                    self.resolve_collision(other_entity)

    def update(self, delta_time: float, scenario: Scenario):
        """
        Phase 2: Applies accumulated forces, pending collision changes,
        and moves the entity. Handles screen border collisions.
        """
        if self.mass > 0:
            acceleration = self._net_force_accumulated / self.mass
            self.velocity += acceleration * delta_time
        self._net_force_accumulated = pygame.Vector2(0, 0)

        self.velocity += self._pending_velocity_change
        self.position += self._pending_position_correction

        self.position += self.velocity * delta_time

        screen_rect = scenario.display_surface.get_rect()

        if self.position.x - self.radius < screen_rect.left:
            self.position.x = screen_rect.left + self.radius
            self.velocity.x *= -self.restitution
            if abs(self.velocity.x) < 0.1: self.velocity.x = 0
        if self.position.x + self.radius > screen_rect.right:
            self.position.x = screen_rect.right - self.radius
            self.velocity.x *= -self.restitution
            if abs(self.velocity.x) < 0.1: self.velocity.x = 0
        if self.position.y - self.radius < screen_rect.top:
            self.position.y = screen_rect.top + self.radius
            self.velocity.y *= -self.restitution
            if abs(self.velocity.y) < 0.1: self.velocity.y = 0
        if self.position.y + self.radius > screen_rect.bottom:
            self.position.y = screen_rect.bottom - self.radius
            self.velocity.y *= -self.restitution
            if abs(self.velocity.y) < 0.1: self.velocity.y = 0

    def render(self, surface: pygame.Surface):
        """Renders the circle on the screen."""
        self._shape.render_shape(surface, self.position, self.color)