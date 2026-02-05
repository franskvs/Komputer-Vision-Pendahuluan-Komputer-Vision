#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 06_bundle_adjustment.py

Deskripsi:
    Program ini mendemonstrasikan Bundle Adjustment, yaitu teknik optimasi
    untuk menyempurnakan rekonstruksi 3D dengan meminimalkan reprojection error
    secara bersamaan untuk semua titik 3D dan pose kamera.

Tujuan:
    1. Memahami konsep Bundle Adjustment
    2. Mengimplementasikan optimasi non-linear untuk SfM
    3. Memahami pentingnya BA untuk akurasi rekonstruksi
    4. Membandingkan hasil sebelum dan sesudah BA

Teori:
    Bundle Adjustment meminimasi:
    
    E = Σᵢ Σⱼ ||xᵢⱼ - π(Pⱼ, Xᵢ)||²
    
    dimana:
    - xᵢⱼ = pengukuran 2D titik i pada kamera j
    - π = fungsi proyeksi
    - Pⱼ = parameter kamera j (R, t, intrinsics)
    - Xᵢ = koordinat 3D titik i

Aplikasi Dunia Nyata:
    - Software fotogrametri (Agisoft, Pix4D)
    - Google Street View
    - Pembuatan peta 3D kota
    - Film VFX

Author: Praktikum Computer Vision
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix
from pathlib import Path
import time

# ============================================================================
# VARIABEL KONFIGURASI - UBAH NILAI INI UNTUK EKSPERIMEN
# ============================================================================

# Jumlah kamera (views)
NUM_CAMERAS = 5

# Jumlah titik 3D
NUM_POINTS = 100

# Parameter kamera
FOCAL_LENGTH = 800
PRINCIPAL_POINT = (320, 240)
IMAGE_SIZE = (640, 480)

# Noise level untuk simulasi
POINT_2D_NOISE = 1.0  # pixel
POINT_3D_NOISE = 0.1  # unit

# Bundle Adjustment parameters
MAX_ITERATIONS = 100
TOLERANCE = 1e-10

# Visualisasi
POINT_SIZE = 5

# ============================================================================
# FUNGSI UTILITAS
# ============================================================================

def rotation_matrix_to_rodrigues(R):
    """Konversi rotation matrix ke Rodrigues vector (axis-angle)."""
    rvec, _ = cv2.Rodrigues(R)
    return rvec.flatten()


def rodrigues_to_rotation_matrix(rvec):
    """Konversi Rodrigues vector ke rotation matrix."""
    R, _ = cv2.Rodrigues(rvec)
    return R


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


def project_points(points_3d, rvec, tvec, K):
    """
    Proyeksikan titik 3D ke 2D.
    
    Parameters:
        points_3d: Nx3 array titik 3D
        rvec: Rodrigues rotation vector (3,)
        tvec: Translation vector (3,)
        K: Camera matrix (3x3)
    
    Returns:
        points_2d: Nx2 array titik 2D
    """
    R = rodrigues_to_rotation_matrix(rvec)
    
    # Transform to camera coordinates
    points_cam = (R @ points_3d.T).T + tvec
    
    # Project to image plane
    points_2d = (K @ points_cam.T).T
    points_2d = points_2d[:, :2] / points_2d[:, 2:3]
    
    return points_2d


