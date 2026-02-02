"""
PRAKTIKUM BAB 7: FEATURE DETECTION DAN MATCHING
================================================

Tujuan:
1. Memahami dan mengimplementasi berbagai feature detectors
2. Membandingkan descriptors (SIFT, SURF, ORB)
3. Feature matching dengan ratio test dan RANSAC
4. Aplikasi: Image stitching sederhana

Kebutuhan:
- Python 3.8+
- OpenCV (opencv-contrib-python untuk SIFT/SURF)
- NumPy
- Matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from typing import Tuple, List, Optional
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# BAGIAN 1: HARRIS CORNER DETECTOR
# ============================================================

print("=" * 60)
print("BAGIAN 1: HARRIS CORNER DETECTOR")
print("=" * 60)

def harris_corner_detector(image: np.ndarray, 
                          k: float = 0.04, 
                          threshold: float = 0.01,
                          block_size: int = 2,
                          ksize: int = 3) -> Tuple[np.ndarray, np.ndarray]:
    """
    Implementasi Harris Corner Detector dari scratch
    
    Args:
        image: Input grayscale image
        k: Harris detector free parameter (0.04-0.06)
        threshold: Response threshold (relative to max)
        block_size: Neighborhood size
        ksize: Sobel kernel size
        
    Returns:
        corners: Binary mask of corner locations
        response: Harris response image
    """
    # Convert to float
    img = image.astype(np.float64) / 255.0
    
    # Compute gradients
    Ix = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    Iy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Compute products of gradients
    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy
    
    # Apply Gaussian smoothing to gradient products
    kernel_size = (block_size * 2 + 1, block_size * 2 + 1)
    Sxx = cv2.GaussianBlur(Ixx, kernel_size, 0)
    Syy = cv2.GaussianBlur(Iyy, kernel_size, 0)
    Sxy = cv2.GaussianBlur(Ixy, kernel_size, 0)
    
    # Harris response
    # R = det(M) - k * trace(M)^2
    # det(M) = Sxx * Syy - Sxy^2
    # trace(M) = Sxx + Syy
    det = Sxx * Syy - Sxy ** 2
    trace = Sxx + Syy
    response = det - k * trace ** 2
    
    # Normalize response
    response_norm = response / response.max()
    
    # Threshold
    corners = response_norm > threshold
    
    # Non-maximum suppression
    response_dilated = cv2.dilate(response, np.ones((3, 3)))
    corners = corners & (response == response_dilated)
    
    return corners, response


def shi_tomasi_detector(image: np.ndarray,
                        threshold: float = 0.01,
                        block_size: int = 2,
                        ksize: int = 3) -> Tuple[np.ndarray, np.ndarray]:
    """
    Shi-Tomasi (Good Features to Track) detector
    
    Response = min(λ1, λ2)
    """
    img = image.astype(np.float64) / 255.0
    
    # Compute gradients
    Ix = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    Iy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Compute products of gradients
    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy
    
    # Apply Gaussian smoothing
    kernel_size = (block_size * 2 + 1, block_size * 2 + 1)
    Sxx = cv2.GaussianBlur(Ixx, kernel_size, 0)
    Syy = cv2.GaussianBlur(Iyy, kernel_size, 0)
    Sxy = cv2.GaussianBlur(Ixy, kernel_size, 0)
    
    # Compute eigenvalues
    # λ = (trace ± sqrt(trace² - 4*det)) / 2
    trace = Sxx + Syy
    det = Sxx * Syy - Sxy ** 2
    
    discriminant = np.sqrt(np.maximum(trace**2 - 4*det, 0))
    lambda1 = (trace + discriminant) / 2
    lambda2 = (trace - discriminant) / 2
    
    # Shi-Tomasi response = min eigenvalue
    response = np.minimum(lambda1, lambda2)
    
    # Normalize and threshold
    response_norm = response / (response.max() + 1e-10)
    corners = response_norm > threshold
    
    # Non-maximum suppression
    response_dilated = cv2.dilate(response, np.ones((3, 3)))
    corners = corners & (response == response_dilated)
    
    return corners, response


def demo_corner_detectors():
    """Demo Harris dan Shi-Tomasi corner detectors"""
    print("\n📊 Demo: Corner Detectors\n")
    
    # Create test image with corners
    img = np.zeros((300, 300), dtype=np.uint8)
    
    # Draw shapes
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)
    cv2.rectangle(img, (170, 80), (250, 180), 255, -1)
    pts = np.array([[150, 200], [200, 280], [100, 280]], np.int32)
    cv2.fillPoly(img, [pts], 255)
    
    # Add some noise
    noise = np.random.randint(0, 20, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    # Detect corners
    harris_corners, harris_response = harris_corner_detector(img, threshold=0.01)
    shi_corners, shi_response = shi_tomasi_detector(img, threshold=0.01)
    
    # OpenCV comparison
    harris_cv = cv2.cornerHarris(img.astype(np.float32), 2, 3, 0.04)
    shi_cv = cv2.goodFeaturesToTrack(img, 50, 0.01, 10)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original Image')
    
    # Harris
    axes[0, 1].imshow(harris_response, cmap='hot')
    axes[0, 1].set_title('Harris Response')
    
    img_harris = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    coords = np.where(harris_corners)
    for y, x in zip(coords[0], coords[1]):
        cv2.circle(img_harris, (x, y), 3, (0, 255, 0), -1)
    axes[0, 2].imshow(img_harris)
    axes[0, 2].set_title(f'Harris Corners ({len(coords[0])} corners)')
    
    # Shi-Tomasi
    axes[1, 1].imshow(shi_response, cmap='hot')
    axes[1, 1].set_title('Shi-Tomasi Response')
    
    img_shi = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    coords = np.where(shi_corners)
    for y, x in zip(coords[0], coords[1]):
        cv2.circle(img_shi, (x, y), 3, (0, 0, 255), -1)
    axes[1, 2].imshow(img_shi)
    axes[1, 2].set_title(f'Shi-Tomasi Corners ({len(coords[0])} corners)')
    
    # OpenCV comparison
    img_cv = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if shi_cv is not None:
        for pt in shi_cv:
            x, y = pt.ravel().astype(int)
            cv2.circle(img_cv, (x, y), 3, (255, 0, 0), -1)
    axes[1, 0].imshow(img_cv)
    axes[1, 0].set_title('OpenCV goodFeaturesToTrack')
    
    for ax in axes.flat:
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_corner_detectors.png', dpi=150)
    plt.show()
    
    print("✅ Corner detector demo selesai!")


# ============================================================
# BAGIAN 2: SCALE-INVARIANT FEATURES
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 2: SCALE-INVARIANT FEATURES")
print("=" * 60)

class FeatureExtractor:
    """
    Unified interface untuk berbagai feature extractors
    """
    
    def __init__(self, method: str = 'orb'):
        """
        Args:
            method: 'sift', 'surf', 'orb', 'brisk', 'akaze'
        """
        self.method = method.lower()
        
        if self.method == 'sift':
            self.detector = cv2.SIFT_create()
        elif self.method == 'surf':
            # SURF requires opencv-contrib
            try:
                self.detector = cv2.xfeatures2d.SURF_create(400)
            except:
                print("SURF not available, using SIFT")
                self.detector = cv2.SIFT_create()
                self.method = 'sift'
        elif self.method == 'orb':
            self.detector = cv2.ORB_create(nfeatures=1000)
        elif self.method == 'brisk':
            self.detector = cv2.BRISK_create()
        elif self.method == 'akaze':
            self.detector = cv2.AKAZE_create()
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def detect_and_compute(self, image: np.ndarray) -> Tuple[List, np.ndarray]:
        """
        Detect keypoints and compute descriptors
        
        Returns:
            keypoints: List of cv2.KeyPoint
            descriptors: Descriptor array
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        keypoints, descriptors = self.detector.detectAndCompute(gray, None)
        
        return keypoints, descriptors
    
    def draw_keypoints(self, image: np.ndarray, keypoints: List,
                       flags: int = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) -> np.ndarray:
        """Draw keypoints on image"""
        return cv2.drawKeypoints(image, keypoints, None, flags=flags)


