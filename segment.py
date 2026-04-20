import cv2
import numpy as np


# ============================================
# 1. Parse Polygon (Handles ALL formats)
# ============================================
def parse_polygon(p):
    if p is None:
        return None

    # Case 1: Already list of points
    if isinstance(p, list):
        if len(p) >= 4:
            return np.array(p, dtype=np.float32)

    # Case 2: Dictionary formats
    if isinstance(p, dict):

        # ✅ YOUR DATASET FORMAT (x0,y0,...)
        if all(k in p for k in ["x0","y0","x1","y1","x2","y2","x3","y3"]):
            return np.array([
                [p["x0"], p["y0"]],
                [p["x1"], p["y1"]],
                [p["x2"], p["y2"]],
                [p["x3"], p["y3"]],
            ], dtype=np.float32)

        # Other formats
        if "points" in p:
            return np.array(p["points"], dtype=np.float32)

        if "vertices" in p:
            return np.array(p["vertices"], dtype=np.float32)

        # Bounding box format
        if all(k in p for k in ["x","y","width","height"]):
            x, y = p["x"], p["y"]
            w, h = p["width"], p["height"]

            return np.array([
                [x, y],
                [x+w, y],
                [x+w, y+h],
                [x, y+h]
            ], dtype=np.float32)

    return None


# ============================================
# 2. Crop Line (ROBUST VERSION)
# ============================================
def crop_line(img, polygon):
    polygon = parse_polygon(polygon)

    # Safety check
    if polygon is None or len(polygon) < 4:
        return None

    try:
        # Bounding box from polygon
        x_min = int(np.min(polygon[:, 0]))
        y_min = int(np.min(polygon[:, 1]))
        x_max = int(np.max(polygon[:, 0]))
        y_max = int(np.max(polygon[:, 1]))

        h, w = img.shape[:2]

        # Clamp values to image size
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_max)
        y_max = min(h, y_max)

        # Reject tiny crops
        if (x_max - x_min) < 10 or (y_max - y_min) < 10:
            return None

        # Crop
        cropped = img[y_min:y_max, x_min:x_max]

        return cropped

    except Exception as e:
        print("❌ Crop error:", e)
        return None