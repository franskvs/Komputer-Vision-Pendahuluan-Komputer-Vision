"""
Praktikum 13.3: Normal Estimation
=================================

Program ini mendemonstrasikan estimasi normal pada point cloud:
1. Estimasi normal dengan KNN search
2. Estimasi normal dengan Radius search
3. Orientasi normal yang konsisten
4. Visualisasi normal vectors

Teori:
------
Normal vector adalah vektor tegak lurus terhadap permukaan lokal di setiap titik.
Normal sangat penting untuk:
- Surface reconstruction (Poisson)
- Lighting dan rendering
- Analisis bentuk permukaan
- Point cloud registration

Estimasi dilakukan dengan fitting plane ke neighbors lokal dan
mengambil eigenvector dengan eigenvalue terkecil dari covariance matrix.

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time

# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent.parent / "data" / "point_clouds"
OUTPUT_DIR = Path(__file__).parent / "output"

# Parameter KNN Normal Estimation
KNN_VALUES = [10, 20, 30, 50]   # Jumlah neighbors untuk perbandingan

# Parameter Radius Normal Estimation
RADIUS_VALUES = [0.05, 0.1, 0.2]  # Radius search untuk perbandingan

# Parameter Default
DEFAULT_KNN = 30                # Default K untuk KNN
DEFAULT_RADIUS = 0.1            # Default radius

# Visualization
NORMAL_LENGTH = 0.03            # Panjang normal untuk visualisasi

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
        return False

def create_sample_point_cloud(shape='sphere', num_points=20000):
    """
    Membuat sample point cloud untuk testing.
    
    Args:
        shape: 'sphere', 'cube', 'bunny_approx'
        num_points: Jumlah titik
    
    Returns:
        o3d.geometry.PointCloud
    """
    import open3d as o3d
    
    print(f"\n[Generate] Membuat {shape} point cloud ({num_points} points)...")
    
    if shape == 'sphere':
        # Fibonacci sphere
        phi = np.pi * (3.0 - np.sqrt(5.0))
        points = []
        
        for i in range(num_points):
            y = 1 - (i / float(num_points - 1)) * 2
            r_at_y = np.sqrt(max(1 - y * y, 0))
            theta = phi * i
            
            x = np.cos(theta) * r_at_y
            z = np.sin(theta) * r_at_y
            points.append([x, y, z])
        
        points = np.array(points)
        
    elif shape == 'cube':
        # Cube surface sampling
        points_per_face = num_points // 6
        points = []
        
        for axis in range(3):
            for sign in [-1, 1]:
                face_points = np.random.uniform(-1, 1, (points_per_face, 3))
                face_points[:, axis] = sign
                points.append(face_points)
        
        points = np.vstack(points)
        
    elif shape == 'bunny_approx':
        # Approximate bunny dengan ellipsoids
        body_points = int(num_points * 0.6)
        head_points = int(num_points * 0.3)
        ear_points = int(num_points * 0.1)
        
        # Body
        theta = np.random.uniform(0, 2*np.pi, body_points)
        phi = np.random.uniform(0, np.pi, body_points)
        x = 0.5 * np.sin(phi) * np.cos(theta)
        y = 0.3 * np.sin(phi) * np.sin(theta)
        z = 0.4 * np.cos(phi)
        body = np.stack([x, y, z], axis=1)
        
        # Head
        theta = np.random.uniform(0, 2*np.pi, head_points)
        phi = np.random.uniform(0, np.pi, head_points)
        x = 0.2 * np.sin(phi) * np.cos(theta)
        y = 0.2 * np.sin(phi) * np.sin(theta) + 0.35
        z = 0.2 * np.cos(phi) + 0.3
        head = np.stack([x, y, z], axis=1)
        
        # Ears
        ears_list = []
        for offset in [-0.1, 0.1]:
            theta = np.random.uniform(0, 2*np.pi, ear_points//2)
            phi = np.random.uniform(0, np.pi, ear_points//2)
            x = 0.05 * np.sin(phi) * np.cos(theta) + offset
            y = 0.05 * np.sin(phi) * np.sin(theta) + 0.5
            z = 0.15 * np.cos(phi) + 0.5
            ears_list.append(np.stack([x, y, z], axis=1))
        
        ears = np.vstack(ears_list)
        points = np.vstack([body, head, ears])
        
        # Normalize
        points = points - points.mean(axis=0)
        points = points / np.abs(points).max()
    
    else:
        # Default random
        points = np.random.uniform(-1, 1, (num_points, 3))
    
    # Add small noise
    points += np.random.normal(0, 0.005, points.shape)
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    print(f"  ✓ Created {len(pcd.points)} points")
    
    return pcd

# ============================================================
# FUNGSI ESTIMASI NORMAL
# ============================================================

def estimate_normals_knn(pcd, k=30):
    """
    Estimasi normal menggunakan K-Nearest Neighbors.
    
    Langkah:
    1. Untuk setiap titik, cari k tetangga terdekat
    2. Compute covariance matrix dari neighbors
    3. Normal = eigenvector dengan eigenvalue terkecil
    
    Args:
        pcd: Input point cloud
        k: Jumlah neighbors
    
    Returns:
        pcd_with_normals: Point cloud dengan normals
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    # Buat copy
    pcd_result = o3d.geometry.PointCloud(pcd)
    
    start_time = time.time()
    
    # Estimate normals dengan KNN search
    pcd_result.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamKNN(knn=k)
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'KNN',
        'k': k,
        'num_points': len(pcd_result.points),
        'time_ms': elapsed_time
    }
    
    return pcd_result, stats

