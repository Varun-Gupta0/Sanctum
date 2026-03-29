"""
Pipeline Core — X (Structure + Pipeline Layer)
Central orchestrator for the structural intelligence system.
"""

import webbrowser
from pathlib import Path

from loader import load_data
from materials import recommend_material, calculate_risk_score
from explain import explain as generate_explanation
from formatter import print_report, write_json
from render_rooms import render_rooms as render_3d, generate_plotly_json


def adapt_wall(wall: dict) -> dict:
    """Convert wall from input format to Y's expected format.

    Input:  {"type": "load_bearing", "length": 31}
    Output: {"load_bearing": True, "length": 31}

    Parameters
    ----------
    wall : dict
        Wall with "type" (str) and "length" (num)

    Returns
    -------
    dict
        Wall adapted for Y's functions with boolean load_bearing key
    """
    wall_type = wall.get("type", "")
    is_load_bearing = wall_type == "load_bearing"

    return {
        "load_bearing": is_load_bearing,
        "length": wall.get("length", 0),
    }


def run_pipeline(
    input_path: str | None = None,
    output_path: str = "output.json",
    render: bool = True,
    data_dict: dict | None = None,
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
    if data_dict is not None:
        data = data_dict
    else:
        data = load_data(input_path)
    rooms = data["rooms"]
    walls = data["walls"]

    results = []
    for wall in walls:
        adapted = adapt_wall(wall)
        material = recommend_material(adapted)
        explanation = generate_explanation(adapted, material)
        risk_score = calculate_risk_score(adapted, material)
        results.append({
            "wall": wall,
            "material": material,
            "explanation": explanation,
            "risk_score": risk_score,
        })
        
    room_scores = {}
    for r in results:
        w = r["wall"]
        rid = w.get("room_id")
        if rid:
            room_scores[rid] = max(room_scores.get(rid, 0), r["risk_score"])
            
    fig_json = generate_plotly_json(rooms, results)

    report = {
        "rooms": rooms,
        "walls": walls,
        "results": results,
        "room_scores": room_scores,
        "diagram": fig_json,
    }

    print_report(report)
    write_json(report, output_path)

    if render:
        render_3d(rooms)

    return report


if __name__ == "__main__":
    run_pipeline(input_path="input.json")