def generate_synthetic_data(n_cameras, n_points, K, image_size, noise_2d=0, noise_3d=0):
    """
    Generate synthetic SfM data untuk testing.
    
    Returns:
        points_3d: Nx3 true 3D points
        camera_params: List of (rvec, tvec) for each camera
        observations: List of (point_idx, camera_idx, x, y)
        points_2d_dict: Dict[cam_idx] -> Mx2 array of 2D points
    """
    np.random.seed(42)
    
    # Generate 3D points dalam kubus di depan kamera (simpler approach)
    points_3d = np.random.uniform(-1, 1, (n_points, 3))
    points_3d[:, 2] = np.abs(points_3d[:, 2]) + 3  # Ensure z > 0 and reasonable distance
    
    # Add small noise to 3D points
    points_3d_noisy = points_3d + np.random.randn(n_points, 3) * min(noise_3d, 0.05)
    
    # Generate simple camera poses 
    camera_params = []
    for i in range(n_cameras):
        # Simple camera positions around origin
        angle = i * 2 * np.pi / n_cameras if n_cameras > 1 else 0
        
        # Camera position (simple circular arrangement)
        cam_x = 1.0 * np.sin(angle)
        cam_z = 4.0 + 0.5 * np.cos(angle)  # Closer to points
        cam_pos = np.array([cam_x, 0, cam_z])
        
        # Simple rotation (look toward origin)
        # Use small rotation angles to avoid numerical issues
        rvec = np.array([0.1 * np.sin(angle), 0.05 * angle, 0.02 * np.cos(angle)])
        
        # Simple translation 
        tvec = np.array([-cam_x * 0.5, 0, -2.0])
        
        camera_params.append((rvec.copy(), tvec.copy()))
    
    # Generate 2D observations
    observations = []
    points_2d_dict = {}
    
    for cam_idx, (rvec, tvec) in enumerate(camera_params):
        try:
            points_2d = project_points(points_3d, rvec, tvec, K)
            
            # Add small noise
            points_2d_noisy = points_2d + np.random.randn(n_points, 2) * min(noise_2d, 2.0)
            
            # Filter points inside image with margin
            margin = 50
            valid = ((points_2d_noisy[:, 0] >= margin) & 
                    (points_2d_noisy[:, 0] < image_size[0] - margin) &
                    (points_2d_noisy[:, 1] >= margin) & 
                    (points_2d_noisy[:, 1] < image_size[1] - margin))
            
            valid_points = []
            for pt_idx in range(n_points):
                if valid[pt_idx]:
                    observations.append((pt_idx, cam_idx, 
                                        points_2d_noisy[pt_idx, 0], 
                                        points_2d_noisy[pt_idx, 1]))
                    valid_points.append(points_2d_noisy[pt_idx])
            
            points_2d_dict[cam_idx] = np.array(valid_points) if valid_points else np.zeros((0, 2))
            
        except Exception as e:
            print(f"  Warning: Error processing camera {cam_idx}: {e}")
            points_2d_dict[cam_idx] = np.zeros((0, 2))
    
    return points_3d, points_3d_noisy, camera_params, observations


def pack_parameters(camera_params, points_3d, n_cameras, n_points):
    """
    Pack camera parameters dan 3D points ke single vector untuk optimasi.
    
    Format: [cam0_rvec, cam0_tvec, cam1_rvec, cam1_tvec, ..., 
             point0_xyz, point1_xyz, ...]
    """
    params = []
    
    # Camera parameters (6 per camera: 3 for rvec, 3 for tvec)
    for rvec, tvec in camera_params:
        params.extend(rvec)
        params.extend(tvec)
    
    # 3D points (3 per point: x, y, z)
    for pt in points_3d:
        params.extend(pt)
    
    return np.array(params)


def unpack_parameters(params, n_cameras, n_points):
    """
    Unpack parameter vector ke camera params dan 3D points.
    """
    camera_params = []
    idx = 0
    
    for _ in range(n_cameras):
        rvec = params[idx:idx+3]
        tvec = params[idx+3:idx+6]
        camera_params.append((rvec, tvec))
        idx += 6
    
    points_3d = params[idx:].reshape(n_points, 3)
    
    return camera_params, points_3d


