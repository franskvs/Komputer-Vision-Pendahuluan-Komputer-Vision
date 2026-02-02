"""
Praktikum 11: Structure from Motion dan SLAM
=============================================
Implementasi konsep-konsep SfM dan Visual SLAM.

Topik:
1. Epipolar Geometry
2. Fundamental & Essential Matrix Estimation
3. Triangulation
4. Two-View Reconstruction
5. Simple Visual Odometry
6. Pose Graph Optimization

Requirements:
- opencv-contrib-python
- numpy
- scipy
- matplotlib
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
import time

# ============================================================================
# BAGIAN 1: EPIPOLAR GEOMETRY
# ============================================================================

class EpipolarGeometry:
    """
    Epipolar geometry dan fundamental matrix estimation.
    """
    
    @staticmethod
    def normalize_points(points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Normalisasi koordinat untuk stabilitas numerik.
        
        Args:
            points: Nx2 array of 2D points
            
        Returns:
            Tuple of (normalized_points, transformation_matrix)
        """
        # Centroid
        centroid = np.mean(points, axis=0)
        
        # Shift ke origin
        shifted = points - centroid
        
        # Scale sehingga avg distance dari origin = sqrt(2)
        avg_dist = np.mean(np.sqrt(np.sum(shifted**2, axis=1)))
        scale = np.sqrt(2) / (avg_dist + 1e-10)
        
        # Normalization matrix
        T = np.array([
            [scale, 0, -scale * centroid[0]],
            [0, scale, -scale * centroid[1]],
            [0, 0, 1]
        ])
        
        # Normalize points
        points_h = np.hstack([points, np.ones((len(points), 1))])
        normalized = (T @ points_h.T).T
        
        return normalized[:, :2], T
    
    def eight_point_algorithm(self, pts1: np.ndarray, pts2: np.ndarray,
                              normalize: bool = True) -> np.ndarray:
        """
        Normalized 8-point algorithm untuk fundamental matrix.
        
        Args:
            pts1, pts2: Nx2 arrays of corresponding points
            normalize: Whether to use normalization
            
        Returns:
            3x3 fundamental matrix
        """
        if normalize:
            pts1_norm, T1 = self.normalize_points(pts1)
            pts2_norm, T2 = self.normalize_points(pts2)
        else:
            pts1_norm, T1 = pts1, np.eye(3)
            pts2_norm, T2 = pts2, np.eye(3)
        
        # Build constraint matrix A
        n = len(pts1)
        A = np.zeros((n, 9))
        
        for i in range(n):
            x1, y1 = pts1_norm[i]
            x2, y2 = pts2_norm[i]
            A[i] = [x2*x1, x2*y1, x2, y2*x1, y2*y1, y2, x1, y1, 1]
        
        # Solve using SVD
        _, _, Vt = np.linalg.svd(A)
        F = Vt[-1].reshape(3, 3)
        
        # Enforce rank 2
        U, S, Vt = np.linalg.svd(F)
        S[2] = 0
        F = U @ np.diag(S) @ Vt
        
        # Denormalize
        if normalize:
            F = T2.T @ F @ T1
        
        return F / F[2, 2]  # Normalize
    
    def ransac_fundamental(self, pts1: np.ndarray, pts2: np.ndarray,
                           threshold: float = 3.0, 
                           max_iterations: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        RANSAC untuk robust fundamental matrix estimation.
        
        Args:
            pts1, pts2: Corresponding points
            threshold: Inlier threshold (pixels)
            max_iterations: Maximum RANSAC iterations
            
        Returns:
            Tuple of (fundamental_matrix, inlier_mask)
        """
        n = len(pts1)
        best_F = None
        best_inliers = np.zeros(n, dtype=bool)
        best_num_inliers = 0
        
        for _ in range(max_iterations):
            # Random sample
            idx = np.random.choice(n, 8, replace=False)
            
            try:
                # Estimate F
                F = self.eight_point_algorithm(pts1[idx], pts2[idx])
                
                # Compute epipolar distance
                inliers = self.compute_inliers(pts1, pts2, F, threshold)
                num_inliers = np.sum(inliers)
                
                if num_inliers > best_num_inliers:
                    best_num_inliers = num_inliers
                    best_inliers = inliers
                    best_F = F
            except:
                continue
        
        # Recompute dengan all inliers
        if best_num_inliers >= 8:
            best_F = self.eight_point_algorithm(
                pts1[best_inliers], pts2[best_inliers]
            )
        
        return best_F, best_inliers
    
    def compute_inliers(self, pts1: np.ndarray, pts2: np.ndarray,
                        F: np.ndarray, threshold: float) -> np.ndarray:
        """
        Compute inlier mask berdasarkan epipolar distance.
        """
        pts1_h = np.hstack([pts1, np.ones((len(pts1), 1))])
        pts2_h = np.hstack([pts2, np.ones((len(pts2), 1))])
        
        # Epipolar lines di image 2
        lines2 = (F @ pts1_h.T).T
        
        # Epipolar lines di image 1
        lines1 = (F.T @ pts2_h.T).T
        
        # Distance point to line
        dist2 = np.abs(np.sum(pts2_h * lines2, axis=1)) / np.sqrt(lines2[:, 0]**2 + lines2[:, 1]**2)
        dist1 = np.abs(np.sum(pts1_h * lines1, axis=1)) / np.sqrt(lines1[:, 0]**2 + lines1[:, 1]**2)
        
        # Symmetric distance
        dist = (dist1 + dist2) / 2
        
        return dist < threshold
    
    @staticmethod
    def fundamental_to_essential(F: np.ndarray, K1: np.ndarray, 
                                  K2: np.ndarray = None) -> np.ndarray:
        """
        Convert fundamental matrix ke essential matrix.
        
        E = K2^T @ F @ K1
        """
        if K2 is None:
            K2 = K1
        return K2.T @ F @ K1
    
    @staticmethod
    def decompose_essential(E: np.ndarray) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Decompose essential matrix ke R dan t.
        
        Returns:
            List of 4 possible (R, t) solutions
        """
        U, _, Vt = np.linalg.svd(E)
        
        # Ensure proper rotation
        if np.linalg.det(U) < 0:
            U = -U
        if np.linalg.det(Vt) < 0:
            Vt = -Vt
        
        W = np.array([[0, -1, 0],
                      [1, 0, 0],
                      [0, 0, 1]])
        
        # 4 possible solutions
        solutions = []
        
        for R in [U @ W @ Vt, U @ W.T @ Vt]:
            for sign in [1, -1]:
                t = sign * U[:, 2]
                solutions.append((R, t))
        
        return solutions
    
    @staticmethod
    def draw_epipolar_lines(img1: np.ndarray, img2: np.ndarray,
                            pts1: np.ndarray, pts2: np.ndarray,
                            F: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Draw epipolar lines pada kedua images.
        """
        img1_out = img1.copy()
        img2_out = img2.copy()
        
        if len(img1_out.shape) == 2:
            img1_out = cv2.cvtColor(img1_out, cv2.COLOR_GRAY2BGR)
            img2_out = cv2.cvtColor(img2_out, cv2.COLOR_GRAY2BGR)
        
        h, w = img1.shape[:2]
        
        for pt1, pt2 in zip(pts1[:10], pts2[:10]):  # Limit untuk clarity
            color = tuple(np.random.randint(0, 255, 3).tolist())
            
            # Epipolar line di image 2
            pt1_h = np.array([pt1[0], pt1[1], 1])
            line2 = F @ pt1_h
            
            # Draw line di image 2
            x0, y0 = 0, int(-line2[2] / line2[1])
            x1, y1 = w, int(-(line2[2] + line2[0] * w) / line2[1])
            cv2.line(img2_out, (x0, y0), (x1, y1), color, 1)
            cv2.circle(img2_out, tuple(pt2.astype(int)), 5, color, -1)
            
            # Epipolar line di image 1
            pt2_h = np.array([pt2[0], pt2[1], 1])
            line1 = F.T @ pt2_h
            
            x0, y0 = 0, int(-line1[2] / line1[1])
            x1, y1 = w, int(-(line1[2] + line1[0] * w) / line1[1])
            cv2.line(img1_out, (x0, y0), (x1, y1), color, 1)
            cv2.circle(img1_out, tuple(pt1.astype(int)), 5, color, -1)
        
        return img1_out, img2_out


def demo_epipolar_geometry():
    """Demo epipolar geometry."""
    print("=" * 60)
    print("DEMO: Epipolar Geometry")
    print("=" * 60)
    
    # Create synthetic scene
    np.random.seed(42)
    
    # 3D points
    n_points = 50
    X = np.random.uniform(-2, 2, (n_points, 3))
    X[:, 2] += 5  # Depth
    
    # Camera intrinsics
    K = np.array([
        [500, 0, 320],
        [0, 500, 240],
        [0, 0, 1]
    ], dtype=float)
    
    # Camera 1 at origin
    R1 = np.eye(3)
    t1 = np.zeros(3)
    P1 = K @ np.hstack([R1, t1.reshape(-1, 1)])
    
    # Camera 2 with rotation and translation
    angle = np.radians(15)
    R2 = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    t2 = np.array([0.5, 0, 0])
    P2 = K @ np.hstack([R2, t2.reshape(-1, 1)])
    
    # Project points
    X_h = np.hstack([X, np.ones((n_points, 1))])
    pts1 = (P1 @ X_h.T).T
    pts1 = pts1[:, :2] / pts1[:, 2:3]
    
    pts2 = (P2 @ X_h.T).T
    pts2 = pts2[:, :2] / pts2[:, 2:3]
    
    # Add noise
    pts1 += np.random.normal(0, 1, pts1.shape)
    pts2 += np.random.normal(0, 1, pts2.shape)
    
    # Estimate fundamental matrix
    epi = EpipolarGeometry()
    
    # 8-point algorithm
    F_8pt = epi.eight_point_algorithm(pts1, pts2)
    
    # RANSAC
    F_ransac, inliers = epi.ransac_fundamental(pts1, pts2)
    
    # OpenCV comparison
    F_cv, mask_cv = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
    
    print(f"Number of points: {n_points}")
    print(f"RANSAC inliers: {np.sum(inliers)}")
    print(f"OpenCV inliers: {np.sum(mask_cv)}")
    
    # Essential matrix
    E = epi.fundamental_to_essential(F_ransac, K)
    solutions = epi.decompose_essential(E)
    
    print(f"\nNumber of E decomposition solutions: {len(solutions)}")
    
    # Create synthetic images
    h, w = 480, 640
    img1 = np.ones((h, w), dtype=np.uint8) * 200
    img2 = img1.copy()
    
    # Draw points
    for pt in pts1:
        if 0 <= pt[0] < w and 0 <= pt[1] < h:
            cv2.circle(img1, tuple(pt.astype(int)), 3, 0, -1)
    for pt in pts2:
        if 0 <= pt[0] < w and 0 <= pt[1] < h:
            cv2.circle(img2, tuple(pt.astype(int)), 3, 0, -1)
    
    # Draw epipolar lines
    img1_epi, img2_epi = epi.draw_epipolar_lines(img1, img2, pts1, pts2, F_ransac)
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    axes[0].imshow(img1_epi)
    axes[0].set_title('Image 1 with Epipolar Lines')
    axes[0].axis('off')
    
    axes[1].imshow(img2_epi)
    axes[1].set_title('Image 2 with Epipolar Lines')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_epipolar.png', dpi=150)
    plt.show()
    
    print("\nHasil disimpan: output_epipolar.png")


# ============================================================================
# BAGIAN 2: TRIANGULATION
# ============================================================================

class Triangulation:
    """
    3D point triangulation dari multiple views.
    """
    
    @staticmethod
    def linear_triangulation(P1: np.ndarray, P2: np.ndarray,
                             pt1: np.ndarray, pt2: np.ndarray) -> np.ndarray:
        """
        DLT triangulation untuk single point.
        
        Args:
            P1, P2: 3x4 projection matrices
            pt1, pt2: 2D points (x, y)
            
        Returns:
            3D point (x, y, z)
        """
        x1, y1 = pt1
        x2, y2 = pt2
        
        # Build A matrix
        A = np.array([
            x1 * P1[2] - P1[0],
            y1 * P1[2] - P1[1],
            x2 * P2[2] - P2[0],
            y2 * P2[2] - P2[1]
        ])
        
        # Solve dengan SVD
        _, _, Vt = np.linalg.svd(A)
        X = Vt[-1]
        
        # Convert dari homogeneous
        return X[:3] / X[3]
    
    def triangulate_points(self, P1: np.ndarray, P2: np.ndarray,
                           pts1: np.ndarray, pts2: np.ndarray) -> np.ndarray:
        """
        Triangulate multiple points.
        """
        n = len(pts1)
        points_3d = np.zeros((n, 3))
        
        for i in range(n):
            points_3d[i] = self.linear_triangulation(P1, P2, pts1[i], pts2[i])
        
        return points_3d
    
    @staticmethod
    def triangulate_opencv(P1: np.ndarray, P2: np.ndarray,
                           pts1: np.ndarray, pts2: np.ndarray) -> np.ndarray:
        """
        OpenCV triangulation.
        """
        pts1_2d = pts1.T.astype(np.float64)
        pts2_2d = pts2.T.astype(np.float64)
        
        X = cv2.triangulatePoints(P1, P2, pts1_2d, pts2_2d)
        
        # Convert dari homogeneous
        return (X[:3] / X[3]).T
    
    @staticmethod
    def compute_reprojection_error(X: np.ndarray, P: np.ndarray, 
                                    pt: np.ndarray) -> float:
        """
        Compute reprojection error untuk single point.
        """
        X_h = np.append(X, 1)
        projected = P @ X_h
        projected = projected[:2] / projected[2]
        
        return np.linalg.norm(projected - pt)


# ============================================================================
# BAGIAN 3: TWO-VIEW RECONSTRUCTION
# ============================================================================

class TwoViewReconstruction:
    """
    Full two-view 3D reconstruction pipeline.
    """
    
    def __init__(self, K: np.ndarray):
        """
        Args:
            K: 3x3 camera intrinsic matrix
        """
        self.K = K
        self.epi = EpipolarGeometry()
        self.tri = Triangulation()
    
    def extract_and_match_features(self, img1: np.ndarray, img2: np.ndarray,
                                    method: str = 'orb'
                                    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract dan match features antara dua images.
        """
        if method == 'orb':
            detector = cv2.ORB_create(nfeatures=2000)
            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        else:
            detector = cv2.SIFT_create()
            matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        
        kp1, desc1 = detector.detectAndCompute(img1, None)
        kp2, desc2 = detector.detectAndCompute(img2, None)
        
        matches = matcher.match(desc1, desc2)
        matches = sorted(matches, key=lambda x: x.distance)
        
        pts1 = np.array([kp1[m.queryIdx].pt for m in matches])
        pts2 = np.array([kp2[m.trainIdx].pt for m in matches])
        
        return pts1, pts2
    
    def recover_pose(self, pts1: np.ndarray, pts2: np.ndarray
                     ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Recover camera pose dari point correspondences.
        
        Returns:
            Tuple of (R, t, inlier_mask)
        """
        # Estimate essential matrix
        E, mask = cv2.findEssentialMat(pts1, pts2, self.K, cv2.RANSAC, 0.999, 1.0)
        
        # Recover pose
        _, R, t, mask_pose = cv2.recoverPose(E, pts1, pts2, self.K, mask)
        
        return R, t.flatten(), mask_pose.flatten() > 0
    
    def select_best_solution(self, solutions: List[Tuple[np.ndarray, np.ndarray]],
                              pts1: np.ndarray, pts2: np.ndarray
                              ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Select best R, t dari 4 solutions dengan cheirality check.
        """
        P1 = self.K @ np.hstack([np.eye(3), np.zeros((3, 1))])
        
        best_count = 0
        best_R, best_t = None, None
        
        for R, t in solutions:
            P2 = self.K @ np.hstack([R, t.reshape(-1, 1)])
            
            # Triangulate
            points_3d = self.tri.triangulate_points(P1, P2, pts1, pts2)
            
            # Check cheirality (points in front of both cameras)
            # Camera 1: z > 0
            in_front_1 = points_3d[:, 2] > 0
            
            # Camera 2: (R @ X + t)[2] > 0
            X_cam2 = (R @ points_3d.T).T + t
            in_front_2 = X_cam2[:, 2] > 0
            
            count = np.sum(in_front_1 & in_front_2)
            
            if count > best_count:
                best_count = count
                best_R, best_t = R, t
        
        return best_R, best_t
    
    def reconstruct(self, img1: np.ndarray, img2: np.ndarray
                   ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Full reconstruction pipeline.
        
        Returns:
            Tuple of (points_3d, R, t, inliers)
        """
        # Extract features
        pts1, pts2 = self.extract_and_match_features(img1, img2)
        print(f"Found {len(pts1)} matches")
        
        # Recover pose
        R, t, inliers = self.recover_pose(pts1, pts2)
        pts1_inlier = pts1[inliers]
        pts2_inlier = pts2[inliers]
        print(f"Inliers: {np.sum(inliers)}")
        
        # Triangulate
        P1 = self.K @ np.hstack([np.eye(3), np.zeros((3, 1))])
        P2 = self.K @ np.hstack([R, t.reshape(-1, 1)])
        
        points_3d = self.tri.triangulate_opencv(P1, P2, pts1_inlier, pts2_inlier)
        
        return points_3d, R, t, inliers


def demo_two_view_reconstruction():
    """Demo two-view reconstruction."""
    print("\n" + "=" * 60)
    print("DEMO: Two-View Reconstruction")
    print("=" * 60)
    
    # Create synthetic scene
    np.random.seed(42)
    
    # 3D points (cube + random)
    cube_points = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ], dtype=float)
    random_points = np.random.uniform(-1.5, 1.5, (50, 3))
    X_true = np.vstack([cube_points, random_points])
    X_true[:, 2] += 5  # Move in front of camera
    
    # Camera intrinsics
    K = np.array([
        [500, 0, 320],
        [0, 500, 240],
        [0, 0, 1]
    ], dtype=float)
    
    # Camera poses
    R1 = np.eye(3)
    t1 = np.zeros(3)
    
    angle = np.radians(20)
    R2 = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    t2 = np.array([0.8, 0, 0])
    
    # Project points
    P1 = K @ np.hstack([R1, t1.reshape(-1, 1)])
    P2 = K @ np.hstack([R2, t2.reshape(-1, 1)])
    
    X_h = np.hstack([X_true, np.ones((len(X_true), 1))])
    
    pts1 = (P1 @ X_h.T).T
    pts1 = pts1[:, :2] / pts1[:, 2:3]
    
    pts2 = (P2 @ X_h.T).T
    pts2 = pts2[:, :2] / pts2[:, 2:3]
    
    # Add noise
    pts1 += np.random.normal(0, 0.5, pts1.shape)
    pts2 += np.random.normal(0, 0.5, pts2.shape)
    
    # Create synthetic images
    h, w = 480, 640
    img1 = np.ones((h, w), dtype=np.uint8) * 128
    img2 = img1.copy()
    
    for pt in pts1:
        x, y = int(pt[0]), int(pt[1])
        if 0 <= x < w and 0 <= y < h:
            cv2.circle(img1, (x, y), 5, 255, -1)
    
    for pt in pts2:
        x, y = int(pt[0]), int(pt[1])
        if 0 <= x < w and 0 <= y < h:
            cv2.circle(img2, (x, y), 5, 255, -1)
    
    # Reconstruction
    reconstructor = TwoViewReconstruction(K)
    
    # Recover pose
    R_est, t_est, inliers = reconstructor.recover_pose(pts1, pts2)
    
    # Triangulate
    tri = Triangulation()
    X_est = tri.triangulate_opencv(P1, K @ np.hstack([R_est, t_est.reshape(-1, 1)]),
                                    pts1[inliers], pts2[inliers])
    
    # Align dengan scale (t hanya direction)
    scale = np.linalg.norm(t2) / np.linalg.norm(t_est)
    t_est_scaled = t_est * scale
    
    print(f"\nTrue translation: {t2}")
    print(f"Estimated translation (normalized): {t_est}")
    print(f"Estimated translation (scaled): {t_est_scaled}")
    
    # Visualize 3D reconstruction
    fig = plt.figure(figsize=(15, 5))
    
    # Image 1
    ax1 = fig.add_subplot(131)
    ax1.imshow(img1, cmap='gray')
    ax1.set_title('Image 1')
    ax1.axis('off')
    
    # Image 2
    ax2 = fig.add_subplot(132)
    ax2.imshow(img2, cmap='gray')
    ax2.set_title('Image 2')
    ax2.axis('off')
    
    # 3D reconstruction
    ax3 = fig.add_subplot(133, projection='3d')
    
    # True points
    ax3.scatter(X_true[:, 0], X_true[:, 1], X_true[:, 2], 
               c='blue', marker='o', label='Ground Truth', alpha=0.5)
    
    # Estimated points (setelah scaling)
    if len(X_est) > 0:
        X_est_scaled = X_est * scale
        ax3.scatter(X_est_scaled[:, 0], X_est_scaled[:, 1], X_est_scaled[:, 2],
                   c='red', marker='^', label='Reconstructed', alpha=0.5)
    
    # Cameras
    ax3.scatter([0], [0], [0], c='green', marker='s', s=100, label='Camera 1')
    ax3.scatter([t2[0]], [t2[1]], [t2[2]], c='purple', marker='s', s=100, label='Camera 2')
    
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.set_title('3D Reconstruction')
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig('output_two_view.png', dpi=150)
    plt.show()
    
    print("\nHasil disimpan: output_two_view.png")


# ============================================================================
# BAGIAN 4: VISUAL ODOMETRY (Simplified)
# ============================================================================

class SimpleVisualOdometry:
    """
    Simple monocular visual odometry.
    """
    
    def __init__(self, K: np.ndarray):
        self.K = K
        self.detector = cv2.ORB_create(nfeatures=2000)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        
        self.prev_frame = None
        self.prev_kp = None
        self.prev_desc = None
        
        # Trajectory
        self.trajectory = [np.eye(4)]  # List of 4x4 pose matrices
        self.R_total = np.eye(3)
        self.t_total = np.zeros((3, 1))
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Process single frame.
        
        Returns:
            Tuple of (R, t) relative to previous frame
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        # Detect features
        kp, desc = self.detector.detectAndCompute(gray, None)
        
        R, t = np.eye(3), np.zeros((3, 1))
        
        if self.prev_frame is not None and self.prev_desc is not None:
            # Match features
            matches = self.matcher.knnMatch(self.prev_desc, desc, k=2)
            
            # Ratio test
            good_matches = []
            for m_n in matches:
                if len(m_n) == 2:
                    m, n = m_n
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            
            if len(good_matches) >= 8:
                pts1 = np.float32([self.prev_kp[m.queryIdx].pt for m in good_matches])
                pts2 = np.float32([kp[m.trainIdx].pt for m in good_matches])
                
                # Essential matrix
                E, mask = cv2.findEssentialMat(pts1, pts2, self.K, cv2.RANSAC, 0.999, 1.0)
                
                if E is not None:
                    # Recover pose
                    _, R, t, mask_pose = cv2.recoverPose(E, pts1, pts2, self.K)
                    
                    # Update total pose
                    self.t_total = self.t_total + self.R_total @ t
                    self.R_total = R @ self.R_total
                    
                    # Store pose
                    pose = np.eye(4)
                    pose[:3, :3] = self.R_total
                    pose[:3, 3] = self.t_total.flatten()
                    self.trajectory.append(pose)
        
        # Update previous
        self.prev_frame = gray
        self.prev_kp = kp
        self.prev_desc = desc
        
        return R, t
    
    def get_trajectory(self) -> np.ndarray:
        """Get trajectory as Nx3 array of positions."""
        positions = []
        for pose in self.trajectory:
            positions.append(pose[:3, 3])
        return np.array(positions)
    
    def reset(self):
        """Reset odometry."""
        self.prev_frame = None
        self.prev_kp = None
        self.prev_desc = None
        self.trajectory = [np.eye(4)]
        self.R_total = np.eye(3)
        self.t_total = np.zeros((3, 1))


def demo_visual_odometry():
    """Demo simple visual odometry."""
    print("\n" + "=" * 60)
    print("DEMO: Simple Visual Odometry")
    print("=" * 60)
    
    # Camera intrinsics
    K = np.array([
        [500, 0, 320],
        [0, 500, 240],
        [0, 0, 1]
    ], dtype=float)
    
    vo = SimpleVisualOdometry(K)
    
    # Simulate circular motion
    n_frames = 100
    radius = 2.0
    true_positions = []
    
    # Create 3D scene
    np.random.seed(42)
    scene_points = np.random.uniform(-5, 5, (200, 3))
    scene_points[:, 2] = np.abs(scene_points[:, 2]) + 2  # Ensure positive Z
    
    print("Simulating camera motion...")
    
    for i in range(n_frames):
        # Camera position on circle
        angle = 2 * np.pi * i / n_frames
        cx = radius * np.cos(angle)
        cz = radius * np.sin(angle)
        cy = 0
        
        true_positions.append([cx, cy, cz])
        
        # Camera rotation (looking at center)
        R = np.array([
            [np.cos(angle + np.pi), 0, np.sin(angle + np.pi)],
            [0, 1, 0],
            [-np.sin(angle + np.pi), 0, np.cos(angle + np.pi)]
        ])
        t = -R @ np.array([cx, cy, cz])
        
        # Project scene points
        P = K @ np.hstack([R, t.reshape(-1, 1)])
        X_h = np.hstack([scene_points, np.ones((len(scene_points), 1))])
        pts_2d = (P @ X_h.T).T
        pts_2d = pts_2d[:, :2] / pts_2d[:, 2:3]
        
        # Filter valid points
        valid = (pts_2d[:, 0] >= 0) & (pts_2d[:, 0] < 640) & \
                (pts_2d[:, 1] >= 0) & (pts_2d[:, 1] < 480)
        pts_2d = pts_2d[valid]
        
        # Create frame
        frame = np.zeros((480, 640), dtype=np.uint8)
        for pt in pts_2d:
            x, y = int(pt[0]), int(pt[1])
            cv2.circle(frame, (x, y), 3, 255, -1)
        
        # Add some texture
        frame = cv2.GaussianBlur(frame, (3, 3), 0)
        noise = np.random.normal(0, 10, frame.shape).astype(np.uint8)
        frame = cv2.add(frame, noise)
        
        # Process frame
        vo.process_frame(frame)
    
    true_positions = np.array(true_positions)
    estimated_positions = vo.get_trajectory()
    
    # Scale estimated trajectory (monocular scale ambiguity)
    scale = np.linalg.norm(true_positions[1] - true_positions[0]) / \
            (np.linalg.norm(estimated_positions[1] - estimated_positions[0]) + 1e-10)
    estimated_positions_scaled = estimated_positions * scale
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Top view (X-Z plane)
    axes[0].plot(true_positions[:, 0], true_positions[:, 2], 'b-', 
                 label='Ground Truth', linewidth=2)
    axes[0].plot(estimated_positions_scaled[:, 0], estimated_positions_scaled[:, 2], 
                 'r--', label='Estimated', linewidth=2)
    axes[0].scatter([true_positions[0, 0]], [true_positions[0, 2]], 
                   c='green', s=100, label='Start', zorder=5)
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Z')
    axes[0].set_title('Top View (X-Z Plane)')
    axes[0].legend()
    axes[0].axis('equal')
    axes[0].grid(True)
    
    # 3D view
    ax3d = fig.add_subplot(122, projection='3d')
    ax3d.plot(true_positions[:, 0], true_positions[:, 1], true_positions[:, 2],
              'b-', label='Ground Truth', linewidth=2)
    ax3d.plot(estimated_positions_scaled[:, 0], estimated_positions_scaled[:, 1], 
              estimated_positions_scaled[:, 2], 'r--', label='Estimated', linewidth=2)
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.set_title('3D Trajectory')
    ax3d.legend()
    
    plt.tight_layout()
    plt.savefig('output_visual_odometry.png', dpi=150)
    plt.show()
    
    print(f"Number of frames: {n_frames}")
    print(f"Scale factor: {scale:.4f}")
    print("Hasil disimpan: output_visual_odometry.png")


# ============================================================================
# BAGIAN 5: POSE GRAPH OPTIMIZATION (Simplified)
# ============================================================================

class SimplePoseGraph:
    """
    Simple pose graph optimization using least squares.
    """
    
    def __init__(self):
        self.poses = []  # List of (x, y, theta)
        self.edges = []  # List of (i, j, dx, dy, dtheta)
    
    def add_pose(self, x: float, y: float, theta: float):
        """Add a pose node."""
        self.poses.append([x, y, theta])
    
    def add_edge(self, i: int, j: int, dx: float, dy: float, dtheta: float):
        """
        Add relative pose constraint between poses i and j.
        """
        self.edges.append((i, j, dx, dy, dtheta))
    
    def optimize(self, num_iterations: int = 50) -> np.ndarray:
        """
        Optimize pose graph using Gauss-Newton.
        
        Returns:
            Optimized poses as Nx3 array
        """
        poses = np.array(self.poses, dtype=float)
        n_poses = len(poses)
        
        for iteration in range(num_iterations):
            # Build H and b
            H = np.zeros((n_poses * 3, n_poses * 3))
            b = np.zeros(n_poses * 3)
            
            total_error = 0
            
            for i, j, dx, dy, dtheta in self.edges:
                # Current poses
                xi, yi, ti = poses[i]
                xj, yj, tj = poses[j]
                
                # Predicted relative pose
                c, s = np.cos(ti), np.sin(ti)
                dx_pred = c * (xj - xi) + s * (yj - yi)
                dy_pred = -s * (xj - xi) + c * (yj - yi)
                dtheta_pred = self.normalize_angle(tj - ti)
                
                # Error
                ex = dx_pred - dx
                ey = dy_pred - dy
                etheta = self.normalize_angle(dtheta_pred - dtheta)
                
                error = np.array([ex, ey, etheta])
                total_error += np.sum(error ** 2)
                
                # Jacobians
                Ji = np.array([
                    [c, s, -(xj - xi) * s + (yj - yi) * c],
                    [-s, c, -(xj - xi) * c - (yj - yi) * s],
                    [0, 0, -1]
                ])
                
                Jj = np.array([
                    [-c, -s, 0],
                    [s, -c, 0],
                    [0, 0, 1]
                ])
                
                # Information matrix (identity for simplicity)
                omega = np.eye(3)
                
                # Update H and b
                ii = i * 3
                jj = j * 3
                
                H[ii:ii+3, ii:ii+3] += Ji.T @ omega @ Ji
                H[ii:ii+3, jj:jj+3] += Ji.T @ omega @ Jj
                H[jj:jj+3, ii:ii+3] += Jj.T @ omega @ Ji
                H[jj:jj+3, jj:jj+3] += Jj.T @ omega @ Jj
                
                b[ii:ii+3] += Ji.T @ omega @ error
                b[jj:jj+3] += Jj.T @ omega @ error
            
            # Fix first pose
            H[0:3, 0:3] += np.eye(3) * 1000
            
            # Solve
            try:
                delta = np.linalg.solve(H, -b)
                poses += delta.reshape(-1, 3)
                poses[:, 2] = np.array([self.normalize_angle(t) for t in poses[:, 2]])
            except np.linalg.LinAlgError:
                break
        
        return poses
    
    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Normalize angle ke [-pi, pi]."""
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle


def demo_pose_graph():
    """Demo pose graph optimization."""
    print("\n" + "=" * 60)
    print("DEMO: Pose Graph Optimization")
    print("=" * 60)
    
    # Create ground truth trajectory (square)
    gt_poses = [
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2, 1, np.pi/2],
        [2, 2, np.pi/2],
        [1, 2, np.pi],
        [0, 2, np.pi],
        [0, 1, -np.pi/2],
    ]
    gt_poses = np.array(gt_poses)
    
    # Create noisy odometry measurements
    np.random.seed(42)
    graph = SimplePoseGraph()
    
    # Add initial pose
    graph.add_pose(0, 0, 0)
    
    accumulated = [0, 0, 0]
    noisy_poses = [[0, 0, 0]]
    
    for i in range(len(gt_poses) - 1):
        # True relative pose
        dx_true = gt_poses[i+1, 0] - gt_poses[i, 0]
        dy_true = gt_poses[i+1, 1] - gt_poses[i, 1]
        dtheta_true = gt_poses[i+1, 2] - gt_poses[i, 2]
        
        # Add noise to odometry
        dx = dx_true + np.random.normal(0, 0.1)
        dy = dy_true + np.random.normal(0, 0.1)
        dtheta = dtheta_true + np.random.normal(0, 0.05)
        
        # Accumulate
        c, s = np.cos(accumulated[2]), np.sin(accumulated[2])
        accumulated[0] += c * dx - s * dy
        accumulated[1] += s * dx + c * dy
        accumulated[2] += dtheta
        
        graph.add_pose(accumulated[0], accumulated[1], accumulated[2])
        noisy_poses.append(accumulated.copy())
        
        # Add odometry edge
        graph.add_edge(i, i+1, dx, dy, dtheta)
    
    noisy_poses = np.array(noisy_poses)
    
    # Add loop closure constraint (pose 0 ↔ pose 7)
    # True relative pose should bring us back
    dx_loop = 0 - gt_poses[-1, 0]
    dy_loop = 0 - gt_poses[-1, 1]
    dtheta_loop = 0 - gt_poses[-1, 2]
    
    c, s = np.cos(gt_poses[-1, 2]), np.sin(gt_poses[-1, 2])
    dx_local = c * dx_loop + s * dy_loop
    dy_local = -s * dx_loop + c * dy_loop
    
    graph.add_edge(len(gt_poses)-1, 0, dx_local, dy_local, dtheta_loop)
    
    # Optimize
    optimized_poses = graph.optimize(num_iterations=100)
    
    # Visualize
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Ground truth
    axes[0].plot(gt_poses[:, 0], gt_poses[:, 1], 'b-o', label='Ground Truth')
    axes[0].set_title('Ground Truth')
    axes[0].axis('equal')
    axes[0].grid(True)
    
    # Noisy odometry
    axes[1].plot(noisy_poses[:, 0], noisy_poses[:, 1], 'r-o', label='Noisy Odometry')
    axes[1].set_title('Noisy Odometry (Before Optimization)')
    axes[1].axis('equal')
    axes[1].grid(True)
    
    # Optimized
    axes[2].plot(gt_poses[:, 0], gt_poses[:, 1], 'b--', alpha=0.5, label='Ground Truth')
    axes[2].plot(optimized_poses[:, 0], optimized_poses[:, 1], 'g-o', label='Optimized')
    axes[2].set_title('After Pose Graph Optimization')
    axes[2].legend()
    axes[2].axis('equal')
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('output_pose_graph.png', dpi=150)
    plt.show()
    
    # Error analysis
    error_before = np.mean(np.linalg.norm(noisy_poses[:, :2] - gt_poses[:, :2], axis=1))
    error_after = np.mean(np.linalg.norm(optimized_poses[:, :2] - gt_poses[:, :2], axis=1))
    
    print(f"Mean position error (before): {error_before:.4f}")
    print(f"Mean position error (after): {error_after:.4f}")
    print(f"Improvement: {(error_before - error_after) / error_before * 100:.1f}%")
    print("Hasil disimpan: output_pose_graph.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function."""
    print("=" * 70)
    print("PRAKTIKUM 11: STRUCTURE FROM MOTION DAN SLAM")
    print("=" * 70)
    
    demos = [
        ("1. Epipolar Geometry", demo_epipolar_geometry),
        ("2. Two-View Reconstruction", demo_two_view_reconstruction),
        ("3. Visual Odometry", demo_visual_odometry),
        ("4. Pose Graph Optimization", demo_pose_graph),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for i, (name, _) in enumerate(demos):
        print(f"  {name}")
    print("  5. Jalankan Semua")
    print("  0. Keluar")
    
    while True:
        try:
            choice = input("\nMasukkan pilihan (0-5): ").strip()
            
            if choice == '0':
                print("Terima kasih!")
                break
            elif choice == '5':
                for name, func in demos:
                    print(f"\n>>> Menjalankan {name}...")
                    func()
                break
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(demos):
                    demos[idx][1]()
                else:
                    print("Pilihan tidak valid!")
        except ValueError:
            print("Input tidak valid!")
        except KeyboardInterrupt:
            print("\nDibatalkan.")
            break


if __name__ == "__main__":
    main()
