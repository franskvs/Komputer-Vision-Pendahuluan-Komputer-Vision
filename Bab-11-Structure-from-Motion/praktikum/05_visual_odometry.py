#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 05_visual_odometry.py

Deskripsi:
    Program ini mendemonstrasikan Visual Odometry (VO), yaitu teknik
    untuk mengestimasi gerakan kamera frame-by-frame dari sekuens video.
    VO adalah komponen penting dalam robot navigasi dan self-driving cars.

Tujuan:
    1. Memahami konsep visual odometry
    2. Mengimplementasikan monocular visual odometry
    3. Memvisualisasikan trajectory kamera
    4. Memahami masalah scale ambiguity

Teori:
    Visual Odometry bekerja dengan:
    1. Mendeteksi fitur di frame t dan t+1
    2. Mencocokkan fitur antar frame
    3. Mengestimasi Essential Matrix
    4. Mendekomposisi menjadi R dan t
    5. Mengakumulasi pose untuk mendapat trajectory

Aplikasi Dunia Nyata:
    - Self-driving cars (Tesla, Waymo)
    - Robot navigasi (vacuum cleaner, warehouse robots)
    - Drone navigation
    - Augmented Reality

Author: Praktikum Computer Vision
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time

# ============================================================================
# VARIABEL KONFIGURASI - UBAH NILAI INI UNTUK EKSPERIMEN
# ============================================================================

# Sumber video: 'webcam', 'video', atau 'synthetic'
VIDEO_SOURCE = 'synthetic'

# Path video (jika VIDEO_SOURCE = 'video')
VIDEO_PATH = ""

# Parameter kamera
FOCAL_LENGTH = 718.8560  # KITTI dataset focal length
PRINCIPAL_POINT = (607.1928, 185.2157)  # KITTI dataset

# Feature detection
DETECTOR_TYPE = 'FAST'  # FAST lebih cepat untuk real-time
MAX_FEATURES = 3000

# Optical flow parameters (Lucas-Kanade)
LK_PARAMS = dict(
    winSize=(21, 21),
    maxLevel=3,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01)
)

# RANSAC parameters
RANSAC_PROB = 0.999
RANSAC_THRESHOLD = 1.0

# Minimum features sebelum re-detection
MIN_FEATURES = 500

# Visualisasi
TRAJECTORY_SCALE = 1.0
SHOW_FEATURES = True

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


