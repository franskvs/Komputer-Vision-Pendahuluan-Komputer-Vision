# ============================================================
# SCRIPT: download_sample_data.py
# PRAKTIKUM COMPUTER VISION - BAB 1: PENDAHULUAN
# ============================================================
# Deskripsi: Script untuk mendownload gambar dan video contoh
#            yang digunakan dalam praktikum
# 
# Cara Penggunaan:
#   python download_sample_data.py
# ============================================================

import os
import urllib.request
import ssl

# Disable SSL verification untuk beberapa server
ssl._create_default_https_context = ssl._create_unverified_context

# ============================================================
# KONFIGURASI
# ============================================================

# Direktori untuk menyimpan data
DIREKTORI_IMAGES = "data/images"
DIREKTORI_VIDEOS = "data/videos"

# Daftar gambar yang akan didownload (URL, nama_file)
DAFTAR_GAMBAR = [
    # Gambar dari Unsplash (free to use)
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=640", "portrait.jpg"),
    ("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=640", "landscape.jpg"),
    ("https://images.unsplash.com/photo-1486325212027-8081e485255e?w=640", "building.jpg"),
    ("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=640", "forest.jpg"),
    ("https://images.unsplash.com/photo-1525909002-1b05e0c869d8?w=640", "colorful.jpg"),
    ("https://images.unsplash.com/photo-1494548162494-384bba4ab999?w=640", "sunrise.jpg"),
    ("https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=640", "cat.jpg"),
    ("https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=640", "dog.jpg"),
    ("https://images.unsplash.com/photo-1560807707-8cc77767d783?w=640", "food.jpg"),
    ("https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=640", "face.jpg"),
]

# ============================================================
# FUNGSI DOWNLOAD
# ============================================================

def buat_direktori():
    """Membuat direktori untuk data jika belum ada"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    
    path_images = os.path.join(direktori_script, DIREKTORI_IMAGES)
    path_videos = os.path.join(direktori_script, DIREKTORI_VIDEOS)
    
    for path in [path_images, path_videos]:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"[INFO] Direktori dibuat: {path}")
    
    return path_images, path_videos


def download_file(url, path_file):
    """Download file dari URL"""
    try:
        print(f"[DOWNLOAD] {os.path.basename(path_file)}...", end=" ")
        urllib.request.urlretrieve(url, path_file)
        ukuran = os.path.getsize(path_file) / 1024  # KB
        print(f"OK ({ukuran:.1f} KB)")
        return True
    except Exception as e:
        print(f"GAGAL ({str(e)})")
        return False


def download_semua_gambar(path_images):
    """Download semua gambar dari daftar"""
    print("\n" + "=" * 50)
    print("DOWNLOADING SAMPLE IMAGES")
    print("=" * 50)
    
    sukses = 0
    gagal = 0
    
    for url, nama_file in DAFTAR_GAMBAR:
        path_file = os.path.join(path_images, nama_file)
        
        # Skip jika sudah ada
        if os.path.exists(path_file):
            print(f"[SKIP] {nama_file} sudah ada")
            sukses += 1
            continue
        
        if download_file(url, path_file):
            sukses += 1
        else:
            gagal += 1
    
    print(f"\n[HASIL] Sukses: {sukses}, Gagal: {gagal}")
    return sukses, gagal


def buat_gambar_test_pattern(path_images):
    """Membuat gambar test pattern menggunakan numpy"""
    try:
        import numpy as np
        import cv2
        
        print("\n[INFO] Membuat test pattern images...")
        
        # 1. Color bars
        color_bars = np.zeros((480, 640, 3), dtype=np.uint8)
        warna = [
            [255, 255, 255],  # Putih
            [0, 255, 255],    # Yellow
            [255, 255, 0],    # Cyan
            [0, 255, 0],      # Green
            [255, 0, 255],    # Magenta
            [0, 0, 255],      # Red
            [255, 0, 0],      # Blue
            [0, 0, 0],        # Hitam
        ]
        lebar_bar = 640 // 8
        for i, w in enumerate(warna):
            color_bars[:, i*lebar_bar:(i+1)*lebar_bar] = w
        cv2.imwrite(os.path.join(path_images, "color_bars.png"), color_bars)
        print("[OK] color_bars.png")
        
        # 2. Gradient grayscale
        gradient = np.zeros((256, 512), dtype=np.uint8)
        for i in range(256):
            gradient[i, :] = i
        cv2.imwrite(os.path.join(path_images, "gradient.png"), gradient)
        print("[OK] gradient.png")
        
        # 3. Checkerboard pattern
        checker = np.zeros((400, 400), dtype=np.uint8)
        for i in range(0, 400, 50):
            for j in range(0, 400, 50):
                if (i//50 + j//50) % 2:
                    checker[i:i+50, j:j+50] = 255
        cv2.imwrite(os.path.join(path_images, "checkerboard.png"), checker)
        print("[OK] checkerboard.png")
        
        # 4. HSV color wheel
        hsv_wheel = np.zeros((300, 300, 3), dtype=np.uint8)
        center = (150, 150)
        for y in range(300):
            for x in range(300):
                dx = x - center[0]
                dy = y - center[1]
                dist = np.sqrt(dx*dx + dy*dy)
                if dist <= 140:
                    hue = int((np.arctan2(dy, dx) + np.pi) * 180 / np.pi / 2)
                    sat = int(dist / 140 * 255)
                    hsv_wheel[y, x] = [hue, sat, 255]
        hsv_wheel_bgr = cv2.cvtColor(hsv_wheel, cv2.COLOR_HSV2BGR)
        cv2.imwrite(os.path.join(path_images, "hsv_wheel.png"), hsv_wheel_bgr)
        print("[OK] hsv_wheel.png")
        
        # 5. Test shapes
        shapes = np.zeros((400, 600, 3), dtype=np.uint8)
        shapes[:] = [50, 50, 50]
        cv2.rectangle(shapes, (50, 50), (150, 150), (255, 0, 0), -1)
        cv2.circle(shapes, (250, 100), 50, (0, 255, 0), -1)
        cv2.ellipse(shapes, (400, 100), (80, 40), 0, 0, 360, (0, 0, 255), -1)
        pts = np.array([[500, 50], [550, 150], [450, 150]], np.int32)
        cv2.fillPoly(shapes, [pts], (255, 255, 0))
        cv2.putText(shapes, "OpenCV Test", (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        cv2.imwrite(os.path.join(path_images, "shapes.png"), shapes)
        print("[OK] shapes.png")
        
        print("[INFO] Test pattern images berhasil dibuat!")
        
    except ImportError:
        print("[WARNING] NumPy atau OpenCV belum terinstall")
        print("          Jalankan: pip install numpy opencv-python")


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    print("\n" + "=" * 50)
    print("DOWNLOAD SAMPLE DATA - PRAKTIKUM COMPUTER VISION")
    print("=" * 50)
    
    # Buat direktori
    path_images, path_videos = buat_direktori()
    
    # Download gambar
    download_semua_gambar(path_images)
    
    # Buat test pattern
    buat_gambar_test_pattern(path_images)
    
    print("\n" + "=" * 50)
    print("DOWNLOAD SELESAI!")
    print("=" * 50)
    print(f"\nGambar tersimpan di: {path_images}")
    print(f"Video tersimpan di : {path_videos}")
    
    # List files
    print("\n[DAFTAR FILE]")
    for f in sorted(os.listdir(path_images)):
        size = os.path.getsize(os.path.join(path_images, f)) / 1024
        print(f"  - {f} ({size:.1f} KB)")


if __name__ == "__main__":
    main()
