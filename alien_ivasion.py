import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class Alieninvasion:
    """Overall class to manage game assets and behaviours"""

    def __init__(self):
        """Initialize the game , and create game resources"""
        pygame.init()
        self.setting = Settings()
        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # create an instance to store game statistics  and sccoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button 
        self._play_button = Button(self, "Play" )

        #set the background colour
        self.bg_colour = (128, 128, 128)

    def run_game(self):
        """Start the main loop for the game"""

        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
        #Get rid of bullets that have disappeared
            self._update_screen()


    def _check_events(self):
            """Respond to keypresses and mouse events"""
            # Watch for keyboard and mouse events .
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self._play_button.rect.collidepoint(mouse_pos)
        if button_clicked and  not self.stats.game_active:

            #Reset the game settings
            self.setting.initialize_dynamic_settings()

            #Reset the game stats first
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()


            #get rid of any remaining aliens and bullets
            self.alien.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

        #Hide the mouse cursor
        pygame.mouse.set_visible(True)

    def _check_keydown_events(self, event): 
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()


    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row 
        # spacing between each alien is to one alien width 
         
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        #Determine the number of rows that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        #Create the first row
       
        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                #Create an alien and place it in the row 
                self._create_alien(alien_number,row_number)

    def _check_fleet_edges(self):
        """Respond appropriatelyif any aliens have reached an edge"""
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break 


    def _change_fleet_directions(self):
        """Drop the entire Fleet and change the fleets direction"""
        for alien in self.alien.sprites():
            alien.rect.y +=  self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1


    def _create_alien(self,alien_number,row_number):      
            alien = Alien(self)
            alien_width,alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.alien.add(alien)

    def _update_aliens(self):
        """check if the fleet is at the edge, and then , Update the positions of all aliens in the fleet """
        self._check_fleet_edges()
        self.alien.update()

        #Look for alien ship collisions 
        if pygame.sprite.spritecollideany(self.ship,self.alien):
              self.ship_hit()

        # Look for aliens hitting the ground 
        self._check_alien_bottom()

    def ship_hit(self):
        """Respond to the ship being hit by an alien"""

        if self.stats.ships_left > 0:
            # Decrement ships_left , update keyboard

            self.stats.ships_left -= 1
            self.sb.prep_ship()


            #Get rid of any remaining aliens and bullets 
            self.alien.empty()
            self.bullets.empty()

            #Create a new fleet of aliens and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause 
            sleep(0.5)

        else:
            self.stats.game_active = False  

    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.alien.sprites():

            if alien.rect.bottom >= screen_rect.bottom :
                #treat this the same as if the ship is hit 
                self._ship_hit()
                break



    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""

        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets """
        self.bullets.update()

        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        
        print(len(self.bullets))
        self._check_bullets_alien_collisions()


    def _check_bullets_alien_collisions(self): 
        # Check for any bullets that have hit an alien 
        # If so, get rid of the bullet and the alien 
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien, True, True)    
        
        if collisions:
            for aliens in collisions.values():                   
                self.stats.score += self.setting.alien_points * len(aliens)
            self.sb.prep_score() 
            self.sb.check_high_score()

        if not self.alien:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""

        # Redraw the screen during each pass through the loop

        self.screen.fill(self.setting.bg_colour)
        self.ship.blitme()


        # Make the most recently drawn screen visible.
       
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.alien.draw(self.screen)

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self._play_button.draw_button()
            
        #Draw the score information
        if self.stats.game_active :
            self.sb.show_score()

        pygame.display.flip()

if __name__ == '__main__':
    #Makes a game instance , and run the game
    ai = Alieninvasion()
    ai.run_game()

  