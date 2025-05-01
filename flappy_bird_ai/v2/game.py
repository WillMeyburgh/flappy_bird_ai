from typing import List
import numpy as np
from pygame import Event, Surface
from flappy_bird_ai.v2.background import Backgound
from flappy_bird_ai.v2.bird import Bird
from flappy_bird_ai.v2.collision_detector import CollisionDetector
from flappy_bird_ai.v2.evolution_fitness_display import EvolutionFitnessDisplay
from flappy_bird_ai.v2.evolution_manager import EvolutionManager
from flappy_bird_ai.v2.floor import Floor
from flappy_bird_ai.v2.input import Input
from flappy_bird_ai.v2.pipe_manager import PipeManager
from flappy_bird_ai.v2.body import Body
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.pipe import Pipe
from flappy_bird_ai.v2.pipe_pair import PipePair
from flappy_bird_ai.v2.player import Player
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.sprite import Sprite


class Game(Node):
    SINGLETON = None

    @classmethod
    def get(cls) -> "Game":
        if cls.SINGLETON is None:
            cls.SINGLETON = Game()
        return cls.SINGLETON

    def __init__(self):
        self.pipe_manager = PipeManager()
        self.evolution_manager = EvolutionManager(Position.new(50, 400))
        self.evolution_fitness_display = EvolutionFitnessDisplay(Position.zeros())
        self.input = Input()
        self.width = 0
        self.height = 0

        super().__init__(
            children=[
                CollisionDetector(
                    children=[
                        Backgound(),
                        self.pipe_manager,
                        self.evolution_manager,
                        # Player(Position.new(50, 200)),
                        Floor(),
                        self.evolution_fitness_display
                    ]
                )
            ]
        )

    def set_mode(self, mode):
        self.width = mode[0]
        self.height = mode[1]

    def process(self, delta: float, events: List[Event]):
        self.input.process(events)

        super().process(delta)