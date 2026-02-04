"""
PRAKTIKUM BAB 8: IMAGE STITCHING
================================
Program 2: OpenCV Stitcher Class

Deskripsi:
    Program ini mendemonstrasikan penggunaan cv2.Stitcher, high-level API
    dari OpenCV untuk image stitching. Stitcher class menghandle semua
    langkah secara otomatis: feature detection, matching, bundle adjustment,
    warping, blending, dan cropping.

Keunggulan Stitcher Class:
    - Mudah digunakan (hanya beberapa baris kode)
    - Otomatis handle multi-image stitching
    - Built-in exposure compensation
    - Multi-band blending untuk hasil seamless
    - Bundle adjustment untuk akurasi global

Mode Stitcher:
    - PANORAMA: Untuk foto panorama (spherical/cylindrical projection)
    - SCANS: Untuk foto dokumen/scan (affine transformation)

Parameter yang dapat dimodifikasi:
    - STITCH_MODE: Mode stitcher ('PANORAMA' atau 'SCANS')
    - TRY_GPU: Gunakan GPU acceleration jika tersedia

Output:
    - Panorama hasil stitching
    - Perbandingan dengan simple stitching

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import glob

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Mode stitcher:
# 'PANORAMA' - untuk foto panorama (default)
# 'SCANS' - untuk dokumen/foto flat
STITCH_MODE = 'PANORAMA'

# Gunakan GPU jika tersedia
TRY_GPU = False

# Path ke gambar
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output2")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def load_images_from_folder(folder_path, pattern="*.jpg"):
    """
    Load semua gambar dari folder dengan pattern tertentu.
    
    Parameters:
        folder_path: Path ke folder
        pattern: Pattern untuk filter file (default: *.jpg)
    
    Returns:
        images: List gambar
        filenames: List nama file
    """
    # Cari file dengan berbagai ekstensi
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    files = []
    
    for ext in extensions:
        files.extend(glob.glob(os.path.join(folder_path, ext)))
    
    files.sort()  # Urutkan berdasarkan nama
    
    images = []
    filenames = []
    
    for f in files:
        img = cv2.imread(f)
        if img is not None:
            images.append(img)
            filenames.append(os.path.basename(f))
            print(f"  Loaded: {os.path.basename(f)} - {img.shape}")
    
    return images, filenames

def stitch_with_stitcher(images, mode='PANORAMA'):
    """
    Gunakan OpenCV Stitcher untuk menggabungkan gambar.
    
    Parameters:
        images: List gambar untuk di-stitch
        mode: 'PANORAMA' atau 'SCANS'
    
    Returns:
        status: Status stitching
        result: Gambar hasil (None jika gagal)
    """
    # Buat Stitcher berdasarkan mode
    if mode == 'SCANS':
        stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    else:
        stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    
    print(f"\nMenjalankan Stitcher (mode: {mode})...")
    start = time.time()
    
    status, result = stitcher.stitch(images)
    
    elapsed = time.time() - start
    print(f"  Waktu proses: {elapsed:.2f} detik")
    
    # Interpretasi status
    status_messages = {
        cv2.Stitcher_OK: "OK - Stitching berhasil",
        cv2.Stitcher_ERR_NEED_MORE_IMGS: "ERROR - Butuh lebih banyak gambar",
        cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "ERROR - Estimasi homography gagal",
        cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "ERROR - Penyesuaian parameter kamera gagal"
    }
    
    print(f"  Status: {status_messages.get(status, f'Unknown ({status})')}")
    
    if status == cv2.Stitcher_OK:
        print(f"  Dimensi output: {result.shape}")
    
    return status, result

def demo_two_images():
    """
    Demo stitching dengan 2 gambar.
    """
    print("\n" + "=" * 60)
    print("DEMO 1: Stitching 2 Gambar")
    print("=" * 60)
    
    # Load gambar
    img1_path = os.path.join(DATA_DIR, "left01.jpg")
    img2_path = os.path.join(DATA_DIR, "right01.jpg")
    
    # Fallback
    if not os.path.exists(img1_path):
        img1_path = os.path.join(DATA_DIR, "graf1.png")
        img2_path = os.path.join(DATA_DIR, "graf3.png")
    
    if not os.path.exists(img1_path):
        print("Gambar tidak ditemukan!")
        return None
    
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    print(f"  Gambar 1: {img1.shape}")
    print(f"  Gambar 2: {img2.shape}")
    
    # Resize jika perlu
    max_dim = 800
    for i, img in enumerate([img1, img2]):
        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            if i == 0:
                img1 = cv2.resize(img1, None, fx=scale, fy=scale)
            else:
                img2 = cv2.resize(img2, None, fx=scale, fy=scale)
    
    images = [img1, img2]
    
    # Stitch
    status, result = stitch_with_stitcher(images, STITCH_MODE)
    
    return images, result, status

def demo_multiple_images():
    """
    Demo stitching dengan multiple gambar dari folder.
    """
    print("\n" + "=" * 60)
    print("DEMO 2: Stitching Multiple Gambar")
    print("=" * 60)
    
    # Cek folder panorama_set
    pano_folder = os.path.join(DATA_DIR, "panorama_set")
    
    if os.path.exists(pano_folder):
        images, filenames = load_images_from_folder(pano_folder)
        if len(images) >= 2:
            print(f"\nDitemukan {len(images)} gambar di panorama_set")
            status, result = stitch_with_stitcher(images, STITCH_MODE)
            return images, result, status
    
    # Jika tidak ada, gunakan gambar default
    print("\nFolder panorama_set tidak ada atau kosong.")
    print("Menggunakan gambar default...")
    
    # Kumpulkan gambar yang tersedia
    default_images = []
    default_files = ["left01.jpg", "right01.jpg", "building.jpg"]
    
    for f in default_files:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            img = cv2.imread(path)
            if img is not None:
                # Resize
                h, w = img.shape[:2]
                if max(h, w) > 600:
                    scale = 600 / max(h, w)
                    img = cv2.resize(img, None, fx=scale, fy=scale)
                default_images.append(img)
                print(f"  Loaded: {f}")
    
    if len(default_images) >= 2:
        status, result = stitch_with_stitcher(default_images[:2], STITCH_MODE)
        return default_images[:2], result, status
    
    return None, None, -1

def compare_modes():
    """
    Bandingkan hasil PANORAMA vs SCANS mode.
    """
    print("\n" + "=" * 60)
    print("DEMO 3: Perbandingan Mode PANORAMA vs SCANS")
    print("=" * 60)
    
    # Load gambar
    img1_path = os.path.join(DATA_DIR, "left01.jpg")
    img2_path = os.path.join(DATA_DIR, "right01.jpg")
    
    if not os.path.exists(img1_path):
        img1_path = os.path.join(DATA_DIR, "graf1.png")
        img2_path = os.path.join(DATA_DIR, "graf3.png")
    
    if not os.path.exists(img1_path):
        print("Gambar tidak ditemukan!")
        return None, None
    
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # Resize
    max_dim = 600
    h, w = img1.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img1 = cv2.resize(img1, None, fx=scale, fy=scale)
        img2 = cv2.resize(img2, None, fx=scale, fy=scale)
    
    images = [img1, img2]
    
    # Stitch dengan PANORAMA mode
    print("\n--- Mode PANORAMA ---")
    status1, result_pano = stitch_with_stitcher(images, 'PANORAMA')
    
    # Stitch dengan SCANS mode
    print("\n--- Mode SCANS ---")
    status2, result_scans = stitch_with_stitcher(images, 'SCANS')
    
    return result_pano, result_scans

def main():
    """
    Fungsi utama untuk menjalankan demo OpenCV Stitcher.
    """
    print("=" * 60)
    print("OPENCV STITCHER CLASS")
    print("=" * 60)
    
    # Buat folder output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = {}
    
    # Demo 1: 2 gambar
    demo1_result = demo_two_images()
    if demo1_result and demo1_result[1] is not None:
        results['two_images'] = demo1_result
    
    # Demo 3: Perbandingan mode (skip demo2 untuk efisiensi)
    pano_result, scans_result = compare_modes()
    if pano_result is not None:
        results['panorama_mode'] = pano_result
    if scans_result is not None:
        results['scans_mode'] = scans_result
    
    # Visualisasi
    if results:
        n_results = len(results)
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        idx = 0
        
        if 'two_images' in results:
            images, result, status = results['two_images']
            # Input
            combined = np.hstack([
                cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB),
                cv2.cvtColor(images[1], cv2.COLOR_BGR2RGB)
            ])
            axes[idx].imshow(combined)
            axes[idx].set_title("Input: 2 Gambar")
            axes[idx].axis('off')
            idx += 1
            
            # Result
            axes[idx].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            axes[idx].set_title(f"Hasil Stitcher (Mode: {STITCH_MODE})")
            axes[idx].axis('off')
            idx += 1
            
            # Simpan
            cv2.imwrite(os.path.join(OUTPUT_DIR, "02_stitcher_result.jpg"), result)
        
        if 'panorama_mode' in results:
            axes[idx].imshow(cv2.cvtColor(results['panorama_mode'], cv2.COLOR_BGR2RGB))
            axes[idx].set_title("Mode: PANORAMA")
            axes[idx].axis('off')
            idx += 1
        
        if 'scans_mode' in results:
            axes[idx].imshow(cv2.cvtColor(results['scans_mode'], cv2.COLOR_BGR2RGB))
            axes[idx].set_title("Mode: SCANS")
            axes[idx].axis('off')
            idx += 1
        
        # Hide unused axes
        while idx < 4:
            axes[idx].axis('off')
            idx += 1
        
        plt.suptitle("OpenCV Stitcher Class Demo", fontsize=14)
        plt.tight_layout()
        
        # Simpan
        output_path = os.path.join(OUTPUT_DIR, "02_opencv_stitcher_comparison.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\nHasil disimpan ke: {output_path}")
        
        plt.show()
    else:
        print("\nTidak ada hasil yang bisa ditampilkan.")
        print("Pastikan gambar tersedia di folder data/images/")

if __name__ == "__main__":
    main()
