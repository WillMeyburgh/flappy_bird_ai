import pygame

from flappy_bird_ai.v2.game import Game


def main():
    pygame.init()
    pygame.font.init() 

    screen = pygame.display.set_mode((864,936))
    clock = pygame.time.Clock()
    running = True

    game = Game.get()
    game.set_mode((864,936))

    while running:
        events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                events.append(event)

        game.draw(screen)
        pygame.display.flip()

        delta = clock.tick(60)/1000
        game.process(delta, events)

    pygame.quit()