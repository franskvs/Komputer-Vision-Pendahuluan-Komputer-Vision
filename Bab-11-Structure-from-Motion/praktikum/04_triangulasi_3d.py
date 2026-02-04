#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 04_triangulasi_3d.py

Deskripsi:
    Program ini mendemonstrasikan triangulasi untuk menghitung posisi 3D
    titik-titik dari proyeksi 2D-nya di beberapa gambar. Triangulasi adalah
    langkah kunci dalam Structure from Motion untuk merekonstruksi dunia 3D.

Tujuan:
    1. Memahami prinsip triangulasi dari multiple views
    2. Mengimplementasikan metode DLT (Direct Linear Transform)
    3. Memvisualisasikan point cloud hasil triangulasi
    4. Mengevaluasi akurasi dengan reprojection error

Teori:
    Untuk titik 3D X yang diproyeksikan ke titik 2D x di gambar:
    x = P * X
    
    dimana P adalah projection matrix (3x4).
    
    Dari dua view, kita dapat menghitung X dengan memecahkan sistem linear:
    [x1 × (P1 * X)] = 0
    [x2 × (P2 * X)] = 0

Aplikasi Dunia Nyata:
    - 3D scanning dengan smartphone
    - Fotogrametri untuk pemetaan
    - Motion capture untuk animasi
    - Rekonstruksi scene untuk VR

Author: Praktikum Computer Vision
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# ============================================================================
# VARIABEL KONFIGURASI - UBAH NILAI INI UNTUK EKSPERIMEN
# ============================================================================

# Parameter kamera
FOCAL_LENGTH = 800
PRINCIPAL_POINT = (320, 240)

# Threshold reprojection error untuk filtering outliers (pixel)
# Titik dengan error lebih besar akan dibuang
REPROJ_ERROR_THRESHOLD = 5.0

# Filter depth (titik terlalu dekat atau terlalu jauh)
MIN_DEPTH = 0.1  # meter (dalam unit normalized)
MAX_DEPTH = 100.0

# Feature detection
DETECTOR_TYPE = 'SIFT'
MAX_FEATURES = 3000
RATIO_THRESHOLD = 0.7

# Visualisasi
POINT_SIZE = 2
SHOW_CAMERA_FRUSTUM = True

# ============================================================================
# FUNGSI UTILITAS
# ============================================================================

def get_camera_matrix(focal_length, principal_point):
    """Membuat Camera Matrix K."""
    fx = fy = focal_length
    cx, cy = principal_point
    K = np.array([
        [fx, 0,  cx],
        [0,  fy, cy],
        [0,  0,  1]
    ], dtype=np.float64)
    return K


def detect_and_match_features(img1, img2, detector_type='SIFT',
                              max_features=3000, ratio_threshold=0.7):
    """Mendeteksi dan mencocokkan fitur antara dua gambar."""
    if detector_type == 'SIFT':
        detector = cv2.SIFT_create(nfeatures=max_features)
    elif detector_type == 'ORB':
        detector = cv2.ORB_create(nfeatures=max_features)
    else:
        detector = cv2.AKAZE_create()
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    if detector_type in ['ORB', 'AKAZE']:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    else:
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        matcher = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = matcher.knnMatch(desc1, desc2, k=2)
    
    good_matches = []
    for m_pair in matches:
        if len(m_pair) == 2:
            m, n = m_pair
            if m.distance < ratio_threshold * n.distance:
                good_matches.append(m)
    
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])
    
    return pts1, pts2, kp1, kp2, good_matches


def estimate_camera_poses(pts1, pts2, K):
    """
    Mengestimasi pose relatif antara dua kamera.
    
    Returns:
        P1: Projection matrix kamera 1 (3x4)
        P2: Projection matrix kamera 2 (3x4)
        mask: Inlier mask
    """
    # Hitung Essential Matrix
    E, mask = cv2.findEssentialMat(pts1, pts2, K, cv2.RANSAC, 0.999, 1.0)
    
    # Recover pose
    _, R, t, pose_mask = cv2.recoverPose(E, pts1, pts2, K)
    
    # Projection matrix kamera 1: P1 = K * [I | 0]
    P1 = K @ np.hstack([np.eye(3), np.zeros((3, 1))])
    
    # Projection matrix kamera 2: P2 = K * [R | t]
    P2 = K @ np.hstack([R, t])
    
    combined_mask = mask.ravel() & pose_mask.ravel()
    
    return P1, P2, R, t, combined_mask.astype(bool)


