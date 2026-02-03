"""
Praktikum 13.5: Poisson Surface Reconstruction
==============================================

Program ini mendemonstrasikan Poisson surface reconstruction:
1. Preprocessing point cloud
2. Poisson reconstruction dengan berbagai depth
3. Density-based mesh cropping
4. Mesh quality analysis

Teori:
------
Poisson Surface Reconstruction memodelkan surface sebagai iso-surface
dari fungsi indicator χ. Algoritma:

1. Estimate normal di setiap point
2. Construct gradient field V dari normals (pointing inward)
3. Solve Poisson equation: ∇²χ = ∇·V
4. Extract iso-surface (biasanya χ = 0)

Kelebihan:
- Menghasilkan mesh watertight (tertutup)
- Smooth dan detail terjaga
- Robust terhadap noise

Parameter utama:
- depth: Kontrol resolusi octree (8-12 typical)

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

# Parameter Poisson Reconstruction
POISSON_DEPTHS = [6, 8, 9, 10]  # Depth levels untuk perbandingan
DEFAULT_DEPTH = 9               # Default depth
POISSON_WIDTH = 0               # Width parameter (0 = auto)
POISSON_SCALE = 1.1             # Scale factor
POISSON_LINEAR_FIT = False      # Linear interpolation

# Parameter Density Cropping
DENSITY_QUANTILE = 0.01         # Remove lowest density vertices

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

def create_sample_point_cloud(shape='bunny', num_points=50000):
    """
    Membuat sample point cloud untuk rekonstruksi.
    
    Args:
        shape: 'bunny', 'sphere', 'dragon'
        num_points: Jumlah titik
    
    Returns:
        o3d.geometry.PointCloud dengan normals
    """
    import open3d as o3d
    
    print(f"\n[Generate] Membuat {shape} point cloud ({num_points} points)...")
    
    if shape == 'bunny':
        # Generate bunny-like shape
        body_points = int(num_points * 0.55)
        head_points = int(num_points * 0.3)
        ear_points = int(num_points * 0.15)
        
        # Body ellipsoid
        theta = np.random.uniform(0, 2*np.pi, body_points)
        phi = np.random.uniform(0, np.pi, body_points)
        x = 0.5 * np.sin(phi) * np.cos(theta)
        y = 0.35 * np.sin(phi) * np.sin(theta)
        z = 0.45 * np.cos(phi)
        body = np.stack([x, y, z], axis=1)
        
        # Head
        theta = np.random.uniform(0, 2*np.pi, head_points)
        phi = np.random.uniform(0, np.pi, head_points)
        x = 0.22 * np.sin(phi) * np.cos(theta)
        y = 0.22 * np.sin(phi) * np.sin(theta) + 0.4
        z = 0.22 * np.cos(phi) + 0.35
        head = np.stack([x, y, z], axis=1)
        
        # Ears
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
        # Perfect sphere
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
        
    elif shape == 'dragon':
        # Dragon approximation (long body + spikes)
        body_n = int(num_points * 0.7)
        spike_n = int(num_points * 0.3)
        
        # Body (elongated ellipsoid)
        t = np.linspace(0, 2*np.pi, body_n)
        x = 0.8 * np.cos(t) + np.random.normal(0, 0.05, body_n)
        y = 0.3 * np.sin(t) + np.random.normal(0, 0.05, body_n)
        z = np.random.uniform(-0.3, 0.3, body_n)
        body = np.stack([x, y, z], axis=1)
        
        # Spikes
        spikes = []
        for _ in range(spike_n // 10):
            base = np.random.uniform(-0.8, 0.8, 3)
            base[2] = np.random.choice([-0.3, 0.3])
            
            spike_points = base + np.random.normal(0, 0.1, (10, 3))
            spike_points[:, 2] += np.linspace(0, 0.3, 10) * np.sign(base[2])
            spikes.append(spike_points)
        
        spikes = np.vstack(spikes) if spikes else np.zeros((0, 3))
        points = np.vstack([body, spikes]) if len(spikes) > 0 else body
        
    else:
        # Default random
        points = np.random.uniform(-1, 1, (num_points, 3))
    
    # Normalize
    points = points - points.mean(axis=0)
    points = points / np.abs(points).max()
    
    # Add small noise
    points += np.random.normal(0, 0.003, points.shape)
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Estimate normals
    print("  Estimating normals...")
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    
    # Orient normals consistently
    pcd.orient_normals_consistent_tangent_plane(k=30)
    
    print(f"  ✓ Created {len(pcd.points)} points with normals")
    
    return pcd

def load_point_cloud_with_normals(filepath):
    """
    Load point cloud dan pastikan memiliki normals.
    
    Args:
        filepath: Path ke file point cloud
    
    Returns:
        o3d.geometry.PointCloud dengan normals
    """
    import open3d as o3d
    
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"  ✗ File tidak ditemukan: {filepath}")
        return None
    
    pcd = o3d.io.read_point_cloud(str(filepath))
    
    if not pcd.has_normals():
        print("  Estimating normals...")
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
        )
        pcd.orient_normals_consistent_tangent_plane(k=30)
    
    return pcd

# ============================================================
# FUNGSI POISSON RECONSTRUCTION
# ============================================================

def poisson_reconstruction(pcd, depth=9, width=0, scale=1.1, linear_fit=False):
    """
    Melakukan Poisson surface reconstruction.
    
    Args:
        pcd: Point cloud dengan normals
        depth: Depth of octree (higher = more detail)
        width: Width parameter (0 = auto)
        scale: Scale factor for reconstruction
        linear_fit: Use linear interpolation
    
    Returns:
        mesh: Triangle mesh hasil rekonstruksi
        densities: Vertex densities
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    if not pcd.has_normals():
        print("  ✗ Point cloud harus memiliki normals!")
        return None, None, None
    
    print(f"\n[Poisson] Reconstruction dengan depth={depth}...")
    
    start_time = time.time()
    
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd,
        depth=depth,
        width=width,
        scale=scale,
        linear_fit=linear_fit
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    densities = np.asarray(densities)
    
    stats = {
        'depth': depth,
        'vertices': len(mesh.vertices),
        'triangles': len(mesh.triangles),
        'time_ms': elapsed_time,
        'density_min': densities.min(),
        'density_max': densities.max(),
        'density_mean': densities.mean()
    }
    
    print(f"  ✓ Vertices: {stats['vertices']:,}")
    print(f"  ✓ Triangles: {stats['triangles']:,}")
    print(f"  ✓ Time: {stats['time_ms']:.2f} ms")
    
    return mesh, densities, stats

