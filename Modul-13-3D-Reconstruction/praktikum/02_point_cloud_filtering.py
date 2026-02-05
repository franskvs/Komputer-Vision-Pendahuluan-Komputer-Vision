"""
Praktikum 13.2: Point Cloud Filtering
=====================================

Program ini mendemonstrasikan teknik filtering pada point cloud:
1. Voxel Grid Downsampling
2. Statistical Outlier Removal
3. Radius Outlier Removal
4. Pass Through Filter

Teori:
------
Filtering adalah tahap preprocessing penting untuk:
- Mengurangi jumlah titik (downsampling) untuk efisiensi komputasi
- Menghapus noise dan outlier
- Menyiapkan data untuk proses selanjutnya (reconstruction)

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
DATA_DIR = Path(__file__).parent / "data" / "point_clouds"
OUTPUT_DIR = Path(__file__).parent / "output" / "output2"

# Parameter Voxel Downsampling
VOXEL_SIZES = [0.01, 0.02, 0.05, 0.1]  # Ukuran voxel untuk perbandingan

# Parameter Statistical Outlier Removal
SOR_NB_NEIGHBORS = 20           # Jumlah tetangga untuk analisis
SOR_STD_RATIO = 2.0             # Threshold standard deviation

# Parameter Radius Outlier Removal
ROR_NB_POINTS = 16              # Minimum neighbors dalam radius
ROR_RADIUS = 0.05               # Radius pencarian

# Parameter untuk generate data noisy
NOISE_LEVEL = 0.02              # Standard deviation noise
NUM_OUTLIERS = 200              # Jumlah outlier yang ditambahkan

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat direktori output."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")

def check_open3d():
    """Periksa ketersediaan Open3D."""
    try:
        import open3d as o3d
        print(f"✓ Open3D version: {o3d.__version__}")
        return True
    except ImportError:
        print("✗ Open3D tidak terinstall!")
        print("  Install dengan: pip install open3d")
        return False

def create_noisy_point_cloud(num_points=50000, noise_std=0.02, num_outliers=200):
    """
    Membuat point cloud sphere dengan noise dan outlier untuk testing.
    
    Args:
        num_points: Jumlah titik
        noise_std: Standard deviation noise
        num_outliers: Jumlah outlier
    
    Returns:
        clean_pcd: Point cloud bersih (ground truth)
        noisy_pcd: Point cloud dengan noise dan outlier
    """
    import open3d as o3d
    
    print(f"\n[Generate] Membuat noisy point cloud...")
    print(f"  - Points: {num_points}")
    print(f"  - Noise std: {noise_std}")
    print(f"  - Outliers: {num_outliers}")
    
    # Generate clean sphere
    phi = np.pi * (3.0 - np.sqrt(5.0))  # Golden angle
    points = []
    
    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2
        r_at_y = np.sqrt(1 - y * y)
        theta = phi * i
        
        x = np.cos(theta) * r_at_y
        z = np.sin(theta) * r_at_y
        
        points.append([x, y, z])
    
    points = np.array(points)
    
    # Buat clean point cloud
    clean_pcd = o3d.geometry.PointCloud()
    clean_pcd.points = o3d.utility.Vector3dVector(points)
    clean_pcd.paint_uniform_color([0, 0.8, 0])  # Green
    
    # Tambahkan noise
    noise = np.random.normal(0, noise_std, points.shape)
    noisy_points = points + noise
    
    # Tambahkan outliers (titik random di luar sphere)
    outliers = np.random.uniform(-2, 2, (num_outliers, 3))
    
    # Gabungkan
    all_points = np.vstack([noisy_points, outliers])
    
    # Buat noisy point cloud
    noisy_pcd = o3d.geometry.PointCloud()
    noisy_pcd.points = o3d.utility.Vector3dVector(all_points)
    
    # Warna: hijau untuk points, merah untuk outliers
    colors = np.zeros((len(all_points), 3))
    colors[:num_points] = [0, 0.8, 0]      # Green for regular points
    colors[num_points:] = [1, 0, 0]        # Red for outliers
    noisy_pcd.colors = o3d.utility.Vector3dVector(colors)
    
    print(f"  ✓ Clean: {len(clean_pcd.points)} points")
    print(f"  ✓ Noisy: {len(noisy_pcd.points)} points (including outliers)")
    
    return clean_pcd, noisy_pcd

# ============================================================
# FUNGSI FILTERING
# ============================================================

def voxel_downsampling(pcd, voxel_size):
    """
    Melakukan voxel grid downsampling.
    
    Konsep:
    - Membagi ruang 3D menjadi grid voxel dengan ukuran tertentu
    - Semua titik dalam satu voxel direpresentasikan oleh centroid-nya
    - Menghasilkan point cloud dengan densitas uniform
    
    Args:
        pcd: Input point cloud
        voxel_size: Ukuran voxel (sisi kubus)
    
    Returns:
        downsampled_pcd: Point cloud hasil downsampling
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    original_count = len(pcd.points)
    
    start_time = time.time()
    downsampled = pcd.voxel_down_sample(voxel_size)
    elapsed_time = (time.time() - start_time) * 1000
    
    new_count = len(downsampled.points)
    reduction = (1 - new_count / original_count) * 100
    
    stats = {
        'voxel_size': voxel_size,
        'original_count': original_count,
        'new_count': new_count,
        'reduction_percent': reduction,
        'time_ms': elapsed_time
    }
    
    return downsampled, stats

