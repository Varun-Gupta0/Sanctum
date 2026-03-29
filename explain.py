"""
Engineering Reasoning Engine — Y (Intelligence Layer) — Phase 2
Part of the AI-based Structural Intelligence System.

"Why Not" engine: returns structured dicts with comparative rejection
reasoning for every alternative material, confidence, and suggestions.

Designed to be imported by X's app.py: from explain import explain
"""


# ── Material properties for comparative reasoning ──
MATERIAL_PROPERTIES = {
    "RCC": {
        "strengths": "high compressive and tensile strength, excellent durability, fire-resistant",
        "weaknesses": "higher cost, longer curing time",
    },
    "Steel Frame": {
        "strengths": "high tensile strength, lightweight, ideal for large spans",
        "weaknesses": "expensive, requires fire-proofing, prone to corrosion",
    },
    "Red Brick": {
        "strengths": "cost-effective, good thermal insulation, fire-resistant, easy to source",
        "weaknesses": "low tensile strength, unsuitable for large spans or heavy loads",
    },
}


def explain(analysis: dict, material: str) -> dict:
    """Generate a structured engineering explanation with comparative reasoning.

    Parameters
    ----------
    analysis : dict
        Output from ``analyze.analyze_wall()`` — includes span, area,
        load_bearing, fire_sensitive, confidence, suggestion, room.
    material : str
        The recommended material from ``recommend_material()``.

    Returns
    -------
    dict
        Structured report with keys: material, confidence, suggestion,
        explanation, why_not.
    """
    span = analysis.get("span", 0)
    load_bearing = analysis.get("load_bearing", False)
    fire_sensitive = analysis.get("fire_sensitive", False)
    confidence = analysis.get("confidence", "Unknown")
    suggestion = analysis.get("suggestion", "")
    room = analysis.get("room", "Unknown")
    area = analysis.get("area", 0)

    wall_type = "load-bearing" if load_bearing else "partition"
    fire_note = " in a fire-sensitive zone" if fire_sensitive else ""

    # ── Build main explanation ──
    explanation = _build_explanation(material, wall_type, span, area, fire_note)

    # ── Build "why not" for rejected materials ──
    why_not = {}
    all_materials = ["RCC", "Steel Frame", "Red Brick"]
    for alt in all_materials:
        if alt != material:
            why_not[alt] = _why_not(alt, wall_type, span, load_bearing, fire_sensitive)

    return {
        "room": room,
        "material": material,
        "confidence": confidence,
        "suggestion": suggestion,
        "explanation": explanation,
        "why_not": why_not,
    }


def _build_explanation(material: str, wall_type: str, span: float,
                       area: float, fire_note: str) -> str:
    """Build the primary reasoning paragraph."""
    props = MATERIAL_PROPERTIES[material]

    if material == "RCC" and span > 10:
        return (
            f"This {wall_type} wall spans {span}m{fire_note}, which is a critical "
            f"long-span scenario. RCC is the only viable choice — it provides "
            f"{props['strengths']}. At {span}m, the structure must resist significant "
            f"bending moments and shear forces that neither brick nor unreinforced "
            f"materials can handle safely."
        )

    if material == "RCC":
        return (
            f"This {wall_type} wall spans {span}m{fire_note} and requires structural "
            f"integrity under load. RCC offers {props['strengths']}, making it the "
            f"safest and most reliable choice. The {area}m² room area confirms that "
            f"this wall supports meaningful structural weight from above."
        )

    if material == "Steel Frame" and span > 10:
        return (
            f"This {wall_type} wall spans {span}m{fire_note} — a large open span "
            f"requiring exceptional lateral rigidity. A steel frame provides "
            f"{props['strengths']}. For a non-load-bearing partition of this scale, "
            f"steel offers the best strength-to-weight ratio without the cost and "
            f"curing overhead of RCC."
        )

    if material == "Steel Frame":
        return (
            f"This {wall_type} wall spans {span}m{fire_note}, exceeding the standard "
            f"5m masonry limit. A steel frame provides {props['strengths']}, ensuring "
            f"the partition remains stable across the full span without intermediate "
            f"supports. This balances structural performance with cost efficiency."
        )

    # Red Brick
    return (
        f"This {wall_type} wall spans {span}m{fire_note} — well within standard "
        f"masonry limits. Red brick offers {props['strengths']}. For a partition "
        f"of this size ({area}m² room), brick provides the best balance of "
        f"performance, cost, and constructability."
    )


