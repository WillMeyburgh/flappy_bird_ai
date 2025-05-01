from dataclasses import dataclass
from typing import List
from flappy_bird_ai.scene import Scene


@dataclass
class Node(Scene):
    children: List[Scene]

    def draw(self, surface):
        for child in self.children:
            child.draw(surface)

    def process(self, delta: float):
        for child in self.children:
            child.process(delta)