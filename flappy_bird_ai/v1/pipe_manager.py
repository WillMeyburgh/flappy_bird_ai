import random
from flappy_bird_ai.node import Node
from flappy_bird_ai.pipe import Pipe
from flappy_bird_ai.pipe_pair import PipePair
from flappy_bird_ai.timer import Timer
from flappy_bird_ai.transform import Transform


class PipeManager(Node):
    OFFSET_MIN = -100
    OFFSET_MAX = 100

    def __init__(self):
        super().__init__([])

        self.timer = Timer(1, self.on_timer)
        self.on_timer()

    def on_timer(self):
        self.spawn_pipe_pair()
        self.timer.start()

    def spawn_pipe_pair(self):
        spawned = False

        for pipe_pair in self.children:
            if pipe_pair.transform.position[0] < -100:
                self.reset_pipe_pair(pipe_pair)
                spawned = True

        if not spawned:
            self.spawn_new_pipe_pair()


    def reset_pipe_pair(self, pipe_pair):
        offset = random.randint(self.OFFSET_MIN, self.OFFSET_MAX)
        pipe_pair.transform = Transform((1000, 384 + offset), 0)

    def spawn_new_pipe_pair(self):
        pipe_pair = PipePair(Transform.zeros())
        self.reset_pipe_pair(pipe_pair)
        self.children.append(pipe_pair)

    def process(self, delta: float):
        super().process(delta)

        self.timer.process(delta)