def statistical_outlier_removal(pcd, nb_neighbors=20, std_ratio=2.0):
    """
    Menghapus outlier berdasarkan statistik jarak ke tetangga.
    
    Konsep:
    - Untuk setiap titik, hitung rata-rata jarak ke k tetangga terdekat
    - Hitung mean dan std dari semua jarak rata-rata
    - Hapus titik yang jaraknya > mean + std_ratio * std
    
    Args:
        pcd: Input point cloud
        nb_neighbors: Jumlah tetangga untuk analisis
        std_ratio: Threshold dalam satuan standard deviation
    
    Returns:
        filtered_pcd: Point cloud hasil filtering
        inlier_indices: Index titik yang dipertahankan
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    original_count = len(pcd.points)
    
    start_time = time.time()
    filtered, inlier_indices = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio
    )
    elapsed_time = (time.time() - start_time) * 1000
    
    removed = original_count - len(filtered.points)
    
    stats = {
        'nb_neighbors': nb_neighbors,
        'std_ratio': std_ratio,
        'original_count': original_count,
        'removed_count': removed,
        'remaining_count': len(filtered.points),
        'time_ms': elapsed_time
    }
    
    return filtered, inlier_indices, stats

def radius_outlier_removal(pcd, nb_points=16, radius=0.05):
    """
    Menghapus outlier berdasarkan jumlah tetangga dalam radius.
    
    Konsep:
    - Untuk setiap titik, hitung jumlah tetangga dalam radius tertentu
    - Hapus titik yang memiliki tetangga < threshold
    
    Args:
        pcd: Input point cloud
        nb_points: Minimum tetangga dalam radius
        radius: Radius pencarian
    
    Returns:
        filtered_pcd: Point cloud hasil filtering
        inlier_indices: Index titik yang dipertahankan
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    original_count = len(pcd.points)
    
    start_time = time.time()
    filtered, inlier_indices = pcd.remove_radius_outlier(
        nb_points=nb_points,
        radius=radius
    )
    elapsed_time = (time.time() - start_time) * 1000
    
    removed = original_count - len(filtered.points)
    
    stats = {
        'nb_points': nb_points,
        'radius': radius,
        'original_count': original_count,
        'removed_count': removed,
        'remaining_count': len(filtered.points),
        'time_ms': elapsed_time
    }
    
    return filtered, inlier_indices, stats

