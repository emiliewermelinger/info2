# actors.py

import pygame
from typing import Tuple
from random import randint

WINDOW_SIZE = (400, 400)

class Vivant:
    def __init__(self, position: pygame.Vector2, energie: int, energie_max: int = None, speed: pygame.Vector2 = pygame.Vector2(0, 0) ) -> None:
        self._position = position
        self._dimension = (10, 10)
        self.energie = energie
        self.energie_max = energie_max
        self._speed = speed
        self._disappear = False  
       
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
        self.age = 0
        self.age_max = age_max
        self.energie_max = energie_max      

    def augmenter_age(self) -> None:
        self.age += 1

class Lapin(Mammifere):
    def __init__(self, position: pygame.Vector2, speed:pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1)), energie: int = 10, energie_max: int = 20) -> None:
        super().__init__(position, energie, energie_max, age_max = 5)
        self._speed = speed
        
    def get_speed(self) -> pygame.Vector2:
        return pygame.Vector2(randint(-1, 1), randint(-1, 1))     

    def deplacer(self, energy_per_step: int = 1) -> None:
        self._position += self.speed
        self.change_energie(-energy_per_step)  
    
    def rencontrer_plante(self, plante) -> None:
        plante_actor = plante._actor
        if self.energie < self.energie_max:  
            self.change_energie(plante_actor.energie)  
            plante._actor.change_energie(-plante._actor.energie)  
            plante_actor.disparaitre() 

    def rencontrer_lapin(self, autre_lapin) -> list:
        self.reproduire() 
        return randint(1, 3)
    
    def reproduire(self) -> None:
        self.change_energie(-2)  

class Renard(Mammifere):
    def __init__(self, position: pygame.Vector2,speed = pygame.Vector2(randint(-2, 2), randint(-2, 2)), energie: int = 25, energie_max: int = 50) -> None:
        super().__init__(position, energie, energie_max , age_max = 3, speed = speed)

    def get_speed(self) -> pygame.Vector2:
        return pygame.Vector2(randint(-2, 2), randint(-2, 2))      
        
    def deplacer(self, energy_per_step: int = 3) -> None:
        self._position += self.speed
        self.change_energie(-energy_per_step)
    
    def rencontrer_lapin(self, lapin) -> None:
        if self.energie < self.energie_max:  
            self.change_energie(lapin.energie) 
            lapin.change_energie(-lapin.energie) 
            lapin.disparaitre()
    
    def rencontrer_renard(self, autre_renard) -> None:
        self.reproduire()  
        return randint(1, 5)
    
    def reproduire(self) -> None:
        self.change_energie(-3)  
        
class Plante(Vivant):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, energie = 3, energie_max = None)

    def change_energie(self, delta: int) -> None:
            super().change_energie(delta)
            if self.energie == 0:
                self.disparaitre()