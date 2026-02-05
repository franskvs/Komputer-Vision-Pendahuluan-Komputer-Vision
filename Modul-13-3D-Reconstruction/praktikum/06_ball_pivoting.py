"""
Praktikum 13.6: Ball Pivoting Algorithm (BPA)
=============================================

Program ini mendemonstrasikan Ball Pivoting Algorithm:
1. Konsep dan cara kerja BPA
2. Pemilihan radius optimal
3. Multi-scale BPA
4. Perbandingan dengan Poisson

Teori:
------
Ball Pivoting Algorithm (BPA) adalah metode rekonstruksi surface
yang bekerja dengan "menggelindingkan" bola virtual pada point cloud.

Algoritma:
1. Pilih seed triangle dari 3 titik yang disentuh bola
2. "Pivot" bola pada edge untuk mencari titik ke-4
3. Bentuk triangle baru
4. Ulangi hingga semua edges diproses

Karakteristik:
- Tidak watertight (bisa ada holes)
- Preservasi detail baik
- Sensitif terhadap pemilihan radius
- Cocok untuk thin structures

Radius optimal: ~2x average point spacing

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
DATA_DIR = Path(__file__).parent / "data" / "point_clouds"
OUTPUT_DIR = Path(__file__).parent / "output" / "output6"

# Parameter Ball Pivoting
SINGLE_RADIUS = 0.02            # Single radius untuk basic demo
MULTI_RADII = [0.01, 0.02, 0.04, 0.08]  # Multiple radii untuk multi-scale

# Parameter untuk testing
NUM_POINTS = 30000              # Jumlah points untuk sample

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

def create_sample_point_cloud(shape='bunny', num_points=30000):
    """
    Membuat sample point cloud untuk rekonstruksi.
    """
    import open3d as o3d
    
    print(f"\n[Generate] Membuat {shape} point cloud ({num_points} points)...")
    
    if shape == 'bunny':
        body_points = int(num_points * 0.55)
        head_points = int(num_points * 0.3)
        ear_points = int(num_points * 0.15)
        
        theta = np.random.uniform(0, 2*np.pi, body_points)
        phi = np.random.uniform(0, np.pi, body_points)
        x = 0.5 * np.sin(phi) * np.cos(theta)
        y = 0.35 * np.sin(phi) * np.sin(theta)
        z = 0.45 * np.cos(phi)
        body = np.stack([x, y, z], axis=1)
        
        theta = np.random.uniform(0, 2*np.pi, head_points)
        phi = np.random.uniform(0, np.pi, head_points)
        x = 0.22 * np.sin(phi) * np.cos(theta)
        y = 0.22 * np.sin(phi) * np.sin(theta) + 0.4
        z = 0.22 * np.cos(phi) + 0.35
        head = np.stack([x, y, z], axis=1)
        
        ears_list = []
        for offset in [-0.12, 0.12]:
            ear_n = ear_points // 2
            theta = np.random.uniform(0, 2*np.pi, ear_n)
            phi = np.random.uniform(0, np.pi, ear_n)
            x = 0.06 * np.sin(phi) * np.cos(theta) + offset
            y = 0.06 * np.sin(phi) * np.sin(theta) + 0.55
            z = 0.18 * np.cos(phi) + 0.55
            ears_list.append(np.stack([x, y, z], axis=1))
        
        ears = np.vstack(ears_list)
        points = np.vstack([body, head, ears])
        
    elif shape == 'sphere':
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
        
    elif shape == 'plane_with_holes':
        # Plane dengan beberapa holes untuk testing BPA
        n = int(np.sqrt(num_points))
        x = np.linspace(-1, 1, n)
        y = np.linspace(-1, 1, n)
        X, Y = np.meshgrid(x, y)
        Z = 0.1 * np.sin(3 * X) * np.cos(3 * Y)
        
        points = np.stack([X.flatten(), Y.flatten(), Z.flatten()], axis=1)
        
        # Remove points in circular regions (holes)
        holes = [
            (0.3, 0.3, 0.2),
            (-0.4, -0.2, 0.15),
            (0.0, -0.5, 0.1)
        ]
        
        mask = np.ones(len(points), dtype=bool)
        for hx, hy, hr in holes:
            dist = np.sqrt((points[:, 0] - hx)**2 + (points[:, 1] - hy)**2)
            mask &= (dist > hr)
        
        points = points[mask]
        
    else:
        points = np.random.uniform(-1, 1, (num_points, 3))
    
    # Normalize
    points = points - points.mean(axis=0)
    points = points / np.abs(points).max()
    
    # Add noise
    points += np.random.normal(0, 0.003, points.shape)
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Estimate normals
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    pcd.orient_normals_consistent_tangent_plane(k=30)
    
    print(f"  ✓ Created {len(pcd.points)} points")
    
    return pcd

def estimate_optimal_radius(pcd, k=10):
    """
    Estimasi radius optimal untuk BPA berdasarkan point spacing.
    
    Args:
        pcd: Point cloud
        k: Jumlah neighbors untuk sampling
    
    Returns:
        optimal_radius: Estimated optimal radius
        point_spacing: Average point spacing
    """
    import open3d as o3d
    
    # Build KDTree
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    points = np.asarray(pcd.points)
    
    # Sample points
    sample_size = min(1000, len(points))
    sample_indices = np.random.choice(len(points), sample_size, replace=False)
    
    nn_distances = []
    
    for idx in sample_indices:
        _, _, dists = pcd_tree.search_knn_vector_3d(points[idx], k + 1)
        # Skip first (self), take mean of rest
        nn_distances.append(np.sqrt(dists[1:]).mean())
    
    point_spacing = np.mean(nn_distances)
    
    # Optimal radius is typically 2-3x point spacing
    optimal_radius = point_spacing * 2.5
    
    return optimal_radius, point_spacing

# ============================================================
# FUNGSI BALL PIVOTING
# ============================================================

def ball_pivoting_single(pcd, radius):
    """
    Ball Pivoting dengan single radius.
    
    Args:
        pcd: Point cloud dengan normals
        radius: Ball radius
    
    Returns:
        mesh: Resulting triangle mesh
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    if not pcd.has_normals():
        print("  ✗ Point cloud harus memiliki normals!")
        return None, None
    
    print(f"\n[BPA] Ball Pivoting dengan radius={radius:.4f}...")
    
    start_time = time.time()
    
    radii = o3d.utility.DoubleVector([radius])
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, radii)
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'radius': radius,
        'radii': [radius],
        'vertices': len(mesh.vertices),
        'triangles': len(mesh.triangles),
        'time_ms': elapsed_time
    }
    
    print(f"  ✓ Vertices: {stats['vertices']:,}")
    print(f"  ✓ Triangles: {stats['triangles']:,}")
    print(f"  ✓ Time: {stats['time_ms']:.2f} ms")
    
    return mesh, stats

