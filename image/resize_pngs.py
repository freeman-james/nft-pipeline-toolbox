import os
from PIL import Image

OUTPUT_DIR = "resized_png"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir("."):
    if not filename.lower().endswith(".png"):
        continue

    in_path = filename
    out_path = os.path.join(OUTPUT_DIR, filename)

    with Image.open(in_path) as img:
        # preserve transparency
        img = img.convert("RGBA")
        new_size = (img.width // 2, img.height // 2)
        img = img.resize(new_size, Image.LANCZOS)
        img.save(out_path)

    print(f"✅ {filename} -> {new_size}")

print("✅ Done. Output in ./resized")
