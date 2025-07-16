import random

import pygame

from PySimEngine.Scenario import Scenario
from PySimObjects.CircleOrbital import CircleOrbital
from PySimObjects.GravityCircle import GravityCircle
from PySimObjects.PhysicsHandlers.GlobalGravity import GlobalGravity


class GravityDemo(Scenario):

    def __init__(self):
        self.global_gravity_handler = GlobalGravity(gravitational_constant=0.1)
        super().__init__()

    def configure(self) -> dict:
        return {
            "width": 1280,
            "height": 720,
            "title": "Orbital Collision Demo",
            "tps": 300
        }

    def create_initial_entities(self):
        central_x = self.width / 2
        central_y = self.height / 2
        self.entity_manager.add(
            CircleOrbital(
                x=central_x,
                y=central_y,
                radius=60,
                color=(255, 255, 0),
                initial_velocity=pygame.Vector2(0, 0),
                mass=100000000,
                restitution=0.5
            )
        )

        for i in range(10):
            self.entity_manager.add(
                CircleOrbital(
                    x=random.randint(100, 700),
                    y=random.randint(100, 700),
                    radius=random.randint(10, 25),
                    color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                    initial_velocity=pygame.Vector2(random.randint(0, 100), random.randint(0, 100)),
                    mass=random.uniform(5, 50),
                    restitution=0.5
                )
            )

if __name__ == "__main__":
    game = GravityDemo()
    game.run()