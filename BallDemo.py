from random import random

import pygame

from PySimEngine.Scenario import Scenario
from PySimObjects.GravityCircle import GravityCircle
from PySimObjects.PhysicsHandlers.LocalGravity import LocalGravity


class BallDemo(Scenario):

    def __init__(self):
        super().__init__()
        self.local_gravity_handler = LocalGravity(pygame.Vector2(0, 300))

    def configure(self) -> dict:
        return {
            "width": 1024,
            "height": 768,
            "title": "Physics Demo",
            "tps": 60
        }

    def create_initial_entities(self):
        for i in range(100):
            ball = GravityCircle(random() * 1024, random() * 768, 10, (random() * 255, random() * 255, random() * 255),
                                  pygame.Vector2(random() * 100, random() * 100), mass=1.0, restitution=0.3)
            self.entity_manager.add(ball)

if __name__ == "__main__":
    my_game = BallDemo()
    my_game.run()