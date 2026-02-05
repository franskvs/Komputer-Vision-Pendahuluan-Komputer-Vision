"""
Praktikum 14.1: Image Warping dan Homography
============================================

Program ini mendemonstrasikan dasar image warping:
1. Homography transformation
2. Feature detection dan matching
3. RANSAC untuk outlier rejection
4. Image warping dengan homography

Teori:
------
Homography adalah transformasi proyektif 2D yang memetakan
titik dari satu plane ke plane lain:

    [x']   [h11 h12 h13] [x]
    [y'] ~ [h21 h22 h23] [y]
    [1 ]   [h31 h32 h33] [1]

Atau: x' = Hx (dalam homogeneous coordinates)

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent / "data" / "panorama_sequences"
OUTPUT_DIR = Path(__file__).parent / "output" / "output1"

# Feature detection parameters
FEATURE_METHOD = 'ORB'              # 'SIFT', 'ORB', 'AKAZE'
NUM_FEATURES = 1000                 # Jumlah features maksimum
RATIO_THRESHOLD = 0.75              # Ratio test threshold

# RANSAC parameters
RANSAC_REPROJ_THRESHOLD = 5.0       # Reprojection error threshold
RANSAC_MAX_ITERS = 2000             # Maximum iterations

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat direktori output."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")

def check_opencv():
    """Periksa ketersediaan OpenCV."""
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        return True
    except ImportError:
        print("✗ OpenCV tidak terinstall!")
        return False

def create_sample_images():
    """
    Buat sample images jika tidak ada data.
    """
    import cv2
    
    print("\n[Generate] Membuat sample images...")
    
    # Image 1: Checkerboard dengan features
    img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Background gradient
    for y in range(480):
        for x in range(640):
            img1[y, x] = [int(100 + x * 0.2), int(150 - y * 0.2), 200]
    
    # Add patterns
    for i in range(0, 640, 50):
        cv2.line(img1, (i, 0), (i, 480), (0, 0, 0), 2)
    for i in range(0, 480, 50):
        cv2.line(img1, (0, i), (640, i), (0, 0, 0), 2)
    
    # Add distinctive features
    cv2.circle(img1, (160, 120), 30, (255, 0, 0), -1)
    cv2.circle(img1, (480, 120), 25, (0, 255, 0), -1)
    cv2.circle(img1, (160, 360), 35, (0, 0, 255), -1)
    cv2.rectangle(img1, (400, 300), (500, 400), (255, 255, 0), -1)
    
    # Image 2: Transformed version (simulating different viewpoint)
    # Create homography
    pts1 = np.float32([[0, 0], [640, 0], [640, 480], [0, 480]])
    pts2 = np.float32([[50, 30], [600, 10], [620, 450], [30, 470]])  # Perspective transform
    
    H = cv2.getPerspectiveTransform(pts1, pts2)
    img2 = cv2.warpPerspective(img1, H, (640, 480))
    
    return img1, img2, H

def load_images(path1=None, path2=None):
    """
    Load dua gambar untuk warping.
    """
    import cv2
    
    if path1 is not None and Path(path1).exists():
        img1 = cv2.imread(str(path1))
        img2 = cv2.imread(str(path2)) if path2 else None
        return img1, img2, None
    
    # Use sample images
    return create_sample_images()

# ============================================================
# FEATURE DETECTION
# ============================================================

def create_detector(method='ORB', nfeatures=1000):
    """
    Buat feature detector.
    
    Args:
        method: 'SIFT', 'ORB', 'AKAZE'
        nfeatures: Jumlah features maksimum
    
    Returns:
        detector object
    """
    import cv2
    
    if method == 'SIFT':
        detector = cv2.SIFT_create(nfeatures=nfeatures)
    elif method == 'ORB':
        detector = cv2.ORB_create(nfeatures=nfeatures)
    elif method == 'AKAZE':
        detector = cv2.AKAZE_create()
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return detector

def detect_and_compute(image, detector):
    """
    Detect keypoints dan compute descriptors.
    
    Args:
        image: Input image (BGR atau grayscale)
        detector: Feature detector
    
    Returns:
        keypoints, descriptors
    """
    import cv2
    
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Detect and compute
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    return keypoints, descriptors

def match_features(desc1, desc2, method='BF', ratio_thresh=0.75):
    """
    Match features antara dua gambar.
    
    Args:
        desc1, desc2: Descriptors dari kedua gambar
        method: 'BF' (Brute Force) atau 'FLANN'
        ratio_thresh: Ratio test threshold
    
    Returns:
        good_matches: List of good matches
    """
    import cv2
    
    if desc1 is None or desc2 is None:
        return []
    
    # Create matcher
    if method == 'BF':
        # Pilih norm berdasarkan descriptor type
        if desc1.dtype == np.uint8:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        else:
            bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        
        matches = bf.knnMatch(desc1, desc2, k=2)
    else:
        # FLANN matcher
        if desc1.dtype == np.uint8:
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
        else:
            index_params = dict(algorithm=1, trees=5)
        
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(desc1, desc2, k=2)
    
    # Ratio test
    good_matches = []
    for match in matches:
        if len(match) == 2:
            m, n = match
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
    
    return good_matches

# ============================================================
# HOMOGRAPHY ESTIMATION
# ============================================================

def estimate_homography(kp1, kp2, matches, method='RANSAC', reproj_thresh=5.0):
    """
    Estimasi homography dari matched features.
    
    Args:
        kp1, kp2: Keypoints dari kedua gambar
        matches: List of matches
        method: 'RANSAC', 'LMEDS', 'RHO'
        reproj_thresh: Reprojection error threshold
    
    Returns:
        H: Homography matrix (3x3)
        mask: Inlier mask
    """
    import cv2
    
    if len(matches) < 4:
        print("  ✗ Tidak cukup matches untuk homography!")
        return None, None
    
    # Extract matched point coordinates
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    # Estimate homography
    if method == 'RANSAC':
        H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, reproj_thresh)
    elif method == 'LMEDS':
        H, mask = cv2.findHomography(pts1, pts2, cv2.LMEDS)
    elif method == 'RHO':
        H, mask = cv2.findHomography(pts1, pts2, cv2.RHO, reproj_thresh)
    else:
        H, mask = cv2.findHomography(pts1, pts2, 0)  # Regular least squares
    
    return H, mask.ravel() if mask is not None else None

def compute_reprojection_error(kp1, kp2, matches, H, mask=None):
    """
    Hitung reprojection error.
    
    Args:
        kp1, kp2: Keypoints
        matches: Matches
        H: Homography matrix
        mask: Inlier mask (optional)
    
    Returns:
        mean_error, max_error, errors
    """
    import cv2
    
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    # Transform pts1 dengan H
    pts1_h = np.hstack([pts1, np.ones((len(pts1), 1))])
    pts1_transformed = (H @ pts1_h.T).T
    pts1_transformed = pts1_transformed[:, :2] / pts1_transformed[:, 2:3]
    
    # Compute errors
    errors = np.linalg.norm(pts1_transformed - pts2, axis=1)
    
    if mask is not None:
        inlier_errors = errors[mask.astype(bool)]
    else:
        inlier_errors = errors
    
    return np.mean(inlier_errors), np.max(inlier_errors), errors

# ============================================================
# IMAGE WARPING
# ============================================================

def warp_image(image, H, output_size=None):
    """
    Warp image menggunakan homography.
    
    Args:
        image: Input image
        H: Homography matrix (3x3)
        output_size: (width, height) atau None untuk auto
    
    Returns:
        Warped image
    """
    import cv2
    
    h, w = image.shape[:2]
    
    if output_size is None:
        # Compute output size dari transformed corners
        corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
        corners_transformed = cv2.perspectiveTransform(corners, H)
        
        min_x = int(np.floor(corners_transformed[:, :, 0].min()))
        max_x = int(np.ceil(corners_transformed[:, :, 0].max()))
        min_y = int(np.floor(corners_transformed[:, :, 1].min()))
        max_y = int(np.ceil(corners_transformed[:, :, 1].max()))
        
        output_size = (max_x - min_x, max_y - min_y)
        
        # Adjust H untuk offset
        translation = np.array([
            [1, 0, -min_x],
            [0, 1, -min_y],
            [0, 0, 1]
        ], dtype=np.float64)
        H = translation @ H
    
    # Warp
    warped = cv2.warpPerspective(image, H, output_size)
    
    return warped

def warp_and_blend(img1, img2, H):
    """
    Warp img1 dan blend dengan img2.
    
    Args:
        img1, img2: Input images
        H: Homography dari img1 ke img2
    
    Returns:
        Blended result
    """
    import cv2
    
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Compute corners setelah transformation
    corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    corners1_transformed = cv2.perspectiveTransform(corners1, H)
    
    corners2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
    
    all_corners = np.vstack([corners1_transformed, corners2])
    
    # Compute output size
    min_x = int(np.floor(all_corners[:, :, 0].min()))
    max_x = int(np.ceil(all_corners[:, :, 0].max()))
    min_y = int(np.floor(all_corners[:, :, 1].min()))
    max_y = int(np.ceil(all_corners[:, :, 1].max()))
    
    output_w = max_x - min_x
    output_h = max_y - min_y
    
    # Translation untuk offset
    T = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ], dtype=np.float64)
    
    # Warp img1
    H_adjusted = T @ H
    warped1 = cv2.warpPerspective(img1, H_adjusted, (output_w, output_h))
    
    # Place img2
    result = np.zeros((output_h, output_w, 3), dtype=np.uint8)
    
    # Copy img2
    x_offset = -min_x
    y_offset = -min_y
    result[y_offset:y_offset+h2, x_offset:x_offset+w2] = img2
    
    # Blend (simple: prefer img2 where both exist)
    mask = (warped1 > 0).any(axis=2)
    mask2 = (result > 0).any(axis=2)
    
    # Only warped1 exists
    only_warped = mask & ~mask2
    result[only_warped] = warped1[only_warped]
    
    # Both exist - simple blend
    both = mask & mask2
    result[both] = (0.5 * warped1[both] + 0.5 * result[both]).astype(np.uint8)
    
    return result

# ============================================================
# VISUALISASI
# ============================================================

def visualize_matches(img1, kp1, img2, kp2, matches, mask=None, title="Matches"):
    """
    Visualisasi feature matches.
    """
    import cv2
    import matplotlib.pyplot as plt
    
    # Filter matches berdasarkan mask
    if mask is not None:
        matches_draw = [m for m, inlier in zip(matches, mask) if inlier]
    else:
        matches_draw = matches
    
    # Draw matches
    img_matches = cv2.drawMatches(
        img1, kp1, img2, kp2, matches_draw, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    plt.figure(figsize=(15, 8))
    plt.imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
    plt.title(f"{title} ({len(matches_draw)} matches)")
    plt.axis('off')
    plt.tight_layout()
    
    # Save
    output_path = OUTPUT_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")

def visualize_warping(original, warped, blended, title="Warping"):
    """
    Visualisasi hasil warping.
    """
    import cv2
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Warped")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Blended")
    axes[2].axis('off')
    
    plt.suptitle(title)
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_feature_detection():
    """Demo feature detection dan matching."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Feature Detection & Matching")
    print("="*60)
    
    # Load images
    img1, img2, gt_H = load_images()
    
    # Test different methods
    methods = ['ORB', 'SIFT', 'AKAZE']
    
    print("\n" + "-"*60)
    print(f"{'Method':<10} {'Keypoints 1':<15} {'Keypoints 2':<15} {'Matches':<10} {'Time (ms)':<10}")
    print("-"*60)
    
    for method in methods:
        start_time = time.time()
        
        try:
            detector = create_detector(method, NUM_FEATURES)
            kp1, desc1 = detect_and_compute(img1, detector)
            kp2, desc2 = detect_and_compute(img2, detector)
            matches = match_features(desc1, desc2, ratio_thresh=RATIO_THRESHOLD)
            
            elapsed = (time.time() - start_time) * 1000
            
            print(f"{method:<10} {len(kp1):<15} {len(kp2):<15} {len(matches):<10} {elapsed:<10.2f}")
            
            # Visualize
            visualize_matches(img1, kp1, img2, kp2, matches, title=f"Matches_{method}")
            
        except Exception as e:
            print(f"{method:<10} Error: {e}")
    
    return img1, img2, gt_H

