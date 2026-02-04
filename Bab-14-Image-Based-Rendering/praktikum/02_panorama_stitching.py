"""
Praktikum 14.2: Panorama Stitching
==================================

Program ini mendemonstrasikan panorama stitching:
1. Image alignment dengan homography
2. Cylindrical projection
3. Multi-image stitching
4. Blending techniques

Teori:
------
Panorama stitching menggabungkan multiple images dengan
overlapping region menjadi satu gambar panoramic.

Pipeline:
1. Feature detection & matching
2. Homography estimation
3. Image warping
4. Blending (alpha, multi-band)

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time
import glob

# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent / "data" / "panorama_sequences"
OUTPUT_DIR = Path(__file__).parent / "output" / "output2"

# Stitching parameters
FEATURE_METHOD = 'SIFT'             # Feature detector
NUM_FEATURES = 2000                 # Jumlah features
RATIO_THRESHOLD = 0.7               # Ratio test threshold
RANSAC_THRESHOLD = 4.0              # RANSAC reprojection threshold

# Blending parameters
BLEND_WIDTH = 50                    # Width of blending region
FEATHER_AMOUNT = 0.5                # Feather blending amount

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

def load_panorama_images(image_dir=None, max_images=None):
    """
    Load sequence of images untuk panorama.
    """
    import cv2
    
    if image_dir is None:
        image_dir = DATA_DIR
    
    image_dir = Path(image_dir)
    
    # Find images
    patterns = ['*.png', '*.jpg', '*.jpeg', '*.ppm']
    image_files = []
    
    for pattern in patterns:
        image_files.extend(sorted(image_dir.glob(pattern)))
    
    if len(image_files) == 0:
        print(f"  ⚠ Tidak ada gambar di {image_dir}, membuat sample...")
        return create_sample_panorama_sequence()
    
    if max_images:
        image_files = image_files[:max_images]
    
    images = []
    for f in image_files:
        img = cv2.imread(str(f))
        if img is not None:
            images.append(img)
            print(f"  ✓ Loaded: {f.name}")
    
    return images

def create_sample_panorama_sequence(num_images=4):
    """Buat sample panorama sequence."""
    import cv2
    
    print(f"\n[Generate] Membuat {num_images} sample images...")
    
    # Create wide scene
    scene_width = 800 * num_images // 2
    scene_height = 480
    
    # Create scene with distinctive features
    scene = np.zeros((scene_height, scene_width, 3), dtype=np.uint8)
    
    # Background gradient
    for x in range(scene_width):
        t = x / scene_width
        r = int(50 + 150 * t)
        g = int(100 + 100 * np.sin(t * np.pi))
        b = int(200 - 100 * t)
        scene[:, x] = [b, g, r]
    
    # Add features
    np.random.seed(42)
    for i in range(100):
        x = np.random.randint(50, scene_width - 50)
        y = np.random.randint(50, scene_height - 50)
        size = np.random.randint(10, 40)
        color = [np.random.randint(0, 255) for _ in range(3)]
        
        if np.random.random() > 0.5:
            cv2.circle(scene, (x, y), size, color, -1)
        else:
            cv2.rectangle(scene, (x - size, y - size), (x + size, y + size), color, -1)
    
    # Add grid lines untuk tracking
    for x in range(0, scene_width, 100):
        cv2.line(scene, (x, 0), (x, scene_height), (255, 255, 255), 1)
    
    # Extract overlapping windows
    images = []
    window_width = 640
    overlap = int(window_width * 0.3)  # 30% overlap
    step = window_width - overlap
    
    for i in range(num_images):
        start_x = i * step
        end_x = start_x + window_width
        
        if end_x > scene_width:
            start_x = scene_width - window_width
            end_x = scene_width
        
        img = scene[:, start_x:end_x].copy()
        images.append(img)
    
    return images

# ============================================================
# FEATURE MATCHING
# ============================================================

def detect_and_match(img1, img2, method='SIFT', ratio_thresh=0.7):
    """
    Detect features dan match antara dua gambar.
    """
    import cv2
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Create detector
    if method == 'SIFT':
        detector = cv2.SIFT_create(nfeatures=NUM_FEATURES)
        bf = cv2.BFMatcher(cv2.NORM_L2)
    elif method == 'ORB':
        detector = cv2.ORB_create(nfeatures=NUM_FEATURES)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    else:
        detector = cv2.AKAZE_create()
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    
    # Detect
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    
    if desc1 is None or desc2 is None:
        return None, None, []
    
    # Match
    matches = bf.knnMatch(desc1, desc2, k=2)
    
    # Ratio test
    good = []
    for m, n in matches:
        if m.distance < ratio_thresh * n.distance:
            good.append(m)
    
    return kp1, kp2, good

def compute_homography(kp1, kp2, matches, reproj_thresh=5.0):
    """Compute homography dari matches."""
    import cv2
    
    if len(matches) < 4:
        return None, None
    
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, reproj_thresh)
    
    return H, mask

# ============================================================
# CYLINDRICAL PROJECTION
# ============================================================

def cylindrical_warp(img, focal_length):
    """
    Warp image ke cylindrical projection.
    
    Args:
        img: Input image
        focal_length: Focal length dalam pixels
    
    Returns:
        Warped image, mask
    """
    import cv2
    
    h, w = img.shape[:2]
    
    # Create meshgrid
    y_i, x_i = np.indices((h, w))
    
    # Center coordinates
    x_c = w / 2
    y_c = h / 2
    
    # Cylindrical coordinates
    theta = (x_i - x_c) / focal_length
    h_cyl = (y_i - y_c) / focal_length
    
    # Convert back to image coordinates
    x_hat = np.sin(theta)
    y_hat = h_cyl
    z_hat = np.cos(theta)
    
    x_img = focal_length * x_hat / z_hat + x_c
    y_img = focal_length * y_hat / z_hat + y_c
    
    # Remap
    x_img = x_img.astype(np.float32)
    y_img = y_img.astype(np.float32)
    
    warped = cv2.remap(img, x_img, y_img, cv2.INTER_LINEAR)
    
    # Create mask
    mask = cv2.remap(np.ones((h, w), dtype=np.uint8) * 255, 
                     x_img, y_img, cv2.INTER_LINEAR)
    
    return warped, mask

def estimate_focal_length(images, method='homography'):
    """
    Estimasi focal length dari sequence images.
    
    Args:
        images: List of images
        method: 'homography' atau 'fixed'
    
    Returns:
        Estimated focal length
    """
    if method == 'fixed':
        # Assume standard FOV
        return images[0].shape[1]  # width sebagai approximation
    
    # Estimate dari homography
    if len(images) < 2:
        return images[0].shape[1]
    
    kp1, kp2, matches = detect_and_match(images[0], images[1])
    
    if len(matches) < 10:
        return images[0].shape[1]
    
    H, _ = compute_homography(kp1, kp2, matches)
    
    if H is None:
        return images[0].shape[1]
    
    # Estimasi dari H
    # Simplified: gunakan average image dimension
    h, w = images[0].shape[:2]
    
    return int(np.sqrt(w * w + h * h))

# ============================================================
# BLENDING
# ============================================================

def simple_blend(img1, img2, mask1, mask2):
    """
    Simple averaging blend.
    """
    mask1 = mask1.astype(float) / 255
    mask2 = mask2.astype(float) / 255
    
    if len(mask1.shape) == 2:
        mask1 = mask1[:, :, np.newaxis]
        mask2 = mask2[:, :, np.newaxis]
    
    # Where both have values, average
    combined_mask = mask1 + mask2
    combined_mask = np.maximum(combined_mask, 1e-10)  # Avoid division by zero
    
    blended = (img1 * mask1 + img2 * mask2) / combined_mask
    
    return blended.astype(np.uint8)

def feather_blend(img1, img2, mask1, mask2, feather_width=50):
    """
    Feather (gradient) blending di overlap region.
    """
    import cv2
    
    # Find overlap
    overlap = (mask1 > 0) & (mask2 > 0)
    
    if not np.any(overlap):
        return simple_blend(img1, img2, mask1, mask2)
    
    # Create feathered masks
    dist1 = cv2.distanceTransform((mask1 > 0).astype(np.uint8), cv2.DIST_L2, 5)
    dist2 = cv2.distanceTransform((mask2 > 0).astype(np.uint8), cv2.DIST_L2, 5)
    
    # Normalize distances dalam overlap region
    total_dist = dist1 + dist2
    total_dist = np.maximum(total_dist, 1e-10)
    
    alpha1 = dist1 / total_dist
    alpha2 = dist2 / total_dist
    
    # Apply blending
    alpha1 = alpha1[:, :, np.newaxis]
    alpha2 = alpha2[:, :, np.newaxis]
    
    blended = (img1 * alpha1 + img2 * alpha2).astype(np.uint8)
    
    # Handle non-overlap regions
    only1 = (mask1 > 0) & (mask2 == 0)
    only2 = (mask2 > 0) & (mask1 == 0)
    
    result = np.zeros_like(img1)
    result[only1] = img1[only1]
    result[only2] = img2[only2]
    result[overlap] = blended[overlap]
    
    return result

def multiband_blend(img1, img2, mask, num_levels=5):
    """
    Multi-band blending menggunakan Laplacian pyramids.
    
    Args:
        img1, img2: Input images (sama size)
        mask: Binary mask (white = img1, black = img2)
        num_levels: Number of pyramid levels
    
    Returns:
        Blended image
    """
    import cv2
    
    # Ensure same size
    h, w = img1.shape[:2]
    
    # Make dimensions divisible by 2^num_levels
    new_h = h - (h % (2 ** num_levels))
    new_w = w - (w % (2 ** num_levels))
    
    img1 = img1[:new_h, :new_w]
    img2 = img2[:new_h, :new_w]
    mask = mask[:new_h, :new_w]
    
    # Build Gaussian pyramids untuk mask
    mask_float = mask.astype(float) / 255
    if len(mask_float.shape) == 2:
        mask_float = np.stack([mask_float] * 3, axis=2)
    
    G_mask = [mask_float.copy()]
    for i in range(num_levels):
        G_mask.append(cv2.pyrDown(G_mask[-1]))
    
    # Build Laplacian pyramids untuk images
    def build_laplacian_pyramid(img, levels):
        G = [img.astype(float)]
        for i in range(levels):
            G.append(cv2.pyrDown(G[-1]))
        
        L = []
        for i in range(levels):
            size = (G[i].shape[1], G[i].shape[0])
            upsampled = cv2.pyrUp(G[i+1], dstsize=size)
            L.append(G[i] - upsampled)
        L.append(G[-1])
        
        return L
    
    L1 = build_laplacian_pyramid(img1, num_levels)
    L2 = build_laplacian_pyramid(img2, num_levels)
    
    # Blend pyramids
    L_blended = []
    for l1, l2, gm in zip(L1, L2, G_mask):
        blended = l1 * gm + l2 * (1 - gm)
        L_blended.append(blended)
    
    # Reconstruct
    result = L_blended[-1]
    for i in range(num_levels - 1, -1, -1):
        size = (L_blended[i].shape[1], L_blended[i].shape[0])
        result = cv2.pyrUp(result, dstsize=size) + L_blended[i]
    
    return np.clip(result, 0, 255).astype(np.uint8)

# ============================================================
# PANORAMA STITCHING
# ============================================================

def stitch_pair(img1, img2, blend_method='feather'):
    """
    Stitch dua gambar.
    
    Args:
        img1, img2: Input images
        blend_method: 'simple', 'feather', 'multiband'
    
    Returns:
        Stitched image
    """
    import cv2
    
    # Match features
    kp1, kp2, matches = detect_and_match(img1, img2, FEATURE_METHOD, RATIO_THRESHOLD)
    
    if len(matches) < 10:
        print(f"  ⚠ Tidak cukup matches ({len(matches)})")
        return None
    
    # Compute homography (img2 -> img1)
    # Note: kita warp img2 ke coordinate system img1
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, RANSAC_THRESHOLD)
    
    if H is None:
        print("  ✗ Gagal mengestimasi homography")
        return None
    
    inliers = mask.sum() if mask is not None else 0
    print(f"  ✓ Matches: {len(matches)}, Inliers: {inliers}")
    
    # Determine output canvas size
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Transform corners of img2
    corners2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
    corners2_transformed = cv2.perspectiveTransform(corners2, H)
    
    # All corners
    corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    all_corners = np.vstack([corners1, corners2_transformed])
    
    # Bounding box
    min_x = int(np.floor(all_corners[:, :, 0].min()))
    max_x = int(np.ceil(all_corners[:, :, 0].max()))
    min_y = int(np.floor(all_corners[:, :, 1].min()))
    max_y = int(np.ceil(all_corners[:, :, 1].max()))
    
    # Translation
    translation = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ], dtype=np.float64)
    
    output_w = max_x - min_x
    output_h = max_y - min_y
    
    # Limit size
    if output_w > 5000 or output_h > 3000:
        print(f"  ⚠ Output terlalu besar ({output_w}x{output_h}), membatasi")
        scale = min(5000 / output_w, 3000 / output_h)
        output_w = int(output_w * scale)
        output_h = int(output_h * scale)
    
    # Warp images
    H_adjusted = translation @ H
    warped2 = cv2.warpPerspective(img2, H_adjusted, (output_w, output_h))
    
    # Create canvas dan place img1
    canvas = np.zeros((output_h, output_w, 3), dtype=np.uint8)
    x_offset = -min_x
    y_offset = -min_y
    
    # Ensure bounds
    y_end = min(y_offset + h1, output_h)
    x_end = min(x_offset + w1, output_w)
    h1_crop = y_end - y_offset
    w1_crop = x_end - x_offset
    
    canvas[y_offset:y_end, x_offset:x_end] = img1[:h1_crop, :w1_crop]
    
    # Create masks
    mask1 = np.zeros((output_h, output_w), dtype=np.uint8)
    mask1[y_offset:y_end, x_offset:x_end] = 255
    
    mask2 = (warped2.sum(axis=2) > 0).astype(np.uint8) * 255
    
    # Blend
    if blend_method == 'simple':
        result = simple_blend(canvas, warped2, mask1, mask2)
    elif blend_method == 'feather':
        result = feather_blend(canvas, warped2, mask1, mask2)
    elif blend_method == 'multiband':
        blend_mask = mask1.copy()
        blend_mask[mask2 > 0] = 0
        result = multiband_blend(canvas, warped2, blend_mask)
    else:
        result = simple_blend(canvas, warped2, mask1, mask2)
    
    return result

def stitch_multiple(images, blend_method='feather'):
    """
    Stitch multiple images.
    
    Args:
        images: List of images
        blend_method: Blending method
    
    Returns:
        Final panorama
    """
    if len(images) < 2:
        return images[0] if images else None
    
    print(f"\n[Stitching] {len(images)} images...")
    
    # Start with first image
    panorama = images[0].copy()
    
    for i in range(1, len(images)):
        print(f"\n  Adding image {i+1}/{len(images)}...")
        
        result = stitch_pair(panorama, images[i], blend_method)
        
        if result is not None:
            panorama = result
        else:
            print(f"  ⚠ Skipping image {i+1}")
    
    return panorama

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_basic_stitching():
    """Demo basic two-image stitching."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Basic Two-Image Stitching")
    print("="*60)
    
    # Load images
    images = load_panorama_images(max_images=2)
    
    if len(images) < 2:
        print("  ✗ Perlu minimal 2 images!")
        return None
    
    print(f"\n  Image 1: {images[0].shape}")
    print(f"  Image 2: {images[1].shape}")
    
    # Stitch
    panorama = stitch_pair(images[0], images[1], 'feather')
    
    if panorama is not None:
        cv2.imwrite(str(OUTPUT_DIR / "basic_stitch.jpg"), panorama)
        print(f"\n✓ Saved: basic_stitch.jpg ({panorama.shape})")
    
    return panorama

