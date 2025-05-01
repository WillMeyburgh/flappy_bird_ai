import numpy as np
from flappy_bird_ai.v2.body import Body
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.sprite import Sprite


class Pipe(Body):
    __ASSET = 'assets/pipe.png'

    def __init__(self, position: Position, top = False):
        position += np.array([-Sprite.load_asset(self.__ASSET).width/2, 0])
        
        if top:
            position += np.array([0, -Sprite.load_asset(self.__ASSET).height])

        super().__init__(
            position,
            Sprite(self.__ASSET, flip_y=top), 
            metadata="pipe"
        )