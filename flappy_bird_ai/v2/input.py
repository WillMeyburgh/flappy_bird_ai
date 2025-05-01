from typing import List
from pygame import Event
import pygame


class Input:
    def __init__(self):
        self.just_down = set()
        self.down = set()
        self.up = set()
        self.mouse_button_up = False

    def process(self, events: List[Event]):
        self.just_down = set()
        self.up = set()
        new_down = set()
        self._mouse_button_up = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                new_down.add(event.key)

                if event.key not in self.down:
                    self.just_down.add(event.key)

            elif event.type == pygame.KEYUP:
                self.up.add(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_button_up = True

        self.down = new_down

    @classmethod
    def just_pressed(cls, key) -> bool:
        return key in cls.get().just_down
    
    @classmethod
    def pressed(cls, key) -> bool:
        return key in cls.get().down
    
    @classmethod
    def released(cls, key) -> bool:
        return key in cls.get().up
    
    @classmethod
    def mouse_pressed(cls) -> bool:
        return cls.get()._mouse_button_up
    
    @classmethod
    def get(cls) -> "Input":
        from flappy_bird_ai.v2.game import Game
        return Game.get().input
