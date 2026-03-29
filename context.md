🧠 Project Overview
We are building an AI-based Structural Intelligence System that:

Takes floor plan data (currently hardcoded)

Converts it into structured geometry (rooms + walls)

Generates a 3D model of the structure

Recommends construction materials

Provides clear engineering explanations for decisions

🏗️ Current Architecture
🔁 Pipeline
Floor Plan Data → Geometry → Material Logic → Explanation → 3D Visualization
👥 Team Structure
🎨 B (Frontend / Visualization)
Responsible for 3D rendering using Plotly

Displays rooms in 3D space

Handles demo and presentation

👨‍💻 A (Backend) split into:
🔵 X (Structure + Pipeline)
Creates data.py (rooms + walls)

Builds app.py (main pipeline)

Structures output for frontend

🟣 Y (Logic + Intelligence)
Builds materials.py (material recommendation)

Builds explain.py (engineering reasoning)

Improves decision logic

📁 Project Structure
project/
│
├── data.py          # room + wall definitions
├── materials.py     # material selection logic
├── explain.py       # explanation generator
├── app.py           # main pipeline
├── model3d.py       # 3D visualization (frontend)
⚙️ Current Implementation Status
✅ Backend
Hardcoded room + wall data

Rule-based material recommendation:

load_bearing → RCC

long span → Steel

otherwise → Brick

Explanation system working

✅ Frontend
Plotly 3D rendering working

Can display one or more rooms

Labels added (room names)

🔄 Data Flow Between Backend & Frontend
Backend outputs:

{
  "rooms": [...],
  "walls": [...],
  "results": [
    {
      "wall": {...},
      "material": "...",
      "explanation": "..."
    }
  ]
}
Frontend uses:

rooms → for 3D rendering

🎯 Key Features
End-to-end working pipeline (even if simplified)

Explainable AI decisions (important for judging)

Modular architecture (easy to extend)

🚧 Future Improvements (Planned)
OpenCV-based floor plan parsing

Better structural validation

Cost optimization

Real-time interaction

⚠️ Constraints
Time limit: 5 hours initial prototype

Focus: working system > perfect system

Avoid heavy ML or complex setups

🧠 Core Idea
“Build a system that not only recommends materials but also explains why, like a real engineer.”

🎤 Demo Narrative
“We convert floor plan data into a 3D structure, analyze wall properties, recommend materials based on engineering rules, and explain each decision clearly.”

