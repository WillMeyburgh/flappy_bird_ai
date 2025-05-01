from matplotlib import pyplot
import numpy as np
import pygame
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.position import Position

import matplotlib.ticker as ticker

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg


import pylab



class EvolutionFitnessDisplay(Node):
    MARGIN = 10

    def __init__(self, position: Position):
        super().__init__(position)
        self.fitnesses = []
        self._surface = None
    
    def append(self, fitness):
        self.fitnesses.append(fitness)
        self._surface = None

    def surface(self) -> pygame.Surface:
        if self._surface is None:
            fig = pylab.figure(
                figsize=[6, 4], # Inches
                dpi=70,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
            )
            ax = fig.gca()
            ax.plot(np.arange(1, len(self.fitnesses)+1),self.fitnesses)
            ax.set_xlabel("Evolution")
            ax.set_ylabel("Score")

            ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_argb()

            size = canvas.get_width_height()
            self._surface = pygame.image.frombytes(raw_data, size,"ARGB")
            pyplot.close(fig)
        return self._surface
    
    def draw(self, surface):
        from flappy_bird_ai.v2.game import Game

        if len(self.fitnesses) >= 1:
            tmp = self.surface()
            surface.blit(
                tmp,
                (
                    Game.get().width-tmp.width-self.MARGIN,
                    Game.get().height-tmp.height-self.MARGIN,
                )
            )