def crop_mesh_by_density(mesh, densities, quantile=0.01):
    """
    Crop mesh berdasarkan density (hapus area dengan density rendah).
    
    Poisson cenderung membuat "extra" surface di area dengan
    sedikit points. Cropping membantu menghapusnya.
    
    Args:
        mesh: Input mesh
        densities: Density values per vertex
        quantile: Quantile threshold untuk cropping
    
    Returns:
        cropped_mesh: Mesh hasil cropping
        stats: Dictionary statistik
    """
    import open3d as o3d
    
    print(f"\n[Crop] Cropping mesh by density (quantile={quantile})...")
    
    # Hitung threshold
    threshold = np.quantile(densities, quantile)
    
    print(f"  Density threshold: {threshold:.4f}")
    
    # Create mask
    vertices_to_remove = densities < threshold
    
    # Remove vertices
    mesh_cropped = copy.deepcopy(mesh)
    mesh_cropped.remove_vertices_by_mask(vertices_to_remove)
    
    removed_vertices = len(mesh.vertices) - len(mesh_cropped.vertices)
    removed_triangles = len(mesh.triangles) - len(mesh_cropped.triangles)
    
    stats = {
        'original_vertices': len(mesh.vertices),
        'cropped_vertices': len(mesh_cropped.vertices),
        'removed_vertices': removed_vertices,
        'original_triangles': len(mesh.triangles),
        'cropped_triangles': len(mesh_cropped.triangles),
        'removed_triangles': removed_triangles
    }
    
    print(f"  ✓ Removed {removed_vertices:,} vertices ({removed_vertices/len(mesh.vertices)*100:.1f}%)")
    print(f"  ✓ Removed {removed_triangles:,} triangles")
    
    return mesh_cropped, stats

