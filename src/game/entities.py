"""Game entities for the Adventure platformer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import pygame

GRAVITY = 1200  # pixels per second squared


@dataclass
class Platform:
    """Static ground element the player and enemies can stand on."""

    rect: pygame.Rect

    @classmethod
    def from_dimensions(cls, x: int, y: int, width: int, height: int) -> "Platform":
        return cls(pygame.Rect(x, y, width, height))


class Entity:
    """Base entity with position and size."""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def apply_gravity(self, dt: float) -> None:
        self.velocity.y += GRAVITY * dt

    def move_and_collide(self, platforms: Sequence[Platform], dt: float) -> None:
        """Move entity and resolve collisions with the provided platforms."""

        # Horizontal movement
        self.rect.x += int(self.velocity.x * dt)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right
                self.velocity.x = 0

        # Vertical movement
        self.rect.y += int(self.velocity.y * dt)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                self.velocity.y = 0


class Player(Entity):
    """Player controlled character."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 40, 60)
        self.speed = 220  # pixels per second
        self.jump_strength = -420
        self.attack_cooldown = 0.4
        self.attack_timer = 0.0
        self.max_health = 3
        self.health = self.max_health
        self.invulnerability_time = 0.8
        self.invulnerability_timer = 0.0

    def update(
        self,
        pressed_keys: Sequence[bool],
        platforms: Sequence[Platform],
        dt: float,
    ) -> None:
        """Update the player's state based on input and world geometry."""

        self.velocity.x = 0
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.velocity.x = self.speed

        if (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]) and self.on_ground:
            self.velocity.y = self.jump_strength

        self.apply_gravity(dt)
        self.move_and_collide(platforms, dt)

        if self.attack_timer > 0:
            self.attack_timer = max(0.0, self.attack_timer - dt)
        if self.invulnerability_timer > 0:
            self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)

    def attack(self, enemies: Iterable["Enemy"]) -> List["Enemy"]:
        """Perform a melee attack and return the enemies that were defeated."""

        if self.attack_timer > 0:
            return []

        self.attack_timer = self.attack_cooldown
        attack_rect = self.rect.inflate(40, 20)
        defeated: List[Enemy] = []
        for enemy in enemies:
            if enemy.rect.colliderect(attack_rect):
                if enemy.take_damage(1):
                    defeated.append(enemy)
        return defeated

    def take_damage(self, amount: int) -> bool:
        """Apply damage to the player. Returns ``True`` when health hits zero."""

        if self.invulnerability_timer > 0:
            return False

        self.health = max(0, self.health - amount)
        if self.health > 0:
            self.invulnerability_timer = self.invulnerability_time
        return self.health <= 0

    @property
    def is_dead(self) -> bool:
        return self.health <= 0


class Enemy(Entity):
    """A basic enemy with a patrol pattern and multiple hit points."""

    def __init__(self, x: int, y: int, patrol_range: tuple[int, int], speed: int = 120, health: int = 3) -> None:
        super().__init__(x, y, 40, 50)
        self.patrol_range = patrol_range
        self.speed = speed
        self.direction = 1
        self.health = max(2, health)

    def update(self, platforms: Sequence[Platform], dt: float) -> None:
        """Update enemy movement and handle collisions."""

        # Patrol horizontally within the given range.
        self.velocity.x = self.speed * self.direction

        self.apply_gravity(dt)
        self.move_and_collide(platforms, dt)

        if self.rect.left <= self.patrol_range[0]:
            self.rect.left = self.patrol_range[0]
            self.direction = 1
        elif self.rect.right >= self.patrol_range[1]:
            self.rect.right = self.patrol_range[1]
            self.direction = -1

        self.velocity.x = self.speed * self.direction

    def take_damage(self, amount: int) -> bool:
        """Deal damage to the enemy. Returns True when the enemy is defeated."""

        self.health -= amount
        return self.health <= 0
