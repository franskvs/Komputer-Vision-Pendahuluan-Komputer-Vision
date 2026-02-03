#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 03_essential_matrix.py

Deskripsi:
    Program ini mendemonstrasikan estimasi Essential Matrix, yang merupakan
    versi "terkalibrasi" dari Fundamental Matrix. Essential Matrix memungkinkan
    kita untuk mengekstrak rotasi (R) dan translasi (t) relatif antara dua kamera.

Tujuan:
    1. Memahami hubungan Essential Matrix dengan Fundamental Matrix
    2. Memahami dekomposisi Essential Matrix menjadi R dan t
    3. Memahami pentingnya kalibrasi kamera dalam SfM
    4. Memvisualisasikan pose kamera

Teori:
    E = K'^T * F * K
    
    Essential Matrix dapat didekomposisi menjadi:
    E = t_x * R
    
    dimana t_x adalah skew-symmetric matrix dari vektor translasi.
    
Aplikasi Dunia Nyata:
    - Visual SLAM
    - Augmented Reality
    - Drone navigation
    - Robot localization

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

# Parameter kalibrasi kamera (intrinsic)
# Untuk kamera webcam standar, nilai ini adalah estimasi
# Focal length dalam pixel (biasanya sekitar 500-1500 untuk webcam)
FOCAL_LENGTH = 800

# Principal point (biasanya di tengah gambar)
# Format: (cx, cy) - koordinat titik pusat optik
PRINCIPAL_POINT = (320, 240)

# Threshold untuk RANSAC (dalam pixel)
RANSAC_THRESHOLD = 1.0

# Confidence level untuk RANSAC
RANSAC_CONFIDENCE = 0.999

# Feature detection parameters
DETECTOR_TYPE = 'SIFT'
MAX_FEATURES = 3000
RATIO_THRESHOLD = 0.7

# ============================================================================
# FUNGSI UTILITAS
# ============================================================================

def get_camera_matrix(focal_length, principal_point):
    """
    Membuat Camera Matrix (K) dari parameter kalibrasi.
    
    K = | fx  0  cx |
        | 0  fy  cy |
        | 0   0   1 |
    
    Asumsi: fx = fy (square pixels)
    """
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
    """
    Mendeteksi dan mencocokkan fitur antara dua gambar.
    """
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
    
    if detector_type in ['ORB', 'AKAZE', 'BRISK']:
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


def compute_essential_matrix(pts1, pts2, K, threshold=1.0, confidence=0.999):
    """
    Menghitung Essential Matrix dari korespondensi titik.
    
    E dapat dihitung langsung menggunakan 5-point algorithm,
    atau dari Fundamental Matrix: E = K'^T * F * K
    """
    E, mask = cv2.findEssentialMat(
        pts1, pts2, K,
        method=cv2.RANSAC,
        prob=confidence,
        threshold=threshold
    )
    
    return E, mask


def decompose_essential_matrix(E, K, pts1, pts2):
    """
    Mendekomposisi Essential Matrix menjadi Rotation dan Translation.
    
    Dari E, kita bisa mendapatkan 4 kemungkinan solusi (R, t).
    Solusi yang benar adalah yang menghasilkan titik 3D dengan
    depth positif di depan kedua kamera.
    
    Returns:
        R: Rotation matrix (3x3)
        t: Translation vector (3x1)
        mask: Inlier mask setelah cheirality check
    """
    # recoverPose melakukan dekomposisi dan cheirality check
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)
    
    return R, t, mask


def rotation_matrix_to_euler(R):
    """
    Mengkonversi rotation matrix ke Euler angles (roll, pitch, yaw).
    """
    sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)
    
    singular = sy < 1e-6
    
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0
    
    return np.degrees([x, y, z])  # roll, pitch, yaw


