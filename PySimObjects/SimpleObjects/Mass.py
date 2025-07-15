from abc import abstractmethod, ABC

class Mass(ABC):
    def __init__(self, mass: float):
        if mass <= 0:
            raise ValueError("Mass must be a positive value.")
        self.mass = mass

    @abstractmethod
    def get_mass(self) -> float:
        """Returns the mass of the entity."""
        pass