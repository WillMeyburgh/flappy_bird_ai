
from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class Position:
    def __init__(self, local: np.ndarray, _global = None):
        self.local = local

        if _global is None:
            _global = np.zeros(shape=(1,2))

        self._global=_global

    @classmethod
    def new(cls, x, y):
        return Position(np.array([x,y]))
    
    @classmethod
    def zeros(cls):
        return cls.new(0,0)

    def update_global(self, other: "Position") -> "Position":
        return Position(self.local, other._global + self.local)

    def __add__(self, other) -> "Position":
        if isinstance(other, np.ndarray):
            return self + Position(other)
        elif isinstance(other, Position):
            return Position(self.local + other.local, self._global + other.local)

    def __sub__(self, other) -> "Position":
        if isinstance(other, np.ndarray):
            return self - Position(other)
        elif isinstance(other, Position):
            return Position(self.local - other.local, self._global - other.local)
        
    def __repr__(self):
        return f"Pos<l: {self.local}, g: {self._global}>"