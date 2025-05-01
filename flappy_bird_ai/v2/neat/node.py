
from dataclasses import dataclass
import math
from typing import Callable

@dataclass
class Node:
    id: int
    activation: Callable
    bias: float

    @classmethod
    def input(cls, id):
        return Node(id, lambda x: x, 0)
    
    @classmethod
    def sigmoid(cls, id):
        return Node(id, lambda x: 1/(1+math.exp(-x)), 0)
    
    def clone(self) -> "Node":
        return Node(
            self.id,
            self.activation,
            self.bias
        )