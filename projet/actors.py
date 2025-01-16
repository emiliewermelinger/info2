# actors.py

import pygame
from typing import Tuple
from random import randint

# Classe de base Actor
class Actor:
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, energie: int = 0, energie_max: int = 0,) -> None:
        self._position = position
        self._speed = speed
        self._dimension = (10, 10)
        self.energie = energie
        self.energie_max = energie_max
       
    def change_energie(self, delta: int) -> None:
        self.energie = max(0, min(self.energie + delta, self.energie_max))

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("each position values must be zero or positive")
        self._position = position

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    @property
    def dimension(self) -> Tuple[int, int]:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Tuple[int, int]) -> None:
        if dimension[0] <= 0 or dimension[1] <= 0:
            raise ValueError("each dimension value must be positive")
        self._dimension = dimension


# Classe Lapin
class Lapin(Actor):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, energie: int, energie_max: int) -> None:
        super().__init__(position, speed, energie, energie_max)
        self.type = 'Lapin'  # Propriété spécifique au lapin
       

# Classe Renard
class Renard(Actor):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, energie: int, energie_max: int) -> None:
        super().__init__(position, speed, energie, energie_max)
        self.type = 'Renard'  # Propriété spécifique au renard


# Classe Plante
class Plante(Actor):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, speed, energie=0, energie_max=0)
        self.type = 'Plante'  # Propriété spécifique à la plante
