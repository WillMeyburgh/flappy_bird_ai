import pygame

from flappy_bird_ai.game import Game


def main():
    pygame.init()

    screen = pygame.display.set_mode((864,936))
    clock = pygame.time.Clock()
    running = True

    game = Game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.draw(screen)
        pygame.display.flip()

        delta = clock.tick(60)/1000
        game.process(delta)

    pygame.quit()