def pass_through_filter(pcd, axis='z', min_val=-np.inf, max_val=np.inf):
    """
    Filter titik berdasarkan range nilai pada axis tertentu.
    
    Args:
        pcd: Input point cloud
        axis: 'x', 'y', atau 'z'
        min_val: Nilai minimum
        max_val: Nilai maksimum
    
    Returns:
        filtered_pcd: Point cloud hasil filtering
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    points = np.asarray(pcd.points)
    original_count = len(points)
    
    axis_idx = {'x': 0, 'y': 1, 'z': 2}[axis.lower()]
    
    start_time = time.time()
    
    # Create mask
    mask = (points[:, axis_idx] >= min_val) & (points[:, axis_idx] <= max_val)
    
    # Filter points
    filtered_points = points[mask]
    
    filtered = o3d.geometry.PointCloud()
    filtered.points = o3d.utility.Vector3dVector(filtered_points)
    
    # Copy colors if available
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)
        filtered.colors = o3d.utility.Vector3dVector(colors[mask])
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'axis': axis,
        'min_val': min_val,
        'max_val': max_val,
        'original_count': original_count,
        'remaining_count': len(filtered_points),
        'time_ms': elapsed_time
    }
    
    return filtered, stats

# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_filtering_result(original, filtered, title="Filtering Result"):
    """
    Visualisasi perbandingan sebelum dan sesudah filtering.
    
    Args:
        original: Point cloud original
        filtered: Point cloud hasil filtering
        title: Judul window
    """
    import open3d as o3d
    
    # Buat copy untuk visualisasi
    original_vis = o3d.geometry.PointCloud(original)
    filtered_vis = o3d.geometry.PointCloud(filtered)
    
    # Geser filtered ke samping
    filtered_vis.translate([2.5, 0, 0])
    
    # Beri warna berbeda
    original_vis.paint_uniform_color([1, 0.7, 0])    # Orange
    filtered_vis.paint_uniform_color([0, 0.8, 0.3])  # Green
    
    print(f"\n[Visualisasi] {title}")
    print(f"  Kiri (Orange): Original ({len(original.points)} points)")
    print(f"  Kanan (Green): Filtered ({len(filtered.points)} points)")
    
    # Visualize
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=title, width=1280, height=720)
    
    vis.add_geometry(original_vis)
    vis.add_geometry(filtered_vis)
    
    # Add coordinate frame
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3)
    vis.add_geometry(coord)
    
    opt = vis.get_render_option()
    opt.point_size = 2.0
    opt.background_color = np.array([0.1, 0.1, 0.1])
    
    vis.run()
    vis.destroy_window()

def visualize_outliers(pcd, inlier_indices, title="Outlier Detection"):
    """
    Visualisasi inliers dan outliers dengan warna berbeda.
    
    Args:
        pcd: Original point cloud
        inlier_indices: Indices of inliers
        title: Window title
    """
    import open3d as o3d
    
    points = np.asarray(pcd.points)
    
    # Create colors array
    colors = np.zeros((len(points), 3))
    colors[inlier_indices] = [0, 0.8, 0]  # Green for inliers
    
    # Set outliers to red
    outlier_mask = np.ones(len(points), dtype=bool)
    outlier_mask[inlier_indices] = False
    colors[outlier_mask] = [1, 0, 0]  # Red for outliers
    
    num_outliers = np.sum(outlier_mask)
    
    pcd_vis = o3d.geometry.PointCloud()
    pcd_vis.points = o3d.utility.Vector3dVector(points)
    pcd_vis.colors = o3d.utility.Vector3dVector(colors)
    
    print(f"\n[Visualisasi] {title}")
    print(f"  Green: Inliers ({len(inlier_indices)} points)")
    print(f"  Red: Outliers ({num_outliers} points)")
    
    o3d.visualization.draw_geometries(
        [pcd_vis],
        window_name=title,
        width=1024,
        height=768
    )

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_voxel_downsampling():
    """Demo voxel grid downsampling dengan berbagai ukuran."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: Voxel Grid Downsampling")
    print("="*60)
    
    # Buat point cloud
    _, noisy_pcd = create_noisy_point_cloud(50000, NOISE_LEVEL, NUM_OUTLIERS)
    
    print("\n" + "-"*40)
    print("Perbandingan berbagai voxel size:")
    print("-"*40)
    print(f"{'Voxel Size':<12} {'Original':<12} {'Result':<12} {'Reduksi':<12} {'Waktu (ms)':<12}")
    print("-"*60)
    
    results = []
    
    for voxel_size in VOXEL_SIZES:
        downsampled, stats = voxel_downsampling(noisy_pcd, voxel_size)
        results.append((voxel_size, downsampled))
        
        print(f"{stats['voxel_size']:<12.3f} "
              f"{stats['original_count']:<12} "
              f"{stats['new_count']:<12} "
              f"{stats['reduction_percent']:<12.1f}% "
              f"{stats['time_ms']:<12.2f}")
    
    # Simpan hasil
    for voxel_size, pcd in results:
        output_path = OUTPUT_DIR / f"downsampled_v{voxel_size:.3f}.ply"
        o3d.io.write_point_cloud(str(output_path), pcd)
    
    return results