def estimate_normals_radius(pcd, radius=0.1):
    """
    Estimasi normal menggunakan Radius Search.
    
    Args:
        pcd: Input point cloud
        radius: Radius pencarian
    
    Returns:
        pcd_with_normals: Point cloud dengan normals
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    pcd_result = o3d.geometry.PointCloud(pcd)
    
    start_time = time.time()
    
    # Estimate normals dengan radius search
    pcd_result.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamRadius(radius=radius)
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'Radius',
        'radius': radius,
        'num_points': len(pcd_result.points),
        'time_ms': elapsed_time
    }
    
    return pcd_result, stats

def estimate_normals_hybrid(pcd, radius=0.1, max_nn=30):
    """
    Estimasi normal menggunakan Hybrid Search (Radius + Max KNN).
    
    Args:
        pcd: Input point cloud
        radius: Radius pencarian
        max_nn: Maximum neighbors
    
    Returns:
        pcd_with_normals: Point cloud dengan normals
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    pcd_result = o3d.geometry.PointCloud(pcd)
    
    start_time = time.time()
    
    # Estimate normals dengan hybrid search
    pcd_result.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=radius, 
            max_nn=max_nn
        )
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'Hybrid',
        'radius': radius,
        'max_nn': max_nn,
        'num_points': len(pcd_result.points),
        'time_ms': elapsed_time
    }
    
    return pcd_result, stats

def orient_normals_consistent(pcd, k=30):
    """
    Membuat orientasi normal konsisten (pointing outward).
    
    Konsep:
    - Normal bisa menunjuk ke dalam atau ke luar
    - Untuk surface reconstruction, orientasi harus konsisten
    - Metode: propagasi orientasi dari neighbors
    
    Args:
        pcd: Point cloud dengan normals
        k: Jumlah neighbors untuk propagasi
    
    Returns:
        pcd_oriented: Point cloud dengan normals terorientasi
    """
    import open3d as o3d
    
    pcd_result = o3d.geometry.PointCloud(pcd)
    
    if not pcd_result.has_normals():
        print("  ✗ Point cloud tidak memiliki normals!")
        return pcd_result
    
    start_time = time.time()
    
    # Orient normals consistently
    pcd_result.orient_normals_consistent_tangent_plane(k=k)
    
    elapsed_time = (time.time() - start_time) * 1000
    
    print(f"  ✓ Normals oriented (k={k}), waktu: {elapsed_time:.2f} ms")
    
    return pcd_result