def _why_not(material: str, wall_type: str, span: float,
             load_bearing: bool, fire_sensitive: bool) -> str:
    """Explain why a specific alternative material was NOT chosen."""
    if material == "RCC":
        if not load_bearing and span <= 5:
            return (
                "RCC would be over-engineered for a short partition wall. "
                "The added cost and construction complexity are not justified "
                "when the wall carries no structural load."
            )
        if not load_bearing:
            return (
                "While RCC would provide adequate strength, it is unnecessarily "
                "expensive for a non-load-bearing wall. The structural overhead "
                "is not warranted."
            )
        return "RCC is viable but a more cost-effective alternative was found."

    if material == "Steel Frame":
        if load_bearing:
            return (
                "Steel frames excel in tension but are less efficient than RCC "
                "for compressive load-bearing applications. Steel also requires "
                "additional fire-proofing and corrosion protection."
            )
        if span <= 5:
            return (
                "A steel frame is over-engineered for a short-span partition. "
                "The cost premium over brick is not justified at this span."
            )
        if fire_sensitive:
            return (
                "Steel requires fire-proofing treatment in fire-sensitive zones, "
                "adding cost and complexity. Other materials offer inherent "
                "fire resistance."
            )
        return "Steel is viable but a more cost-effective alternative was selected."

    # Red Brick
    if load_bearing:
        return (
            "Red brick lacks the tensile reinforcement needed for load-bearing "
            "walls. Under sustained axial and lateral loads, brick masonry "
            "risks cracking and structural failure."
        )
    if span > 5:
        return (
            f"At {span}m, red brick would require intermediate supports to "
            f"prevent lateral instability. This adds cost and defeats the "
            f"simplicity advantage of brick construction."
        )
    if fire_sensitive and span > 5:
        return (
            "While brick is naturally fire-resistant, it cannot safely span "
            f"{span}m without intermediate support in a fire-sensitive zone."
        )
    return "Red brick is viable but a stronger material was preferred for this configuration."


# ──────────── standalone tests ────────────
if __name__ == "__main__":
    test_cases = [
        ({"room": "Living Room", "span": 12, "area": 72, "load_bearing": True,
          "fire_sensitive": False, "confidence": "Medium",
          "suggestion": "Reinforce with additional RCC beams at mid-span"}, "RCC"),
        ({"room": "Kitchen", "span": 4, "area": 12, "load_bearing": False,
          "fire_sensitive": True, "confidence": "High",
          "suggestion": "No special intervention needed"}, "Red Brick"),
        ({"room": "Office", "span": 11, "area": 55, "load_bearing": False,
          "fire_sensitive": False, "confidence": "Medium",
          "suggestion": "Consider reinforcement or intermediate support"}, "Steel Frame"),
        ({"room": "Bedroom 1", "span": 5, "area": 20, "load_bearing": True,
          "fire_sensitive": False, "confidence": "High",
          "suggestion": "No special intervention needed"}, "RCC"),
    ]

    for analysis, material in test_cases:
        result = explain(analysis, material)
        print(f"--- [{result['room']}] ---")
        print(f"  Material:    {result['material']}")
        print(f"  Confidence:  {result['confidence']}")
        print(f"  Suggestion:  {result['suggestion']}")
        print(f"  Explanation: {result['explanation']}")
        print(f"  Why not:")
        for alt, reason in result["why_not"].items():
            print(f"    ❌ {alt}: {reason}")
        print()

        # Verify structure
        assert "material" in result
        assert "confidence" in result
        assert "suggestion" in result
        assert "explanation" in result
        assert "why_not" in result
        assert len(result["why_not"]) == 2  # exactly 2 rejected alternatives

    print("✅ All explain.py Phase 2 tests passed!")
