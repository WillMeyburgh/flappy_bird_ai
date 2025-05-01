from flappy_bird_ai.v2.body import Body
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.sprite import Sprite


class Backgound(Body):
    __ASSET = "assets/bg.png"

    def __init__(self):
        super().__init__(
            Position.zeros(),
            Sprite(self.__ASSET),
            CollisionShape.rectangle(Sprite.load_asset(self.__ASSET).width, 200, position=Position.new(0, -199), metadata="ceiling")
        )