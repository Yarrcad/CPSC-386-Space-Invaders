class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 1200
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 1

        # Alien settings
        self.fleet_drop_speed = 10
        # fleet_direction 1 represents right; -1 represents left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # Game settings
        self.game_speed = 60

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 20
        self.bullet_speed_factor = 16
        self.alien_speed_factor = 1

        # Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale