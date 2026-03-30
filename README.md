# PlanWise – AI Structural Layout & Material Intelligence

> **Engineering Smarter Structures: Where Computer Vision meets Structural Integrity.**

PlanWise is an end-to-end structural intelligence platform that transforms 2D floor plans into intelligent, material-optimized 3D models. It pairs high-precision structural analysis with AI-driven engineering reasoning to bridge the gap between architectural sketches and construction-ready insights.

---

## 📉 The Problem
Traditional structural planning is often a slow, manual, and disconnected process. Engineers frequently face:
- **Inefficient Workflows**: Manually converting 2D designs to structural models takes hours of redundant work.
- **Lack of Quick Insights**: Estimating material requirements and structural risks early in the design phase is prone to human error.
- **Complexity in Recommendations**: Identifying the optimal material (RCC, Steel, Masonry) for specific spans require deep calculation that isn't instantly available to architects or builders.

## 💡 The Solution
**PlanWise** automates the heavy lifting. By combining a multi-stage AI pipeline with a decentralized trust layer, it provides:
- **Instant 3D Reconstruction**: Automated conversion from image/JSON to interactive 3D plots.
- **Intelligent Material Mapping**: Real-time span calculation and load-bearing logic to suggest the best construction materials.
- **Explainable Engineering**: Every recommendation comes with a professional LLM-generated justification, providing the "why" behind the "what."

---

## ✨ Features
- **📤 Dual-Mode Ingestion**: Upload a standard floor plan (JPG/PNG) or load raw geometric JSON data.
- **🔍 Automated Structural Analysis**: High-precision span detection and load-bearing classification.
- **🧱 Smart Material Engine**: Logic-based material selection (RCC, Steel, Bricks, AAC) tailored to structural needs.
- **💬 Technical Reasoning**: Integration with **Gemma-3** to provide professional engineering justifications for every recommendation.
- **📊 Interactive 3D Visualization**: Full 3D rendering with phase-by-phase autoplay (Layout → Walls → Analysis → Materials).
- **🔗 Blockchain Integrity**: Optional report hashing on the **Stellar Testnet** (Soroban) for immutable project records.
- **🎨 Modern Glassmorphic UI**: High-contrast, premium engineering dashboard with real-time status tracking.

---

## 🛠️ Tech Stack
- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **AI/ML**: Google Gemini (Vision), OpenRouter / Gemma (Reasoning)
- **Visualization**: Plotly.js (3D Mesh Rendering)
- **Blockchain**: Stellar Network (Soroban / Rust WASM)
- **Data Handling**: ND-JSON Streaming

---

## 🏗️ Architecture Overview
`Input (Plan/JSON)` → `Vision Processing (CV/Gemini)` → `Structural Analysis (Pipeline)` → `Material Logic (Engineering Engine)` → `Insight Generation (LLM)` → `3D Visualization (Plotly)`

---

## 📁 Project Structure
- **`server.py`**: The core API entry point handling analysis requests and streaming.
- **`pipeline.py`**: Orchestrates the data flow through vision and structural logic steps.
- **`materials.py`**: Contains the core engineering rules for span calculation and material mapping.
- **`explain.py`**: Dedicated module for generating LLM-powered engineering justifications.
- **`vision_parser.py`**: Handles OpenCV parsing and Gemini Vision fallback.
- **`blockchain.py`**: Manages immutable report hashing on the Stellar ledger.
- **`frontend/`**: Contains the complete glassmorphic web dashboard.

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/mayankj0919/Sanctum-Labs.git
cd Sanctum-Labs
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend
```bash
python server.py
```

### 4. Open the Frontend
Since the frontend is served statically, you can host it using Python's built-in server:
```bash
python -m http.server 8000 --directory frontend
```
Navigate to `http://localhost:8000` in your browser.

---

## 🔮 Future Improvements
- **🤖 Deep Learning Parser**: Trained ML models for even higher accuracy in non-standard blueprint detection.
- **📐 Real CAD Support**: Direct parsing of `.dwg` and `.dxf` vectorized architectural files.
- **☁️ Cloud-Native Deployment**: Scale analysis threads using AWS/Azure serverless functions.
- **🔄 Real-time Collaborative Editing**: Multiple engineers collaborating on a single 3D structural model in real-time.

---

## 👥 Contributors
- **[Your Name/Team Name]** - *Initial Work & Architecture*
- Placeholder for future contributors.

---
*Created for the [Project Name/Hackathon] - 2026*
