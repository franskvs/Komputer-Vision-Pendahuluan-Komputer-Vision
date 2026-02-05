#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 10_radial_distortion_plumbline.py

Deskripsi:
    Program ini mendemonstrasikan konsep radial distortion (Section 11.1.4)
    dengan membuat grid garis lurus, menerapkan distorsi radial, lalu
    mengestimasi parameter distorsi menggunakan pendekatan plumb-line sederhana.

Tujuan:
    1. Memahami efek radial distortion
    2. Mengestimasi parameter distorsi k1 secara sederhana
    3. Memulihkan garis lurus dari gambar terdistorsi

Aplikasi Dunia Nyata:
    - Kalibrasi kamera wide-angle
    - Perbaikan lensa fisheye
    - Pre-processing untuk SfM dan SLAM

Author: Praktikum Computer Vision
"""

# Import path untuk output
from pathlib import Path
# Import numpy untuk operasi numerik
import numpy as np
# Import OpenCV untuk gambar
import cv2
# Import matplotlib untuk plotting
import matplotlib.pyplot as plt

# =============================================================================
# KONFIGURASI
# =============================================================================

# Ukuran gambar
IMAGE_WIDTH = 600
# Ukuran gambar
IMAGE_HEIGHT = 600
# Warna background
BACKGROUND_COLOR = (20, 20, 20)
# Warna garis
LINE_COLOR = (220, 220, 220)
# Parameter distorsi ground truth
K1_TRUE = -0.25
# Jumlah garis grid
GRID_LINES = 10

# =============================================================================
# FUNGSI UTILITAS
# =============================================================================

# Fungsi untuk membuat grid garis lurus
def create_grid_image():
    # Buat canvas kosong
    img = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
    # Isi background
    img[:] = BACKGROUND_COLOR
    # Hitung jarak antar garis
    step = IMAGE_WIDTH // (GRID_LINES + 1)
    # Gambar garis vertikal
    for i in range(1, GRID_LINES + 1):
        # Hitung posisi x
        x = i * step
        # Gambar garis vertikal
        cv2.line(img, (x, 0), (x, IMAGE_HEIGHT - 1), LINE_COLOR, 1)
    # Gambar garis horizontal
    for i in range(1, GRID_LINES + 1):
        # Hitung posisi y
        y = i * step
        # Gambar garis horizontal
        cv2.line(img, (0, y), (IMAGE_WIDTH - 1, y), LINE_COLOR, 1)
    # Kembalikan image
    return img


# Fungsi untuk menerapkan distorsi radial ke titik
def distort_points(points, k1, cx, cy):
    # Copy points
    pts = points.copy().astype(np.float64)
    # Hitung x relatif
    x = pts[:, 0] - cx
    # Hitung y relatif
    y = pts[:, 1] - cy
    # Hitung radius kuadrat
    r2 = x * x + y * y
    # Hitung faktor distorsi
    factor = 1.0 + k1 * r2
    # Terapkan distorsi
    x_dist = x * factor + cx
    # Terapkan distorsi
    y_dist = y * factor + cy
    # Kembalikan points terdistorsi
    return np.stack([x_dist, y_dist], axis=1)


# Fungsi untuk distort gambar grid
def distort_image(img, k1):
    # Ambil ukuran gambar
    h, w = img.shape[:2]
    # Hitung center
    cx, cy = w / 2.0, h / 2.0
    # Buat grid koordinat
    grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))
    # Gabungkan jadi points
    points = np.stack([grid_x.ravel(), grid_y.ravel()], axis=1)
    # Distort points
    distorted = distort_points(points, k1, cx, cy)
    # Reshape ke map
    map_x = distorted[:, 0].reshape(h, w).astype(np.float32)
    # Reshape ke map
    map_y = distorted[:, 1].reshape(h, w).astype(np.float32)
    # Warp image
    distorted_img = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    # Kembalikan image
    return distorted_img


# Fungsi untuk mengukur straightness (jarak titik ke garis)
def straightness_score(img):
    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Deteksi edge
    edges = cv2.Canny(gray, 50, 150)
    # Deteksi garis dengan Hough
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=80, maxLineGap=5)
    # Jika tidak ada garis, return skor besar
    if lines is None:
        return 1e9
    # Inisialisasi total error
    total_error = 0.0
    # Inisialisasi count
    count = 0
    # Loop garis
    for line in lines:
        # Ambil koordinat
        x1, y1, x2, y2 = line[0]
        # Hitung parameter garis
        a = y1 - y2
        # Hitung parameter garis
        b = x2 - x1
        # Hitung parameter garis
        c = x1 * y2 - x2 * y1
        # Hitung panjang normal
        norm = np.sqrt(a * a + b * b) + 1e-9
        # Sample titik sepanjang garis
        for t in np.linspace(0, 1, 10):
            # Interpolasi titik
            x = x1 + t * (x2 - x1)
            # Interpolasi titik
            y = y1 + t * (y2 - y1)
            # Hitung jarak ke garis
            dist = abs(a * x + b * y + c) / norm
            # Tambah ke total error
            total_error += dist
            # Increment count
            count += 1
    # Return mean error
    return total_error / max(count, 1)


# Fungsi untuk mencari k1 terbaik dengan grid search

def estimate_k1_plumbline(distorted_img, k1_candidates):
    # Inisialisasi best k1
    best_k1 = None
    # Inisialisasi best score
    best_score = 1e9
    # Ambil ukuran image
    h, w = distorted_img.shape[:2]
    # Hitung center
    cx, cy = w / 2.0, h / 2.0
    # Loop kandidat k1
    for k1 in k1_candidates:
        # Undistort dengan k1 kandidat (inverse kira-kira)
        undistorted = distort_image(distorted_img, -k1)
        # Hitung straightness score
        score = straightness_score(undistorted)
        # Update best jika lebih kecil
        if score < best_score:
            best_score = score
            best_k1 = k1
    # Kembalikan best k1
    return best_k1


# =============================================================================
# MAIN PROGRAM
# =============================================================================

# Fungsi utama

def main():
    # Print header
    print("=" * 70)
    # Print header
    print("RADIAL DISTORTION - PLUMB LINE METHOD")
    # Print header
    print("=" * 70)

    # Setup output dir
    script_dir = Path(__file__).parent.resolve()
    # Setup output dir
    output_dir = script_dir / "output"
    # Buat output dir
    output_dir.mkdir(exist_ok=True)

    # Buat image grid
    grid_img = create_grid_image()
    # Distort image grid
    distorted_img = distort_image(grid_img, K1_TRUE)

    # Buat kandidat k1
    k1_candidates = np.linspace(-0.5, 0.5, 41)
    # Estimasi k1
    k1_est = estimate_k1_plumbline(distorted_img, k1_candidates)

    # Undistort menggunakan k1 estimasi
    undistorted_img = distort_image(distorted_img, -k1_est)

    # Print hasil
    print(f"K1 Ground Truth: {K1_TRUE}")
    # Print hasil
    print(f"K1 Estimasi: {k1_est}")

    # Simpan visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    # Tampilkan original
    axes[0].imshow(cv2.cvtColor(grid_img, cv2.COLOR_BGR2RGB))
    # Set title
    axes[0].set_title("Original Grid")
    # Hide axis
    axes[0].axis("off")

    # Tampilkan distorted
    axes[1].imshow(cv2.cvtColor(distorted_img, cv2.COLOR_BGR2RGB))
    # Set title
    axes[1].set_title(f"Distorted (k1={K1_TRUE})")
    # Hide axis
    axes[1].axis("off")

    # Tampilkan undistorted
    axes[2].imshow(cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2RGB))
    # Set title
    axes[2].set_title(f"Undistorted (k1={k1_est:.2f})")
    # Hide axis
    axes[2].axis("off")

    # Simpan output
    output_path = output_dir / "10_radial_distortion.png"
    # Save figure
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    # Close figure
    plt.close()

    # Simpan report
    report_path = output_dir / "10_radial_distortion_report.txt"
    # Buka file
    with open(report_path, "w", encoding="utf-8") as f:
        # Tulis header
        f.write("LAPORAN RADIAL DISTORTION\n")
        # Tulis k1 true
        f.write(f"K1 Ground Truth: {K1_TRUE}\n")
        # Tulis k1 estimasi
        f.write(f"K1 Estimasi: {k1_est}\n")

    # Print output
    print(f"Output disimpan di: {output_path}")
    # Print selesai
    print("\n✓ Program selesai!")


# Entry point
if __name__ == "__main__":
    # Panggil main
    main()
