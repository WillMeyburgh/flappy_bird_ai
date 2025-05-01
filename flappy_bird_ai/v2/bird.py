import numpy as np
import pygame
from flappy_bird_ai.v2.body import Body
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.input import Input
from flappy_bird_ai.v2.position import Position
from flappy_bird_ai.v2.sprite import Sprite


class Bird(Body):
    __ASSET = "assets/bird2.png"

    GRAVITY = 1800

    FLAP = 800
    FLAP_AV = np.pi / 5

    KILL_AV = 10*np.pi

    def __init__(self, position):
        self.sprite = Sprite(self.__ASSET)

        super().__init__(
            position, 
            self.sprite, 
            CollisionShape.circle(
                18, 
                position=Position.new(8,0), 
                metadata="bird", 
                input=True,
                callback=self.on_collision
            )
        )

        self.reset()

    def on_collision(self, metadata):
        if metadata == 'score':
            if self.flying:
                self.score += 1
        else:
            if self.flying:
                self.angular_velocity += self.KILL_AV
                self.flying = False
            if metadata == 'floor':
                self.dead = True
                self.children[-1].active=False

    def process(self, delta: float):
        super().process(delta)

        self.velocity += self.GRAVITY*delta

        self.position -= np.array((0, -self.velocity*delta))

        self.sprite.rotation += self.angular_velocity

        if self.position._global[0][1] > 1000 or self.position._global[0][1] < -100:
            self.flying = False

    def flap(self):
        if self.flying:
            self.velocity = -self.FLAP
            self.angular_velocity += self.FLAP_AV

    def reset(self):
        self.flying = True
        self.dead = False

        self.velocity = 0
        self.angular_velocity = 0

        self.score = 0

        self.sprite.rotation = 0

