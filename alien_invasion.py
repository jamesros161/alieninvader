import pygame
from pygame.sprite import Group

from scoreboard import Scoreboard
from background import Background
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from planet import Planet
import game_functions as gf


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Set background image
    background = Background(screen)

    # Make Ship
    ship = Ship(ai_settings, screen)

    # Make a group for alien fleet and create alien fleet
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Make Planets
    planet = Planet(screen, 0, 0)

    # Make a group to store bullets in
    bullets = Group()

    # Create an instance to store game statistics and create a scoreboard.
    sb = Scoreboard(ai_settings, screen, stats)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, planet, background, play_button)


run_game()
