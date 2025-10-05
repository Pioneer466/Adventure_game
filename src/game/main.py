"""Entry point for the Adventure platformer using Pygame."""

from __future__ import annotations

from typing import List, Optional, Tuple

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
    pygame.Rect,
    Tuple[int, int],
    List[entities.EnergyOrb],
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
    checkpoint_data = data.get("checkpoint")
    checkpoint_rect = pygame.Rect(*checkpoint_data["zone"]) if checkpoint_data else pygame.Rect(0, 0, 0, 0)
    checkpoint_respawn: Tuple[int, int] = tuple(checkpoint_data["respawn"]) if checkpoint_data else player_start
    energy_orbs = [
        entities.EnergyOrb.from_center(orb["x"], orb["y"], orb.get("diameter", 28))
        for orb in data.get("energy_orbs", [])
    ]
    return player, platforms, enemies, finish_rect, world_size, checkpoint_rect, checkpoint_respawn, energy_orbs


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
) -> tuple[bool, str, bool, bool]:
    """Process events, returning (running, current_state, restart_requested, jump_pressed)."""

    restart_requested = False
    running = True
    jump_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                jump_pressed = True
            elif event.key == pygame.K_SPACE and state == "playing":
                defeated = player.attack(enemies)
                for enemy in defeated:
                    enemies.remove(enemy)
            elif event.key == pygame.K_r and state == "game_over":
                restart_requested = True
    return running, state, restart_requested, jump_pressed


def draw(
    screen: pygame.Surface,
    player: entities.Player,
    platforms: List[entities.Platform],
    enemies: List[entities.Enemy],
    finish_rect: pygame.Rect,
    camera: pygame.Vector2,
    state: str,
    font: pygame.font.Font,
    energy_orbs: List[entities.EnergyOrb],
    checkpoint_rect: pygame.Rect,
) -> None:
    """Render the current game state to the screen."""

    screen.fill(BACKGROUND_COLOR)

    # Draw ground/platforms
    for platform in platforms:
        offset_rect = platform.rect.move(-camera.x, -camera.y)
        pygame.draw.rect(screen, (46, 139, 87), offset_rect)

    if checkpoint_rect.width > 0 and checkpoint_rect.height > 0:
        checkpoint_draw = checkpoint_rect.move(-camera.x, -camera.y)
        pygame.draw.rect(screen, (173, 216, 230), checkpoint_draw, 2)

    for orb in energy_orbs:
        orb_rect = orb.rect.move(-camera.x, -camera.y)
        if orb.active:
            pygame.draw.ellipse(screen, (255, 255, 0), orb_rect)
            inner = orb_rect.inflate(-orb_rect.width // 2, -orb_rect.height // 2)
            pygame.draw.ellipse(screen, (255, 140, 0), inner)
        else:
            faded = orb_rect.inflate(-orb_rect.width // 5, -orb_rect.height // 5)
            pygame.draw.ellipse(screen, (180, 180, 180), faded, 2)

    # Finish zone
    pygame.draw.rect(screen, (255, 215, 0), finish_rect.move(-camera.x, -camera.y))

    # Draw enemies and player
    for enemy in enemies:
        pygame.draw.rect(screen, (220, 20, 60), enemy.rect.move(-camera.x, -camera.y))
    player_rect = player.rect.move(-camera.x, -camera.y)
    pygame.draw.rect(screen, (65, 105, 225), player_rect)

    if player.is_attacking:
        attack_rect = player.get_attack_hitbox().move(-camera.x, -camera.y)
        overlay = pygame.Surface(attack_rect.size, pygame.SRCALPHA)
        overlay.fill((255, 215, 0, 120))
        screen.blit(overlay, attack_rect.topleft)

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
        "Saut : ↑ ou W (double saut après une boule d'énergie)",
        "Attaque : barre d'espace",
        "R : Rejouer au dernier checkpoint",
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
    jump_pressed: bool,
    energy_orbs: List[entities.EnergyOrb],
    checkpoint_rect: pygame.Rect,
    checkpoint_reached: bool,
    checkpoint_respawn: Tuple[int, int],
) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """Update all game entities. Returns checkpoint status and optional respawn."""

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, jump_pressed, platforms, dt)

    for enemy in list(enemies):
        enemy.update(platforms, dt)
        if enemy.health <= 0:
            enemies.remove(enemy)

        if player.rect.colliderect(enemy.rect):
            player.take_damage(1)

    new_respawn_point: Optional[Tuple[int, int]] = None
    if checkpoint_rect.width > 0 and checkpoint_rect.height > 0 and not checkpoint_reached:
        if player.rect.colliderect(checkpoint_rect):
            checkpoint_reached = True
            new_respawn_point = checkpoint_respawn

    for orb in energy_orbs:
        orb.update(dt)
        if orb.active and player.rect.colliderect(orb.rect):
            player.add_double_jump_charge()
            orb.collect()

    # Falling off the world defeats the player immediately.
    if player.rect.top > world_size[1]:
        player.health = 0

    return checkpoint_reached, new_respawn_point


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
        pygame.Rect,
        Tuple[int, int],
        List[entities.EnergyOrb],
    ]:
        return load_level()

    (
        player,
        platforms,
        enemies,
        finish_rect,
        world_size,
        checkpoint_rect,
        checkpoint_respawn,
        energy_orbs,
    ) = reset_level()
    state = "playing"
    checkpoint_reached = False
    current_respawn = tuple(player.rect.topleft)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        running, state, restart, jump_pressed = handle_events(player, enemies, state)
        if not running:
            break

        if restart:
            if checkpoint_reached:
                player.respawn(current_respawn)
                state = "playing"
            else:
                (
                    player,
                    platforms,
                    enemies,
                    finish_rect,
                    world_size,
                    checkpoint_rect,
                    checkpoint_respawn,
                    energy_orbs,
                ) = reset_level()
                checkpoint_reached = False
                current_respawn = tuple(player.rect.topleft)
                state = "playing"
            continue

        if state == "playing":
            checkpoint_reached, new_respawn = update_game(
                player,
                platforms,
                enemies,
                world_size,
                dt,
                jump_pressed,
                energy_orbs,
                checkpoint_rect,
                checkpoint_reached,
                checkpoint_respawn,
            )
            if new_respawn:
                current_respawn = new_respawn

            if player.is_dead:
                state = "game_over"
            elif player.rect.colliderect(finish_rect):
                state = "victory"

        camera = compute_camera(player.rect, world_size, screen.get_size())
        draw(
            screen,
            player,
            platforms,
            enemies,
            finish_rect,
            camera,
            state,
            font,
            energy_orbs,
            checkpoint_rect,
        )

    pygame.quit()


def main() -> None:
    """Allow running with ``python -m src.game.main``."""

    run()


if __name__ == "__main__":
    main()
