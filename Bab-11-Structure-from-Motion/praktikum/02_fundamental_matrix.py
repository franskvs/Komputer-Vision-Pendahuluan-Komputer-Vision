#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 02_fundamental_matrix.py

Deskripsi:
    Program ini mendemonstrasikan estimasi Fundamental Matrix untuk
    menemukan hubungan geometris antara dua gambar dari sudut pandang berbeda.
    Fundamental Matrix menggambarkan constraint epipolar tanpa memerlukan
    kalibrasi kamera.

Tujuan:
    1. Memahami konsep Fundamental Matrix
    2. Memahami epipolar geometry
    3. Memahami penggunaan RANSAC untuk robust estimation
    4. Memvisualisasikan epipolar lines

Teori:
    Untuk titik x di gambar 1 dan titik korespondensi x' di gambar 2:
    x'^T * F * x = 0
    
    Epipolar line di gambar 2: l' = F * x
    Epipolar line di gambar 1: l = F^T * x'

Aplikasi Dunia Nyata:
    - Stereo vision untuk robot
    - Rekonstruksi 3D
    - Visual odometry
    - Camera pose estimation

Author: Praktikum Computer Vision
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# VARIABEL KONFIGURASI - UBAH NILAI INI UNTUK EKSPERIMEN
# ============================================================================

# Metode estimasi Fundamental Matrix
# cv2.FM_RANSAC: Random Sample Consensus (robust terhadap outliers)
# cv2.FM_LMEDS: Least Median of Squares (alternatif robust)
# cv2.FM_7POINT: 7-point algorithm (memerlukan exactly 7 matches)
# cv2.FM_8POINT: 8-point algorithm (normalized)
ESTIMATION_METHOD = cv2.FM_RANSAC

# Threshold untuk RANSAC (dalam pixel)
# Jarak maksimum titik ke epipolar line agar dianggap inlier
# Nilai kecil = lebih ketat, Nilai besar = lebih longgar
# Range yang disarankan: 1.0 - 5.0
RANSAC_THRESHOLD = 3.0

# Confidence level untuk RANSAC
# Probabilitas bahwa hasil benar
# Range: 0.9 - 0.999
RANSAC_CONFIDENCE = 0.99

# Jumlah epipolar lines yang divisualisasikan
NUM_EPIPOLAR_LINES = 15

# Feature detector untuk mencari korespondensi
DETECTOR_TYPE = 'SIFT'
MAX_FEATURES = 3000
RATIO_THRESHOLD = 0.7

# ============================================================================
# FUNGSI UTILITAS
# ============================================================================

def detect_and_match_features(img1, img2, detector_type='SIFT', 
                              max_features=3000, ratio_threshold=0.7):
    """
    Mendeteksi dan mencocokkan fitur antara dua gambar.
    
    Returns:
        pts1: Koordinat titik di gambar 1 (Nx2)
        pts2: Koordinat titik korespondensi di gambar 2 (Nx2)
    """
    # Buat detector
    if detector_type == 'SIFT':
        detector = cv2.SIFT_create(nfeatures=max_features)
    elif detector_type == 'ORB':
        detector = cv2.ORB_create(nfeatures=max_features)
    else:
        detector = cv2.AKAZE_create()
    
    # Konversi ke grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Deteksi keypoints dan descriptors
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    # Matching
    if detector_type in ['ORB', 'AKAZE', 'BRISK']:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    else:
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        matcher = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = matcher.knnMatch(desc1, desc2, k=2)
    
    # Ratio test
    good_matches = []
    for m_pair in matches:
        if len(m_pair) == 2:
            m, n = m_pair
            if m.distance < ratio_threshold * n.distance:
                good_matches.append(m)
    
    # Ekstrak koordinat
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])
    
    return pts1, pts2, kp1, kp2, good_matches


def compute_fundamental_matrix(pts1, pts2, method=cv2.FM_RANSAC, 
                               threshold=3.0, confidence=0.99):
    """
    Menghitung Fundamental Matrix dari korespondensi titik.
    
    Parameters:
        pts1, pts2: Koordinat titik korespondensi (Nx2)
        method: Metode estimasi
        threshold: Threshold RANSAC
        confidence: Confidence level
        
    Returns:
        F: Fundamental Matrix (3x3)
        mask: Inlier mask
    """
    F, mask = cv2.findFundamentalMat(pts1, pts2, method, threshold, confidence)
    
    return F, mask


