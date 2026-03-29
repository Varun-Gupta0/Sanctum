import webbrowser
from pathlib import Path

import plotly.graph_objects as go


def get_material(room):
    width = room.get("width", 0)
    length = room.get("length", 0)
    primary = "RCC" if width > 5 or length > 5 else "Brick"
    secondary = "Steel Frame"
    return {"primary": primary, "secondary": secondary}


def get_risk(room):
    span = max(room.get("width", 0), room.get("length", 0))
    if span > 5:
        return "⚠️ Large span - structural support required"
    return "✅ Structurally safe"


def get_explanation(room, material):
    width = room.get("width", 0)
    length = room.get("length", 0)
    span = max(width, length)
    room_name = room.get("name", "Room")
    if material["primary"] == "RCC":
        return (
            f"{room_name} spans {span:.1f}m, which is above safe limits for brick in this geometry. "
            "RCC is recommended for strength and durability in longer spans, while Steel Frame stays "
            "as an alternative for future refinement."
        )
    return (
        f"{room_name} has a compact span of {span:.1f}m, where Brick is efficient and cost-effective. "
        "Steel Frame is listed as a solid alternative in case of architectural changes or higher loads."
    )


def render_rooms(rooms):
    fig = go.Figure()
    h = 3.0
    label_z_offset = 1.05
    # 12 triangles: two per face of axis-aligned cuboid
    tri_i = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3]
    tri_j = [1, 2, 6, 7, 4, 5, 5, 6, 6, 7, 7, 4]
    tri_k = [2, 3, 5, 6, 5, 1, 6, 2, 7, 3, 4, 0]
    edge_pairs = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    )

    xmin = ymin = float("inf")
    xmax = ymax = float("-inf")

    for idx, room in enumerate(rooms):
        x = float(room.get("x", 0))
        y = float(room.get("y", 0))
        width = float(room.get("width", 0))
        length = float(room.get("length", 0))

        vx = [x, x + width, x + width, x, x, x + width, x + width, x]
        vy = [y, y, y + length, y + length, y, y, y + length, y + length]
        vz = [0, 0, 0, 0, h, h, h, h]

        material = get_material(room)
        risk = get_risk(room)
        explanation = get_explanation(room, material)

        if "⚠️" in risk:
            mesh_color = "rgb(255,0,0)"
            mesh_opacity = 0.72
            risk_line = "⚠️ At risk"
            label_color = "rgb(90,0,0)"
        elif "✅" in risk:
            mesh_color = "rgb(0,200,0)"
            mesh_opacity = 0.52
            risk_line = "✅ Safe"
            label_color = "rgb(15,55,15)"
        else:
            mesh_color = "rgb(128,128,128)"
            mesh_opacity = 0.58
            risk_line = risk
            label_color = "rgb(20,20,20)"

        name = room.get("name", f"Room {idx+1}")
        label_text = f"{name}<br>{material['primary']}<br>{risk_line}"

        fig.add_trace(
            go.Mesh3d(
                x=vx,
                y=vy,
                z=vz,
                i=tri_i,
                j=tri_j,
                k=tri_k,
                color=mesh_color,
                opacity=mesh_opacity,
                name=name,
                flatshading=True,
                lighting=dict(ambient=0.5, diffuse=0.8, specular=0.3),
            )
        )

        ex, ey, ez = [], [], []
        for a, b in edge_pairs:
            ex.extend((vx[a], vx[b], None))
            ey.extend((vy[a], vy[b], None))
            ez.extend((vz[a], vz[b], None))
        fig.add_trace(
            go.Scatter3d(
                x=ex,
                y=ey,
                z=ez,
                mode="lines",
                line=dict(color="rgba(30,30,30,0.75)", width=2),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        cx = x + width / 2
        cy = y + length / 2
        cz = h + label_z_offset
        fig.add_trace(
            go.Scatter3d(
                x=[cx],
                y=[cy],
                z=[cz],
                mode="text",
                text=[label_text],
                textposition="top center",
                textfont=dict(color=label_color, size=12),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        print(f"Room: {room.get('name', 'Unnamed')}")
        print(f"  Material: {material['primary']} (Primary), {material['secondary']} (Alternative)")
        print(f"  Risk: {risk}")
        print(f"  Explanation: {explanation}")
        print("-" * 60)

        xmin = min(xmin, x)
        xmax = max(xmax, x + width)
        ymin = min(ymin, y)
        ymax = max(ymax, y + length)

    if rooms:
        cx = (xmin + xmax) / 2
        cy = (ymin + ymax) / 2
        cz = h / 2
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=cx, y=cy, z=cz),
            eye=dict(x=cx + 2.2, y=cy + 2.2, z=cz + 1.2),
        )
    else:
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=2.2, y=2.2, z=1.2),
        )

    fig.update_layout(
        title="AI Structural Layout & Risk Analysis",
        scene=dict(
            xaxis=dict(
                title="X",
                backgroundcolor="rgba(255,255,255,0.35)",
                gridcolor="rgba(0,0,0,0.12)",
                showgrid=True,
                zeroline=False,
                range=[-1, 10],
            ),
            yaxis=dict(
                title="Y",
                backgroundcolor="rgba(255,255,255,0.35)",
                gridcolor="rgba(0,0,0,0.12)",
                showgrid=True,
                zeroline=False,
                range=[-1, 10],
            ),
            zaxis=dict(
                title="Z",
                backgroundcolor="rgba(255,255,255,0.35)",
                gridcolor="rgba(0,0,0,0.12)",
                showgrid=True,
                zeroline=False,
                range=[0, 5],
            ),
            aspectmode="cube",
            camera=camera,
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
    )

    out_html = Path(__file__).resolve().parent / "floorplan_3d.html"
    fig.write_html(str(out_html), include_plotlyjs="cdn", auto_open=False)
    webbrowser.open(out_html.as_uri())
    print(f"Interactive plot: {out_html}")


if __name__ == "__main__":
    rooms = [
        {"name": "Bedroom", "x": 0, "y": 0, "width": 4, "length": 4},
        {"name": "Hall", "x": 4, "y": 0, "width": 5, "length": 4},
        {"name": "Kitchen", "x": 0, "y": 4, "width": 4, "length": 3},
        {"name": "Bathroom", "x": 4, "y": 4, "width": 4, "length": 3},
    ]


    render_rooms(rooms)

