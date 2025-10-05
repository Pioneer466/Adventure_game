"""Definition for the first level of the Adventure platformer."""

from __future__ import annotations

from typing import Dict, List, Tuple

LevelData = Dict[str, object]


def load_level() -> LevelData:
    """Return the level data describing geometry and entity placement."""

    width, height = 2600, 640
    ground_height = 90

    platforms: List[Tuple[int, int, int, int]] = []

    ground_y = height - ground_height

    # Ground segments with forgiving spacing to encourage forward motion.
    platforms.extend(
        [
            (0, ground_y, 520, ground_height),
            (600, ground_y, 340, ground_height),
            (1000, ground_y, 320, ground_height),
            (1380, ground_y, 320, ground_height),
            (1760, ground_y, 340, ground_height),
            (2140, ground_y, 460, ground_height),
        ]
    )

    # Floating platforms with gentle height differences for approachable jumps.
    platforms.extend(
        [
            (200, ground_y - 70, 150, 24),
            (420, ground_y - 120, 160, 24),
            (660, ground_y - 110, 160, 24),
            (880, ground_y - 150, 150, 24),
            (1100, ground_y - 120, 180, 24),
            (1260, ground_y - 170, 180, 24),
            (1480, ground_y - 110, 170, 24),
            (1660, ground_y - 160, 170, 24),
            (1860, ground_y - 110, 170, 24),
            (2040, ground_y - 160, 180, 24),
            (2240, ground_y - 120, 170, 24),
            (2420, ground_y - 90, 130, 24),
        ]
    )

    # Access ramps near the checkpoint.
    platforms.extend(
        [
            (1180, ground_y - 40, 90, 40),
            (1540, ground_y - 40, 90, 40),
        ]
    )

    # Enclosed finale to highlight the goal chamber.
    finish_top = ground_y - 120
    platforms.extend(
        [
            (2320, finish_top, 20, 120),
            (2460, finish_top, 20, 120),
            (2320, finish_top, 160, 20),
            (2340, finish_top + 60, 120, 20),
        ]
    )

    enemies = [
        {"x": 260, "y": ground_y - 50, "min_x": 120, "max_x": 420, "health": 3},
        {"x": 720, "y": ground_y - 150, "min_x": 660, "max_x": 820, "health": 3},
        {"x": 1180, "y": ground_y - 200, "min_x": 1100, "max_x": 1300, "health": 3},
        {"x": 1560, "y": ground_y - 70, "min_x": 1480, "max_x": 1660, "health": 3},
        {"x": 1980, "y": ground_y - 200, "min_x": 1880, "max_x": 2060, "health": 3},
        {"x": 2360, "y": ground_y - 100, "min_x": 2240, "max_x": 2440, "health": 3},
    ]

    finish_zone = (2360, finish_top + 20, 120, 80)

    checkpoint_zone = (1280, ground_y - 180, 200, 200)
    checkpoint_respawn = (1340, ground_y - 140)

    energy_orbs = [
        {"x": 620, "y": ground_y - 140},
        {"x": 1400, "y": ground_y - 210},
        {"x": 1860, "y": ground_y - 180},
        {"x": 2260, "y": ground_y - 150},
    ]

    return {
        "player_start": (50, ground_y - 60),
        "platforms": platforms,
        "enemies": enemies,
        "finish_zone": finish_zone,
        "world_size": (width, height),
        "checkpoint": {"zone": checkpoint_zone, "respawn": checkpoint_respawn},
        "energy_orbs": energy_orbs,
    }
