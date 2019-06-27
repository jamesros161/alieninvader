import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A Class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) an then set correct positions
        self.image = pygame.image.load('images/laser.png')
        self.image = pygame.transform.scale(self.image, (45, 128))
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.orientation = True

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ Move the bullet up the screen"""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rct position.
        self.rect.y = self.y
        # Update orientation
        self.orientation = not self.orientation

    def blitme(self):
        if self.orientation == True:
            self.screen.blit(self.image, self.rect)
        elif self.orientation == False:
            self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)