def triangulate_points_cv(pts1, pts2, P1, P2):
    """
    Triangulasi menggunakan fungsi OpenCV.
    
    Returns:
        points_3d: Array titik 3D (Nx3)
    """
    # OpenCV mengharapkan 2xN array
    pts1_t = pts1.T
    pts2_t = pts2.T
    
    # Triangulasi menghasilkan homogeneous coordinates (4xN)
    points_4d = cv2.triangulatePoints(P1, P2, pts1_t, pts2_t)
    
    # Konversi ke koordinat 3D (normalisasi dengan w)
    points_3d = (points_4d[:3] / points_4d[3]).T
    
    return points_3d


def triangulate_point_dlt(pt1, pt2, P1, P2):
    """
    Triangulasi satu titik menggunakan Direct Linear Transform (DLT).
    
    Untuk setiap view, kita dapat membuat 2 persamaan dari:
    x * (P[2] @ X) = P[0] @ X
    y * (P[2] @ X) = P[1] @ X
    
    yang dapat ditulis sebagai A @ X = 0
    """
    A = np.array([
        pt1[0] * P1[2] - P1[0],
        pt1[1] * P1[2] - P1[1],
        pt2[0] * P2[2] - P2[0],
        pt2[1] * P2[2] - P2[1]
    ])
    
    # SVD untuk mendapatkan null space
    _, _, Vt = np.linalg.svd(A)
    X = Vt[-1]
    
    # Normalisasi homogeneous coordinate
    X = X[:3] / X[3]
    
    return X


def compute_reprojection_error(pts1, pts2, points_3d, P1, P2):
    """
    Menghitung reprojection error untuk setiap titik.
    
    Error = jarak antara titik asli dengan proyeksi ulang titik 3D.
    """
    errors1 = []
    errors2 = []
    
    for i, pt3d in enumerate(points_3d):
        # Proyeksikan kembali ke gambar 1
        pt_h = np.append(pt3d, 1)
        proj1 = P1 @ pt_h
        proj1 = proj1[:2] / proj1[2]
        err1 = np.linalg.norm(pts1[i] - proj1)
        errors1.append(err1)
        
        # Proyeksikan kembali ke gambar 2
        proj2 = P2 @ pt_h
        proj2 = proj2[:2] / proj2[2]
        err2 = np.linalg.norm(pts2[i] - proj2)
        errors2.append(err2)
    
    return np.array(errors1), np.array(errors2)


def filter_points(points_3d, pts1, pts2, errors1, errors2, 
                  error_threshold, min_depth, max_depth, R, t):
    """
    Filter titik berdasarkan:
    1. Reprojection error
    2. Depth (harus positif dan dalam range)
    3. Di depan kedua kamera
    """
    mask = np.ones(len(points_3d), dtype=bool)
    
    # Filter by reprojection error
    mask &= (errors1 < error_threshold) & (errors2 < error_threshold)
    
    # Filter by depth in camera 1 (z > 0)
    mask &= points_3d[:, 2] > min_depth
    mask &= points_3d[:, 2] < max_depth
    
    # Filter by depth in camera 2
    points_cam2 = (R @ points_3d.T).T + t.T
    mask &= points_cam2[:, 2] > min_depth
    
    return mask


