"""import pygame
from typing import Callable

class CycleManager:
    def __init__(self, duration: int, callback: Callable) -> None:
        """
        #Initialise un cycle.
        #:param duration: Durée du cycle (en nombre de frames).
        #:param callback: Fonction appelée à la fin de chaque cycle.
        #"""
        #self.duration = duration
        #self.callback = callback
        #self.current_frame = 0

    #def update(self) -> None:
        #"""
        #Met à jour le compteur de frames et appelle le callback à la fin du cycle.
        #"""
        #self.current_frame += 1
        #if self.current_frame >= self.duration:
           # self.callback()
           # self.current_frame = 0
