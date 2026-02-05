#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 11_tomasi_kanade_factorization.py

Deskripsi:
    Program ini mendemonstrasikan factorization method Tomasi-Kanade (Section 11.4.1)
    untuk rekonstruksi 3D dari motion under orthographic camera model.
    Menggunakan data sintetis: titik 3D pada sphere, diproyeksikan dari beberapa
    frame rotasi, lalu direkonstruksi menggunakan SVD.

Tujuan:
    1. Memahami factorization method
    2. Merekonstruksi 3D dari multi-frame 2D tracks
    3. Visualisasi point cloud hasil rekonstruksi

Aplikasi Dunia Nyata:
    - Motion capture sederhana
    - Rekonstruksi objek berotasi
    - Inisialisasi bundle adjustment

Author: Praktikum Computer Vision
"""

# Import path
from pathlib import Path
# Import numpy
import numpy as np
# Import matplotlib
import matplotlib.pyplot as plt

# =============================================================================
# KONFIGURASI
# =============================================================================

# Jumlah titik 3D
NUM_POINTS = 60
# Jumlah frame
NUM_FRAMES = 10
# Radius sphere
SPHERE_RADIUS = 1.0

# =============================================================================
# FUNGSI UTILITAS
# =============================================================================

# Fungsi untuk membuat titik 3D di sphere

def generate_sphere_points(num_points, radius):
    # Buat random angles
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    # Buat random phi
    phi = np.random.uniform(0, np.pi, num_points)
    # Hitung x
    x = radius * np.sin(phi) * np.cos(theta)
    # Hitung y
    y = radius * np.sin(phi) * np.sin(theta)
    # Hitung z
    z = radius * np.cos(phi)
    # Stack points
    points = np.stack([x, y, z], axis=1)
    # Kembalikan
    return points


# Fungsi untuk rotasi titik pada setiap frame

def rotate_points(points, angle):
    # Buat matrix rotasi sumbu Y
    R = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)],
    ])
    # Rotasikan points
    return points @ R.T


# Fungsi untuk projection orthographic

def orthographic_project(points):
    # Ambil x dan y saja
    return points[:, :2]


# =============================================================================
# MAIN PROGRAM
# =============================================================================

# Fungsi utama

def main():
    # Set seed
    np.random.seed(42)

    # Print header
    print("=" * 70)
    # Print header
    print("TOMASI-KANADE FACTORIZATION")
    # Print header
    print("=" * 70)

    # Setup output dir
    script_dir = Path(__file__).parent.resolve()
    # Setup output dir
    output_dir = script_dir / "output"
    # Buat output dir
    output_dir.mkdir(exist_ok=True)

    # Generate titik 3D
    points_3d = generate_sphere_points(NUM_POINTS, SPHERE_RADIUS)

    # Buat measurement matrix W (2F x P)
    W = []

    # Loop frame
    for i in range(NUM_FRAMES):
        # Hitung angle rotasi
        angle = 2 * np.pi * i / NUM_FRAMES
        # Rotasikan points
        rotated = rotate_points(points_3d, angle)
        # Project orthographic
        projected = orthographic_project(rotated)
        # Append x dan y
        W.append(projected[:, 0])
        W.append(projected[:, 1])

    # Stack menjadi matrix
    W = np.array(W)

    # Subtract mean (centering)
    W_mean = W.mean(axis=1, keepdims=True)
    W_centered = W - W_mean

    # SVD factorization
    U, S, Vt = np.linalg.svd(W_centered)

    # Ambil rank-3 approximation
    U3 = U[:, :3]
    S3 = np.diag(S[:3])
    V3 = Vt[:3, :]

    # Rekonstruksi motion dan structure
    M = U3 @ np.sqrt(S3)
    S_recon = np.sqrt(S3) @ V3

    # S_recon (3 x P) -> transpose
    points_recon = S_recon.T

    # Print ringkasan
    print(f"Measurement matrix shape: {W.shape}")
    print(f"Reconstructed points: {points_recon.shape}")

    # Plot hasil
    fig = plt.figure(figsize=(10, 4))

    # Plot ground truth
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.scatter(points_3d[:, 0], points_3d[:, 1], points_3d[:, 2], c="blue", s=10)
    ax1.set_title("Ground Truth 3D")

    # Plot reconstruction
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.scatter(points_recon[:, 0], points_recon[:, 1], points_recon[:, 2], c="red", s=10)
    ax2.set_title("Reconstructed 3D")

    # Simpan output
    output_path = output_dir / "11_factorization.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    # Simpan report
    report_path = output_dir / "11_factorization_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("LAPORAN TOMASI-KANADE FACTORIZATION\n")
        f.write(f"Measurement matrix shape: {W.shape}\n")
        f.write(f"Reconstructed points: {points_recon.shape}\n")

    # Print output
    print(f"Output disimpan di: {output_path}")
    # Print selesai
    print("\n✓ Program selesai!")


# Entry point
if __name__ == "__main__":
    main()
