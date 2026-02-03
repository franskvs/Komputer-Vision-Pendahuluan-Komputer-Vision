"""
Praktikum 13.4: Point Cloud Registration
========================================

Program ini mendemonstrasikan teknik registrasi point cloud:
1. Iterative Closest Point (ICP) - Point to Point
2. ICP - Point to Plane
3. Global Registration dengan RANSAC
4. Colored ICP

Teori:
------
Registration adalah proses alignment dua atau lebih point cloud ke
sistem koordinat yang sama. Penting untuk:
- Multi-view reconstruction
- Merging scans dari berbagai posisi
- Object tracking
- SLAM (Simultaneous Localization and Mapping)

ICP bekerja secara iteratif:
1. Find closest point correspondence
2. Estimate transformation (R, t)
3. Apply transformation
4. Repeat until convergence

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time
import copy

# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent.parent / "data" / "point_clouds"
OUTPUT_DIR = Path(__file__).parent / "output"

# Parameter ICP
ICP_THRESHOLD = 0.02            # Max correspondence distance
ICP_MAX_ITERATION = 50          # Maximum iterations
ICP_RELATIVE_FITNESS = 1e-6     # Convergence threshold (fitness)
ICP_RELATIVE_RMSE = 1e-6        # Convergence threshold (RMSE)

# Parameter RANSAC
RANSAC_DISTANCE_THRESHOLD = 0.05
RANSAC_EDGE_LENGTH = 0.9
RANSAC_N_POINTS = 3

# Parameter Transformasi untuk Testing
TEST_ROTATION_ANGLE = 30        # Derajat
TEST_TRANSLATION = [0.2, 0.1, 0.05]  # (x, y, z)

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

def create_sample_point_cloud(num_points=30000):
    """
    Membuat sample point cloud bunny-like untuk testing.
    
    Returns:
        o3d.geometry.PointCloud dengan normals
    """
    import open3d as o3d
    
    print(f"\n[Generate] Membuat sample point cloud ({num_points} points)...")
    
    # Generate bunny-like shape
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
    
    # Add small noise
    points += np.random.normal(0, 0.003, points.shape)
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0.5, 0.5, 0.5])
    
    # Estimate normals
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    
    print(f"  ✓ Created {len(pcd.points)} points with normals")
    
    return pcd

def apply_transformation(pcd, rotation_deg=30, translation=[0.2, 0.1, 0.05], add_noise=False):
    """
    Apply transformasi ke point cloud untuk simulasi.
    
    Args:
        pcd: Input point cloud
        rotation_deg: Sudut rotasi (derajat)
        translation: Vektor translasi
        add_noise: Tambahkan noise setelah transformasi
    
    Returns:
        pcd_transformed: Point cloud hasil transformasi
        transformation_matrix: Ground truth transformation
    """
    import open3d as o3d
    
    # Buat copy
    pcd_transformed = copy.deepcopy(pcd)
    
    # Rotation matrix (around Y axis)
    angle_rad = np.deg2rad(rotation_deg)
    R = np.array([
        [np.cos(angle_rad), 0, np.sin(angle_rad)],
        [0, 1, 0],
        [-np.sin(angle_rad), 0, np.cos(angle_rad)]
    ])
    
    # Translation vector
    t = np.array(translation)
    
    # Build 4x4 transformation matrix
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t
    
    # Apply transformation
    pcd_transformed.transform(T)
    
    # Add noise if requested
    if add_noise:
        points = np.asarray(pcd_transformed.points)
        noise = np.random.normal(0, 0.005, points.shape)
        pcd_transformed.points = o3d.utility.Vector3dVector(points + noise)
    
    return pcd_transformed, T

def compute_registration_error(source, target, transformation):
    """
    Hitung error registration.
    
    Args:
        source: Source point cloud
        target: Target point cloud
        transformation: Transformation matrix 4x4
    
    Returns:
        rmse: Root Mean Square Error
        fitness: Proporsi titik yang match
    """
    import open3d as o3d
    
    # Transform source
    source_transformed = copy.deepcopy(source)
    source_transformed.transform(transformation)
    
    # Compute point-to-point distances
    distances = source_transformed.compute_point_cloud_distance(target)
    distances = np.asarray(distances)
    
    # RMSE
    rmse = np.sqrt(np.mean(distances ** 2))
    
    # Fitness (points within threshold)
    threshold = 0.05
    inliers = np.sum(distances < threshold)
    fitness = inliers / len(distances)
    
    return rmse, fitness

# ============================================================
# FUNGSI REGISTRASI
# ============================================================

def icp_point_to_point(source, target, threshold=0.02, init_transform=None):
    """
    Point-to-Point ICP registration.
    
    Meminimalkan:
    E = Σ ||p_i - T(q_i)||²
    
    Args:
        source: Source point cloud
        target: Target point cloud
        threshold: Maximum correspondence distance
        init_transform: Initial transformation guess
    
    Returns:
        result: Registration result
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    if init_transform is None:
        init_transform = np.eye(4)
    
    start_time = time.time()
    
    result = o3d.pipelines.registration.registration_icp(
        source, target, threshold, init_transform,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.pipelines.registration.ICPConvergenceCriteria(
            max_iteration=ICP_MAX_ITERATION,
            relative_fitness=ICP_RELATIVE_FITNESS,
            relative_rmse=ICP_RELATIVE_RMSE
        )
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'Point-to-Point ICP',
        'fitness': result.fitness,
        'inlier_rmse': result.inlier_rmse,
        'time_ms': elapsed_time
    }
    
    return result, stats

