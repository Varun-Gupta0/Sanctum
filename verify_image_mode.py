import cv2
import numpy as np
import os
from pipeline import run_pipeline

def create_test_floorplan(filename="test_floorplan.png"):
    # Create white image
    img = np.ones((600, 800), dtype=np.uint8) * 255
    
    # Draw black walls (thick black rectangles)
    # Border
    cv2.rectangle(img, (0, 0), (799, 599), (0, 0, 0), 20)
    
    # Room 1: Bedroom (Top Left)
    cv2.rectangle(img, (50, 50), (300, 250), (0, 0, 0), 10)
    # Room 2: Living Room (Right)
    cv2.rectangle(img, (350, 50), (750, 550), (0, 0, 0), 5)
    # Room 3: Kitchen (Bottom Left)
    cv2.rectangle(img, (50, 300), (300, 550), (0, 0, 0), 5)
    
    cv2.imwrite(filename, img)
    print(f"Created dummy floorplan image: {filename}")
    return filename

if __name__ == "__main__":
    # 1. Create dummy image
    img_path = create_test_floorplan()
    
    # 2. Run pipeline with the image
    print("\n--- Testing Pipeline with Image Mode ---")
    try:
        # We set render=False to avoid opening a browser in the background
        report = run_pipeline(input_path=img_path, render=False)
        print("\n✅ Verification SUCCESS: Found", len(report["rooms"]), "rooms in the image.")
    except Exception as e:
        print("\n❌ Verification FAILED:", e)
    
    # Cleanup (optional):
    # os.remove(img_path)