def demo_blending_comparison():
    """Demo perbandingan blending methods."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: Blending Methods Comparison")
    print("="*60)
    
    # Load images
    images = load_panorama_images(max_images=2)
    
    if len(images) < 2:
        return
    
    methods = ['simple', 'feather', 'multiband']
    results = {}
    
    for method in methods:
        print(f"\n  Blending: {method}...")
        result = stitch_pair(images[0], images[1], method)
        
        if result is not None:
            results[method] = result
            cv2.imwrite(str(OUTPUT_DIR / f"blend_{method}.jpg"), result)
            print(f"  ✓ Saved: blend_{method}.jpg")
    
    return results

def demo_multi_image_panorama():
    """Demo multi-image panorama."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: Multi-Image Panorama")
    print("="*60)
    
    # Load all images
    images = load_panorama_images()
    
    if len(images) < 2:
        return None
    
    print(f"\nLoaded {len(images)} images")
    
    # Stitch
    panorama = stitch_multiple(images, 'feather')
    
    if panorama is not None:
        cv2.imwrite(str(OUTPUT_DIR / "panorama_full.jpg"), panorama, 
                    [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"\n✓ Saved: panorama_full.jpg ({panorama.shape})")
    
    return panorama

def demo_cylindrical_panorama():
    """Demo cylindrical projection panorama."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: Cylindrical Projection Panorama")
    print("="*60)
    
    # Load images
    images = load_panorama_images()
    
    if len(images) < 2:
        return None
    
    # Estimate focal length
    focal_length = estimate_focal_length(images)
    print(f"\n  Estimated focal length: {focal_length}")
    
    # Warp to cylindrical
    print("\n  Warping to cylindrical...")
    warped_images = []
    
    for i, img in enumerate(images):
        warped, mask = cylindrical_warp(img, focal_length)
        warped_images.append(warped)
        print(f"    Image {i+1}: done")
    
    # Stitch cylindrical images
    print("\n  Stitching cylindrical images...")
    panorama = stitch_multiple(warped_images, 'feather')
    
    if panorama is not None:
        cv2.imwrite(str(OUTPUT_DIR / "panorama_cylindrical.jpg"), panorama,
                    [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"\n✓ Saved: panorama_cylindrical.jpg ({panorama.shape})")
    
    return panorama

def demo_opencv_stitcher():
    """Demo menggunakan OpenCV Stitcher class."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 5: OpenCV Stitcher Class")
    print("="*60)
    
    # Load images
    images = load_panorama_images()
    
    if len(images) < 2:
        return None
    
    print(f"\n  Using OpenCV Stitcher with {len(images)} images...")
    
    # Create stitcher
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    
    # Stitch
    start_time = time.time()
    status, panorama = stitcher.stitch(images)
    elapsed = time.time() - start_time
    
    status_names = {
        cv2.Stitcher_OK: "OK",
        cv2.Stitcher_ERR_NEED_MORE_IMGS: "Need more images",
        cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Homography estimation failed",
        cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Camera params adjustment failed"
    }
    
    print(f"\n  Status: {status_names.get(status, 'Unknown')}")
    print(f"  Time: {elapsed:.2f}s")
    
    if status == cv2.Stitcher_OK:
        cv2.imwrite(str(OUTPUT_DIR / "opencv_stitcher.jpg"), panorama,
                    [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"  ✓ Saved: opencv_stitcher.jpg ({panorama.shape})")
        return panorama
    
    return None

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import cv2
    
    print("="*60)
    print("PRAKTIKUM 14.2: PANORAMA STITCHING")
    print("="*60)
    
    # Check dependencies
    if not check_opencv():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_basic_stitching()
    
    demo_blending_comparison()
    
    demo_multi_image_panorama()
    
    demo_cylindrical_panorama()
    
    demo_opencv_stitcher()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nKey Concepts:")
    print("  1. Feature matching untuk alignment")
    print("  2. Homography estimation dengan RANSAC")
    print("  3. Cylindrical projection untuk 360°")
    print("  4. Blending techniques:")
    print("     - Simple: averaging overlap")
    print("     - Feather: gradient blending")
    print("     - Multi-band: Laplacian pyramid")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
