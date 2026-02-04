#!/usr/bin/env python3
"""
=============================================================================
PRAKTIKUM 5: DISPARITY TO DEPTH CONVERSION
=============================================================================
Deskripsi:
    Program untuk mengkonversi disparity map ke depth map (jarak dalam meter).
    Memahami hubungan matematis antara disparity dan depth dalam stereo vision.

Rumus Dasar:
    depth = (baseline × focal_length) / disparity
    
    Dimana:
    - depth: jarak dari kamera ke objek (meter atau mm)
    - baseline: jarak antar pusat kamera (meter atau mm)
    - focal_length: focal length dalam pixel
    - disparity: perbedaan posisi horizontal (pixel)

Hubungan Disparity dan Depth:
    - Disparity tinggi → objek dekat
    - Disparity rendah → objek jauh
    - Disparity = 0 → objek di infinity
    
Koordinat 3D:
    Menggunakan Q matrix dari stereo rectification:
    [X]   [x]
    [Y] = Q × [y]
    [Z]   [d]
    [W]   [1]
    
    Kemudian X = X/W, Y = Y/W, Z = Z/W

Output:
    - Depth map dalam meter
    - Point cloud 3D
    - Visualisasi depth dengan colormap
    - Analisis statistik depth

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
DATA_DIR = Path(__file__).parent / "data"

# Disparity map (dari praktikum sebelumnya)
DISPARITY_FILE = DATA_DIR / "disparity" / "disparity_sgbm_float.npy"

# Gambar kiri untuk referensi warna
LEFT_IMAGE = DATA_DIR / "rectified" / "rectified_left.png"
LEFT_IMAGE_FALLBACK = DATA_DIR / "stereo" / "synthetic_left.png"

# Parameter kamera (dalam mm dan pixel)
# PENTING: Sesuaikan dengan kamera yang digunakan!
BASELINE = 120.0  # Jarak antar kamera dalam mm
FOCAL_LENGTH = 500.0  # Focal length dalam pixel

# Alternatif: gunakan Q matrix dari kalibrasi
# Q matrix menyimpan informasi baseline dan focal length
CALIB_FILE = DATA_DIR / "calibration_results" / "stereo_calibration.yaml"

# Path output
OUTPUT_DIR = Path(__file__).parent / "output" / "output5" / "depth"

# Range depth yang valid (dalam meter)
MIN_DEPTH = 0.1  # 10 cm
MAX_DEPTH = 20.0  # 20 meter

# Colormap untuk visualisasi depth
DEPTH_COLORMAP = cv2.COLORMAP_PLASMA

# Flag untuk point cloud
GENERATE_POINT_CLOUD = True

# =============================================================================
# FUNGSI-FUNGSI
# =============================================================================

def load_disparity():
    """
    Memuat disparity map dari file.
    
    Returns:
        Disparity map (float32) atau None jika gagal
    """
    if DISPARITY_FILE.exists():
        disparity = np.load(str(DISPARITY_FILE))
        print(f"[OK] Loaded disparity from {DISPARITY_FILE}")
        return disparity
    
    # Coba cari file disparity lain
    disp_dir = DATA_DIR / "disparity"
    npy_files = list(disp_dir.glob("*.npy"))
    
    if npy_files:
        disparity = np.load(str(npy_files[0]))
        print(f"[OK] Loaded disparity from {npy_files[0]}")
        return disparity
    
    return None


def load_calibration():
    """
    Memuat parameter kalibrasi dari file YAML.
    
    Returns:
        Dictionary dengan parameter atau None jika gagal
    """
    if not CALIB_FILE.exists():
        return None
    
    try:
        fs = cv2.FileStorage(str(CALIB_FILE), cv2.FILE_STORAGE_READ)
        
        Q_node = fs.getNode('Q')
        if not Q_node.empty():
            Q = Q_node.mat()
        else:
            Q = None
        
        T_node = fs.getNode('T')
        if not T_node.empty():
            T = T_node.mat()
            baseline = abs(T[0, 0])  # Baseline dari translation vector
        else:
            baseline = BASELINE
        
        P1_node = fs.getNode('P1')
        if not P1_node.empty():
            P1 = P1_node.mat()
            focal = P1[0, 0]  # Focal length dari projection matrix
        else:
            focal = FOCAL_LENGTH
        
        fs.release()
        
        return {
            'Q': Q,
            'baseline': baseline,
            'focal': focal
        }
    except Exception as e:
        print(f"[WARNING] Error loading calibration: {e}")
        return None


def disparity_to_depth_simple(disparity, baseline, focal_length):
    """
    Konversi disparity ke depth menggunakan rumus sederhana.
    
    depth = (baseline × focal_length) / disparity
    
    Args:
        disparity: Disparity map (float, dalam pixel)
        baseline: Jarak antar kamera (mm)
        focal_length: Focal length (pixel)
        
    Returns:
        Depth map dalam mm
    """
    # Hindari division by zero
    depth = np.zeros_like(disparity, dtype=np.float32)
    
    valid_mask = disparity > 0
    depth[valid_mask] = (baseline * focal_length) / disparity[valid_mask]
    
    # Set invalid disparity ke 0
    depth[~valid_mask] = 0
    
    return depth


def disparity_to_depth_with_Q(disparity, Q):
    """
    Konversi disparity ke depth menggunakan Q matrix.
    
    Q matrix dari stereoRectify sudah mengandung informasi
    baseline dan focal length.
    
    Args:
        disparity: Disparity map
        Q: 4x4 reprojection matrix
        
    Returns:
        Depth map dalam satuan yang sama dengan calibration (biasanya mm)
    """
    # reprojectImageTo3D menggunakan Q untuk konversi
    points_3d = cv2.reprojectImageTo3D(disparity, Q)
    
    # Extract Z component (depth)
    depth = points_3d[:, :, 2]
    
    # Handle invalid values
    depth[~np.isfinite(depth)] = 0
    depth[depth < 0] = 0
    
    return depth, points_3d


def filter_depth(depth, min_depth, max_depth):
    """
    Filter depth map untuk range yang valid.
    
    Args:
        depth: Depth map (dalam meter atau mm)
        min_depth: Minimum depth
        max_depth: Maximum depth
        
    Returns:
        Filtered depth map
    """
    filtered = depth.copy()
    filtered[(filtered < min_depth) | (filtered > max_depth)] = 0
    return filtered


def create_depth_visualization(depth, min_depth, max_depth, colormap=cv2.COLORMAP_PLASMA):
    """
    Membuat visualisasi depth map dengan colormap.
    
    Args:
        depth: Depth map
        min_depth: Minimum depth untuk normalisasi
        max_depth: Maximum depth untuk normalisasi
        colormap: OpenCV colormap
        
    Returns:
        Colored depth image
    """
    # Normalize ke 0-255
    depth_normalized = depth.copy()
    depth_normalized = np.clip(depth_normalized, min_depth, max_depth)
    depth_normalized = (depth_normalized - min_depth) / (max_depth - min_depth)
    depth_normalized = (255 * depth_normalized).astype(np.uint8)
    
    # Invert sehingga dekat = merah, jauh = biru
    depth_normalized = 255 - depth_normalized
    
    # Apply colormap
    depth_colored = cv2.applyColorMap(depth_normalized, colormap)
    
    # Set invalid areas ke hitam
    depth_colored[depth == 0] = [0, 0, 0]
    
    return depth_colored


def analyze_depth(depth, unit="m"):
    """
    Menganalisis statistik depth map.
    
    Args:
        depth: Depth map
        unit: Satuan ("m" atau "mm")
        
    Returns:
        Dictionary dengan statistik
    """
    valid_mask = depth > 0
    valid_depth = depth[valid_mask]
    
    if len(valid_depth) == 0:
        return {'valid_percentage': 0}
    
    stats = {
        'valid_percentage': (np.sum(valid_mask) / depth.size) * 100,
        'min': float(np.min(valid_depth)),
        'max': float(np.max(valid_depth)),
        'mean': float(np.mean(valid_depth)),
        'median': float(np.median(valid_depth)),
        'std': float(np.std(valid_depth)),
        'unit': unit
    }
    
    return stats


def create_point_cloud(depth, rgb_image, focal_length, cx=None, cy=None):
    """
    Membuat point cloud dari depth map.
    
    Args:
        depth: Depth map (mm)
        rgb_image: RGB image untuk warna
        focal_length: Focal length (pixel)
        cx, cy: Principal point (default = center)
        
    Returns:
        Tuple (points, colors)
    """
    height, width = depth.shape
    
    if cx is None:
        cx = width / 2
    if cy is None:
        cy = height / 2
    
    # Create mesh grid
    u = np.arange(width)
    v = np.arange(height)
    u, v = np.meshgrid(u, v)
    
    # Convert to 3D coordinates
    # X = (u - cx) * Z / f
    # Y = (v - cy) * Z / f
    # Z = depth
    
    Z = depth.copy()
    X = (u - cx) * Z / focal_length
    Y = (v - cy) * Z / focal_length
    
    # Valid points only
    valid = Z > 0
    
    points = np.stack([X[valid], Y[valid], Z[valid]], axis=1)
    
    # Get colors
    if len(rgb_image.shape) == 3:
        colors = rgb_image[valid] / 255.0  # BGR
        colors = colors[:, ::-1]  # Convert to RGB
    else:
        colors = np.stack([rgb_image[valid]] * 3, axis=1) / 255.0
    
    return points, colors


def save_point_cloud_ply(filename, points, colors):
    """
    Menyimpan point cloud ke file PLY.
    
    Args:
        filename: Path file output
        points: Nx3 array of XYZ coordinates
        colors: Nx3 array of RGB colors (0-1)
    """
    # Convert colors to 0-255
    colors_255 = (colors * 255).astype(np.uint8)
    
    # Create PLY file
    with open(filename, 'w') as f:
        # Header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        # Data
        for i in range(len(points)):
            f.write(f"{points[i, 0]:.6f} {points[i, 1]:.6f} {points[i, 2]:.6f} "
                   f"{colors_255[i, 0]} {colors_255[i, 1]} {colors_255[i, 2]}\n")


def visualize_with_open3d(points, colors):
    """
    Visualisasi point cloud dengan Open3D (jika tersedia).
    
    Args:
        points: Nx3 array of XYZ
        colors: Nx3 array of RGB (0-1)
    """
    try:
        import open3d as o3d
        
        # Create point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        
        # Visualize
        print("\n[INFO] Open3D viewer:")
        print("  - Scroll: Zoom")
        print("  - Left drag: Rotate")
        print("  - Right drag: Pan")
        print("  - Q: Quit")
        
        o3d.visualization.draw_geometries([pcd], window_name="Point Cloud")
        
        return True
    except ImportError:
        print("[WARNING] Open3D tidak tersedia untuk visualisasi 3D")
        return False


def create_synthetic_disparity():
    """
    Membuat disparity map sintetis untuk demo.
    """
    height, width = 480, 640
    disparity = np.zeros((height, width), dtype=np.float32)
    
    # Background disparity (far)
    disparity[:] = 10
    
    # Objects at different depths
    cv2.circle(disparity, (200, 200), 60, 40, -1)  # Close object
    cv2.rectangle(disparity, (400, 150), (550, 350), 25, -1)  # Medium distance
    cv2.circle(disparity, (150, 380), 40, 50, -1)  # Very close
    
    # Add some noise
    noise = np.random.randn(height, width).astype(np.float32) * 0.5
    disparity = np.maximum(disparity + noise, 0)
    
    return disparity


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    print("="*60)
    print("DISPARITY TO DEPTH CONVERSION")
    print("="*60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load disparity
    print("\n[STEP 1] Memuat disparity map...")
    disparity = load_disparity()
    
    if disparity is None:
        print("[WARNING] Disparity tidak ditemukan. Membuat disparity sintetis...")
        disparity = create_synthetic_disparity()
    
    print(f"  Shape: {disparity.shape}")
    print(f"  Disparity range: {disparity[disparity > 0].min():.2f} - {disparity.max():.2f} pixels")
    
    # Load calibration
    print("\n[STEP 2] Memuat parameter kalibrasi...")
    calib = load_calibration()
    
    if calib is not None and calib.get('Q') is not None:
        print("  [OK] Menggunakan Q matrix dari kalibrasi")
        Q = calib['Q']
        baseline = calib['baseline']
        focal = calib['focal']
        use_Q = True
    else:
        print("  [INFO] Menggunakan parameter manual")
        baseline = BASELINE
        focal = FOCAL_LENGTH
        use_Q = False
    
    print(f"  Baseline: {baseline:.2f} mm")
    print(f"  Focal length: {focal:.2f} pixels")
    
    # Convert disparity to depth
    print("\n[STEP 3] Mengkonversi disparity ke depth...")
    
    if use_Q:
        depth_mm, points_3d = disparity_to_depth_with_Q(disparity, Q)
    else:
        depth_mm = disparity_to_depth_simple(disparity, baseline, focal)
        points_3d = None
    
    # Convert to meters
    depth_m = depth_mm / 1000.0
    
    # Filter depth
    print("\n[STEP 4] Filter depth range...")
    depth_filtered = filter_depth(depth_m, MIN_DEPTH, MAX_DEPTH)
    
    # Analyze
    print("\n[STEP 5] Menganalisis hasil...")
    stats = analyze_depth(depth_filtered, "m")
    
    print(f"\n  Depth Statistics:")
    print(f"  -----------------")
    print(f"  Valid pixels: {stats['valid_percentage']:.1f}%")
    if stats['valid_percentage'] > 0:
        print(f"  Min depth: {stats['min']:.3f} m")
        print(f"  Max depth: {stats['max']:.3f} m")
        print(f"  Mean depth: {stats['mean']:.3f} m")
        print(f"  Median depth: {stats['median']:.3f} m")
        print(f"  Std depth: {stats['std']:.3f} m")
    
    # Visualize
    print("\n[STEP 6] Membuat visualisasi...")
    depth_vis = create_depth_visualization(depth_filtered, MIN_DEPTH, MAX_DEPTH, DEPTH_COLORMAP)
    
    # Save depth
    cv2.imwrite(str(OUTPUT_DIR / "depth_map.png"), depth_vis)
    np.save(str(OUTPUT_DIR / "depth_meters.npy"), depth_filtered)
    print(f"  Saved: {OUTPUT_DIR / 'depth_map.png'}")
    
    # Load RGB for point cloud
    img_left = cv2.imread(str(LEFT_IMAGE))
    if img_left is None:
        img_left = cv2.imread(str(LEFT_IMAGE_FALLBACK))
    if img_left is None:
        img_left = np.random.randint(100, 200, (disparity.shape[0], disparity.shape[1], 3), dtype=np.uint8)
    
    # Generate point cloud
    if GENERATE_POINT_CLOUD:
        print("\n[STEP 7] Membuat point cloud...")
        points, colors = create_point_cloud(depth_mm, img_left, focal)
        print(f"  Number of points: {len(points)}")
        
        # Save PLY
        ply_file = OUTPUT_DIR / "point_cloud.ply"
        save_point_cloud_ply(str(ply_file), points, colors)
        print(f"  Saved: {ply_file}")
        
        # Visualize with Open3D
        if len(points) > 0:
            visualize_with_open3d(points, colors)
    
    # Display results
    print("\n[STEP 8] Menampilkan hasil...")
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Disparity
    axes[0, 0].imshow(disparity, cmap='turbo')
    axes[0, 0].set_title("Disparity Map (pixels)")
    axes[0, 0].axis('off')
    plt.colorbar(axes[0, 0].images[0], ax=axes[0, 0])
    
    # Depth
    depth_plot = axes[0, 1].imshow(depth_filtered, cmap='plasma', 
                                    vmin=MIN_DEPTH, vmax=MAX_DEPTH)
    axes[0, 1].set_title("Depth Map (meters)")
    axes[0, 1].axis('off')
    plt.colorbar(depth_plot, ax=axes[0, 1], label='Depth (m)')
    
    # Histogram
    valid_depth = depth_filtered[depth_filtered > 0]
    if len(valid_depth) > 0:
        axes[1, 0].hist(valid_depth.flatten(), bins=50, color='blue', alpha=0.7)
        axes[1, 0].axvline(stats['mean'], color='r', linestyle='--', label=f"Mean: {stats['mean']:.2f}m")
        axes[1, 0].axvline(stats['median'], color='g', linestyle='--', label=f"Median: {stats['median']:.2f}m")
        axes[1, 0].set_xlabel("Depth (meters)")
        axes[1, 0].set_ylabel("Frequency")
        axes[1, 0].set_title("Depth Distribution")
        axes[1, 0].legend()
    
    # Disparity vs Depth curve
    disp_range = np.linspace(1, 100, 100)
    depth_curve = (baseline * focal / 1000) / disp_range  # In meters
    axes[1, 1].plot(disp_range, depth_curve, 'b-', linewidth=2)
    axes[1, 1].set_xlabel("Disparity (pixels)")
    axes[1, 1].set_ylabel("Depth (meters)")
    axes[1, 1].set_title(f"Disparity vs Depth\n(baseline={baseline}mm, f={focal}px)")
    axes[1, 1].set_xlim([0, 100])
    axes[1, 1].set_ylim([0, 10])
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(str(OUTPUT_DIR / "depth_analysis.png"), dpi=150, bbox_inches='tight')
    
    # OpenCV display
    combined = np.hstack([img_left, depth_vis])
    cv2.putText(combined, "Left Image", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(combined, "Depth Map", (img_left.shape[1] + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    cv2.imshow("Depth Estimation", combined)
    
    plt.show()
    
    print("\nTekan sembarang tombol untuk keluar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n[SUCCESS] Konversi depth selesai!")
    print(f"Hasil disimpan di: {OUTPUT_DIR}")
    
    # Print formula reminder
    print("\n" + "="*60)
    print("RUMUS DEPTH ESTIMATION")
    print("="*60)
    print("Rumus dasar:")
    print("  depth = (baseline × focal_length) / disparity")
    print(f"\nDengan parameter saat ini:")
    print(f"  depth = ({baseline} × {focal}) / disparity")
    print(f"  depth = {baseline * focal:.0f} / disparity (mm)")
    print("\nContoh:")
    print(f"  disparity = 30 pixels → depth = {baseline * focal / 30 / 1000:.2f} m")
    print(f"  disparity = 50 pixels → depth = {baseline * focal / 50 / 1000:.2f} m")
    print(f"  disparity = 80 pixels → depth = {baseline * focal / 80 / 1000:.2f} m")


if __name__ == "__main__":
    main()