def demo_feature_comparison():
    """Compare different feature detectors"""
    print("\n📊 Demo: Feature Detector Comparison\n")
    
    # Create test image
    img = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(img, (30, 30), (130, 130), 200, -1)
    cv2.circle(img, (200, 80), 50, 200, -1)
    cv2.ellipse(img, (150, 220), (60, 30), 0, 0, 360, 200, -1)
    # Add texture
    for i in range(0, 300, 10):
        cv2.line(img, (i, 0), (i, 300), 50, 1)
    
    # Add Gaussian noise
    noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
    img = cv2.add(img, noise)
    
    methods = ['sift', 'orb', 'brisk', 'akaze']
    results = {}
    
    for method in methods:
        try:
            extractor = FeatureExtractor(method)
            start = time.time()
            kps, descs = extractor.detect_and_compute(img)
            elapsed = time.time() - start
            
            results[method] = {
                'keypoints': kps,
                'descriptors': descs,
                'time': elapsed
            }
            print(f"{method.upper()}: {len(kps)} keypoints, {elapsed*1000:.2f} ms")
        except Exception as e:
            print(f"{method.upper()}: Error - {e}")
    
    # Visualize
    n_methods = len(results)
    fig, axes = plt.subplots(1, n_methods, figsize=(4*n_methods, 4))
    
    for idx, (method, data) in enumerate(results.items()):
        img_with_kps = cv2.drawKeypoints(
            img, data['keypoints'], None,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )
        axes[idx].imshow(img_with_kps)
        axes[idx].set_title(f'{method.upper()}\n{len(data["keypoints"])} kps, {data["time"]*1000:.1f}ms')
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_feature_comparison.png', dpi=150)
    plt.show()
    
    print("✅ Feature comparison demo selesai!")


