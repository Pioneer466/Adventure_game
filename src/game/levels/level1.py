"""Definition for the first level of the Adventure platformer."""

from __future__ import annotations

from typing import Dict, List, Tuple

LevelData = Dict[str, object]


def load_level() -> LevelData:
    """Return the level data describing geometry and entity placement."""

    width, height = 2200, 680
    ground_height = 110

    platforms: List[Tuple[int, int, int, int]] = []

    ground_y = height - ground_height

    # Ground segments with gentle gaps to create rhythm over a longer run.
    platforms.extend(
        [
            (0, ground_y, 420, ground_height),
            (460, ground_y, 320, ground_height),
            (820, ground_y, 260, ground_height),
            (1120, ground_y, 220, ground_height),
            (1380, ground_y, 220, ground_height),
            (1660, ground_y, 220, ground_height),
            (1920, ground_y, 280, ground_height),
        ]
    )

    # Staggered upper platforms to build a flowing skyline route.
    platforms.extend(
        [
            (320, ground_y - 70, 120, 20),
            (520, ground_y - 120, 140, 20),
            (700, ground_y - 160, 140, 20),
            (880, ground_y - 200, 140, 20),
            (1020, ground_y - 150, 140, 20),
            (1080, ground_y - 90, 160, 20),
            (1180, ground_y - 200, 140, 20),
            (1320, ground_y - 240, 140, 20),
            (1480, ground_y - 190, 140, 20),
            (1640, ground_y - 230, 150, 20),
            (1800, ground_y - 180, 150, 20),
            (1980, ground_y - 220, 150, 20),
            (2100, ground_y - 150, 120, 20),
        ]
    )

    # Enclosed finale to showcase the goal room clearly.
    finish_top = ground_y - 150
    platforms.extend(
        [
            (2020, finish_top, 20, 150),
            (2150, finish_top, 20, 150),
            (2020, finish_top, 150, 20),
            (2040, finish_top + 60, 110, 20),
        ]
    )

    enemies = [
        {"x": 220, "y": ground_y - 50, "min_x": 120, "max_x": 360, "health": 3},
        {"x": 600, "y": ground_y - 170, "min_x": 520, "max_x": 700, "health": 3},
        {"x": 880, "y": ground_y - 250, "min_x": 820, "max_x": 940, "health": 3},
        {"x": 1260, "y": ground_y - 50, "min_x": 1180, "max_x": 1360, "health": 3},
        {"x": 1720, "y": ground_y - 80, "min_x": 1660, "max_x": 1820, "health": 3},
        {"x": 2050, "y": ground_y - 210, "min_x": 1980, "max_x": 2100, "health": 3},
    ]

    finish_zone = (2060, finish_top + 20, 90, 110)

    checkpoint_zone = (1090, ground_y - 200, 140, 200)
    checkpoint_respawn = (1120, ground_y - 150)

    energy_orbs = [
        {"x": 760, "y": ground_y - 190},
        {"x": 1220, "y": ground_y - 170},
        {"x": 1820, "y": ground_y - 210},
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
