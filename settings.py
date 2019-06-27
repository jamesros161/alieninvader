import game_functions as gf
from alien import Alien

class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.do_print = False

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 7

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.6
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game."""
        # Toggles Debug modes
        self.debug = False
        self.ship_speed_factor = 12
        self.alien_speed_factor = 6
        self.bullet_speed_factor = 10
        self.fleet_drop_speed = 10

        # Scoring
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed Settings and alien point values."""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def set_debug(self):
        """Change Settings for Debugging"""
        # Toggles Debug modes
        self.debug = True

        self.ship_speed_factor = 12
        self.bullet_speed_factor = 12
        self.alien_speed_factor = 12
        self.fleet_drop_speed = 20