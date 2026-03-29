# PLANWISE AI - Project Context for AI

## Project Overview
**PLANWISE AI Structural Intelligence System** - An AI-based system that converts floor plan data into 3D structural models, recommends construction materials, and provides engineering explanations.

---

## Architecture

### Current Pipeline
```
Floor Plan Data → Geometry → Material Logic → Explanation → 3D Visualization
```

### Files Created

| File | Purpose | Status |
|------|---------|--------|
| `data.py` | Room + wall definitions | ✅ Complete |
| `materials.py` | Material recommendation logic | ✅ Complete |
| `explain.py` | Engineering explanation generator | ✅ Complete |
| `app.py` | Main pipeline orchestration | ✅ Complete |
| `model3d.py` / `render_rooms.py` | 3D visualization (Plotly) | ✅ Complete |
| `frontend/index.html` | Dashboard UI | ✅ Complete |
| `frontend/style.css` | Dark theme styling | ✅ Complete |
| `frontend/app.js` | Frontend interactions | ✅ Complete |

---

## What's Working

### Backend (Python)
- Hardcoded room + wall data
- Rule-based material selection:
  - Load-bearing walls → RCC
  - Long spans → Steel
  - Otherwise → Brick
- Explanation system for engineering decisions
- 3D room rendering with Plotly
- JSON input/output pipeline

### Frontend (Vanilla HTML/CSS/JS)
- Dark-themed "Digital Blueprint" aesthetic
- 40/60 split layout
- Drag-and-drop image upload
- Preview area with dot-grid background
- Sample floor plan loader
- Glassmorphism effects
- Analyze button with loading state (mocked)

---

## What's NOT Done / Future Work

1. **Floor Plan Parsing** - Currently uses hardcoded data. Need OpenCV/image recognition to extract rooms/walls from uploaded images

2. **Frontend-Backend Integration** - Frontend is standalone. Need to connect to Python pipeline via Flask or FastAPI

3. **Material Logic** - Currently basic rules. Could be improved with:
   - Cost optimization
   - Structural validation
   - Regional code compliance

4. **Real-time Interaction** - 3D view is static. Could add:
   - Room selection
   - Material override
   - Export options

5. **Testing** - No unit tests exist

6. **Production Polish** - Error handling, loading states, edge cases

---

## Quick Start

### Run Backend
```bash
python app.py
```

### View 3D Output
Open `floorplan_3d.html` in browser

### View Frontend
Open `frontend/index.html` in browser

---

## Tech Stack
- **Backend**: Python
- **Visualization**: Plotly
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **UI**: Custom dark theme (no framework)

---

## Project Structure
```
PlanWise-1/
├── data.py           # Room/wall definitions
├── materials.py      # Material logic
├── explain.py        # Explanation generator
├── app.py            # Main pipeline
├── render_rooms.py   # 3D rendering
├── floorplan_3d.html # 3D output
├── frontend/
│   ├── index.html    # Main UI
│   ├── style.css     # Styling
│   └── app.js        # Interactions
└── AI_CONTEXT.md     # This file
```
