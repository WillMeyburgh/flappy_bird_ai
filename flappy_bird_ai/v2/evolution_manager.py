import random
from pygame import Color, Surface
import pygame
from flappy_bird_ai.v2.evolution_fitness_display import EvolutionFitnessDisplay
from flappy_bird_ai.v2.genome_player import GenomePlayer
from flappy_bird_ai.v2.neat.genome_manager import GenomeManager
from flappy_bird_ai.v2.node import Node
from flappy_bird_ai.v2.phenotype_display import PhenotypeDisplay
from flappy_bird_ai.v2.position import Position


class EvolutionManager(Node):
    MARGIN = 10
    GENERATION_SIZE = 200
    NEXT_GENERATION_POOL = 4
    GENERATION_COLOR = Color(255, 255, 255)
    SEED_RESET_GEN = 5

    def __init__(self, initial_position):
        self.phenotype_display = PhenotypeDisplay(Position.zeros(), None)

        self.players = Node()

        super().__init__(
            children=[
                self.players
            ]
        )

        self.initial_position = initial_position
        self.genome_manager = GenomeManager(6, 1)
        self.generation = 0
        self.font = pygame.font.SysFont("Sans", 20, True)
        self.rng = random.Random()
        self.last_score = 0
        self.top_score = 0

        self.next_generation()

    def draw(self, surface: Surface):
        super().draw(surface)

        surface.blit(self.font.render(f"{self.generation}: {self.last_score:.2f}({self.top_score:.2f})", True, color=self.GENERATION_COLOR), (30, 30))

        from flappy_bird_ai.v2.game import Game
        
        if self.phenotype_display.phenotype is not None:
            display = self.phenotype_display.surface()


            surface.blit(
                display,
                (
                    Game.get().width-display.width-self.MARGIN,
                    self.MARGIN,
                )
            )

    def player(self, genome, score_bonus=0) -> GenomePlayer:
        return GenomePlayer(self.initial_position, genome, score_bonus=score_bonus)

    def next_generation(self):
        self.generation += 1
        self.last_score = 0

        if len(self.players.children) == 0:
            for _ in range(self.GENERATION_SIZE):
                self.players.children.append(self.player(self.genome_manager.new()))
        else:
            genomes = []
            best_actual_score = 0

            while len(self.players.children) > 0:
                player = self.players.children.pop(0)
                best_actual_score = max(best_actual_score, player.score - player.score_bonus)
                genomes.append((player.score, player.genome))

            from flappy_bird_ai.v2.game import Game
            Game.get().evolution_fitness_display.append(best_actual_score)
            if len(Game.get().evolution_fitness_display.fitnesses)%self.SEED_RESET_GEN:
                Game.get().pipe_manager.seed = self.rng.randint(0, 1000)

            genomes.sort(key=lambda x: x[0], reverse=True)

            genomes = list(genomes[:self.NEXT_GENERATION_POOL])

            self.players.children.append(self.player(genomes[0][1], genomes[0][0]/2))
            for i in range(1, len(genomes)):
                if len(self.players.children) < self.GENERATION_SIZE:
                    self.players.children.append(self.player(self.genome_manager.crossover(genomes[0][1],genomes[i][1]), (genomes[0][0]+genomes[i][0])/6))

            weights = [100]

            for _ in range(1, self.NEXT_GENERATION_POOL):
                weights.append(max(weights[-1]//2,1))

            while len(self.players.children) < self.GENERATION_SIZE:
                left, right = tuple(self.rng.choices(genomes, weights, k=2))

                self.players.children.append(self.player(self.genome_manager.crossover(left[1],right[1])))

    def process(self, delta: float):
        self.phenotype_display.phenotype = None
        self.last_score = 0

        for player in self.players.children:
            if self.phenotype_display.phenotype is None and player.flying:
                self.phenotype_display.phenotype = player.genome.phenotype
                
            self.last_score = max(self.last_score, player.score - player.score_bonus)
            self.top_score = max(self.top_score, self.last_score)

        if self.phenotype_display.phenotype is None:
            from flappy_bird_ai.v2.game import Game
            self.next_generation()
            Game.get().pipe_manager.reset()

        super().process(delta)