def detect_features(image, detector_type='FAST', max_features=3000):
    """
    Mendeteksi fitur (corners) pada gambar.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    if detector_type == 'FAST':
        detector = cv2.FastFeatureDetector_create(threshold=20)
        keypoints = detector.detect(gray)
        # Sort by response dan ambil top N
        keypoints = sorted(keypoints, key=lambda x: x.response, reverse=True)[:max_features]
        points = np.array([kp.pt for kp in keypoints], dtype=np.float32)
    elif detector_type == 'GFTT':
        # Good Features To Track (Shi-Tomasi corners)
        points = cv2.goodFeaturesToTrack(
            gray,
            maxCorners=max_features,
            qualityLevel=0.01,
            minDistance=10
        )
        points = points.reshape(-1, 2) if points is not None else np.array([])
    else:
        detector = cv2.SIFT_create(nfeatures=max_features)
        keypoints = detector.detect(gray)
        points = np.array([kp.pt for kp in keypoints], dtype=np.float32)
    
    return points.reshape(-1, 1, 2) if len(points) > 0 else None


def track_features(prev_gray, curr_gray, prev_points, lk_params):
    """
    Track fitur menggunakan Lucas-Kanade optical flow.
    
    Returns:
        prev_points_good: Titik yang berhasil di-track (frame sebelumnya)
        curr_points_good: Titik hasil tracking (frame saat ini)
    """
    if prev_points is None or len(prev_points) == 0:
        return None, None
    
    # Forward tracking
    curr_points, status, err = cv2.calcOpticalFlowPyrLK(
        prev_gray, curr_gray, prev_points, None, **lk_params
    )
    
    # Backward tracking untuk validasi
    prev_points_back, status_back, _ = cv2.calcOpticalFlowPyrLK(
        curr_gray, prev_gray, curr_points, None, **lk_params
    )
    
    # Filter: hanya ambil yang konsisten forward-backward
    if prev_points_back is not None:
        diff = abs(prev_points - prev_points_back).reshape(-1, 2).max(-1)
        status = status & (diff < 1.0).reshape(-1, 1).astype(np.uint8)
    
    # Filter by status
    good_mask = status.ravel() == 1
    
    if not good_mask.any():
        return None, None
    
    prev_points_good = prev_points[good_mask]
    curr_points_good = curr_points[good_mask]
    
    return prev_points_good, curr_points_good


def estimate_motion(prev_points, curr_points, K):
    """
    Estimasi motion (R, t) dari korespondensi titik.
    """
    if prev_points is None or curr_points is None:
        return None, None, None
    
    if len(prev_points) < 5:
        return None, None, None
    
    prev_pts = prev_points.reshape(-1, 2)
    curr_pts = curr_points.reshape(-1, 2)
    
    # Hitung Essential Matrix
    E, mask = cv2.findEssentialMat(
        prev_pts, curr_pts, K,
        method=cv2.RANSAC,
        prob=RANSAC_PROB,
        threshold=RANSAC_THRESHOLD
    )
    
    if E is None:
        return None, None, None
    
    # Recover pose
    _, R, t, mask = cv2.recoverPose(E, prev_pts, curr_pts, K)
    
    return R, t, mask


def create_synthetic_video():
    """
    Membuat video sintetis untuk demo visual odometry.
    Menampilkan kotak yang bergerak mensimulasikan kamera bergerak maju.
    """
    frames = []
    width, height = 640, 480
    
    # Simulasi kamera bergerak maju
    for i in range(100):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background dengan titik-titik (bintang)
        np.random.seed(42)  # Supaya konsisten
        for _ in range(200):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            # Titik bergerak dari tengah ke luar (simulasi forward motion)
            cx, cy = width // 2, height // 2
            scale = 1 + i * 0.02  # Expanding
            x_new = int(cx + (x - cx) * scale) % width
            y_new = int(cy + (y - cy) * scale) % height
            cv2.circle(frame, (x_new, y_new), 2, (255, 255, 255), -1)
        
        # Objek di scene (simulasi gedung)
        for j, offset in enumerate([-200, -100, 0, 100, 200]):
            x_base = width // 2 + offset
            # Parallax effect: objek lebih dekat bergerak lebih cepat
            depth_factor = 1 + j * 0.5
            x_pos = int(x_base + (i * 2 * depth_factor) - 100)
            
            if 0 < x_pos < width - 50:
                h = 100 + j * 30
                cv2.rectangle(frame, (x_pos, height - h), 
                            (x_pos + 50, height), (100 + j*30, 100 + j*20, 150), -1)
        
        # Horizon line
        cv2.line(frame, (0, height // 2), (width, height // 2), (50, 50, 50), 1)
        
        frames.append(frame)
    
    return frames


class VisualOdometry:
    """
    Kelas untuk Visual Odometry.
    """
    def __init__(self, K, detector_type='FAST', max_features=3000):
        self.K = K
        self.detector_type = detector_type
        self.max_features = max_features
        
        # State
        self.prev_gray = None
        self.prev_points = None
        
        # Trajectory
        self.cur_R = np.eye(3)
        self.cur_t = np.zeros((3, 1))
        self.trajectory = [self.cur_t.copy()]
        
        # Statistics
        self.frame_count = 0
        self.feature_counts = []
    
    def process_frame(self, frame):
        """
        Proses satu frame dan update pose.
        
        Returns:
            success: True jika berhasil
            num_features: Jumlah fitur yang di-track
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        if self.prev_gray is None:
            # Frame pertama: deteksi fitur
            self.prev_gray = gray
            self.prev_points = detect_features(gray, self.detector_type, self.max_features)
            self.frame_count += 1
            return True, len(self.prev_points) if self.prev_points is not None else 0
        
        # Track fitur
        prev_pts, curr_pts = track_features(
            self.prev_gray, gray, self.prev_points, LK_PARAMS
        )
        
        num_features = len(curr_pts) if curr_pts is not None else 0
        self.feature_counts.append(num_features)
        
        if num_features < 10:
            # Tidak cukup fitur, re-detect
            self.prev_gray = gray
            self.prev_points = detect_features(gray, self.detector_type, self.max_features)
            return False, num_features
        
        # Estimasi motion
        R, t, mask = estimate_motion(prev_pts, curr_pts, self.K)
        
        if R is not None:
            # Update pose kumulatif
            # cur_t = cur_t + scale * cur_R @ t
            # cur_R = R @ cur_R
            scale = 1.0  # Scale ambiguity - dalam praktik perlu estimasi dari sensor lain
            self.cur_t = self.cur_t + scale * self.cur_R @ t
            self.cur_R = R @ self.cur_R
            self.trajectory.append(self.cur_t.copy())
        
        # Re-detect jika fitur terlalu sedikit
        if num_features < MIN_FEATURES:
            self.prev_points = detect_features(gray, self.detector_type, self.max_features)
        else:
            self.prev_points = curr_pts.reshape(-1, 1, 2)
        
        self.prev_gray = gray
        self.frame_count += 1
        
        return R is not None, num_features
    
    def get_trajectory(self):
        """Mengembalikan trajectory sebagai array Nx3."""
        return np.array([t.flatten() for t in self.trajectory])
    
    def draw_features(self, frame, prev_pts, curr_pts):
        """Menggambar fitur dan optical flow pada frame."""
        vis = frame.copy()
        
        if prev_pts is not None and curr_pts is not None:
            for p1, p2 in zip(prev_pts.reshape(-1, 2), curr_pts.reshape(-1, 2)):
                p1 = tuple(map(int, p1))
                p2 = tuple(map(int, p2))
                cv2.circle(vis, p2, 2, (0, 255, 0), -1)
                cv2.line(vis, p1, p2, (255, 0, 0), 1)
        
        return vis


