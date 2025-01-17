import pygame
from random import randint
from sys import exit
from typing import List, Tuple
from actors2 import Vivant,Lapin, Renard, Plante

WINDOW_SIZE: Tuple[int, int] = (400, 400)
WINDOW_TITLE: str = "pygame window 12"
FPS = 24


class ActorSprite(pygame.sprite.Sprite):
    _surface: pygame.Surface
    # added to get information about the surface where sprite move to test boundaries
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
        # function to test boundaries
        # we only use relatives positions
        # so we don't have to use a lot of maths
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
        

    def update(self):
        '''random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))'''
        self.change_direction_timer-=1
        if self.change_direction_timer<=0:
            self._actor.speed=pygame.Vector2(randint(-1, 1), randint(-1, 1))
            self.change_direction_timer=24
        self._rect.move_ip(self._actor.speed)
        if not self.test_touching_surface_boundaries():
            self._actor.position = pygame.Vector2(self.rect.topleft)


class ActorSpriteDrivenBySpeed(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Vivant, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, color_name, *groups)

    def update(self):
        self.rect.move_ip(0,0)
        if not self.test_touching_surface_boundaries():
            self._actor.position = pygame.Vector2(self.rect.topleft)


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

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __init_actors(self) -> None:
        self.__player_sprite = pygame.sprite.Group()
        self.__actors_sprites = pygame.sprite.Group()
        self.plants = pygame.sprite.Group()  # Group for plants
        self.lapins = pygame.sprite.Group()  # Group for lapins
        self.renards = pygame.sprite.Group()  # Group for renards

        # Plantes
        for _ in range(700): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            plante= Plante(position)
            ActorSpriteDrivenBySpeed(self.__screen, plante, "green", [self.plants, self.__actors_sprites])

        # Lapins
        for _ in range(520):
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
            speed = pygame.Vector2(randint(-1,1), randint(-1,1))
            lapin = Lapin(position)
            ActorSpriteDrivenByRandom(self.__screen, lapin, "white", [self.lapins, self.__actors_sprites])

        # Renards
        for _ in range(22): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            speed= pygame.Vector2 (randint(-2,2),randint(-2,2))
            renard= Renard(position)
            ActorSpriteDrivenByRandom(self.__screen, renard, "red", [self.renards, self.__actors_sprites])

    def __update_actors(self) -> None:
        self.__actors_sprites.update()

        # Handle collisions
        # Lapins eat plants
        collisions = pygame.sprite.groupcollide(self.lapins, self.plants, False, True)
        for lapin, plantes_touches in collisions.items():
            for plante in plantes_touches:
            # Le lapin mange la plante, prend son énergie
                lapin._actor.rencontrer_plante(plante._actor)
          
        # Renards eat lapins
        collisions = pygame.sprite.groupcollide(self.renards, self.lapins, False, True)
        for renard, lapins_touches in collisions.items():
            for lapin in lapins_touches:
        # Le renard mange le lapin, prend son énergie
                renard._actor.rencontrer_lapin(lapin._actor)

        collisions = pygame.sprite.groupcollide(self.lapins, self.lapins, False, False)
        for lapin1, lapins_touches in collisions.items():
            for lapin2 in lapins_touches:
                if lapin1 != lapin2 and lapin1._actor.energie > 15 and lapin2._actor.energie > 15:
            # Créez un nouveau lapin
                    num_new_lapins= randint(1,3)
                    for _ in range(num_new_lapins):
                        position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                       # speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))     
                        lapin = Lapin(position)
                        ActorSpriteDrivenByRandom(self.__screen, lapin, "yellow", [self.lapins, self.__actors_sprites])
            

# Renards se reproduisent
        collisions = pygame.sprite.groupcollide(self.renards, self.renards, False, False)
        for renard1, renards_touches in collisions.items():
            for renard2 in renards_touches:
                if renard1 != renard2 and renard1._actor.energie > 30 and renard2._actor.energie > 30:
            # Créez un nouveau renard
                    num_new_renards= randint(1,5)
                    for _ in range(num_new_renards):
                        position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                        #speed = pygame.Vector2(randint(-2, 2), randint(-2, 2))
                        renard = Renard(position)
                        ActorSpriteDrivenByRandom(self.__screen, renard, "orange", [self.renards, self.__actors_sprites])
            

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        self.__actors_sprites.draw(self.__screen)

    def execute(self) -> None:
        clock = pygame.time.Clock()
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    exit()
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    app = App()
    app.execute()

