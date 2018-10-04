import pygame
from pygame.sprite import Sprite
import sys

def load_image(name):
    image = pygame.image.load(name)
    return image

class ABullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, alien):
        """Create a bullet object, at the ship's current position."""
        super(ABullet, self).__init__()
        self.screen = screen

        # Create bullet rect at (0, 0), then set correct position.
        self.images = []
        self.images.append(load_image('images/abullet-1.png'))
        self.images.append(load_image('images/abullet-2.png'))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom
        self.index = 0
        self.image = self.images[self.index]
        self.image_speed = 30

        # Store a decimal value for the bullet's position.
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet down the screen."""
        # Update the decimal position of the bullet.
        self.y += self.speed_factor/2

        # Update the rect position.
        self.rect.y = self.y

        # Change sprite.
        self.image_speed -= 1
        if self.image_speed == 0:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.image_speed = 30

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx