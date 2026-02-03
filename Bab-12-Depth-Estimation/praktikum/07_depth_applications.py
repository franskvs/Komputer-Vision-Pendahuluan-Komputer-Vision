#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 7: DEPTH MAP APPLICATIONS
=============================================================================
Deskripsi:
    Program untuk mendemonstrasikan berbagai aplikasi dari depth map,
    termasuk segmentasi berbasis depth, bokeh effect, obstacle detection,
    dan konversi ke point cloud 3D.

Aplikasi Depth Map:
    1. Depth-based Segmentation - Memisahkan foreground/background
    2. Bokeh Effect - Blur background seperti kamera profesional
    3. Obstacle Detection - Mendeteksi objek di depan kamera
    4. Point Cloud Generation - Konversi ke representasi 3D
    5. Depth-aware Image Editing - Filter berbasis kedalaman
    6. Distance Measurement - Mengukur jarak ke objek

Konsep:
    - Depth map memberikan informasi 3D dari scene
    - Depth dapat digunakan untuk segmentasi tanpa ML
    - Bokeh effect: blur area dengan depth berbeda dari fokus
    - Obstacle detection: identifikasi objek pada depth tertentu

Output:
    - Hasil segmentasi foreground/background
    - Gambar dengan bokeh effect
    - Visualisasi obstacle detection
    - Point cloud 3D

Penulis: Praktikum Computer Vision
Tanggal: 2024
Python: 3.8+
Dependensi: opencv-python, numpy, matplotlib, open3d (opsional)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time

# =============================================================================
# KONFIGURASI - UBAH SESUAI KEBUTUHAN
# =============================================================================

# Path ke data
DATA_DIR = Path(__file__).parent.parent / "data"

# Input files (dari praktikum sebelumnya)
DEPTH_FILE = DATA_DIR / "depth" / "depth_meters.npy"
DEPTH_FILE_MONO = DATA_DIR / "depth_mono" / "depth_mono_raw.npy"

RGB_IMAGE = DATA_DIR / "stereo" / "synthetic_left.png"
RGB_IMAGE_ALT = DATA_DIR / "images" / "street_scene.png"

# Path output
OUTPUT_DIR = DATA_DIR / "applications"

# Parameter untuk segmentasi
# Range depth untuk foreground (dalam meter atau normalized)
FOREGROUND_MIN_DEPTH = 0.5
FOREGROUND_MAX_DEPTH = 3.0

# Parameter untuk bokeh effect
FOCUS_DEPTH = 2.0  # Depth yang menjadi fokus (meter)
DEPTH_OF_FIELD = 0.5  # Range depth yang tajam (±meters)
MAX_BLUR_KERNEL = 31  # Maximum blur kernel size

# Parameter untuk obstacle detection
OBSTACLE_THRESHOLD = 5.0  # Maksimum depth untuk dianggap obstacle (meter)
GROUND_HEIGHT = -0.3  # Tinggi ground dari kamera (meter, negatif = di bawah)
MIN_OBSTACLE_SIZE = 500  # Minimum pixel untuk dianggap obstacle

# Parameter kamera (untuk point cloud)
FOCAL_LENGTH = 500.0  # pixel
BASELINE = 120.0  # mm

# =============================================================================
# FUNGSI APLIKASI
# =============================================================================

def depth_based_segmentation(depth, rgb, min_depth, max_depth, use_normalized=False):
    """
    Segmentasi berdasarkan range depth.
    
    Args:
        depth: Depth map
        rgb: RGB image
        min_depth, max_depth: Range depth untuk foreground
        use_normalized: True jika depth dalam range 0-1
        
    Returns:
        Dictionary dengan mask, foreground, background
    """
    # Create mask
    if use_normalized:
        # Untuk normalized depth, perlu inversi logika
        # Depth tinggi = dekat (setelah normalisasi biasanya)
        mask = (depth > min_depth) & (depth < max_depth)
    else:
        # Untuk depth dalam meter
        valid = depth > 0
        mask = valid & (depth > min_depth) & (depth < max_depth)
    
    # Clean up mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = mask.astype(bool)
    
    # Create foreground/background
    foreground = rgb.copy()
    background = rgb.copy()
    
    foreground[~mask] = 0
    background[mask] = 0
    
    return {
        'mask': mask,
        'foreground': foreground,
        'background': background,
        'mask_3ch': np.stack([mask] * 3, axis=-1)
    }


def create_bokeh_effect(rgb, depth, focus_depth, dof, max_blur=31, use_normalized=False):
    """
    Membuat efek bokeh (blur background) berdasarkan depth.
    
    Args:
        rgb: RGB image
        depth: Depth map
        focus_depth: Depth yang menjadi fokus
        dof: Depth of field (range yang tajam)
        max_blur: Maximum blur kernel size
        use_normalized: True jika depth normalized
        
    Returns:
        Gambar dengan bokeh effect
    """
    height, width = depth.shape
    result = np.zeros_like(rgb, dtype=np.float32)
    
    # Calculate blur amount based on distance from focus
    if use_normalized:
        # Untuk normalized depth
        focus_norm = focus_depth
        dof_norm = dof
        depth_distance = np.abs(depth - focus_norm)
    else:
        # Untuk depth dalam meter
        valid = depth > 0
        depth_distance = np.abs(depth - focus_depth)
        depth_distance[~valid] = max_blur
    
    # Normalize to blur kernel size
    max_distance = depth_distance.max() if depth_distance.max() > 0 else 1
    blur_map = (depth_distance / max_distance * max_blur).astype(np.int32)
    
    # Apply blur threshold
    blur_map[blur_map < 3] = 0  # No blur for in-focus areas
    
    # Create blurred versions
    blur_levels = list(range(0, max_blur + 1, 2))
    if 0 not in blur_levels:
        blur_levels.insert(0, 0)
    
    blurred_images = {}
    for blur in blur_levels:
        if blur == 0:
            blurred_images[0] = rgb.astype(np.float32)
        else:
            k = blur | 1  # Make odd
            blurred_images[blur] = cv2.GaussianBlur(rgb, (k, k), 0).astype(np.float32)
    
    # Composite
    for y in range(height):
        for x in range(width):
            blur = blur_map[y, x]
            # Find nearest blur level
            nearest = min(blur_levels, key=lambda b: abs(b - blur))
            result[y, x] = blurred_images[nearest][y, x]
    
    return result.astype(np.uint8)


def create_bokeh_effect_fast(rgb, depth, focus_depth, dof, max_blur=31, use_normalized=False):
    """
    Versi cepat dari bokeh effect menggunakan multi-scale blending.
    
    Args:
        rgb: RGB image
        depth: Depth map
        focus_depth: Depth yang menjadi fokus
        dof: Depth of field
        max_blur: Maximum blur kernel size
        use_normalized: True jika depth normalized
        
    Returns:
        Gambar dengan bokeh effect
    """
    # Calculate blur amount
    if use_normalized:
        depth_distance = np.abs(depth - focus_depth)
        max_dist = 1.0
    else:
        valid = depth > 0
        depth_clean = depth.copy()
        depth_clean[~valid] = focus_depth + dof * 5
        depth_distance = np.abs(depth_clean - focus_depth)
        max_dist = max(depth_distance.max(), 1)
    
    # Normalize blur amount
    blur_amount = np.clip(depth_distance / (dof + 0.1), 0, 1)
    
    # Create multiple blur levels
    blur1 = cv2.GaussianBlur(rgb, (5, 5), 0)
    blur2 = cv2.GaussianBlur(rgb, (15, 15), 0)
    blur3 = cv2.GaussianBlur(rgb, (31, 31), 0)
    
    # Create weights
    w1 = np.clip(1 - blur_amount * 3, 0, 1)
    w2 = np.clip(blur_amount * 3 - 1, 0, 1) * np.clip(2 - blur_amount * 3, 0, 1)
    w3 = np.clip(blur_amount * 3 - 2, 0, 1)
    
    # Expand weights to 3 channels
    w1 = np.stack([w1] * 3, axis=-1)
    w2 = np.stack([w2] * 3, axis=-1)
    w3 = np.stack([w3] * 3, axis=-1)
    
    # Blend
    result = (rgb * w1 + blur1 * (1 - w1 - w2 - w3).clip(0, 1) + 
              blur2 * w2 + blur3 * w3).astype(np.uint8)
    
    return result


