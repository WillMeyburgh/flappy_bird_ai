from pygame import Surface
import pygame
from flappy_bird_ai.collision_shape_2d import CollisionShape2D
from flappy_bird_ai.node_2d import Node2D
from flappy_bird_ai.sprite_2d import Sprite2D
from flappy_bird_ai.transform import Transform


class Pipe(Node2D):
    __IMG = None

    @classmethod
    def img(cls) -> Surface:
        if cls.__IMG is None:
            cls.__IMG = pygame.image.load("assets/pipe.png").convert_alpha()
        return cls.__IMG

    def __init__(self, transform, bottom=True):
        self.bottom = bottom

        mul = 1 if bottom else -1
        
        if not bottom:
            transform += Transform((0, -self.img().height), 0)

        super().__init__(
            transform, [
                Sprite2D(self.img(), scale=(1, mul))
            ]
        )