def ball_pivoting_multi(pcd, radii):
    """
    Ball Pivoting dengan multiple radii (multi-scale).
    
    Multi-scale BPA mencoba radii dari kecil ke besar,
    memungkinkan rekonstruksi area dengan kepadatan berbeda.
    
    Args:
        pcd: Point cloud dengan normals
        radii: List of radii (dari kecil ke besar)
    
    Returns:
        mesh: Resulting triangle mesh
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    if not pcd.has_normals():
        print("  ✗ Point cloud harus memiliki normals!")
        return None, None
    
    # Sort radii
    radii = sorted(radii)
    
    print(f"\n[BPA Multi-scale] Radii: {radii}...")
    
    start_time = time.time()
    
    radii_vector = o3d.utility.DoubleVector(radii)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, radii_vector)
    
    elapsed_time = (time.time() - start_time) * 1000
    
    stats = {
        'radii': radii,
        'vertices': len(mesh.vertices),
        'triangles': len(mesh.triangles),
        'time_ms': elapsed_time
    }
    
    print(f"  ✓ Vertices: {stats['vertices']:,}")
    print(f"  ✓ Triangles: {stats['triangles']:,}")
    print(f"  ✓ Time: {stats['time_ms']:.2f} ms")
    
    return mesh, stats

# ============================================================
# FUNGSI ANALISIS
# ============================================================

def analyze_bpa_mesh(mesh, pcd, name="BPA Mesh"):
    """
    Analisis mesh hasil BPA.
    
    Args:
        mesh: Triangle mesh
        pcd: Original point cloud
        name: Nama untuk display
    """
    import open3d as o3d
    
    print(f"\n{'='*50}")
    print(f"ANALISIS: {name}")
    print(f"{'='*50}")
    
    # Basic stats
    print(f"Vertices: {len(mesh.vertices):,}")
    print(f"Triangles: {len(mesh.triangles):,}")
    
    # Mesh properties
    is_watertight = mesh.is_watertight()
    is_manifold = mesh.is_edge_manifold()
    
    print(f"\nWatertight: {'Yes' if is_watertight else 'No'}")
    print(f"Edge Manifold: {'Yes' if is_manifold else 'No'}")
    
    # Holes estimation
    # BPA cenderung memiliki boundary edges (holes)
    edges = mesh.get_non_manifold_edges()
    print(f"Non-manifold edges: {len(edges)}")
    
    # Coverage
    # Hitung berapa points yang "tercakup" oleh mesh
    mesh_pcd = mesh.sample_points_uniformly(number_of_points=len(pcd.points))
    
    distances_pcd_to_mesh = pcd.compute_point_cloud_distance(mesh_pcd)
    distances_pcd_to_mesh = np.asarray(distances_pcd_to_mesh)
    
    threshold = 0.02
    covered = np.sum(distances_pcd_to_mesh < threshold)
    coverage = covered / len(pcd.points) * 100
    
    print(f"\nCoverage: {coverage:.1f}% of points within {threshold}")
    print(f"Mean distance to mesh: {distances_pcd_to_mesh.mean():.6f}")
    print(f"Max distance to mesh: {distances_pcd_to_mesh.max():.6f}")

def compare_bpa_poisson(pcd):
    """
    Perbandingan BPA vs Poisson reconstruction.
    
    Args:
        pcd: Point cloud dengan normals
    
    Returns:
        Comparison results
    """
    import open3d as o3d
    
    print("\n" + "="*60)
    print("PERBANDINGAN: BPA vs Poisson")
    print("="*60)
    
    # BPA
    print("\n1. Ball Pivoting Algorithm...")
    optimal_r, spacing = estimate_optimal_radius(pcd)
    radii = [optimal_r * 0.5, optimal_r, optimal_r * 2]
    mesh_bpa, stats_bpa = ball_pivoting_multi(pcd, radii)
    
    # Poisson
    print("\n2. Poisson Reconstruction...")
    start_time = time.time()
    mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9
    )
    poisson_time = (time.time() - start_time) * 1000
    
    # Crop Poisson
    densities = np.asarray(densities)
    threshold = np.quantile(densities, 0.01)
    mask = densities < threshold
    mesh_poisson.remove_vertices_by_mask(mask)
    
    stats_poisson = {
        'vertices': len(mesh_poisson.vertices),
        'triangles': len(mesh_poisson.triangles),
        'time_ms': poisson_time
    }
    
    # Compare
    print("\n" + "-"*60)
    print(f"{'Metric':<25} {'BPA':<20} {'Poisson':<20}")
    print("-"*60)
    
    print(f"{'Vertices':<25} {stats_bpa['vertices']:<20,} {stats_poisson['vertices']:<20,}")
    print(f"{'Triangles':<25} {stats_bpa['triangles']:<20,} {stats_poisson['triangles']:<20,}")
    print(f"{'Time (ms)':<25} {stats_bpa['time_ms']:<20.2f} {stats_poisson['time_ms']:<20.2f}")
    print(f"{'Watertight':<25} {'Yes' if mesh_bpa.is_watertight() else 'No':<20} {'Yes' if mesh_poisson.is_watertight() else 'No':<20}")
    print(f"{'Edge Manifold':<25} {'Yes' if mesh_bpa.is_edge_manifold() else 'No':<20} {'Yes' if mesh_poisson.is_edge_manifold() else 'No':<20}")
    
    return mesh_bpa, mesh_poisson

# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_bpa_mesh(mesh, title="BPA Mesh"):
    """
    Visualisasi mesh hasil BPA.
    """
    import open3d as o3d
    
    print(f"\n[Visualisasi] {title}")
    
    mesh.compute_vertex_normals()
    
    o3d.visualization.draw_geometries(
        [mesh],
        window_name=title,
        width=1024,
        height=768,
        mesh_show_back_face=True
    )

def visualize_comparison(mesh_bpa, mesh_poisson, title="BPA vs Poisson"):
    """
    Visualisasi perbandingan BPA dan Poisson side by side.
    """
    import open3d as o3d
    
    mesh_bpa_vis = copy.deepcopy(mesh_bpa)
    mesh_poisson_vis = copy.deepcopy(mesh_poisson)
    
    # Geser
    mesh_poisson_vis.translate([2.5, 0, 0])
    
    # Normals untuk lighting
    mesh_bpa_vis.compute_vertex_normals()
    mesh_poisson_vis.compute_vertex_normals()
    
    # Warna berbeda
    mesh_bpa_vis.paint_uniform_color([0.8, 0.5, 0.2])      # Orange
    mesh_poisson_vis.paint_uniform_color([0.2, 0.5, 0.8])  # Blue
    
    print(f"\n[Visualisasi] {title}")
    print("  Kiri (Orange): Ball Pivoting Algorithm")
    print("  Kanan (Blue): Poisson Reconstruction")
    
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2)
    
    o3d.visualization.draw_geometries(
        [mesh_bpa_vis, mesh_poisson_vis, coord],
        window_name=title,
        width=1400,
        height=800,
        mesh_show_back_face=True
    )

def visualize_radius_effect(pcd, radii_list, title="Radius Effect"):
    """
    Visualisasi efek pemilihan radius.
    """
    import open3d as o3d
    
    meshes = []
    offset = 0
    
    for radius in radii_list:
        mesh, _ = ball_pivoting_single(pcd, radius)
        if mesh is not None:
            mesh.compute_vertex_normals()
            mesh.translate([offset, 0, 0])
            meshes.append(mesh)
            offset += 2.5
    
    print(f"\n[Visualisasi] {title}")
    for i, r in enumerate(radii_list):
        print(f"  Position {i}: radius={r:.4f}")
    
    o3d.visualization.draw_geometries(
        meshes,
        window_name=title,
        width=1400,
        height=800,
        mesh_show_back_face=True
    )

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_basic_bpa():
    """Demo BPA dasar dengan single radius."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: Basic Ball Pivoting Algorithm")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('bunny', NUM_POINTS)
    
    # Estimate optimal radius
    optimal_r, spacing = estimate_optimal_radius(pcd)
    print(f"\nEstimated point spacing: {spacing:.6f}")
    print(f"Estimated optimal radius: {optimal_r:.6f}")
    
    # Run BPA
    mesh, stats = ball_pivoting_single(pcd, optimal_r)
    
    # Analyze
    analyze_bpa_mesh(mesh, pcd, "Basic BPA")
    
    return pcd, mesh

