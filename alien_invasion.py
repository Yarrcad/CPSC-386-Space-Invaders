import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scorebord
from button import Button
from ship import Ship
from ralien import RAlien
from menu import Menu
from audio import Audio
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(screen, "PLAY GAME", 80/100)

    # Make the High Score button.
    score_button = Button(screen, "HIGH SCORES", 90/100)

    # Audio
    audio = Audio()

    # Make the menu
    menu = Menu()

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scorebord(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    ralien = RAlien(ai_settings, screen)
    bullets = Group()
    abullets = Group()
    aliens = Group()
    death = Group()
    bunkers = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, aliens)

    # Start the main loop for the game.
    while True:
        pygame.time.Clock().tick(ai_settings.game_speed)
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,
                        score_button, menu, audio, bunkers)

        if stats.game_active:
            ship.update(audio)
            ralien.update(audio)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
                              abullets, ralien, audio, death, bunkers)
            gf.update_aliens(ai_settings, screen, ship, aliens, abullets, bunkers)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button,
                         score_button, abullets, menu, ralien, audio, death, bunkers)


run_game()
