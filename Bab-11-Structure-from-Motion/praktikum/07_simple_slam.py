#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRAKTIKUM COMPUTER VISION - BAB 11: STRUCTURE FROM MOTION
Program: 07_simple_slam.py

Deskripsi:
    Program ini mendemonstrasikan Simple Visual SLAM yang membangun peta
    (map) sekaligus melokalisasi kamera secara bersamaan. Ini adalah
    versi sederhana untuk memahami konsep dasar SLAM.

Tujuan:
    1. Memahami konsep SLAM (Simultaneous Localization and Mapping)
    2. Mengimplementasikan keyframe-based SLAM sederhana
    3. Memahami konsep loop closure (akan dibahas secara teori)
    4. Memvisualisasikan map dan trajectory secara real-time

Teori:
    Visual SLAM terdiri dari:
    - Frontend: Feature tracking, pose estimation
    - Backend: Map optimization (Bundle Adjustment)
    - Loop Closure: Detect revisited places untuk koreksi drift

Aplikasi Dunia Nyata:
    - Robot vacuum (Roomba)
    - AR glasses (HoloLens, Meta Quest)
    - Self-driving vehicles
    - Drone navigation

Author: Praktikum Computer Vision
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
from collections import deque

# ============================================================================
# VARIABEL KONFIGURASI - UBAH NILAI INI UNTUK EKSPERIMEN
# ============================================================================

# Sumber video: 'webcam', 'video', atau 'synthetic'
VIDEO_SOURCE = 'synthetic'
VIDEO_PATH = ""

# Parameter kamera
FOCAL_LENGTH = 500
PRINCIPAL_POINT = (320, 240)
IMAGE_SIZE = (640, 480)

# SLAM parameters
KEYFRAME_THRESHOLD = 20  # Minimum parallax (pixels) untuk keyframe baru
MIN_FEATURES = 100       # Minimum features sebelum re-detection
MAX_MAP_POINTS = 5000    # Maximum map points

# Feature detection
DETECTOR_TYPE = 'ORB'
MAX_FEATURES = 1000

# Local BA window
LOCAL_BA_WINDOW = 5  # Jumlah keyframes terakhir untuk local BA

# Visualization
VIS_SCALE = 50  # Scale untuk visualisasi trajectory

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


class MapPoint:
    """
    Representasi satu titik 3D dalam map.
    """
    _id_counter = 0
    
    def __init__(self, position, descriptor=None):
        self.id = MapPoint._id_counter
        MapPoint._id_counter += 1
        self.position = position  # 3D position
        self.descriptor = descriptor
        self.observations = []  # List of (keyframe_id, keypoint_idx)
        self.bad = False


class KeyFrame:
    """
    Representasi satu keyframe.
    """
    _id_counter = 0
    
    def __init__(self, frame, R, t, keypoints, descriptors):
        self.id = KeyFrame._id_counter
        KeyFrame._id_counter += 1
        self.frame = frame
        self.R = R
        self.t = t
        self.keypoints = keypoints
        self.descriptors = descriptors
        self.map_points = {}  # keypoint_idx -> MapPoint


