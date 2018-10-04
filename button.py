import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg, y):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg = msg

        # Set the dimensions and properties of the button.
        self.active = False
        self.font = pygame.font.SysFont(None, 48)
        self.width, self.height = self.font.size(self.msg)
        self.button_color = (0, 0, 0)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.screen_rect.centerx, self.screen_rect.bottom * y)

    def prep_msg(self):
        """Turn msg into a rendered image and center text on the button."""
        if self.active:
            self.text_color = (0, 255, 0)
        else:
            self.text_color = (255, 255, 255)
        self.msg_image = self.font.render(self.msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Prep the message, draw blank button and then draw message.
        self.prep_msg()
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)