# ============================================================
# FUNGSI ANALISIS MESH
# ============================================================

def analyze_mesh(mesh, name="Mesh"):
    """
    Analisis kualitas mesh.
    
    Args:
        mesh: Triangle mesh
        name: Nama untuk display
    """
    import open3d as o3d
    
    print(f"\n{'='*50}")
    print(f"ANALISIS: {name}")
    print(f"{'='*50}")
    
    # Basic info
    print(f"Vertices: {len(mesh.vertices):,}")
    print(f"Triangles: {len(mesh.triangles):,}")
    
    # Bounding box
    bbox = mesh.get_axis_aligned_bounding_box()
    min_bound = bbox.min_bound
    max_bound = bbox.max_bound
    dimensions = max_bound - min_bound
    
    print(f"\nBounding Box:")
    print(f"  Min: ({min_bound[0]:.3f}, {min_bound[1]:.3f}, {min_bound[2]:.3f})")
    print(f"  Max: ({max_bound[0]:.3f}, {max_bound[1]:.3f}, {max_bound[2]:.3f})")
    print(f"  Size: ({dimensions[0]:.3f}, {dimensions[1]:.3f}, {dimensions[2]:.3f})")
    
    # Watertight check
    is_watertight = mesh.is_watertight()
    print(f"\nWatertight: {'Yes ✓' if is_watertight else 'No ✗'}")
    
    # Edge manifold
    is_edge_manifold = mesh.is_edge_manifold()
    print(f"Edge Manifold: {'Yes ✓' if is_edge_manifold else 'No ✗'}")
    
    # Self-intersecting
    is_self_intersecting = mesh.is_self_intersecting()
    print(f"Self-Intersecting: {'Yes ✗' if is_self_intersecting else 'No ✓'}")
    
    # Surface area and volume (jika watertight)
    if is_watertight:
        area = mesh.get_surface_area()
        volume = mesh.get_volume()
        print(f"\nSurface Area: {area:.6f}")
        print(f"Volume: {volume:.6f}")
    
    # Triangle area statistics
    vertices = np.asarray(mesh.vertices)
    triangles = np.asarray(mesh.triangles)
    
    areas = []
    for tri in triangles:
        v0, v1, v2 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
        area = 0.5 * np.linalg.norm(np.cross(v1 - v0, v2 - v0))
        areas.append(area)
    
    areas = np.array(areas)
    print(f"\nTriangle Areas:")
    print(f"  Min: {areas.min():.8f}")
    print(f"  Max: {areas.max():.8f}")
    print(f"  Mean: {areas.mean():.8f}")
    print(f"  Std: {areas.std():.8f}")

def compute_hausdorff_distance(mesh, pcd):
    """
    Hitung Hausdorff distance antara mesh dan point cloud.
    
    Args:
        mesh: Triangle mesh
        pcd: Original point cloud
    
    Returns:
        mean_distance: Mean distance
        max_distance: Maximum distance (Hausdorff)
    """
    import open3d as o3d
    
    # Sample points dari mesh
    mesh_pcd = mesh.sample_points_uniformly(number_of_points=len(pcd.points))
    
    # Compute distances
    distances = mesh_pcd.compute_point_cloud_distance(pcd)
    distances = np.asarray(distances)
    
    return distances.mean(), distances.max()

# ============================================================
# FUNGSI VISUALISASI
# ============================================================

