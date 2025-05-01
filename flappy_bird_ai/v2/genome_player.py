from typing import List
from flappy_bird_ai.v2.bird import Bird
from flappy_bird_ai.v2.neat.genome import Genome


class GenomePlayer(Bird):
    def __init__(self, position, genome: Genome, score_bonus=0):
        super().__init__(position)

        self.score_bonus = score_bonus
        self.score += score_bonus
        self.genome = genome

    def inputs(self, delta) -> List[float]:
        from flappy_bird_ai.v2.game import Game
        inputs = Game.get().pipe_manager.next_pipe_pair(self)

        if inputs is None:
            return None

        inputs.extend([self.velocity/100,delta])

        return inputs

    def do_flap(self, delta) -> bool:
        inputs = self.inputs(delta)

        if inputs is None:
            return False

        return self.genome.phenotype.forward(inputs)[0] > 0.5

    def process(self, delta: float):
        if self.flying and self.do_flap(delta):
            self.flap()

        super().process(delta)

    def draw(self, surface):
        if not self.dead:
            super().draw(surface)