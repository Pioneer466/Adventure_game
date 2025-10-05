"""Definition for the first level of the Adventure platformer."""

from __future__ import annotations

from typing import Dict, List, Tuple

LevelData = Dict[str, object]


def load_level() -> LevelData:
    """Return the level data describing geometry and entity placement."""

    width, height = 960, 640
    ground_height = 80

    platforms: List[Tuple[int, int, int, int]] = []

    # Ground platform covering the bottom of the level.
    platforms.append((0, height - ground_height, width, ground_height))

    # Floating platforms to create vertical gameplay.
    platforms.extend(
        [
            (150, 420, 160, 20),
            (360, 340, 140, 20),
            (580, 280, 180, 20),
            (780, 200, 120, 20),
        ]
    )

    # Elevated platforms leading to the finish room.
    platforms.extend(
        [
            (100, 520, 140, 20),
            (320, 480, 160, 20),
            (540, 440, 160, 20),
            (760, 400, 160, 20),
        ]
    )

    enemies = [
        {"x": 200, "y": height - ground_height - 50, "min_x": 150, "max_x": 320, "health": 3},
        {"x": 420, "y": 320, "min_x": 360, "max_x": 500, "health": 2},
        {"x": 610, "y": 260, "min_x": 580, "max_x": 760, "health": 3},
    ]

    finish_zone = (880, height - ground_height - 120, 60, 120)

    return {
        "player_start": (50, height - ground_height - 60),
        "platforms": platforms,
        "enemies": enemies,
        "finish_zone": finish_zone,
        "world_size": (width, height),
    }