def icp_point_to_plane(source, target, threshold=0.02, init_transform=None):
    """
    Point-to-Plane ICP registration.
    
    Meminimalkan:
    E = Σ ((p_i - T(q_i)) · n_i)²
    
    Membutuhkan normals pada target point cloud.
    Lebih akurat untuk surfaces yang smooth.
    
    Args:
        source: Source point cloud
        target: Target point cloud (dengan normals)
        threshold: Maximum correspondence distance
        init_transform: Initial transformation guess
    
    Returns:
        result: Registration result
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    # Pastikan target memiliki normals
    if not target.has_normals():
        target.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
        )
    
    if init_transform is None:
        init_transform = np.eye(4)
    
    start_time = time.time()
    
    result = o3d.pipelines.registration.registration_icp(
        source, target, threshold, init_transform,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(
            max_iteration=ICP_MAX_ITERATION,
            relative_fitness=ICP_RELATIVE_FITNESS,
            relative_rmse=ICP_RELATIVE_RMSE
        )
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'Point-to-Plane ICP',
        'fitness': result.fitness,
        'inlier_rmse': result.inlier_rmse,
        'time_ms': elapsed_time
    }
    
    return result, stats

def global_registration_ransac(source, target, voxel_size=0.05):
    """
    Global registration menggunakan RANSAC dengan FPFH features.
    
    Cocok untuk initial alignment ketika transformasi tidak diketahui.
    
    Args:
        source: Source point cloud
        target: Target point cloud
        voxel_size: Voxel size untuk downsampling
    
    Returns:
        result: Registration result
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    start_time = time.time()
    
    # Preprocessing: downsample
    source_down = source.voxel_down_sample(voxel_size)
    target_down = target.voxel_down_sample(voxel_size)
    
    # Estimate normals
    radius_normal = voxel_size * 2
    source_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )
    target_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )
    
    # Compute FPFH features
    radius_feature = voxel_size * 5
    source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        source_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100)
    )
    target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        target_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100)
    )
    
    # RANSAC registration
    distance_threshold = voxel_size * 1.5
    
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3,  # ransac_n
        [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)
        ],
        o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999)
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'RANSAC Global Registration',
        'fitness': result.fitness,
        'inlier_rmse': result.inlier_rmse,
        'time_ms': elapsed_time,
        'correspondence_set_size': len(result.correspondence_set)
    }
    
    return result, stats

