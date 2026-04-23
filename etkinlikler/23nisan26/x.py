import os
from PIL import Image

MAX_SIZE = 1000  # max kenar uzunluğu (px)

INPUT_FOLDER = "./"
OUTPUT_FOLDER = "output"  # None yaparsan üzerine yazar

def resize_image(input_path, output_path):
    with Image.open(input_path) as img:
        width, height = img.size

        # Zaten küçükse dokunma
        if max(width, height) <= MAX_SIZE:
            if OUTPUT_FOLDER:
                img.save(output_path, "JPEG", quality=90)
            return

        # Oranı koruyarak yeni boyut hesapla
        if width > height:
            new_width = MAX_SIZE
            new_height = int((MAX_SIZE / width) * height)
        else:
            new_height = MAX_SIZE
            new_width = int((MAX_SIZE / height) * width)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        resized_img.save(output_path, "JPEG", quality=90, optimize=True)

def process_folder():
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg")):
                input_path = os.path.join(root, file)

                if OUTPUT_FOLDER:
                    relative_path = os.path.relpath(root, INPUT_FOLDER)
                    output_dir = os.path.join(OUTPUT_FOLDER, relative_path)
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, file)
                else:
                    output_path = input_path

                try:
                    resize_image(input_path, output_path)
                    print(f"İşlendi: {input_path}")
                except Exception as e:
                    print(f"Hata: {input_path} -> {e}")

if __name__ == "__main__":
    process_folder()