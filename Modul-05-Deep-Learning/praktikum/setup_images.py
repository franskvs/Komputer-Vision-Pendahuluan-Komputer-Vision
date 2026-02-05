#!/usr/bin/env python3
# ============================================================
# SETUP IMAGES: Generate sample images for BAB 5
# ============================================================
# Deskripsi: Script untuk membuat gambar sample yang digunakan
#            dalam praktikum Bab 5 - Deep Learning
# ============================================================

import os
import urllib.request
import ssl
import sys

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Setup directory
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_SCRIPT, "data", "images")
DIR_MODELS = os.path.join(DIR_SCRIPT, "data", "models")
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# Buat folder yang diperlukan
os.makedirs(DIR_DATA, exist_ok=True)
os.makedirs(DIR_MODELS, exist_ok=True)
os.makedirs(DIR_OUTPUT, exist_ok=True)

# Buat folder output untuk setiap program
for i in range(1, 13):
    os.makedirs(os.path.join(DIR_OUTPUT, f"output{i}"), exist_ok=True)

print("=" * 80)
print("SETUP IMAGES FOR BAB 5: DEEP LEARNING")
print("=" * 80)

# ============================================================
# IMAGE DEFINITIONS
# ============================================================

IMAGES_TO_DOWNLOAD = [
    ("https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=512", "dog.jpg"),
    ("https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=512", "cat.jpg"),
    ("https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=640", "street.jpg"),
    ("https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=640", "car.jpg"),
]

def download_images():
    """Download images dari URL."""
    print("\n[1/3] DOWNLOADING IMAGES...")
    
    sukses = 0
    gagal = 0
    
    for url, filename in IMAGES_TO_DOWNLOAD:
        filepath = os.path.join(DIR_DATA, filename)
        
        if os.path.exists(filepath):
            print(f"  [SKIP] {filename} sudah ada")
            sukses += 1
            continue
        
        try:
            print(f"  [DOWNLOAD] {filename}...", end=" ", flush=True)
            urllib.request.urlretrieve(url, filepath)
            size = os.path.getsize(filepath) / 1024
            print(f"OK ({size:.1f} KB)")
            sukses += 1
        except Exception as e:
            print(f"GAGAL ({str(e)[:50]})")
            gagal += 1
    
    print(f"  Download: {sukses} sukses, {gagal} gagal")
    return sukses > 0