def orient_normals_to_camera(pcd, camera_location=[0, 0, 5]):
    """
    Orient normal menuju posisi kamera.
    
    Args:
        pcd: Point cloud dengan normals
        camera_location: Posisi kamera
    
    Returns:
        pcd_oriented: Point cloud dengan normals terorientasi ke kamera
    """
    import open3d as o3d
    
    pcd_result = o3d.geometry.PointCloud(pcd)
    
    if not pcd_result.has_normals():
        print("  ✗ Point cloud tidak memiliki normals!")
        return pcd_result
    
    start_time = time.time()
    
    # Orient toward camera
    pcd_result.orient_normals_towards_camera_location(
        camera_location=camera_location
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    print(f"  ✓ Normals oriented to camera {camera_location}, waktu: {elapsed_time:.2f} ms")
    
    return pcd_result

# ============================================================
# FUNGSI ANALISIS
# ============================================================

def analyze_normals(pcd, name="Point Cloud"):
    """
    Analisis kualitas normal estimation.
    
    Args:
        pcd: Point cloud dengan normals
        name: Nama untuk display
    """
    if not pcd.has_normals():
        print(f"\n[{name}] Tidak memiliki normals!")
        return
    
    normals = np.asarray(pcd.normals)
    
    print(f"\n{'='*50}")
    print(f"ANALISIS NORMAL: {name}")
    print(f"{'='*50}")
    
    print(f"Jumlah normals: {len(normals)}")
    
    # Check magnitude (should be ~1 for unit normals)
    magnitudes = np.linalg.norm(normals, axis=1)
    print(f"\nMagnitude statistics:")
    print(f"  Mean: {magnitudes.mean():.6f}")
    print(f"  Std:  {magnitudes.std():.6f}")
    print(f"  Min:  {magnitudes.min():.6f}")
    print(f"  Max:  {magnitudes.max():.6f}")
    
    # Check for zero normals
    zero_normals = np.sum(magnitudes < 1e-6)
    print(f"\nZero normals: {zero_normals}")
    
    # Direction distribution
    print(f"\nDirection distribution (component means):")
    print(f"  X: {normals[:, 0].mean():.4f} (std: {normals[:, 0].std():.4f})")
    print(f"  Y: {normals[:, 1].mean():.4f} (std: {normals[:, 1].std():.4f})")
    print(f"  Z: {normals[:, 2].mean():.4f} (std: {normals[:, 2].std():.4f})")

def compute_normal_consistency(pcd, k=20):
    """
    Hitung metrik konsistensi normal dengan neighbors.
    
    Args:
        pcd: Point cloud dengan normals
        k: Jumlah neighbors untuk analisis
    
    Returns:
        consistency_score: Score 0-1 (1 = perfectly consistent)
    """
    import open3d as o3d
    
    if not pcd.has_normals():
        return 0.0
    
    points = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    
    # Build KDTree
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    
    # Sample points for efficiency
    sample_size = min(1000, len(points))
    sample_indices = np.random.choice(len(points), sample_size, replace=False)
    
    dot_products = []
    
    for idx in sample_indices:
        # Find k nearest neighbors
        _, nn_indices, _ = pcd_tree.search_knn_vector_3d(points[idx], k)
        
        # Compute dot product with neighbors' normals
        for nn_idx in nn_indices[1:]:  # Skip self
            dot = np.dot(normals[idx], normals[nn_idx])
            dot_products.append(abs(dot))  # Use abs for consistency regardless of direction
    
    consistency_score = np.mean(dot_products)
    
    return consistency_score

# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_normals(pcd, title="Normal Visualization"):
    """
    Visualisasi point cloud dengan normal vectors.
    
    Args:
        pcd: Point cloud dengan normals
        title: Judul window
    """
    import open3d as o3d
    
    if not pcd.has_normals():
        print("  ✗ Point cloud tidak memiliki normals!")
        return
    
    print(f"\n[Visualisasi] {title}")
    print("  Tips: Tekan 'N' untuk toggle normal display")
    
    # Warnai berdasarkan arah normal
    normals = np.asarray(pcd.normals)
    colors = (normals + 1) / 2  # Map [-1,1] to [0,1]
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # Visualize with normals
    o3d.visualization.draw_geometries(
        [pcd],
        window_name=title,
        width=1024,
        height=768,
        point_show_normal=True
    )

def visualize_normal_comparison(pcd_list, names, title="Normal Comparison"):
    """
    Visualisasi perbandingan beberapa hasil estimasi normal.
    
    Args:
        pcd_list: List of point clouds dengan normals
        names: List of names
        title: Window title
    """
    import open3d as o3d
    
    print(f"\n[Visualisasi] {title}")
    
    geometries = []
    offset = 0
    
    for i, (pcd, name) in enumerate(zip(pcd_list, names)):
        pcd_vis = o3d.geometry.PointCloud(pcd)
        
        # Geser untuk visualisasi
        pcd_vis.translate([offset, 0, 0])
        offset += 2.5
        
        # Warnai berdasarkan arah normal
        if pcd_vis.has_normals():
            normals = np.asarray(pcd_vis.normals)
            colors = (normals + 1) / 2
            pcd_vis.colors = o3d.utility.Vector3dVector(colors)
        
        geometries.append(pcd_vis)
        print(f"  {name}: offset=[{offset-2.5}, 0, 0]")
    
    # Add coordinate frame
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3)
    geometries.append(coord)
    
    o3d.visualization.draw_geometries(
        geometries,
        window_name=title,
        width=1400,
        height=800,
        point_show_normal=True
    )

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_knn_normal_estimation():
    """Demo estimasi normal dengan berbagai nilai K."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: KNN Normal Estimation")
    print("="*60)
    
    # Buat point cloud
    pcd = create_sample_point_cloud('sphere', 20000)
    
    print("\n" + "-"*40)
    print("Perbandingan nilai K:")
    print("-"*40)
    print(f"{'K':<10} {'Time (ms)':<15} {'Consistency':<15}")
    print("-"*40)
    
    results = []
    
    for k in KNN_VALUES:
        pcd_with_normals, stats = estimate_normals_knn(pcd, k)
        consistency = compute_normal_consistency(pcd_with_normals)
        
        print(f"{k:<10} {stats['time_ms']:<15.2f} {consistency:<15.4f}")
        results.append((pcd_with_normals, f"K={k}"))
    
    return results

def demo_radius_normal_estimation():
    """Demo estimasi normal dengan berbagai radius."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Radius Normal Estimation")
    print("="*60)
    
    # Buat point cloud
    pcd = create_sample_point_cloud('cube', 15000)
    
    print("\n" + "-"*40)
    print("Perbandingan nilai Radius:")
    print("-"*40)
    print(f"{'Radius':<10} {'Time (ms)':<15} {'Consistency':<15}")
    print("-"*40)
    
    results = []
    
    for radius in RADIUS_VALUES:
        pcd_with_normals, stats = estimate_normals_radius(pcd, radius)
        consistency = compute_normal_consistency(pcd_with_normals)
        
        print(f"{radius:<10.3f} {stats['time_ms']:<15.2f} {consistency:<15.4f}")
        results.append((pcd_with_normals, f"R={radius}"))
    
    return results

