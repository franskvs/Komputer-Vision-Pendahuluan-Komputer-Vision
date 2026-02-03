"""
Praktikum 14.4: View Interpolation
==================================

Program ini mendemonstrasikan view interpolation:
1. Linear blending antar views
2. Depth-based view synthesis
3. Forward/backward warping
4. Occlusion handling

Teori:
------
View Interpolation menghasilkan novel views antara
dua atau lebih input views.

Pendekatan:
1. Image-based: Direct pixel interpolation
2. Depth-based: Gunakan depth untuk 3D warping
3. Flow-based: Gunakan optical flow

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time

# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

# View interpolation parameters
NUM_INTERPOLATED_FRAMES = 10       # Jumlah frame interpolasi
DEPTH_SCALE = 50.0                 # Skala depth untuk warping
OCCLUSION_THRESHOLD = 10           # Threshold untuk deteksi oklusi

# Hole filling parameters
HOLE_FILL_METHOD = 'inpaint'       # 'inpaint', 'interpolate', 'none'
INPAINT_RADIUS = 5                 # Radius inpainting

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

def load_stereo_pair():
    """Load stereo image pair."""
    import cv2
    
    left_path = DATA_DIR / "stereo_pairs" / "left_01.png"
    right_path = DATA_DIR / "stereo_pairs" / "right_01.png"
    
    if left_path.exists() and right_path.exists():
        left = cv2.imread(str(left_path))
        right = cv2.imread(str(right_path))
        
        if left is not None and right is not None:
            return left, right
    
    print("  Membuat synthetic stereo pair...")
    return create_synthetic_stereo()

def create_synthetic_stereo():
    """Buat synthetic stereo pair dengan known depth."""
    import cv2
    
    h, w = 480, 640
    
    # Create scene dengan objects di berbagai depth
    left = np.zeros((h, w, 3), dtype=np.uint8)
    right = np.zeros((h, w, 3), dtype=np.uint8)
    depth = np.zeros((h, w), dtype=np.float32)
    
    # Background
    for y in range(h):
        bg_color = [int(50 + 100 * y / h), int(100 + 50 * y / h), 150]
        left[y, :] = bg_color
        right[y, :] = bg_color
    depth[:] = 100
    
    # Objects dengan different depths dan disparities
    # Disparity = baseline * focal_length / depth
    baseline = 5  # Simulated baseline
    focal = w     # Simulated focal length
    
    objects = [
        # (center_x, center_y, radius, depth, color)
        (150, 200, 50, 30, (255, 100, 100)),
        (320, 240, 70, 50, (100, 255, 100)),
        (480, 280, 40, 20, (100, 100, 255)),
        (250, 350, 60, 40, (255, 255, 100)),
    ]
    
    for cx, cy, radius, obj_depth, color in objects:
        # Disparity
        disparity = int(baseline * focal / obj_depth) // 10
        
        # Draw pada left
        cv2.circle(left, (cx, cy), radius, color, -1)
        
        # Draw pada right (shifted)
        cv2.circle(right, (cx + disparity, cy), radius, color, -1)
        
        # Update depth
        y, x = np.ogrid[:h, :w]
        mask = (x - cx)**2 + (y - cy)**2 <= radius**2
        depth[mask] = obj_depth
    
    # Add texture
    np.random.seed(42)
    for _ in range(50):
        x = np.random.randint(0, w)
        y = np.random.randint(0, h)
        d = depth[y, x]
        disp = int(baseline * focal / d) // 10
        color = [np.random.randint(100, 200) for _ in range(3)]
        
        cv2.circle(left, (x, y), 3, color, -1)
        cv2.circle(right, (x + disp, y), 3, color, -1)
    
    return left, right

def load_depth_map(filename=None):
    """Load atau compute depth map."""
    import cv2
    
    if filename:
        path = DATA_DIR / "stereo_pairs" / filename
        if path.exists():
            depth = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
            if depth is not None:
                return depth.astype(np.float32)
    
    # Compute dari stereo
    left, right = load_stereo_pair()
    return compute_depth_from_stereo(left, right)

def compute_depth_from_stereo(left, right):
    """Compute depth dari stereo pair."""
    import cv2
    
    # Convert to grayscale
    gray_left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    
    # Stereo matching
    stereo = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=64,
        blockSize=5,
        P1=8 * 3 * 5**2,
        P2=32 * 3 * 5**2,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
    
    disparity = stereo.compute(gray_left, gray_right)
    disparity = disparity.astype(np.float32) / 16.0
    
    # Convert ke depth (simplified)
    # depth = baseline * focal / disparity
    disparity = np.maximum(disparity, 1)
    depth = 1000.0 / disparity
    
    return depth

# ============================================================
# LINEAR VIEW INTERPOLATION
# ============================================================

def linear_interpolate(img1, img2, t):
    """
    Simple linear interpolation antara dua images.
    
    Args:
        img1, img2: Input images
        t: Interpolation factor (0 = img1, 1 = img2)
    
    Returns:
        Interpolated image
    """
    result = (1 - t) * img1.astype(float) + t * img2.astype(float)
    return result.astype(np.uint8)

def generate_linear_interpolation(img1, img2, num_frames):
    """
    Generate sequence interpolasi linear.
    
    Args:
        img1, img2: Input images
        num_frames: Jumlah frame output
    
    Returns:
        List of interpolated frames
    """
    frames = []
    
    for i in range(num_frames):
        t = i / (num_frames - 1)
        frame = linear_interpolate(img1, img2, t)
        frames.append(frame)
    
    return frames

# ============================================================
# FLOW-BASED INTERPOLATION
# ============================================================

def compute_optical_flow(img1, img2):
    """
    Compute optical flow antara dua images.
    
    Args:
        img1, img2: Input images (BGR)
    
    Returns:
        flow: Optical flow (h, w, 2)
    """
    import cv2
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Farneback optical flow
    flow = cv2.calcOpticalFlowFarneback(
        gray1, gray2,
        None,
        pyr_scale=0.5,
        levels=3,
        winsize=15,
        iterations=3,
        poly_n=5,
        poly_sigma=1.2,
        flags=0
    )
    
    return flow

def warp_with_flow(img, flow):
    """
    Warp image menggunakan optical flow.
    
    Args:
        img: Input image
        flow: Optical flow
    
    Returns:
        Warped image
    """
    import cv2
    
    h, w = img.shape[:2]
    
    # Create coordinate map
    y, x = np.mgrid[:h, :w].astype(np.float32)
    
    # Add flow
    x_new = x + flow[:, :, 0]
    y_new = y + flow[:, :, 1]
    
    # Remap
    warped = cv2.remap(img, x_new, y_new, cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_CONSTANT)
    
    return warped

def flow_interpolation(img1, img2, t, flow_forward=None, flow_backward=None):
    """
    Interpolasi menggunakan bidirectional optical flow.
    
    Args:
        img1, img2: Input images
        t: Interpolation factor
        flow_forward: Flow dari img1 ke img2
        flow_backward: Flow dari img2 ke img1
    
    Returns:
        Interpolated image
    """
    import cv2
    
    if flow_forward is None:
        flow_forward = compute_optical_flow(img1, img2)
    if flow_backward is None:
        flow_backward = compute_optical_flow(img2, img1)
    
    # Warp img1 forward
    flow_1_to_t = flow_forward * t
    warped1 = warp_with_flow(img1, flow_1_to_t)
    
    # Warp img2 backward
    flow_2_to_t = flow_backward * (1 - t)
    warped2 = warp_with_flow(img2, flow_2_to_t)
    
    # Blend
    result = linear_interpolate(warped1, warped2, t)
    
    return result

def generate_flow_interpolation(img1, img2, num_frames):
    """
    Generate interpolated frames menggunakan optical flow.
    
    Args:
        img1, img2: Input images
        num_frames: Jumlah frame
    
    Returns:
        List of interpolated frames
    """
    # Compute flows once
    flow_forward = compute_optical_flow(img1, img2)
    flow_backward = compute_optical_flow(img2, img1)
    
    frames = []
    for i in range(num_frames):
        t = i / (num_frames - 1)
        frame = flow_interpolation(img1, img2, t, flow_forward, flow_backward)
        frames.append(frame)
    
    return frames

# ============================================================
# DEPTH-BASED VIEW SYNTHESIS
# ============================================================

def forward_warp(img, depth, translation, focal_length=None):
    """
    Forward warp image berdasarkan depth.
    
    Args:
        img: Input image
        depth: Depth map
        translation: Camera translation [tx, ty, tz]
        focal_length: Focal length (default: image width)
    
    Returns:
        Warped image, validity mask
    """
    import cv2
    
    h, w = img.shape[:2]
    
    if focal_length is None:
        focal_length = w
    
    tx, ty, tz = translation
    
    # Create output
    output = np.zeros_like(img)
    depth_buffer = np.full((h, w), np.inf)
    
    # Center
    cx = w / 2
    cy = h / 2
    
    for y in range(h):
        for x in range(w):
            z = depth[y, x]
            if z <= 0:
                continue
            
            # 3D point
            X = (x - cx) * z / focal_length
            Y = (y - cy) * z / focal_length
            Z = z
            
            # Translate
            X_new = X + tx
            Y_new = Y + ty
            Z_new = Z + tz
            
            if Z_new <= 0:
                continue
            
            # Project back
            x_new = int(X_new * focal_length / Z_new + cx)
            y_new = int(Y_new * focal_length / Z_new + cy)
            
            if 0 <= x_new < w and 0 <= y_new < h:
                if Z_new < depth_buffer[y_new, x_new]:
                    output[y_new, x_new] = img[y, x]
                    depth_buffer[y_new, x_new] = Z_new
    
    # Validity mask
    mask = depth_buffer < np.inf
    
    return output, mask.astype(np.uint8) * 255

def backward_warp(img, depth, translation, focal_length=None):
    """
    Backward warp - untuk setiap pixel di output, cari source.
    
    Args:
        img: Source image
        depth: Depth map (di target view)
        translation: Camera translation [tx, ty, tz]
        focal_length: Focal length
    
    Returns:
        Warped image
    """
    import cv2
    
    h, w = img.shape[:2]
    
    if focal_length is None:
        focal_length = w
    
    tx, ty, tz = translation
    
    # Center
    cx = w / 2
    cy = h / 2
    
    # Create coordinate grid
    y, x = np.mgrid[:h, :w].astype(np.float32)
    
    # For each target pixel, find source
    # Inverse: X_src = X_tgt - tx, etc.
    z = depth
    
    # Target 3D point
    X_tgt = (x - cx) * z / focal_length
    Y_tgt = (y - cy) * z / focal_length
    Z_tgt = z
    
    # Source 3D point
    X_src = X_tgt - tx
    Y_src = Y_tgt - ty
    Z_src = Z_tgt - tz
    
    # Avoid division by zero
    Z_src = np.maximum(Z_src, 1e-6)
    
    # Project ke source image
    x_src = X_src * focal_length / Z_src + cx
    y_src = Y_src * focal_length / Z_src + cy
    
    # Remap
    x_src = x_src.astype(np.float32)
    y_src = y_src.astype(np.float32)
    
    warped = cv2.remap(img, x_src, y_src, cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_CONSTANT)
    
    return warped

def depth_based_interpolation(img1, img2, depth1, depth2, t, baseline=1.0):
    """
    Interpolasi view menggunakan depth.
    
    Args:
        img1, img2: Input images
        depth1, depth2: Depth maps
        t: Interpolation factor
        baseline: Distance antara cameras
    
    Returns:
        Interpolated image
    """
    import cv2
    
    # Translations
    trans_1_to_t = [baseline * t, 0, 0]
    trans_2_to_t = [-baseline * (1 - t), 0, 0]
    
    # Warp images
    warped1 = backward_warp(img1, depth1, trans_1_to_t)
    warped2 = backward_warp(img2, depth2, trans_2_to_t)
    
    # Create masks (non-zero pixels)
    mask1 = (warped1.sum(axis=2) > 0).astype(float)
    mask2 = (warped2.sum(axis=2) > 0).astype(float)
    
    # Blend dengan weighting
    mask1 = mask1[:, :, np.newaxis] * (1 - t)
    mask2 = mask2[:, :, np.newaxis] * t
    
    total_weight = mask1 + mask2
    total_weight = np.maximum(total_weight, 1e-10)
    
    result = (warped1 * mask1 + warped2 * mask2) / total_weight
    
    # Fill holes
    result = fill_holes(result.astype(np.uint8))
    
    return result

def fill_holes(img, method='inpaint'):
    """
    Fill holes dalam warped image.
    
    Args:
        img: Input image dengan holes (black pixels)
        method: 'inpaint', 'interpolate', 'none'
    
    Returns:
        Image dengan holes filled
    """
    import cv2
    
    if method == 'none':
        return img
    
    # Detect holes
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = (gray == 0).astype(np.uint8)
    
    if method == 'inpaint':
        # OpenCV inpainting
        result = cv2.inpaint(img, mask, INPAINT_RADIUS, cv2.INPAINT_TELEA)
    elif method == 'interpolate':
        # Simple nearest neighbor
        result = img.copy()
        h, w = img.shape[:2]
        
        for y in range(h):
            for x in range(w):
                if mask[y, x]:
                    # Find nearest non-hole pixel
                    for r in range(1, max(h, w)):
                        found = False
                        for dy in range(-r, r+1):
                            for dx in range(-r, r+1):
                                ny, nx = y + dy, x + dx
                                if 0 <= ny < h and 0 <= nx < w:
                                    if not mask[ny, nx]:
                                        result[y, x] = img[ny, nx]
                                        found = True
                                        break
                            if found:
                                break
                        if found:
                            break
    else:
        result = img
    
    return result

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_linear_interpolation():
    """Demo linear interpolation."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Linear View Interpolation")
    print("="*60)
    
    # Load stereo pair
    left, right = load_stereo_pair()
    print(f"\n  Left: {left.shape}")
    print(f"  Right: {right.shape}")
    
    # Generate interpolation
    print(f"\n  Generating {NUM_INTERPOLATED_FRAMES} frames...")
    frames = generate_linear_interpolation(left, right, NUM_INTERPOLATED_FRAMES)
    
    # Save frames
    for i, frame in enumerate(frames):
        filename = f"linear_interp_{i:02d}.jpg"
        cv2.imwrite(str(OUTPUT_DIR / filename), frame)
    
    print(f"  ✓ Saved {len(frames)} frames")
    
    # Create montage
    montage_frames = frames[::max(1, len(frames)//5)]
    montage = np.hstack(montage_frames)
    montage = cv2.resize(montage, None, fx=0.5, fy=0.5)
    cv2.imwrite(str(OUTPUT_DIR / "linear_montage.jpg"), montage)
    print(f"  ✓ Saved: linear_montage.jpg")
    
    return frames

def demo_flow_interpolation():
    """Demo flow-based interpolation."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: Optical Flow Interpolation")
    print("="*60)
    
    # Load stereo pair
    left, right = load_stereo_pair()
    
    # Compute flows
    print("\n  Computing optical flows...")
    start = time.time()
    
    flow_forward = compute_optical_flow(left, right)
    flow_backward = compute_optical_flow(right, left)
    
    elapsed = time.time() - start
    print(f"  Flow computation: {elapsed:.2f}s")
    
    # Visualize flow
    def flow_to_color(flow):
        mag, ang = cv2.cartToPolar(flow[:, :, 0], flow[:, :, 1])
        hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.uint8)
        hsv[:, :, 0] = ang * 180 / np.pi / 2
        hsv[:, :, 1] = 255
        hsv[:, :, 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    flow_vis = flow_to_color(flow_forward)
    cv2.imwrite(str(OUTPUT_DIR / "flow_visualization.jpg"), flow_vis)
    print(f"  ✓ Saved: flow_visualization.jpg")
    
    # Generate interpolation
    print(f"\n  Generating {NUM_INTERPOLATED_FRAMES} frames...")
    frames = []
    for i in range(NUM_INTERPOLATED_FRAMES):
        t = i / (NUM_INTERPOLATED_FRAMES - 1)
        frame = flow_interpolation(left, right, t, flow_forward, flow_backward)
        frames.append(frame)
        
        filename = f"flow_interp_{i:02d}.jpg"
        cv2.imwrite(str(OUTPUT_DIR / filename), frame)
    
    print(f"  ✓ Saved {len(frames)} frames")
    
    # Create montage
    montage_frames = frames[::max(1, len(frames)//5)]
    montage = np.hstack(montage_frames)
    montage = cv2.resize(montage, None, fx=0.5, fy=0.5)
    cv2.imwrite(str(OUTPUT_DIR / "flow_montage.jpg"), montage)
    print(f"  ✓ Saved: flow_montage.jpg")
    
    return frames

def demo_depth_interpolation():
    """Demo depth-based view synthesis."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: Depth-Based View Synthesis")
    print("="*60)
    
    # Load stereo pair
    left, right = load_stereo_pair()
    
    # Compute depth
    print("\n  Computing depth maps...")
    depth = compute_depth_from_stereo(left, right)
    
    # Normalize dan save depth
    depth_vis = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
    depth_vis = depth_vis.astype(np.uint8)
    depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
    cv2.imwrite(str(OUTPUT_DIR / "depth_map.jpg"), depth_vis)
    print(f"  ✓ Saved: depth_map.jpg")
    
    # Generate views
    print(f"\n  Generating {NUM_INTERPOLATED_FRAMES} views...")
    frames = []
    
    for i in range(NUM_INTERPOLATED_FRAMES):
        t = i / (NUM_INTERPOLATED_FRAMES - 1)
        
        frame = depth_based_interpolation(left, right, depth, depth, t, baseline=DEPTH_SCALE)
        frames.append(frame)
        
        filename = f"depth_interp_{i:02d}.jpg"
        cv2.imwrite(str(OUTPUT_DIR / filename), frame)
    
    print(f"  ✓ Saved {len(frames)} frames")
    
    # Create montage
    montage_frames = frames[::max(1, len(frames)//5)]
    montage = np.hstack(montage_frames)
    montage = cv2.resize(montage, None, fx=0.5, fy=0.5)
    cv2.imwrite(str(OUTPUT_DIR / "depth_montage.jpg"), montage)
    print(f"  ✓ Saved: depth_montage.jpg")
    
    return frames

def demo_forward_vs_backward_warp():
    """Demo perbandingan forward dan backward warping."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: Forward vs Backward Warping")
    print("="*60)
    
    # Load data
    left, right = load_stereo_pair()
    depth = compute_depth_from_stereo(left, right)
    
    translation = [20, 0, 0]  # Move right
    
    print(f"\n  Translation: {translation}")
    
    # Forward warp
    print("\n  Forward warping...")
    start = time.time()
    forward, mask_forward = forward_warp(left, depth, translation)
    time_forward = time.time() - start
    print(f"  Time: {time_forward:.3f}s")
    
    # Backward warp
    print("\n  Backward warping...")
    start = time.time()
    backward = backward_warp(left, depth, translation)
    time_backward = time.time() - start
    print(f"  Time: {time_backward:.3f}s")
    
    # Save results
    cv2.imwrite(str(OUTPUT_DIR / "forward_warp.jpg"), forward)
    cv2.imwrite(str(OUTPUT_DIR / "backward_warp.jpg"), backward)
    cv2.imwrite(str(OUTPUT_DIR / "forward_mask.jpg"), mask_forward)
    
    # Fill holes
    forward_filled = fill_holes(forward, 'inpaint')
    cv2.imwrite(str(OUTPUT_DIR / "forward_filled.jpg"), forward_filled)
    
    print(f"\n  ✓ Saved warping results")
    
    # Comparison
    comparison = np.hstack([left, forward_filled, backward])
    comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
    
    # Add labels
    h = comparison.shape[0]
    cv2.putText(comparison, "Original", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(comparison, "Forward", (left.shape[1]//2 + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(comparison, "Backward", (left.shape[1] + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imwrite(str(OUTPUT_DIR / "warp_comparison.jpg"), comparison)
    print(f"  ✓ Saved: warp_comparison.jpg")
    
    return forward_filled, backward

def demo_comparison():
    """Demo perbandingan metode interpolasi."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 5: Method Comparison")
    print("="*60)
    
    # Load stereo
    left, right = load_stereo_pair()
    
    t = 0.5  # Middle frame
    
    print(f"\n  Interpolation at t = {t}")
    
    # Methods
    print("\n  1. Linear interpolation...")
    linear = linear_interpolate(left, right, t)
    
    print("  2. Flow-based interpolation...")
    flow_forward = compute_optical_flow(left, right)
    flow_backward = compute_optical_flow(right, left)
    flow = flow_interpolation(left, right, t, flow_forward, flow_backward)
    
    print("  3. Depth-based interpolation...")
    depth = compute_depth_from_stereo(left, right)
    depth_based = depth_based_interpolation(left, right, depth, depth, t, DEPTH_SCALE)
    
    # Save
    cv2.imwrite(str(OUTPUT_DIR / "compare_linear.jpg"), linear)
    cv2.imwrite(str(OUTPUT_DIR / "compare_flow.jpg"), flow)
    cv2.imwrite(str(OUTPUT_DIR / "compare_depth.jpg"), depth_based)
    
    # Side by side
    comparison = np.hstack([linear, flow, depth_based])
    comparison = cv2.resize(comparison, None, fx=0.6, fy=0.6)
    
    cv2.imwrite(str(OUTPUT_DIR / "method_comparison.jpg"), comparison)
    print(f"\n  ✓ Saved: method_comparison.jpg")
    
    # Quality metrics
    print("\n  Quality comparison (vs linear):")
    
    def mse(a, b):
        return np.mean((a.astype(float) - b.astype(float))**2)
    
    def psnr(a, b):
        m = mse(a, b)
        if m == 0:
            return float('inf')
        return 10 * np.log10(255**2 / m)
    
    print(f"    Flow vs Linear: PSNR = {psnr(flow, linear):.2f} dB")
    print(f"    Depth vs Linear: PSNR = {psnr(depth_based, linear):.2f} dB")
    
    return linear, flow, depth_based

def demo_multiview_interpolation():
    """Demo interpolasi dengan multiple views."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 6: Multi-View Interpolation")
    print("="*60)
    
    # Create 3 views
    print("\n  Creating 3-view setup...")
    
    h, w = 480, 640
    
    # Create scene
    scene = np.zeros((h, w * 2, 3), dtype=np.uint8)
    
    # Background
    for y in range(h):
        color = [int(50 + 150 * y / h), 100, 150]
        scene[y, :] = color
    
    # Objects
    np.random.seed(42)
    for _ in range(30):
        x = np.random.randint(50, w * 2 - 50)
        y = np.random.randint(50, h - 50)
        r = np.random.randint(10, 40)
        color = [np.random.randint(0, 255) for _ in range(3)]
        cv2.circle(scene, (x, y), r, color, -1)
    
    # Extract 3 views
    views = []
    offsets = [0, w // 4, w // 2]
    
    for i, offset in enumerate(offsets):
        view = scene[:, offset:offset + w].copy()
        views.append(view)
    
    # Save views
    for i, view in enumerate(views):
        cv2.imwrite(str(OUTPUT_DIR / f"view_{i+1}.jpg"), view)
    
    print(f"  ✓ Created {len(views)} views")
    
    # Interpolate between views
    print("\n  Interpolating between views...")
    
    all_frames = []
    
    # View 1 -> View 2
    frames_1_2 = generate_linear_interpolation(views[0], views[1], 5)
    all_frames.extend(frames_1_2)
    
    # View 2 -> View 3
    frames_2_3 = generate_linear_interpolation(views[1], views[2], 5)
    all_frames.extend(frames_2_3)
    
    # Save all
    for i, frame in enumerate(all_frames):
        cv2.imwrite(str(OUTPUT_DIR / f"multiview_frame_{i:02d}.jpg"), frame)
    
    print(f"  ✓ Saved {len(all_frames)} interpolated frames")
    
    # Create strip
    strip_frames = all_frames[::2]
    strip = np.hstack([cv2.resize(f, (w//3, h//3)) for f in strip_frames])
    cv2.imwrite(str(OUTPUT_DIR / "multiview_strip.jpg"), strip)
    print(f"  ✓ Saved: multiview_strip.jpg")
    
    return all_frames

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import cv2
    
    print("="*60)
    print("PRAKTIKUM 14.4: VIEW INTERPOLATION")
    print("="*60)
    
    # Check dependencies
    if not check_opencv():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_linear_interpolation()
    
    demo_flow_interpolation()
    
    demo_depth_interpolation()
    
    demo_forward_vs_backward_warp()
    
    demo_comparison()
    
    demo_multiview_interpolation()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nInterpolation Methods:")
    print("  1. Linear: Simple blending (ghosting artifacts)")
    print("  2. Flow-based: Menggunakan optical flow")
    print("  3. Depth-based: 3D warping dengan depth")
    
    print("\nWarping Types:")
    print("  - Forward: Source → Target (holes)")
    print("  - Backward: Target → Source (no holes, smearing)")
    
    print("\nOcclusion Handling:")
    print("  - Inpainting untuk fill holes")
    print("  - Bidirectional warping untuk blending")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
