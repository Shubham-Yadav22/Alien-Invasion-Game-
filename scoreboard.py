import pygame.font
from pygame.sprite import Group 

from ship import Ship

class Scoreboard :
    """A class to report scoring information"""

    def __init__(self,ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game 
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.setting
        self.stats = ai_game.stats

        #font setting for scoring information
        self.text_color = (255,255,255)            #White

        self.font = pygame.font.SysFont(None, 48)

        #prepare the initial score image 
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()


    def prep_ship(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width 
            ship.rect.y = 10 
            self.ships.add(ship)


    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.settings.bg_colour)

        #Position the level below the score 
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10



    def prep_high_score(self):
        """Turn the high score in a rendered image"""
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_colour)

    # center the high score at the top of the screen .
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = 20


    def prep_score(self):
        """Turn the score into a rendered image"""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str ,True ,self.text_color,self.settings.bg_colour)

        #Display the score at the top right 
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20 
        


    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)


    def check_high_score(self):
        """Check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()



