from abc import ABC, abstractmethod

from pygame import Surface


class Scene(ABC):
    @abstractmethod
    def draw(self, surface: Surface):
        pass

    def process(self, delta: float):
        pass