def copy_from_bab1():
    """Copy images from Bab-01 if available."""
    print("\n[2/3] CHECKING BAB-01 IMAGES...")
    
    bab1_data = os.path.join(DIR_SCRIPT, "..", "..", "Bab-01-Pendahuluan", 
                             "praktikum", "data", "images")
    
    if not os.path.exists(bab1_data):
        print(f"  [INFO] Bab-01 data folder tidak ditemukan")
        return False
    
    import shutil
    copied = 0
    
    for filename in os.listdir(bab1_data):
        src = os.path.join(bab1_data, filename)
        dst = os.path.join(DIR_DATA, filename)
        
        if os.path.isfile(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  [COPY] {filename}")
            copied += 1
    
    print(f"  Copied: {copied} files from Bab-01")
    return True


def generate_synthetic_images():
    """Generate synthetic images using numpy and OpenCV."""
    print("\n[3/3] GENERATING SYNTHETIC IMAGES...")
    
    try:
        import numpy as np
        import cv2
    except ImportError:
        print("  [ERROR] numpy dan opencv-python diperlukan!")
        return False
    
    generated = 0
    
    # 1. Dog fallback
    filepath = os.path.join(DIR_DATA, "dog.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        img[:, :] = [180, 200, 150]  # Background
        # Simple dog shape
        cv2.ellipse(img, (256, 300), (120, 100), 0, 0, 360, (80, 60, 40), -1)  # Body
        cv2.ellipse(img, (256, 180), (70, 60), 0, 0, 360, (80, 60, 40), -1)  # Head
        cv2.circle(img, (220, 160), 15, (0, 0, 0), -1)  # Eye
        cv2.circle(img, (292, 160), 15, (0, 0, 0), -1)  # Eye
        cv2.ellipse(img, (256, 200), (20, 10), 0, 0, 360, (0, 0, 0), -1)  # Nose
        cv2.imwrite(filepath, img)
        print(f"  [OK] dog.jpg (synthetic)")
        generated += 1
    
    # 2. Cat fallback
    filepath = os.path.join(DIR_DATA, "cat.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        img[:, :] = [200, 180, 160]  # Background
        # Simple cat shape
        cv2.ellipse(img, (256, 320), (100, 80), 0, 0, 360, (150, 140, 130), -1)  # Body
        cv2.ellipse(img, (256, 180), (80, 70), 0, 0, 360, (150, 140, 130), -1)  # Head
        cv2.circle(img, (220, 160), 20, (50, 200, 50), -1)  # Eye
        cv2.circle(img, (292, 160), 20, (50, 200, 50), -1)  # Eye
        # Ears (triangles)
        pts1 = np.array([[190, 130], [170, 80], [210, 100]], np.int32)
        pts2 = np.array([[322, 130], [342, 80], [302, 100]], np.int32)
        cv2.fillPoly(img, [pts1], (150, 140, 130))
        cv2.fillPoly(img, [pts2], (150, 140, 130))
        cv2.imwrite(filepath, img)
        print(f"  [OK] cat.jpg (synthetic)")
        generated += 1
    
    # 3. Street scene fallback
    filepath = os.path.join(DIR_DATA, "street.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        # Sky
        img[:200, :] = [180, 150, 100]
        # Ground/road
        img[200:, :] = [80, 80, 80]
        # Buildings
        cv2.rectangle(img, (50, 80), (150, 200), (100, 100, 120), -1)
        cv2.rectangle(img, (180, 50), (280, 200), (90, 90, 110), -1)
        cv2.rectangle(img, (400, 100), (550, 200), (110, 110, 130), -1)
        # Road markings
        for x in range(100, 600, 100):
            cv2.rectangle(img, (x, 330), (x+50, 340), (255, 255, 255), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] street.jpg (synthetic)")
        generated += 1
    
    # 4. Car fallback
    filepath = os.path.join(DIR_DATA, "car.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img[:, :] = [180, 180, 180]  # Background
        # Car body
        cv2.rectangle(img, (150, 200), (490, 320), (50, 50, 200), -1)
        cv2.rectangle(img, (200, 150), (440, 200), (50, 50, 200), -1)
        # Windows
        cv2.rectangle(img, (210, 160), (300, 195), (200, 220, 240), -1)
        cv2.rectangle(img, (320, 160), (430, 195), (200, 220, 240), -1)
        # Wheels
        cv2.circle(img, (220, 320), 40, (30, 30, 30), -1)
        cv2.circle(img, (420, 320), 40, (30, 30, 30), -1)
        cv2.circle(img, (220, 320), 20, (100, 100, 100), -1)
        cv2.circle(img, (420, 320), 20, (100, 100, 100), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] car.jpg (synthetic)")
        generated += 1
    
    # 5. Sample for augmentation
    filepath = os.path.join(DIR_DATA, "sample_augment.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((256, 256, 3), dtype=np.uint8)
        for i in range(256):
            for j in range(256):
                img[i, j] = [100 + i//3, 100 + j//3, 100]
        cv2.rectangle(img, (50, 50), (200, 200), (255, 255, 0), -1)
        cv2.circle(img, (128, 128), 50, (0, 0, 255), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] sample_augment.jpg")
        generated += 1
    
    print(f"  Generated: {generated} images")
    return True


def create_imagenet_labels():
    """Create a sample ImageNet labels file."""
    labels_path = os.path.join(DIR_MODELS, "imagenet_labels.txt")
    if not os.path.exists(labels_path):
        # Sample labels (subset)
        labels = [
            "tench", "goldfish", "great_white_shark", "tiger_shark", "hammerhead",
            "electric_ray", "stingray", "cock", "hen", "ostrich",
            "dog", "cat", "bird", "horse", "elephant"
        ]
        with open(labels_path, "w") as f:
            for label in labels:
                f.write(label + "\n")
        print(f"  [OK] imagenet_labels.txt (sample)")


def main():
    """Main setup function."""
    print(f"\nDirectory: {DIR_SCRIPT}")
    print(f"Data folder: {DIR_DATA}")
    print(f"Models folder: {DIR_MODELS}")
    print(f"Output folder: {DIR_OUTPUT}\n")
    
    # Copy from Bab-01 if available
    copy_from_bab1()
    
    # Download images
    download_images()
    
    # Generate synthetic images
    generate_synthetic_images()
    
    # Create labels file
    create_imagenet_labels()
    
    # List final images
    print("\n" + "=" * 80)
    print("GAMBAR YANG TERSEDIA")
    print("=" * 80)
    
    if os.path.exists(DIR_DATA):
        files = sorted(os.listdir(DIR_DATA))
        for f in files:
            size = os.path.getsize(os.path.join(DIR_DATA, f)) / 1024
            print(f"  {f:30} ({size:.1f} KB)")
        print(f"\nTotal: {len(files)} files")
    
    print("\n" + "=" * 80)
    print("✅ SETUP COMPLETE!")
    print("=" * 80)
    print("\nSekarang Anda bisa menjalankan program praktikum:")
    print("  python3 01_opencv_dnn_classification.py")
    print("  python3 run_all_tests.py  (untuk test semua program)")
    print("\n⚠️  Beberapa program memerlukan library tambahan:")
    print("  pip install torch torchvision tensorflow keras ultralytics onnx")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
