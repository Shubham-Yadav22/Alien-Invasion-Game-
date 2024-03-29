class Settings:
    """A class to store all of our settings for alien invasion"""

    def __init__(self):
        """Initialise the games static settings"""

        #Screen Settings
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_colour = (0, 0, 0)

        #Ship Settings

        self.ship_limit = 3

        #Bullet Settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Alien settings

        self.fleet_drop_speed = 15

        # how fast the games speed up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change """
        self.ship_speed = 2.0
        self.bullet_speed = 2.0
        self.alien_speed = 0.7

        # fleet direction of 1 represents right and -1 represents left
        self.fleet_direction = 1
        
        #scoring 
        self.alien_points = 50 


    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *=  self.speedup_scale