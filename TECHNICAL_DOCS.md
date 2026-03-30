# 🌐 SANCTUM AI — Complete Technical & Conceptual Documentation

> **"Bridging the Gap Between 2D Sketches and Structural Reality with AI & Blockchain."**

---

## 1. PROJECT OVERVIEW
### What is SANCTUM AI?
SANCTUM AI is an end-to-end Structural Intelligence System. It isn't just a 3D visualizer; it is a decision-support engine that takes raw floor plans (images or JSON) and automatically determines the structural "skeleton" of a building. It identifies load-bearing elements, recommends specific construction materials, and generates professional engineering justifications for those choices.

### Why does it exist?
In the early stages of design, architects and builders often lack immediate structural feedback. Traditional structural consultation is expensive and slow. SANCTUM AI provides **instant, data-driven structural "pre-checks"** to help teams make informed decisions before a single brick is laid.

### Real-world relevance
By automating the initial structural assessment, we reduce the manual CAD-to-Analysis workflow from hours to seconds. It acts as a digital technical partner, ensuring that early-stage designs are grounded in structural reality.

---

## 2. SYSTEM ARCHITECTURE
The system operates as a linear, modular pipeline where each step enriches the data before passing it to the next.

**The Pipeline Flow:**
`Input (Plan/JSON)` → `Vision Processor (OpenCV/Gemini)` → `Geometry Extraction` → `Structural Analysis (Spans & Loads)` → `Material Logic` → `Engineering Explanation (LLM)` → `Blockchain Commitment (Stellar)` → `3D UI Rendering`

---

## 3. MODULE BREAKDOWN
Each file in SANCTUM AI has a specific, isolated responsibility:

*   **`server.py`**: The API Gateway. It serves the Flask endpoints, handles the ND-JSON streaming for the dashboard, and manages the non-blocking response flow.
*   **`pipeline.py`**: The Orchestrator. It coordinates the movement of data between the vision, engineering, and explanation modules.
*   **`vision_parser.py`**: The "Eyes" of the system. It uses OpenCV for high-speed geometric detection and features a **Gemini 1.5 Flash fallback** to interpret messy or complex hand-drawn plans.
*   **`materials.py`**: The "Structural Brain." It contains the hardcoded engineering logic for calculating spans, identifying load-bearing walls, and selecting materials.
*   **`explain.py`**: The "Technical Consultant." It connects to **Google Gemma-3** to generate human-readable, professional justifications for every structural recommendation.
*   **`blockchain.py`**: The "Notary." It handles the asynchronous process of hashing the final report and storing it on the Stellar Testnet via Soroban smart contracts.
*   **`frontend/`**: The "Command Center."
    *   `app.js`: Manages the 3D rendering (Plotly), auto-verification timers, and report downloads.
    *   `style.css`: A premium glassmorphic interface designed for clarity and a professional feel.
    *   `index.html`: The structural skeleton of the dashboard.

---

## 4. DATA FLOW: STEP-BY-STEP
1.  **Ingestion**: User uploads an image. 
2.  **Vision**: OpenCV detects wall lines and room boundaries.
3.  **Geometry**: Coordinates are normalized into a standard "Room/Wall" object list.
4.  **Rules**: `materials.py` checks wall lengths. If a span is >4.5m, it's flagged as load-bearing.
5.  **Assignment**: The system assigns RCC for load-bearing, Steel for long spans, and Bricks for partitions.
6.  **Reasoning**: Gemma-3 reads the context and writes: *"RCC chosen for Wall W1 to ensure vertical stability over a 5m span."*
7.  **Hashing**: A unique SHA-256 hash of the final JSON report is generated.
8.  **Commitment**: The hash is sent to the Stellar ledger (async thread to prevent UI lag).
9.  **Delivery**: The UI renders the 3D model phase-by-phase (Layout → Final).
10. **Verification**: 3 seconds later, the UI calls `/verify` to confirm the hash is permanently on the ledger.

---