def visualize_trajectory(trajectory, output_path):
    """
    Memvisualisasikan trajectory kamera.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Top-down view (X vs Z)
    axes[0].plot(trajectory[:, 0], trajectory[:, 2], 'b-', linewidth=1)
    axes[0].plot(trajectory[0, 0], trajectory[0, 2], 'go', markersize=10, label='Start')
    axes[0].plot(trajectory[-1, 0], trajectory[-1, 2], 'ro', markersize=10, label='End')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Z (Forward)')
    axes[0].set_title('Trajectory Top-Down View')
    axes[0].legend()
    axes[0].grid(True)
    axes[0].axis('equal')
    
    # 3D trajectory
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 'b-', linewidth=1)
    ax2.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2], 
               c='green', s=100, label='Start')
    ax2.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], 
               c='red', s=100, label='End')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('3D Trajectory')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("VISUAL ODOMETRY - ESTIMASI GERAKAN KAMERA")
    print("="*70)
    print(f"\nKonfigurasi:")
    print(f"  - Video Source: {VIDEO_SOURCE}")
    print(f"  - Detector: {DETECTOR_TYPE}")
    print(f"  - Max Features: {MAX_FEATURES}")
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent.resolve()
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Camera matrix
    K = get_camera_matrix(FOCAL_LENGTH, PRINCIPAL_POINT)
    
    # Initialize VO
    vo = VisualOdometry(K, DETECTOR_TYPE, MAX_FEATURES)
    
    # Get video source
    if VIDEO_SOURCE == 'synthetic':
        print("Menggunakan video sintetis...")
        frames = create_synthetic_video()
        total_frames = len(frames)
    elif VIDEO_SOURCE == 'webcam':
        print("Menggunakan webcam...")
        cap = cv2.VideoCapture(0)
        total_frames = 200  # Proses 200 frame
    else:
        print(f"Membuka video: {VIDEO_PATH}")
        cap = cv2.VideoCapture(VIDEO_PATH)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Total frames: {total_frames}")
    print("\nMemproses frames...")
    
    # Process frames
    frame_idx = 0
    processed_frames = []
    
    while frame_idx < total_frames:
        if VIDEO_SOURCE == 'synthetic':
            frame = frames[frame_idx]
        else:
            ret, frame = cap.read()
            if not ret:
                break
        
        # Process frame
        start_time = time.time()
        success, num_features = vo.process_frame(frame)
        process_time = (time.time() - start_time) * 1000
        
        # Save some processed frames for visualization
        if frame_idx % 10 == 0 and SHOW_FEATURES:
            processed_frames.append(frame.copy())
        
        if frame_idx % 20 == 0:
            print(f"  Frame {frame_idx}/{total_frames}, Features: {num_features}, "
                  f"Time: {process_time:.1f}ms")
        
        frame_idx += 1
    
    if VIDEO_SOURCE != 'synthetic':
        cap.release()
    
    # Get trajectory
    trajectory = vo.get_trajectory()
    
    print(f"\nTrajectory computed: {len(trajectory)} poses")
    
    # Visualize
    print("\nMemvisualisasikan hasil...")
    visualize_trajectory(trajectory, output_dir / "05_vo_trajectory.png")
    
    # Plot feature count over time
    plt.figure(figsize=(10, 4))
    plt.plot(vo.feature_counts, 'b-', linewidth=0.5)
    plt.axhline(MIN_FEATURES, color='r', linestyle='--', label=f'Min threshold: {MIN_FEATURES}')
    plt.xlabel('Frame')
    plt.ylabel('Number of Features')
    plt.title('Tracked Features Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "05_feature_count.png", dpi=150)
    plt.close()
    print(f"Hasil disimpan: {output_dir / '05_feature_count.png'}")
    
    # Statistik
    print("\n" + "="*50)
    print("STATISTIK VISUAL ODOMETRY")
    print("="*50)
    print(f"Total frames diproses: {frame_idx}")
    print(f"Trajectory length: {len(trajectory)} poses")
    
    if len(trajectory) > 1:
        total_distance = np.sum(np.linalg.norm(np.diff(trajectory, axis=0), axis=1))
        print(f"Total distance traveled: {total_distance:.2f} units")
        print(f"Final position: [{trajectory[-1,0]:.2f}, {trajectory[-1,1]:.2f}, {trajectory[-1,2]:.2f}]")
    
    if vo.feature_counts:
        print(f"\nFeature Statistics:")
        print(f"  Mean: {np.mean(vo.feature_counts):.0f}")
        print(f"  Min: {np.min(vo.feature_counts)}")
        print(f"  Max: {np.max(vo.feature_counts)}")
    
    print("\n✓ Program selesai!")
    print("\nNote: Pada monocular VO, scale tidak dapat ditentukan.")
    print("      Untuk scale absolut, diperlukan stereo camera atau sensor lain.")


if __name__ == "__main__":
    main()