def demo_statistical_outlier_removal():
    """Demo statistical outlier removal."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Statistical Outlier Removal")
    print("="*60)
    
    # Buat noisy point cloud
    clean_pcd, noisy_pcd = create_noisy_point_cloud(30000, 0.02, 300)
    
    print("\n" + "-"*40)
    print("Perbandingan parameter:")
    print("-"*40)
    print(f"{'Neighbors':<12} {'Std Ratio':<12} {'Removed':<12} {'Remaining':<12} {'Time (ms)':<12}")
    print("-"*60)
    
    # Test berbagai parameter
    params = [
        (10, 1.0),
        (20, 2.0),
        (30, 2.0),
        (20, 3.0),
    ]
    
    for nb_neighbors, std_ratio in params:
        filtered, indices, stats = statistical_outlier_removal(
            noisy_pcd, nb_neighbors, std_ratio
        )
        
        print(f"{stats['nb_neighbors']:<12} "
              f"{stats['std_ratio']:<12.1f} "
              f"{stats['removed_count']:<12} "
              f"{stats['remaining_count']:<12} "
              f"{stats['time_ms']:<12.2f}")
    
    # Gunakan parameter default
    filtered, inlier_indices, _ = statistical_outlier_removal(
        noisy_pcd, SOR_NB_NEIGHBORS, SOR_STD_RATIO
    )
    
    # Simpan hasil
    o3d.io.write_point_cloud(str(OUTPUT_DIR / "sor_filtered.ply"), filtered)
    
    return noisy_pcd, filtered, inlier_indices

def demo_radius_outlier_removal():
    """Demo radius outlier removal."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Radius Outlier Removal")
    print("="*60)
    
    # Buat noisy point cloud
    clean_pcd, noisy_pcd = create_noisy_point_cloud(30000, 0.02, 300)
    
    print("\n" + "-"*40)
    print("Perbandingan parameter:")
    print("-"*40)
    print(f"{'Nb Points':<12} {'Radius':<12} {'Removed':<12} {'Remaining':<12} {'Time (ms)':<12}")
    print("-"*60)
    
    # Test berbagai parameter
    params = [
        (10, 0.03),
        (16, 0.05),
        (20, 0.05),
        (16, 0.1),
    ]
    
    for nb_points, radius in params:
        filtered, indices, stats = radius_outlier_removal(
            noisy_pcd, nb_points, radius
        )
        
        print(f"{stats['nb_points']:<12} "
              f"{stats['radius']:<12.3f} "
              f"{stats['removed_count']:<12} "
              f"{stats['remaining_count']:<12} "
              f"{stats['time_ms']:<12.2f}")
    
    # Gunakan parameter default
    filtered, inlier_indices, _ = radius_outlier_removal(
        noisy_pcd, ROR_NB_POINTS, ROR_RADIUS
    )
    
    # Simpan hasil
    o3d.io.write_point_cloud(str(OUTPUT_DIR / "ror_filtered.ply"), filtered)
    
    return noisy_pcd, filtered, inlier_indices

