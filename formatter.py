"""
Output Formatter — X (Structure + Pipeline Layer)
Console display and JSON output for the structural intelligence report.
"""

from __future__ import annotations

import json
from pathlib import Path


def print_report(report: dict) -> None:
    """Print a formatted console report of the structural analysis.

    Parameters
    ----------
    report : dict
        Must contain: "rooms" (list), "walls" (list), "results" (list)
    """
    rooms = report.get("rooms", [])
    walls = report.get("walls", [])
    results = report.get("results", [])

    num_rooms = len(rooms)
    num_walls = len(walls)

    print()
    print("=" * 60)
    print("  PLANWISE — Structural Intelligence Report")
    print("=" * 60)
    print(f"\n  House Layout: {num_rooms} rooms, {num_walls} walls")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        wall = result.get("wall", {})
        material = result.get("material", "Unknown")
        explanation = result.get("explanation", "No explanation available.")

        wall_type = wall.get("type", "unknown")
        length = wall.get("length", 0)

        print(f"\n  [WALL #{i}]  {wall_type.title():15} |  {length}m")
        print(f"  Material   : {material}")
        print(f"  Reason     : {explanation}")
        print("-" * 60)

    print(f"\n  Report complete. {num_walls} walls analyzed.")
    print("=" * 60)


def write_json(report: dict, path: str = "output.json") -> None:
    """Write the report to a JSON file for frontend consumption.

    Parameters
    ----------
    report : dict
        The complete report dictionary.
    path : str
        Output file path (default: "output.json")
    """
    out_path = Path(path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n  JSON report saved -> {out_path.name}")