## 5. MATERIAL LOGIC (ENGINEERING CORE)
We don't guess; we apply engineering heuristics:
*   **Spans & Loads**: Central walls or walls supporting long spans are automatically classified as **Load-Bearing**.
*   **Material Selection**:
    *   **RCC (Reinforced Concrete)**: Used for primary structural support (high compressive strength).
    *   **Steel**: Recommended for exceptionally long spans to handle tensile stress without bulky columns.
    *   **AAC Blocks / Bricks**: Used for internal partitions where weight reduction is prioritized over load-carrying.

---

## 6. EXPLAINABLE AI
Unlike "black-box" models that just give you a result, SANCTUM AI provides a **Traceable Narrative**.
*   **Why it matters**: In construction, a mistake can be fatal. Engineers need to know *why* a system suggested Steel over RCC.
*   **Mechanism**: We feed the structural context (span, room type, score) into the LLM, which then references engineering principles to justify the choice.

---

## 7. BLOCKCHAIN INTEGRATION: THE TRUST LAYER
### Why use a Blockchain?
Construction reports are often prone to "version drift" or tampering. By storing a **SHA-256 Hash** of the report on the **Stellar Testnet**, we create an immutable timestamp.

### What is stored?
We **do not** store the full data on-chain (it's too expensive and slow). We store:
1.  `Project ID`
2.  `Report Hash`

### Verification Flow
The `/verify/<project_id>` endpoint invokes the Stellar CLI to pull the hash from the smart contract. If it matches your local copy, the system is "Verified."

---

## 8. DESIGN DECISIONS: THE "WHYS"
*   **Rule-Based vs. ML**: We chose rule-based structural logic because it is **deterministic**. In engineering, 2+2 must always be 4. ML can be "hallucinatory" when it comes to load calculations.
*   **Async Blockchain**: We run blockchain tasks in a background thread. This ensures the user sees their 3D model instantly (low latency) while the ledger works in the background.
*   **NDJSON Streaming**: We stream the analysis results chunk-by-chunk. High perceived performance—the user sees the layout rendering while the AI is still "thinking" about materials.

---

## 9. PERFORMANCE & STABILITY
*   **Fault Tolerance**: All CLI calls (Stellar) are wrapped in sanitization blocks to handle non-ASCII characters and empty outputs gracefully.
*   **Concurrency**: Uses Python's `threading` for blockchain tasks, ensuring the Flask server never hangs during network congestion.

---

## 10. LIMITATIONS
*   **Vision Sensitivity**: Highly "noisy" blueprints with lots of text/furniture can sometimes confuse the OpenCV parser (though Gemini fallback helps).
*   **Simplification**: This is a structural *intelligence* system for early-stage planning, not a substitute for a full Finite Element Analysis (FEA).

---

## 11. FUTURE SCOPE
*   **Real-time CAD Sync**: Bi-directional sync with AutoCAD/Revit.
*   **Cost Estimation**: Integrating live market prices for RCC vs. Steel.
*   **BIM Integration**: Exporting analysis directly into 3D BIM formats.

---

## 12. DEMO FLOW
1.  **Upload**: Drag a floor plan onto the glassmorphic dropzone.
2.  **Analyze**: Watch the status bar change as the pipeline extracts geometry.
3.  **Inspect**: Once the 3D model appears, click "Autoplay" to see the construction phases.
4.  **Verify**: Point to the "Blockchain Verification" panel. It will transition from "Pending" to "Verified" automatically.
5.  **Export**: Click the download button to get a professional TXT summary.

---

## 13. JUDGE Q&A (THE CHEAT SHEET)

**Q: Why use a blockchain for this?**
*A: It's about data integrity. In multi-stakeholder projects (Architect, Builder, Client), having a "source of truth" hash on Stellar ensures that the report analyzed on Day 1 is the same report used on Day 30.*

**Q: Why not just use a Database?**
*A: Databases are mutable. An admin can change a record. A decentralized ledger like Stellar provides third-party trust that is mathematically guaranteed to be tamper-proof.*

**Q: Is the material logic accurate?**
*A: It follows standard civil engineering heuristics for span-to-depth ratios and load distribution, making it an excellent "first-pass" analysis tool.*

**Q: Why use LLMs for explanations?**
*A: A raw risk score of "85" doesn't help a human as much as a sentence saying "This 6m span creates excessive deflection, requiring RCC reinforcement."*

---
*Documentation State: Final Submission Ready - merge-visuals branch*
