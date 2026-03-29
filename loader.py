"""
Data Loader — X (Structure + Pipeline Layer)
Loads room/wall data from JSON, Images, or falls back to data.py defaults.
"""

import json
from pathlib import Path
from typing import Optional

import data
from image_parser import extract_rooms_from_image


def load_data(path: Optional[str] = None) -> dict:
    """Load room and wall data from a JSON or Image file, or fall back to defaults.

    Parameters
    ----------
    path : str | None
        Path to JSON or Image (.png, .jpg, .jpeg) input file. 
        If None, or file not found, falls back to data.py defaults.

    Returns
    -------
    dict
        Keys: "rooms" (list), "walls" (list)
    """
    if path:
        file_path = Path(path)
        if file_path.exists():
            # 1. Image Input Mode
            if file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                print(f"[LOADER] Image Mode active. Extracting layout from {file_path.name}")
                return extract_rooms_from_image(str(file_path), scale_factor=0.05)
            
            # 2. Standard JSON Input
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                print(f"[LOADER] Reading from {file_path.name}")
                _validate_data(loaded)
                return loaded
            except Exception as e:
                print(f"[LOADER] Error reading JSON '{path}': {e}")
        else:
            print(f"[LOADER] File '{path}' not found, using default layout.")

    print("[LOADER] Falling back to default layout from data.py")
    return {
        "rooms": data.rooms,
        "walls": data.walls,
    }


def _validate_data(data_dict: dict) -> None:
    """Validate that required keys exist in loaded data."""
    if "rooms" not in data_dict:
        raise ValueError("JSON must contain 'rooms' key")
    if "walls" not in data_dict:
        raise ValueError("JSON must contain 'walls' key")

    for i, room in enumerate(data_dict["rooms"]):
        required = ("name", "x", "y", "width", "length")
        for key in required:
            if key not in room:
                raise ValueError(f"rooms[{i}]: missing required key '{key}'")

    for i, wall in enumerate(data_dict["walls"]):
        if "type" not in wall:
            raise ValueError(f"walls[{i}]: missing required key 'type'")
        if "length" not in wall:
            raise ValueError(f"walls[{i}]: missing required key 'length'")


if __name__ == "__main__":
    d = load_data()
    print(f"Loaded {len(d['rooms'])} rooms, {len(d['walls'])} walls")