def demo_homography_estimation():
    """Demo homography estimation dengan RANSAC."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: Homography Estimation")
    print("="*60)
    
    # Load images
    img1, img2, gt_H = load_images()
    
    # Detect features
    detector = create_detector(FEATURE_METHOD, NUM_FEATURES)
    kp1, desc1 = detect_and_compute(img1, detector)
    kp2, desc2 = detect_and_compute(img2, detector)
    matches = match_features(desc1, desc2, ratio_thresh=RATIO_THRESHOLD)
    
    print(f"\nFeatures: {len(kp1)} x {len(kp2)}")
    print(f"Initial matches: {len(matches)}")
    
    # Test different RANSAC thresholds
    thresholds = [1.0, 3.0, 5.0, 10.0]
    
    print("\n" + "-"*60)
    print(f"{'Threshold':<12} {'Inliers':<10} {'Mean Error':<12} {'Max Error':<12}")
    print("-"*60)
    
    for thresh in thresholds:
        H, mask = estimate_homography(kp1, kp2, matches, reproj_thresh=thresh)
        
        if H is not None:
            inliers = mask.sum()
            mean_err, max_err, _ = compute_reprojection_error(kp1, kp2, matches, H, mask)
            
            print(f"{thresh:<12.1f} {inliers:<10} {mean_err:<12.4f} {max_err:<12.4f}")
    
    # Final estimation dengan default threshold
    H, mask = estimate_homography(kp1, kp2, matches, reproj_thresh=RANSAC_REPROJ_THRESHOLD)
    
    # Visualize inliers
    visualize_matches(img1, kp1, img2, kp2, matches, mask, title="Inlier_Matches")
    
    # Compare dengan ground truth jika ada
    if gt_H is not None:
        print(f"\nGround Truth Homography:\n{gt_H}")
        print(f"\nEstimated Homography:\n{H}")
    
    return img1, img2, H, kp1, kp2, matches, mask

def demo_image_warping():
    """Demo image warping."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: Image Warping")
    print("="*60)
    
    # Load images
    img1, img2, _ = load_images()
    
    # Estimate homography
    detector = create_detector(FEATURE_METHOD, NUM_FEATURES)
    kp1, desc1 = detect_and_compute(img1, detector)
    kp2, desc2 = detect_and_compute(img2, detector)
    matches = match_features(desc1, desc2, ratio_thresh=RATIO_THRESHOLD)
    
    H, mask = estimate_homography(kp1, kp2, matches, reproj_thresh=RANSAC_REPROJ_THRESHOLD)
    
    if H is None:
        print("  ✗ Tidak dapat mengestimasi homography!")
        return
    
    print(f"\nHomography matrix:\n{H}")
    
    # Warp img1
    warped = warp_image(img1, H, output_size=(img2.shape[1], img2.shape[0]))
    
    # Blend
    blended = warp_and_blend(img1, img2, H)
    
    # Save results
    cv2.imwrite(str(OUTPUT_DIR / "warped.png"), warped)
    cv2.imwrite(str(OUTPUT_DIR / "blended.png"), blended)
    
    # Visualize
    visualize_warping(img1, warped, blended, "Image_Warping")
    
    print(f"\n✓ Warped image saved: warped.png")
    print(f"✓ Blended image saved: blended.png")
    
    return warped, blended

