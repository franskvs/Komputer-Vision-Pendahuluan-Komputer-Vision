"""
Praktikum 13.1: Point Cloud Basics
==================================

Program ini mendemonstrasikan operasi dasar pada point cloud:
1. Membuat point cloud dari data
2. Load dan save berbagai format
3. Visualisasi point cloud
4. Akses atribut (coordinates, colors, normals)

Teori:
------
Point cloud adalah representasi 3D paling fundamental, berupa kumpulan
titik-titik dalam ruang 3D. Setiap titik memiliki koordinat (x, y, z)
dan dapat memiliki atribut tambahan seperti warna RGB atau normal vector.

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent / "data" / "point_clouds"
OUTPUT_DIR = Path(__file__).parent / "output" / "output1"

# Parameter point cloud generation
NUM_POINTS_SPHERE = 10000       # Jumlah titik untuk sphere
NUM_POINTS_CUBE = 8000          # Jumlah titik untuk cube
NUM_POINTS_RANDOM = 5000        # Jumlah titik untuk random cloud

# Visualization settings
POINT_SIZE = 2.0                # Ukuran titik saat visualisasi
BACKGROUND_COLOR = [0.1, 0.1, 0.1]  # Warna background (dark gray)

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat direktori output jika belum ada."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")

def check_open3d():
    """Periksa apakah Open3D tersedia."""
    try:
        import open3d as o3d
        print(f"✓ Open3D version: {o3d.__version__}")
        return True
    except ImportError:
        print("✗ Open3D tidak terinstall!")
        print("  Install dengan: pip install open3d")
        return False

# ============================================================
# FUNGSI PEMBUATAN POINT CLOUD
# ============================================================

def create_sphere_point_cloud(num_points=10000, radius=1.0):
    """
    Membuat point cloud berbentuk sphere menggunakan Fibonacci sampling.
    
    Metode Fibonacci menghasilkan distribusi titik yang hampir uniform
    pada permukaan sphere.
    
    Args:
        num_points: Jumlah titik yang akan digenerate
        radius: Radius sphere
    
    Returns:
        o3d.geometry.PointCloud: Point cloud sphere dengan warna
    """
    import open3d as o3d
    
    print(f"\n[Sphere] Generating {num_points} points dengan Fibonacci sampling...")
    
    # Fibonacci sphere algorithm
    # Golden angle in radians
    phi = np.pi * (3.0 - np.sqrt(5.0))
    
    points = []
    colors = []
    
    for i in range(num_points):
        # y goes from 1 to -1
        y = 1 - (i / float(num_points - 1)) * 2
        
        # Radius at y
        r_at_y = np.sqrt(1 - y * y)
        
        # Golden angle increment
        theta = phi * i
        
        x = np.cos(theta) * r_at_y
        z = np.sin(theta) * r_at_y
        
        points.append([x * radius, y * radius, z * radius])
        
        # Warna berdasarkan posisi (RGB mapping)
        colors.append([
            (x + 1) / 2,    # Red: berdasarkan x
            (y + 1) / 2,    # Green: berdasarkan y
            (z + 1) / 2     # Blue: berdasarkan z
        ])
    
    # Buat point cloud Open3D
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.array(points))
    pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
    
    print(f"  ✓ Sphere point cloud dibuat: {len(pcd.points)} points")
    
    return pcd

def create_cube_point_cloud(num_points=8000, size=2.0):
    """
    Membuat point cloud berbentuk cube dengan sampling pada permukaan.
    
    Args:
        num_points: Jumlah titik total
        size: Ukuran sisi cube
    
    Returns:
        o3d.geometry.PointCloud: Point cloud cube
    """
    import open3d as o3d
    
    print(f"\n[Cube] Generating {num_points} points pada permukaan cube...")
    
    half = size / 2
    points_per_face = num_points // 6
    
    all_points = []
    all_colors = []
    
    # Definisi 6 faces dengan warna berbeda
    faces = [
        # (axis, value, color)
        (0, half, [1, 0, 0]),     # Right face (Red)
        (0, -half, [0.5, 0, 0]),  # Left face (Dark Red)
        (1, half, [0, 1, 0]),     # Top face (Green)
        (1, -half, [0, 0.5, 0]),  # Bottom face (Dark Green)
        (2, half, [0, 0, 1]),     # Front face (Blue)
        (2, -half, [0, 0, 0.5])   # Back face (Dark Blue)
    ]
    
    for axis, value, color in faces:
        for _ in range(points_per_face):
            point = [0, 0, 0]
            point[axis] = value
            
            # Random pada 2 axis lainnya
            other_axes = [i for i in range(3) if i != axis]
            for ax in other_axes:
                point[ax] = np.random.uniform(-half, half)
            
            all_points.append(point)
            all_colors.append(color)
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.array(all_points))
    pcd.colors = o3d.utility.Vector3dVector(np.array(all_colors))
    
    print(f"  ✓ Cube point cloud dibuat: {len(pcd.points)} points")
    
    return pcd

def create_random_point_cloud(num_points=5000, bounds=(-1, 1)):
    """
    Membuat point cloud dengan distribusi random.
    
    Args:
        num_points: Jumlah titik
        bounds: Batas koordinat (min, max)
    
    Returns:
        o3d.geometry.PointCloud: Random point cloud
    """
    import open3d as o3d
    
    print(f"\n[Random] Generating {num_points} random points...")
    
    # Random points dalam bounding box
    points = np.random.uniform(bounds[0], bounds[1], (num_points, 3))
    
    # Warna berdasarkan jarak dari origin
    distances = np.linalg.norm(points, axis=1)
    distances_norm = (distances - distances.min()) / (distances.max() - distances.min())
    
    # Colormap: biru (dekat) -> merah (jauh)
    colors = np.zeros((num_points, 3))
    colors[:, 0] = distances_norm       # Red
    colors[:, 2] = 1 - distances_norm   # Blue
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    print(f"  ✓ Random point cloud dibuat: {len(pcd.points)} points")
    
    return pcd

# ============================================================
# FUNGSI I/O
# ============================================================

def save_point_cloud(pcd, filepath, format_type='ply'):
    """
    Menyimpan point cloud ke file.
    
    Args:
        pcd: Open3D PointCloud object
        filepath: Path output
        format_type: 'ply', 'pcd', 'xyz', 'pts'
    """
    import open3d as o3d
    
    filepath = Path(filepath)
    
    print(f"\n[Save] Menyimpan point cloud ke {filepath}...")
    
    success = o3d.io.write_point_cloud(str(filepath), pcd)
    
    if success:
        size_kb = filepath.stat().st_size / 1024
        print(f"  ✓ Berhasil! Ukuran: {size_kb:.1f} KB")
    else:
        print(f"  ✗ Gagal menyimpan!")
    
    return success

def load_point_cloud(filepath):
    """
    Memuat point cloud dari file.
    
    Args:
        filepath: Path ke file point cloud
    
    Returns:
        o3d.geometry.PointCloud atau None jika gagal
    """
    import open3d as o3d
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"  ✗ File tidak ditemukan: {filepath}")
        return None
    
    print(f"\n[Load] Memuat point cloud dari {filepath}...")
    
    start_time = time.time()
    pcd = o3d.io.read_point_cloud(str(filepath))
    load_time = (time.time() - start_time) * 1000
    
    print(f"  ✓ Berhasil! {len(pcd.points)} points, waktu: {load_time:.2f} ms")
    
    return pcd

def convert_format(input_path, output_path):
    """
    Konversi format point cloud.
    
    Args:
        input_path: Path file input
        output_path: Path file output (format ditentukan dari ekstensi)
    """
    pcd = load_point_cloud(input_path)
    if pcd is not None:
        save_point_cloud(pcd, output_path)

# ============================================================
# FUNGSI ANALISIS
# ============================================================

def analyze_point_cloud(pcd, name="Point Cloud"):
    """
    Menganalisis dan menampilkan informasi point cloud.
    
    Args:
        pcd: Open3D PointCloud object
        name: Nama untuk display
    """
    import open3d as o3d
    
    print(f"\n{'='*50}")
    print(f"ANALISIS: {name}")
    print(f"{'='*50}")
    
    # Basic info
    num_points = len(pcd.points)
    print(f"Jumlah titik: {num_points:,}")
    
    # Bounding box
    if num_points > 0:
        points = np.asarray(pcd.points)
        
        min_bound = points.min(axis=0)
        max_bound = points.max(axis=0)
        
        print(f"\nBounding Box:")
        print(f"  Min: ({min_bound[0]:.3f}, {min_bound[1]:.3f}, {min_bound[2]:.3f})")
        print(f"  Max: ({max_bound[0]:.3f}, {max_bound[1]:.3f}, {max_bound[2]:.3f})")
        
        dimensions = max_bound - min_bound
        print(f"  Dimensions: ({dimensions[0]:.3f}, {dimensions[1]:.3f}, {dimensions[2]:.3f})")
        
        # Center
        center = (min_bound + max_bound) / 2
        print(f"  Center: ({center[0]:.3f}, {center[1]:.3f}, {center[2]:.3f})")
    
    # Colors
    has_colors = pcd.has_colors()
    print(f"\nWarna: {'Ya' if has_colors else 'Tidak'}")
    if has_colors:
        colors = np.asarray(pcd.colors)
        print(f"  Range: [{colors.min():.2f}, {colors.max():.2f}]")
    
    # Normals
    has_normals = pcd.has_normals()
    print(f"Normal: {'Ya' if has_normals else 'Tidak'}")
    
    # Memory estimate
    memory_mb = (num_points * 3 * 8) / (1024 * 1024)  # 3 coords, 8 bytes each
    if has_colors:
        memory_mb += (num_points * 3 * 8) / (1024 * 1024)
    if has_normals:
        memory_mb += (num_points * 3 * 8) / (1024 * 1024)
    
    print(f"\nEstimasi memori: {memory_mb:.2f} MB")

def compute_point_cloud_statistics(pcd):
    """
    Menghitung statistik detail point cloud.
    
    Args:
        pcd: Open3D PointCloud object
    
    Returns:
        dict: Dictionary berisi statistik
    """
    points = np.asarray(pcd.points)
    
    stats = {
        'num_points': len(points),
        'mean': points.mean(axis=0),
        'std': points.std(axis=0),
        'min': points.min(axis=0),
        'max': points.max(axis=0),
        'centroid': points.mean(axis=0)
    }
    
    # Compute nearest neighbor distances (sample untuk efisiensi)
    if len(points) > 100:
        sample_idx = np.random.choice(len(points), min(1000, len(points)), replace=False)
        sample_points = points[sample_idx]
        
        # Pairwise distances
        from scipy.spatial import distance
        dist_matrix = distance.cdist(sample_points[:100], sample_points)
        np.fill_diagonal(dist_matrix[:100, :100], np.inf)
        
        nn_distances = dist_matrix.min(axis=1)
        stats['mean_nn_distance'] = nn_distances.mean()
        stats['std_nn_distance'] = nn_distances.std()
    
    return stats

# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_point_cloud(pcd, window_name="Point Cloud Viewer", point_size=2.0):
    """
    Visualisasi interaktif point cloud dengan Matplotlib (Wayland-compatible).
    
    Args:
        pcd: Open3D PointCloud object atau list of PointClouds
        window_name: Judul window
        point_size: Ukuran titik
    """
    print(f"\n[Visualisasi] Membuka viewer dengan Matplotlib...")
    print("  Kontrol:")
    print("  - Klik dan drag: Rotate")
    print("  - Scroll: Zoom")
    print("  - Close window: Keluar")
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot point clouds
    if isinstance(pcd, list):
        colors_list = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
        for idx, p in enumerate(pcd):
            points = np.asarray(p.points)
            color = colors_list[idx % len(colors_list)]
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                      c=color, s=point_size, alpha=0.6, label=f"Cloud {idx}")
        ax.legend()
    else:
        points = np.asarray(pcd.points)
        if pcd.has_colors():
            colors = np.asarray(pcd.colors)
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                      c=colors, s=point_size, alpha=0.6)
        else:
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                      c='blue', s=point_size, alpha=0.6)
    
    # Labels dan title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(window_name, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Set background
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#2a2a2a')
    
    plt.tight_layout()
    plt.show()
    print("  ✓ Visualization closed")

def visualize_multiple_point_clouds(point_clouds, names=None, colors=None):
    """
    Visualisasi multiple point clouds dengan warna berbeda (Matplotlib).
    
    Args:
        point_clouds: List of PointCloud objects
        names: List of names for each cloud
        colors: List of colors for each cloud
    """
    if colors is None:
        # Default colors untuk matplotlib
        default_colors = [
            'red', 'green', 'blue', 'yellow', 
            'cyan', 'magenta', 'orange', 'purple'
        ]
        colors = default_colors[:len(point_clouds)]
    
    print(f"\n[Multi-View] Menampilkan {len(point_clouds)} point clouds...")
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot setiap point cloud
    for idx, pcd in enumerate(point_clouds):
        points = np.asarray(pcd.points)
        label = names[idx] if names and idx < len(names) else f"Cloud {idx}"
        
        if pcd.has_colors():
            pc_colors = np.asarray(pcd.colors)
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                      c=pc_colors, s=2, alpha=0.6, label=label)
        else:
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                      c=colors[idx % len(colors)], s=2, alpha=0.6, label=label)
    
    # Labels dan title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("Multiple Point Clouds", fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Set background
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#2a2a2a')
    
    plt.tight_layout()
    plt.show()
    print("  ✓ Visualization closed")

# ============================================================
# DEMONSTRASI UTAMA
# ============================================================

def demo_create_and_save():
    """Demo pembuatan dan penyimpanan point cloud."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: Membuat dan Menyimpan Point Cloud")
    print("="*60)
    
    # Buat berbagai jenis point cloud
    sphere_pcd = create_sphere_point_cloud(NUM_POINTS_SPHERE)
    cube_pcd = create_cube_point_cloud(NUM_POINTS_CUBE)
    random_pcd = create_random_point_cloud(NUM_POINTS_RANDOM)
    
    # Simpan dalam berbagai format
    save_point_cloud(sphere_pcd, OUTPUT_DIR / "sphere.ply")
    save_point_cloud(sphere_pcd, OUTPUT_DIR / "sphere.pcd")
    save_point_cloud(cube_pcd, OUTPUT_DIR / "cube.ply")
    save_point_cloud(random_pcd, OUTPUT_DIR / "random.xyz")
    
    return sphere_pcd, cube_pcd, random_pcd

