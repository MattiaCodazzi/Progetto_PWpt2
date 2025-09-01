import os
from PIL import Image

# Cartelle di input e output
INPUT_DIR = "gallery/static/img"
OUTPUT_DIR = "gallery/static/img_ottimizzate"

# File da ottimizzare (solo background)
TARGET_FILES = [
    "bg_chiaro.png",
    "bg_scuro.png",
    "bg_nero.png",
    "background.jpg"
]

# Dimensioni massime per gli sfondi
MAX_WIDTH = 2400
MAX_HEIGHT = 1600

# Parametri di compressione
FORMAT = "webp"   # puoi mettere "orig" per mantenere il formato originale
QUALITY = 82

def ottimizza_background(file):
    in_path = os.path.join(INPUT_DIR, file)
    if not os.path.exists(in_path):
        print(f"⚠️ File non trovato: {file}")
        return
    
    try:
        img = Image.open(in_path)
        w, h = img.size
        scale = min(MAX_WIDTH / w, MAX_HEIGHT / h, 1.0)
        new_size = (int(w * scale), int(h * scale))
        img_resized = img.resize(new_size, Image.LANCZOS)

        # Nome file di output
        name, _ = os.path.splitext(file)
        out_file = f"{name}_bg.webp" if FORMAT == "webp" else file
        out_path = os.path.join(OUTPUT_DIR, out_file)

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        params = {"quality": QUALITY, "optimize": True}
        if FORMAT == "orig":
            img_resized.save(out_path, **params)
        else:
            img_resized.save(out_path, FORMAT.upper(), **params)

        print(f"✅ {file} → {out_file} ({img.size} → {new_size})")

    except Exception as e:
        print(f"❌ Errore con {file}: {e}")

def main():
    print("=== Ottimizzazione sfondi museo ===")
    for file in TARGET_FILES:
        ottimizza_background(file)

if __name__ == "__main__":
    main()
