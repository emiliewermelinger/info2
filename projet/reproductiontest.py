import pygame
from random import randint
from sys import exit
from typing import List, Tuple

WINDOW_SIZE: Tuple[int, int] = (400, 400)
WINDOW_TITLE: str = "pygame window 12"
FPS = 24

class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2
    _dimension: Tuple
    energie:int
    energie_max: int
    def change_energie(self, delta: int)->None:
        self.energie= max(0,min(self.energie+delta, self.energie_max))
    
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2,energie: int=0,energie_max: int=0 ) -> None:
        self._position = position
        self._speed = speed
        self._dimension = (10,10)
        self.energie= energie
        self.energie_max= energie_max

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


class ActorSprite(pygame.sprite.Sprite):
    _surface: pygame.Surface
    # added to get information about the surface where sprite move to test boundaries
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(self, surface: pygame.Surface, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
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
    def __init__(self, surface: pygame.Surface, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
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
    def __init__(self, surface: pygame.Surface, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
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
            speed= pygame.Vector2(0,0)
            actor= Actor(position,speed,0,0)
            ActorSpriteDrivenBySpeed(self.__screen, actor, "green", [self.plants, self.__actors_sprites])

        # Lapins
        for _ in range(520):
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
            speed = pygame.Vector2(randint(-1,1), randint(-1,1))
            energie = 10
            energie_max = 20
            actor = Actor(position,speed,energie,energie_max)
            ActorSpriteDrivenByRandom(self.__screen, actor, "white", [self.lapins, self.__actors_sprites])
            
            energie_min = 0

        # Renards
        for _ in range(22): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            speed= pygame.Vector2 (randint(-2,2),randint(-2,2))
            energie = 25
            energie_max = 50
            actor= Actor(position, speed,energie,energie_max)
            ActorSpriteDrivenByRandom(self.__screen, actor, "red", [self.renards, self.__actors_sprites])
            
            energie_min = 0

    def __update_actors(self) -> None:
        self.__player_sprite.update()
        self.__actors_sprites.update()

        # Handle collisions
        # Lapins eat plants
        collisions = pygame.sprite.groupcollide(self.lapins, self.plants, False, True)
        for lapin in collisions:
            lapin._actor.change_energie(10)
          # lapin.energie += 10 
        #taille du lapin qui change? ou bien il faut un print? same question pour les renards

        # Renards eat lapins
        collisions = pygame.sprite.groupcollide(self.renards, self.lapins, False, True)
        for renard in collisions:
            # Add logic to increase renard energy here (not yet implemented)
            renard._actor.change_energie(15)

        collisions = pygame.sprite.groupcollide(self.lapins, self.lapins, False, False)
        for lapin1, lapins_touches in collisions.items():
            for lapin2 in lapins_touches:
                if lapin1 != lapin2 and lapin1._actor.energie > 15 and lapin2._actor.energie > 15:
            # Créez un nouveau lapin
                    position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                    speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
                    energie = 10  # Énergie initiale du nouveau lapin
                    energie_max = 20
                    actor = Actor(position, speed, energie, energie_max)
                    ActorSpriteDrivenByRandom(self.__screen, actor, "yellow", [self.lapins, self.__actors_sprites])
            
            # Réduisez l'énergie des parents
                    lapin1._actor.energie -= 5
                    lapin2._actor.energie -= 5

# Renards se reproduisent
        collisions = pygame.sprite.groupcollide(self.renards, self.renards, False, False)
        for renard1, renards_touches in collisions.items():
            for renard2 in renards_touches:
                if renard1 != renard2 and renard1._actor.energie > 30 and renard2._actor.energie > 30:
            # Créez un nouveau renard
                    position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
                    speed = pygame.Vector2(randint(-2, 2), randint(-2, 2))
                    energie = 15  # Énergie initiale du nouveau renard
                    energie_max = 50
                    actor = Actor(position, speed, energie, energie_max)
                    ActorSpriteDrivenByRandom(self.__screen, actor, "orange", [self.renards, self.__actors_sprites])
            
            # Réduisez l'énergie des parents
                    renard1._actor.energie -= 10
                    renard2._actor.energie -= 10

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
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()

