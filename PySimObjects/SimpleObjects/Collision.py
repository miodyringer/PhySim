from abc import abstractmethod, ABC


class Collision(ABC):
    def __init__(self, shape: 'Shape'):
        self.shape = shape

    @abstractmethod
    def get_collision_shape(self) -> 'Shape':
        pass

    @abstractmethod
    def resolve_collision(self, other: 'Collidable'):
        pass