def visualize_camera_poses(R, t, output_path):
    """
    Memvisualisasikan pose relatif dua kamera dalam 3D.
    """
    fig = plt.figure(figsize=(12, 5))
    
    # Camera 1 (origin)
    cam1_pos = np.array([0, 0, 0])
    cam1_dir = np.array([0, 0, 1])  # looking along z-axis
    
    # Camera 2 (transformed)
    cam2_pos = t.flatten()
    cam2_dir = R @ np.array([0, 0, 1])  # rotated direction
    
    # 3D visualization
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Draw camera 1
    ax1.scatter(*cam1_pos, color='blue', s=100, label='Camera 1')
    ax1.quiver(*cam1_pos, *cam1_dir*0.5, color='blue', arrow_length_ratio=0.2)
    
    # Draw camera 2
    ax1.scatter(*cam2_pos, color='red', s=100, label='Camera 2')
    ax1.quiver(*cam2_pos, *cam2_dir*0.5, color='red', arrow_length_ratio=0.2)
    
    # Draw axes
    ax1.quiver(0, 0, 0, 0.3, 0, 0, color='red', alpha=0.5)
    ax1.quiver(0, 0, 0, 0, 0.3, 0, color='green', alpha=0.5)
    ax1.quiver(0, 0, 0, 0, 0, 0.3, color='blue', alpha=0.5)
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Camera Poses (3D View)')
    ax1.legend()
    
    # Set equal aspect ratio
    max_range = max(abs(cam2_pos).max(), 1) * 1.5
    ax1.set_xlim([-max_range, max_range])
    ax1.set_ylim([-max_range, max_range])
    ax1.set_zlim([-0.5, max_range])
    
    # Top-down view
    ax2 = fig.add_subplot(122)
    
    ax2.scatter(cam1_pos[0], cam1_pos[2], color='blue', s=100, label='Camera 1')
    ax2.scatter(cam2_pos[0], cam2_pos[2], color='red', s=100, label='Camera 2')
    
    # Draw viewing directions
    ax2.arrow(cam1_pos[0], cam1_pos[2], cam1_dir[0]*0.3, cam1_dir[2]*0.3,
              head_width=0.05, color='blue')
    ax2.arrow(cam2_pos[0], cam2_pos[2], cam2_dir[0]*0.3, cam2_dir[2]*0.3,
              head_width=0.05, color='red')
    
    ax2.set_xlabel('X')
    ax2.set_ylabel('Z (Depth)')
    ax2.set_title('Camera Poses (Top-Down View)')
    ax2.legend()
    ax2.grid(True)
    ax2.axis('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def visualize_essential_matrix(E, output_path):
    """
    Memvisualisasikan Essential Matrix sebagai heatmap.
    """
    plt.figure(figsize=(8, 6))
    
    im = plt.imshow(E, cmap='RdBu', aspect='equal')
    plt.colorbar(im)
    
    # Annotate values
    for i in range(3):
        for j in range(3):
            plt.text(j, i, f'{E[i,j]:.4f}', ha='center', va='center', fontsize=10)
    
    plt.title('Essential Matrix E\n(x\'ᵀ E x = 0)')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def verify_essential_matrix(E):
    """
    Memverifikasi properti Essential Matrix:
    1. Rank harus 2
    2. Dua singular values harus sama, satu harus 0
    """
    # SVD
    U, S, Vt = np.linalg.svd(E)
    
    # Rank
    rank = np.linalg.matrix_rank(E)
    
    return {
        'rank': rank,
        'singular_values': S,
        'valid_rank': rank == 2,
        'valid_sv': abs(S[0] - S[1]) < 0.1 * S[0] and S[2] < 0.1 * S[0]
    }


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("ESTIMASI ESSENTIAL MATRIX DAN POSE KAMERA")
    print("="*70)
    print(f"\nParameter Kamera:")
    print(f"  - Focal Length: {FOCAL_LENGTH} pixel")
    print(f"  - Principal Point: {PRINCIPAL_POINT}")
    print(f"\nKonfigurasi RANSAC:")
    print(f"  - Threshold: {RANSAC_THRESHOLD} pixel")
    print(f"  - Confidence: {RANSAC_CONFIDENCE}")
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent.resolve()
    data_dir = script_dir.parent / "data" / "images"
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Load gambar
    img1_path = data_dir / "building1.jpg"
    img2_path = data_dir / "building2.jpg"
    
    if not img1_path.exists() or not img2_path.exists():
        print("Gambar sampel tidak ditemukan. Membuat gambar dummy...")
        img1 = np.zeros((480, 640, 3), dtype=np.uint8)
        img2 = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Pattern untuk feature detection
        for i in range(8):
            for j in range(10):
                x1, y1 = 40 + j*60, 40 + i*55
                cv2.circle(img1, (x1, y1), 15, (255, 255, 255), -1)
                # Simulasi translasi kamera ke kanan
                x2, y2 = x1 - 20, y1
                if 0 < x2 < 640:
                    cv2.circle(img2, (x2, y2), 15, (255, 255, 255), -1)
    else:
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
    
    if img1 is None or img2 is None:
        print("Error: Tidak dapat membaca gambar!")
        return
    
    # Update principal point based on image size
    h, w = img1.shape[:2]
    principal_point = (w // 2, h // 2)
    
    print(f"Ukuran gambar: {img1.shape}")
    print(f"Principal point (updated): {principal_point}")
    
    # Step 1: Buat camera matrix
    print("\n[1] Membuat Camera Matrix K...")
    K = get_camera_matrix(FOCAL_LENGTH, principal_point)
    print("Camera Matrix K:")
    print(K)
    
    # Step 2: Detect dan match features
    print("\n[2] Mendeteksi dan mencocokkan fitur...")
    pts1, pts2, kp1, kp2, matches = detect_and_match_features(
        img1, img2, DETECTOR_TYPE, MAX_FEATURES, RATIO_THRESHOLD
    )
    print(f"    Jumlah korespondensi: {len(pts1)}")
    
    if len(pts1) < 5:
        print("Error: Tidak cukup korespondensi!")
        return
    
    # Step 3: Compute Essential Matrix
    print("\n[3] Menghitung Essential Matrix...")
    E, mask = compute_essential_matrix(pts1, pts2, K, RANSAC_THRESHOLD, RANSAC_CONFIDENCE)
    
    mask = mask.ravel().astype(bool)
    pts1_inliers = pts1[mask]
    pts2_inliers = pts2[mask]
    
    print(f"    Inliers: {mask.sum()} dari {len(mask)}")
    print("\nEssential Matrix E:")
    print(E)
    
    # Step 4: Verifikasi Essential Matrix
    print("\n[4] Memverifikasi Essential Matrix...")
    verification = verify_essential_matrix(E)
    print(f"    Rank: {verification['rank']} (valid: {verification['valid_rank']})")
    print(f"    Singular values: {verification['singular_values']}")
    print(f"    Valid SV ratio: {verification['valid_sv']}")
    
    # Visualisasi Essential Matrix
    visualize_essential_matrix(E, output_dir / "03_essential_matrix.png")
    
    # Step 5: Decompose Essential Matrix
    print("\n[5] Mendekomposisi Essential Matrix menjadi R dan t...")
    R, t, pose_mask = decompose_essential_matrix(E, K, pts1_inliers, pts2_inliers)
    
    print("\nRotation Matrix R:")
    print(R)
    print(f"\nTranslation Vector t (normalized):")
    print(t.flatten())
    
    # Convert to Euler angles
    euler = rotation_matrix_to_euler(R)
    print(f"\nEuler Angles (degrees):")
    print(f"    Roll:  {euler[0]:.2f}°")
    print(f"    Pitch: {euler[1]:.2f}°")
    print(f"    Yaw:   {euler[2]:.2f}°")
    
    # Step 6: Visualisasi camera poses
    print("\n[6] Memvisualisasikan pose kamera...")
    visualize_camera_poses(R, t, output_dir / "03_camera_poses.png")
    
    # Step 7: Verifikasi dekomposisi
    print("\n[7] Memverifikasi dekomposisi...")
    # Rekonstruksi E dari R dan t
    t_skew = np.array([
        [0, -t[2,0], t[1,0]],
        [t[2,0], 0, -t[0,0]],
        [-t[1,0], t[0,0], 0]
    ])
    E_reconstructed = t_skew @ R
    
    # Normalisasi untuk perbandingan
    E_norm = E / np.linalg.norm(E)
    E_recon_norm = E_reconstructed / np.linalg.norm(E_reconstructed)
    
    reconstruction_error = np.linalg.norm(E_norm - E_recon_norm)
    print(f"    Reconstruction error: {reconstruction_error:.6f}")
    
    # Ringkasan
    print("\n" + "="*50)
    print("RINGKASAN")
    print("="*50)
    print(f"Total korespondensi: {len(pts1)}")
    print(f"Inliers: {mask.sum()}")
    print(f"Rotasi: Roll={euler[0]:.1f}°, Pitch={euler[1]:.1f}°, Yaw={euler[2]:.1f}°")
    print(f"Translasi: [{t[0,0]:.3f}, {t[1,0]:.3f}, {t[2,0]:.3f}]")
    print("\nNote: Translasi hanya arah (normalized), bukan magnitude absolut.")
    print("      Untuk mendapatkan scale, diperlukan informasi tambahan (e.g., known distance).")
    print("\n✓ Program selesai!")


if __name__ == "__main__":
    main()