def colored_icp(source, target, voxel_size=0.02, init_transform=None):
    """
    Colored ICP - menggunakan informasi warna selain geometri.
    
    Lebih robust untuk scenes dengan textures.
    
    Args:
        source: Source point cloud dengan warna
        target: Target point cloud dengan warna
        voxel_size: Voxel size untuk processing
        init_transform: Initial transformation
    
    Returns:
        result: Registration result
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    if init_transform is None:
        init_transform = np.eye(4)
    
    start_time = time.time()
    
    # Estimate normals
    if not source.has_normals():
        source.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size*2, max_nn=30)
        )
    if not target.has_normals():
        target.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size*2, max_nn=30)
        )
    
    result = o3d.pipelines.registration.registration_colored_icp(
        source, target, voxel_size, init_transform,
        o3d.pipelines.registration.TransformationEstimationForColoredICP(),
        o3d.pipelines.registration.ICPConvergenceCriteria(
            relative_fitness=1e-6,
            relative_rmse=1e-6,
            max_iteration=50
        )
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'method': 'Colored ICP',
        'fitness': result.fitness,
        'inlier_rmse': result.inlier_rmse,
        'time_ms': elapsed_time
    }
    
    return result, stats

# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_registration(source, target, transformation=None, title="Registration"):
    """
    Visualisasi hasil registrasi.
    
    Args:
        source: Source point cloud (akan di-transform)
        target: Target point cloud
        transformation: Transformation matrix
        title: Window title
    """
    import open3d as o3d
    
    # Buat copy
    source_vis = copy.deepcopy(source)
    target_vis = copy.deepcopy(target)
    
    # Apply transformation ke source
    if transformation is not None:
        source_vis.transform(transformation)
    
    # Beri warna
    source_vis.paint_uniform_color([1, 0, 0])      # Red
    target_vis.paint_uniform_color([0, 1, 0])      # Green
    
    print(f"\n[Visualisasi] {title}")
    print("  Red: Source (transformed)")
    print("  Green: Target")
    
    o3d.visualization.draw_geometries(
        [source_vis, target_vis],
        window_name=title,
        width=1024,
        height=768
    )

def visualize_registration_before_after(source, target, transformation, title="Before vs After"):
    """
    Visualisasi sebelum dan sesudah registrasi side by side.
    """
    import open3d as o3d
    
    # Before (kiri)
    source_before = copy.deepcopy(source)
    target_before = copy.deepcopy(target)
    source_before.paint_uniform_color([1, 0, 0])
    target_before.paint_uniform_color([0, 1, 0])
    
    # After (kanan)
    source_after = copy.deepcopy(source)
    target_after = copy.deepcopy(target)
    source_after.transform(transformation)
    source_after.translate([3, 0, 0])
    target_after.translate([3, 0, 0])
    source_after.paint_uniform_color([1, 0.5, 0])  # Orange
    target_after.paint_uniform_color([0, 0.8, 0.3])  # Light green
    
    print(f"\n[Visualisasi] {title}")
    print("  Kiri: Before registration")
    print("  Kanan: After registration")
    
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2)
    
    o3d.visualization.draw_geometries(
        [source_before, target_before, source_after, target_after, coord],
        window_name=title,
        width=1400,
        height=800
    )

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_point_to_point_icp():
    """Demo Point-to-Point ICP."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: Point-to-Point ICP")
    print("="*60)
    
    # Create target
    target = create_sample_point_cloud(20000)
    
    # Create source dengan transformasi
    source, gt_transform = apply_transformation(
        target, 
        rotation_deg=TEST_ROTATION_ANGLE, 
        translation=TEST_TRANSLATION
    )
    source.paint_uniform_color([1, 0, 0])
    target.paint_uniform_color([0, 1, 0])
    
    print(f"\nGround truth transformation:")
    print(f"  Rotation: {TEST_ROTATION_ANGLE}° around Y axis")
    print(f"  Translation: {TEST_TRANSLATION}")
    
    # Run ICP
    print("\nRunning Point-to-Point ICP...")
    result, stats = icp_point_to_point(source, target, ICP_THRESHOLD)
    
    print(f"\nResults:")
    print(f"  Fitness: {stats['fitness']:.6f}")
    print(f"  RMSE: {stats['inlier_rmse']:.6f}")
    print(f"  Time: {stats['time_ms']:.2f} ms")
    
    print(f"\nEstimated transformation:")
    print(result.transformation)
    
    return source, target, result.transformation

