import pygame
from pygame.sprite import Sprite


class Dead(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, screen, rect):
        """Initialize the alien and set its starting position."""
        super(Dead, self).__init__()
        self.screen = screen

        # Load the aliens image nd set its rect attribute.
        self.image = pygame.image.load('images/ad.png')
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.image_speed = 15
        self.expectancy = True

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left."""
        self.image_speed -= 1
        if self.image_speed == 0:
            self.expectancy = False
