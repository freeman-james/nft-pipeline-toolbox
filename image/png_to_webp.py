import os
from PIL import Image

OUTPUT_DIR = "webp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir("."):
    if not filename.lower().endswith(".png"):
        continue

    in_path = filename
    out_name = os.path.splitext(filename)[0] + ".webp"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    with Image.open(in_path) as img:
        # Ensure alpha preserved
        img = img.convert("RGBA")
        img.save(out_path, format="WEBP", lossless=True, method=6)

    print(f"✅ {filename} -> {out_path}")

print("✅ Done. Lossless WebP files in ./webp")
