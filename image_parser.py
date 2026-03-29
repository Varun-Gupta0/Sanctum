"""
Image Mode Parser — Structural Intelligence System
Extracts room boundaries from a floor plan image using OpenCV heuristics.
"""

import cv2
import numpy as np

def extract_rooms_from_image(image_path: str, scale_factor: float = 0.05) -> dict:
    """
    Extract rooms and rough walls from a floor plan image using contour heuristics.
    
    Parameters
    ----------
    image_path : str
        Path to the floor plan image
    scale_factor : float
        Meters per pixel (approximate) to convert pixel dimensions to real-world units
        
    Returns
    -------
    dict
        Dictionary containing extracted "rooms" and "walls" matching data.py format
    """
    # 1. Read image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # 2. Preprocess: Threshold to get dark walls on white background 
    # (Assuming standard floorplan where walls are black lines on white paper)
    # Invert so walls are white (255) and background is black (0)
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    # 3. Morphological operations to close gaps in walls (doors/windows)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

    # 4. Find the rooms based on the enclosed black spaces
    # Invert back to make the empty rooms white (255) and walls black (0)
    rooms_mask = cv2.bitwise_not(closing)
    
    # 5. Extract contours of the white regions (the rooms)
    contours, _ = cv2.findContours(rooms_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rooms = []
    walls = []
    
    # Heuristics for filtering contours
    min_area = 500  # ignore noise
    img_area = img.shape[0] * img.shape[1]
    
    room_count = 1
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Ignore tiny spots or the entire image boundary
        if area < min_area or area > img_area * 0.9:
            continue
            
        # Get bounding box
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Convert pixel scale to meters
        width_m = round(w * scale_factor, 1)
        length_m = round(h * scale_factor, 1)
        x_m = round(x * scale_factor, 1)
        y_m = round(y * scale_factor, 1)
        
        # Basic heuristic mapping to room types based on area
        area_m = width_m * length_m
        if area_m < 5.0:
            name = f"Bathroom/Storage {room_count}"
        elif area_m > 25.0:
            name = f"Living/Dining {room_count}"
        else:
            name = f"Bedroom {room_count}"
            
        rooms.append({
            "name": name,
            "width": width_m,
            "length": length_m,
            "x": x_m,
            "y": y_m
        })
        room_count += 1
        
        # Synthesize general walls based on bounding box
        # Real structural inference would merge shared walls, but we keep it simple here
        span = max(width_m, length_m)
        w_type = "load_bearing" if span > 5 else "partition"
        
        # Only add walls once for simplicity, representing the two main dimensions
        walls.append({"type": w_type, "length": length_m})
        walls.append({"type": w_type, "length": width_m})
        
    return {
        "rooms": rooms,
        "walls": walls
    }

if __name__ == "__main__":
    import os
    # Example Usage dummy:
    print("Image Parser Module Loaded.")
    print("Usage: extract_rooms_from_image('floorplan.png', scale_factor=0.05)")
    # data = extract_rooms_from_image("test.png")