def visualize_3d_points(points_3d, R, t, output_path, title="3D Point Cloud"):
    """
    Memvisualisasikan point cloud hasil triangulasi beserta posisi kamera.
    """
    fig = plt.figure(figsize=(14, 6))
    
    # 3D scatter plot
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Plot points
    ax1.scatter(points_3d[:, 0], points_3d[:, 1], points_3d[:, 2],
               c=points_3d[:, 2], cmap='viridis', s=POINT_SIZE, alpha=0.6)
    
    if SHOW_CAMERA_FRUSTUM:
        # Camera 1 at origin
        ax1.scatter(0, 0, 0, c='blue', s=100, marker='^', label='Camera 1')
        
        # Camera 2
        cam2_pos = -R.T @ t
        ax1.scatter(cam2_pos[0], cam2_pos[1], cam2_pos[2], 
                   c='red', s=100, marker='^', label='Camera 2')
        
        # Draw line between cameras
        ax1.plot([0, cam2_pos[0,0]], [0, cam2_pos[1,0]], [0, cam2_pos[2,0]], 
                'k--', alpha=0.5)
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z (Depth)')
    ax1.set_title(f'{title}\n{len(points_3d)} points')
    ax1.legend()
    
    # 2D projections
    ax2 = fig.add_subplot(122)
    
    # Top-down view (X vs Z)
    scatter = ax2.scatter(points_3d[:, 0], points_3d[:, 2],
                         c=points_3d[:, 1], cmap='viridis', s=POINT_SIZE, alpha=0.6)
    plt.colorbar(scatter, ax=ax2, label='Y coordinate')
    
    if SHOW_CAMERA_FRUSTUM:
        ax2.scatter(0, 0, c='blue', s=100, marker='^', label='Camera 1')
        ax2.scatter(cam2_pos[0], cam2_pos[2], c='red', s=100, marker='^', label='Camera 2')
    
    ax2.set_xlabel('X')
    ax2.set_ylabel('Z (Depth)')
    ax2.set_title('Top-Down View')
    ax2.legend()
    ax2.grid(True)
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def visualize_reprojection_error(errors1, errors2, output_path):
    """
    Memvisualisasikan distribusi reprojection error.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Histogram error gambar 1
    axes[0].hist(errors1, bins=50, edgecolor='black', alpha=0.7, color='blue')
    axes[0].axvline(np.mean(errors1), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(errors1):.2f}')
    axes[0].set_xlabel('Reprojection Error (px)')
    axes[0].set_ylabel('Frekuensi')
    axes[0].set_title('Error Gambar 1')
    axes[0].legend()
    
    # Histogram error gambar 2
    axes[1].hist(errors2, bins=50, edgecolor='black', alpha=0.7, color='green')
    axes[1].axvline(np.mean(errors2), color='red', linestyle='--',
                   label=f'Mean: {np.mean(errors2):.2f}')
    axes[1].set_xlabel('Reprojection Error (px)')
    axes[1].set_ylabel('Frekuensi')
    axes[1].set_title('Error Gambar 2')
    axes[1].legend()
    
    # Combined error
    combined = (errors1 + errors2) / 2
    axes[2].hist(combined, bins=50, edgecolor='black', alpha=0.7, color='purple')
    axes[2].axvline(np.mean(combined), color='red', linestyle='--',
                   label=f'Mean: {np.mean(combined):.2f}')
    axes[2].set_xlabel('Average Reprojection Error (px)')
    axes[2].set_ylabel('Frekuensi')
    axes[2].set_title('Combined Error')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("TRIANGULASI 3D DARI STEREO IMAGES")
    print("="*70)
    print(f"\nKonfigurasi:")
    print(f"  - Focal Length: {FOCAL_LENGTH} px")
    print(f"  - Reproj Error Threshold: {REPROJ_ERROR_THRESHOLD} px")
    print(f"  - Depth Range: [{MIN_DEPTH}, {MAX_DEPTH}]")
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
        # Buat gambar dengan pola grid
        img1 = np.zeros((480, 640, 3), dtype=np.uint8)
        img2 = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Checkerboard dengan perspektif berbeda
        for i in range(6):
            for j in range(8):
                x1, y1 = 40 + j*75, 40 + i*75
                cv2.rectangle(img1, (x1, y1), (x1+30, y1+30), (255, 255, 255), -1)
                # Simulasi translasi kamera
                x2 = x1 - 25 + int(10 * (x1 - 320) / 320)  # parallax effect
                if 10 < x2 < 610:
                    cv2.rectangle(img2, (x2, y1), (x2+30, y1+30), (255, 255, 255), -1)
    else:
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
    
    if img1 is None or img2 is None:
        print("Error: Tidak dapat membaca gambar!")
        return
    
    h, w = img1.shape[:2]
    principal_point = (w // 2, h // 2)
    
    print(f"Ukuran gambar: {img1.shape}")
    
    # Step 1: Camera matrix
    print("\n[1] Membuat Camera Matrix...")
    K = get_camera_matrix(FOCAL_LENGTH, principal_point)
    
    # Step 2: Feature matching
    print("[2] Mendeteksi dan mencocokkan fitur...")
    pts1, pts2, kp1, kp2, matches = detect_and_match_features(
        img1, img2, DETECTOR_TYPE, MAX_FEATURES, RATIO_THRESHOLD
    )
    print(f"    Jumlah matches: {len(pts1)}")
    
    if len(pts1) < 8:
        print("Error: Tidak cukup matches!")
        return
    
    # Step 3: Estimate camera poses
    print("[3] Mengestimasi pose kamera...")
    P1, P2, R, t, pose_mask = estimate_camera_poses(pts1, pts2, K)
    
    pts1_inliers = pts1[pose_mask]
    pts2_inliers = pts2[pose_mask]
    print(f"    Inliers untuk triangulasi: {len(pts1_inliers)}")
    
    # Step 4: Triangulasi
    print("[4] Melakukan triangulasi...")
    points_3d = triangulate_points_cv(pts1_inliers, pts2_inliers, P1, P2)
    print(f"    Jumlah titik 3D: {len(points_3d)}")
    
    # Step 5: Compute reprojection error
    print("[5] Menghitung reprojection error...")
    errors1, errors2 = compute_reprojection_error(pts1_inliers, pts2_inliers, 
                                                   points_3d, P1, P2)
    print(f"    Mean error gambar 1: {errors1.mean():.2f} px")
    print(f"    Mean error gambar 2: {errors2.mean():.2f} px")
    
    # Step 6: Filter points
    print("[6] Memfilter outliers...")
    valid_mask = filter_points(points_3d, pts1_inliers, pts2_inliers,
                              errors1, errors2, REPROJ_ERROR_THRESHOLD,
                              MIN_DEPTH, MAX_DEPTH, R, t)
    
    points_3d_filtered = points_3d[valid_mask]
    errors1_filtered = errors1[valid_mask]
    errors2_filtered = errors2[valid_mask]
    
    print(f"    Titik setelah filtering: {len(points_3d_filtered)}")
    
    # Step 7: Visualisasi
    print("[7] Memvisualisasikan hasil...")
    
    visualize_3d_points(points_3d_filtered, R, t,
                       output_dir / "04_triangulated_points.png",
                       "Triangulated 3D Point Cloud")
    
    visualize_reprojection_error(errors1_filtered, errors2_filtered,
                                output_dir / "04_reprojection_error.png")
    
    # Statistik
    print("\n" + "="*50)
    print("STATISTIK HASIL TRIANGULASI")
    print("="*50)
    print(f"Total matches: {len(pts1)}")
    print(f"Inliers: {len(pts1_inliers)}")
    print(f"Titik 3D valid: {len(points_3d_filtered)}")
    print(f"\nReprojection Error (setelah filtering):")
    print(f"  Mean (img1): {errors1_filtered.mean():.3f} px")
    print(f"  Mean (img2): {errors2_filtered.mean():.3f} px")
    print(f"  Max:  {max(errors1_filtered.max(), errors2_filtered.max()):.3f} px")
    
    if len(points_3d_filtered) > 0:
        print(f"\n3D Point Statistics:")
        print(f"  X range: [{points_3d_filtered[:,0].min():.2f}, {points_3d_filtered[:,0].max():.2f}]")
        print(f"  Y range: [{points_3d_filtered[:,1].min():.2f}, {points_3d_filtered[:,1].max():.2f}]")
        print(f"  Z range: [{points_3d_filtered[:,2].min():.2f}, {points_3d_filtered[:,2].max():.2f}]")
    
    print("\n✓ Program selesai!")


if __name__ == "__main__":
    main()