def visualize_mesh(mesh, title="Mesh Visualization"):
    """
    Visualisasi mesh.
    
    Args:
        mesh: Triangle mesh
        title: Window title
    """
    import open3d as o3d
    
    print(f"\n[Visualisasi] {title}")
    print("  Kontrol:")
    print("  - Mouse kiri: Rotate")
    print("  - Mouse kanan: Pan")
    print("  - Scroll: Zoom")
    
    # Compute normals untuk lighting
    mesh.compute_vertex_normals()
    
    o3d.visualization.draw_geometries(
        [mesh],
        window_name=title,
        width=1024,
        height=768,
        mesh_show_back_face=True
    )

def visualize_mesh_with_density(mesh, densities, title="Mesh with Density"):
    """
    Visualisasi mesh dengan warna berdasarkan density.
    
    Args:
        mesh: Triangle mesh
        densities: Density values
        title: Window title
    """
    import open3d as o3d
    
    mesh_vis = copy.deepcopy(mesh)
    
    # Normalize densities
    densities_norm = (densities - densities.min()) / (densities.max() - densities.min())
    
    # Create colormap (blue=low, red=high)
    colors = np.zeros((len(densities_norm), 3))
    colors[:, 0] = densities_norm      # Red channel
    colors[:, 2] = 1 - densities_norm  # Blue channel
    
    mesh_vis.vertex_colors = o3d.utility.Vector3dVector(colors)
    
    print(f"\n[Visualisasi] {title}")
    print("  Warna: Blue=Low density, Red=High density")
    
    o3d.visualization.draw_geometries(
        [mesh_vis],
        window_name=title,
        width=1024,
        height=768
    )

def visualize_comparison(pcd, mesh, title="Point Cloud vs Mesh"):
    """
    Visualisasi perbandingan point cloud dan mesh.
    
    Args:
        pcd: Original point cloud
        mesh: Reconstructed mesh
        title: Window title
    """
    import open3d as o3d
    
    # Geser untuk side-by-side
    pcd_vis = copy.deepcopy(pcd)
    mesh_vis = copy.deepcopy(mesh)
    
    mesh_vis.translate([2.5, 0, 0])
    mesh_vis.compute_vertex_normals()
    
    pcd_vis.paint_uniform_color([0, 0.8, 0.3])
    
    print(f"\n[Visualisasi] {title}")
    print("  Kiri: Point Cloud")
    print("  Kanan: Reconstructed Mesh")
    
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3)
    
    o3d.visualization.draw_geometries(
        [pcd_vis, mesh_vis, coord],
        window_name=title,
        width=1400,
        height=800,
        mesh_show_back_face=True
    )

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_basic_reconstruction():
    """Demo rekonstruksi Poisson dasar."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: Basic Poisson Reconstruction")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('bunny', 50000)
    
    # Reconstruct
    mesh, densities, stats = poisson_reconstruction(pcd, depth=DEFAULT_DEPTH)
    
    # Analyze
    analyze_mesh(mesh, "Poisson Reconstruction")
    
    return pcd, mesh, densities

def demo_depth_comparison():
    """Demo perbandingan berbagai depth levels."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Depth Level Comparison")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('sphere', 40000)
    
    print("\n" + "-"*60)
    print(f"{'Depth':<10} {'Vertices':<15} {'Triangles':<15} {'Time (ms)':<15}")
    print("-"*60)
    
    results = []
    
    for depth in POISSON_DEPTHS:
        mesh, densities, stats = poisson_reconstruction(pcd, depth=depth)
        
        print(f"{stats['depth']:<10} "
              f"{stats['vertices']:<15,} "
              f"{stats['triangles']:<15,} "
              f"{stats['time_ms']:<15.2f}")
        
        results.append((mesh, densities, stats))
        
        # Save
        output_path = OUTPUT_DIR / f"poisson_depth{depth}.ply"
        o3d.io.write_triangle_mesh(str(output_path), mesh)
    
    return results

