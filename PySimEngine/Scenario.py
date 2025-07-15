from abc import abstractmethod, ABC

import pygame

from PySimEngine.EntityManager import EntityManager
from PySimEngine.InputManager import InputManager


class Scenario(ABC):
    """
    The abstract base class for any game built with this framework.
    It handles the main game loop and system management. The user only needs to
    inherit from this class and implement the abstract methods.
    """

    def __init__(self):
        config = self.configure()
        self._width = config.get("width", 800)
        self._height = config.get("height", 600)
        self._title = config.get("title", "Pygame Framework")
        self._tps = config.get("tps", 60)

        pygame.init()
        pygame.display.set_caption(self._title)
        self.display_surface = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._running = False
        self._paused = False
        self._speed = 1.0

        self.input_manager = InputManager()
        self.entity_manager = EntityManager()

        self.create_initial_entities()

    @abstractmethod
    def configure(self) -> dict:
        """
        Return a dictionary with game settings.
        Example:
        return {
            "width": 1280,
            "height": 720,
            "title": "My Awesome Game",
            "tps": 60
        }
        """
        pass

    @abstractmethod
    def create_initial_entities(self):
        """
        Use `self.entity_manager.add()` to create the starting
        objects for your game.
        """
        pass

    def stop(self):
        """Stops the game loop, leading to a clean exit."""
        self._running = False

    def pause(self):
        """Toggles the paused state of the game loop."""
        self._paused = not self._paused
        if not self._paused:
            self._clock.tick(self._tps)

    def set_speed(self, speed: float):
        """Sets the speed of the game."""
        self._speed = speed

    def run(self):
        """Starts and manages the main game loop."""
        self._running = True
        while self._running:
            raw_delta_time_ms = self._clock.tick(self._tps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            self.input_manager.update()

            if self.input_manager.is_pressed(pygame.K_SPACE):
                self.pause()
            if self.input_manager.is_pressed(pygame.K_ESCAPE):
                self.stop()
            if self.input_manager.is_pressed(pygame.K_PLUS):
                self.set_speed(self._speed + 0.2)
            if self.input_manager.is_pressed(pygame.K_MINUS):
                self.set_speed(self._speed - 0.2)

            if not self._paused:
                delta_time = self._speed * raw_delta_time_ms / 1000.0

                self.entity_manager.apply_changes()

                for entity in self.entity_manager.get_entities():
                    entity.calculate_physics(delta_time, self)

                for entity in self.entity_manager.get_entities():
                    entity.update(delta_time, self)

            self.display_surface.fill((20, 0, 30) if self._paused else (0, 20, 30))
            for entity in self.entity_manager.get_entities():
                entity.render(self.display_surface)

            pygame.display.flip()

        pygame.quit()