def detect_obstacles(depth, max_depth, min_size=500):
    """
    Mendeteksi obstacle berdasarkan depth.
    
    Args:
        depth: Depth map
        max_depth: Maximum depth untuk dianggap obstacle
        min_size: Minimum pixel untuk obstacle valid
        
    Returns:
        Dictionary dengan mask, contours, bboxes
    """
    # Create obstacle mask
    valid = depth > 0
    obstacle_mask = valid & (depth < max_depth)
    
    # Clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    obstacle_mask = cv2.morphologyEx(obstacle_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    obstacle_mask = cv2.morphologyEx(obstacle_mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(obstacle_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by size and compute bboxes
    valid_contours = []
    bboxes = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_size:
            valid_contours.append(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Estimate distance (mean depth in bbox)
            roi_depth = depth[y:y+h, x:x+w]
            valid_roi = roi_depth > 0
            if np.sum(valid_roi) > 0:
                distance = np.median(roi_depth[valid_roi])
            else:
                distance = 0
            
            bboxes.append({
                'bbox': (x, y, w, h),
                'area': area,
                'distance': distance
            })
    
    return {
        'mask': obstacle_mask,
        'contours': valid_contours,
        'obstacles': bboxes
    }


def draw_obstacle_overlay(rgb, obstacles, depth):
    """
    Menggambar overlay obstacle pada gambar.
    
    Args:
        rgb: RGB image
        obstacles: Dictionary dari detect_obstacles()
        depth: Depth map
        
    Returns:
        Image dengan obstacle overlay
    """
    result = rgb.copy()
    
    # Draw contours
    cv2.drawContours(result, obstacles['contours'], -1, (0, 255, 0), 2)
    
    # Draw bboxes dengan distance
    for obs in obstacles['obstacles']:
        x, y, w, h = obs['bbox']
        distance = obs['distance']
        
        # Color based on distance (closer = more red)
        ratio = min(distance / OBSTACLE_THRESHOLD, 1.0)
        color = (0, int(255 * ratio), int(255 * (1 - ratio)))  # BGR
        
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)
        cv2.putText(result, f"{distance:.1f}m", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Warning if obstacle too close
    close_obstacles = [o for o in obstacles['obstacles'] if o['distance'] < 2.0 and o['distance'] > 0]
    if close_obstacles:
        cv2.putText(result, "WARNING: Close obstacle!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    
    return result


def create_depth_edge_image(depth, rgb):
    """
    Membuat edge image berbasis depth (depth discontinuities).
    
    Args:
        depth: Depth map
        rgb: RGB image
        
    Returns:
        Edge image
    """
    # Compute depth gradients
    depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    sobelx = cv2.Sobel(depth_norm, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(depth_norm, cv2.CV_64F, 0, 1, ksize=3)
    
    depth_edges = np.sqrt(sobelx**2 + sobely**2)
    depth_edges = cv2.normalize(depth_edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Threshold
    _, depth_edges_binary = cv2.threshold(depth_edges, 30, 255, cv2.THRESH_BINARY)
    
    return depth_edges, depth_edges_binary


def distance_measurement(depth, points):
    """
    Mengukur jarak ke titik-titik tertentu di gambar.
    
    Args:
        depth: Depth map (dalam meter)
        points: List of (x, y) coordinates
        
    Returns:
        List of distances
    """
    distances = []
    
    for x, y in points:
        if 0 <= y < depth.shape[0] and 0 <= x < depth.shape[1]:
            d = depth[y, x]
            if d > 0:
                distances.append(d)
            else:
                # Sample neighborhood
                h, w = depth.shape
                y1, y2 = max(0, y-5), min(h, y+5)
                x1, x2 = max(0, x-5), min(w, x+5)
                region = depth[y1:y2, x1:x2]
                valid = region > 0
                if np.sum(valid) > 0:
                    distances.append(np.median(region[valid]))
                else:
                    distances.append(0)
        else:
            distances.append(0)
    
    return distances


def depth_to_point_cloud_simple(depth, rgb, focal, cx=None, cy=None):
    """
    Konversi depth map ke point cloud (simplified).
    
    Args:
        depth: Depth map (mm atau m)
        rgb: RGB image untuk warna
        focal: Focal length (pixels)
        cx, cy: Principal point
        
    Returns:
        Tuple (points, colors)
    """
    height, width = depth.shape
    
    if cx is None:
        cx = width / 2
    if cy is None:
        cy = height / 2
    
    # Create coordinate grids
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    
    # Back-project to 3D
    Z = depth.copy()
    X = (u - cx) * Z / focal
    Y = (v - cy) * Z / focal
    
    # Valid points
    valid = Z > 0
    
    points = np.stack([X[valid], Y[valid], Z[valid]], axis=1)
    
    if len(rgb.shape) == 3:
        colors = rgb[valid] / 255.0
        colors = colors[:, ::-1]  # BGR to RGB
    else:
        colors = np.stack([rgb[valid]] * 3, axis=1) / 255.0
    
    return points, colors


def load_data():
    """Memuat depth dan RGB image."""
    # Load depth
    depth = None
    is_normalized = False
    
    if DEPTH_FILE.exists():
        depth = np.load(str(DEPTH_FILE))
        print(f"[OK] Loaded stereo depth from {DEPTH_FILE}")
    elif DEPTH_FILE_MONO.exists():
        depth = np.load(str(DEPTH_FILE_MONO))
        # Normalize monocular depth
        depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8)
        is_normalized = True
        print(f"[OK] Loaded mono depth from {DEPTH_FILE_MONO}")
    
    # Load RGB
    rgb = cv2.imread(str(RGB_IMAGE))
    if rgb is None:
        rgb = cv2.imread(str(RGB_IMAGE_ALT))
    
    return depth, rgb, is_normalized


def create_synthetic_data():
    """Membuat data sintetis untuk demo."""
    height, width = 480, 640
    
    # Create RGB
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Background gradient
    for y in range(height):
        rgb[y, :] = [100 + y//4, 80, 60]
    
    # Objects
    cv2.circle(rgb, (200, 240), 60, (255, 100, 100), -1)  # Blue sphere
    cv2.rectangle(rgb, (400, 180), (550, 350), (100, 255, 100), -1)  # Green box
    cv2.circle(rgb, (150, 380), 40, (100, 100, 255), -1)  # Red sphere
    
    # Create corresponding depth
    depth = np.ones((height, width), dtype=np.float32) * 10.0  # Background at 10m
    
    cv2.circle(depth, (200, 240), 60, 2.0, -1)  # Sphere at 2m
    cv2.rectangle(depth, (400, 180), (550, 350), 4.0, -1)  # Box at 4m
    cv2.circle(depth, (150, 380), 40, 1.5, -1)  # Sphere at 1.5m
    
    return depth, rgb, False


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("DEPTH MAP APPLICATIONS")
    print("="*60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("\n[STEP 1] Memuat data...")
    depth, rgb, is_normalized = load_data()
    
    if depth is None or rgb is None:
        print("[WARNING] Data tidak ditemukan. Membuat data sintetis...")
        depth, rgb, is_normalized = create_synthetic_data()
    
    # Resize if needed
    if rgb.shape[:2] != depth.shape:
        depth = cv2.resize(depth, (rgb.shape[1], rgb.shape[0]))
    
    print(f"  Image size: {rgb.shape[1]}x{rgb.shape[0]}")
    print(f"  Depth type: {'Normalized' if is_normalized else 'Metric (meters)'}")
    
    # Application 1: Depth-based Segmentation
    print("\n[APP 1] Depth-based Segmentation...")
    if is_normalized:
        seg_result = depth_based_segmentation(depth, rgb, 0.3, 0.7, True)
    else:
        seg_result = depth_based_segmentation(depth, rgb, 
                                               FOREGROUND_MIN_DEPTH, 
                                               FOREGROUND_MAX_DEPTH, False)
    
    cv2.imwrite(str(OUTPUT_DIR / "segmentation_foreground.png"), seg_result['foreground'])
    cv2.imwrite(str(OUTPUT_DIR / "segmentation_mask.png"), seg_result['mask'].astype(np.uint8) * 255)
    print(f"  Foreground pixels: {np.sum(seg_result['mask'])}")
    
    # Application 2: Bokeh Effect
    print("\n[APP 2] Bokeh Effect...")
    if is_normalized:
        bokeh = create_bokeh_effect_fast(rgb, depth, 0.5, 0.15, MAX_BLUR_KERNEL, True)
    else:
        bokeh = create_bokeh_effect_fast(rgb, depth, FOCUS_DEPTH, DEPTH_OF_FIELD, MAX_BLUR_KERNEL, False)
    
    cv2.imwrite(str(OUTPUT_DIR / "bokeh_effect.png"), bokeh)
    print(f"  Focus depth: {FOCUS_DEPTH if not is_normalized else 0.5}")
    
    # Application 3: Obstacle Detection
    print("\n[APP 3] Obstacle Detection...")
    if not is_normalized:
        obstacles = detect_obstacles(depth, OBSTACLE_THRESHOLD, MIN_OBSTACLE_SIZE)
        obstacle_vis = draw_obstacle_overlay(rgb, obstacles, depth)
        cv2.imwrite(str(OUTPUT_DIR / "obstacle_detection.png"), obstacle_vis)
        print(f"  Detected obstacles: {len(obstacles['obstacles'])}")
        for i, obs in enumerate(obstacles['obstacles']):
            print(f"    [{i+1}] Distance: {obs['distance']:.2f}m, Size: {obs['area']} px")
    else:
        print("  [SKIP] Obstacle detection requires metric depth")
        obstacle_vis = rgb.copy()
    
    # Application 4: Depth Edges
    print("\n[APP 4] Depth Edge Detection...")
    depth_edges, depth_edges_binary = create_depth_edge_image(depth, rgb)
    cv2.imwrite(str(OUTPUT_DIR / "depth_edges.png"), depth_edges)
    print(f"  Edge pixels: {np.sum(depth_edges_binary > 0)}")
    
    # Application 5: Point Cloud
    print("\n[APP 5] Point Cloud Generation...")
    if not is_normalized:
        points, colors = depth_to_point_cloud_simple(depth * 1000, rgb, FOCAL_LENGTH)  # Convert to mm
    else:
        # For normalized depth, use arbitrary scale
        points, colors = depth_to_point_cloud_simple(depth * 1000, rgb, FOCAL_LENGTH)
    
    print(f"  Total points: {len(points)}")
    
    # Save PLY
    ply_file = OUTPUT_DIR / "point_cloud.ply"
    with open(str(ply_file), 'w') as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
        f.write("end_header\n")
        colors_255 = (colors * 255).astype(np.uint8)
        for i in range(len(points)):
            f.write(f"{points[i,0]:.3f} {points[i,1]:.3f} {points[i,2]:.3f} ")
            f.write(f"{colors_255[i,0]} {colors_255[i,1]} {colors_255[i,2]}\n")
    print(f"  Saved: {ply_file}")
    
    # Create visualization figure
    print("\n[STEP 2] Membuat visualisasi...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Original
    axes[0, 0].imshow(cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')
    
    # Depth
    axes[0, 1].imshow(depth, cmap='plasma')
    axes[0, 1].set_title("Depth Map")
    axes[0, 1].axis('off')
    
    # Segmentation
    axes[0, 2].imshow(cv2.cvtColor(seg_result['foreground'], cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title(f"Foreground Segmentation\n(depth: {FOREGROUND_MIN_DEPTH}-{FOREGROUND_MAX_DEPTH}m)")
    axes[0, 2].axis('off')
    
    # Bokeh
    axes[1, 0].imshow(cv2.cvtColor(bokeh, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"Bokeh Effect\n(focus: {FOCUS_DEPTH}m)")
    axes[1, 0].axis('off')
    
    # Obstacle Detection
    axes[1, 1].imshow(cv2.cvtColor(obstacle_vis, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title("Obstacle Detection")
    axes[1, 1].axis('off')
    
    # Depth Edges
    axes[1, 2].imshow(depth_edges, cmap='gray')
    axes[1, 2].set_title("Depth Discontinuities")
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig(str(OUTPUT_DIR / "applications_overview.png"), dpi=150, bbox_inches='tight')
    
    # Display with OpenCV
    combined1 = np.hstack([rgb, seg_result['foreground'], bokeh])
    combined2 = np.hstack([
        obstacle_vis, 
        cv2.cvtColor(depth_edges, cv2.COLOR_GRAY2BGR),
        cv2.applyColorMap(cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8), 
                         cv2.COLORMAP_PLASMA)
    ])
    combined = np.vstack([combined1, combined2])
    
    # Resize for display
    max_width = 1400
    if combined.shape[1] > max_width:
        scale = max_width / combined.shape[1]
        combined = cv2.resize(combined, None, fx=scale, fy=scale)
    
    cv2.imshow("Depth Map Applications", combined)
    
    plt.show()
    
    print("\nTekan sembarang tombol untuk keluar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n[SUCCESS] Depth applications selesai!")
    print(f"Hasil disimpan di: {OUTPUT_DIR}")
    
    # Print summary
    print("\n" + "="*60)
    print("RINGKASAN APLIKASI DEPTH MAP")
    print("="*60)
    print("1. Segmentation: Memisahkan objek berdasarkan jarak")
    print("2. Bokeh Effect: Blur background untuk efek artistik")
    print("3. Obstacle Detection: Mendeteksi halangan di depan")
    print("4. Depth Edges: Menemukan batas kedalaman")
    print("5. Point Cloud: Representasi 3D dari scene")
    print("\nAplikasi lain yang mungkin:")
    print("- Augmented Reality (AR)")
    print("- Robot Navigation")
    print("- 3D Scanning")
    print("- Volume Measurement")


if __name__ == "__main__":
    main()
