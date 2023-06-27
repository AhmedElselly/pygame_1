import pygame
from settings import *
from overworld import Overworld
from level import Level

class Game:
    def __init__(self, screen):
        self.max_level = 0
        self.screen = screen
        self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
        self.level_status = 'level'
        self.overworld_status = 'overworld'
        self.status = self.overworld_status
    
    def create_level(self, current_level):
        self.level = Level(current_level, self.screen, self.create_overworld)
        self.status = self.level_status
    
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.screen, self.create_level)
        self.status = self.overworld_status

    def run(self):
        if self.status == self.overworld_status:
            self.overworld.run()
        else:
            self.level.run()