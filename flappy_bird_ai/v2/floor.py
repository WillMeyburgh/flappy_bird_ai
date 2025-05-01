from flappy_bird_ai.v2.body import Body
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.sprite import Sprite


class Floor(Body):
    __ASSET = "assets/ground.png"
    def __init__(self):
        super().__init__(Position.new(0, 768), Sprite(self.__ASSET), metadata="floor")