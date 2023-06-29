import pygame
from settings import *
from overworld import Overworld
from level import Level
from ui import UI

class Game:
    def __init__(self, screen):
        # game attributes
        self.max_level = 0
        self.cur_health = 100
        self.max_health = 100        
        self.coins = 0
        self.screen = screen
        # overworld creation
        self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
        self.level_status = 'level'
        self.overworld_status = 'overworld'
        self.status = self.overworld_status

        # user interface
        self.ui = UI(self.screen)
    
    def create_level(self, current_level):
        self.level = Level(current_level, self.screen, self.create_overworld, self.change_coins)
        self.status = self.level_status
    
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.screen, self.create_level)
        self.status = self.overworld_status

    def change_coins(self, amount):
        self.coins += amount

    def run(self):
        if self.status == self.overworld_status:
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)