def demo_load_and_analyze():
    """Demo loading dan analisis point cloud."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Load dan Analisis Point Cloud")
    print("="*60)
    
    # Coba load dari data yang sudah ada
    test_files = [
        DATA_DIR / "sphere.ply",
        OUTPUT_DIR / "sphere.ply",
        OUTPUT_DIR / "cube.ply"
    ]
    
    for filepath in test_files:
        if filepath.exists():
            pcd = load_point_cloud(filepath)
            if pcd is not None:
                analyze_point_cloud(pcd, filepath.name)
                return pcd
    
    # Jika tidak ada file, buat baru
    print("\n[Info] Tidak ada file ditemukan, membuat point cloud baru...")
    pcd = create_sphere_point_cloud(5000)
    analyze_point_cloud(pcd, "Generated Sphere")
    return pcd

def demo_visualization():
    """Demo visualisasi point cloud."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Visualisasi Point Cloud")
    print("="*60)
    
    # Buat point clouds
    sphere = create_sphere_point_cloud(5000, radius=0.5)
    cube = create_cube_point_cloud(4000, size=1.5)
    
    # Geser cube supaya tidak overlap
    cube_points = np.asarray(cube.points)
    cube_points[:, 0] += 2  # Geser ke kanan
    cube.points = o3d.utility.Vector3dVector(cube_points)
    
    print("\n[Demo] Menampilkan sphere dan cube bersamaan...")
    visualize_multiple_point_clouds(
        [sphere, cube], 
        names=["Sphere", "Cube"]
    )

