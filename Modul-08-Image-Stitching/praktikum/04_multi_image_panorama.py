"""
PRAKTIKUM BAB 8: IMAGE STITCHING
================================
Program 4: Multi-Image Panorama

Deskripsi:
    Program ini mendemonstrasikan pembuatan panorama dari 3 atau lebih gambar.
    Berbeda dengan stitching 2 gambar, multi-image panorama memerlukan:
    - Penentuan urutan gambar yang benar
    - Incremental stitching atau global registration
    - Handling accumulated error

Metode Multi-Image Stitching:
    1. Incremental: Stitch gambar satu per satu dari kiri ke kanan
    2. Center-out: Mulai dari gambar tengah, expand ke kiri dan kanan
    3. Bundle Adjustment: Optimasi global semua parameter sekaligus

Program ini menggunakan metode incremental yang sederhana namun efektif
untuk jumlah gambar yang tidak terlalu banyak (< 10 gambar).

Parameter yang dapat dimodifikasi:
    - METHOD: Metode stitching ('incremental' atau 'stitcher')
    - MIN_MATCHES: Minimum matches untuk proceed

Output:
    - Panorama multi-image
    - Visualisasi proses incremental

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import time

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Metode stitching:
# 'incremental' - stitch satu per satu (lebih kontrol)
# 'stitcher' - gunakan OpenCV Stitcher (lebih robust)
METHOD = 'stitcher'

# Minimum good matches untuk proceed
MIN_MATCHES = 10

# Ratio test threshold
RATIO_TEST = 0.75

# Path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output4")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def load_panorama_images(folder_path=None):
    """
    Load gambar untuk panorama.
    
    Returns:
        images: List gambar
        names: List nama file
    """
    images = []
    names = []
    
    # Coba folder panorama_set dulu
    if folder_path is None:
        folder_path = os.path.join(DATA_DIR, "panorama_set")
    
    if os.path.exists(folder_path):
        files = sorted(glob.glob(os.path.join(folder_path, "*.[jp][pn][g]*")))
        if len(files) >= 2:
            for f in files:
                img = cv2.imread(f)
                if img is not None:
                    images.append(img)
                    names.append(os.path.basename(f))
            print(f"Loaded {len(images)} gambar dari {folder_path}")
            return images, names
    
    # Fallback: gunakan gambar default
    default_files = [
        "left01.jpg", "right01.jpg",
        "graf1.png", "graf3.png",
        "building.jpg", "home.jpg"
    ]
    
    for f in default_files:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            img = cv2.imread(path)
            if img is not None:
                images.append(img)
                names.append(f)
    
    print(f"Loaded {len(images)} gambar default")
    return images, names

def resize_images(images, max_dim=600):
    """
    Resize semua gambar ke ukuran yang seragam.
    """
    resized = []
    for img in images:
        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(img, None, fx=scale, fy=scale)
        resized.append(img)
    return resized

def stitch_two_images(img1, img2):
    """
    Stitch dua gambar menggunakan feature matching dan homography.
    """
    # Konversi ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Deteksi fitur dengan ORB
    orb = cv2.ORB_create(nfeatures=3000)
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)
    
    if des1 is None or des2 is None:
        return None
    
    # Match dengan BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    # Konversi ke float untuk FLANN compatibility
    des1_f = np.float32(des1)
    des2_f = np.float32(des2)
    
    matches = bf.knnMatch(des1_f, des2_f, k=2)
    
    # Ratio test
    good = []
    for m, n in matches:
        if m.distance < RATIO_TEST * n.distance:
            good.append(m)
    
    if len(good) < MIN_MATCHES:
        print(f"    Tidak cukup matches: {len(good)}")
        return None
    
    # Hitung homography
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    
    H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
    
    if H is None:
        return None
    
    # Warp dan blend
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Hitung canvas size
    corners2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
    warped_corners = cv2.perspectiveTransform(corners2, H)
    
    corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    all_corners = np.concatenate([corners1, warped_corners], axis=0)
    
    [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 0.5)
    
    # Batasi ukuran output untuk mencegah memory issue
    max_output = 4000
    if x_max - x_min > max_output or y_max - y_min > max_output:
        scale = max_output / max(x_max - x_min, y_max - y_min)
        x_min = int(x_min * scale)
        x_max = int(x_max * scale)
        y_min = int(y_min * scale)
        y_max = int(y_max * scale)
    
    translation = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])
    
    # Warp
    output_size = (x_max - x_min, y_max - y_min)
    result = cv2.warpPerspective(img2, translation @ H, output_size)
    
    # Overlay img1
    y_start = max(0, -y_min)
    y_end = min(y_start + h1, result.shape[0])
    x_start = max(0, -x_min)
    x_end = min(x_start + w1, result.shape[1])
    
    h_copy = y_end - y_start
    w_copy = x_end - x_start
    
    if h_copy > 0 and w_copy > 0:
        # Simple blending di overlap
        roi = result[y_start:y_end, x_start:x_end]
        img1_crop = img1[:h_copy, :w_copy]
        
        mask = (roi.sum(axis=2) > 0).astype(np.float32)[:,:,np.newaxis]
        blended = (1 - mask) * img1_crop + mask * (0.5 * roi + 0.5 * img1_crop)
        result[y_start:y_end, x_start:x_end] = blended.astype(np.uint8)
    
    return result

def incremental_stitching(images, names):
    """
    Stitch gambar secara incremental dari kiri ke kanan.
    """
    print("\nIncremental Stitching...")
    
    if len(images) < 2:
        print("Butuh minimal 2 gambar!")
        return None, []
    
    # Mulai dari gambar pertama
    panorama = images[0].copy()
    steps = [panorama.copy()]
    
    for i in range(1, len(images)):
        print(f"  Stitching gambar {i+1}/{len(images)}: {names[i]}...")
        
        result = stitch_two_images(panorama, images[i])
        
        if result is not None:
            panorama = result
            # Resize jika terlalu besar
            h, w = panorama.shape[:2]
            if max(h, w) > 2000:
                scale = 2000 / max(h, w)
                panorama = cv2.resize(panorama, None, fx=scale, fy=scale)
            
            steps.append(panorama.copy())
            print(f"    OK - ukuran saat ini: {panorama.shape}")
        else:
            print(f"    SKIP - tidak bisa di-stitch")
    
    return panorama, steps

def stitcher_method(images):
    """
    Gunakan OpenCV Stitcher untuk multi-image panorama.
    """
    print("\nMenggunakan OpenCV Stitcher...")
    
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    
    status, result = stitcher.stitch(images)
    
    status_msg = {
        cv2.Stitcher_OK: "OK",
        cv2.Stitcher_ERR_NEED_MORE_IMGS: "Butuh lebih banyak gambar",
        cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Estimasi homography gagal",
        cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Penyesuaian kamera gagal"
    }
    
    print(f"  Status: {status_msg.get(status, f'Unknown ({status})')}")
    
    if status == cv2.Stitcher_OK:
        return result
    return None

def main():
    """
    Fungsi utama untuk multi-image panorama.
    """
    print("=" * 60)
    print("MULTI-IMAGE PANORAMA")
    print("=" * 60)
    
    # Buat folder output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load gambar
    images, names = load_panorama_images()
    
    if len(images) < 2:
        print("ERROR: Butuh minimal 2 gambar!")
        print("Letakkan gambar panorama di folder data/images/panorama_set/")
        return
    
    print(f"\nGambar yang dimuat:")
    for i, (img, name) in enumerate(zip(images, names)):
        print(f"  {i+1}. {name} - {img.shape}")
    
    # Resize
    images = resize_images(images, max_dim=500)
    
    # Pilih metode
    if METHOD == 'stitcher':
        # Gunakan OpenCV Stitcher
        start = time.time()
        panorama = stitcher_method(images)
        elapsed = time.time() - start
        steps = []
    else:
        # Incremental stitching
        start = time.time()
        panorama, steps = incremental_stitching(images, names)
        elapsed = time.time() - start
    
    if panorama is None:
        print("\nERROR: Stitching gagal!")
        print("Tips:")
        print("  - Pastikan gambar memiliki overlap 20-50%")
        print("  - Coba dengan gambar yang diambil dengan tripod")
        print("  - Gunakan gambar dengan banyak fitur")
        return
    
    print(f"\nWaktu proses: {elapsed:.2f} detik")
    print(f"Dimensi panorama: {panorama.shape}")
    
    # Visualisasi
    n_images = len(images)
    
    if steps:
        # Tampilkan proses incremental
        n_steps = len(steps)
        cols = 3
        rows = (n_steps + 2) // cols + 1
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
        axes = axes.flatten()
        
        # Input images
        for i, (img, name) in enumerate(zip(images[:min(3, n_images)], names[:3])):
            axes[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[i].set_title(f"Input {i+1}: {name}")
            axes[i].axis('off')
        
        # Steps
        for i, step in enumerate(steps):
            axes[3 + i].imshow(cv2.cvtColor(step, cv2.COLOR_BGR2RGB))
            axes[3 + i].set_title(f"Setelah stitch {i+1} gambar")
            axes[3 + i].axis('off')
        
        # Hide unused
        for i in range(3 + len(steps), len(axes)):
            axes[i].axis('off')
        
    else:
        # Tampilkan input dan output saja
        n_show = min(4, n_images)
        fig, axes = plt.subplots(2, max(2, n_show), figsize=(14, 8))
        
        # Input images (row 1)
        for i in range(n_show):
            axes[0, i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
            axes[0, i].set_title(f"Input {i+1}")
            axes[0, i].axis('off')
        
        # Panorama (row 2, span all columns)
        for ax in axes[1, :]:
            ax.axis('off')
        
        axes[1, 0].imshow(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title(f"Panorama ({n_images} gambar)")
    
    plt.suptitle(f"Multi-Image Panorama\n"
                f"Method: {METHOD}, Images: {n_images}, Time: {elapsed:.2f}s", 
                fontsize=14)
    plt.tight_layout()
    
    # Simpan
    output_path = os.path.join(OUTPUT_DIR, "04_multi_image_panorama.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nVisualisasi disimpan ke: {output_path}")
    
    pano_path = os.path.join(OUTPUT_DIR, "04_panorama_result.jpg")
    cv2.imwrite(pano_path, panorama)
    print(f"Panorama disimpan ke: {pano_path}")
    
    # Auto-close setelah 2 detik
    print("\n[INFO] Menampilkan hasil... (akan auto-close dalam 2 detik)")
    plt.show(block=False)
    plt.pause(2)
    plt.close('all')
    print("[INFO] Selesai!")

if __name__ == "__main__":
    main()
