import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, x):
        """Initialize the alien and set its starting position."""
        super(Bunker, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        self.image = pygame.image.load('images/bunker.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.screen_rect.bottom * 8/10
        self.rect.x = self.screen_rect.right * x / 6 - self.rect.width / 2

    def update(self):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
