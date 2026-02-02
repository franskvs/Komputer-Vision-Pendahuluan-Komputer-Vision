"""
Praktikum 08: Image Alignment dan Stitching
============================================
Implementasi berbagai teknik image alignment dan panorama stitching.

Topik:
1. Lucas-Kanade Alignment
2. Direct Image Alignment dengan ECC
3. Feature-Based Alignment
4. Homography Estimation dengan RANSAC
5. Panorama Stitching
6. Multi-Band Blending

Requirements:
- opencv-contrib-python
- numpy
- matplotlib
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
import os

# ============================================================================
# BAGIAN 1: TRANSFORMASI 2D
# ============================================================================

class Transform2D:
    """Kelas untuk berbagai transformasi 2D."""
    
    @staticmethod
    def translation_matrix(tx: float, ty: float) -> np.ndarray:
        """
        Buat matrix translasi.
        
        Args:
            tx: Translation x
            ty: Translation y
            
        Returns:
            Matrix 3x3
        """
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=np.float64)
    
    @staticmethod
    def rotation_matrix(theta: float, center: Tuple[float, float] = (0, 0)) -> np.ndarray:
        """
        Buat matrix rotasi.
        
        Args:
            theta: Sudut rotasi dalam radian
            center: Pusat rotasi
            
        Returns:
            Matrix 3x3
        """
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        cx, cy = center
        
        # Rotate around center
        T1 = Transform2D.translation_matrix(-cx, -cy)
        R = np.array([
            [cos_t, -sin_t, 0],
            [sin_t, cos_t, 0],
            [0, 0, 1]
        ], dtype=np.float64)
        T2 = Transform2D.translation_matrix(cx, cy)
        
        return T2 @ R @ T1
    
    @staticmethod
    def scale_matrix(sx: float, sy: float = None) -> np.ndarray:
        """
        Buat matrix scaling.
        
        Args:
            sx: Scale x
            sy: Scale y (default = sx untuk uniform)
            
        Returns:
            Matrix 3x3
        """
        if sy is None:
            sy = sx
            
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ], dtype=np.float64)
    
    @staticmethod
    def similarity_matrix(scale: float, theta: float, tx: float, ty: float) -> np.ndarray:
        """
        Buat matrix similarity transform.
        
        Args:
            scale: Uniform scale
            theta: Rotation angle (radian)
            tx, ty: Translation
            
        Returns:
            Matrix 3x3
        """
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        
        return np.array([
            [scale * cos_t, -scale * sin_t, tx],
            [scale * sin_t, scale * cos_t, ty],
            [0, 0, 1]
        ], dtype=np.float64)
    
    @staticmethod
    def affine_matrix(params: np.ndarray) -> np.ndarray:
        """
        Buat matrix affine dari 6 parameter.
        
        Args:
            params: [a11, a12, a21, a22, tx, ty]
            
        Returns:
            Matrix 3x3
        """
        a11, a12, a21, a22, tx, ty = params
        
        return np.array([
            [a11, a12, tx],
            [a21, a22, ty],
            [0, 0, 1]
        ], dtype=np.float64)
    
    @staticmethod
    def apply_transform(image: np.ndarray, H: np.ndarray, 
                       output_size: Tuple[int, int] = None) -> np.ndarray:
        """
        Terapkan transformasi ke gambar.
        
        Args:
            image: Input image
            H: Transformation matrix (3x3)
            output_size: (width, height) output
            
        Returns:
            Transformed image
        """
        if output_size is None:
            output_size = (image.shape[1], image.shape[0])
            
        # Untuk affine (2x3 matrix)
        if H.shape[0] == 3:
            return cv2.warpPerspective(image, H, output_size)
        else:
            return cv2.warpAffine(image, H, output_size)


def demo_transformations():
    """Demo berbagai transformasi 2D."""
    print("=" * 60)
    print("DEMO: Transformasi 2D")
    print("=" * 60)
    
    # Buat gambar test sederhana
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), -1)
    cv2.circle(img, (150, 150), 30, (255, 0, 0), -1)
    cv2.putText(img, "CV", (120, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Berbagai transformasi
    transforms = {
        'Original': np.eye(3),
        'Translation': Transform2D.translation_matrix(50, 30),
        'Rotation 30°': Transform2D.rotation_matrix(np.radians(30), (150, 150)),
        'Scale 0.7x': Transform2D.scale_matrix(0.7),
        'Similarity': Transform2D.similarity_matrix(0.8, np.radians(15), 30, 20),
    }
    
    # Terapkan dan visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.ravel()
    
    for idx, (name, H) in enumerate(transforms.items()):
        if idx < len(axes):
            transformed = Transform2D.apply_transform(img, H)
            axes[idx].imshow(cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB))
            axes[idx].set_title(name)
            axes[idx].axis('off')
    
    # Homography example
    # 4 titik source dan destination
    src_pts = np.float32([[100, 100], [200, 100], [200, 200], [100, 200]])
    dst_pts = np.float32([[80, 120], [220, 100], [200, 220], [120, 200]])
    H_homo = cv2.getPerspectiveTransform(src_pts, dst_pts)
    transformed = Transform2D.apply_transform(img, H_homo)
    axes[5].imshow(cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB))
    axes[5].set_title('Homography')
    axes[5].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_transformations.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_transformations.png")


# ============================================================================
# BAGIAN 2: LUCAS-KANADE ALIGNMENT
# ============================================================================

class LucasKanadeTracker:
    """
    Implementasi Lucas-Kanade optical flow tracker.
    """
    
    def __init__(self, win_size: int = 21, max_level: int = 3):
        """
        Args:
            win_size: Window size untuk tracking
            max_level: Level pyramid maksimum
        """
        self.win_size = win_size
        self.max_level = max_level
        
        # Parameter untuk cv2.calcOpticalFlowPyrLK
        self.lk_params = dict(
            winSize=(win_size, win_size),
            maxLevel=max_level,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01)
        )
    
    def track_points(self, prev_gray: np.ndarray, curr_gray: np.ndarray,
                    prev_pts: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Track titik-titik dari frame sebelumnya ke current.
        
        Args:
            prev_gray: Previous grayscale frame
            curr_gray: Current grayscale frame
            prev_pts: Points to track (Nx1x2 or Nx2)
            
        Returns:
            curr_pts: Tracked points
            status: Status array (1=found, 0=lost)
            error: Error for each point
        """
        if prev_pts.ndim == 2:
            prev_pts = prev_pts.reshape(-1, 1, 2).astype(np.float32)
        
        # Forward tracking
        curr_pts, status, error = cv2.calcOpticalFlowPyrLK(
            prev_gray, curr_gray, prev_pts, None, **self.lk_params
        )
        
        return curr_pts, status.ravel(), error.ravel()
    
    def track_with_backward_check(self, prev_gray: np.ndarray, curr_gray: np.ndarray,
                                  prev_pts: np.ndarray, threshold: float = 1.0
                                  ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Track dengan forward-backward consistency check.
        
        Args:
            prev_gray: Previous grayscale frame
            curr_gray: Current grayscale frame
            prev_pts: Points to track
            threshold: Maximum backward error
            
        Returns:
            curr_pts: Tracked points (valid only)
            prev_pts_valid: Corresponding previous points
            mask: Valid mask
        """
        if prev_pts.ndim == 2:
            prev_pts = prev_pts.reshape(-1, 1, 2).astype(np.float32)
        
        # Forward tracking
        curr_pts, st_fwd, _ = cv2.calcOpticalFlowPyrLK(
            prev_gray, curr_gray, prev_pts, None, **self.lk_params
        )
        
        # Backward tracking
        prev_pts_back, st_bwd, _ = cv2.calcOpticalFlowPyrLK(
            curr_gray, prev_gray, curr_pts, None, **self.lk_params
        )
        
        # Compute backward error
        diff = np.linalg.norm(prev_pts - prev_pts_back, axis=2).ravel()
        
        # Valid points: found in both directions and low backward error
        mask = (st_fwd.ravel() == 1) & (st_bwd.ravel() == 1) & (diff < threshold)
        
        return curr_pts[mask], prev_pts[mask], mask


class DirectAlignment:
    """
    Direct image alignment menggunakan berbagai metode.
    """
    
    @staticmethod
    def align_ecc(template: np.ndarray, image: np.ndarray,
                  warp_mode: int = cv2.MOTION_EUCLIDEAN,
                  num_iterations: int = 1000,
                  epsilon: float = 1e-6) -> Tuple[np.ndarray, float]:
        """
        Align image ke template menggunakan ECC algorithm.
        
        Args:
            template: Template/reference image
            image: Image to align
            warp_mode: Type of transformation
                - cv2.MOTION_TRANSLATION
                - cv2.MOTION_EUCLIDEAN
                - cv2.MOTION_AFFINE
                - cv2.MOTION_HOMOGRAPHY
            num_iterations: Maximum iterations
            epsilon: Convergence threshold
            
        Returns:
            warp_matrix: Estimated transformation
            ecc_value: Final ECC value
        """
        # Convert to grayscale if needed
        if len(template.shape) == 3:
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        else:
            template_gray = template
            
        if len(image.shape) == 3:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        
        # Initialize warp matrix
        if warp_mode == cv2.MOTION_HOMOGRAPHY:
            warp_matrix = np.eye(3, 3, dtype=np.float32)
        else:
            warp_matrix = np.eye(2, 3, dtype=np.float32)
        
        # Criteria
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                   num_iterations, epsilon)
        
        # Run ECC
        try:
            ecc_value, warp_matrix = cv2.findTransformECC(
                template_gray, image_gray, warp_matrix, warp_mode, criteria
            )
        except cv2.error:
            print("ECC alignment failed!")
            ecc_value = 0
        
        return warp_matrix, ecc_value
    
    @staticmethod
    def apply_warp(image: np.ndarray, warp_matrix: np.ndarray,
                   size: Tuple[int, int]) -> np.ndarray:
        """Apply warp matrix ke image."""
        if warp_matrix.shape[0] == 3:
            return cv2.warpPerspective(image, warp_matrix, size,
                                       flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        else:
            return cv2.warpAffine(image, warp_matrix, size,
                                  flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)


def demo_direct_alignment():
    """Demo direct image alignment dengan ECC."""
    print("\n" + "=" * 60)
    print("DEMO: Direct Image Alignment (ECC)")
    print("=" * 60)
    
    # Buat gambar test
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (150, 150), (0, 255, 0), -1)
    cv2.circle(img, (280, 150), 50, (255, 0, 0), -1)
    cv2.putText(img, "TEST", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Buat versi transformed (simulate misalignment)
    H_true = Transform2D.similarity_matrix(1.0, np.radians(5), 15, -10)
    img_warped = cv2.warpPerspective(img, H_true, (400, 300))
    
    # Align menggunakan ECC
    aligner = DirectAlignment()
    
    # Test berbagai motion models
    modes = {
        'Translation': cv2.MOTION_TRANSLATION,
        'Euclidean': cv2.MOTION_EUCLIDEAN,
        'Affine': cv2.MOTION_AFFINE,
        'Homography': cv2.MOTION_HOMOGRAPHY
    }
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Template (Reference)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img_warped, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Misaligned Image')
    axes[0, 1].axis('off')
    
    plot_idx = 2
    for name, mode in modes.items():
        warp_matrix, ecc = aligner.align_ecc(img, img_warped, warp_mode=mode)
        aligned = aligner.apply_warp(img_warped, warp_matrix, (400, 300))
        
        row, col = plot_idx // 3, plot_idx % 3
        axes[row, col].imshow(cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB))
        axes[row, col].set_title(f'{name}\nECC: {ecc:.4f}')
        axes[row, col].axis('off')
        
        print(f"{name}: ECC = {ecc:.4f}")
        plot_idx += 1
    
    plt.tight_layout()
    plt.savefig('output_ecc_alignment.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_ecc_alignment.png")


# ============================================================================
# BAGIAN 3: FEATURE-BASED ALIGNMENT
# ============================================================================

class FeatureBasedAligner:
    """
    Feature-based image alignment dengan RANSAC.
    """
    
    def __init__(self, detector_type: str = 'ORB'):
        """
        Args:
            detector_type: 'ORB', 'SIFT', atau 'AKAZE'
        """
        self.detector_type = detector_type
        
        if detector_type == 'ORB':
            self.detector = cv2.ORB_create(nfeatures=2000)
            self.norm = cv2.NORM_HAMMING
        elif detector_type == 'SIFT':
            self.detector = cv2.SIFT_create()
            self.norm = cv2.NORM_L2
        elif detector_type == 'AKAZE':
            self.detector = cv2.AKAZE_create()
            self.norm = cv2.NORM_HAMMING
        else:
            raise ValueError(f"Unknown detector: {detector_type}")
        
        self.matcher = cv2.BFMatcher(self.norm, crossCheck=False)
    
    def detect_and_compute(self, image: np.ndarray) -> Tuple[list, np.ndarray]:
        """Detect keypoints dan compute descriptors."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        return self.detector.detectAndCompute(gray, None)
    
    def match_features(self, desc1: np.ndarray, desc2: np.ndarray,
                       ratio_thresh: float = 0.75) -> List[cv2.DMatch]:
        """
        Match features dengan ratio test.
        
        Args:
            desc1, desc2: Descriptors
            ratio_thresh: Lowe's ratio threshold
            
        Returns:
            List of good matches
        """
        if desc1 is None or desc2 is None:
            return []
        
        matches = self.matcher.knnMatch(desc1, desc2, k=2)
        
        # Ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
        
        return good_matches
    
    def estimate_homography(self, kp1: list, kp2: list, matches: list,
                           ransac_thresh: float = 5.0
                           ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estimate homography dengan RANSAC.
        
        Args:
            kp1, kp2: Keypoints
            matches: Good matches
            ransac_thresh: RANSAC threshold
            
        Returns:
            H: Homography matrix
            mask: Inlier mask
        """
        if len(matches) < 4:
            return None, None
        
        # Extract matched points
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        # RANSAC
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_thresh)
        
        return H, mask.ravel() if mask is not None else None
    
    def estimate_affine(self, kp1: list, kp2: list, matches: list,
                        ransac_thresh: float = 5.0
                        ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estimate affine transformation dengan RANSAC.
        """
        if len(matches) < 3:
            return None, None
        
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        M, mask = cv2.estimateAffine2D(src_pts, dst_pts, method=cv2.RANSAC,
                                        ransacReprojThreshold=ransac_thresh)
        
        return M, mask.ravel() if mask is not None else None
    
    def align_images(self, img1: np.ndarray, img2: np.ndarray,
                    transform_type: str = 'homography'
                    ) -> Tuple[np.ndarray, np.ndarray, int]:
        """
        Align img2 ke img1.
        
        Args:
            img1: Reference image
            img2: Image to align
            transform_type: 'homography' atau 'affine'
            
        Returns:
            aligned: Aligned image
            transform: Transformation matrix
            num_inliers: Number of inliers
        """
        # Detect dan match
        kp1, desc1 = self.detect_and_compute(img1)
        kp2, desc2 = self.detect_and_compute(img2)
        matches = self.match_features(desc1, desc2)
        
        print(f"Found {len(matches)} good matches")
        
        # Estimate transformation
        if transform_type == 'homography':
            transform, mask = self.estimate_homography(kp1, kp2, matches)
            if transform is not None:
                h, w = img1.shape[:2]
                aligned = cv2.warpPerspective(img2, transform, (w, h))
        else:
            transform, mask = self.estimate_affine(kp1, kp2, matches)
            if transform is not None:
                h, w = img1.shape[:2]
                aligned = cv2.warpAffine(img2, transform, (w, h))
        
        if transform is None:
            return None, None, 0
        
        num_inliers = np.sum(mask) if mask is not None else 0
        
        return aligned, transform, num_inliers
    
    def visualize_matches(self, img1: np.ndarray, img2: np.ndarray,
                          kp1: list, kp2: list, matches: list,
                          mask: np.ndarray = None) -> np.ndarray:
        """Visualize matches."""
        if mask is not None:
            matches_mask = mask.tolist()
        else:
            matches_mask = None
        
        draw_params = dict(
            matchColor=(0, 255, 0),
            singlePointColor=(255, 0, 0),
            matchesMask=matches_mask,
            flags=cv2.DrawMatchesFlags_DEFAULT
        )
        
        return cv2.drawMatches(img1, kp1, img2, kp2, matches, None, **draw_params)


def demo_feature_alignment():
    """Demo feature-based alignment."""
    print("\n" + "=" * 60)
    print("DEMO: Feature-Based Alignment")
    print("=" * 60)
    
    # Buat gambar test dengan texture
    img1 = np.zeros((400, 500, 3), dtype=np.uint8)
    
    # Tambah pattern untuk features
    for i in range(0, 500, 50):
        for j in range(0, 400, 50):
            color = ((i * 5) % 255, (j * 5) % 255, ((i + j) * 3) % 255)
            cv2.circle(img1, (i + 25, j + 25), 15, color, -1)
    
    cv2.putText(img1, "ALIGN", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Buat versi transformed
    angle = np.radians(10)
    scale = 0.9
    tx, ty = 30, -20
    
    center = (250, 200)
    M = cv2.getRotationMatrix2D(center, np.degrees(angle), scale)
    M[0, 2] += tx
    M[1, 2] += ty
    
    img2 = cv2.warpAffine(img1, M, (500, 400))
    
    # Feature-based alignment
    aligner = FeatureBasedAligner(detector_type='ORB')
    
    aligned, transform, num_inliers = aligner.align_images(img1, img2, 'homography')
    
    print(f"Inliers: {num_inliers}")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Reference Image')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Transformed Image')
    axes[0, 1].axis('off')
    
    if aligned is not None:
        axes[1, 0].imshow(cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title(f'Aligned Image\n({num_inliers} inliers)')
        axes[1, 0].axis('off')
        
        # Difference
        diff = cv2.absdiff(img1, aligned)
        axes[1, 1].imshow(cv2.cvtColor(diff, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Difference (should be minimal)')
        axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_feature_alignment.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_feature_alignment.png")


# ============================================================================
# BAGIAN 4: PANORAMA STITCHING
# ============================================================================

class PanoramaStitcher:
    """
    Panorama stitching dengan feature matching dan blending.
    """
    
    def __init__(self, detector_type: str = 'ORB'):
        """
        Args:
            detector_type: Feature detector type
        """
        self.aligner = FeatureBasedAligner(detector_type)
    
    def stitch_pair(self, img_left: np.ndarray, img_right: np.ndarray,
                   blend: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Stitch dua gambar.
        
        Args:
            img_left: Left image (reference)
            img_right: Right image
            blend: Whether to apply blending
            
        Returns:
            panorama: Stitched panorama
            H: Homography matrix
        """
        # Detect dan match features
        kp1, desc1 = self.aligner.detect_and_compute(img_left)
        kp2, desc2 = self.aligner.detect_and_compute(img_right)
        matches = self.aligner.match_features(desc1, desc2)
        
        print(f"Matches found: {len(matches)}")
        
        if len(matches) < 10:
            print("Not enough matches!")
            return None, None
        
        # Estimate homography (right to left)
        H, mask = self.aligner.estimate_homography(kp2, kp1, matches)
        
        if H is None:
            print("Homography estimation failed!")
            return None, None
        
        # Calculate panorama size
        h1, w1 = img_left.shape[:2]
        h2, w2 = img_right.shape[:2]
        
        # Get corners of right image after transformation
        corners_right = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
        corners_transformed = cv2.perspectiveTransform(corners_right, H)
        
        # Combine with left image corners
        corners_left = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
        all_corners = np.concatenate([corners_left, corners_transformed], axis=0)
        
        # Find bounding box
        [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 0.5)
        
        # Translation to shift to positive coordinates
        translation = np.array([[1, 0, -x_min],
                               [0, 1, -y_min],
                               [0, 0, 1]], dtype=np.float32)
        
        # Warp right image
        panorama_size = (x_max - x_min, y_max - y_min)
        warped_right = cv2.warpPerspective(img_right, translation @ H, panorama_size)
        
        # Place left image
        panorama = warped_right.copy()
        panorama[-y_min:-y_min + h1, -x_min:-x_min + w1] = img_left
        
        if blend:
            # Simple alpha blending in overlap region
            panorama = self._blend_images(panorama, warped_right, img_left, 
                                         -x_min, -y_min, w1, h1)
        
        return panorama, H
    
    def _blend_images(self, panorama: np.ndarray, warped: np.ndarray,
                     reference: np.ndarray, offset_x: int, offset_y: int,
                     ref_w: int, ref_h: int) -> np.ndarray:
        """Simple linear blending."""
        # Create masks
        mask_warped = (warped > 0).any(axis=2).astype(np.float32)
        
        mask_ref = np.zeros(panorama.shape[:2], dtype=np.float32)
        mask_ref[offset_y:offset_y + ref_h, offset_x:offset_x + ref_w] = 1.0
        
        # Overlap region
        overlap = mask_warped * mask_ref
        
        # Create blending weights
        # Distance transform for smooth blending
        dist_warped = cv2.distanceTransform((mask_warped > 0).astype(np.uint8), cv2.DIST_L2, 5)
        dist_ref = cv2.distanceTransform((mask_ref > 0).astype(np.uint8), cv2.DIST_L2, 5)
        
        # Normalize weights in overlap
        total = dist_warped + dist_ref + 1e-6
        weight_warped = dist_warped / total
        weight_ref = dist_ref / total
        
        # Apply blending
        result = panorama.copy().astype(np.float32)
        
        for c in range(3):
            result[:, :, c] = weight_warped * warped[:, :, c] + weight_ref * panorama[:, :, c]
        
        return result.astype(np.uint8)
    
    def stitch_multiple(self, images: List[np.ndarray]) -> np.ndarray:
        """
        Stitch multiple images.
        
        Args:
            images: List of images (ordered left to right)
            
        Returns:
            panorama: Final stitched panorama
        """
        if len(images) < 2:
            return images[0] if images else None
        
        # Start with middle image as reference
        mid_idx = len(images) // 2
        panorama = images[mid_idx]
        
        # Stitch images to the left
        for i in range(mid_idx - 1, -1, -1):
            print(f"Stitching image {i} to panorama...")
            panorama, _ = self.stitch_pair(images[i], panorama)
            if panorama is None:
                print(f"Failed at image {i}")
                return None
        
        # Stitch images to the right
        for i in range(mid_idx + 1, len(images)):
            print(f"Stitching image {i} to panorama...")
            panorama, _ = self.stitch_pair(panorama, images[i])
            if panorama is None:
                print(f"Failed at image {i}")
                return None
        
        return panorama


class MultiBandBlender:
    """
    Multi-band blending untuk seamless stitching.
    """
    
    def __init__(self, num_levels: int = 5):
        """
        Args:
            num_levels: Number of pyramid levels
        """
        self.num_levels = num_levels
    
    def _build_gaussian_pyramid(self, img: np.ndarray) -> List[np.ndarray]:
        """Build Gaussian pyramid."""
        pyramid = [img.astype(np.float32)]
        
        for _ in range(self.num_levels - 1):
            img = cv2.pyrDown(pyramid[-1])
            pyramid.append(img)
        
        return pyramid
    
    def _build_laplacian_pyramid(self, img: np.ndarray) -> List[np.ndarray]:
        """Build Laplacian pyramid."""
        gaussian_pyr = self._build_gaussian_pyramid(img)
        laplacian_pyr = []
        
        for i in range(self.num_levels - 1):
            expanded = cv2.pyrUp(gaussian_pyr[i + 1], 
                                dstsize=(gaussian_pyr[i].shape[1], gaussian_pyr[i].shape[0]))
            laplacian = gaussian_pyr[i] - expanded
            laplacian_pyr.append(laplacian)
        
        laplacian_pyr.append(gaussian_pyr[-1])
        
        return laplacian_pyr
    
    def _reconstruct_from_laplacian(self, laplacian_pyr: List[np.ndarray]) -> np.ndarray:
        """Reconstruct image from Laplacian pyramid."""
        img = laplacian_pyr[-1]
        
        for i in range(self.num_levels - 2, -1, -1):
            expanded = cv2.pyrUp(img, dstsize=(laplacian_pyr[i].shape[1], 
                                               laplacian_pyr[i].shape[0]))
            img = expanded + laplacian_pyr[i]
        
        return img
    
    def blend(self, img1: np.ndarray, img2: np.ndarray, 
              mask: np.ndarray) -> np.ndarray:
        """
        Blend two images using multi-band blending.
        
        Args:
            img1: First image
            img2: Second image
            mask: Binary mask (1 for img1, 0 for img2)
            
        Returns:
            Blended image
        """
        # Ensure same size
        assert img1.shape == img2.shape == mask.shape[:2] + (3,) if len(mask.shape) == 2 else mask.shape
        
        # Build Laplacian pyramids for images
        lap1 = self._build_laplacian_pyramid(img1)
        lap2 = self._build_laplacian_pyramid(img2)
        
        # Build Gaussian pyramid for mask
        if len(mask.shape) == 2:
            mask = np.dstack([mask] * 3)
        mask_pyr = self._build_gaussian_pyramid(mask.astype(np.float32))
        
        # Blend at each level
        blended_pyr = []
        for l1, l2, m in zip(lap1, lap2, mask_pyr):
            blended = m * l1 + (1 - m) * l2
            blended_pyr.append(blended)
        
        # Reconstruct
        result = self._reconstruct_from_laplacian(blended_pyr)
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result


def demo_panorama_stitching():
    """Demo panorama stitching."""
    print("\n" + "=" * 60)
    print("DEMO: Panorama Stitching")
    print("=" * 60)
    
    # Buat gambar simulasi panorama
    # Gambar besar yang akan di-split
    full_width = 800
    full_height = 300
    
    full_img = np.zeros((full_height, full_width, 3), dtype=np.uint8)
    
    # Tambah gradien background
    for x in range(full_width):
        color = int(255 * x / full_width)
        full_img[:, x] = [color, 100, 255 - color]
    
    # Tambah objek
    cv2.circle(full_img, (150, 150), 60, (0, 255, 0), -1)
    cv2.rectangle(full_img, (350, 100), (450, 200), (255, 0, 0), -1)
    cv2.circle(full_img, (650, 150), 70, (0, 255, 255), -1)
    
    # Tambah texture untuk features
    for i in range(0, full_width, 40):
        for j in range(0, full_height, 40):
            cv2.circle(full_img, (i + 20, j + 20), 5, (255, 255, 255), -1)
    
    # Split menjadi overlapping images
    overlap = 100
    img_width = 300
    
    img1 = full_img[:, 0:img_width].copy()
    img2 = full_img[:, img_width - overlap:2*img_width - overlap].copy()
    img3 = full_img[:, 2*img_width - 2*overlap:].copy()
    
    print(f"Image sizes: {img1.shape}, {img2.shape}, {img3.shape}")
    
    # Stitch
    stitcher = PanoramaStitcher(detector_type='ORB')
    
    # Stitch pair
    pano_12, H = stitcher.stitch_pair(img1, img2, blend=True)
    
    if pano_12 is not None:
        print(f"Pairwise panorama size: {pano_12.shape}")
    
    # Try OpenCV Stitcher juga
    print("\nUsing OpenCV Stitcher...")
    cv_stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, cv_panorama = cv_stitcher.stitch([img1, img2, img3])
    
    if status == cv2.Stitcher_OK:
        print(f"OpenCV panorama size: {cv_panorama.shape}")
    else:
        print(f"OpenCV Stitcher failed with status: {status}")
        cv_panorama = None
    
    # Visualize
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(full_img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original Full Image')
    axes[0, 0].axis('off')
    
    # Show individual images
    axes[0, 1].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Image 1 (Left)')
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Image 2 (Center)')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Image 3 (Right)')
    axes[1, 1].axis('off')
    
    if pano_12 is not None:
        axes[2, 0].imshow(cv2.cvtColor(pano_12, cv2.COLOR_BGR2RGB))
        axes[2, 0].set_title('Custom Stitched (1+2)')
        axes[2, 0].axis('off')
    
    if cv_panorama is not None:
        axes[2, 1].imshow(cv2.cvtColor(cv_panorama, cv2.COLOR_BGR2RGB))
        axes[2, 1].set_title('OpenCV Stitcher Result')
        axes[2, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_panorama_stitching.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_panorama_stitching.png")


def demo_multiband_blending():
    """Demo multi-band blending."""
    print("\n" + "=" * 60)
    print("DEMO: Multi-Band Blending")
    print("=" * 60)
    
    # Buat dua gambar berbeda
    size = 400
    
    # Image 1: Orange gradient dengan pattern
    img1 = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        img1[:, i] = [0, int(128 + 127 * i / size), 255]
    cv2.circle(img1, (100, 200), 50, (255, 0, 0), -1)
    cv2.rectangle(img1, (50, 300), (150, 380), (0, 255, 0), -1)
    
    # Image 2: Blue gradient dengan pattern
    img2 = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        img2[:, i] = [255, int(127 - 127 * i / size), 0]
    cv2.circle(img2, (300, 200), 60, (0, 255, 255), -1)
    cv2.rectangle(img2, (250, 300), (380, 380), (255, 0, 255), -1)
    
    # Create mask (vertical seam)
    mask = np.zeros((size, size), dtype=np.float32)
    mask[:, :size//2] = 1.0
    
    # Different blending methods
    # 1. Hard cut
    blend_hard = img1.copy()
    blend_hard[:, size//2:] = img2[:, size//2:]
    
    # 2. Linear blend
    alpha = np.linspace(1, 0, size).reshape(1, -1)
    alpha = np.tile(alpha, (size, 1))
    blend_linear = (alpha[:, :, np.newaxis] * img1 + 
                   (1 - alpha[:, :, np.newaxis]) * img2).astype(np.uint8)
    
    # 3. Multi-band blend
    blender = MultiBandBlender(num_levels=5)
    blend_multiband = blender.blend(img1, img2, mask)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Image 1')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Image 2')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(mask, cmap='gray')
    axes[0, 2].set_title('Mask')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(blend_hard, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Hard Cut\n(visible seam)')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(blend_linear, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Linear Blend\n(ghosting artifacts)')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(blend_multiband, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('Multi-Band Blend\n(seamless)')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_multiband_blending.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_multiband_blending.png")


# ============================================================================
# BAGIAN 5: VIDEO STABILIZATION
# ============================================================================

class VideoStabilizer:
    """
    Simple video stabilization menggunakan feature tracking.
    """
    
    def __init__(self, smoothing_radius: int = 30):
        """
        Args:
            smoothing_radius: Radius for trajectory smoothing
        """
        self.smoothing_radius = smoothing_radius
        self.tracker = LucasKanadeTracker()
    
    def _moving_average(self, trajectory: np.ndarray, radius: int) -> np.ndarray:
        """Apply moving average smoothing."""
        smoothed = np.copy(trajectory)
        
        for i in range(len(trajectory)):
            start = max(0, i - radius)
            end = min(len(trajectory), i + radius + 1)
            smoothed[i] = np.mean(trajectory[start:end], axis=0)
        
        return smoothed
    
    def stabilize_frames(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """
        Stabilize a sequence of frames.
        
        Args:
            frames: List of video frames
            
        Returns:
            stabilized: List of stabilized frames
        """
        n_frames = len(frames)
        
        # Estimate motion between consecutive frames
        transforms = np.zeros((n_frames - 1, 3))  # [dx, dy, da]
        
        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        
        for i in range(n_frames - 1):
            # Detect features
            prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, 
                                               qualityLevel=0.01, minDistance=30)
            
            curr_gray = cv2.cvtColor(frames[i + 1], cv2.COLOR_BGR2GRAY)
            
            if prev_pts is not None:
                # Track features
                curr_pts, status, _ = self.tracker.track_points(prev_gray, curr_gray, prev_pts)
                
                # Filter valid points
                idx = np.where(status == 1)[0]
                prev_pts_valid = prev_pts[idx]
                curr_pts_valid = curr_pts[idx]
                
                if len(prev_pts_valid) >= 3:
                    # Estimate transformation
                    M, _ = cv2.estimateAffinePartial2D(prev_pts_valid, curr_pts_valid)
                    
                    if M is not None:
                        # Extract parameters
                        dx = M[0, 2]
                        dy = M[1, 2]
                        da = np.arctan2(M[1, 0], M[0, 0])
                        transforms[i] = [dx, dy, da]
            
            prev_gray = curr_gray
        
        # Compute trajectory (cumulative sum)
        trajectory = np.cumsum(transforms, axis=0)
        
        # Smooth trajectory
        smoothed_trajectory = self._moving_average(trajectory, self.smoothing_radius)
        
        # Calculate difference to apply
        difference = smoothed_trajectory - trajectory
        transforms_smooth = transforms + np.vstack([difference, [0, 0, 0]])[:-1]
        
        # Apply stabilization
        stabilized = []
        h, w = frames[0].shape[:2]
        
        for i in range(n_frames):
            if i < n_frames - 1:
                dx, dy, da = transforms_smooth[i]
                
                # Build transformation matrix
                M = np.array([
                    [np.cos(da), -np.sin(da), dx],
                    [np.sin(da), np.cos(da), dy]
                ], dtype=np.float32)
                
                frame_stabilized = cv2.warpAffine(frames[i], M, (w, h))
            else:
                frame_stabilized = frames[i]
            
            stabilized.append(frame_stabilized)
        
        return stabilized


def demo_video_stabilization():
    """Demo video stabilization dengan synthetic shaky video."""
    print("\n" + "=" * 60)
    print("DEMO: Video Stabilization")
    print("=" * 60)
    
    # Create synthetic video dengan motion
    n_frames = 60
    h, w = 300, 400
    
    # Base image
    base_img = np.zeros((h + 100, w + 100, 3), dtype=np.uint8)
    
    # Add content
    cv2.rectangle(base_img, (100, 100), (300, 250), (0, 255, 0), -1)
    cv2.circle(base_img, (200, 175), 40, (255, 0, 0), -1)
    cv2.putText(base_img, "STABLE", (120, 185), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (255, 255, 255), 2)
    
    # Add texture
    for i in range(0, base_img.shape[1], 30):
        for j in range(0, base_img.shape[0], 30):
            cv2.circle(base_img, (i + 15, j + 15), 3, (100, 100, 100), -1)
    
    # Generate shaky frames
    np.random.seed(42)
    shaky_frames = []
    
    for i in range(n_frames):
        # Random shake
        dx = int(20 * np.sin(i * 0.3) + np.random.randn() * 5)
        dy = int(15 * np.cos(i * 0.4) + np.random.randn() * 5)
        
        # Crop with offset
        x_start = 50 + dx
        y_start = 50 + dy
        
        frame = base_img[y_start:y_start + h, x_start:x_start + w].copy()
        shaky_frames.append(frame)
    
    print(f"Created {n_frames} shaky frames")
    
    # Stabilize
    stabilizer = VideoStabilizer(smoothing_radius=15)
    stabilized_frames = stabilizer.stabilize_frames(shaky_frames)
    
    print("Stabilization complete")
    
    # Visualize comparison
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    sample_indices = [0, 15, 30, 45]
    
    for idx, i in enumerate(sample_indices):
        axes[0, idx].imshow(cv2.cvtColor(shaky_frames[i], cv2.COLOR_BGR2RGB))
        axes[0, idx].set_title(f'Shaky Frame {i}')
        axes[0, idx].axis('off')
        
        axes[1, idx].imshow(cv2.cvtColor(stabilized_frames[i], cv2.COLOR_BGR2RGB))
        axes[1, idx].set_title(f'Stabilized Frame {i}')
        axes[1, idx].axis('off')
    
    plt.suptitle('Video Stabilization Demo')
    plt.tight_layout()
    plt.savefig('output_video_stabilization.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_video_stabilization.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function untuk menjalankan semua demo."""
    print("=" * 70)
    print("PRAKTIKUM 08: IMAGE ALIGNMENT DAN STITCHING")
    print("=" * 70)
    
    demos = [
        ("1. Transformasi 2D", demo_transformations),
        ("2. Direct Alignment (ECC)", demo_direct_alignment),
        ("3. Feature-Based Alignment", demo_feature_alignment),
        ("4. Panorama Stitching", demo_panorama_stitching),
        ("5. Multi-Band Blending", demo_multiband_blending),
        ("6. Video Stabilization", demo_video_stabilization),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for i, (name, _) in enumerate(demos):
        print(f"  {name}")
    print("  7. Jalankan Semua")
    print("  0. Keluar")
    
    while True:
        try:
            choice = input("\nMasukkan pilihan (0-7): ").strip()
            
            if choice == '0':
                print("Terima kasih!")
                break
            elif choice == '7':
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
