#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 08_vanishing_points_calibration.py

Deskripsi:
    Program ini mendemonstrasikan kalibrasi kamera sederhana menggunakan
    vanishing points (titik hilang) dari dua arah ortogonal pada sebuah
    scene sintetis. Ini mengimplementasikan konsep Section 11.1.1 (Vanishing Points)
    pada PDF, termasuk estimasi focal length dengan asumsi principal point di tengah.

Tujuan:
    1. Memahami konsep vanishing points
    2. Memahami cara estimasi focal length dari dua vanishing points ortogonal
    3. Memvisualisasikan garis paralel dan titik hilang

Aplikasi Dunia Nyata:
    - Kalibrasi kamera dari foto bangunan
    - Single-view metrology (mengukur dimensi dari 1 foto)
    - Rekonstruksi arsitektur

Author: Praktikum Computer Vision
"""

# Import modul untuk operasi file dan path
from pathlib import Path
# Import numpy untuk operasi numerik
import numpy as np
# Import OpenCV untuk menggambar
import cv2
# Import matplotlib untuk visualisasi
import matplotlib.pyplot as plt

# =============================================================================
# KONFIGURASI
# =============================================================================

# Lebar gambar sintetis
IMAGE_WIDTH = 800
# Tinggi gambar sintetis
IMAGE_HEIGHT = 600
# Warna background (BGR)
BACKGROUND_COLOR = (30, 30, 30)
# Warna garis (BGR)
LINE_COLOR = (200, 200, 200)
# Warna titik hilang (BGR)
VP_COLOR = (0, 0, 255)
# Jumlah garis per arah
LINES_PER_DIRECTION = 6

# =============================================================================
# FUNGSI UTILITAS
# =============================================================================

# Fungsi untuk membuat titik acak dalam rentang gambar
def random_point_in_image(margin=50):
    # Buat koordinat x acak dalam range
    x = np.random.randint(margin, IMAGE_WIDTH - margin)
    # Buat koordinat y acak dalam range
    y = np.random.randint(margin, IMAGE_HEIGHT - margin)
    # Kembalikan sebagai tuple
    return (int(x), int(y))


# Fungsi untuk membuat garis yang mengarah ke vanishing point tertentu
def generate_lines_towards_vp(vp, count, jitter=40):
    # Inisialisasi list untuk menyimpan garis
    lines = []
    # Loop sebanyak jumlah garis
    for _ in range(count):
        # Buat titik awal acak di area gambar
        start = random_point_in_image(margin=80)
        # Tambahkan jitter pada arah garis
        offset = (np.random.randint(-jitter, jitter), np.random.randint(-jitter, jitter))
        # Buat titik target (arah ke VP + jitter)
        target = (vp[0] + offset[0], vp[1] + offset[1])
        # Simpan pasangan titik sebagai garis
        lines.append((start, target))
    # Kembalikan list garis
    return lines


# Fungsi untuk menghitung persamaan garis ax + by + c = 0 dari dua titik
def line_from_points(p1, p2):
    # Ambil koordinat titik pertama
    x1, y1 = p1
    # Ambil koordinat titik kedua
    x2, y2 = p2
    # Hitung koefisien a
    a = y1 - y2
    # Hitung koefisien b
    b = x2 - x1
    # Hitung koefisien c
    c = x1 * y2 - x2 * y1
    # Kembalikan sebagai array
    return np.array([a, b, c], dtype=np.float64)


# Fungsi untuk menghitung intersection dua garis
def intersect_lines(l1, l2):
    # Hitung cross product sebagai titik perpotongan
    p = np.cross(l1, l2)
    # Cek jika perpotongan di tak hingga
    if abs(p[2]) < 1e-9:
        # Kembalikan None jika tidak valid
        return None
    # Normalisasi ke koordinat kartesian
    x = p[0] / p[2]
    # Normalisasi ke koordinat kartesian
    y = p[1] / p[2]
    # Kembalikan titik perpotongan
    return (float(x), float(y))


# Fungsi untuk estimasi vanishing point dari sekumpulan garis
def estimate_vanishing_point(lines):
    # Inisialisasi list intersection points
    intersections = []
    # Loop semua pasangan garis
    for i in range(len(lines)):
        # Loop pasangan setelah i
        for j in range(i + 1, len(lines)):
            # Hitung persamaan garis ke-i
            l1 = line_from_points(lines[i][0], lines[i][1])
            # Hitung persamaan garis ke-j
            l2 = line_from_points(lines[j][0], lines[j][1])
            # Cari titik perpotongan
            pt = intersect_lines(l1, l2)
            # Jika valid, simpan
            if pt is not None:
                intersections.append(pt)
    # Konversi ke numpy array
    intersections = np.array(intersections, dtype=np.float64)
    # Ambil rata-rata sebagai estimasi VP
    vp = intersections.mean(axis=0)
    # Kembalikan hasil estimasi
    return vp


# Fungsi untuk menghitung focal length dari dua vanishing points ortogonal
def estimate_focal_length(vp1, vp2, principal_point):
    # Ubah vp ke koordinat relatif terhadap principal point
    v1 = np.array(vp1) - np.array(principal_point)
    # Ubah vp ke koordinat relatif terhadap principal point
    v2 = np.array(vp2) - np.array(principal_point)
    # Hitung dot product
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    # Jika dot > 0, focal length menjadi imaginer (tidak valid)
    if dot >= 0:
        # Kembalikan None jika tidak valid
        return None
    # Hitung f^2 = -dot
    f_sq = -dot
    # Hitung f
    f = np.sqrt(f_sq)
    # Kembalikan f
    return float(f)


# =============================================================================
# MAIN PROGRAM
# =============================================================================

# Fungsi utama
def main():
    # Set seed untuk reproducibility
    np.random.seed(42)

    # Tampilkan judul program
    print("=" * 70)
    # Tampilkan judul program
    print("KALIBRASI KAMERA DENGAN VANISHING POINTS")
    # Tampilkan judul program
    print("=" * 70)

    # Setup path output
    script_dir = Path(__file__).parent.resolve()
    # Setup path output directory
    output_dir = script_dir / "output"
    # Buat folder output jika belum ada
    output_dir.mkdir(exist_ok=True)

    # Buat canvas kosong
    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
    # Isi background
    image[:] = BACKGROUND_COLOR

    # Definisikan vanishing points ground truth
    vp1_true = (-200, 300)   # Vanishing point horizontal kiri
    # Definisikan vanishing points ground truth
    vp2_true = (1000, 250)   # Vanishing point horizontal kanan

    # Generate garis menuju VP1
    lines_vp1 = generate_lines_towards_vp(vp1_true, LINES_PER_DIRECTION)
    # Generate garis menuju VP2
    lines_vp2 = generate_lines_towards_vp(vp2_true, LINES_PER_DIRECTION)

    # Gambar garis untuk arah pertama
    for p1, p2 in lines_vp1:
        # Gambar garis di canvas
        cv2.line(image, p1, p2, LINE_COLOR, 2)

    # Gambar garis untuk arah kedua
    for p1, p2 in lines_vp2:
        # Gambar garis di canvas
        cv2.line(image, p1, p2, LINE_COLOR, 2)

    # Estimasi vanishing point dari garis pertama
    vp1_est = estimate_vanishing_point(lines_vp1)
    # Estimasi vanishing point dari garis kedua
    vp2_est = estimate_vanishing_point(lines_vp2)

    # Definisikan principal point (tengah gambar)
    principal_point = (IMAGE_WIDTH / 2.0, IMAGE_HEIGHT / 2.0)
    # Estimasi focal length
    focal_est = estimate_focal_length(vp1_est, vp2_est, principal_point)

    # Gambar VP estimasi
    cv2.circle(image, (int(vp1_est[0]), int(vp1_est[1])), 8, VP_COLOR, -1)
    # Gambar VP estimasi
    cv2.circle(image, (int(vp2_est[0]), int(vp2_est[1])), 8, VP_COLOR, -1)

    # Gambar principal point
    cv2.circle(image, (int(principal_point[0]), int(principal_point[1])), 6, (0, 255, 0), -1)

    # Konversi BGR ke RGB untuk matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Buat figure untuk plotting
    plt.figure(figsize=(10, 7))
    # Tampilkan gambar
    plt.imshow(image_rgb)
    # Tampilkan judul
    plt.title("Vanishing Points dan Estimasi Focal Length")
    # Hilangkan axis
    plt.axis("off")

    # Simpan hasil visualisasi
    output_path = output_dir / "08_vanishing_points.png"
    # Save figure
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    # Close figure
    plt.close()

    # Print hasil estimasi
    print(f"VP1 Estimasi: {vp1_est}")
    # Print hasil estimasi
    print(f"VP2 Estimasi: {vp2_est}")
    # Print principal point
    print(f"Principal Point: {principal_point}")
    # Print focal length
    print(f"Estimasi Focal Length: {focal_est:.2f} px")
    # Print output path
    print(f"Output disimpan di: {output_path}")

    # Simpan ringkasan ke file teks
    report_path = output_dir / "08_vanishing_points_report.txt"
    # Buka file untuk ditulis
    with open(report_path, "w", encoding="utf-8") as f:
        # Tulis header
        f.write("LAPORAN VANISHING POINTS\n")
        # Tulis VP1
        f.write(f"VP1 Estimasi: {vp1_est}\n")
        # Tulis VP2
        f.write(f"VP2 Estimasi: {vp2_est}\n")
        # Tulis principal point
        f.write(f"Principal Point: {principal_point}\n")
        # Tulis focal length
        f.write(f"Estimasi Focal Length: {focal_est:.2f} px\n")

    # Tampilkan selesai
    print("\n✓ Program selesai!")


# Entry point
if __name__ == "__main__":
    # Panggil fungsi main
    main()
