import pygame


class InputManager:
    """Manages keyboard input states."""
    def __init__(self):
        self._current_keys = pygame.key.get_pressed()
        self._last_keys = self._current_keys

    def update(self):
        self._last_keys = self._current_keys
        self._current_keys = pygame.key.get_pressed()

    def is_pressed(self, key_code) -> bool:
        return self._current_keys[key_code] and not self._last_keys[key_code]

    def is_released(self, key_code) -> bool:
        return not self._current_keys[key_code] and self._last_keys[key_code]

    def is_held(self, key_code) -> bool:
        return self._current_keys[key_code]