def compute_residuals(params, n_cameras, n_points, observations, K):
    """
    Compute reprojection error residuals.
    
    Returns:
        residuals: Array of (x_error, y_error) for each observation
    """
    camera_params, points_3d = unpack_parameters(params, n_cameras, n_points)
    
    residuals = []
    
    for pt_idx, cam_idx, x_obs, y_obs in observations:
        rvec, tvec = camera_params[cam_idx]
        pt_3d = points_3d[pt_idx:pt_idx+1]
        
        pt_2d = project_points(pt_3d, rvec, tvec, K)
        
        residuals.append(pt_2d[0, 0] - x_obs)
        residuals.append(pt_2d[0, 1] - y_obs)
    
    return np.array(residuals)


def bundle_adjustment_sparsity(n_cameras, n_points, observations):
    """
    Compute sparsity structure of Jacobian for efficient optimization.
    """
    n_observations = len(observations)
    n_params = n_cameras * 6 + n_points * 3
    
    # Jacobian matrix: (2*n_observations) x n_params
    A = lil_matrix((2 * n_observations, n_params), dtype=int)
    
    for i, (pt_idx, cam_idx, _, _) in enumerate(observations):
        # Each observation affects:
        # - Camera parameters (6 params)
        # - Point parameters (3 params)
        
        # Camera params
        cam_start = cam_idx * 6
        A[2*i:2*i+2, cam_start:cam_start+6] = 1
        
        # Point params
        pt_start = n_cameras * 6 + pt_idx * 3
        A[2*i:2*i+2, pt_start:pt_start+3] = 1
    
    return A


def run_bundle_adjustment(camera_params, points_3d, observations, K,
                         max_iter=100, tol=1e-10):
    """
    Run Bundle Adjustment using Levenberg-Marquardt.
    """
    n_cameras = len(camera_params)
    n_points = len(points_3d)
    
    # Pack initial parameters
    x0 = pack_parameters(camera_params, points_3d, n_cameras, n_points)
    
    # Compute sparsity
    A = bundle_adjustment_sparsity(n_cameras, n_points, observations)
    
    print(f"  Parameters: {len(x0)}")
    print(f"  Residuals: {2 * len(observations)}")
    
    # Check for invalid values in x0
    if not np.all(np.isfinite(x0)):
        print("  Warning: Invalid values in x0, cleaning...")
        x0 = np.nan_to_num(x0, nan=0.0, posinf=1.0, neginf=-1.0)
    
    # Compute initial residuals to validate
    try:
        initial_residuals = compute_residuals(x0, n_cameras, n_points, observations, K)
        if not np.all(np.isfinite(initial_residuals)):
            print("  Warning: Invalid initial residuals, adjusting parameters...")
            # Try to fix by reducing noise in 3D points
            points_start = n_cameras * 6
            x0[points_start:] *= 0.5  # Reduce 3D point coordinates
    except Exception as e:
        print(f"  Error in initial residual computation: {e}")
        print("  Attempting to fix parameters...")
        # Reset problematic parameters
        x0 = np.clip(x0, -10, 10)  # Reasonable bounds
    
    print(f"  Running optimization...")
    
    # Run optimization with bounds to prevent divergence
    bounds = (
        [-np.pi] * (n_cameras * 3) + [-100] * (n_cameras * 3) + [-10] * (n_points * 3),  # lower
        [np.pi] * (n_cameras * 3) + [100] * (n_cameras * 3) + [10] * (n_points * 3)      # upper
    )
    
    result = least_squares(
        compute_residuals,
        x0,
        bounds=bounds,
        jac_sparsity=A,
        verbose=0,
        ftol=tol,
        xtol=tol,
        max_nfev=max_iter,
        args=(n_cameras, n_points, observations, K),
        method='trf'
    )
    
    # Unpack optimized parameters
    camera_params_opt, points_3d_opt = unpack_parameters(
        result.x, n_cameras, n_points
    )
    
    return camera_params_opt, points_3d_opt, result


