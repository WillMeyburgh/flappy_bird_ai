import pygame
from flappy_bird_ai.collision_shape_2d import CollisionShape2D
from flappy_bird_ai.node_2d import Node2D
from flappy_bird_ai.sprite_2d import Sprite2D
from flappy_bird_ai.transform import Transform


class Floor(Node2D):
    def __init__(self, y_offset):
        super().__init__(
            Transform((0, y_offset),0),
            [
                Sprite2D(pygame.image.load("assets/ground.png").convert())
            ]
        )