def demo_radius_comparison():
    """Demo perbandingan berbagai radius."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Radius Comparison")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('sphere', NUM_POINTS)
    
    # Get optimal radius
    optimal_r, _ = estimate_optimal_radius(pcd)
    
    # Test different radii
    radii = [optimal_r * 0.5, optimal_r, optimal_r * 2, optimal_r * 4]
    
    print("\n" + "-"*60)
    print(f"{'Radius':<15} {'Vertices':<15} {'Triangles':<15} {'Time (ms)':<15}")
    print("-"*60)
    
    results = []
    
    for r in radii:
        mesh, stats = ball_pivoting_single(pcd, r)
        
        print(f"{r:<15.4f} "
              f"{stats['vertices']:<15,} "
              f"{stats['triangles']:<15,} "
              f"{stats['time_ms']:<15.2f}")
        
        results.append((mesh, r))
        
        # Save
        output_path = OUTPUT_DIR / f"bpa_r{r:.4f}.ply"
        o3d.io.write_triangle_mesh(str(output_path), mesh)
    
    return pcd, results

def demo_multi_scale():
    """Demo multi-scale BPA."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Multi-Scale Ball Pivoting")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('bunny', NUM_POINTS)
    
    # Estimate optimal
    optimal_r, _ = estimate_optimal_radius(pcd)
    
    # Single scale
    print("\n--- Single Scale ---")
    mesh_single, stats_single = ball_pivoting_single(pcd, optimal_r)
    
    # Multi scale
    print("\n--- Multi Scale ---")
    radii = [optimal_r * 0.5, optimal_r, optimal_r * 2, optimal_r * 4]
    mesh_multi, stats_multi = ball_pivoting_multi(pcd, radii)
    
    # Compare
    print("\n" + "-"*40)
    print("Comparison:")
    print(f"  Single scale triangles: {stats_single['triangles']:,}")
    print(f"  Multi scale triangles: {stats_multi['triangles']:,}")
    print(f"  Improvement: {(stats_multi['triangles'] - stats_single['triangles']) / stats_single['triangles'] * 100:.1f}%")
    
    # Save
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "bpa_multi.ply"), mesh_multi)
    
    return mesh_single, mesh_multi

