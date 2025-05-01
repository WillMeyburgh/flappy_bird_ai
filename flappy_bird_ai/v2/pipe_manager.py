import random
from typing import List
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.pipe_pair import PipePair
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.timer import Timer


class PipeManager(Node):
    __GAP = 150
    OFFSET_MIN = -90
    OFFSET_MAX = 90
    SPAWN_RATE=1

    def __init__(self):
        self.timer = Timer(self.SPAWN_RATE, self.on_timer)

        self.pipe_pairs = Node()

        super().__init__(children=[self.timer, self.pipe_pairs])

        self.seed = random.randint(0, 10000)
        self.rng = random.Random(self.seed)

        self.on_timer()

    def on_timer(self):
        self.spawn_pipe_pair()
        self.timer.start()

    def spawn_pipe_pair(self):
        spawned = False

        for pipe_pair in self.pipe_pairs.children:
                if pipe_pair.position.local[0] < -100:
                    self.reset_pipe_pair(pipe_pair)
                    spawned = True

        if not spawned:
            self.spawn_new_pipe_pair()


    def reset_pipe_pair(self, pipe_pair):
        offset = self.rng.randint(self.OFFSET_MIN, self.OFFSET_MAX)
        pipe_pair.position = Position.new(1000, 384 + offset)

    def spawn_new_pipe_pair(self):
        pipe_pair = PipePair(Position.zeros(), self.__GAP)
        self.reset_pipe_pair(pipe_pair)
        self.pipe_pairs.children.append(pipe_pair)

    def reset(self):
        self.timer.stop()

        self.rng = random.Random(self.seed)
        offset = 0

        for i in range(len(self.pipe_pairs.children)):
            if isinstance(self.pipe_pairs.children[i-offset], PipePair):
                self.pipe_pairs.children.pop(i-offset)
                offset += 1

        self.on_timer()

    def next_pipe_pair(self, bird: Node) -> List[float]:
        pipe_pairs = []

        for pipe_pair in self.pipe_pairs.children:
            pipe_pairs.append(
                [
                    bird.position.local[1] - (pipe_pair.position.local[1]+self.__GAP),
                    bird.position.local[1] - (pipe_pair.position.local[1]-self.__GAP),
                    pipe_pair.position.local[0] - bird.position.local[0],
                    100*self.timer.time
                ]
            )

        low = None

        for i in range(len(pipe_pairs)):
            if pipe_pairs[i][2] >= 0:
                if low is None or pipe_pairs[i][2] < low[2]:
                    low = pipe_pairs[i]
        
        return [v/100 for v in low] if low is not None else None