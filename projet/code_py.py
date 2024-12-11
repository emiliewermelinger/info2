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


    def __init__(self, position: pygame.Vector2) -> None:
        self._position = position
        self._speed = pygame.Vector2(randint(-1,1), randint(-1,1))
        self._dimension = (10,10)

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


class ActorSpriteDrivenByMouse(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, color_name, *groups)

    def update(self):
        if pygame.mouse.get_focused():
            self._rect.topleft = pygame.mouse.get_pos()
            self._rect.move_ip(1, 1)
            if not self.test_touching_surface_boundaries():
                self._actor.position = pygame.Vector2(self.rect.topleft)


class ActorSpriteDrivenByRandom(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, color_name, *groups)

    def update(self):
        random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        self._rect.move_ip(random_speed)
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
        for actor_00 in range(700): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            actor= Actor(position)
            ActorSpriteDrivenBySpeed(self.__screen, actor, "green", [self.__actors_sprites])

        for actor_001 in range (520):
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0] - 10), randint(0, WINDOW_SIZE[1] - 10))
            actor = Actor(position)
            ActorSpriteDrivenByRandom(self.__screen, actor, "white", [self.__actors_sprites])

        for _ in range(22): 
            position = pygame.Vector2(randint(0, WINDOW_SIZE[0]-10), randint(0, WINDOW_SIZE[1]-10))
            actor= Actor(position)
            ActorSpriteDrivenByRandom(self.__screen, actor, "red", [self.__actors_sprites])

    def __update_actors(self) -> None:
        self.__player_sprite.update()
        self.__actors_sprites.update()

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
