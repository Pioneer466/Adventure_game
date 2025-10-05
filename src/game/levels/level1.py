"""Definition for the first level of the Adventure platformer."""

from __future__ import annotations

from typing import Dict, List, Tuple

LevelData = Dict[str, object]


def load_level() -> LevelData:
    """Return the level data describing geometry and entity placement."""

    width, height = 1800, 720
    ground_height = 100

    platforms: List[Tuple[int, int, int, int]] = []

    ground_y = height - ground_height

    # Ground segments with gaps to encourage jumping and pacing.
    platforms.extend(
        [
            (0, ground_y, 360, ground_height),
            (480, ground_y, 240, ground_height),
            (820, ground_y, 220, ground_height),
            (1120, ground_y, 240, ground_height),
            (1420, ground_y, 380, ground_height),
        ]
    )

    # Introductory ramps easing the player into the first jumps.
    platforms.extend(
        [
            (320, ground_y - 60, 140, 20),
            (420, ground_y - 120, 110, 20),
        ]
    )

    # Mid-level floating platforms forming a winding aerial route.
    platforms.extend(
        [
            (560, ground_y - 80, 140, 20),
            (700, ground_y - 120, 120, 20),
            (860, ground_y - 160, 140, 20),
            (940, ground_y - 260, 120, 20),
            (1060, ground_y - 200, 140, 20),
            (1160, ground_y - 160, 140, 20),
            (1240, ground_y - 280, 100, 20),
            (1320, ground_y - 200, 120, 20),
            (1360, ground_y - 140, 120, 20),
            (1380, ground_y - 100, 100, 20),
            (1460, ground_y - 60, 80, 20),
        ]
    )

    # Finish room structure with walls, ceiling and a raised floor.
    platforms.extend(
        [
            (1440, ground_y - 120, 20, 120),
            (1780, ground_y - 120, 20, 120),
            (1440, ground_y - 120, 360, 20),
            (1520, ground_y - 60, 200, 20),
            (1420, ground_y - 60, 60, 20),
        ]
    )

    enemies = [
        {"x": 180, "y": ground_y - 50, "min_x": 80, "max_x": 320, "health": 3},
        {"x": 600, "y": ground_y - 130, "min_x": 560, "max_x": 700, "health": 2},
        {"x": 880, "y": ground_y - 210, "min_x": 860, "max_x": 1000, "health": 3},
        {"x": 950, "y": ground_y - 50, "min_x": 820, "max_x": 1060, "health": 3},
        {"x": 1620, "y": ground_y - 110, "min_x": 1520, "max_x": 1720, "health": 4},
    ]

    finish_zone = (1600, ground_y - 160, 120, 120)

    return {
        "player_start": (50, height - ground_height - 60),
        "platforms": platforms,
        "enemies": enemies,
        "finish_zone": finish_zone,
        "world_size": (width, height),
    }
