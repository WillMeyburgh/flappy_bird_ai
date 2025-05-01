import pygame

from flappy_bird_ai.bird import Bird
from flappy_bird_ai.floor import Floor
from flappy_bird_ai.node import Node
from flappy_bird_ai.pipe_manager import PipeManager
from flappy_bird_ai.scene import Scene
from flappy_bird_ai.sprite_2d import Sprite2D
from flappy_bird_ai.transform import Transform


class Game(Node):
    def __init__(self):
        bg_img = pygame.image.load("assets/bg.png").convert()

        self.pipe_manager = PipeManager()

        super().__init__([
            Sprite2D(bg_img), 
            self.pipe_manager,
            Bird(Transform((50, 600),0), self.pipe_manager),
            Floor(bg_img.height)
        ])