from abc import ABC, abstractmethod
from dataclasses import dataclass
from turtle import position
from typing import List

from pygame import Surface

from flappy_bird_ai.scene import Scene
from flappy_bird_ai.transform import Transform

@dataclass
class Node2D(Scene):
    transform: Transform
    children: List["Node2D"]

    def draw_transform(self, surface: Surface, transform: Transform):
        transform += self.transform

        for child in self.children:
            child.draw_transform(surface, transform)

    def draw(self, surface: Surface):
        self.draw_transform(surface, Transform.zeros())

    def process(self, delta: float):
        for child in self.children:
            child.process(delta)

    