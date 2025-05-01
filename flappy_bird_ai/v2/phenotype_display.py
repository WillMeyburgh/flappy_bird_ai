import numpy as np
from pygame import Color, Surface
import pygame
from flappy_bird_ai.v2.neat.phenotype import Phenotype
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.position import Position


class PhenotypeDisplay(Node):
    BG_COLOR = Color(128, 128, 128)
    NODE_LOW_COLOR = Color(0, 0, 0)
    NODE_HIGH_COLOR = Color(0, 0, 255)
    TEXT_COLOR = Color(255, 255, 255)
    LINK_LOW_COLOR = Color(255, 0, 0)
    LINK_HIGH_COLOR = Color(0, 255, 0)
    LINK_DISABLED_COLOR = Color(200, 200, 200)
    LINK_WIDTH = 2
    NODE_RADIUS = 15
    NODE_SPACING = 20
    LAYER_SPACING = 20
    PADDING = 30

    def __init__(self, position, phenotype: Phenotype):
        super().__init__(position)
        self.phenotype = phenotype
        self.font = pygame.font.SysFont("Sans", 10)

    def node_center(self, node) -> np.ndarray:
        for i, layer in enumerate(self.phenotype.layers):
            if node in layer:
                j = layer.index(node)

                x = self.PADDING + self.NODE_RADIUS + i*(2*self.NODE_RADIUS + self.LAYER_SPACING)

                center_offset = 0

                if len(layer)%2 == 0:
                    center_j = (j+1-len(layer)/2)
                    if center_j <= 0:
                        center_j -= 1

                    center_offset = self.NODE_SPACING/2 + (abs(center_j)-1)*(2*self.NODE_RADIUS+self.NODE_SPACING) + self.NODE_RADIUS
                    center_offset *= np.sign(center_j)
                else:
                    center_j = (j-len(layer)//2)
                    center_offset = (abs(center_j))*(2*self.NODE_RADIUS+self.NODE_SPACING)
                    center_offset *= np.sign(center_j)

                y = self.height/2+center_offset

                return np.array((x, y))

    def between_color(self, left, right, ratio) -> Color:
        ratio = np.clip(ratio, 0 , 1)
        return Color(
            int(left.r + (right.r - left.r) * ratio),
            int(left.g + (right.g - left.g) * ratio),
            int(left.b + (right.b - left.b) * ratio),
        )


    def link_color(self, value, max_value):
        ratio = (value + max_value)/(2*max_value+0.001)
        return self.between_color(self.LINK_LOW_COLOR, self.LINK_HIGH_COLOR, ratio)
        
    def draw_links(self, surface: Surface):
        max_value = 0

        for link in self.phenotype.genome.links.values():
            if link.active:
                max_value = max(max_value, abs(link.weight))

        for (left, right), link in self.phenotype.genome.links.items():
            color = self.link_color(link.weight, max_value)

            if not link.active:
                color = self.LINK_DISABLED_COLOR

    
            pygame.draw.line(surface, color, self.node_center(left), self.node_center(right))
            

    def draw_nodes(self, surface: Surface):
        for node in self.phenotype.genome.nodes:
            center = self.node_center(node)

            color = self.NODE_HIGH_COLOR

            text = str(node)

            if node in self.phenotype.outputs:
                text+=f": {self.phenotype.outputs[node]:.2f}"
                if node >= self.phenotype.genome.input_size:
                    color = self.between_color(self.NODE_LOW_COLOR, self.NODE_HIGH_COLOR, self.phenotype.outputs[node])

            pygame.draw.circle(surface, color, center, self.NODE_RADIUS)
            text = self.font.render(text, True, self.TEXT_COLOR)

            surface.blit(text, center-np.array((text.width/2,text.height/2)))

            bias_text = self.font.render(f"{self.phenotype.genome.nodes[node].bias:.2f}", True, self.TEXT_COLOR)

            surface.blit(bias_text, center+np.array((self.NODE_RADIUS,self.NODE_RADIUS)))

    def surface(self) -> Surface:
        max_layer_size = max(len(l) for l in self.phenotype.layers)
        layer_count = len(self.phenotype.layers)
        self.width = self.PADDING*2 + layer_count*2*self.NODE_RADIUS + (layer_count-1)*self.LAYER_SPACING
        self.height = self.PADDING*2 + max_layer_size*2*self.NODE_RADIUS + (max_layer_size-1)*self.NODE_SPACING

        surface = Surface((self.width, self.height))
        surface.fill(self.BG_COLOR)

        self.draw_links(surface)
        self.draw_nodes(surface)

        return surface

    def draw(self, surface: Surface):
        if self.phenotype is None:
            return

        surface.blit(self.surface(), self.position._global[0])