import pygame
import random
from pygame.sprite import Sprite


class RAlien(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super(RAlien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        self.image = pygame.image.load('images/ralien.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.right = self.screen_rect.left
        self.rect.y = self.screen_rect.bottom / 10

        # Prep score
        self.font = pygame.font.Font(None, 46)
        self.text = self.font.render("200", 1, (255, 0, 0))
        self.width, self.height = self.font.size("200")

        # Movement flags.
        self.moving_right = False

        # Death.
        self.count = 0

    def update(self, audio):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if random.randint(0, 5000) == 0 and not self.moving_right:
            self.moving_right = True
            self.rect.right = self.screen_rect.left
        if self.moving_right:
            self.rect.centerx += self.ai_settings.ship_speed_factor / 10
            if not audio.oscia.get_busy():
                audio.oscia.play(audio.oscib)
        if self.rect.left > self.screen_rect.right:
            self.rect.right = self.screen_rect.left
            self.moving_right = False

    def blitme(self):
        """Draw the ship at its current location."""
        if self.moving_right:
            self.screen.blit(self.image, self.rect)
        elif self.count > 0:
            self.screen.blit(self.text, self.rect)
            self.count -= 1

    def dead(self):
        self.moving_right = False
        self.count = 60
