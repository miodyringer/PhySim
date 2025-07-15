# PySimObjects/SimpleObjects/OrbitalCircle.py
import pygame

# Import necessary classes
from PySimEngine.Scenario import Scenario # For game context (e.g., accessing global_gravity_handler)
from PySimObjects.SimpleObjects.Orbital import Orbital # Inherit from our new Orbital base
from PySimObjects.SimpleObjects.Collision import Collision # For type hinting resolve_collision
from PySimObjects.CircleShape import CircleShape
from PySimObjects.PhysicsHandlers.GlobalGravity import GlobalGravity


class CircleOrbital(Orbital):
    """
    A circular entity that participates in global orbital mechanics,
    is movable, collidable, has mass, and can receive forces.
    """
    def __init__(self, x: float, y: float, radius: float, color: tuple,
                 initial_velocity: pygame.Vector2, mass: float = 1.0,
                 restitution: float = 0.8):
        # Initialize Orbital (which in turn calls its parents including Entity)
        super().__init__(x=x, y=y, velocity=initial_velocity, mass=mass,
                         shape=CircleShape(radius), restitution=restitution)

        self.color = color
        self.radius = radius # Redundant but kept for direct access if needed


    # --- Implementations for Collision ---
    def get_collision_shape(self) -> CircleShape:
        """Returns the circle's shape for collision detection."""
        return self.shape # 'shape' is set in Orbital's __init__ via Collision.__init__

    def resolve_collision(self, other: 'Collision'):
        """
        Calculates collision resolution (position correction and velocity impulse)
        and stores them in pending variables. Does NOT apply changes immediately.
        """
        # Ensure 'other' is an OrbitalCircle to access its specific physics properties
        if isinstance(other, CircleOrbital):
            other_circle = other
            distance = self.position.distance_to(other_circle.position)
            combined_radii = self.radius + other_circle.radius

            # Collision detected and not directly on top of each other
            if distance < combined_radii and distance != 0:
                # Calculate separation for position correction
                overlap = combined_radii - distance
                direction = (self.position - other_circle.position).normalize()

                # Store pending position corrections for both circles
                self._pending_position_correction += direction * (overlap / 2)
                other_circle._pending_position_correction -= direction * (overlap / 2)

                # Relative velocity before collision
                relative_velocity = self.velocity - other_circle.velocity
                # Velocity component along the collision normal
                velocity_along_normal = relative_velocity.dot(direction)

                # Only resolve if objects are moving towards each other
                if velocity_along_normal < 0:
                    # Calculate impulse scalar using coefficient of restitution
                    e = min(self.restitution, other_circle.restitution) # Use minimum restitution for inelastic collision
                    j = -(1 + e) * velocity_along_normal
                    j /= (1 / self.mass) + (1 / other_circle.mass)

                    # Store pending velocity changes (impulses) for both circles
                    impulse = j * direction
                    self._pending_velocity_change += impulse / self.mass
                    other_circle._pending_velocity_change -= impulse / other_circle.mass


    # --- Implementations for Entity's calculate_physics method (Phase 1) ---
    def calculate_physics(self, delta_time: float, scenario: Scenario):
        """
        Phase 1: Accumulates forces (including global gravity) and calculates collision effects.
        Does NOT modify position or velocity directly.
        """
        # 1. Apply global gravity from other orbital bodies
        if hasattr(scenario, 'global_gravity_handler') and isinstance(scenario.global_gravity_handler, GlobalGravity):
            for other_entity in scenario.entity_manager.get_entities():
                # Only apply gravity from other OrbitalCircle instances that have mass
                if other_entity is not self and isinstance(other_entity, CircleOrbital) and other_entity.get_mass() > 0:
                    grav_force = scenario.global_gravity_handler.calculate_gravitational_force(
                        self.position, self.get_mass(),
                        other_entity.position, other_entity.get_mass()
                    )
                    self.apply_force(grav_force, delta_time) # Accumulate gravity force via ReceiveForce

        # 2. Reset pending changes from the *previous* frame's resolution
        self._pending_velocity_change = pygame.Vector2(0, 0)
        self._pending_position_correction = pygame.Vector2(0, 0)

        # 3. Detect and calculate collision resolutions with other entities
        # This loop only *calculates* the changes and stores them in pending variables.
        # It does not apply them yet.
        for other_entity in scenario.entity_manager.get_entities():
            if other_entity is not self and isinstance(other_entity, Collision):
                # Check for intersection using the shape's intersects method
                if self.get_collision_shape().intersects(other_entity.get_collision_shape(), self.position, other_entity.position):
                    self.resolve_collision(other_entity) # This fills _pending_velocity_change and _pending_position_correction

    # --- Implementations for Entity's apply_physics_update method (Phase 2) ---
    def update(self, delta_time: float, scenario: Scenario):
        """
        Phase 2: Applies accumulated forces, pending collision changes,
        and moves the entity. Handles screen border collisions.
        """
        # 1. Apply accumulated forces to update acceleration and then velocity
        if self.mass > 0:
            acceleration = self._net_force_accumulated / self.mass
            self.velocity += acceleration * delta_time
        self._net_force_accumulated = pygame.Vector2(0, 0) # Reset for next frame

        # 2. Apply pending velocity changes from collisions (impulses)
        self.velocity += self._pending_velocity_change

        # 3. Apply pending position corrections from collisions (separation)
        self.position += self._pending_position_correction

        # 4. Apply general movement (velocity to position)
        self.position += self.velocity * delta_time

    # --- Entity's render method ---
    def render(self, surface: pygame.Surface):
        """Renders the circle on the screen."""
        self.shape.render_shape(surface, self.position, self.color)