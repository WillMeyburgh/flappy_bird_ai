import numpy as np
import pygame
from flappy_bird_ai.v2.node import Node


class Sprite(Node):
    __ASSETS = {}

    @classmethod
    def load_asset(cls, asset) -> pygame.Surface:
        if asset not in cls.__ASSETS:
            cls.__ASSETS[asset] = pygame.image.load(asset).convert_alpha()
        return cls.__ASSETS[asset]

    def __init__(self, asset: str, flip_x = False, flip_y = False, rotation = 0, **kwargs):
        super().__init__(**kwargs)

        self.asset = asset
        self.sprite = self.load_asset(asset)

        if flip_x or flip_y:
            self.sprite = pygame.transform.flip(self.sprite, flip_x, flip_y)

        self.rotation = rotation

    def draw(self, surface: pygame.Surface):
        super().draw(surface)

        if self.rotation != 0:
            sprite = pygame.transform.rotate(self.sprite, self.rotation)
            surface.blit(sprite, self.position._global[0] - np.array((sprite.width-self.sprite.width, sprite.height-self.sprite.height))/2)
        else:
            surface.blit(self.sprite, self.position._global[0])