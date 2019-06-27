import pygame

class Planet():

    def __init__(self, screen, xpos, ypos):
        """Initialize the ship and set its starting position"""
        self.screen = screen

        # Load the ship and get its rect.
        self.image = pygame.image.load('images/planet2.png')
        self.image = pygame.transform.scale(self.image, (154, 149))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.x = 5
        self.rect.y = 5

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)