# Demos/ForceFieldDemo.py
import pygame
import random

from PySimEngine.Scenario import Scenario
from PySimObjects.ForceFieldCircle import ForceFieldCircle
from PySimObjects.SimpleObjects.ForceField import ForceField


class ForceFieldDemo(Scenario):
    """
    A demo scenario showcasing AttractedCircle entities being affected by ForceField objects.
    """

    def configure(self) -> dict:
        return {
            "width": 1280,
            "height": 720,
            "title": "Force Field Demo",
            "tps": 60
        }

    def create_initial_entities(self):
        self.entity_manager.add(
            ForceField(x=200, y=300, radius=150, strength=500, direction_vector=pygame.Vector2(1, 0),
                       color=(255, 150, 0)))
        self.entity_manager.add(
            ForceField(x=1000, y=300, radius=150, strength=500, direction_vector=pygame.Vector2(-0.7, 0.7),
                       color=(0, 200, 255)))
        self.entity_manager.add(
            ForceField(x=640, y=100, radius=100, strength=700, direction_vector=pygame.Vector2(0, -1),
                       color=(255, 0, 200)))
        self.entity_manager.add(
            ForceField(x=640, y=600, radius=100, strength=700, direction_vector=pygame.Vector2(0, 1),
                       color=(0, 255, 100)))

        num_circles = 25
        for i in range(num_circles):
            start_x = random.randint(50, self.width - 50)
            start_y = random.randint(50, self.height - 50)
            initial_vel_x = random.uniform(-50, 50)
            initial_vel_y = random.uniform(-50, 50)

            mass = random.uniform(5, 20)
            radius = int(8 + mass * 0.5)

            self.entity_manager.add(
                ForceFieldCircle(
                    x=start_x,
                    y=start_y,
                    radius=radius,
                    color=(random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)),
                    initial_velocity=pygame.Vector2(initial_vel_x, initial_vel_y),
                    mass=mass,
                    restitution=0.7
                )
            )

    def custom_updates(self):
        pass


if __name__ == "__main__":
    game = ForceFieldDemo()
    game.run()