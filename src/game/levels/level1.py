"""Definition for the first level of the Adventure platformer."""

from __future__ import annotations

from typing import Dict, List, Tuple

LevelData = Dict[str, object]


def load_level() -> LevelData:
    """Return the level data describing geometry and entity placement."""

    width, height = 1400, 640
    ground_height = 100

    platforms: List[Tuple[int, int, int, int]] = []

    ground_y = height - ground_height

    # Core ground path with gentle gaps that introduce basic jumping.
    platforms.extend(
        [
            (0, ground_y, 360, ground_height),
            (380, ground_y, 300, ground_height),
            (720, ground_y, 260, ground_height),
            (1020, ground_y, 200, ground_height),
            (1240, ground_y, 160, ground_height),
        ]
    )

    # Low ramps to ease players across the first pit.
    platforms.extend(
        [
            (320, ground_y - 60, 120, 20),
            (460, ground_y - 100, 120, 20),
        ]
    )

    # Floating platforms forming an optional upper route with safe spacing.
    platforms.extend(
        [
            (600, ground_y - 120, 140, 20),
            (760, ground_y - 160, 140, 20),
            (920, ground_y - 140, 140, 20),
            (1080, ground_y - 180, 120, 20),
            (1180, ground_y - 120, 120, 20),
        ]
    )

    # Finish alcove with clear entry and exit height.
    platforms.extend(
        [
            (1180, ground_y - 140, 20, 140),
            (1360, ground_y - 140, 20, 140),
            (1180, ground_y - 140, 200, 20),
            (1200, ground_y - 80, 160, 20),
        ]
    )

    enemies = [
        {"x": 200, "y": ground_y - 50, "min_x": 120, "max_x": 320, "health": 3},
        {"x": 640, "y": ground_y - 170, "min_x": 600, "max_x": 760, "health": 3},
        {"x": 860, "y": ground_y - 50, "min_x": 780, "max_x": 940, "health": 3},
        {"x": 1150, "y": ground_y - 50, "min_x": 1080, "max_x": 1220, "health": 3},
    ]

    finish_zone = (1220, ground_y - 160, 120, 120)

    return {
        "player_start": (50, height - ground_height - 60),
        "platforms": platforms,
        "enemies": enemies,
        "finish_zone": finish_zone,
        "world_size": (width, height),
    }
