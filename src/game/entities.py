"""Game entities for the Adventure platformer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

import pygame

GRAVITY = 1200  # pixels per second squared


@dataclass
class Platform:
    """Static ground element the player and enemies can stand on."""

    rect: pygame.Rect

    @classmethod
    def from_dimensions(cls, x: int, y: int, width: int, height: int) -> "Platform":
        return cls(pygame.Rect(x, y, width, height))


@dataclass
class EnergyOrb:
    """Collectible granting a temporary double-jump charge."""

    rect: pygame.Rect
    respawn_delay: float = 5.0
    active: bool = True
    timer: float = 0.0

    @classmethod
    def from_center(cls, x: int, y: int, diameter: int = 28) -> "EnergyOrb":
        rect = pygame.Rect(0, 0, diameter, diameter)
        rect.center = (x, y)
        return cls(rect)

    def collect(self) -> None:
        self.active = False
        self.timer = 0.0

    def update(self, dt: float) -> None:
        if self.active:
            return
        self.timer += dt
        if self.timer >= self.respawn_delay:
            self.active = True
            self.timer = 0.0


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

    _sprite_surface: Optional[pygame.Surface] = None
    _sprite_surface_flipped: Optional[pygame.Surface] = None

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 40, 60)
        self.speed = 220  # pixels per second
        self.jump_strength = -500
        self.attack_cooldown = 0.4
        self.attack_timer = 0.0
        self.attack_indicator_duration = 0.18
        self.attack_indicator_timer = 0.0
        self.last_attack_rect = self.rect.copy()
        self.max_health = 3
        self.health = self.max_health
        self.invulnerability_time = 0.8
        self.invulnerability_timer = 0.0
        self.facing = 1
        self.double_jump_charges = 0
        self.air_jump_performed = False
        self.jump_buffer_window = 0.15
        self.jump_buffer_timer = 0.0
        self.coyote_time = 0.12
        self.coyote_timer = 0.0
        self._ensure_sprite()

    def update(
        self,
        pressed_keys: Sequence[bool],
        jump_pressed: bool,
        platforms: Sequence[Platform],
        dt: float,
    ) -> None:
        """Update the player's state based on input and world geometry."""

        self.velocity.x = 0
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.velocity.x = self.speed

        if self.velocity.x > 0:
            self.facing = 1
        elif self.velocity.x < 0:
            self.facing = -1

        if self.on_ground:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        if jump_pressed:
            self.jump_buffer_timer = self.jump_buffer_window

        can_ground_jump = self.on_ground or self.coyote_timer > 0.0
        if can_ground_jump and self.jump_buffer_timer > 0.0:
            self.velocity.y = self.jump_strength
            self.on_ground = False
            self.air_jump_performed = False
            self.jump_buffer_timer = 0.0
            self.coyote_timer = 0.0
        elif jump_pressed and self.double_jump_charges > 0 and not self.air_jump_performed:
            self.velocity.y = self.jump_strength
            self.double_jump_charges = max(0, self.double_jump_charges - 1)
            self.air_jump_performed = True

        self.apply_gravity(dt)
        self.move_and_collide(platforms, dt)

        if self.on_ground:
            self.air_jump_performed = False
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        if self.jump_buffer_timer > 0.0:
            self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)

        if self.attack_timer > 0:
            self.attack_timer = max(0.0, self.attack_timer - dt)
        if self.attack_indicator_timer > 0:
            self.attack_indicator_timer = max(0.0, self.attack_indicator_timer - dt)
        if self.invulnerability_timer > 0:
            self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)

    def attack(self, enemies: Iterable["Enemy"]) -> List["Enemy"]:
        """Perform a melee attack and return the enemies that were defeated."""

        if self.attack_timer > 0:
            return []

        self.attack_timer = self.attack_cooldown
        attack_rect = self.rect.inflate(50, 24)
        reach = 80
        if self.facing >= 0:
            attack_rect.width += reach
        else:
            attack_rect.left -= reach
            attack_rect.width += reach
        self.last_attack_rect = attack_rect.copy()
        self.attack_indicator_timer = self.attack_indicator_duration
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

    @property
    def is_attacking(self) -> bool:
        return self.attack_indicator_timer > 0

    def get_attack_hitbox(self) -> pygame.Rect:
        return self.last_attack_rect.copy()

    def add_double_jump_charge(self, amount: int = 1) -> None:
        self.double_jump_charges += max(0, amount)

    def respawn(self, position: Tuple[int, int]) -> None:
        self.rect.topleft = position
        self.velocity.update(0, 0)
        self.health = self.max_health
        self.invulnerability_timer = 0.0
        self.attack_timer = 0.0
        self.attack_indicator_timer = 0.0
        self.double_jump_charges = 0
        self.air_jump_performed = False
        self.on_ground = False
        self.jump_buffer_timer = 0.0
        self.coyote_timer = 0.0

    def _ensure_sprite(self) -> Optional[pygame.Surface]:
        """Load and cache the hero sprite if the asset is available."""

        cls = type(self)
        if cls._sprite_surface is not None:
            return cls._sprite_surface

        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        sprite_path = assets_dir / "hero.png"
        if not sprite_path.exists():
            return None

        try:
            image = pygame.image.load(str(sprite_path))
        except pygame.error:
            return None

        if pygame.display.get_surface():
            try:
                image = image.convert_alpha()
            except pygame.error:
                pass

        cls._sprite_surface = pygame.transform.scale(image, self.rect.size)
        return cls._sprite_surface

    def get_oriented_sprite(self) -> Optional[pygame.Surface]:
        """Return the sprite oriented based on facing direction, if available."""

        base = self._sprite_surface or self._ensure_sprite()
        if base is None:
            return None
        if self.facing >= 0:
            return base
        cls = type(self)
        if cls._sprite_surface_flipped is None:
            cls._sprite_surface_flipped = pygame.transform.flip(base, True, False)
        return cls._sprite_surface_flipped


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
