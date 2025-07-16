from abc import abstractmethod, ABC

from PhySimObjects.SimpleObjects.Shape import Shape


class Collision(ABC):
    def __init__(self, shape: Shape):
        self.shape = shape

    @abstractmethod
    def get_collision_shape(self) -> Shape:
        """Returns the shape of the collision object.
        :returns: the shape of the collision object"""
        pass

    @abstractmethod
    def resolve_collision(self, other: 'Collision'):
        """Resolves collision between this object and another object."""
        pass