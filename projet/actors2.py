# actors.py

import pygame
from typing import Tuple
from random import randint

# Classe de base Actor
class Vivant:
    def __init__(self, position: pygame.Vector2, energie: int, energie_max: int = None) -> None:
        self._position = position
        self._dimension = (10, 10)
        self.energie = energie
        self.energie_max = energie_max
        self._speed = pygame.Vector2(0, 0)
        self._disappear = False  # Initialiser _disappear à False
       
    def change_energie(self, delta: int) -> None:
        self.energie = max(0,min(self.energie_max, self.energie+ delta))
        if self.energie == 0:
            self.disparaitre()

    
    def disparaitre(self) -> None:
        self._disappear = True

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

class Mammifere(Vivant):
    def __init__(self, position: pygame.Vector2, energie: int, energie_max: int, age_max: int) -> None:
        super().__init__(position, energie, energie_max)
        self.type = 'Mammifère'
        self.age = 0
        self.age_max = age_max
        self.energie_max = energie_max

    def augmenter_age(self) -> None:
        """Incrémente l'âge de l'acteur"""
        if self.age < self.age_max:
            self.age += 1  # Augmente l'âge de l'acteur

    def deplacer(self) -> None:
        """Déplace l'acteur en fonction de sa vitesse et modifie son énergie."""
        self._position += self._speed
        self.change_energie(-2)  # Perdre 2 points d'énergie à chaque déplacement

    def reproduire(self) -> None:
        """Quand un mammifère se reproduit, il perd 3 points d'énergie."""
        self.change_energie(-3)  # Perdre 3 points d'énergie lors de la reproduction


# Classe Lapin
class Lapin(Mammifere):
    def __init__(self, position: pygame.Vector2, energie: int = 10, energie_max: int = 20) -> None:
        super().__init__(position, energie, energie_max, age_max = 5)
        self.speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
    
    
    def rencontrer_plante(self, plante) -> None:
        if self.energie < self.energie_max:  # Vérifie si le lapin a de la place pour plus d'énergie
            self.change_energie(3)  # Le lapin acquiert l'énergie de la plante
            plante.change_energie(-plante.energie)  # La plante est mangée (son énergie devient 0)

    def rencontrer_lapin(self, autre_lapin) -> list:
        """Quand un lapin rencontre un autre lapin, ils se reproduisent et créent de 1 à 3 nouveaux lapins."""
        self.reproduire()  # Le lapin perd de l'énergie lors de la reproduction
        return [Lapin(position=self._position) for _ in range(randint(1, 3))]

# Classe Renard
class Renard(Mammifere):
    def __init__(self, position: pygame.Vector2, energie: int = 25, energie_max: int = 50) -> None:
        super().__init__(position, energie, energie_max , age_max = 3)
        self.speed = pygame.Vector2(randint(-2, 2), randint(-2, 2))

    

    def rencontrer_lapin(self, lapin) -> None:
        if self.energie < self.energie_max:  # Vérifie si le renard a de la place pour plus d'énergie
            self.change_energie(lapin.energie) 
            lapin.change_energie(-lapin.energie)  # Le lapin est mangé (son énergie devient 0)
            lapin.disparaitre()
    
    def rencontrer_renard(self, autre_renard) -> None:
        """Quand un renard rencontre un autre renard, ils se reproduisent et créent de 1 à 5 nouveaux renards."""
        self.reproduire()  # Le renard perd de l'énergie lors de la reproduction
        return [Renard(position=self._position) for _ in range(randint(1, 5))]


# Classe Plante
class Plante(Vivant):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, energie = 3)
        self.type = 'Plante'  # Propriété spécifique à la plante

    def change_energie(self, delta: int) -> None:
            super().change_energie(delta)
