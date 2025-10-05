"""Entry point for the Adventure platformer using Pygame."""

from __future__ import annotations

from typing import List

import pygame

from . import entities
from .levels import level1

BACKGROUND_COLOR = (135, 206, 235)  # Sky blue


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


def handle_events(player: entities.Player, enemies: List[entities.Enemy]) -> bool:
    """Process Pygame events. Returns False when the game should quit."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                defeated = player.attack(enemies)
                for enemy in defeated:
                    enemies.remove(enemy)
    return True


def draw(screen: pygame.Surface, player: entities.Player, platforms: List[entities.Platform], enemies: List[entities.Enemy], finish_rect: pygame.Rect) -> None:
    """Render the current game state to the screen."""

    screen.fill(BACKGROUND_COLOR)

    # Draw ground/platforms
    for platform in platforms:
        pygame.draw.rect(screen, (139, 69, 19), platform.rect)

    # Finish zone
    pygame.draw.rect(screen, (255, 215, 0), finish_rect)

    # Draw enemies and player
    for enemy in enemies:
        pygame.draw.rect(screen, (220, 20, 60), enemy.rect)
    pygame.draw.rect(screen, (65, 105, 225), player.rect)

    pygame.display.flip()


def update_game(player: entities.Player, platforms: List[entities.Platform], enemies: List[entities.Enemy], dt: float) -> None:
    """Update all game entities."""

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, platforms, dt)

    for enemy in list(enemies):
        enemy.update(platforms, dt)
        if enemy.health <= 0:
            enemies.remove(enemy)


def run() -> None:
    """Initialize the Pygame window and run the main loop."""

    pygame.init()
    pygame.display.set_caption("Adventure Platformer")
    player, platforms, enemies, finish_rect, world_size = load_level()
    screen = pygame.display.set_mode(world_size)
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        running = handle_events(player, enemies)
        if not running:
            break

        update_game(player, platforms, enemies, dt)

        if player.rect.colliderect(finish_rect):
            running = False

        draw(screen, player, platforms, enemies, finish_rect)

    pygame.quit()


def main() -> None:
    """Allow running with ``python -m src.game.main``."""

    run()


if __name__ == "__main__":
    main()
