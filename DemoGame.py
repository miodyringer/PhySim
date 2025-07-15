from PySimEngine.Game import Game
from PySimObjects.Orbital import Orbital


class DemoGame(Game):

    def custom_updates(self):
        Orbital.update_all_physics()

    def configure(self) -> dict:
        return {
            "width": 1024,
            "height": 768,
            "title": "Physics Demo",
            "tps": 60
        }

    def create_initial_entities(self):
        sun = Orbital(x=512, y=384, mass=10000, color=(255, 255, 0), velocity=(10, 0))
        planet1 = Orbital(x=312, y=384, mass=100, color=(0, 150, 255), velocity=(0, -500))
        planet2 = Orbital(x=712, y=384, mass=100, color=(200, 200, 200), velocity=(0, 500))

        self.entity_manager.add(sun)
        self.entity_manager.add(planet1)
        self.entity_manager.add(planet2)

if __name__ == "__main__":
    my_game = DemoGame()
    my_game.run()