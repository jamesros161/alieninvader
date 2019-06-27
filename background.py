import pygame

class Background():

    def __init__(self, screen):
        """Initialize the background and set its starting position"""
        self.screen = screen

        # Load the background and get its rect.
        self.image = pygame.image.load('images/background.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new background at the top corner.
        self.rect.x = 0
        self.rect.y = 0

    def blitme(self):
        """Draw the background at its current location."""
        self.screen.blit(self.image, self.rect)