"""
Vision Parser — Clean Stable Version (Hackathon Ready)

- Uses OpenCV only (fast & reliable)
- Extracts rooms using contours
- Generates consistent rooms + walls
- Normalized scaling (no crazy 50m rooms)
"""

import os
import io
import json
import numpy as np
import cv2
from PIL import Image

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import google.genai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# -------------------------------
# MAIN ENTRY
# -------------------------------
def is_valid_result(result):
    rooms = result.get("rooms", [])

    # Must detect enough rooms
    if len(rooms) < 3:
        return False

    # Reject unrealistic scaling
    for r in rooms:
        if r["width"] > 20 or r["length"] > 20:
            return False
        if r["width"] < 2 or r["length"] < 2:
            return False

    return True

def parse_floor_plan(image_data: bytes) -> dict:
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return get_default_structure()

    # Step 1: OpenCV
    opencv_result = parse_with_opencv(img)

    # Step 2: Validate
    if is_valid_result(opencv_result):
        print("Using OpenCV result")
        return opencv_result

    print("OpenCV weak -> switching to Gemini")

    # Step 3: Gemini fallback
    if GEMINI_AVAILABLE and os.environ.get("GEMINI_API_KEY"):
        try:
            return parse_with_llm_fallback(image_data)
        except Exception as e:
            print("Gemini failed:", e)

    # Step 4: fallback
    return opencv_result if opencv_result else get_default_structure()


# -------------------------------
# CORE LOGIC
# -------------------------------
def parse_with_opencv(img: np.ndarray) -> dict:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold (walls = white)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Close gaps (doors/windows)
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(
        closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    img_h, img_w = img.shape[:2]
    img_area = img_h * img_w

    rooms = []

    # Normalize scale -> max ~20 meters
    scale_factor = 20 / max(img_w, img_h)

    # Ignore largest contour (outer boundary)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(contours) > 0:
        contours = contours[1:]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Scale to real-world units (meters)
        width = round(w * scale_factor, 1)
        length = round(h * scale_factor, 1)
        area = width * length
        aspect_ratio = max(width, length) / max(min(width, length), 0.001)

        # 5. DEBUG MODE
        print(f"Detected contour: area={area:.2f}, aspect={aspect_ratio:.2f}, dimensions={width}x{length}")

        # 1. MIN AREA FILTER
        if area < 4:
            print("  -> Skipped: area < 4 (tiny shape)")
            continue
            
        # 2. ASPECT RATIO CHECK
        if aspect_ratio > 4:
            print("  -> Skipped: aspect > 4 (likely window/door)")
            continue
            
        # 3. WALL THICKNESS FILTER
        if min(width, length) < 1.5:
            print("  -> Skipped: thickness < 1.5 (structural element)")
            continue

        rooms.append({
            "width": width,
            "length": length,
            "x": round(x * scale_factor, 1),
            "y": round(y * scale_factor, 1)
        })

    # Sort rooms for consistency
    rooms.sort(key=lambda r: (r["y"], r["x"]))

    # Assign IDs and names after sorting
    for idx, r in enumerate(rooms, 1):
        r["id"] = f"room_{idx}"
        r["name"] = classify_room(r["width"], r["length"], idx)

    print(f"Detected {len(rooms)} rooms using OpenCV")

    if not rooms:
        return get_default_structure()

    walls = infer_walls_from_rooms(rooms)

    return {"rooms": rooms, "walls": walls}


# -------------------------------
# ROOM CLASSIFICATION (SIMPLE)
# -------------------------------
def classify_room(width, length, idx):
    area = width * length

    # 4. Improve ROOM CLASSIFICATION
    if area > 30:
        return f"Living Room {idx}"
    elif 12 < area <= 30:
        return f"Bedroom {idx}"
    elif 6 < area <= 12:
        return f"Kitchen {idx}"
    elif 3 < area <= 6:
        return f"Bathroom {idx}"
    else:
        return f"Utility/Storage {idx}"


# -------------------------------
# WALL GENERATION (CLEAN)
# -------------------------------
def infer_walls_from_rooms(rooms):
    walls = []
    wall_id = 1

    for room in rooms:
        x, y = room["x"], room["y"]
        w, l = room["width"], room["length"]

        # simple structural rule
        is_load_bearing = max(w, l) > 5
        wall_type = "load_bearing" if is_load_bearing else "partition"

        walls.extend([
            {"id": f"w{wall_id}", "type": wall_type, "length": w, "x1": x, "y1": y, "x2": x + w, "y2": y, "room_id": room["id"]},
            {"id": f"w{wall_id+1}", "type": wall_type, "length": w, "x1": x, "y1": y + l, "x2": x + w, "y2": y + l, "room_id": room["id"]},
            {"id": f"w{wall_id+2}", "type": wall_type, "length": l, "x1": x, "y1": y, "x2": x, "y2": y + l, "room_id": room["id"]},
            {"id": f"w{wall_id+3}", "type": wall_type, "length": l, "x1": x + w, "y1": y, "x2": x + w, "y2": y + l, "room_id": room["id"]}
        ])

        wall_id += 4

    return walls


# -------------------------------
# FALLBACK
# -------------------------------
def parse_with_llm_fallback(image_data: bytes) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    
    client = genai.Client(api_key=api_key)
    image = Image.open(io.BytesIO(image_data))
    
    prompt = """Analyze this floor plan and extract ALL rooms.

Requirements:
- Detect ALL visible rooms (at least 4 if present)
- Each room must have realistic dimensions (2m-10m)
- Maintain correct spatial layout
- Output JSON ONLY

Format:
{
  "rooms": [
    {"id": "...", "name": "...", "width": ..., "length": ..., "x": ..., "y": ...}
  ]
}
"""
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[prompt, image]
    )
    
    json_str = response.text.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    if json_str.startswith("```"):
        json_str = json_str[3:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    
    data = json.loads(json_str.strip())
    if "walls" not in data:
        data["walls"] = infer_walls_from_rooms(data["rooms"])
        
    return data

def get_default_structure():
    rooms = [
        {"id": "room_1", "name": "Living Room", "width": 10, "length": 12, "x": 0, "y": 0},
        {"id": "room_2", "name": "Bedroom", "width": 8, "length": 10, "x": 10, "y": 0},
    ]
    return {
        "rooms": rooms,
        "walls": infer_walls_from_rooms(rooms)
    }


# -------------------------------
# CLI TEST
# -------------------------------
def parse_floor_plan_from_file(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        return parse_floor_plan(f.read())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = parse_floor_plan_from_file(sys.argv[1])
        print(json.dumps(result, indent=2))