from pygame import Surface
import pygame
from flappy_bird_ai.collision_shape_2d import CollisionShape2D
from flappy_bird_ai.node_2d import Node2D
from flappy_bird_ai.pipe_manager import PipeManager
from flappy_bird_ai.sprite_2d import Sprite2D
from flappy_bird_ai.transform import Transform


class Bird(Node2D):
    __IMG = None

    @classmethod
    def img(cls) -> Surface:
        if cls.__IMG is None:
            cls.__IMG = pygame.image.load("assets/bird2.png").convert_alpha()
        return cls.__IMG
    
    def __init__(self, transform: Transform, pipe_manager: PipeManager):
        super().__init__(
            transform, [
                Sprite2D(self.img())
            ]
        )

        self.pipe_manager = pipe_manager

    def move_and_collide(self, y_offset):
        self.transform.position[1] += y_offset

        for pipe_pair in self.pipe_manager.children:
            for pipe in pipe_pair.children:
                p_shape = 

    def process(self, delta:float):
        self.move_and_collide(0)