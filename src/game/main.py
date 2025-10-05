"""Entry point for the Adventure platformer using Pygame."""

from __future__ import annotations

from typing import List, Tuple

import pygame

from . import entities
from .levels import level1

BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
SCREEN_SIZE = (960, 540)


def load_level() -> tuple[
    entities.Player,
    List[entities.Platform],
    List[entities.Enemy],
    pygame.Rect,
    tuple[int, int],
]:
    """Load the first level and return the initialized objects."""

    data = level1.load_level()
    platforms = [entities.Platform.from_dimensions(*platform) for platform in data["platforms"]]
    enemies = [
        entities.Enemy(enemy["x"], enemy["y"], (enemy["min_x"], enemy["max_x"]), enemy.get("speed", 120), enemy.get("health", 3))
        for enemy in data["enemies"]
    ]
    player_start = data["player_start"]
    player = entities.Player(player_start[0], player_start[1])
    finish_rect = pygame.Rect(*data["finish_zone"])
    world_size = tuple(data.get("world_size", (960, 640)))
    return player, platforms, enemies, finish_rect, world_size


def compute_camera(
    target: pygame.Rect, world_size: tuple[int, int], screen_size: tuple[int, int]
) -> pygame.Vector2:
    """Center the camera on the target while clamping to the level bounds."""

    cam_x = target.centerx - screen_size[0] // 2
    cam_y = target.centery - screen_size[1] // 2

    max_x = max(0, world_size[0] - screen_size[0])
    max_y = max(0, world_size[1] - screen_size[1])

    cam_x = max(0, min(cam_x, max_x))
    cam_y = max(0, min(cam_y, max_y))

    return pygame.Vector2(cam_x, cam_y)


def handle_events(
    player: entities.Player,
    enemies: List[entities.Enemy],
    state: str,
) -> tuple[bool, str, bool]:
    """Process events, returning (running, current_state, restart_requested)."""

    restart_requested = False
    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and state == "playing":
                defeated = player.attack(enemies)
                for enemy in defeated:
                    enemies.remove(enemy)
            elif event.key == pygame.K_r and state == "game_over":
                restart_requested = True
    return running, state, restart_requested


def draw(
    screen: pygame.Surface,
    player: entities.Player,
    platforms: List[entities.Platform],
    enemies: List[entities.Enemy],
    finish_rect: pygame.Rect,
    camera: pygame.Vector2,
    state: str,
    font: pygame.font.Font,
) -> None:
    """Render the current game state to the screen."""

    screen.fill(BACKGROUND_COLOR)

    # Draw ground/platforms
    for platform in platforms:
        offset_rect = platform.rect.move(-camera.x, -camera.y)
        pygame.draw.rect(screen, (139, 69, 19), offset_rect)

    # Finish zone
    pygame.draw.rect(screen, (255, 215, 0), finish_rect.move(-camera.x, -camera.y))

    # Draw enemies and player
    for enemy in enemies:
        pygame.draw.rect(screen, (220, 20, 60), enemy.rect.move(-camera.x, -camera.y))
    player_rect = player.rect.move(-camera.x, -camera.y)
    pygame.draw.rect(screen, (65, 105, 225), player_rect)

    # Draw health (three hearts)
    heart_size = 20
    spacing = 6
    for index in range(player.max_health):
        x = 20 + index * (heart_size + spacing)
        heart_rect = pygame.Rect(x, 20, heart_size, heart_size)
        color = (220, 20, 60) if index < player.health else (169, 169, 169)
        pygame.draw.rect(screen, color, heart_rect, border_radius=4)

    instructions = [
        "Déplacements : flèches / WASD",
        "Saut : ↑ ou W",
        "Attaque : barre d'espace",
    ]
    for idx, line in enumerate(instructions):
        text_surface = font.render(line, True, (20, 20, 20))
        screen.blit(text_surface, (20, 60 + idx * 24))

    if state == "game_over":
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        text = font.render("Vous êtes vaincu ! Appuyez sur R pour rejouer", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
    elif state == "victory":
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        text = font.render("Bravo ! Appuyez sur Échap pour quitter", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()


def update_game(
    player: entities.Player,
    platforms: List[entities.Platform],
    enemies: List[entities.Enemy],
    world_size: Tuple[int, int],
    dt: float,
) -> None:
    """Update all game entities."""

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, platforms, dt)

    for enemy in list(enemies):
        enemy.update(platforms, dt)
        if enemy.health <= 0:
            enemies.remove(enemy)

        if player.rect.colliderect(enemy.rect):
            player.take_damage(1)

    # Falling off the world defeats the player immediately.
    if player.rect.top > world_size[1]:
        player.health = 0


def run() -> None:
    """Initialize the Pygame window and run the main loop."""

    pygame.init()
    pygame.display.set_caption("Adventure Platformer")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    def reset_level() -> tuple[
        entities.Player,
        List[entities.Platform],
        List[entities.Enemy],
        pygame.Rect,
        Tuple[int, int],
    ]:
        return load_level()

    player, platforms, enemies, finish_rect, world_size = reset_level()
    state = "playing"

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        running, state, restart = handle_events(player, enemies, state)
        if not running:
            break

        if restart:
            player, platforms, enemies, finish_rect, world_size = reset_level()
            state = "playing"
            continue

        if state == "playing":
            update_game(player, platforms, enemies, world_size, dt)

            if player.is_dead:
                state = "game_over"
            elif player.rect.colliderect(finish_rect):
                state = "victory"

        camera = compute_camera(player.rect, world_size, screen.get_size())
        draw(screen, player, platforms, enemies, finish_rect, camera, state, font)

    pygame.quit()


def main() -> None:
    """Allow running with ``python -m src.game.main``."""

    run()


if __name__ == "__main__":
    main()