# ============================================================
# BAGIAN 3: FEATURE MATCHING
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 3: FEATURE MATCHING")
print("=" * 60)

class FeatureMatcher:
    """
    Feature matching dengan berbagai strategi
    """
    
    def __init__(self, method: str = 'bf', descriptor_type: str = 'float'):
        """
        Args:
            method: 'bf' (brute-force) atau 'flann'
            descriptor_type: 'float' atau 'binary'
        """
        self.method = method
        self.descriptor_type = descriptor_type
        
        if method == 'bf':
            if descriptor_type == 'binary':
                self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            else:
                self.matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        elif method == 'flann':
            if descriptor_type == 'binary':
                FLANN_INDEX_LSH = 6
                index_params = dict(algorithm=FLANN_INDEX_LSH,
                                   table_number=6,
                                   key_size=12,
                                   multi_probe_level=1)
            else:
                FLANN_INDEX_KDTREE = 1
                index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
    
    def match(self, desc1: np.ndarray, desc2: np.ndarray) -> List:
        """Simple nearest neighbor matching"""
        matches = self.matcher.match(desc1, desc2)
        return sorted(matches, key=lambda x: x.distance)
    
    def match_ratio_test(self, desc1: np.ndarray, desc2: np.ndarray,
                        ratio: float = 0.75) -> List:
        """
        Matching dengan Lowe's ratio test
        
        Args:
            desc1, desc2: Descriptors
            ratio: Threshold untuk ratio test (0.7-0.8)
        """
        matches = self.matcher.knnMatch(desc1, desc2, k=2)
        
        good_matches = []
        for m, n in matches:
            if m.distance < ratio * n.distance:
                good_matches.append(m)
        
        return good_matches
    
    def match_cross_check(self, desc1: np.ndarray, desc2: np.ndarray) -> List:
        """
        Mutual nearest neighbor matching
        """
        # Forward matches
        matches_12 = self.matcher.match(desc1, desc2)
        
        # Backward matches
        matches_21 = self.matcher.match(desc2, desc1)
        
        # Find mutual matches
        mutual = []
        for m12 in matches_12:
            for m21 in matches_21:
                if m12.queryIdx == m21.trainIdx and m12.trainIdx == m21.queryIdx:
                    mutual.append(m12)
                    break
        
        return sorted(mutual, key=lambda x: x.distance)


