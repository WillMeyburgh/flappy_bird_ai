
from dataclasses import dataclass
from typing import Tuple

from pygame import Surface
import pygame
from flappy_bird_ai.node_2d import Node2D
from flappy_bird_ai.transform import Transform


class Sprite2D(Node2D):
    def __init__(self, sprite: Surface, scale: Tuple[float, float] = (1, 1), transform=Transform.zeros()):
        super().__init__(transform, [])
        self.sprite = sprite
        self.scale = scale

    def draw_transform(self, surface: Surface, transform: Transform):
        transform += self.transform

        sprite = pygame.transform.rotate(self.sprite, transform.rotation)
        sprite = pygame.transform.flip(sprite, self.scale[0] < 0, self.scale[1] < 0)
        surface.blit(sprite, transform.position)