def demo_density_cropping():
    """Demo cropping berdasarkan density."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Density-Based Cropping")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('bunny', 50000)
    
    # Reconstruct
    mesh, densities, _ = poisson_reconstruction(pcd, depth=9)
    
    print(f"\nDensity statistics:")
    print(f"  Min: {densities.min():.4f}")
    print(f"  Max: {densities.max():.4f}")
    print(f"  Mean: {densities.mean():.4f}")
    print(f"  Std: {densities.std():.4f}")
    
    # Try different quantiles
    quantiles = [0.01, 0.05, 0.1]
    
    print("\n" + "-"*60)
    print(f"{'Quantile':<12} {'Vertices Before':<18} {'Vertices After':<18} {'Removed %':<12}")
    print("-"*60)
    
    results = []
    
    for q in quantiles:
        mesh_cropped, stats = crop_mesh_by_density(mesh, densities, q)
        
        removed_pct = stats['removed_vertices'] / stats['original_vertices'] * 100
        
        print(f"{q:<12.2f} "
              f"{stats['original_vertices']:<18,} "
              f"{stats['cropped_vertices']:<18,} "
              f"{removed_pct:<12.1f}")
        
        results.append((mesh_cropped, q))
    
    # Save best result
    best_mesh, _ = crop_mesh_by_density(mesh, densities, 0.01)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "poisson_cropped.ply"), best_mesh)
    
    return mesh, densities, results

def demo_reconstruction_quality():
    """Demo evaluasi kualitas rekonstruksi."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: Reconstruction Quality Evaluation")
    print("="*60)
    
    # Create point cloud
    pcd = create_sample_point_cloud('bunny', 50000)
    
    print("\n" + "-"*60)
    print(f"{'Depth':<10} {'Mean Dist':<15} {'Max Dist':<15} {'Watertight':<12}")
    print("-"*60)
    
    for depth in [7, 8, 9, 10]:
        mesh, _, _ = poisson_reconstruction(pcd, depth=depth)
        
        mean_dist, max_dist = compute_hausdorff_distance(mesh, pcd)
        is_watertight = "Yes" if mesh.is_watertight() else "No"
        
        print(f"{depth:<10} "
              f"{mean_dist:<15.6f} "
              f"{max_dist:<15.6f} "
              f"{is_watertight:<12}")
    
    # Final reconstruction
    mesh_final, densities_final, _ = poisson_reconstruction(pcd, depth=9)
    mesh_final, _ = crop_mesh_by_density(mesh_final, densities_final, 0.01)
    
    return mesh_final

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import open3d as o3d
    
    print("="*60)
    print("PRAKTIKUM 13.5: POISSON SURFACE RECONSTRUCTION")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    pcd, mesh, densities = demo_basic_reconstruction()
    
    depth_results = demo_depth_comparison()
    
    mesh_orig, densities_orig, crop_results = demo_density_cropping()
    
    mesh_final = demo_reconstruction_quality()
    
    # Save final result
    print("\n" + "-"*40)
    print("Menyimpan hasil akhir...")
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "poisson_final.ply"), mesh_final)
    print(f"✓ Saved: {OUTPUT_DIR / 'poisson_final.ply'}")
    
    # Visualisasi (optional)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi? (y/n): ").strip().lower()
        if response == 'y':
            print("\n1. Basic Reconstruction...")
            visualize_comparison(pcd, mesh, "Point Cloud vs Mesh")
            
            print("\n2. Density Visualization...")
            visualize_mesh_with_density(mesh_orig, densities_orig, "Mesh Density")
            
            print("\n3. Final Mesh...")
            visualize_mesh(mesh_final, "Final Reconstructed Mesh")
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)
    print(f"\nFile output tersimpan di: {OUTPUT_DIR}")
    for f in OUTPUT_DIR.glob("poisson*.ply"):
        size_kb = f.stat().st_size / 1024
        print(f"  • {f.name}: {size_kb:.1f} KB")

if __name__ == "__main__":
    main()