class SimpleSLAM:
    """
    Simple Visual SLAM implementation.
    """
    def __init__(self, K, detector_type='ORB', max_features=1000):
        self.K = K
        self.max_features = max_features
        
        # Feature detector
        if detector_type == 'ORB':
            self.detector = cv2.ORB_create(nfeatures=max_features)
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        else:
            self.detector = cv2.SIFT_create(nfeatures=max_features)
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Map
        self.keyframes = []
        self.map_points = []
        
        # Current state
        self.current_frame = None
        self.current_R = np.eye(3)
        self.current_t = np.zeros((3, 1))
        
        # Tracking state
        self.prev_frame = None
        self.prev_keypoints = None
        self.prev_descriptors = None
        
        # Statistics
        self.frame_count = 0
        self.lost_count = 0
    
    def detect_features(self, frame):
        """Detect features in frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        keypoints, descriptors = self.detector.detectAndCompute(gray, None)
        return keypoints, descriptors
    
    def match_features(self, desc1, desc2, ratio=0.75):
        """Match features between two frames."""
        if desc1 is None or desc2 is None:
            return []
        
        matches = self.matcher.knnMatch(desc1, desc2, k=2)
        
        good_matches = []
        for m_pair in matches:
            if len(m_pair) == 2:
                m, n = m_pair
                if m.distance < ratio * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    def estimate_pose(self, kp1, kp2, matches):
        """Estimate relative pose from matches."""
        if len(matches) < 8:
            return None, None, None
        
        pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
        pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
        
        E, mask = cv2.findEssentialMat(pts1, pts2, self.K, cv2.RANSAC, 0.999, 1.0)
        if E is None:
            return None, None, None
        
        _, R, t, mask = cv2.recoverPose(E, pts1, pts2, self.K)
        
        return R, t, mask.ravel().astype(bool)
    
    def triangulate(self, kp1, kp2, matches, R1, t1, R2, t2):
        """Triangulate 3D points from matches."""
        if len(matches) == 0:
            return np.array([]), []
        
        pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).T
        pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).T
        
        P1 = self.K @ np.hstack([R1, t1])
        P2 = self.K @ np.hstack([R2, t2])
        
        points_4d = cv2.triangulatePoints(P1, P2, pts1, pts2)
        points_3d = (points_4d[:3] / points_4d[3]).T
        
        # Filter points behind camera
        valid = points_3d[:, 2] > 0
        
        return points_3d[valid], valid
    
    def is_keyframe(self, matches, kp1, kp2):
        """Check if current frame should be a keyframe."""
        if len(matches) < 20:
            return False
        
        # Compute mean parallax
        pts1 = np.array([kp1[m.queryIdx].pt for m in matches])
        pts2 = np.array([kp2[m.trainIdx].pt for m in matches])
        
        parallax = np.linalg.norm(pts2 - pts1, axis=1).mean()
        
        return parallax > KEYFRAME_THRESHOLD
    
    def process_frame(self, frame):
        """
        Process a single frame.
        
        Returns:
            success: True if tracking succeeded
            is_keyframe: True if this frame was added as keyframe
        """
        self.frame_count += 1
        self.current_frame = frame.copy()
        
        # Detect features
        keypoints, descriptors = self.detect_features(frame)
        
        if len(keypoints) < MIN_FEATURES:
            self.lost_count += 1
            return False, False
        
        # First frame initialization
        if self.prev_frame is None:
            self.prev_frame = frame.copy()
            self.prev_keypoints = keypoints
            self.prev_descriptors = descriptors
            
            # Add first keyframe
            kf = KeyFrame(frame, self.current_R.copy(), self.current_t.copy(),
                         keypoints, descriptors)
            self.keyframes.append(kf)
            
            return True, True
        
        # Match with previous frame
        matches = self.match_features(self.prev_descriptors, descriptors)
        
        if len(matches) < 10:
            self.lost_count += 1
            self.prev_keypoints = keypoints
            self.prev_descriptors = descriptors
            return False, False
        
        # Estimate pose
        R, t, mask = self.estimate_pose(self.prev_keypoints, keypoints, matches)
        
        if R is None:
            self.lost_count += 1
            return False, False
        
        # Update pose
        self.current_t = self.current_t + self.current_R @ t
        self.current_R = R @ self.current_R
        
        # Check if keyframe
        is_kf = self.is_keyframe(matches, self.prev_keypoints, keypoints)
        
        if is_kf:
            # Add keyframe
            kf = KeyFrame(frame, self.current_R.copy(), self.current_t.copy(),
                         keypoints, descriptors)
            self.keyframes.append(kf)
            
            # Triangulate new points
            if len(self.keyframes) >= 2:
                prev_kf = self.keyframes[-2]
                new_points, valid = self.triangulate(
                    prev_kf.keypoints, keypoints, matches,
                    prev_kf.R, prev_kf.t, self.current_R, self.current_t
                )
                
                # Add to map
                for i, pt in enumerate(new_points):
                    if len(self.map_points) < MAX_MAP_POINTS:
                        mp = MapPoint(pt)
                        self.map_points.append(mp)
        
        # Update previous frame
        self.prev_frame = frame.copy()
        self.prev_keypoints = keypoints
        self.prev_descriptors = descriptors
        
        return True, is_kf
    
    def get_trajectory(self):
        """Get camera trajectory from keyframes."""
        if len(self.keyframes) == 0:
            return np.array([[0, 0, 0]])
        
        trajectory = []
        for kf in self.keyframes:
            # Camera position = -R^T @ t
            pos = -kf.R.T @ kf.t
            trajectory.append(pos.flatten())
        
        return np.array(trajectory)
    
    def get_map_points(self):
        """Get all map points as Nx3 array."""
        if len(self.map_points) == 0:
            return np.array([])
        
        return np.array([mp.position for mp in self.map_points if not mp.bad])


def create_synthetic_slam_video():
    """
    Create synthetic video sequence for SLAM demo.
    Simulates camera moving through a 3D environment.
    """
    np.random.seed(42)
    
    width, height = IMAGE_SIZE
    frames = []
    
    # Create 3D scene points
    n_points = 500
    scene_points = np.random.uniform(-5, 5, (n_points, 3))
    scene_points[:, 2] = np.abs(scene_points[:, 2]) + 2  # All in front
    
    K = get_camera_matrix(FOCAL_LENGTH, PRINCIPAL_POINT)
    
    # Camera trajectory: circular path
    n_frames = 150
    for i in range(n_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Camera pose (circular motion)
        angle = i * 2 * np.pi / n_frames * 0.5  # Half circle
        radius = 3
        cam_x = radius * np.sin(angle)
        cam_z = radius * np.cos(angle)
        cam_pos = np.array([cam_x, 0, cam_z])
        
        # Camera looks at center
        forward = -cam_pos / np.linalg.norm(cam_pos)
        up = np.array([0, -1, 0])
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)
        
        R = np.array([right, up, forward])
        t = -R @ cam_pos
        
        # Project scene points
        P = K @ np.hstack([R, t.reshape(3, 1)])
        
        for pt in scene_points:
            pt_h = np.append(pt, 1)
            proj = P @ pt_h
            
            if proj[2] > 0:  # In front of camera
                x = int(proj[0] / proj[2])
                y = int(proj[1] / proj[2])
                
                if 0 <= x < width and 0 <= y < height:
                    # Size based on depth
                    depth = proj[2]
                    size = max(1, int(10 / depth))
                    color = (255, 255, 255)
                    cv2.circle(frame, (x, y), size, color, -1)
        
        # Add some structure (lines/edges)
        for j in range(10):
            x_base = (j * 100 + int(i * 5)) % width
            y_base = height // 2
            cv2.line(frame, (x_base, 0), (x_base, height), (100, 100, 100), 1)
        
        frames.append(frame)
    
    return frames


def visualize_slam_result(slam, output_path):
    """Visualize SLAM results."""
    fig = plt.figure(figsize=(15, 5))
    
    trajectory = slam.get_trajectory()
    map_points = slam.get_map_points()
    
    # Top-down view
    ax1 = fig.add_subplot(131)
    if len(trajectory) > 0:
        ax1.plot(trajectory[:, 0] * VIS_SCALE, trajectory[:, 2] * VIS_SCALE, 
                'b-', linewidth=2, label='Trajectory')
        ax1.plot(trajectory[0, 0] * VIS_SCALE, trajectory[0, 2] * VIS_SCALE, 
                'go', markersize=10, label='Start')
        ax1.plot(trajectory[-1, 0] * VIS_SCALE, trajectory[-1, 2] * VIS_SCALE, 
                'ro', markersize=10, label='End')
    
    if len(map_points) > 0:
        ax1.scatter(map_points[:, 0] * VIS_SCALE, map_points[:, 2] * VIS_SCALE,
                   c='gray', s=1, alpha=0.3, label='Map Points')
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Z')
    ax1.set_title('Top-Down View')
    ax1.legend()
    ax1.grid(True)
    ax1.axis('equal')
    
    # 3D view
    ax2 = fig.add_subplot(132, projection='3d')
    if len(trajectory) > 0:
        ax2.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 
                'b-', linewidth=2)
        ax2.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2], 
                   c='green', s=100, marker='o')
        ax2.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], 
                   c='red', s=100, marker='o')
    
    if len(map_points) > 0:
        ax2.scatter(map_points[:, 0], map_points[:, 1], map_points[:, 2],
                   c='gray', s=1, alpha=0.3)
    
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('3D View')
    
    # Statistics
    ax3 = fig.add_subplot(133)
    ax3.axis('off')
    
    stats_text = f"""
    SLAM Statistics
    ===============
    
    Total Frames: {slam.frame_count}
    Keyframes: {len(slam.keyframes)}
    Map Points: {len(slam.map_points)}
    Lost Frames: {slam.lost_count}
    
    Trajectory Length: {len(trajectory)} poses
    """
    
    if len(trajectory) > 1:
        total_dist = np.sum(np.linalg.norm(np.diff(trajectory, axis=0), axis=1))
        stats_text += f"Total Distance: {total_dist:.2f} units\n"
        stats_text += f"Final Position: [{trajectory[-1, 0]:.2f}, {trajectory[-1, 1]:.2f}, {trajectory[-1, 2]:.2f}]"
    
    ax3.text(0.1, 0.5, stats_text, transform=ax3.transAxes, 
            fontsize=10, verticalalignment='center', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Hasil disimpan: {output_path}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("SIMPLE VISUAL SLAM")
    print("="*70)
    print(f"\nKonfigurasi:")
    print(f"  - Video Source: {VIDEO_SOURCE}")
    print(f"  - Keyframe Threshold: {KEYFRAME_THRESHOLD} px")
    print(f"  - Max Map Points: {MAX_MAP_POINTS}")
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent.resolve()
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Camera matrix
    K = get_camera_matrix(FOCAL_LENGTH, PRINCIPAL_POINT)
    
    # Initialize SLAM
    slam = SimpleSLAM(K, DETECTOR_TYPE, MAX_FEATURES)
    
    # Get video source
    if VIDEO_SOURCE == 'synthetic':
        print("Creating synthetic SLAM sequence...")
        frames = create_synthetic_slam_video()
        total_frames = len(frames)
    elif VIDEO_SOURCE == 'webcam':
        cap = cv2.VideoCapture(0)
        total_frames = 200
    else:
        cap = cv2.VideoCapture(VIDEO_PATH)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Total frames: {total_frames}")
    print("\nRunning SLAM...")
    
    frame_idx = 0
    keyframe_count = 0
    
    while frame_idx < total_frames:
        if VIDEO_SOURCE == 'synthetic':
            frame = frames[frame_idx]
        else:
            ret, frame = cap.read()
            if not ret:
                break
        
        # Process frame
        start_time = time.time()
        success, is_kf = slam.process_frame(frame)
        process_time = (time.time() - start_time) * 1000
        
        if is_kf:
            keyframe_count += 1
        
        if frame_idx % 20 == 0:
            trajectory = slam.get_trajectory()
            print(f"  Frame {frame_idx}/{total_frames}, "
                  f"KF: {keyframe_count}, "
                  f"MapPts: {len(slam.map_points)}, "
                  f"Time: {process_time:.1f}ms")
        
        frame_idx += 1
    
    if VIDEO_SOURCE != 'synthetic':
        cap.release()
    
    # Final results
    print("\n" + "="*50)
    print("SLAM COMPLETED")
    print("="*50)
    
    print(f"\nTotal frames processed: {slam.frame_count}")
    print(f"Keyframes created: {len(slam.keyframes)}")
    print(f"Map points: {len(slam.map_points)}")
    print(f"Lost frames: {slam.lost_count}")
    
    trajectory = slam.get_trajectory()
    if len(trajectory) > 1:
        total_dist = np.sum(np.linalg.norm(np.diff(trajectory, axis=0), axis=1))
        print(f"\nTrajectory statistics:")
        print(f"  Total distance: {total_dist:.2f} units")
        print(f"  Start: [{trajectory[0, 0]:.2f}, {trajectory[0, 1]:.2f}, {trajectory[0, 2]:.2f}]")
        print(f"  End: [{trajectory[-1, 0]:.2f}, {trajectory[-1, 1]:.2f}, {trajectory[-1, 2]:.2f}]")
    
    # Visualize
    print("\nVisualisasi hasil...")
    visualize_slam_result(slam, output_dir / "07_slam_result.png")
    
    print("\n✓ Program selesai!")
    print("\nNote: Ini adalah implementasi SLAM sederhana untuk pembelajaran.")
    print("      Untuk aplikasi nyata, gunakan library seperti ORB-SLAM, OpenVSLAM, dll.")


if __name__ == "__main__":
    main()