def demo_manual_homography():
    """Demo manual homography transformation."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: Manual Homography Transformations")
    print("="*60)
    
    # Create sample image
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (500, 300), (255, 255, 255), -1)
    cv2.putText(img, "HELLO", (150, 230), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
    
    # Different transformations
    h, w = img.shape[:2]
    
    # 1. Rotation
    angle = 30
    cx, cy = w // 2, h // 2
    R = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    rotated = cv2.warpAffine(img, R, (w, h))
    
    # 2. Perspective (simulate viewing from side)
    pts1 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    pts2 = np.float32([[100, 50], [w-50, 0], [w-100, h], [50, h-50]])
    H_perspective = cv2.getPerspectiveTransform(pts1, pts2)
    perspective = cv2.warpPerspective(img, H_perspective, (w, h))
    
    # 3. Shear
    shear = np.float32([[1, 0.3, 0], [0, 1, 0]])
    sheared = cv2.warpAffine(img, shear, (int(w * 1.3), h))
    
    # Save results
    cv2.imwrite(str(OUTPUT_DIR / "transform_original.png"), img)
    cv2.imwrite(str(OUTPUT_DIR / "transform_rotated.png"), rotated)
    cv2.imwrite(str(OUTPUT_DIR / "transform_perspective.png"), perspective)
    cv2.imwrite(str(OUTPUT_DIR / "transform_sheared.png"), sheared)
    
    print(f"  ✓ Saved: transform_original.png")
    print(f"  ✓ Saved: transform_rotated.png (angle={angle}°)")
    print(f"  ✓ Saved: transform_perspective.png")
    print(f"  ✓ Saved: transform_sheared.png")
    
    return img, rotated, perspective, sheared

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    print("="*60)
    print("PRAKTIKUM 14.1: IMAGE WARPING DAN HOMOGRAPHY")
    print("="*60)
    
    # Check dependencies
    if not check_opencv():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_feature_detection()
    
    demo_homography_estimation()
    
    demo_image_warping()
    
    demo_manual_homography()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nKey Concepts:")
    print("  1. Homography: Transformasi proyektif 2D (3x3 matrix)")
    print("  2. Feature Detection: SIFT, ORB, AKAZE")
    print("  3. Feature Matching: Ratio test untuk filtering")
    print("  4. RANSAC: Robust estimation dengan outlier rejection")
    print("  5. Warping: cv2.warpPerspective() untuk apply homography")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
