
from dataclasses import dataclass
from typing import Dict, List, Tuple

from flappy_bird_ai.v2.neat.link import Link
from flappy_bird_ai.v2.neat.node import Node

@dataclass
class Genome:
    input_size: int
    output_size: int
    nodes: Dict[int, Node]
    links: Dict[Tuple[int, int], Link]
    _phenotype = None

    @property
    def phenotype(self):
        from flappy_bird_ai.v2.neat.phenotype import Phenotype

        if self._phenotype is None:
            self._phenotype = Phenotype(self)
        return self._phenotype