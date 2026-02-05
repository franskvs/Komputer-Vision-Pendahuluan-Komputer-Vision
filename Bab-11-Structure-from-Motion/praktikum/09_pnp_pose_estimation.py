#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 09_pnp_pose_estimation.py

Deskripsi:
    Program ini mendemonstrasikan estimasi pose kamera menggunakan PnP
    (Perspective-n-Point). Ini adalah implementasi Section 11.2 (Pose Estimation)
    dari PDF, dengan data sintetis 3D-2D dan penyelesaian menggunakan cv2.solvePnP.

Tujuan:
    1. Memahami konsep PnP
    2. Mengestimasi pose kamera (R, t) dari korespondensi 3D-2D
    3. Mengukur reprojection error

Aplikasi Dunia Nyata:
    - AR marker tracking
    - Robot pose estimation
    - Kamera tracking pada film

Author: Praktikum Computer Vision
"""

# Import modul untuk path
from pathlib import Path
# Import numpy untuk operasi numerik
import numpy as np
# Import OpenCV untuk PnP
import cv2
# Import matplotlib untuk visualisasi
import matplotlib.pyplot as plt

# =============================================================================
# KONFIGURASI
# =============================================================================

# Ukuran image sintetis
IMAGE_WIDTH = 640
# Ukuran image sintetis
IMAGE_HEIGHT = 480
# Focal length (px)
FOCAL_LENGTH = 800.0
# Principal point
PRINCIPAL_POINT = (IMAGE_WIDTH / 2.0, IMAGE_HEIGHT / 2.0)
# Noise untuk 2D points
NOISE_STD = 1.0

# =============================================================================
# FUNGSI UTILITAS
# =============================================================================

# Fungsi untuk membuat matrix kamera K
def build_camera_matrix(f, pp):
    # Ambil principal point
    cx, cy = pp
    # Buat matrix kamera
    K = np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]], dtype=np.float64)
    # Kembalikan matrix
    return K


# Fungsi untuk membuat 3D points pada kubus
def create_cube_points(size=1.0):
    # Definisikan titik-titik kubus
    points = np.array([
        [-size, -size, 0],
        [ size, -size, 0],
        [ size,  size, 0],
        [-size,  size, 0],
        [-size, -size, 2*size],
        [ size, -size, 2*size],
        [ size,  size, 2*size],
        [-size,  size, 2*size],
    ], dtype=np.float64)
    # Kembalikan titik 3D
    return points


# Fungsi untuk membuat pose kamera ground truth
def create_ground_truth_pose():
    # Definisikan rotasi (Rodrigues)
    rvec = np.array([0.2, -0.1, 0.3], dtype=np.float64)
    # Definisikan translasi
    tvec = np.array([[0.0], [0.0], [5.0]], dtype=np.float64)
    # Kembalikan pose
    return rvec, tvec


# Fungsi untuk project 3D ke 2D
def project_points(points_3d, rvec, tvec, K):
    # Project points menggunakan OpenCV
    points_2d, _ = cv2.projectPoints(points_3d, rvec, tvec, K, None)
    # Reshape ke Nx2
    return points_2d.reshape(-1, 2)


# Fungsi untuk menambahkan noise pada titik 2D
def add_noise(points_2d, std):
    # Buat noise gaussian
    noise = np.random.normal(0, std, points_2d.shape)
    # Tambahkan noise ke titik
    noisy = points_2d + noise
    # Kembalikan noisy points
    return noisy


# =============================================================================
# MAIN PROGRAM
# =============================================================================

# Fungsi utama
def main():
    # Set seed untuk reproducibility
    np.random.seed(42)

    # Print judul
    print("=" * 70)
    # Print judul
    print("POSE ESTIMATION DENGAN PNP")
    # Print judul
    print("=" * 70)

    # Setup output dir
    script_dir = Path(__file__).parent.resolve()
    # Setup output dir
    output_dir = script_dir / "output"
    # Buat output dir jika belum ada
    output_dir.mkdir(exist_ok=True)

    # Buat matrix kamera
    K = build_camera_matrix(FOCAL_LENGTH, PRINCIPAL_POINT)
    # Buat titik 3D kubus
    points_3d = create_cube_points(size=1.0)
    # Buat pose ground truth
    rvec_gt, tvec_gt = create_ground_truth_pose()

    # Project titik ke 2D (ground truth)
    points_2d = project_points(points_3d, rvec_gt, tvec_gt, K)
    # Tambahkan noise
    points_2d_noisy = add_noise(points_2d, NOISE_STD)

    # Estimasi pose dengan solvePnP
    success, rvec_est, tvec_est = cv2.solvePnP(points_3d, points_2d_noisy, K, None)

    # Project ulang menggunakan pose estimasi
    points_2d_est = project_points(points_3d, rvec_est, tvec_est, K)

    # Hitung reprojection error
    errors = np.linalg.norm(points_2d_est - points_2d_noisy, axis=1)
    # Hitung mean error
    mean_error = np.mean(errors)

    # Print hasil
    print(f"SolvePnP Success: {success}")
    # Print rvec
    print(f"rvec (GT):  {rvec_gt.ravel()}")
    # Print rvec
    print(f"rvec (Est): {rvec_est.ravel()}")
    # Print tvec
    print(f"tvec (GT):  {tvec_gt.ravel()}")
    # Print tvec
    print(f"tvec (Est): {tvec_est.ravel()}")
    # Print error
    print(f"Mean Reprojection Error: {mean_error:.3f} px")

    # Buat visualisasi perbandingan
    plt.figure(figsize=(7, 5))
    # Plot noisy observations
    plt.scatter(points_2d_noisy[:, 0], points_2d_noisy[:, 1], c="red", label="Noisy Observations")
    # Plot reprojection estimasi
    plt.scatter(points_2d_est[:, 0], points_2d_est[:, 1], c="green", marker="x", label="Reprojection")
    # Tambah judul
    plt.title("PnP: Observasi vs Reprojection")
    # Balik sumbu y agar sesuai koordinat image
    plt.gca().invert_yaxis()
    # Tambah legend
    plt.legend()
    # Tambah grid
    plt.grid(True, alpha=0.3)

    # Simpan output
    output_path = output_dir / "09_pnp_pose.png"
    # Save figure
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    # Close figure
    plt.close()

    # Simpan ringkasan ke file
    report_path = output_dir / "09_pnp_pose_report.txt"
    # Buka file untuk ditulis
    with open(report_path, "w", encoding="utf-8") as f:
        # Tulis header
        f.write("LAPORAN PNP POSE ESTIMATION\n")
        # Tulis success
        f.write(f"SolvePnP Success: {success}\n")
        # Tulis rvec
        f.write(f"rvec (GT):  {rvec_gt.ravel()}\n")
        # Tulis rvec
        f.write(f"rvec (Est): {rvec_est.ravel()}\n")
        # Tulis tvec
        f.write(f"tvec (GT):  {tvec_gt.ravel()}\n")
        # Tulis tvec
        f.write(f"tvec (Est): {tvec_est.ravel()}\n")
        # Tulis error
        f.write(f"Mean Reprojection Error: {mean_error:.3f} px\n")

    # Print output
    print(f"Output disimpan di: {output_path}")
    # Print selesai
    print("\n✓ Program selesai!")


# Entry point
if __name__ == "__main__":
    # Panggil fungsi main
    main()
