import pygame

class LocalGravity:
    """Handles constant acceleration due to local gravity."""
    def __init__(self, gravity_vector: pygame.Vector2):
        """
        Initializes the local gravity handler.
        :param gravity_vector: A pygame.Vector2 representing the acceleration).
        """
        self.gravity_vector = gravity_vector

    def apply_gravity(self, entity_velocity: pygame.Vector2, delta_time: float) -> pygame.Vector2:
        """
        Calculates the change in velocity due to gravity over a delta_time.
        :param entity_velocity: The current velocity of the entity.
        :param delta_time: Time in seconds since the last update.
        :return: The updated velocity after applying gravity.
        """
        return entity_velocity + (self.gravity_vector * delta_time)