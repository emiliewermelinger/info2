# actors.py

import pygame
from typing import Tuple
from random import randint

WINDOW_SIZE = (400, 400)


# Classe de base Actor
class Vivant:
    def __init__(self, position: pygame.Vector2, energie: int, energie_max: int = None, speed: pygame.Vector2 = pygame.Vector2(0, 0) ) -> None:
        self._position = position
        self._dimension = (10, 10)
        self.energie = energie
        self.energie_max = energie_max
        self._speed = speed
        self._disappear = False  # Initialiser _disappear à False
       
    def change_energie(self, delta: int) -> None:
        if self.energie_max is not None:
            self.energie = max(0,min(self.energie_max, self.energie+ delta))
        else :
            self.energie = max(0, self.energie + delta)
        if  self.energie == 0:
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
    def __init__(self, position: pygame.Vector2, energie: int, energie_max: int, age_max: int, speed: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        super().__init__(position, energie, speed)
        self.type = 'Mammifère'
        self.age = 0
        self.age_max = age_max
        self.energie_max = energie_max

    
    def deplacer(self, max_steps: int, energy_per_step: int = 1) -> pygame.Vector2:
        steps_x = randint(-max_steps, max_steps)
        steps_y = randint(-max_steps, max_steps)
        speed = pygame.Vector2(steps_x, steps_y)
        self._position += speed  # Déplacer l'acteur
        self.change_energie(-energy_per_step)
        

       

    def augmenter_age(self) -> None:
        """Incrémente l'âge de l'acteur"""
        if self.age < self.age_max:
            self.age += 1  # Augmente l'âge de l'acteur

    

    def reproduire(self) -> None:
        """Quand un mammifère se reproduit, il perd 3 points d'énergie."""
        self.change_energie(-6)  # Perdre 3 points d'énergie lors de la reproduction


# Classe Lapin
class Lapin(Mammifere):
    def __init__(self, position: pygame.Vector2, speed:pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1)), energie: int = 10, energie_max: int = 20) -> None:
        super().__init__(position, energie, energie_max, age_max = 5)
        self._speed = speed

    def get_speed(self) -> pygame.Vector2:
        """Retourne la vitesse du renard : déplacement d'au plus deux cases."""
        return pygame.Vector2(randint(-1, 1), randint(-1, 1))

        

    def deplacer(self, max_steps: int = 1, energy_per_step: int = 2) -> None:
        self._position += self.speed
        self.change_energie(-energy_per_step)
        
         
    
    
    def rencontrer_plante(self, plante) -> None:
        plante_actor = plante._actor
        if self.energie < self.energie_max:  # Vérifie si le lapin a de la place pour plus d'énergie
            self.change_energie(plante_actor.energie)  # Le lapin acquiert l'énergie de la plante
            plante._actor.change_energie(-plante._actor.energie)  # La plante est mangée (son énergie devient 0)
            plante_actor.disparaitre() 

    def rencontrer_lapin(self, autre_lapin) -> list:
        """Quand un lapin rencontre un autre lapin, ils se reproduisent et créent de 1 à 3 nouveaux lapins."""
        self.reproduire()  # Le lapin perd de l'énergie lors de la reproduction
        return randint(1, 3)

# Classe Renard
class Renard(Mammifere):
    def __init__(self, position: pygame.Vector2,speed = pygame.Vector2(randint(-2, 2), randint(-2, 2)), energie: int = 25, energie_max: int = 50) -> None:
        super().__init__(position, energie, energie_max , age_max = 3, speed = speed)
    
    def get_speed(self) -> pygame.Vector2:
        """Retourne la vitesse du lapin : déplacement d'au plus une case."""
        return pygame.Vector2(randint(-2, 2), randint(-2, 2))
        
        
    def deplacer(self, max_steps: int = 1, energy_per_step: int = 1) -> None:
        self._position += self.speed
        self.change_energie(-energy_per_step)
        


    def rencontrer_lapin(self, lapin) -> None:
        if self.energie < self.energie_max:  # Vérifie si le renard a de la place pour plus d'énergie
            self.change_energie(lapin.energie) 
            lapin.change_energie(-lapin.energie)  # Le lapin est mangé (son énergie devient 0)
            lapin.disparaitre()
    
    def rencontrer_renard(self, autre_renard) -> None:
        """Quand un renard rencontre un autre renard, ils se reproduisent et créent de 1 à 5 nouveaux renards."""
        self.reproduire()  # Le renard perd de l'énergie lors de la reproduction
        return randint(1, 5)
        


# Classe Plante
class Plante(Vivant):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, energie = 3, energie_max = None)
        self.type = 'Plante'  # Propriété spécifique à la plante

    def change_energie(self, delta: int) -> None:
            super().change_energie(delta)
            if self.energie == 0:
                self.disparaitre()