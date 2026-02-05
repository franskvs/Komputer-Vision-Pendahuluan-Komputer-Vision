#!/usr/bin/env python3
# ============================================================
# SETUP IMAGES: Generate sample images for BAB 4
# ============================================================
# Deskripsi: Script untuk membuat gambar sample yang digunakan
#            dalam praktikum Bab 4 - Model Fitting
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
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# Buat folder yang diperlukan
os.makedirs(DIR_DATA, exist_ok=True)
os.makedirs(DIR_OUTPUT, exist_ok=True)

# Buat folder output untuk setiap program
for i in range(1, 12):
    os.makedirs(os.path.join(DIR_OUTPUT, f"output{i}"), exist_ok=True)

print("=" * 80)
print("SETUP IMAGES FOR BAB 4: MODEL FITTING")
print("=" * 80)

# ============================================================
# IMAGE DEFINITIONS
# ============================================================

IMAGES_TO_DOWNLOAD = [
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=512", "portrait.jpg"),
    ("https://images.unsplash.com/photo-1486325212027-8081e485255e?w=512", "building.jpg"),
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
    
    # 1. Feature detection sample with corners
    filepath = os.path.join(DIR_DATA, "features_sample.png")
    if not os.path.exists(filepath):
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        img[:, :] = [50, 50, 50]
        # Checkerboard pattern (banyak corners)
        for i in range(5):
            for j in range(7):
                if (i + j) % 2 == 0:
                    x1, y1 = j * 60 + 50, i * 60 + 50
                    cv2.rectangle(img, (x1, y1), (x1+50, y1+50), (200, 200, 200), -1)
        # Additional shapes
        cv2.rectangle(img, (420, 50), (550, 150), (255, 255, 255), 2)
        cv2.circle(img, (480, 280), 50, (0, 255, 255), 2)
        cv2.imwrite(filepath, img)
        print(f"  [OK] features_sample.png")
        generated += 1
    
    # 2. Lines sample for Hough
    filepath = os.path.join(DIR_DATA, "lines_sample.png")
    if not os.path.exists(filepath):
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        img[:, :] = [30, 30, 30]
        # Draw various lines
        cv2.line(img, (50, 50), (550, 100), (255, 255, 255), 2)
        cv2.line(img, (50, 150), (550, 150), (255, 255, 255), 2)
        cv2.line(img, (100, 50), (100, 350), (255, 255, 255), 2)
        cv2.line(img, (300, 50), (400, 350), (255, 255, 255), 2)
        cv2.line(img, (500, 350), (550, 50), (255, 255, 255), 2)
        # Some diagonal lines
        cv2.line(img, (50, 350), (300, 200), (200, 200, 200), 2)
        cv2.imwrite(filepath, img)
        print(f"  [OK] lines_sample.png")
        generated += 1
    
    # 3. Circles sample for Hough circles
    filepath = os.path.join(DIR_DATA, "coins.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        img[:, :] = [50, 50, 50]
        # Draw circles of various sizes
        cv2.circle(img, (100, 100), 40, (200, 200, 200), -1)
        cv2.circle(img, (250, 100), 50, (180, 180, 180), -1)
        cv2.circle(img, (350, 150), 30, (220, 220, 220), -1)
        cv2.circle(img, (80, 250), 35, (190, 190, 190), -1)
        cv2.circle(img, (200, 280), 45, (210, 210, 210), -1)
        cv2.circle(img, (320, 300), 55, (170, 170, 170), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] coins.jpg")
        generated += 1
    
    # 4. Road-like image for lane detection
    filepath = os.path.join(DIR_DATA, "road.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        # Sky (top)
        img[:200, :] = [180, 150, 100]
        # Ground (bottom)
        img[200:, :] = [50, 50, 50]
        # Road lines
        pts = np.array([[220, 480], [280, 200], [360, 200], [420, 480]], np.int32)
        cv2.fillPoly(img, [pts], (80, 80, 80))
        # Lane markers
        cv2.line(img, (300, 480), (320, 200), (255, 255, 255), 3)
        cv2.line(img, (340, 480), (320, 200), (255, 255, 255), 3)
        cv2.imwrite(filepath, img)
        print(f"  [OK] road.jpg")
        generated += 1
    
    # 5. Portrait fallback
    filepath = os.path.join(DIR_DATA, "portrait.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        img[:, :] = [180, 200, 230]
        cv2.ellipse(img, (256, 256), (150, 200), 0, 0, 360, (160, 180, 210), -1)
        cv2.circle(img, (200, 220), 25, (50, 50, 50), -1)
        cv2.circle(img, (312, 220), 25, (50, 50, 50), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] portrait.jpg (synthetic)")
        generated += 1
    
    # 6. Building fallback
    filepath = os.path.join(DIR_DATA, "building.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((500, 400, 3), dtype=np.uint8)
        img[:, :] = [180, 200, 230]  # Sky
        # Building
        cv2.rectangle(img, (80, 100), (320, 450), (100, 100, 120), -1)
        # Windows
        for row in range(4):
            for col in range(3):
                x = 100 + col * 70
                y = 130 + row * 80
                cv2.rectangle(img, (x, y), (x+40, y+50), (200, 220, 240), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] building.jpg (synthetic)")
        generated += 1
    
    print(f"  Generated: {generated} images")
    return True


def main():
    """Main setup function."""
    print(f"\nDirectory: {DIR_SCRIPT}")
    print(f"Data folder: {DIR_DATA}")
    print(f"Output folder: {DIR_OUTPUT}\n")
    
    # Copy from Bab-01 if available
    copy_from_bab1()
    
    # Download images
    download_images()
    
    # Generate synthetic images
    generate_synthetic_images()
    
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
    print("  python3 01_feature_detection.py")
    print("  python3 run_all_tests.py  (untuk test semua program)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
