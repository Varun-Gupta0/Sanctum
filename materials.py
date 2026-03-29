"""
Material Recommendation Engine — Y (Intelligence Layer)
Part of the AI-based Structural Intelligence System.

Smarter rule-based logic with prioritized multi-factor decisions.
Designed to be imported by X's app.py: from materials import recommend_material
"""

# ──────────────────────────────────────────────
# RULES — evaluated top-down, first match wins.
# To extend: just append (predicate, material).
# ──────────────────────────────────────────────
RULES = [
    # Priority 1: load-bearing AND long span → strongest pick
    (lambda w: w.get("load_bearing", False) and w.get("length", 0) > 5, "RCC"),
    # Priority 2: load-bearing (any length) → structural safety
    (lambda w: w.get("load_bearing", False), "RCC"),
    # Priority 3: long span partition → needs rigid support
    (lambda w: w.get("length", 0) > 5, "Steel Frame"),
]

DEFAULT_MATERIAL = "Red Brick"


def recommend_material(wall: dict) -> str:
    """Recommend the optimal construction material for a wall.

    Parameters
    ----------
    wall : dict
        Keys: ``load_bearing`` (bool), ``length`` (float/int), etc.

    Returns
    -------
    str
        One of ``"RCC"``, ``"Steel Frame"``, or ``"Red Brick"``.
    """
    for predicate, material in RULES:
        if predicate(wall):
            return material
    return DEFAULT_MATERIAL


# ──────────── standalone tests ────────────
if __name__ == "__main__":
    tests = [
        ({"load_bearing": True, "length": 8},  "RCC"),          # priority 1
        ({"load_bearing": True, "length": 3},  "RCC"),          # priority 2
        ({"load_bearing": False, "length": 7}, "Steel Frame"),  # priority 3
        ({"load_bearing": False, "length": 3}, "Red Brick"),    # default
        ({"load_bearing": True, "length": 6},  "RCC"),          # combo → RCC wins
        ({},                                    "Red Brick"),    # empty wall
    ]
    for wall, expected in tests:
        result = recommend_material(wall)
        status = "✓" if result == expected else "✗"
        print(f"  {status}  {wall!s:<45} → {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    print("\n✅ All materials.py tests passed!")
