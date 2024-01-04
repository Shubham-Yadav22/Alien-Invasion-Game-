class GameStats :
    """Track statistics for Alien Invasion"""

    def __init__(self,ai_game):
        """Initialize Statistics"""
        self.setting = ai_game.setting
        self.reset_stats()

        # Start alien invasion in inactive stats 
        self.game_active = False

        # High Score should not be reset 
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1

                

    
