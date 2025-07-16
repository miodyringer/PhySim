from abc import abstractmethod, ABC
import pygame

from PhySimEngine.Entity import Entity


class ApplyForce(ABC):
    @abstractmethod
    def get_applied_force(self, target_entity: Entity) -> pygame.Vector2:
        """
        Calculates and returns the force exerted on a target entity.
        :param target_entity: The entity to apply the force to.
        :return: The applied force.
        """
        pass

    @abstractmethod
    def get_force_origin(self) -> pygame.Vector2:
        """
        Returns the point from which the force originates.
        :return: The origin of the force.
        """
        pass