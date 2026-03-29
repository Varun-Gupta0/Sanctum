"""
Pipeline Core — X (Structure + Pipeline Layer)
Central orchestrator for the structural intelligence system.
"""

from typing import Optional
from pathlib import Path

from loader import load_data
from analyze import analyze_wall
from materials import recommend_material
from explain import explain as generate_explanation
from formatter import print_report, write_json
from render_rooms import render_rooms as render_3d


def adapt_wall(wall: dict) -> dict:
    """Convert wall from X's input format to Y's enriched analysis format.

    Routes through analyze_wall() so Y's intelligence functions always receive
    the full enriched dict (span, area, load_bearing, confidence, suggestion…).

    Input:  {"type": "load_bearing", "length": 31}
    Output: analyze_wall() enriched dict

    Parameters
    ----------
    wall : dict
        Wall with "type" (str) and "length" (num)

    Returns
    -------
    dict
        Fully enriched analysis dict from analyze_wall()
    """
    wall_type = wall.get("type", "")
    is_load_bearing = wall_type == "load_bearing"
    length = wall.get("length", 0)

    # Synthesize a minimal room dict to feed into analyze_wall.
    # Walls don't have width/length as separate dims, so treat span = length.
    synthetic_room = {
        "name": wall_type.replace("_", " ").title(),
        "width": length,
        "length": length,
        "load_bearing": is_load_bearing,
    }
    return analyze_wall(synthetic_room)


def run_pipeline(
    input_path: Optional[str] = None,
    output_path: str = "output.json",
    render: bool = True,
) -> dict:
    """Execute the full structural intelligence pipeline.

    Parameters
    ----------
    input_path : str | None
        Path to JSON input file. If None, uses defaults from data.py
    output_path : str
        Path for JSON report output (default: "output.json")
    render : bool
        Whether to render 3D visualization (default: True)

    Returns
    -------
    dict
        The complete report with rooms, walls, and results
    """
    data = load_data(input_path)
    rooms = data["rooms"]
    walls = data["walls"]

    results = []
    for wall in walls:
        adapted = adapt_wall(wall)
        material = recommend_material(adapted)
        report_entry = generate_explanation(adapted, material)  # returns rich dict
        results.append({
            "wall": wall,
            "material": material,
            # Unpack all Y intelligence fields at top level for easy consumption
            "explanation": report_entry.get("explanation", ""),
            "confidence": report_entry.get("confidence", ""),
            "suggestion": report_entry.get("suggestion", ""),
            "why_not": report_entry.get("why_not", {}),
        })

    report = {
        "rooms": rooms,
        "walls": walls,
        "results": results,
    }

    print_report(report)
    write_json(report, output_path)

    if render:
        render_3d(rooms)

    return report


if __name__ == "__main__":
    run_pipeline(input_path="input.json")
