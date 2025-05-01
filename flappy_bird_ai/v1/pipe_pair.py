from flappy_bird_ai.node_2d import Node2D
from flappy_bird_ai.pipe import Pipe
from flappy_bird_ai.transform import Transform


class PipePair(Node2D):
    GAP = 100
    SPEED = 400

    def __init__(self, transform):
        super().__init__(
            transform,
            [
                Pipe(Transform((0, -self.GAP/2), 0), bottom=False),
                Pipe(Transform((0, self.GAP/2), 0), bottom=True),
            ]
        )

    def process(self, delta: float):
        self.transform -= Transform((delta * self.SPEED,0), 0)