def demo_point_to_plane_icp():
    """Demo Point-to-Plane ICP."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Point-to-Plane ICP")
    print("="*60)
    
    # Create target
    target = create_sample_point_cloud(20000)
    
    # Create source dengan transformasi
    source, gt_transform = apply_transformation(
        target, 
        rotation_deg=TEST_ROTATION_ANGLE, 
        translation=TEST_TRANSLATION
    )
    
    # Run ICP
    print("\nRunning Point-to-Plane ICP...")
    result, stats = icp_point_to_plane(source, target, ICP_THRESHOLD)
    
    print(f"\nResults:")
    print(f"  Fitness: {stats['fitness']:.6f}")
    print(f"  RMSE: {stats['inlier_rmse']:.6f}")
    print(f"  Time: {stats['time_ms']:.2f} ms")
    
    return source, target, result.transformation

def demo_global_registration():
    """Demo Global Registration dengan RANSAC."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Global Registration (RANSAC)")
    print("="*60)
    
    # Create target
    target = create_sample_point_cloud(20000)
    
    # Create source dengan transformasi BESAR
    source, gt_transform = apply_transformation(
        target, 
        rotation_deg=60,  # Rotasi besar
        translation=[0.5, 0.3, 0.2]  # Translasi besar
    )
    
    print(f"\nTransformasi besar:")
    print(f"  Rotation: 60° around Y axis")
    print(f"  Translation: [0.5, 0.3, 0.2]")
    
    # Run global registration
    print("\nRunning RANSAC Global Registration...")
    result_global, stats_global = global_registration_ransac(source, target, voxel_size=0.05)
    
    print(f"\nGlobal Registration Results:")
    print(f"  Fitness: {stats_global['fitness']:.6f}")
    print(f"  RMSE: {stats_global['inlier_rmse']:.6f}")
    print(f"  Time: {stats_global['time_ms']:.2f} ms")
    print(f"  Correspondences: {stats_global['correspondence_set_size']}")
    
    # Refinement dengan ICP
    print("\nRefining with Point-to-Plane ICP...")
    result_refine, stats_refine = icp_point_to_plane(
        source, target, ICP_THRESHOLD, 
        init_transform=result_global.transformation
    )
    
    print(f"\nRefined Results:")
    print(f"  Fitness: {stats_refine['fitness']:.6f}")
    print(f"  RMSE: {stats_refine['inlier_rmse']:.6f}")
    
    return source, target, result_refine.transformation

def demo_comparison():
    """Perbandingan berbagai metode registrasi."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: Perbandingan Metode")
    print("="*60)
    
    # Create point clouds
    target = create_sample_point_cloud(15000)
    source, _ = apply_transformation(target, 25, [0.15, 0.1, 0.05])
    
    print("\n" + "-"*60)
    print(f"{'Method':<25} {'Fitness':<12} {'RMSE':<12} {'Time (ms)':<12}")
    print("-"*60)
    
    # Point-to-Point ICP
    result_p2p, stats_p2p = icp_point_to_point(source, target)
    print(f"{'Point-to-Point ICP':<25} "
          f"{stats_p2p['fitness']:<12.6f} "
          f"{stats_p2p['inlier_rmse']:<12.6f} "
          f"{stats_p2p['time_ms']:<12.2f}")
    
    # Point-to-Plane ICP
    result_p2l, stats_p2l = icp_point_to_plane(source, target)
    print(f"{'Point-to-Plane ICP':<25} "
          f"{stats_p2l['fitness']:<12.6f} "
          f"{stats_p2l['inlier_rmse']:<12.6f} "
          f"{stats_p2l['time_ms']:<12.2f}")
    
    # RANSAC + ICP
    result_ransac, stats_ransac = global_registration_ransac(source, target)
    result_combined, _ = icp_point_to_plane(source, target, init_transform=result_ransac.transformation)
    print(f"{'RANSAC + ICP':<25} "
          f"{result_combined.fitness:<12.6f} "
          f"{result_combined.inlier_rmse:<12.6f} "
          f"{stats_ransac['time_ms']:<12.2f}")
    
    return source, target, result_p2l.transformation

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import open3d as o3d
    
    print("="*60)
    print("PRAKTIKUM 13.4: POINT CLOUD REGISTRATION")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    source_p2p, target_p2p, transform_p2p = demo_point_to_point_icp()
    
    source_p2l, target_p2l, transform_p2l = demo_point_to_plane_icp()
    
    source_global, target_global, transform_global = demo_global_registration()
    
    source_cmp, target_cmp, transform_cmp = demo_comparison()
    
    # Save results
    print("\n" + "-"*40)
    print("Menyimpan hasil...")
    
    # Save aligned point clouds
    source_aligned = copy.deepcopy(source_p2l)
    source_aligned.transform(transform_p2l)
    merged = source_aligned + target_p2l
    o3d.io.write_point_cloud(str(OUTPUT_DIR / "registered_merged.ply"), merged)
    print(f"✓ Saved: {OUTPUT_DIR / 'registered_merged.ply'}")
    
    # Visualisasi (optional)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi? (y/n): ").strip().lower()
        if response == 'y':
            print("\n1. Point-to-Point ICP Result...")
            visualize_registration_before_after(
                source_p2p, target_p2p, transform_p2p,
                "Point-to-Point ICP: Before vs After"
            )
            
            print("\n2. Global Registration Result...")
            visualize_registration(
                source_global, target_global, transform_global,
                "Global Registration Result"
            )
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
