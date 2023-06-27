import pygame, sys
from settings import *
from level import Level
from game import Game
from game_data import level_0

pygame.init()

# screen = pygame.display.set_mode((screen_width, screen_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
# level = Level(level_0, screen)
game = Game(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)