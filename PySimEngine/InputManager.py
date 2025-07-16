import pygame


class InputManager:
    """Manages keyboard input states."""
    def __init__(self):
        self.current_keys = pygame.key.get_pressed()
        self.last_keys = self.current_keys

    def update(self):
        """Updates the keyboard input."""
        self.last_keys = self.current_keys
        self.current_keys = pygame.key.get_pressed()

    def is_pressed(self, key_code) -> bool:
        """
        Checks if a key is pressed.
        :param key_code: The key code to check.
        :return: True if the key is pressed, False otherwise.
        """
        return self.current_keys[key_code] and not self.last_keys[key_code]

    def is_released(self, key_code) -> bool:
        """
        Checks if a key is released.
        :param key_code: The key code to check.
        :return: True if the key is released, False otherwise.
        """
        return not self.current_keys[key_code] and self.last_keys[key_code]

    def is_held(self, key_code) -> bool:
        """
        Checks if a key is held.
        :param key_code: The key code to check.
        :return: The key is held, False otherwise.
        """
        return self.current_keys[key_code]