def demo_normal_orientation():
    """Demo orientasi normal yang konsisten."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Normal Orientation")
    print("="*60)
    
    # Buat point cloud
    pcd = create_sample_point_cloud('bunny_approx', 15000)
    
    # Estimate normals
    print("\n1. Estimate normals...")
    pcd_with_normals, _ = estimate_normals_knn(pcd, 30)
    
    # Analisis sebelum orientasi
    print("\n2. Analisis sebelum orientasi:")
    normals_before = np.asarray(pcd_with_normals.normals).copy()
    analyze_normals(pcd_with_normals, "Before Orientation")
    
    # Orient normals consistently
    print("\n3. Orient normals consistently...")
    pcd_oriented = orient_normals_consistent(pcd_with_normals, k=50)
    
    # Analisis setelah orientasi
    print("\n4. Analisis setelah orientasi:")
    analyze_normals(pcd_oriented, "After Orientation")
    
    # Orient toward camera
    print("\n5. Orient toward camera...")
    pcd_to_camera = o3d.geometry.PointCloud(pcd_with_normals)
    pcd_to_camera = orient_normals_to_camera(pcd_to_camera, [0, 0, 3])
    
    return pcd_with_normals, pcd_oriented, pcd_to_camera

def demo_hybrid_estimation():
    """Demo hybrid normal estimation."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: Hybrid Normal Estimation")
    print("="*60)
    
    # Buat point cloud
    pcd = create_sample_point_cloud('sphere', 20000)
    
    print("\n" + "-"*40)
    print("Perbandingan metode:")
    print("-"*40)
    print(f"{'Method':<20} {'Time (ms)':<15} {'Consistency':<15}")
    print("-"*50)
    
    # KNN
    pcd_knn, stats_knn = estimate_normals_knn(pcd, 30)
    cons_knn = compute_normal_consistency(pcd_knn)
    print(f"{'KNN (k=30)':<20} {stats_knn['time_ms']:<15.2f} {cons_knn:<15.4f}")
    
    # Radius
    pcd_radius, stats_radius = estimate_normals_radius(pcd, 0.1)
    cons_radius = compute_normal_consistency(pcd_radius)
    print(f"{'Radius (r=0.1)':<20} {stats_radius['time_ms']:<15.2f} {cons_radius:<15.4f}")
    
    # Hybrid
    pcd_hybrid, stats_hybrid = estimate_normals_hybrid(pcd, 0.1, 30)
    cons_hybrid = compute_normal_consistency(pcd_hybrid)
    print(f"{'Hybrid (r=0.1,k=30)':<20} {stats_hybrid['time_ms']:<15.2f} {cons_hybrid:<15.4f}")
    
    return [
        (pcd_knn, "KNN"),
        (pcd_radius, "Radius"),
        (pcd_hybrid, "Hybrid")
    ]

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import open3d as o3d
    
    print("="*60)
    print("PRAKTIKUM 13.3: NORMAL ESTIMATION")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    knn_results = demo_knn_normal_estimation()
    
    radius_results = demo_radius_normal_estimation()
    
    pcd_before, pcd_oriented, pcd_camera = demo_normal_orientation()
    
    method_results = demo_hybrid_estimation()
    
    # Save results
    print("\n" + "-"*40)
    print("Menyimpan hasil...")
    
    # Save best result
    pcd_final, _ = estimate_normals_hybrid(
        create_sample_point_cloud('sphere', 30000), 
        0.1, 30
    )
    pcd_final = orient_normals_consistent(pcd_final, k=50)
    o3d.io.write_point_cloud(str(OUTPUT_DIR / "normals_estimated.ply"), pcd_final)
    print(f"✓ Saved: {OUTPUT_DIR / 'normals_estimated.ply'}")
    
    # Visualisasi (optional)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi? (y/n): ").strip().lower()
        if response == 'y':
            print("\n1. KNN Normal Estimation...")
            visualize_normals(knn_results[1][0], "KNN Normal (K=20)")
            
            print("\n2. Normal Orientation Comparison...")
            visualize_normal_comparison(
                [pcd_before, pcd_oriented],
                ["Before Orientation", "After Orientation"],
                "Normal Orientation Comparison"
            )
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)
    print(f"\nFile output tersimpan di: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
