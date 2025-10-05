"""Definition for the first level of the Adventure platformer."""

from __future__ import annotations

from typing import Dict, List, Tuple

LevelData = Dict[str, object]


def load_level() -> LevelData:
    """Return the level data describing geometry and entity placement."""

    width, height = 3000, 640
    ground_height = 90

    platforms: List[Tuple[int, int, int, int]] = []

    ground_y = height - ground_height

    # Ground segments with moderate gaps to encourage platforming without blocking progress.
    platforms.extend(
        [
            (0, ground_y, 560, ground_height),
            (640, ground_y, 420, ground_height),
            (1200, ground_y, 460, ground_height),
            (1840, ground_y, 520, ground_height),
            (2500, ground_y, 500, ground_height),
        ]
    )

    # Gentle ramps and ledges supporting jumps around the checkpoint and finale.
    platforms.extend(
        [
            (1100, ground_y - 60, 120, 60),
            (1720, ground_y - 60, 160, 60),
            (2380, ground_y - 60, 160, 60),
            (2840, ground_y - 80, 120, 80),
        ]
    )

    # Floating platforms with controlled heights for smoother traversal.
    platforms.extend(
        [
            (140, ground_y - 90, 150, 26),
            (340, ground_y - 130, 140, 26),
            (560, ground_y - 110, 150, 26),
            (780, ground_y - 120, 150, 26),
            (960, ground_y - 150, 160, 26),
            (1160, ground_y - 120, 160, 26),
            (1380, ground_y - 90, 160, 26),
            (1560, ground_y - 130, 160, 26),
            (1760, ground_y - 100, 170, 26),
            (1980, ground_y - 140, 170, 26),
            (2180, ground_y - 110, 150, 26),
            (2360, ground_y - 150, 150, 26),
            (2560, ground_y - 110, 170, 26),
            (2760, ground_y - 90, 140, 26),
            (2880, ground_y - 140, 140, 26),
        ]
    )

    enemies = [
        {"x": 260, "y": ground_y - 50, "min_x": 120, "max_x": 520, "health": 3},
        {"x": 820, "y": ground_y - 170, "min_x": 780, "max_x": 930, "health": 3},
        {"x": 1360, "y": ground_y - 140, "min_x": 1380, "max_x": 1540, "health": 3},
        {"x": 1760, "y": ground_y - 110, "min_x": 1720, "max_x": 1880, "health": 3},
        {"x": 2040, "y": ground_y - 190, "min_x": 1980, "max_x": 2150, "health": 3},
        {"x": 2420, "y": ground_y - 110, "min_x": 2380, "max_x": 2540, "health": 3},
        {"x": 2760, "y": ground_y - 140, "min_x": 2760, "max_x": 2900, "health": 3},
    ]

    finish_zone = (2860, ground_y - 120, 120, 120)

    checkpoint_zone = (1680, ground_y - 200, 220, 200)
    checkpoint_respawn = (1760, ground_y - 160)

    energy_orbs = [
        {"x": 940, "y": ground_y - 170},
        {"x": 2060, "y": ground_y - 190},
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
