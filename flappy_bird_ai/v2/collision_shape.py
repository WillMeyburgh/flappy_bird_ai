from enum import Flag
from pygame import Color, Surface
import pygame
from shapely import Point
import shapely
from flappy_bird_ai.v2.node import Node
from shapely.geometry import Polygon, mapping


class CollisionShape(Node):
    _DRAW_COLLIDER = False
    __COLLIDER_INACTIVE_COLOR = Color(255, 0, 0, 128)
    __COLLIDER_ACTIVE_COLOR = Color(0, 255, 0, 128)
    id_generator = 0

    def __init__(self, shape: Polygon, callback=None, input=False, metadata=None, **kwargs):
        super().__init__(**kwargs)

        self.shape = shape
        self.callback = callback
        self.input = input
        self.metadata = metadata
        self.id = CollisionShape.id_generator
        CollisionShape.id_generator+=1
        self.active = True

        self._old_collision = set()
        self._collision = set()
        

    def draw(self, surface: Surface):
        super().draw(surface)

        if self._DRAW_COLLIDER:
            tmp = Surface(self.shape.bounds[2:], pygame.SRCALPHA)
            pygame.draw.polygon(
                tmp,
                self.__COLLIDER_ACTIVE_COLOR if len(self._collision) > 0 else self.__COLLIDER_INACTIVE_COLOR,
                mapping(self.shape)['coordinates'][0]
            )
            surface.blit(tmp, self.position._global[0])

    def translated_shape(self):
        return shapely.affinity.translate(self.shape, *self.position._global[0])

    def collide(self, other: "CollisionShape"):
        self._collision.add(other.id)
        other._collision.add(self.id)
        
        if self.callback is not None and other.id not in self._old_collision:
            self.callback(other.metadata)
        if other.callback is not None and self.id not in other._old_collision:
            other.callback(self.metadata)

    @classmethod
    def draw_colliders(cls):
        cls._DRAW_COLLIDER = True

    @classmethod
    def circle(cls, radius: float, **kwargs):
        return cls(Point(radius,radius).buffer(radius), **kwargs)

    @classmethod
    def rectangle(cls, width: float, height: float, **kwargs):
        return cls(
            Polygon([
                (0,0),
                (width, 0),
                (width, height),
                (0, height)
            ]),
            **kwargs
        )