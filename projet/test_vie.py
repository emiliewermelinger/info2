import pygame
from random import randint
from sys import exit
from typing import List, Tuple
from actors2 import *

WINDOW_SIZE: Tuple[int, int] = (400, 400)
WINDOW_TITLE: str = "pygame window 12"
FPS =12

class ActorSprite(pygame.sprite.Sprite):
    _surface: pygame.Surface
    _actor: Vivant
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(self, surface: pygame.Surface, actor: Vivant, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self._surface = surface
        self._actor = actor
        self._set_color(color_name)
        self._set_image()
        self._set_rect()

    @property
    def color(self) -> pygame.Color:
        return self._color

    def _set_color(self, color_name: str) -> None:
        if color_name not in pygame.color.THECOLORS.keys():
            raise ValueError("color must be in list of pygame.Color")
        self._color = pygame.Color(color_name)

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def _set_image(self) -> None:
        image: pygame.Surface = pygame.Surface(self._actor.dimension)
        image.fill(pygame.Color("black"))
        image.set_colorkey(pygame.Color("black"))
        image.set_alpha(255)
        pygame.draw.rect(image, self.color, ((0, 0), image.get_size()), 5)
        self._image = image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._actor.position, self.image.get_size())
        self._rect = rect

    def test_touching_surface_boundaries(self) -> bool:
        
        touch_boundaries = False
        if not self._surface.get_rect().collidepoint(self.rect.topleft):
            touch_boundaries = True
        if self.rect.left < 0:
            self.rect.move_ip(1, 0)
        if self.rect.right > self._surface.get_width():
            self.rect.move_ip(-1, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, 1)
        if self.rect.bottom > self._surface.get_height():
            self.rect.move_ip(0, -1)
        return touch_boundaries

    def update(self) -> None:
        pass

class ActorSpriteDrivenByRandom(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Vivant, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, color_name, *groups)
        self.change_direction_timer=24
        self._actor.speed = self._actor.get_speed()
        
    def update(self):
        self.change_direction_timer-=1
        if self.change_direction_timer<=0:
            self._actor.speed=self._actor.get_speed()
            self.change_direction_timer=24
        new_position = self.rect.move(self._actor.speed)
        new_position.x = max(0, min(new_position.x, self._surface.get_width() - self.rect.width))
        new_position.y = max(0, min(new_position.y, self._surface.get_height() - self.rect.height))
        self.rect.topleft = new_position.topleft
        self._actor.position = pygame.Vector2(self.rect.topleft)
        self._actor.deplacer()
        if self._actor.energie == 0:
            self.kill()

