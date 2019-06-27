import re

class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start Alien Invasion in an inactive state
        self.game_active = False

        # High score should never be reset.
        self.filename = 'high_score.txt'
        try:
            with open(self.filename, 'r') as self.f_obj:
                self.high_score = self.f_obj.read()
                if re.match("^[0-9].*", str(self.high_score)):
                    self.high_score = int(self.high_score)
                else:
                    self.high_score = 0
        except FileNotFoundError:
            self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1