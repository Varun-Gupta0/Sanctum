import json
import webbrowser
from pathlib import Path

import plotly.graph_objects as go

# --- INTEGRATION: IMPORT Y-INTELLIGENCE MODULES ---
from data import rooms as DATA_ROOMS
from analyze import analyze_wall, get_confidence, get_suggestion
from materials import recommend_material
from explain import explain

# [REPLACED] Old internal logic functions get_material, get_risk, get_explanation removed.

def render_rooms(rooms):
    """3D floor-plan visualization powered by Intelligence Layer logic."""
    fig = go.Figure()
    h = 3.0
    label_z_offset = 1.05
    
    # 12 triangles: two per face of axis-aligned cuboid
    tri_i = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3]
    tri_j = [1, 2, 6, 7, 4, 5, 5, 6, 6, 7, 7, 4]
    tri_k = [2, 3, 5, 6, 5, 1, 6, 2, 7, 3, 4, 0]
    edge_pairs = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    )

    xmin = ymin = float("inf")
    xmax = ymax = float("-inf")

    print("\n" + "="*60)
    print("🏠 AI STRUCTURAL ANALYSIS PIPELINE (Phase 2)")
    print("="*60)

    for idx, room in enumerate(rooms):
        # --- Y INTELLIGENCE INTEGRATION ---
        # 1. Analyze geometry (span, area, load-bearing)
        analysis = analyze_wall(room)
        # 2. Recommend optimal material based on multi-factor analysis
        material_choice = recommend_material(analysis)
        # 3. Generate detailed engineering justification and comparative 'why not' engine
        report = explain(analysis, material_choice)
        
        x = float(room.get("x", 0))
        y = float(room.get("y", 0))
        width = float(room.get("width", 0))
        length = float(room.get("length", 0))

        vx = [x, x + width, x + width, x, x, x + width, x + width, x]
        vy = [y, y, y + length, y + length, y, y, y + length, y + length]
        vz = [0, 0, 0, 0, h, h, h, h]

        # Map Intelligence results to visualization colors
        conf = report["confidence"]
        if conf == "Low":
            mesh_color, mesh_opacity = "rgb(255,50,50)", 0.72 # Red
            risk_line = "⚠️ CRITICAL"
            label_color = "rgb(150,0,0)"
        elif conf == "Medium":
            mesh_color, mesh_opacity = "rgb(255,165,0)", 0.62 # Orange
            risk_line = "🔸 REVIEW"
            label_color = "rgb(120,80,0)"
        else: # High confidence
            mesh_color, mesh_opacity = "rgb(0,200,80)", 0.52 # Green
            risk_line = "✅ SAFE"
            label_color = "rgb(10,80,10)"

        name = room.get("name", f"Room {idx+1}")
        label_text = f"{name}<br>{report['material']}<br>{risk_line}"

        # Add 3D representation
        fig.add_trace(go.Mesh3d(
            x=vx, y=vy, z=vz, i=tri_i, j=tri_j, k=tri_k,
            color=mesh_color, opacity=mesh_opacity, name=name,
            flatshading=True, lighting=dict(ambient=0.5, diffuse=0.8, specular=0.3),
        ))

        # Add wireframe edges
        ex, ey, ez = [], [], []
        for a, b in edge_pairs:
            ex.extend((vx[a], vx[b], None))
            ey.extend((vy[a], vy[b], None))
            ez.extend((vz[a], vz[b], None))
        fig.add_trace(go.Scatter3d(
            x=ex, y=ey, z=ez, mode="lines",
            line=dict(color="rgba(30,30,30,0.75)", width=2),
            showlegend=False, hoverinfo="skip",
        ))

        # Add data-driven labels (Name, Material, Intelligence result)
        cx, cy, cz = x + width/2, y + length/2, h + label_z_offset
        fig.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[cz], mode="text", text=[label_text],
            textposition="top center", textfont=dict(color=label_color, size=12, family="Arial Black"),
            showlegend=False, hoverinfo="skip",
        ))

        # Console Output (Clean structured log for demo)
        print(f"\n[ROOM: {name.upper()}]")
        print(f"  Material   : {report['material']}")
        print(f"  Confidence : {report['confidence']}")
        print(f"  Suggestion : {report['suggestion']}")
        print(f"  Reasoning  : {report['explanation'][:100]}...")
        
        # Track bounds for camera
        xmin = min(xmin, x); xmax = max(xmax, x + width)
        ymin = min(ymin, y); ymax = max(ymax, y + length)

    # Visualization layout settings
    fig.update_layout(
        title="AI-based Structural Intelligence System (Phase 2)",
        scene=dict(
            xaxis=dict(title="Width (X)"),
            yaxis=dict(title="Length (Y)"),
            zaxis=dict(title="Height (Z)"),
            aspectmode="data",
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
    )

    out_html = Path(__file__).resolve().parent / "floorplan_3d.html"
    fig.write_html(str(out_html), include_plotlyjs="cdn", auto_open=False)
    print("\n" + "="*60)
    print(f"✅ Interactive 3D visualization generated: {out_html.name}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Load rooms from external dataset (standardized across modules)
    try:
        from data import rooms as DATA_ROOMS
    except ImportError:
        DATA_ROOMS = [{"name": "Default Room", "x": 0, "y": 0, "width": 5, "length": 5}]

    # --- PHASE 2 CORE FEATURE: GENERATE JSON PIPELINE REPORT ---
    pipeline_results = []
    for r in DATA_ROOMS:
        ana = analyze_wall(r)
        mat = recommend_material(ana)
        pipeline_results.append(explain(ana, mat))
    
    with open("output.json", "w") as f:
        json.dump({
            "rooms": DATA_ROOMS, 
            "structural_analysis": pipeline_results
        }, f, indent=2)
    
    # Run interactive visualization
    render_rooms(DATA_ROOMS)
