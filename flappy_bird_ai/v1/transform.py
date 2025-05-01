from dataclasses import dataclass
from typing import Tuple


@dataclass
class Transform:
    position: Tuple[float, float]
    rotation: float

    @classmethod
    def zeros(cls) -> "Transform":
        return Transform(position=(0,0), rotation=0)
    
    def __add__(self, other: "Transform") -> "Transform":
        return Transform(
            position=(
                self.position[0] + other.position[0],
                self.position[1] + other.position[1],
            ), 
            rotation=self.rotation+other.rotation
        )
    
    def __sub__(self, other: "Transform") -> "Transform":
        return Transform(
            position=(
                self.position[0] - other.position[0],
                self.position[1] - other.position[1],
            ), 
            rotation=self.rotation-other.rotation
        )