def compute_epipolar_line(F, point, image_shape, source='left'):
    """
    Menghitung epipolar line dari sebuah titik.
    
    Parameters:
        F: Fundamental Matrix
        point: Titik (x, y)
        image_shape: Shape gambar tujuan
        source: 'left' jika titik dari gambar kiri, 'right' jika dari kanan
        
    Returns:
        line_start, line_end: Koordinat untuk menggambar garis
    """
    pt_homogeneous = np.array([point[0], point[1], 1.0])
    
    if source == 'left':
        # Epipolar line di gambar kanan: l' = F * x
        line = F @ pt_homogeneous
    else:
        # Epipolar line di gambar kiri: l = F^T * x'
        line = F.T @ pt_homogeneous
    
    # line = [a, b, c] dimana ax + by + c = 0
    a, b, c = line
    
    # Hitung titik di edge gambar
    h, w = image_shape[:2]
    
    # Titik di x=0 dan x=w
    if abs(b) > 1e-6:
        y_at_0 = -c / b
        y_at_w = -(a * w + c) / b
        
        points = []
        if 0 <= y_at_0 <= h:
            points.append((0, int(y_at_0)))
        if 0 <= y_at_w <= h:
            points.append((w, int(y_at_w)))
        
        # Titik di y=0 dan y=h
        if abs(a) > 1e-6:
            x_at_0 = -c / a
            x_at_h = -(b * h + c) / a
            if 0 <= x_at_0 <= w:
                points.append((int(x_at_0), 0))
            if 0 <= x_at_h <= w:
                points.append((int(x_at_h), h))
        
        if len(points) >= 2:
            return points[0], points[1]
    
    return None, None


def verify_fundamental_matrix(F, pts1, pts2):
    """
    Memverifikasi Fundamental Matrix dengan menghitung epipolar error.
    
    Error = x'^T * F * x (seharusnya = 0 untuk korespondensi sempurna)
    """
    errors = []
    for pt1, pt2 in zip(pts1, pts2):
        pt1_h = np.array([pt1[0], pt1[1], 1.0])
        pt2_h = np.array([pt2[0], pt2[1], 1.0])
        
        # Hitung error: x'^T * F * x
        error = abs(pt2_h @ F @ pt1_h)
        errors.append(error)
    
    return np.array(errors)