def ransac_homography(src_pts: np.ndarray, dst_pts: np.ndarray,
                     threshold: float = 4.0, max_iters: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    RANSAC untuk estimasi homography
    
    Args:
        src_pts: Source points (N, 2)
        dst_pts: Destination points (N, 2)
        threshold: Inlier threshold in pixels
        max_iters: Maximum iterations
        
    Returns:
        H: 3x3 homography matrix
        inliers: Boolean mask of inliers
    """
    n_points = len(src_pts)
    best_inliers = np.zeros(n_points, dtype=bool)
    best_H = None
    
    for _ in range(max_iters):
        # Random sample 4 points
        indices = np.random.choice(n_points, 4, replace=False)
        
        # Compute homography from 4 points
        src_sample = src_pts[indices].reshape(-1, 1, 2).astype(np.float32)
        dst_sample = dst_pts[indices].reshape(-1, 1, 2).astype(np.float32)
        
        H, _ = cv2.findHomography(src_sample, dst_sample, 0)
        
        if H is None:
            continue
        
        # Transform all source points
        src_homogeneous = np.hstack([src_pts, np.ones((n_points, 1))])
        projected = (H @ src_homogeneous.T).T
        projected = projected[:, :2] / projected[:, 2:3]
        
        # Compute distances
        distances = np.linalg.norm(projected - dst_pts, axis=1)
        
        # Count inliers
        inliers = distances < threshold
        
        if inliers.sum() > best_inliers.sum():
            best_inliers = inliers
            best_H = H
    
    # Recompute H with all inliers
    if best_inliers.sum() >= 4:
        src_inliers = src_pts[best_inliers].reshape(-1, 1, 2).astype(np.float32)
        dst_inliers = dst_pts[best_inliers].reshape(-1, 1, 2).astype(np.float32)
        best_H, _ = cv2.findHomography(src_inliers, dst_inliers, 0)
    
    return best_H, best_inliers


def demo_feature_matching():
    """Demo feature matching"""
    print("\n📊 Demo: Feature Matching\n")
    
    # Create two images (simulated rotation + scale)
    img1 = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(img1, (50, 50), (200, 200), 200, -1)
    cv2.circle(img1, (125, 125), 30, 100, -1)
    # Add texture
    for i in range(50, 200, 15):
        cv2.line(img1, (i, 50), (i, 200), 150, 1)
    
    # Create transformed version (rotation + scale)
    center = (150, 150)
    angle = 25  # degrees
    scale = 0.8
    M = cv2.getRotationMatrix2D(center, angle, scale)
    img2 = cv2.warpAffine(img1, M, (300, 300))
    
    # Add noise
    noise1 = np.random.normal(0, 10, img1.shape).astype(np.int16)
    noise2 = np.random.normal(0, 10, img2.shape).astype(np.int16)
    img1 = np.clip(img1.astype(np.int16) + noise1, 0, 255).astype(np.uint8)
    img2 = np.clip(img2.astype(np.int16) + noise2, 0, 255).astype(np.uint8)
    
    # Detect features (using ORB)
    extractor = FeatureExtractor('orb')
    kps1, desc1 = extractor.detect_and_compute(img1)
    kps2, desc2 = extractor.detect_and_compute(img2)
    
    print(f"Image 1: {len(kps1)} keypoints")
    print(f"Image 2: {len(kps2)} keypoints")
    
    if desc1 is None or desc2 is None:
        print("Not enough features detected")
        return
    
    # Match dengan berbagai strategi
    matcher = FeatureMatcher('bf', 'binary')
    
    # Simple matching
    simple_matches = matcher.match(desc1, desc2)[:50]
    
    # Ratio test
    ratio_matches = matcher.match_ratio_test(desc1, desc2, ratio=0.75)
    
    # Cross-check
    cross_matches = matcher.match_cross_check(desc1, desc2)[:50]
    
    print(f"\nSimple matching: {len(simple_matches)} matches")
    print(f"Ratio test: {len(ratio_matches)} matches")
    print(f"Cross-check: {len(cross_matches)} matches")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Draw images side by side
    img_combined = np.hstack([img1, img2])
    axes[0, 0].imshow(img_combined, cmap='gray')
    axes[0, 0].set_title('Input Images (with rotation + scale)')
    axes[0, 0].axis('off')
    
    # Simple matches
    img_simple = cv2.drawMatches(img1, kps1, img2, kps2, simple_matches, None,
                                  flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    axes[0, 1].imshow(img_simple)
    axes[0, 1].set_title(f'Simple Matching ({len(simple_matches)} matches)')
    axes[0, 1].axis('off')
    
    # Ratio test matches
    img_ratio = cv2.drawMatches(img1, kps1, img2, kps2, ratio_matches, None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    axes[1, 0].imshow(img_ratio)
    axes[1, 0].set_title(f'Ratio Test ({len(ratio_matches)} matches)')
    axes[1, 0].axis('off')
    
    # Cross-check matches
    img_cross = cv2.drawMatches(img1, kps1, img2, kps2, cross_matches, None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    axes[1, 1].imshow(img_cross)
    axes[1, 1].set_title(f'Cross-Check ({len(cross_matches)} matches)')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_feature_matching.png', dpi=150)
    plt.show()
    
    print("✅ Feature matching demo selesai!")


# ============================================================
# BAGIAN 4: HOMOGRAPHY ESTIMATION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 4: HOMOGRAPHY ESTIMATION")
print("=" * 60)

def demo_homography_estimation():
    """Demo homography estimation dengan RANSAC"""
    print("\n📊 Demo: Homography Estimation\n")
    
    # Create source image with distinct pattern
    img1 = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.rectangle(img1, (50, 50), (350, 350), (200, 200, 200), -1)
    cv2.rectangle(img1, (100, 100), (300, 300), (100, 100, 100), -1)
    cv2.circle(img1, (200, 200), 50, (255, 255, 255), -1)
    # Add checkerboard pattern
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                x, y = 80 + i*60, 80 + j*60
                cv2.rectangle(img1, (x, y), (x+50, y+50), (150, 100, 50), -1)
    
    # Define homography (perspective transform)
    h, w = img1.shape[:2]
    src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst_pts = np.float32([[50, 30], [w-30, 50], [w-60, h-20], [30, h-40]])
    
    H_true = cv2.getPerspectiveTransform(src_pts, dst_pts)
    img2 = cv2.warpPerspective(img1, H_true, (w, h))
    
    # Convert to grayscale for feature detection
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Detect and match features
    extractor = FeatureExtractor('sift')
    kps1, desc1 = extractor.detect_and_compute(gray1)
    kps2, desc2 = extractor.detect_and_compute(gray2)
    
    if desc1 is None or desc2 is None or len(desc1) < 10 or len(desc2) < 10:
        print("Not enough features")
        return
    
    # Match
    matcher = FeatureMatcher('bf', 'float')
    matches = matcher.match_ratio_test(desc1, desc2, ratio=0.7)
    
    print(f"Found {len(matches)} matches after ratio test")
    
    if len(matches) < 4:
        print("Not enough matches")
        return
    
    # Get matched point coordinates
    src_match_pts = np.float32([kps1[m.queryIdx].pt for m in matches])
    dst_match_pts = np.float32([kps2[m.trainIdx].pt for m in matches])
    
    # Estimate homography with RANSAC (using OpenCV)
    H_estimated, mask = cv2.findHomography(src_match_pts, dst_match_pts, cv2.RANSAC, 5.0)
    
    inliers = mask.ravel().astype(bool)
    inlier_matches = [m for m, is_inlier in zip(matches, inliers) if is_inlier]
    
    print(f"RANSAC inliers: {sum(inliers)}/{len(matches)}")
    
    # Warp image using estimated homography
    img1_warped = cv2.warpPerspective(img1, H_estimated, (w, h))
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Source Image')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Target Image (transformed)')
    axes[0, 1].axis('off')
    
    # Draw inlier matches
    img_matches = cv2.drawMatches(img1, kps1, img2, kps2, inlier_matches, None,
                                   matchColor=(0, 255, 0),
                                   flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    axes[1, 0].imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f'Inlier Matches ({len(inlier_matches)} matches)')
    axes[1, 0].axis('off')
    
    # Show warped result overlaid
    overlay = cv2.addWeighted(img2, 0.5, img1_warped, 0.5, 0)
    axes[1, 1].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Overlay (warped source + target)')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_homography_estimation.png', dpi=150)
    plt.show()
    
    print("\n✅ Homography estimation demo selesai!")


# ============================================================
# BAGIAN 5: SIMPLE IMAGE STITCHING
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 5: SIMPLE IMAGE STITCHING")
print("=" * 60)

def simple_image_stitch(img1: np.ndarray, img2: np.ndarray) -> Optional[np.ndarray]:
    """
    Simple image stitching using homography
    
    Args:
        img1: First image (will be reference)
        img2: Second image (will be warped)
        
    Returns:
        stitched: Stitched panorama or None if failed
    """
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Detect features
    extractor = FeatureExtractor('sift')
    kps1, desc1 = extractor.detect_and_compute(gray1)
    kps2, desc2 = extractor.detect_and_compute(gray2)
    
    if desc1 is None or desc2 is None:
        print("Failed to detect features")
        return None
    
    # Match features
    matcher = FeatureMatcher('bf', 'float')
    matches = matcher.match_ratio_test(desc1, desc2, ratio=0.75)
    
    if len(matches) < 10:
        print(f"Not enough matches: {len(matches)}")
        return None
    
    # Get point coordinates
    src_pts = np.float32([kps2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kps1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Find homography (img2 -> img1)
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    if H is None:
        print("Failed to find homography")
        return None
    
    # Get dimensions
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Find output canvas size
    corners_img2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
    corners_warped = cv2.perspectiveTransform(corners_img2, H)
    
    all_corners = np.concatenate([
        np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2),
        corners_warped
    ])
    
    x_min, y_min = np.int32(all_corners.min(axis=0).ravel() - 0.5)
    x_max, y_max = np.int32(all_corners.max(axis=0).ravel() + 0.5)
    
    # Translation to put everything in positive coordinates
    translation = np.array([
        [1, 0, -x_min],
        [0, 1, -y_min],
        [0, 0, 1]
    ], dtype=np.float32)
    
    # Warp img2
    output_size = (x_max - x_min, y_max - y_min)
    img2_warped = cv2.warpPerspective(img2, translation @ H, output_size)
    
    # Copy img1 onto canvas
    stitched = img2_warped.copy()
    stitched[-y_min:-y_min+h1, -x_min:-x_min+w1] = img1
    
    # Simple blending (could be improved with multi-band blending)
    mask1 = np.zeros((output_size[1], output_size[0]), dtype=np.float32)
    mask1[-y_min:-y_min+h1, -x_min:-x_min+w1] = 1
    
    mask2 = cv2.warpPerspective(
        np.ones((h2, w2), dtype=np.float32),
        translation @ H, output_size
    )
    
    overlap = (mask1 > 0) & (mask2 > 0)
    
    # Simple average in overlap region
    for c in range(3):
        stitched_c = stitched[:, :, c].astype(np.float32)
        img1_c = np.zeros((output_size[1], output_size[0]), dtype=np.float32)
        img1_c[-y_min:-y_min+h1, -x_min:-x_min+w1] = img1[:, :, c]
        
        stitched_c[overlap] = (stitched_c[overlap] + img1_c[overlap]) / 2
        stitched[:, :, c] = stitched_c.astype(np.uint8)
    
    return stitched


def demo_image_stitching():
    """Demo simple image stitching"""
    print("\n📊 Demo: Image Stitching\n")
    
    # Create overlapping images
    # Full scene
    scene = np.zeros((300, 600, 3), dtype=np.uint8)
    scene[:] = (50, 50, 50)
    
    # Add objects
    cv2.rectangle(scene, (50, 50), (200, 200), (200, 100, 100), -1)
    cv2.rectangle(scene, (350, 80), (550, 250), (100, 200, 100), -1)
    cv2.circle(scene, (280, 150), 60, (100, 100, 200), -1)
    
    # Add texture
    for i in range(0, 600, 20):
        cv2.line(scene, (i, 0), (i, 300), (70, 70, 70), 1)
    
    # Create two overlapping views
    img1 = scene[:, :350].copy()  # Left part
    img2 = scene[:, 200:].copy()  # Right part (overlap 150 pixels)
    
    # Add some variation
    img2 = cv2.convertScaleAbs(img2, alpha=1.1, beta=10)
    
    print(f"Image 1 size: {img1.shape}")
    print(f"Image 2 size: {img2.shape}")
    
    # Stitch
    stitched = simple_image_stitch(img1, img2)
    
    if stitched is None:
        print("Stitching failed")
        return
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Image 1 (Left)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Image 2 (Right)')
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(scene, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Original Scene (ground truth)')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Stitched Result')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_image_stitching.png', dpi=150)
    plt.show()
    
    print("✅ Image stitching demo selesai!")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PRAKTIKUM BAB 7: FEATURE DETECTION DAN MATCHING")
    print("=" * 60)
    
    # Demo 1: Corner Detectors
    demo_corner_detectors()
    
    # Demo 2: Feature Comparison
    demo_feature_comparison()
    
    # Demo 3: Feature Matching
    demo_feature_matching()
    
    # Demo 4: Homography Estimation
    demo_homography_estimation()
    
    # Demo 5: Image Stitching
    demo_image_stitching()
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM SELESAI!")
    print("=" * 60)
    print("\nFile output yang dihasilkan:")
    print("  - output_corner_detectors.png")
    print("  - output_feature_comparison.png")
    print("  - output_feature_matching.png")
    print("  - output_homography_estimation.png")
    print("  - output_image_stitching.png")
    print("\n📝 Tugas: Lihat file tugas/tugas_bab_07.md")
