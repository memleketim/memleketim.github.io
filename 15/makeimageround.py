import os
from PIL import Image, ImageDraw

def circle_crop_image(img: Image.Image) -> Image.Image:
    """Bir resmi ortalanmış daire içine alır, dışını transparan yapar."""
    w, h = img.size
    r = min(w, h) // 2
    cx, cy = w // 2, h // 2

    # Maske (siyah arkaplan)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    # Ortalanmış daire koordinatları
    left_up = (cx - r, cy - r)
    right_down = (cx + r, cy + r)
    draw.ellipse([left_up, right_down], fill=255)

    # Sonuç resmi oluştur
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    result.paste(img, (0, 0), mask=mask)
    return result

def process_folder(input_dir="input", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    # Desteklenen resim uzantıları
    extensions = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")  
            # Hepsi PNG olarak kaydedilir (transparan destek için)

            img = Image.open(input_path).convert("RGBA")
            result = circle_crop_image(img)
            result.save(output_path, format="PNG")
            print(f"✔ {filename} işlendi → {output_path}")

# Çalıştır
process_folder("input", "output")
