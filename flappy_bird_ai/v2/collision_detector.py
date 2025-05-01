from typing import List, Tuple

from pygame import Color, Surface
import pygame
from flappy_bird_ai.v2.collision_shape import CollisionShape
from flappy_bird_ai.v2.input import Input
from flappy_bird_ai.v2.node import Node
from shapely.strtree import STRtree


class CollisionDetector(Node):
    TOGGLE_OFF_COLOR = Color(255,0,0)
    TOGGLE_ON_COLOR = Color(0,255,0)
    TOGGLE_SIZE = (40,20)
    TOGGLE_MARGIN = 10

    def __init__(self, children):
        super().__init__(children=children)

        self.draw_colliders = False

    def retrieve_colliders(self, root: Node) -> Tuple[List[CollisionShape], List[CollisionShape]]:
        if isinstance(root, CollisionShape):
            if root.active:
                root._old_collision = root._collision
                root._collision = set()

                if root.input:
                    return [root], []
                else:
                    return [], [root]
            
        input_colliders, output_colliders = [], []

        for child in root.children:
            tmp_input_colliders, tmp_output_colliders = self.retrieve_colliders(child)
            input_colliders.extend(tmp_input_colliders)
            output_colliders.extend(tmp_output_colliders)
        
        return input_colliders, output_colliders
            

    def update_collisions(self):
        input_colliders, output_colliders = self.retrieve_colliders(self)

        tree = STRtree([collider.translated_shape() for collider in output_colliders])

        for input_collider in input_colliders:
            for i in tree.query(input_collider.translated_shape()):
                input_collider.collide(output_colliders[i])

    def process(self, delta: float):
        self.update_collisions()

        from .game import Game
        if Input.get().mouse_pressed():
            pos =  pygame.mouse.get_pos()
            rect = (
                self.TOGGLE_MARGIN,
                Game.get().height-self.TOGGLE_MARGIN-self.TOGGLE_SIZE[1],
                *self.TOGGLE_SIZE
            )
            
            if rect[0] <= pos[0] <= rect[0]+rect[2] and rect[1] <= pos[1] <= rect[1]+rect[3]:
                self.draw_colliders = not self.draw_colliders
                CollisionShape._DRAW_COLLIDER = self.draw_colliders

        super().process(delta)

    def draw(self, surface: Surface):
        super().draw(surface)

        from .game import Game
        pygame.draw.rect(
            surface, 
            self.TOGGLE_ON_COLOR if self.draw_colliders else self.TOGGLE_OFF_COLOR, 
            (
                self.TOGGLE_MARGIN,
                Game.get().height-self.TOGGLE_MARGIN-self.TOGGLE_SIZE[1],
                *self.TOGGLE_SIZE
            )
        )

