from PIL import Image
import os

# cartelle input e output
input_dir = "gallery/static/img"
output_dir = "gallery/static/img_ottimizzate"
os.makedirs(output_dir, exist_ok=True)

# dimensione finale (quadrata)
TARGET_SIZE = (500, 500)  # puoi aumentare/diminuire

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path).convert("RGB")

        # taglio centrale quadrato
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        img_cropped = img.crop((left, top, right, bottom))

        # ridimensiono
        img_resized = img_cropped.resize(TARGET_SIZE, Image.LANCZOS)

        # salvo ottimizzato
        out_path = os.path.join(output_dir, filename)
        img_resized.save(out_path, quality=90, optimize=True)

        print(f"✅ {filename} ottimizzato e salvato in {output_dir}")
