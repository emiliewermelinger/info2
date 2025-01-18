# actors.py
#modifié
import pygame
from typing import Tuple
from random import randint

# Classe de base Vivant
class Vivant:
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, energie: int = 0, energie_max: int = 0) -> None:
        self._position = position
        self._speed = speed
        self._dimension = (10, 10)
        self.energie = energie
    
       
    def change_energie(self, delta: int) -> None:
        self.energie = max(0, min(self.energie + delta, self.energie_max))

    def vieillir(self):
        """Augmente l'âge de l'entité et retourne False si elle dépasse son âge maximal."""
        self.age += 1
        return self.age <= self.age_max or self.age_max == 0  # 0 pour plantes qui vivent éternellement


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

class Mammifères(Vivant):
   def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, energie: int = 0, energie_max: int = 0) -> None:
        self._position = position
        self._speed = speed
        self._dimension = (10, 10)
        self.energie = energie
        self.energie_max = energie_max
        self.age = 0
        self.age_max = self.age_max


# Classe Lapin
class Lapin(Vivant):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2,energie: int, energie_max: int) -> None:
        super().__init__(position, speed, energie=10, energie_max=20, age_max=5)
        self.type = 'Lapin'  # Propriété spécifique au lapin
       

# Classe Renard
class Renard(Mammifères):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, energie: int, energie_max: int) -> None:
        super().__init__(position, speed, energie=25, energie_max=50, age_max=3)
        self.type = 'Renard'  # Propriété spécifique au renard


# Classe Plante
class Plante(Mammifères):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
  # Appel à Actor avec énergie initiale et maximale fixées à 0
        super().__init__(position, speed, energie=0, energie_max=0)
        self.type = 'Plante'
        self.energie_fournie = 3  # Énergie donnée quand mangée par un lapin