import pygame
from flappy_bird_ai.v2.bird import Bird
from flappy_bird_ai.v2.input import Input


class Player(Bird):
    def __init__(self, position):
        self.initial_position = position

        super().__init__(position)


    def process(self, delta: float):
        if Input.just_pressed(pygame.K_SPACE):
            self.flap()

        super().process(delta)

    def reset(self):
        super().reset()
        self.position = self.initial_position


    def on_collision(self, metadata):
        super().on_collision(metadata)

        if metadata == 'floor':
            self.reset()
            from flappy_bird_ai.v2.game import Game
            Game.get().pipe_manager.reset()
