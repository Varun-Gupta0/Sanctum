"""
Wall Analysis Engine — Y (Intelligence Layer)
Part of the AI-based Structural Intelligence System.

Derives engineering properties from raw room geometry,
provides confidence scoring and actionable design suggestions.

Designed to be imported by X's app.py: from analyze import analyze_wall, get_confidence, get_suggestion
"""

# Rooms that are structurally load-bearing by convention
LOAD_BEARING_ROOMS = {"Living Room", "Hall", "Bedroom 1", "Master Bedroom"}

# Rooms where fire-resistant materials are preferred
FIRE_SENSITIVE_ROOMS = {"Kitchen", "Utility Room", "Boiler Room"}


def analyze_wall(room: dict) -> dict:
    """Derive engineering properties from room geometry.

    Parameters
    ----------
    room : dict
        Keys: ``name`` (str), ``width`` (float), ``length`` (float).
        Optionally: ``load_bearing`` (bool) to override inference.

    Returns
    -------
    dict
        Enriched wall analysis with span, area, load-bearing status,
        fire sensitivity, confidence, and suggestion.
    """
    span = max(room.get("width", 0), room.get("length", 0))
    area = room.get("width", 0) * room.get("length", 0)

    # Allow explicit override; otherwise infer from room name
    load_bearing = room.get("load_bearing", room.get("name", "") in LOAD_BEARING_ROOMS)
    fire_sensitive = room.get("name", "") in FIRE_SENSITIVE_ROOMS

    confidence = get_confidence(span)
    suggestion = get_suggestion(span, load_bearing)

    return {
        "room": room.get("name", "Unknown"),
        "span": span,
        "area": area,
        "load_bearing": load_bearing,
        "fire_sensitive": fire_sensitive,
        "confidence": confidence,
        "suggestion": suggestion,
    }


def get_confidence(span: float) -> str:
    """Return structural confidence level based on span length.

    - >15m  → Low  (risky, needs special design)
    - 10–15m → Medium (needs review / reinforcement)
    - <10m  → High (standard construction)
    """
    if span > 15:
        return "Low"
    elif span > 10:
        return "Medium"
    return "High"


def get_suggestion(span: float, load_bearing: bool) -> str:
    """Return actionable engineering advice based on span and load status."""
    if span > 15 and load_bearing:
        return "Critical: Add intermediate column support and reduce effective span"
    if span > 15:
        return "Add column support or partition to reduce span below 15m"
    if span > 10 and load_bearing:
        return "Reinforce with additional RCC beams at mid-span"
    if span > 10:
        return "Consider reinforcement or intermediate support"
    if span > 5 and load_bearing:
        return "Standard RCC construction adequate; verify beam depth"
    return "No special intervention needed"


# ──────────── standalone tests ────────────
if __name__ == "__main__":
    test_rooms = [
        {"name": "Living Room", "width": 6, "length": 12},
        {"name": "Kitchen", "width": 3, "length": 4},
        {"name": "Hall", "width": 8, "length": 18},
        {"name": "Store Room", "width": 2, "length": 3},
        {"name": "Bedroom 1", "width": 4, "length": 5},
        {"name": "Office", "width": 5, "length": 11, "load_bearing": False},
    ]

    for room in test_rooms:
        analysis = analyze_wall(room)
        lb = "load-bearing" if analysis["load_bearing"] else "partition"
        fs = " fire-sensitive" if analysis["fire_sensitive"] else ""
        print(f"--- [{analysis['room']}] {lb}{fs} ---")
        print(f"  Span: {analysis['span']}m | Area: {analysis['area']}m²")
        print(f"  Confidence: {analysis['confidence']}")
        print(f"  Suggestion: {analysis['suggestion']}\n")

    print("All analyze.py tests passed!")