def demo_point_cloud_operations():
    """Demo operasi dasar pada point cloud."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: Operasi Point Cloud")
    print("="*60)
    
    # Buat point cloud
    pcd = create_sphere_point_cloud(10000)
    
    # 1. Akses koordinat
    print("\n1. Akses Koordinat:")
    points = np.asarray(pcd.points)
    print(f"   Shape: {points.shape}")
    print(f"   5 titik pertama:\n{points[:5]}")
    
    # 2. Akses warna
    print("\n2. Akses Warna:")
    colors = np.asarray(pcd.colors)
    print(f"   Shape: {colors.shape}")
    print(f"   5 warna pertama:\n{colors[:5]}")
    
    # 3. Transformasi
    print("\n3. Transformasi Point Cloud:")
    
    # Translasi
    pcd_translated = o3d.geometry.PointCloud(pcd)
    pcd_translated.translate([1, 0, 0])
    print("   ✓ Translasi: [1, 0, 0]")
    
    # Rotasi
    pcd_rotated = o3d.geometry.PointCloud(pcd)
    R = pcd_rotated.get_rotation_matrix_from_xyz([0, np.pi/4, 0])
    pcd_rotated.rotate(R, center=[0, 0, 0])
    print("   ✓ Rotasi: 45° pada sumbu Y")
    
    # Scaling
    pcd_scaled = o3d.geometry.PointCloud(pcd)
    pcd_scaled.scale(1.5, center=[0, 0, 0])
    print("   ✓ Scaling: 1.5x")
    
    # 4. Paint uniform color
    print("\n4. Paint Uniform Color:")
    pcd_red = o3d.geometry.PointCloud(pcd)
    pcd_red.paint_uniform_color([1, 0, 0])
    print("   ✓ Semua titik diwarnai merah")
    
    # 5. Gabungkan point clouds
    print("\n5. Gabungkan Point Clouds:")
    pcd_combined = pcd + pcd_translated
    print(f"   Original: {len(pcd.points)} points")
    print(f"   Translated: {len(pcd_translated.points)} points")
    print(f"   Combined: {len(pcd_combined.points)} points")
    
    return pcd, pcd_translated, pcd_rotated, pcd_scaled

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    
    print("="*60)
    print("PRAKTIKUM 13.1: POINT CLOUD BASICS")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    sphere, cube, random_cloud = demo_create_and_save()
    
    demo_load_and_analyze()
    
    demo_point_cloud_operations()
    
    # Visualisasi (optional - membutuhkan display)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi interaktif? (y/n): ").strip().lower()
        if response == 'y':
            demo_visualization()
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)
    print(f"\nFile output tersimpan di: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
