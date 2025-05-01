from typing import Optional
from pygame import Color, Surface
import pygame
from shapely import Polygon
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.sprite import Sprite


class Body(Node):
    def __init__(self, position: Position, sprite: Sprite, collision_shape: Optional[CollisionShape] = None, metadata=None):
        if collision_shape is None:
            collision_shape = self.__collision_shape_from_asset(sprite.asset, metadata=metadata)
            
        super().__init__(
            position=position,
            children=[
                sprite,
                collision_shape
            ]
        )

    @staticmethod
    def __collision_shape_from_asset(asset: str, metadata=None) -> CollisionShape:
        img = Sprite.load_asset(asset)

        return CollisionShape.rectangle(img.width, img.height, metadata=metadata)