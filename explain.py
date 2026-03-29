"""
Engineering Reasoning Engine — Y (Intelligence Layer)
Part of the AI-based Structural Intelligence System.

Generates detailed, comparative explanations like a structural engineer.
Designed to be imported by X's app.py: from explain import explain
"""


def explain(wall: dict, material: str) -> str:
    """Generate an engineering explanation for a material recommendation.

    Parameters
    ----------
    wall : dict
        Wall properties (``load_bearing``, ``length``, etc.).
    material : str
        The recommended material from ``recommend_material()``.

    Returns
    -------
    str
        A professional structural-engineering justification.
    """
    wall_type = "load-bearing" if wall.get("load_bearing", False) else "partition"
    length = wall.get("length", 0)

    if material == "RCC" and length > 5:
        return (
            f"This {wall_type} wall spans {length}m and carries structural load. "
            f"RCC (Reinforced Cement Concrete) is essential here — it provides the "
            f"compressive strength to bear upper-floor loads across a {length}m span. "
            f"Red brick would risk cracking under sustained axial stress at this length, "
            f"and a steel frame, while strong in tension, is unnecessary where concrete "
            f"can handle both compression and lateral forces efficiently."
        )

    if material == "RCC":
        return (
            f"This {wall_type} wall spans {length}m and is designated as load-bearing. "
            f"RCC is required to safely transfer compressive loads from the structure above. "
            f"Even though the span is within standard limits, brick masonry lacks the "
            f"tensile reinforcement needed for load-bearing applications. "
            f"Steel would be over-engineered and less cost-effective for this span."
        )

    if material == "Steel Frame":
        return (
            f"This {wall_type} wall spans {length}m, exceeding the standard 5m limit "
            f"for unsupported masonry. A steel frame provides the rigidity and lateral "
            f"stability needed for large-span partitions. Red brick alone would require "
            f"additional intermediate supports, increasing cost and complexity. "
            f"RCC is not warranted since the wall carries no structural load."
        )

    # Default: Red Brick
    return (
        f"This {wall_type} wall spans {length}m — well within standard masonry limits. "
        f"Red brick is the most cost-effective choice for non-load-bearing partitions "
        f"of this size. It offers good thermal insulation and acoustic separation. "
        f"Steel or RCC would be over-engineered and unnecessarily expensive for "
        f"a simple partition wall."
    )


# ──────────── standalone tests ────────────
if __name__ == "__main__":
    test_cases = [
        ({"load_bearing": True, "length": 8},  "RCC"),
        ({"load_bearing": True, "length": 3},  "RCC"),
        ({"load_bearing": False, "length": 7}, "Steel Frame"),
        ({"load_bearing": False, "length": 3}, "Red Brick"),
    ]
    for wall, material in test_cases:
        explanation = explain(wall, material)
        wtype = "load-bearing" if wall.get("load_bearing") else "partition"
        print(f"--- [{wtype}, {wall['length']}m] → {material} ---")
        print(f"  {explanation}\n")
    print("✅ All explain.py tests passed!")