class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS

    __player_sprite: pygame.sprite.Group
    __actors_sprites: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True
        self.__cycle_count = 0  # Initialisation du compteur de cycles
        self.__max_cycles = randint(10, 50)  # Nombre aléatoire de cycles entre 10 et 50
        self.__frames_per_cycle = 12 # Nombre de frames par cycle
        self.__frame_count = 0
        self.cycle_counter = 0 
        self.display_population()

    def display_population(self):
        lapins_count = len(self.lapins)
        renards_count = len(self.renards)
        print(f"Cycle {self.__cycle_count}/{self.__max_cycles} -Population Lapins: {lapins_count}, Renards: {renards_count}")

    def __incrementer_age(self):
        for lapin in list(self.lapins):
            lapin._actor.augmenter_age()
            if lapin._actor.age >= lapin._actor.age_max:
                lapin.kill()

        for renard in list(self.renards):
            renard._actor.augmenter_age()
            if renard._actor.age >= renard._actor.age_max:
                renard.kill()    

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def ajouter_nouvel_lapin(self, lapin: Lapin) -> None:
        ActorSpriteDrivenByRandom(self.__screen, lapin, "yellow", [self.lapins, self.__actors_sprites])

    def ajouter_nouveau_renard(self, renard: Renard) -> None:
        ActorSpriteDrivenByRandom(self.__screen, renard, "orange", [self.renards, self.__actors_sprites])

    def gerer_reproduction(self, acteur, nouveaux_petits: int, type_acteur: str) -> None:
        acteur.reproduire()

        for _ in range(nouveaux_petits):
            position_libre = False
            while not position_libre:
                position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                position_libre = self.position_libre(position, self.__actors_sprites)

            if type_acteur == 'Lapin':
                nouvel_lapin = Lapin(position)
                self.ajouter_nouvel_lapin(nouvel_lapin)
            elif type_acteur == 'Renard':
                nouvel_renard = Renard(position)
                self.ajouter_nouveau_renard(nouvel_renard)
    
    def position_libre(self, position: pygame.Vector2, actors_sprites) -> bool:
        for actor in self.__actors_sprites:
            if actor._actor.position == position:
                return False  
        return True 

    def __init_actors(self) -> None:
        self.__player_sprite = pygame.sprite.Group()
        self.__actors_sprites = pygame.sprite.Group()
        self.plants = pygame.sprite.Group()  
        self.lapins = pygame.sprite.Group()  
        self.renards = pygame.sprite.Group()  

        # Plantes
        for _ in range(700): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            plante= Plante(position)
            ActorSprite(self.__screen, plante, "green", [self.plants, self.__actors_sprites])

        # Lapins
        for _ in range(520):
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
            while not self.position_libre(position, self.__actors_sprites):
                position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
        
            lapin = Lapin(position)
            ActorSpriteDrivenByRandom(self.__screen, lapin, "white", [self.lapins, self.__actors_sprites])     

        # Renards
        for _ in range(22): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            while not self.position_libre(position, self.__actors_sprites):
                position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
        
            renard= Renard(position)
            ActorSpriteDrivenByRandom(self.__screen, renard, "red", [self.renards, self.__actors_sprites])
            
    def __update_actors(self) -> None:
        self.__player_sprite.update()
        self.__actors_sprites.update()

        # Lapins mangent plantes
        collisions = pygame.sprite.groupcollide(self.lapins, self.plants, False, True)
        for lapin, plantes in collisions.items():
            for plante in plantes:
                lapin._actor.rencontrer_plante(plante)
     
        # Renards mangent lapins
        collisions = pygame.sprite.groupcollide(self.renards, self.lapins, False, True)
        for renard, lapins in collisions.items():
            for lapin in lapins:
                renard._actor.rencontrer_lapin(lapin._actor)

        collisions = pygame.sprite.groupcollide(self.lapins, self.lapins, False, False)
        for lapin1, lapins_touches in collisions.items():
            for lapin2 in lapins_touches:
                if lapin1 != lapin2 and lapin1._actor.energie > 10 and lapin2._actor.energie > 10:
                    nouveaux_petits = lapin1._actor.rencontrer_lapin(lapin2._actor)
                    self.gerer_reproduction(lapin1._actor, nouveaux_petits, 'Lapin')

# Renards se reproduisent
        collisions = pygame.sprite.groupcollide(self.renards, self.renards, False, False)
        for renard1, renards_touches in collisions.items():
            for renard2 in renards_touches:
                if renard1 != renard2 and renard1._actor.energie > 15 and renard2._actor.energie > 15:
                    nouveaux_petits = renard1._actor.rencontrer_renard(renard2._actor)
                    self.gerer_reproduction(renard1._actor, nouveaux_petits, 'Renard')

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        self.__player_sprite.draw(self.__screen)
        self.__actors_sprites.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__frame_count += 1
            if self.__frame_count >= self.__frames_per_cycle:
                self.__frame_count = 0
                self.__cycle_count += 1
                self.display_population()
                self.__incrementer_age()

            if self.__cycle_count >= self.__max_cycles:
                print("Fin de la simulation.")
                self.__running = False
                break
            
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()

if __name__ == "__main__":
    app = App()
    app.execute()