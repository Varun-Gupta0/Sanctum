"""
3D floor-plan room visualization with Plotly (Mesh3d cuboids, edges, labels).
"""

from __future__ import annotations

import colorsys
import math

import plotly.graph_objects as go
import plotly.io as pio

# Prefer browser so fig.show() works outside notebooks
pio.renderers.default = "browser"

ROOM_HEIGHT = 3.0
MESH_OPACITY = 0.62
LABEL_CLEARANCE = 0.65  # z above roof so text clears geometry

# Two triangles per face, 12 triangles total
_CUBOID_TRIS = (
    (0, 1, 2),
    (0, 2, 3),
    (4, 6, 5),
    (4, 7, 6),
    (0, 4, 5),
    (0, 5, 1),
    (1, 5, 6),
    (1, 6, 2),
    (2, 6, 7),
    (2, 7, 3),
    (3, 7, 4),
    (3, 4, 0),
)

_CUBOID_I = [t[0] for t in _CUBOID_TRIS]
_CUBOID_J = [t[1] for t in _CUBOID_TRIS]
_CUBOID_K = [t[2] for t in _CUBOID_TRIS]

_EDGES = (
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


def cuboid_vertices(
    x: float, y: float, width: float, length: float, height: float
) -> tuple[list[float], list[float], list[float]]:
    """Return Mesh3d-style vertex coordinates for an axis-aligned cuboid on the z=0 plane."""
    w, l, h = width, length, height
    return (
        [x, x + w, x + w, x, x, x + w, x + w, x],
        [y, y, y + l, y + l, y, y, y + l, y + l],
        [0.0, 0.0, 0.0, 0.0, h, h, h, h],
    )


def _room_color(index: int, total: int) -> str:
    """Distinct, evenly spaced hues (golden ratio step avoids clustering)."""
    if total <= 0:
        total = 1
    h = ((index * 0.618033988749895) + 0.07) % 1.0
    s = 0.62 + 0.08 * math.sin(index * 2.17)
    v = 0.88
    r, g, b = colorsys.hsv_to_rgb(h, min(0.75, max(0.45, s)), v)
    return f"rgb({int(r * 255)},{int(g * 255)},{int(b * 255)})"


def _edge_line_coords(
    x: float, y: float, w: float, length: float, h: float
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    vx, vy, vz = cuboid_vertices(x, y, w, length, h)
    xs: list[float | None] = []
    ys: list[float | None] = []
    zs: list[float | None] = []
    for a, b in _EDGES:
        xs.extend((vx[a], vx[b], None))
        ys.extend((vy[a], vy[b], None))
        zs.extend((vz[a], vz[b], None))
    return xs, ys, zs


def _validate_room(room: dict, index: int) -> None:
    required = ("name", "x", "y", "width", "length")
    for key in required:
        if key not in room:
            raise ValueError(f"room[{index}]: missing key {key!r}")
    try:
        float(room["x"])
        float(room["y"])
        w = float(room["width"])
        length = float(room["length"])
    except (TypeError, ValueError) as e:
        raise ValueError(f"room[{index}]: x, y, width, length must be numbers") from e
    if not (w > 0 and length > 0):
        raise ValueError(f"room[{index}]: width and length must be positive")


def _parse_room(room: dict, index: int) -> tuple[str, float, float, float, float]:
    _validate_room(room, index)
    return (
        str(room["name"]),
        float(room["x"]),
        float(room["y"]),
        float(room["width"]),
        float(room["length"]),
    )


def render_rooms(rooms: list) -> None:
    fig = go.Figure()

    if not rooms:
        fig.update_layout(
            title=dict(text="3D Structural Layout", x=0.5, xanchor="center"),
            scene=dict(
                aspectmode="cube",
                xaxis=dict(title="X", showgrid=True, zeroline=False),
                yaxis=dict(title="Y", showgrid=True, zeroline=False),
                zaxis=dict(title="Z", showgrid=True, zeroline=False),
                camera=dict(eye=dict(x=1.4, y=1.4, z=0.9)),
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            annotations=[
                dict(
                    text="No rooms to display",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=14, color="#666"),
                )
            ],
        )
        fig.show()
        return

    n = len(rooms)
    lx, ly, lz, labels = [], [], [], []
    xmin = ymin = float("inf")
    xmax = ymax = float("-inf")

    for idx, raw in enumerate(rooms):
        name, x, y, w, length = _parse_room(raw, idx)
        color = _room_color(idx, n)
        vx, vy, vz = cuboid_vertices(x, y, w, length, ROOM_HEIGHT)

        fig.add_trace(
            go.Mesh3d(
                x=vx,
                y=vy,
                z=vz,
                i=_CUBOID_I,
                j=_CUBOID_J,
                k=_CUBOID_K,
                name=name,
                color=color,
                flatshading=True,
                opacity=MESH_OPACITY,
                lighting=dict(ambient=0.45, diffuse=0.85, specular=0.35),
                showlegend=True,
            )
        )

        ex, ey, ez = _edge_line_coords(x, y, w, length, ROOM_HEIGHT)
        fig.add_trace(
            go.Scatter3d(
                x=ex,
                y=ey,
                z=ez,
                mode="lines",
                line=dict(color="rgba(20,20,24,0.75)", width=2.5),
                showlegend=False,
                hoverinfo="skip",
                name=f"{name} (edges)",
            )
        )

        lx.append(x + w / 2)
        ly.append(y + length / 2)
        lz.append(ROOM_HEIGHT + LABEL_CLEARANCE)
        labels.append(name)

        xmin = min(xmin, x)
        xmax = max(xmax, x + w)
        ymin = min(ymin, y)
        ymax = max(ymax, y + length)

    fig.add_trace(
        go.Scatter3d(
            x=lx,
            y=ly,
            z=lz,
            mode="text",
            text=labels,
            textposition="top center",
            textfont=dict(size=14, color="rgb(25,25,28)", family="Arial Black, Arial, sans-serif"),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    cz = ROOM_HEIGHT / 2
    span_xy = max(xmax - xmin, ymax - ymin, 1e-6)
    span = max(span_xy, ROOM_HEIGHT)
    d = span * 1.35

    fig.update_layout(
        title=dict(text="3D Structural Layout", x=0.5, xanchor="center"),
        scene=dict(
            aspectmode="data",
            xaxis=dict(title="X", showgrid=True, zeroline=False),
            yaxis=dict(title="Y", showgrid=True, zeroline=False),
            zaxis=dict(title="Z", showgrid=True, zeroline=False),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=cx, y=cy, z=cz),
                eye=dict(x=cx + d, y=cy - d * 0.85, z=cz + d * 0.75),
            ),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor="rgba(255,255,255,0.7)"),
    )

    fig.show()


if __name__ == "__main__":
    demo = [
        {"name": "Bedroom", "x": 0, "y": 0, "width": 4, "length": 3},
        {"name": "Hall", "x": 4, "y": 0, "width": 5, "length": 4},
    ]
    render_rooms(demo)
