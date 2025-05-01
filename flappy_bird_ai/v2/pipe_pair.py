from flappy_bird_ai.v2.body import Body
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.pipe import Pipe
from flappy_bird_ai.v2.position import Position


class PipePair(Node):
    SPEED = 600

    def __init__(self, position, gap):
        super().__init__(
            position,
            [
                Pipe(Position.new(0, -gap/2), top = True),
                Pipe(Position.new(0, gap/2), top = False),
                CollisionShape.rectangle(
                    2,
                    1000,
                    position=Position.new(0, -500),
                    metadata="score"
                )
            ]
        )

    def process(self, delta: float):
        super().process(delta)

        self.position -= Position.new(delta * self.SPEED,0)