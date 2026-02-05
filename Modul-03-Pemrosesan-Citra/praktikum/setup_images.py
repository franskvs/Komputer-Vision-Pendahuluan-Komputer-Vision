#!/usr/bin/env python3
# ============================================================
# SETUP IMAGES: Generate sample images for BAB 3
# ============================================================
# Deskripsi: Script untuk membuat gambar sample yang digunakan
#            dalam praktikum Bab 3 - Pemrosesan Citra
# ============================================================

import os
import urllib.request
import ssl
import sys

# Disable SSL verification untuk beberapa server
ssl._create_default_https_context = ssl._create_unverified_context

# Setup directory
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_SCRIPT, "data", "images")
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# Buat folder yang diperlukan
os.makedirs(DIR_DATA, exist_ok=True)
os.makedirs(DIR_OUTPUT, exist_ok=True)

# Buat folder output untuk setiap program
for i in range(1, 17):
    os.makedirs(os.path.join(DIR_OUTPUT, f"output{i}"), exist_ok=True)

print("=" * 80)
print("SETUP IMAGES FOR BAB 3: PEMROSESAN CITRA")
print("=" * 80)

# ============================================================
# IMAGE DEFINITIONS
# ============================================================

IMAGES_TO_DOWNLOAD = [
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=512", "portrait.jpg"),
    ("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=512", "landscape.jpg"),
    ("https://images.unsplash.com/photo-1525909002-1b05e0c869d8?w=512", "colorful.jpg"),
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
    
    # 1. Noise sample for denoising
    filepath = os.path.join(DIR_DATA, "noise_sample.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        # Gradient background
        for i in range(400):
            for j in range(400):
                img[i, j] = [100 + i//4, 100, 100 + j//4]
        # Add shapes
        cv2.rectangle(img, (50, 50), (150, 150), (255, 255, 255), -1)
        cv2.circle(img, (300, 200), 60, (0, 255, 255), -1)
        # Add Gaussian noise
        noise = np.random.normal(0, 25, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        cv2.imwrite(filepath, img)
        print(f"  [OK] noise_sample.jpg")
        generated += 1
    
    # 2. Edges demo
    filepath = os.path.join(DIR_DATA, "edges_demo.png")
    if not os.path.exists(filepath):
        img = np.zeros((400, 400), dtype=np.uint8)
        img[50:150, 50:150] = 255
        img[100:200, 200:350] = 200
        cv2.circle(img, (300, 300), 50, 150, -1)
        # Add gradient
        for i in range(200, 400):
            img[i, 50:150] = (i - 200)
        cv2.imwrite(filepath, img)
        print(f"  [OK] edges_demo.png")
        generated += 1
    
    # 3. Text document for thresholding
    filepath = os.path.join(DIR_DATA, "text_document.jpg")
    if not os.path.exists(filepath):
        img = np.ones((600, 800, 3), dtype=np.uint8) * 240
        # Add some "text" (lines)
        for y in range(50, 550, 30):
            width = np.random.randint(300, 700)
            cv2.line(img, (50, y), (50 + width, y), (30, 30, 30), 2)
        # Add noise
        noise = np.random.normal(0, 10, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        cv2.imwrite(filepath, img)
        print(f"  [OK] text_document.jpg")
        generated += 1
    
    # 4. Low contrast image for histogram equalization
    filepath = os.path.join(DIR_DATA, "low_contrast.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        for i in range(400):
            for j in range(400):
                val = 100 + int(20 * np.sin(i/30) * np.cos(j/30))
                img[i, j] = [val, val, val]
        cv2.rectangle(img, (100, 100), (300, 300), (120, 120, 120), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] low_contrast.jpg")
        generated += 1
    
    # 5. Morphology sample
    filepath = os.path.join(DIR_DATA, "morphology_sample.png")
    if not os.path.exists(filepath):
        img = np.zeros((400, 400), dtype=np.uint8)
        cv2.rectangle(img, (50, 50), (150, 150), 255, -1)
        cv2.circle(img, (250, 100), 40, 255, -1)
        cv2.ellipse(img, (320, 280), (60, 30), 45, 0, 360, 255, -1)
        # Add some noise
        for _ in range(50):
            x, y = np.random.randint(0, 400, 2)
            cv2.circle(img, (x, y), 3, 255, -1)
        for _ in range(30):
            x, y = np.random.randint(0, 400, 2)
            cv2.circle(img, (x, y), 2, 0, -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] morphology_sample.png")
        generated += 1
    
    # 6. Portrait fallback
    filepath = os.path.join(DIR_DATA, "portrait.jpg")
    if not os.path.exists(filepath):
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        img[:, :] = [180, 200, 230]
        cv2.ellipse(img, (256, 256), (150, 200), 0, 0, 360, (160, 180, 210), -1)
        cv2.circle(img, (200, 220), 25, (50, 50, 50), -1)
        cv2.circle(img, (312, 220), 25, (50, 50, 50), -1)
        cv2.circle(img, (200, 220), 10, (255, 255, 255), -1)
        cv2.circle(img, (312, 220), 10, (255, 255, 255), -1)
        cv2.line(img, (256, 240), (256, 290), (120, 140, 170), 3)
        cv2.ellipse(img, (256, 340), (50, 20), 0, 0, 180, (100, 100, 200), -1)
        cv2.imwrite(filepath, img)
        print(f"  [OK] portrait.jpg (synthetic)")
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
    print("  python3 01_brightness_contrast.py")
    print("  python3 run_all_tests.py  (untuk test semua program)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
