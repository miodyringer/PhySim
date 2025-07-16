import pygame

# Import necessary classes
from PhySimEngine.Scenario import Scenario # For game context (e.g., accessing global_gravity_handler)
from PhySimObjects.SimpleObjects.Orbital import Orbital # Inherit from our new Orbital base
from PhySimObjects.SimpleObjects.Collision import Collision # For type hinting resolve_collision
from PhySimObjects.CircleShape import CircleShape
from PhySimObjects.PhysicsHandlers.GlobalGravity import GlobalGravity


class CircleOrbital(Orbital):
    """
    A circular entity that participates in global orbital mechanics,
    is movable, collidable, has mass, and can receive forces.
    """
    def __init__(self, x: int, y: int, radius: float, color: tuple,
                 initial_velocity: pygame.Vector2, mass: float = 1.0,
                 restitution: float = 0.8):
        super().__init__(x=x, y=y, velocity=initial_velocity, mass=mass,
                         shape=CircleShape(radius), restitution=restitution)

        self.color = color
        self.radius = radius


    def get_collision_shape(self) -> CircleShape:
        return self.shape

    def resolve_collision(self, other: 'Collision'):
        if isinstance(other, CircleOrbital):
            other_circle = other
            distance = self.position.distance_to(other_circle.position)
            combined_radii = self.radius + other_circle.radius

            if distance < combined_radii and distance != 0:
                overlap = combined_radii - distance
                direction = (self.position - other_circle.position).normalize()

                self.pending_position_correction += direction * (overlap / 2)
                other_circle.pending_position_correction -= direction * (overlap / 2)

                relative_velocity = self.velocity - other_circle.velocity
                velocity_along_normal = relative_velocity.dot(direction)

                if velocity_along_normal < 0:
                    e = min(self.restitution, other_circle.restitution)
                    j = -(1 + e) * velocity_along_normal
                    j /= (1 / self.mass) + (1 / other_circle.mass)

                    impulse = j * direction
                    self.pending_velocity_change += impulse / self.mass
                    other_circle.pending_velocity_change -= impulse / other_circle.mass


    def calculate_physics(self, delta_time: float, scenario: Scenario):
        if hasattr(scenario, 'global_gravity_handler') and isinstance(scenario.global_gravity_handler, GlobalGravity):
            for other_entity in scenario.entity_manager.get_entities():
                if other_entity is not self and isinstance(other_entity, CircleOrbital) and other_entity.get_mass() > 0:
                    grav_force = scenario.global_gravity_handler.calculate_gravitational_force(
                        self.position, self.get_mass(),
                        other_entity.position, other_entity.get_mass()
                    )
                    self.apply_force(grav_force, delta_time)

        self.pending_velocity_change = pygame.Vector2(0, 0)
        self.pending_position_correction = pygame.Vector2(0, 0)

        for other_entity in scenario.entity_manager.get_entities():
            if other_entity is not self and isinstance(other_entity, Collision):
                if self.get_collision_shape().intersects(other_entity.get_collision_shape(), self.position, other_entity.position):
                    self.resolve_collision(other_entity)

    def update(self, delta_time: float, scenario: Scenario):
        if self.mass > 0:
            acceleration = self.force_accumulated / self.mass
            self.velocity += acceleration * delta_time
        self.force_accumulated = pygame.Vector2(0, 0)

        self.velocity += self.pending_velocity_change
        self.position += self.pending_position_correction

        self.position += self.velocity * delta_time

    def render(self, surface: pygame.Surface):
        self.shape.render_shape(surface, self.position, self.color)
        pygame.draw.circle(surface, self.color, self.position, int(self.radius / (0.05) ** 0.5), 1)