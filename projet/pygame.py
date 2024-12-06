import projet.pygame as pygame
from sys import exit
from typing import Dict,Tuple


WINDOW_SIZE : Tuple[int,int] =(480,360)
WINDOW_TITLE: str= "pygame"

colors:Dict ={
    "White":(255,255,255),
}

def init_screen() -> pygame.Surface:
    screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    return screen

def handle_events(event)->None:
    if event.type==pygame.QUIT:
        pygame.quit()
        exit()

def execute()->None:
    pygame.init()
    screen= init_screen()
    running= True
    while running:
        for event in pygame.event.get():
            handle_events(event)
            pygame.draw.rect(screen,colors["white"], (210,160,60,40))
       





