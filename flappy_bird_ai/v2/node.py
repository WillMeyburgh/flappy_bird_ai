import inspect
import sys
from typing import List
import numpy as np
from pygame import Surface

from flappy_bird_ai.v2.position import Position


class Node:
    def __init__(self, position = Position.zeros(), children: List["Node"] = None):
        self.position = position
        self.children = children if children is not None else []

    def draw(self, surface: Surface):
        for child in self.children:
            child.position = child.position.update_global(self.position)
            child.draw(surface)

    def process(self, delta: float):
        for child in self.children:
            child.process(delta)
            child.position = child.position.update_global(self.position)