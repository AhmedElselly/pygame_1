import pygame, sys
from settings import *
from overworld import Overworld
from level import Level

class Game:
    def __init__(self):
        self.max_level = 3
        self.overworld = Overworld(1, self.max_level, screen, self.create_level)
        self.level_status = 'level'
        self.overworld_status = 'overworld'
        self.status = self.overworld_status
    
    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = self.level_status
    
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = self.overworld_status

    def run(self):
        if self.status == self.overworld_status:
            self.overworld.run()
        else:
            self.level.run()

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)