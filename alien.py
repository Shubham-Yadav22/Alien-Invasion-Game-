import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single Alien in the fleet"""

    def __init__(self,ai_game):
        """Initialize the alien and set its starting postion"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting

        #Load the alien image and set rect attributes
        self.image = pygame.image.load('image/alien_green.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height

        #store the alien's exact horizontal position
        self.x = float(self.rect.x)


    def update(self):
        """Move the alien to the right or left"""
        self.x += (self.setting.alien_speed * self.setting.fleet_direction)
        self.rect.x = self.x
       

    def check_edges(self):
        """Return true if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0 :
            return True