def demo_combined_filtering():
    """Demo kombinasi beberapa teknik filtering."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: Combined Filtering Pipeline")
    print("="*60)
    
    # Buat noisy point cloud
    _, noisy_pcd = create_noisy_point_cloud(50000, 0.03, 500)
    
    print(f"\nInput: {len(noisy_pcd.points)} points")
    
    # Step 1: Voxel downsampling
    print("\nStep 1: Voxel Downsampling (voxel_size=0.02)")
    pcd_step1, stats1 = voxel_downsampling(noisy_pcd, 0.02)
    print(f"  Result: {len(pcd_step1.points)} points ({stats1['reduction_percent']:.1f}% reduction)")
    
    # Step 2: Statistical outlier removal
    print("\nStep 2: Statistical Outlier Removal")
    pcd_step2, _, stats2 = statistical_outlier_removal(pcd_step1, 20, 2.0)
    print(f"  Result: {len(pcd_step2.points)} points ({stats2['removed_count']} removed)")
    
    # Step 3: Radius outlier removal
    print("\nStep 3: Radius Outlier Removal")
    pcd_step3, _, stats3 = radius_outlier_removal(pcd_step2, 10, 0.05)
    print(f"  Result: {len(pcd_step3.points)} points ({stats3['removed_count']} removed)")
    
    # Summary
    total_reduction = (1 - len(pcd_step3.points) / len(noisy_pcd.points)) * 100
    print(f"\n" + "-"*40)
    print(f"SUMMARY:")
    print(f"  Input:  {len(noisy_pcd.points):,} points")
    print(f"  Output: {len(pcd_step3.points):,} points")
    print(f"  Total reduction: {total_reduction:.1f}%")
    
    # Save result
    o3d.io.write_point_cloud(str(OUTPUT_DIR / "combined_filtered.ply"), pcd_step3)
    
    return noisy_pcd, pcd_step3

def demo_pass_through_filter():
    """Demo pass-through filter."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 5: Pass-Through Filter")
    print("="*60)
    
    # Buat point cloud
    _, pcd = create_noisy_point_cloud(30000, 0.01, 0)
    
    print(f"\nInput: {len(pcd.points)} points")
    
    # Filter pada Z axis
    print("\nFiltering Z axis: [-0.5, 0.5]")
    filtered_z, stats_z = pass_through_filter(pcd, 'z', -0.5, 0.5)
    print(f"  Result: {stats_z['remaining_count']} points")
    
    # Filter pada Y axis
    print("\nFiltering Y axis: [0, 1]")
    filtered_y, stats_y = pass_through_filter(pcd, 'y', 0, 1)
    print(f"  Result: {stats_y['remaining_count']} points")
    
    # Combined filter
    print("\nCombined: Z[-0.5, 0.5] then Y[0, 1]")
    filtered_combined, _ = pass_through_filter(filtered_z, 'y', 0, 1)
    print(f"  Result: {len(filtered_combined.points)} points")
    
    # Save
    o3d.io.write_point_cloud(str(OUTPUT_DIR / "passthrough_filtered.ply"), filtered_combined)
    
    return pcd, filtered_combined

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    
    print("="*60)
    print("PRAKTIKUM 13.2: POINT CLOUD FILTERING")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_voxel_downsampling()
    
    noisy_pcd, sor_filtered, sor_indices = demo_statistical_outlier_removal()
    
    _, ror_filtered, ror_indices = demo_radius_outlier_removal()
    
    noisy_combined, combined_filtered = demo_combined_filtering()
    
    pcd_pt, filtered_pt = demo_pass_through_filter()
    
    # Visualisasi (optional)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi? (y/n): ").strip().lower()
        if response == 'y':
            print("\n1. Statistical Outlier Removal...")
            visualize_outliers(noisy_pcd, sor_indices, "Statistical Outlier Removal")
            
            print("\n2. Combined Filtering Result...")
            visualize_filtering_result(noisy_combined, combined_filtered, "Combined Filtering")
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    # Summary
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)
    print(f"\nFile output tersimpan di: {OUTPUT_DIR}")
    print("\nFiles generated:")
    for f in OUTPUT_DIR.glob("*.ply"):
        size_kb = f.stat().st_size / 1024
        print(f"  • {f.name}: {size_kb:.1f} KB")

if __name__ == "__main__":
    main()