def demo_bpa_vs_poisson():
    """Demo perbandingan BPA vs Poisson."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: BPA vs Poisson Comparison")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('bunny', NUM_POINTS)
    
    mesh_bpa, mesh_poisson = compare_bpa_poisson(pcd)
    
    # Save both
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "comparison_bpa.ply"), mesh_bpa)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "comparison_poisson.ply"), mesh_poisson)
    
    return mesh_bpa, mesh_poisson

def demo_holes_handling():
    """Demo bagaimana BPA menangani point cloud dengan holes."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 5: Handling Sparse Regions / Holes")
    print("="*60)
    
    # Create point cloud dengan holes
    pcd = create_sample_point_cloud('plane_with_holes', NUM_POINTS)
    
    print(f"\nPoint cloud dengan holes: {len(pcd.points)} points")
    
    # BPA
    optimal_r, _ = estimate_optimal_radius(pcd)
    mesh_bpa, _ = ball_pivoting_multi(pcd, [optimal_r*0.5, optimal_r, optimal_r*2])
    
    analyze_bpa_mesh(mesh_bpa, pcd, "BPA on Holey Surface")
    
    # Poisson (untuk perbandingan)
    mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=8
    )
    
    print(f"\nPoisson: {len(mesh_poisson.triangles)} triangles (fills holes)")
    print(f"BPA: {len(mesh_bpa.triangles)} triangles (preserves holes)")
    
    return mesh_bpa, mesh_poisson

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import open3d as o3d
    
    print("="*60)
    print("PRAKTIKUM 13.6: BALL PIVOTING ALGORITHM")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    pcd, mesh_basic = demo_basic_bpa()
    
    pcd_radius, radius_results = demo_radius_comparison()
    
    mesh_single, mesh_multi = demo_multi_scale()
    
    mesh_bpa, mesh_poisson = demo_bpa_vs_poisson()
    
    mesh_holes_bpa, mesh_holes_poisson = demo_holes_handling()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    print("\nKapan menggunakan BPA:")
    print("  ✓ Thin structures (lembar tipis)")
    print("  ✓ Preservasi holes yang disengaja")
    print("  ✓ Point cloud dengan variasi kepadatan")
    print("  ✓ Ketika watertight tidak diperlukan")
    
    print("\nKapan menggunakan Poisson:")
    print("  ✓ Mesh watertight diperlukan")
    print("  ✓ Surface yang smooth")
    print("  ✓ Point cloud yang uniform")
    print("  ✓ Untuk 3D printing")
    
    # Visualisasi (optional)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi? (y/n): ").strip().lower()
        if response == 'y':
            print("\n1. Basic BPA Result...")
            visualize_bpa_mesh(mesh_basic, "Basic BPA")
            
            print("\n2. BPA vs Poisson...")
            visualize_comparison(mesh_bpa, mesh_poisson)
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)
    print(f"\nFile output tersimpan di: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
