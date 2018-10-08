import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from bunker import Bunker
from dead import Dead


def check_keydown_events(event, ai_settings, screen, ship, bullets, audio):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, audio)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,
                 score_button, menu, audio, bunkers):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and stats.game_active:
            check_keydown_events(event, ai_settings, screen, ship, bullets, audio)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y, bunkers)
            check_score_button(score_button, mouse_x, mouse_y, menu)
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            play_button.active = True
        else:
            play_button.active = False
        if score_button.rect.collidepoint(pygame.mouse.get_pos()):
            score_button.active = True
        else:
            score_button.active = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,
                      mouse_x, mouse_y, bunkers):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.reset()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, aliens)
        create_bunkers(ai_settings, screen, bunkers)
        ship.center_ship()


def check_score_button(score_button, mouse_x, mouse_y, menu):
    """Start a new game when the player clicks Play."""
    button_clicked = score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and menu.show_scores:
        menu.show_scores = False
    elif button_clicked and not menu.show_scores:
        menu.show_scores = True


def fire_bullet(ai_settings, screen, ship, bullets, audio):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed and not ship.dead:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        audio.pewa.play(audio.pewb)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, score_button,
                  abullets, menu, ralien, audio, death, bunkers):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Draw the play button if the game is inactive
    if not stats.game_active:
        if not menu.show_scores:
            menu.main(play_button, score_button, screen)
        else:
            menu.scores(score_button, screen)
    else:
        if ship.deadc == 0:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, abullets, ralien)
        # Redraw all bullets, behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        for abullet in abullets.sprites():
            abullet.draw_bullet()
        ship.blitme()
        ralien.blitme()
        aliens.draw(screen)
        for dead in death.sprites():
            dead.blitme()
        for bunker in bunkers.sprites():
            bunker.blitme()
        bunkers.update()
        death.update()
        for dead in death.copy():
            if not dead.expectancy:
                death.remove(dead)
        if ai_settings.alien_tracker <= ai_settings.alien_mtracker * 4 / 5:
            ai_settings.audio_level = 1
        if ai_settings.alien_tracker <= ai_settings.alien_mtracker * 3 / 5:
            ai_settings.audio_level = 2
        if ai_settings.alien_tracker <= ai_settings.alien_mtracker * 2 / 5:
            ai_settings.audio_level = 3
        if not audio.omin.get_busy() and not ship.dead:
            if ai_settings.audio_level == 0:
                audio.omin.play(audio.omina)
            if ai_settings.audio_level == 1:
                audio.omin.play(audio.ominb)
            if ai_settings.audio_level == 2:
                audio.omin.play(audio.ominc)
            if ai_settings.audio_level >= 3:
                audio.omin.play(audio.omina)

        # Draw the score information.
        sb.show_score()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, abullets, ralien, audio, death, bunkers):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    abullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for abullet in abullets.copy():
        if abullet.rect.top >= ai_settings.screen_height:
            abullets.remove(abullet)

    check_bullet_alien_collisions(ai_settings, screen, stats,  sb, ship, aliens, bullets, abullets,
                                  ralien, audio, death, bunkers)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, abullets,
                                  ralien, audio, death, bunkers):
    """Respond to bullet-alien collisions"""
    # Remove any bullets and aliens that have collided.
    if pygame.sprite.spritecollideany(ship, abullets):
        if ship.deadc == 10:
            ship.dead = True
    if pygame.sprite.groupcollide(bullets, bunkers, True, False) or \
            pygame.sprite.groupcollide(abullets, bunkers, True, False):
        audio.exploa.play(audio.explob)
    collisions = pygame.sprite.spritecollideany(ralien, bullets)
    if collisions:
        bullets.remove(collisions)
        ralien.dead()
        stats.score += 200
        sb.prep_score()
        audio.exploa.play(audio.explob)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        ai_settings.alien_tracker -= 1
        audio.exploa.play(audio.explob)
        for alien in collisions.values():
            ali = alien.pop()
            death.add(Dead(screen, ali.rect))
            audio.exploa.play(audio.explob)
            stats.score += ali.worth
            sb.prep_score()
        check_high_score(stats, sb)
        if ai_settings.speed_buffer > 0:
            ai_settings.speed_buffer -= 1
        else:
            ai_settings.increase_speed()
            ai_settings.speed_buffer = 2
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.reset()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens)


def score(stats, alien):
    stats.score += alien.worth


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    availble_space_y = (ai_settings.screen_height -
                        (3 * alien_height) - ship_height)
    number_rows = int(availble_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen, row_number, alien_number)
    alien_width = alien.rect.width
    alien.x = (35 - alien_width/2) + 2 * 35 * alien_number
    alien.rect.x = alien.x
    alien.rect.y = ai_settings.screen_height * 2/10 + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_bunker(ai_settings, screen, bunkers, x):
    """Create an alien and place it in the row."""
    bunker = Bunker(ai_settings, screen, x)
    bunkers.add(bunker)


def create_fleet(ai_settings, screen, aliens):
    """Create a full fleet of aliens."""
    # Create the fleet of aliens.
    for row_number in range(6):
        for alien_number in range(10):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            ai_settings.alien_tracker += 1
    ai_settings.alien_mtracker = ai_settings.alien_tracker


def create_bunkers(ai_settings, screen, bunkers):
    """Create Bunkers"""
    create_bunker(ai_settings, screen, bunkers, 1)
    create_bunker(ai_settings, screen, bunkers, 3)
    create_bunker(ai_settings, screen, bunkers, 5)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, abullets, ralien):
    """Respond to ship beinghit by alien."""
    if stats.ships_left > 0:
        ralien.dead()
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        abullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        ship.image = pygame.image.load('images/ship.png')
        ship.deadc = 10
        ship.dead = False
        ship.image_speed = 1

        # Pause.
        sleep(0.5)

    else:
        with open('hs.txt', 'a') as f:
            f.write('\n' + str(stats.high_score))
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(screen, ship, aliens):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            if ship.deadc == 10:
                ship.dead = True
            break


def update_aliens(ai_settings, screen, ship, aliens, abullets, bunkers):
    """
    Check if the fleet is at an edge,
      and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update(ai_settings, screen, abullets)

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        if ship.deadc == 10:
            ship.dead = True
    pygame.sprite.groupcollide(aliens, bunkers, False, True)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(screen, ship, aliens)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