def compute_reprojection_error(camera_params, points_3d, observations, K):
    """
    Compute mean reprojection error.
    """
    errors = []
    
    for pt_idx, cam_idx, x_obs, y_obs in observations:
        rvec, tvec = camera_params[cam_idx]
        pt_3d = points_3d[pt_idx:pt_idx+1]
        pt_2d = project_points(pt_3d, rvec, tvec, K)
        
        error = np.sqrt((pt_2d[0, 0] - x_obs)**2 + (pt_2d[0, 1] - y_obs)**2)
        errors.append(error)
    
    return np.array(errors)


def visualize_reconstruction(points_3d_true, points_3d_before, points_3d_after,
                            camera_params, output_path):
    """
    Visualisasi rekonstruksi 3D sebelum dan sesudah Bundle Adjustment.
    """
    fig = plt.figure(figsize=(15, 5))
    
    # Before BA
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(points_3d_before[:, 0], points_3d_before[:, 1], points_3d_before[:, 2],
               c='blue', s=POINT_SIZE, alpha=0.6, label='Estimated')
    ax1.scatter(points_3d_true[:, 0], points_3d_true[:, 1], points_3d_true[:, 2],
               c='green', s=POINT_SIZE, alpha=0.6, label='Ground Truth')
    ax1.set_title('Before Bundle Adjustment')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.legend()
    
    # After BA
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(points_3d_after[:, 0], points_3d_after[:, 1], points_3d_after[:, 2],
               c='red', s=POINT_SIZE, alpha=0.6, label='After BA')
    ax2.scatter(points_3d_true[:, 0], points_3d_true[:, 1], points_3d_true[:, 2],
               c='green', s=POINT_SIZE, alpha=0.6, label='Ground Truth')
    ax2.set_title('After Bundle Adjustment')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.legend()
    
    # Comparison
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.scatter(points_3d_before[:, 0], points_3d_before[:, 1], points_3d_before[:, 2],
               c='blue', s=POINT_SIZE, alpha=0.4, label='Before BA')
    ax3.scatter(points_3d_after[:, 0], points_3d_after[:, 1], points_3d_after[:, 2],
               c='red', s=POINT_SIZE, alpha=0.4, label='After BA')
    ax3.scatter(points_3d_true[:, 0], points_3d_true[:, 1], points_3d_true[:, 2],
               c='green', s=POINT_SIZE, alpha=0.4, label='Ground Truth')
    
    # Draw cameras
    for rvec, tvec in camera_params:
        R = rodrigues_to_rotation_matrix(rvec)
        cam_pos = -R.T @ tvec
        ax3.scatter(cam_pos[0], cam_pos[1], cam_pos[2], c='black', s=50, marker='^')
    
    ax3.set_title('Comparison')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def visualize_error_comparison(errors_before, errors_after, output_path):
    """
    Visualisasi perbandingan reprojection error.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Histogram before
    axes[0].hist(errors_before, bins=50, edgecolor='black', alpha=0.7, color='blue')
    axes[0].axvline(np.mean(errors_before), color='red', linestyle='--',
                   label=f'Mean: {np.mean(errors_before):.3f}')
    axes[0].set_xlabel('Reprojection Error (px)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Before Bundle Adjustment')
    axes[0].legend()
    
    # Histogram after
    axes[1].hist(errors_after, bins=50, edgecolor='black', alpha=0.7, color='red')
    axes[1].axvline(np.mean(errors_after), color='blue', linestyle='--',
                   label=f'Mean: {np.mean(errors_after):.3f}')
    axes[1].set_xlabel('Reprojection Error (px)')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('After Bundle Adjustment')
    axes[1].legend()
    
    # Comparison bar chart
    metrics = ['Mean', 'Median', 'Max', 'Std']
    before_vals = [np.mean(errors_before), np.median(errors_before),
                   np.max(errors_before), np.std(errors_before)]
    after_vals = [np.mean(errors_after), np.median(errors_after),
                  np.max(errors_after), np.std(errors_after)]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    axes[2].bar(x - width/2, before_vals, width, label='Before BA', color='blue', alpha=0.7)
    axes[2].bar(x + width/2, after_vals, width, label='After BA', color='red', alpha=0.7)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(metrics)
    axes[2].set_ylabel('Error (px)')
    axes[2].set_title('Error Metrics Comparison')
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
    print("BUNDLE ADJUSTMENT - OPTIMASI REKONSTRUKSI 3D")
    print("="*70)
    print(f"\nKonfigurasi:")
    print(f"  - Jumlah Kamera: {NUM_CAMERAS}")
    print(f"  - Jumlah Titik 3D: {NUM_POINTS}")
    print(f"  - 2D Noise Level: {POINT_2D_NOISE} px")
    print(f"  - 3D Noise Level: {POINT_3D_NOISE}")
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent.resolve()
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Camera matrix
    K = get_camera_matrix(FOCAL_LENGTH, PRINCIPAL_POINT)
    
    # Generate synthetic data
    print("[1] Generating synthetic SfM data...")
    points_3d_true, points_3d_noisy, camera_params, observations = generate_synthetic_data(
        NUM_CAMERAS, NUM_POINTS, K, IMAGE_SIZE, 
        noise_2d=POINT_2D_NOISE, noise_3d=POINT_3D_NOISE
    )
    print(f"    Generated {len(observations)} observations")
    
    # Compute initial error
    print("\n[2] Computing initial reprojection error...")
    errors_before = compute_reprojection_error(
        camera_params, points_3d_noisy, observations, K
    )
    print(f"    Mean error: {errors_before.mean():.3f} px")
    print(f"    Max error: {errors_before.max():.3f} px")
    
    # Run Bundle Adjustment
    print("\n[3] Running Bundle Adjustment...")
    start_time = time.time()
    camera_params_opt, points_3d_opt, result = run_bundle_adjustment(
        camera_params, points_3d_noisy, observations, K,
        max_iter=MAX_ITERATIONS, tol=TOLERANCE
    )
    ba_time = time.time() - start_time
    
    print(f"    Optimization finished in {ba_time:.2f} seconds")
    print(f"    Iterations: {result.nfev}")
    print(f"    Termination: {result.message}")
    
    # Compute optimized error
    print("\n[4] Computing optimized reprojection error...")
    errors_after = compute_reprojection_error(
        camera_params_opt, points_3d_opt, observations, K
    )
    print(f"    Mean error: {errors_after.mean():.3f} px")
    print(f"    Max error: {errors_after.max():.3f} px")
    
    # Visualize results
    print("\n[5] Visualizing results...")
    visualize_reconstruction(
        points_3d_true, points_3d_noisy, points_3d_opt,
        camera_params_opt, output_dir / "06_ba_reconstruction.png"
    )
    
    visualize_error_comparison(
        errors_before, errors_after,
        output_dir / "06_ba_error_comparison.png"
    )
    
    # Compute 3D point accuracy
    error_3d_before = np.linalg.norm(points_3d_noisy - points_3d_true, axis=1)
    error_3d_after = np.linalg.norm(points_3d_opt - points_3d_true, axis=1)
    
    # Summary
    print("\n" + "="*50)
    print("RINGKASAN BUNDLE ADJUSTMENT")
    print("="*50)
    
    print("\nReprojection Error:")
    print(f"  Before BA: {errors_before.mean():.4f} px (mean), {errors_before.max():.4f} px (max)")
    print(f"  After BA:  {errors_after.mean():.4f} px (mean), {errors_after.max():.4f} px (max)")
    print(f"  Improvement: {(1 - errors_after.mean()/errors_before.mean())*100:.1f}%")
    
    print("\n3D Point Accuracy (distance to ground truth):")
    print(f"  Before BA: {error_3d_before.mean():.4f} (mean)")
    print(f"  After BA:  {error_3d_after.mean():.4f} (mean)")
    print(f"  Improvement: {(1 - error_3d_after.mean()/error_3d_before.mean())*100:.1f}%")
    
    print("\n✓ Program selesai!")


if __name__ == "__main__":
    main()