def visualize_epipolar_lines(img1, img2, pts1, pts2, F, num_lines, output_path):
    """
    Memvisualisasikan epipolar lines pada kedua gambar.
    """
    # Buat salinan gambar
    img1_vis = img1.copy()
    img2_vis = img2.copy()
    
    # Pilih subset titik secara acak
    n_pts = min(num_lines, len(pts1))
    indices = np.random.choice(len(pts1), n_pts, replace=False)
    
    # Warna untuk setiap pasangan
    colors = plt.cm.rainbow(np.linspace(0, 1, n_pts))
    colors = (colors[:, :3] * 255).astype(int)
    
    for idx, i in enumerate(indices):
        color = tuple(map(int, colors[idx]))
        pt1 = pts1[i]
        pt2 = pts2[i]
        
        # Gambar titik
        cv2.circle(img1_vis, tuple(map(int, pt1)), 5, color, -1)
        cv2.circle(img2_vis, tuple(map(int, pt2)), 5, color, -1)
        
        # Gambar epipolar line di gambar 2 (dari titik di gambar 1)
        line_start, line_end = compute_epipolar_line(F, pt1, img2.shape, 'left')
        if line_start is not None:
            cv2.line(img2_vis, line_start, line_end, color, 1)
        
        # Gambar epipolar line di gambar 1 (dari titik di gambar 2)
        line_start, line_end = compute_epipolar_line(F, pt2, img1.shape, 'right')
        if line_start is not None:
            cv2.line(img1_vis, line_start, line_end, color, 1)
    
    # Gabungkan gambar
    combined = np.hstack([img1_vis, img2_vis])
    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(combined_rgb)
    plt.title(f'Epipolar Lines ({num_lines} pasang titik)\n'
              'Titik berwarna = korespondensi, Garis = epipolar line', fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("ESTIMASI FUNDAMENTAL MATRIX DAN VISUALISASI EPIPOLAR GEOMETRY")
    print("="*70)
    print(f"\nKonfigurasi:")
    
    # Map method to name
    method_names = {
        cv2.FM_RANSAC: 'RANSAC',
        cv2.FM_LMEDS: 'LMEDS', 
        cv2.FM_7POINT: '7POINT',
        cv2.FM_8POINT: '8POINT'
    }
    method_name = method_names.get(ESTIMATION_METHOD, 'UNKNOWN')
    
    print(f"  - Metode Estimasi: {method_name}")
    print(f"  - RANSAC Threshold: {RANSAC_THRESHOLD} pixel")
    print(f"  - Confidence: {RANSAC_CONFIDENCE}")
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent.resolve()
    data_dir = script_dir / "data" / "images"
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Load gambar
    img1_path = data_dir / "building1.jpg"
    img2_path = data_dir / "building2.jpg"
    
    if not img1_path.exists() or not img2_path.exists():
        print("Gambar sampel tidak ditemukan. Membuat gambar dummy...")
        
        # Buat gambar dummy dengan checkerboard pattern
        img1 = np.zeros((480, 640, 3), dtype=np.uint8)
        img2 = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Checkerboard pattern
        block_size = 40
        for i in range(0, 480, block_size):
            for j in range(0, 640, block_size):
                if (i // block_size + j // block_size) % 2 == 0:
                    img1[i:i+block_size, j:j+block_size] = [200, 200, 200]
                    # Sedikit offset untuk gambar 2
                    i2, j2 = max(0, i-5), max(0, j+10)
                    img2[i2:min(480, i2+block_size), j2:min(640, j2+block_size)] = [200, 200, 200]
        
        # Tambahkan fitur tambahan
        for _ in range(30):
            x, y = np.random.randint(50, 590), np.random.randint(50, 430)
            cv2.circle(img1, (x, y), 10, (255, 255, 255), -1)
            cv2.circle(img2, (x+15, y-5), 10, (255, 255, 255), -1)
    else:
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
    
    if img1 is None or img2 is None:
        print("Error: Tidak dapat membaca gambar!")
        return
    
    print(f"Ukuran gambar: {img1.shape}")
    
    # Step 1: Detect dan match features
    print("\n[1] Mendeteksi dan mencocokkan fitur...")
    pts1, pts2, kp1, kp2, matches = detect_and_match_features(
        img1, img2, DETECTOR_TYPE, MAX_FEATURES, RATIO_THRESHOLD
    )
    print(f"    Jumlah korespondensi: {len(pts1)}")
    
    if len(pts1) < 8:
        print("Error: Tidak cukup korespondensi untuk menghitung Fundamental Matrix!")
        return
    
    # Step 2: Compute Fundamental Matrix
    print("\n[2] Menghitung Fundamental Matrix...")
    F, mask = compute_fundamental_matrix(
        pts1, pts2, ESTIMATION_METHOD, RANSAC_THRESHOLD, RANSAC_CONFIDENCE
    )
    
    # Filter inliers
    mask = mask.ravel().astype(bool)
    pts1_inliers = pts1[mask]
    pts2_inliers = pts2[mask]
    
    print(f"    Inliers: {mask.sum()} dari {len(mask)}")
    print(f"    Inlier ratio: {mask.sum()/len(mask)*100:.1f}%")
    
    # Step 3: Tampilkan Fundamental Matrix
    print("\n[3] Fundamental Matrix F:")
    print(F)
    
    # Verifikasi rank (seharusnya rank 2)
    rank = np.linalg.matrix_rank(F)
    print(f"\n    Rank F: {rank} (seharusnya 2)")
    
    # Step 4: Verifikasi epipolar constraint
    print("\n[4] Memverifikasi epipolar constraint...")
    errors = verify_fundamental_matrix(F, pts1_inliers, pts2_inliers)
    print(f"    Mean epipolar error: {errors.mean():.6f}")
    print(f"    Max epipolar error: {errors.max():.6f}")
    print(f"    Std epipolar error: {errors.std():.6f}")
    
    # Step 5: Visualisasi
    print("\n[5] Memvisualisasikan epipolar lines...")
    visualize_epipolar_lines(
        img1, img2, pts1_inliers, pts2_inliers, F, NUM_EPIPOLAR_LINES,
        output_dir / "02_epipolar_lines.png"
    )
    
    # Step 6: Plot distribusi error
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.hist(errors, bins=50, edgecolor='black')
    plt.xlabel('Epipolar Error')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Epipolar Error')
    
    plt.subplot(1, 2, 2)
    plt.plot(sorted(errors), 'b-')
    plt.xlabel('Index (sorted)')
    plt.ylabel('Epipolar Error')
    plt.title('Sorted Epipolar Errors')
    
    plt.tight_layout()
    plt.savefig(output_dir / "02_epipolar_error_dist.png", dpi=150)
    plt.close()
    print(f"Hasil disimpan: {output_dir / '02_epipolar_error_dist.png'}")
    
    # Ringkasan
    print("\n" + "="*50)
    print("RINGKASAN")
    print("="*50)
    print(f"Total korespondensi: {len(pts1)}")
    print(f"Inliers setelah RANSAC: {len(pts1_inliers)}")
    print(f"Mean epipolar error: {errors.mean():.6f}")
    print(f"Fundamental Matrix berhasil diestimasi!")
    print("\n✓ Program selesai!")


if __name__ == "__main__":
    main()
