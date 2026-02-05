"""
Download Sample Data untuk Praktikum Bab 10: Computational Photography
======================================================================

Script ini mendownload gambar-gambar sampel yang diperlukan untuk
praktikum computational photography (HDR, denoising, enhancement).

Penggunaan:
    python download_sample_data.py

Data yang didownload:
    - Multi-exposure bracket images (untuk HDR)
    - Images untuk denoising test
    - Portrait images (untuk bokeh simulation)
    - Low-quality images (untuk enhancement)
"""

import urllib.request
import os
import sys
import cv2
import numpy as np

def download_file(url, filepath):
    """
    Download file dari URL ke filepath yang ditentukan.
    """
    try:
        print(f"  Downloading {os.path.basename(filepath)}...", end=" ")
        urllib.request.urlretrieve(url, filepath)
        print("✓")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def create_exposure_bracket(output_dir, base_name="scene"):
    """
    Buat synthetic exposure bracket dari satu gambar.
    """
    print("  Creating synthetic exposure bracket...", end=" ")
    
    # Create a synthetic HDR-like scene
    h, w = 480, 640
    
    # Create base image with high dynamic range content
    base = np.zeros((h, w, 3), dtype=np.float32)
    
    # Sky gradient (bright)
    for y in range(h//3):
        brightness = 200 + 55 * (1 - y/(h//3))
        base[y, :] = [brightness * 0.8, brightness * 0.9, brightness]
    
    # Ground (darker)
    for y in range(h//3, h):
        base[y, :] = [50, 80, 50]
    
    # Sun (very bright)
    cv2.circle(base, (w//4, h//6), 40, (255, 255, 220), -1)
    
    # Building silhouette (very dark)
    pts = np.array([[w//2, h], [w//2, h//2], [w//2+50, h//3], 
                    [w//2+100, h//2], [w//2+100, h]], np.int32)
    cv2.fillPoly(base, [pts], (30, 30, 40))
    
    # Window (bright spot in dark building)
    cv2.rectangle(base, (w//2+30, h//2+20), (w//2+50, h//2+50), (180, 180, 120), -1)
    
    # Create different exposures
    exposures = []
    exposure_times = [1/30, 1/4, 1]  # Under, normal, over
    
    for i, ev in enumerate([-2, 0, 2]):  # EV adjustments
        factor = 2 ** ev
        exposed = np.clip(base * factor, 0, 255).astype(np.uint8)
        exposures.append(exposed)
        
        filename = f"{base_name}_exp{i+1}.jpg"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, exposed)
    
    print("✓")
    return True

def create_noisy_images(output_dir):
    """
    Buat gambar dengan berbagai level noise untuk testing denoising.
    """
    print("  Creating noisy test images...", end=" ")
    
    # Create clean base image
    h, w = 480, 640
    clean = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Gradient background
    for y in range(h):
        for x in range(w):
            clean[y, x] = [
                int(100 + 50 * np.sin(x/50)),
                int(100 + 50 * np.cos(y/50)),
                int(120)
            ]
    
    # Add some shapes
    cv2.circle(clean, (w//3, h//2), 80, (50, 150, 200), -1)
    cv2.rectangle(clean, (w//2, h//3), (w*2//3, h*2//3), (200, 100, 50), -1)
    # Tulis teks ke gambar
    # a (clean): canvas/gambar tujuan
    # b ("TEST"): teks yang akan ditulis
    # c ((w//2-60, h-50)): posisi (x, y) baseline teks
    # font: tipe font (Hershey Simplex)
    # font_scale: ukuran teks (2)
    # color: warna teks dalam BGR (putih)
    # thickness: ketebalan garis teks (3)
    cv2.putText(clean, "TEST", (w//2-60, h-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Save clean
    cv2.imwrite(os.path.join(output_dir, "clean_image.jpg"), clean)
    
    # Add different noise levels
    for sigma in [15, 30, 50]:
        noisy = clean.astype(np.float32)
        noise = np.random.normal(0, sigma, clean.shape)
        noisy = np.clip(noisy + noise, 0, 255).astype(np.uint8)
        cv2.imwrite(os.path.join(output_dir, f"noisy_sigma{sigma}.jpg"), noisy)
    
    print("✓")
    return True

def create_portrait_image(output_dir):
    """
    Buat gambar portrait sederhana dengan depth map simulasi.
    """
    print("  Creating portrait test image...", end=" ")
    
    h, w = 480, 640
    
    # Background
    portrait = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        portrait[y, :] = [100 + y//10, 80 + y//10, 60]
    
    # Subject (ellipse as face)
    cv2.ellipse(portrait, (w//2, h//2), (80, 100), 0, 0, 360, (180, 160, 150), -1)
    
    # Eyes
    cv2.circle(portrait, (w//2-30, h//2-20), 15, (255, 255, 255), -1)
    cv2.circle(portrait, (w//2+30, h//2-20), 15, (255, 255, 255), -1)
    cv2.circle(portrait, (w//2-30, h//2-20), 8, (50, 50, 50), -1)
    cv2.circle(portrait, (w//2+30, h//2-20), 8, (50, 50, 50), -1)
    
    # Nose and mouth
    cv2.line(portrait, (w//2, h//2-10), (w//2, h//2+20), (150, 130, 120), 2)
    cv2.ellipse(portrait, (w//2, h//2+50), (30, 10), 0, 0, 180, (150, 100, 100), 2)
    
    cv2.imwrite(os.path.join(output_dir, "portrait.jpg"), portrait)
    
    # Create simple depth map
    depth = np.zeros((h, w), dtype=np.uint8)
    depth[:] = 255  # Background = far
    
    # Face closer
    cv2.ellipse(depth, (w//2, h//2), (80, 100), 0, 0, 360, 100, -1)
    
    cv2.imwrite(os.path.join(output_dir, "portrait_depth.png"), depth)
    
    print("✓")
    return True

def main():
    """
    Fungsi utama untuk mendownload/membuat semua data sampel.
    """
    print("=" * 60)
    print("DOWNLOAD SAMPLE DATA - BAB 10: COMPUTATIONAL PHOTOGRAPHY")
    print("=" * 60)
    
    # Setup directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    images_dir = os.path.join(data_dir, "images")
    hdr_dir = os.path.join(data_dir, "hdr_bracket")
    output_dir = os.path.join(script_dir, "output")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(hdr_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nFolder data: {data_dir}")
    print(f"Folder output: {output_dir}\n")
    
    success_count = 0
    fail_count = 0
    
    # Download some sample images
    print("Downloading sample images...")
    
    image_urls = {
        "lena.png": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg",
        "building.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/building.jpg",
        "fruits.jpg": "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/fruits.jpg",
    }
    
    for filename, url in image_urls.items():
        filepath = os.path.join(images_dir, filename)
        if os.path.exists(filepath):
            print(f"  {filename} sudah ada, skip.")
            success_count += 1
        else:
            if download_file(url, filepath):
                success_count += 1
            else:
                fail_count += 1
    
    # Create synthetic data
    print("\nMembuat data sintetis...")
    
    # HDR bracket
    if create_exposure_bracket(hdr_dir):
        success_count += 1
    else:
        fail_count += 1
    
    # Noisy images
    if create_noisy_images(images_dir):
        success_count += 1
    else:
        fail_count += 1
    
    # Portrait
    if create_portrait_image(images_dir):
        success_count += 1
    else:
        fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Berhasil: {success_count}")
    print(f"  Gagal: {fail_count}")
    
    if fail_count == 0:
        print("\n✅ Semua data berhasil disiapkan!")
    else:
        print("\n⚠️  Beberapa file gagal dibuat/didownload.")
    
    print("\n" + "=" * 60)
    print("STRUKTUR DATA")
    print("=" * 60)
    print("""
data/
├── images/
│   ├── lena.png
│   ├── building.jpg
│   ├── fruits.jpg
│   ├── clean_image.jpg
│   ├── noisy_sigma15.jpg
│   ├── noisy_sigma30.jpg
│   ├── noisy_sigma50.jpg
│   ├── portrait.jpg
│   └── portrait_depth.png
└── hdr_bracket/
    ├── scene_exp1.jpg (underexposed)
    ├── scene_exp2.jpg (normal)
    └── scene_exp3.jpg (overexposed)
""")
    
    print("TIPS:")
    print("- Untuk HDR terbaik, gunakan foto bracketed dari kamera/smartphone")
    print("- Ambil 3-5 foto dengan exposure berbeda (EV -2, 0, +2)")
    print("- Gunakan tripod untuk menghindari pergeseran")
    
    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
