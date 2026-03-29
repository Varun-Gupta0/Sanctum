"""
Material Recommendation Engine — Y (Intelligence Layer) — Phase 2
Part of the AI-based Structural Intelligence System.

Multi-factor decision engine: uses span, area, load-bearing status,
room type, and fire sensitivity. Safety first, then cost optimization.

Designed to be imported by X's app.py: from materials import recommend_material
"""


def recommend_material(analysis: dict) -> str:
    """Recommend construction material from enriched wall analysis.

    Parameters
    ----------
    analysis : dict
        Output from ``analyze.analyze_wall()`` — must include:
        ``span``, ``area``, ``load_bearing``, ``fire_sensitive``.

    Returns
    -------
    str
        One of ``"RCC"``, ``"Steel Frame"``, or ``"Red Brick"``.
    """
    span = analysis.get("span", 0)
    area = analysis.get("area", 0)
    load_bearing = analysis.get("load_bearing", False)
    fire_sensitive = analysis.get("fire_sensitive", False)

    # ── SAFETY-CRITICAL: load-bearing walls ──
    if load_bearing and span > 10:
        return "RCC"           # heavy span + structural load → only RCC
    if load_bearing and span > 5:
        return "RCC"           # moderate span + load → RCC preferred
    if load_bearing:
        return "RCC"           # any load-bearing → RCC for safety

    # ── FIRE-SENSITIVE rooms ──
    if fire_sensitive and span > 5:
        return "RCC"           # fire zone + large span → RCC (non-combustible + strong)
    if fire_sensitive:
        return "Red Brick"     # fire zone + short span → brick (naturally fire-resistant)

    # ── PARTITIONS by span ──
    if span > 10:
        return "Steel Frame"   # very large partition → steel rigidity
    if span > 5:
        return "Steel Frame"   # large partition → steel support

    # ── AREA-BASED refinement ──
    if area > 30:
        return "Steel Frame"   # large open room even with short walls → steel stiffness

    return "Red Brick"         # standard short partition → cost-effective brick


# ──────────── standalone tests ────────────
if __name__ == "__main__":
    tests = [
        # (analysis_dict, expected_material)
        ({"span": 12, "area": 72, "load_bearing": True, "fire_sensitive": False},  "RCC"),
        ({"span": 6,  "area": 24, "load_bearing": True, "fire_sensitive": False},  "RCC"),
        ({"span": 3,  "area": 12, "load_bearing": True, "fire_sensitive": False},  "RCC"),
        ({"span": 7,  "area": 28, "load_bearing": False, "fire_sensitive": True},  "RCC"),
        ({"span": 3,  "area": 12, "load_bearing": False, "fire_sensitive": True},  "Red Brick"),
        ({"span": 12, "area": 48, "load_bearing": False, "fire_sensitive": False}, "Steel Frame"),
        ({"span": 7,  "area": 28, "load_bearing": False, "fire_sensitive": False}, "Steel Frame"),
        ({"span": 3,  "area": 36, "load_bearing": False, "fire_sensitive": False}, "Steel Frame"),
        ({"span": 3,  "area": 12, "load_bearing": False, "fire_sensitive": False}, "Red Brick"),
    ]

    print("materials.py — Phase 2 Multi-Factor Tests\n")
    all_pass = True
    for analysis, expected in tests:
        result = recommend_material(analysis)
        ok = result == expected
        if not ok:
            all_pass = False
        status = "✓" if ok else "✗"
        lb = "LB" if analysis["load_bearing"] else "PT"
        fs = " 🔥" if analysis["fire_sensitive"] else ""
        print(f"  {status}  [{lb}{fs}] span={analysis['span']}m area={analysis['area']}m² → {result}")

    assert all_pass, "Some tests failed!"
    print("\n✅ All materials.py Phase 2 tests passed!")
