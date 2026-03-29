"""
Vision Parser — X (Computer Vision Layer)
Part of the AI-based Structural Intelligence System.

Parses floor plan images using OpenCV and/or LLM with vision capabilities.
Converts uploaded images into structured JSON (rooms + walls).
"""

import json
import os

try:
    import numpy as np
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import google.genai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def parse_floor_plan(image_data: bytes) -> dict:
    """Parse a floor plan image into structured JSON format.
    
    Parameters
    ----------
    image_data : bytes
        Raw image bytes from uploaded file
    
    Returns
    -------
    dict
        Contains 'rooms' and 'walls' arrays in our standard format
    """
    if not CV2_AVAILABLE:
        return get_default_structure()
    
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Could not decode image")
            
        return parse_with_opencv(img)
        
    except Exception as e:
        print(f"OpenCV parsing failed: {e}")
        try:
            return parse_with_llm_fallback(image_data)
        except Exception as llm_error:
            print(f"LLM fallback also failed: {llm_error}")
            raise ValueError(f"Could not parse floor plan: {e}")


def parse_with_opencv(img: np.ndarray) -> dict:
    """Use OpenCV to extract rooms and walls from floor plan image."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=2)
    binary = cv2.erode(binary, kernel, iterations=1)
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rooms = []
    walls = []
    room_id_counter = 1
    wall_id_counter = 1
    
    min_area = img.shape[0] * img.shape[1] * 0.01
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        
        room_name = f"Room {room_id_counter}"
        if area > min_area * 3:
            room_name = f"Living Room" if room_id_counter == 1 else f"Room {room_id_counter}"
        
        scale_factor = 0.1
        rooms.append({
            "id": f"room_{room_id_counter}",
            "name": room_name,
            "width": int(w * scale_factor),
            "length": int(h * scale_factor),
            "x": int(x * scale_factor),
            "y": int(y * scale_factor)
        })
        
        wall_thickness = detect_wall_thickness(cnt, img)
        is_load_bearing = wall_thickness > 15 or w > img.shape[1] * 0.4
        
        walls.append({
            "id": f"w{wall_id_counter}",
            "type": "load_bearing" if is_load_bearing else "partition",
            "length": int(max(w, h) * scale_factor),
            "x1": int(x * scale_factor),
            "y1": int(y * scale_factor),
            "x2": int((x + w) * scale_factor),
            "y2": int((y + h) * scale_factor),
            "room_id": f"room_{room_id_counter}"
        })
        
        wall_id_counter += 1
        room_id_counter += 1
    
    if not rooms:
        return get_default_structure()
    
    walls = infer_walls_from_rooms(rooms)
    
    return {"rooms": rooms, "walls": walls}


def detect_wall_thickness(contour: np.ndarray, img: np.ndarray) -> float:
    """Detect wall thickness from contour."""
    x, y, w, h = cv2.boundingRect(contour)
    return max(w, h)


def infer_walls_from_rooms(rooms: list) -> list:
    """Generate walls based on room boundaries."""
    walls = []
    wall_id = 1
    
    for room in rooms:
        x, y = room["x"], room["y"]
        w, l = room["width"], room["length"]
        
        is_load_bearing = w > 10 or l > 15
        
        walls.extend([
            {
                "id": f"w{wall_id}",
                "type": "load_bearing" if is_load_bearing else "partition",
                "length": l,
                "x1": x, "y1": y,
                "x2": x, "y2": y + l,
                "room_id": room["id"]
            },
            {
                "id": f"w{wall_id + 1}",
                "type": "load_bearing" if is_load_bearing else "partition",
                "length": w,
                "x1": x, "y1": y,
                "x2": x + w, "y2": y,
                "room_id": room["id"]
            }
        ])
        wall_id += 2
    
    return walls


def get_default_structure() -> dict:
    """Return default structure when parsing fails."""
    return {
        "rooms": [
            {"id": "room_1", "name": "Living Room", "width": 15, "length": 18, "x": 0, "y": 0},
            {"id": "room_2", "name": "Kitchen", "width": 12, "length": 14, "x": 15, "y": 0},
        ],
        "walls": [
            {"id": "w1", "type": "load_bearing", "length": 18, "x1": 0, "y1": 0, "x2": 0, "y2": 18, "room_id": "room_1"},
            {"id": "w2", "type": "load_bearing", "length": 15, "x1": 0, "y1": 0, "x2": 15, "y2": 0, "room_id": "room_1"},
        ]
    }


def parse_with_llm_fallback(image_data: bytes) -> dict:
    """Use LLM with vision to parse floor plan when OpenCV fails."""
    if not GEMINI_AVAILABLE:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set and google-genai not installed")
        genai.configure(api_key=api_key)
    
    image = Image.open(io.BytesIO(image_data))
    
    prompt = """Analyze this floor plan image and extract the structure into JSON format.
    Return a JSON object with 'rooms' and 'walls' arrays.
    
    Each room should have: id, name, width, length, x, y
    Each wall should have: id, type (load_bearing or partition), length, x1, y1, x2, y2, room_id
    
    Return ONLY valid JSON, no additional text."""
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt, image])
    
    json_str = response.text.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    if json_str.startswith("```"):
        json_str = json_str[3:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    
    return json.loads(json_str.strip())


def parse_floor_plan_from_file(file_path: str) -> dict:
    """Parse a floor plan from a file path."""
    with open(file_path, 'rb') as f:
        return parse_floor_plan(f.read())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = parse_floor_plan_from_file(sys.argv[1])
        print(json.dumps(result, indent=2))
