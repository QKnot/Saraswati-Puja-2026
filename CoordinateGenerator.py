from PIL import Image
import json
import os

# -------- CONFIG --------
IMAGE_PATH = "./image/s28.png"      # path to your image
OUTPUT_JSON = "s28.json"
WHITE_THRESHOLD = 20   # how white a pixel must be (0–255, higher = whiter)
# ------------------------

def is_non_white(pixel):
    """Check if a pixel is NOT white or near-white"""
    if isinstance(pixel, int):  # grayscale
        return pixel <= WHITE_THRESHOLD
    r, g, b = pixel[:3]
    # A pixel is non-white if ANY channel is below the threshold
    return r <= WHITE_THRESHOLD or g <= WHITE_THRESHOLD or b <= WHITE_THRESHOLD

def extract_non_white_pixels(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = img.load()
    
    non_white_pixels = []
    for y in range(height):
        for x in range(width):
            if is_non_white(pixels[x, y]):
                non_white_pixels.append({"x": x, "y": y})
    
    return {
        "image_name": os.path.basename(image_path),
        "width": width,
        "height": height,
        "non_white_pixel_count": len(non_white_pixels),
        "pixels": non_white_pixels
    }

if __name__ == "__main__":
    data = extract_non_white_pixels(IMAGE_PATH)
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Found {data['non_white_pixel_count']} non-white pixels")
    print(f"📄 Saved to {OUTPUT_JSON}")