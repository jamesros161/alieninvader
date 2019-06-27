import sys
import pygame
from background import Background
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, stats, aliens, ai_settings, screen, ship, bullets, sb):
    """Respond to Keypresses"""
    # Right Arrow Key Pressed - Move ship right
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # Left Arrow Key Pressed = Move ship left
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # Space Button Pressed = Fire Weapon
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # V button pressed = Toggle Console Printing during game
    elif event.key == pygame.K_v:
        ai_settings.do_print = not ai_settings.do_print
        print_debug_info(ai_settings, Alien, screen)

    # GAME START KEY PRESSES #
    # P key pressed = Start Normal Game
    elif event.key == pygame.K_p and not stats.game_active:
        reset_game(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # D key pressed = Start Game in Debug mode
    elif event.key == pygame.K_d and not stats.game_active:
        reset_game(ai_settings, stats, screen, ship, aliens, bullets, sb)
        ai_settings.set_debug()
        ai_settings.do_print = True

    # Q key pressed = Quit Game
    elif event.key == pygame.K_q:
        save_game(stats)
        sys.exit()


def check_keyup_events(event, ship):
    """
    Respond to Key releases
    :param event:
    :param ship:
    :return:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
    """
    Respond to keypresses and mouse events.
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, stats, aliens, ai_settings, screen, ship, bullets, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            reset_game(ai_settings, stats, screen, ship, aliens, bullets, sb)


def reset_game(ai_settings, stats, screen, ship, aliens, bullets, sb):
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images:
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions"""
    # CHeck for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, planet, background, play_button):
    """
    Update image on screen and flip screen"
    :param ai_settings:
    :param screen:
    :param ship:
    :param planet:
    :return:
    """
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    background.blitme()

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.blitme()

    ship.blitme()
    planet.blitme()
    aliens.draw(screen)
    # Draw the score information:
    sb.show_score()
    # Draw the Play Button if the game is Inactive:
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible:
    pygame.display.flip()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of alients that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int((available_space_x - alien_width) / alien_width)
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    # Create an alien and place it in the row.
    alien = Alien(ai_settings, screen)
    alien.row_number = row_number
    if row_number == 0:
        alien.direction_mod = 1
    elif row_number == 1:
        alien.direction_mod = -1
    elif row_number % 2 == 0:
        alien.direction_mod = 1
    elif row_number % 2 > 0:
        alien.direction_mod = -1
    alien_width = alien.rect.width
    alien.x = (0.5 * alien_width) + (2 * alien_width) * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""

    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

    print_debug_info(ai_settings, alien, screen)


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


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    check_aliens_hit_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Respond to ship being hit by alien."""

    if stats.ships_left >= 1:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_hit_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break


def print_debug_info(ai_settings, alien, screen):
    """Prints Debug Information """

    # If Speed print is turned on, print speed
    if ai_settings.do_print:
        print("Turning on Debug Printing\n")
        print("Current Speed Factors Are")
        print("\tShip: " + str(ai_settings.ship_speed_factor))
        print("\tBullet: " + str(ai_settings.bullet_speed_factor))
        print("\tAlien: " + str(ai_settings.alien_speed_factor))
        print("\tFleet: " + str(ai_settings.fleet_drop_speed) + "\n")
        try:
            ai_settings.number_aliens = get_number_aliens_x(ai_settings, alien.rect.width)
        except AttributeError:
            alien = Alien(ai_settings, screen)
            ai_settings.number_aliens = get_number_aliens_x(ai_settings, alien.rect.width)
        else:
            ai_settings.number_aliens = get_number_aliens_x(ai_settings, alien.rect.width)
        print("\tAliens / Row: " + str(ai_settings.number_aliens))
    else:
        print("Turning off Debug Printing\n")


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def save_game(stats):
    filename = 'high_score.txt'
    with open(filename, 'w') as file_object:
        file_object.write(str(stats.high_score))