"""
Praktikum 13.7: Mesh Processing
===============================

Program ini mendemonstrasikan operasi mesh processing:
1. Mesh smoothing (Laplacian, Taubin)
2. Mesh simplification (decimation)
3. Mesh subdivision
4. Hole filling
5. Mesh repair dan cleaning
6. Texture/color mapping

Teori:
------
Setelah surface reconstruction, mesh sering memerlukan
post-processing untuk:
- Mengurangi noise (smoothing)
- Mengurangi kompleksitas (simplification)
- Memperbaiki defects (repair)
- Menambah detail (subdivision)

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
DATA_DIR = Path(__file__).parent.parent / "data" / "meshes"
OUTPUT_DIR = Path(__file__).parent / "output"

# Smoothing parameters
LAPLACIAN_ITERATIONS = 10           # Jumlah iterasi Laplacian
LAPLACIAN_LAMBDA = 0.5              # Lambda untuk Laplacian (0-1)
TAUBIN_ITERATIONS = 10              # Jumlah iterasi Taubin
TAUBIN_LAMBDA = 0.5                 # Lambda untuk Taubin
TAUBIN_MU = -0.53                   # Mu untuk Taubin (harus negatif, |mu| > lambda)

# Simplification parameters
TARGET_TRIANGLES = 1000             # Target jumlah triangles
SIMPLIFY_RATIO = 0.1                # Rasio simplification (0.1 = 10% dari original)

# Subdivision parameters
SUBDIVISION_ITERATIONS = 2          # Jumlah iterasi subdivision

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

def create_sample_mesh(mesh_type='noisy_bunny'):
    """
    Membuat sample mesh untuk processing.
    """
    import open3d as o3d
    
    print(f"\n[Generate] Membuat {mesh_type} mesh...")
    
    if mesh_type == 'noisy_bunny':
        # Buat bunny approximation dengan noise
        pcd = create_bunny_point_cloud(20000)
        
        # Poisson reconstruction
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=8
        )
        
        # Add noise ke vertices
        vertices = np.asarray(mesh.vertices)
        noise = np.random.normal(0, 0.01, vertices.shape)
        mesh.vertices = o3d.utility.Vector3dVector(vertices + noise)
        mesh.compute_vertex_normals()
        
    elif mesh_type == 'sphere':
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=1.0, resolution=30)
        
        # Add noise
        vertices = np.asarray(mesh.vertices)
        noise = np.random.normal(0, 0.05, vertices.shape)
        mesh.vertices = o3d.utility.Vector3dVector(vertices + noise)
        mesh.compute_vertex_normals()
        
    elif mesh_type == 'torus':
        mesh = o3d.geometry.TriangleMesh.create_torus(
            torus_radius=1.0, 
            tube_radius=0.3,
            radial_resolution=50,
            tubular_resolution=30
        )
        
        # Add noise
        vertices = np.asarray(mesh.vertices)
        noise = np.random.normal(0, 0.02, vertices.shape)
        mesh.vertices = o3d.utility.Vector3dVector(vertices + noise)
        mesh.compute_vertex_normals()
        
    elif mesh_type == 'with_holes':
        # Create mesh dengan holes
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=1.0, resolution=30)
        
        # Remove beberapa triangles untuk membuat holes
        triangles = np.asarray(mesh.triangles)
        vertices = np.asarray(mesh.vertices)
        
        # Remove triangles in specific regions
        centers = vertices[triangles].mean(axis=1)
        mask = np.ones(len(triangles), dtype=bool)
        
        # Create holes
        hole_centers = [
            np.array([0.5, 0.5, 0.5]),
            np.array([-0.3, -0.3, 0.8]),
            np.array([0.0, 0.7, -0.7])
        ]
        
        for hc in hole_centers:
            distances = np.linalg.norm(centers - hc, axis=1)
            mask &= (distances > 0.3)
        
        mesh.triangles = o3d.utility.Vector3iVector(triangles[mask])
        mesh.remove_unreferenced_vertices()
        mesh.compute_vertex_normals()
        
    else:  # cube
        mesh = o3d.geometry.TriangleMesh.create_box(width=2.0, height=2.0, depth=2.0)
        mesh.translate([-1, -1, -1])
        mesh.compute_vertex_normals()
    
    print(f"  ✓ Created mesh: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")
    
    return mesh

def create_bunny_point_cloud(num_points=20000):
    """Membuat bunny-like point cloud."""
    import open3d as o3d
    
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
    
    points = points - points.mean(axis=0)
    points = points / np.abs(points).max()
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    pcd.orient_normals_consistent_tangent_plane(k=30)
    
    return pcd

def get_mesh_stats(mesh):
    """Dapatkan statistik mesh."""
    return {
        'vertices': len(mesh.vertices),
        'triangles': len(mesh.triangles),
        'watertight': mesh.is_watertight(),
        'edge_manifold': mesh.is_edge_manifold(),
        'vertex_manifold': mesh.is_vertex_manifold()
    }

def print_mesh_stats(mesh, name="Mesh"):
    """Print statistik mesh."""
    stats = get_mesh_stats(mesh)
    print(f"\n{name} Statistics:")
    print(f"  Vertices: {stats['vertices']:,}")
    print(f"  Triangles: {stats['triangles']:,}")
    print(f"  Watertight: {stats['watertight']}")
    print(f"  Edge Manifold: {stats['edge_manifold']}")
    print(f"  Vertex Manifold: {stats['vertex_manifold']}")

# ============================================================
# MESH SMOOTHING
# ============================================================

def laplacian_smooth(mesh, iterations=10, lambda_filter=0.5):
    """
    Laplacian smoothing.
    
    Setiap vertex digeser ke rata-rata posisi neighbors.
    Simple tapi cenderung menyusutkan mesh (shrinkage).
    
    Args:
        mesh: Input mesh
        iterations: Jumlah iterasi
        lambda_filter: Smoothing factor (0-1), higher = more smooth
    
    Returns:
        Smoothed mesh
    """
    import open3d as o3d
    
    print(f"\n[Smoothing] Laplacian (iterations={iterations}, lambda={lambda_filter})...")
    
    mesh_smooth = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_smooth = mesh_smooth.filter_smooth_laplacian(
        number_of_iterations=iterations,
        lambda_filter=lambda_filter
    )
    elapsed = time.time() - start_time
    
    mesh_smooth.compute_vertex_normals()
    
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_smooth

def taubin_smooth(mesh, iterations=10, lambda_filter=0.5, mu=-0.53):
    """
    Taubin smoothing.
    
    Two-step smoothing untuk menghindari shrinkage:
    1. Smooth dengan lambda (menyusut)
    2. Smooth dengan mu negatif (ekspansi)
    
    Requirement: |mu| > lambda untuk mencegah shrinkage
    
    Args:
        mesh: Input mesh
        iterations: Jumlah iterasi
        lambda_filter: Smoothing factor
        mu: Anti-shrinkage factor (negatif, |mu| > lambda)
    
    Returns:
        Smoothed mesh
    """
    import open3d as o3d
    
    print(f"\n[Smoothing] Taubin (iterations={iterations}, lambda={lambda_filter}, mu={mu})...")
    
    mesh_smooth = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_smooth = mesh_smooth.filter_smooth_taubin(
        number_of_iterations=iterations,
        lambda_filter=lambda_filter,
        mu=mu
    )
    elapsed = time.time() - start_time
    
    mesh_smooth.compute_vertex_normals()
    
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_smooth

def simple_smooth(mesh, iterations=5):
    """
    Simple average smoothing.
    
    Args:
        mesh: Input mesh
        iterations: Jumlah iterasi
    
    Returns:
        Smoothed mesh
    """
    import open3d as o3d
    
    print(f"\n[Smoothing] Simple (iterations={iterations})...")
    
    mesh_smooth = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_smooth = mesh_smooth.filter_smooth_simple(
        number_of_iterations=iterations
    )
    elapsed = time.time() - start_time
    
    mesh_smooth.compute_vertex_normals()
    
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_smooth

# ============================================================
# MESH SIMPLIFICATION
# ============================================================

def simplify_quadric_decimation(mesh, target_triangles):
    """
    Quadric Error Metric decimation.
    
    Mengurangi jumlah triangles dengan tetap mempertahankan
    bentuk mesh secara optimal.
    
    Args:
        mesh: Input mesh
        target_triangles: Target jumlah triangles
    
    Returns:
        Simplified mesh
    """
    import open3d as o3d
    
    print(f"\n[Simplification] Quadric Decimation (target={target_triangles})...")
    print(f"  Original: {len(mesh.triangles)} triangles")
    
    mesh_simple = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_simple = mesh_simple.simplify_quadric_decimation(
        target_number_of_triangles=target_triangles
    )
    elapsed = time.time() - start_time
    
    mesh_simple.compute_vertex_normals()
    
    print(f"  ✓ Result: {len(mesh_simple.triangles)} triangles")
    print(f"  ✓ Reduction: {(1 - len(mesh_simple.triangles)/len(mesh.triangles))*100:.1f}%")
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_simple

def simplify_vertex_clustering(mesh, voxel_size=0.05):
    """
    Vertex clustering simplification.
    
    Menggabungkan vertices dalam voxel yang sama.
    Fast tapi kurang akurat.
    
    Args:
        mesh: Input mesh
        voxel_size: Size of voxel grid
    
    Returns:
        Simplified mesh
    """
    import open3d as o3d
    
    print(f"\n[Simplification] Vertex Clustering (voxel_size={voxel_size})...")
    print(f"  Original: {len(mesh.triangles)} triangles")
    
    mesh_simple = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_simple = mesh_simple.simplify_vertex_clustering(
        voxel_size=voxel_size,
        contraction=o3d.geometry.SimplificationContraction.Average
    )
    elapsed = time.time() - start_time
    
    mesh_simple.compute_vertex_normals()
    
    print(f"  ✓ Result: {len(mesh_simple.triangles)} triangles")
    print(f"  ✓ Reduction: {(1 - len(mesh_simple.triangles)/len(mesh.triangles))*100:.1f}%")
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_simple

# ============================================================
# MESH SUBDIVISION
# ============================================================

def subdivide_loop(mesh, iterations=1):
    """
    Loop subdivision.
    
    Membagi setiap triangle menjadi 4 triangles baru,
    dengan posisi vertices yang dihaluskan.
    
    Args:
        mesh: Input mesh
        iterations: Jumlah iterasi subdivision
    
    Returns:
        Subdivided mesh
    """
    import open3d as o3d
    
    print(f"\n[Subdivision] Loop (iterations={iterations})...")
    print(f"  Original: {len(mesh.triangles)} triangles")
    
    mesh_sub = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_sub = mesh_sub.subdivide_loop(number_of_iterations=iterations)
    elapsed = time.time() - start_time
    
    mesh_sub.compute_vertex_normals()
    
    print(f"  ✓ Result: {len(mesh_sub.triangles)} triangles")
    print(f"  ✓ Increase: {len(mesh_sub.triangles)/len(mesh.triangles):.1f}x")
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_sub

def subdivide_midpoint(mesh, iterations=1):
    """
    Midpoint subdivision.
    
    Membagi setiap triangle dengan menambah vertex di
    tengah setiap edge.
    
    Args:
        mesh: Input mesh
        iterations: Jumlah iterasi subdivision
    
    Returns:
        Subdivided mesh
    """
    import open3d as o3d
    
    print(f"\n[Subdivision] Midpoint (iterations={iterations})...")
    print(f"  Original: {len(mesh.triangles)} triangles")
    
    mesh_sub = copy.deepcopy(mesh)
    
    start_time = time.time()
    mesh_sub = mesh_sub.subdivide_midpoint(number_of_iterations=iterations)
    elapsed = time.time() - start_time
    
    mesh_sub.compute_vertex_normals()
    
    print(f"  ✓ Result: {len(mesh_sub.triangles)} triangles")
    print(f"  ✓ Increase: {len(mesh_sub.triangles)/len(mesh.triangles):.1f}x")
    print(f"  ✓ Time: {elapsed*1000:.2f} ms")
    
    return mesh_sub

# ============================================================
# MESH REPAIR & CLEANING
# ============================================================

def clean_mesh(mesh):
    """
    Clean mesh dari degenerate triangles dan unreferenced vertices.
    
    Args:
        mesh: Input mesh
    
    Returns:
        Cleaned mesh
    """
    import open3d as o3d
    
    print("\n[Cleaning] Removing degenerates and unreferenced vertices...")
    
    mesh_clean = copy.deepcopy(mesh)
    
    original_v = len(mesh_clean.vertices)
    original_t = len(mesh_clean.triangles)
    
    # Remove degenerate
    mesh_clean.remove_degenerate_triangles()
    mesh_clean.remove_duplicated_triangles()
    mesh_clean.remove_duplicated_vertices()
    mesh_clean.remove_unreferenced_vertices()
    
    mesh_clean.compute_vertex_normals()
    
    print(f"  ✓ Vertices: {original_v} → {len(mesh_clean.vertices)}")
    print(f"  ✓ Triangles: {original_t} → {len(mesh_clean.triangles)}")
    
    return mesh_clean

def remove_non_manifold(mesh):
    """
    Remove non-manifold vertices dan edges.
    
    Args:
        mesh: Input mesh
    
    Returns:
        Manifold mesh
    """
    import open3d as o3d
    
    print("\n[Repair] Removing non-manifold geometry...")
    
    mesh_repaired = copy.deepcopy(mesh)
    
    # Check sebelum
    nm_edges_before = len(mesh_repaired.get_non_manifold_edges())
    nm_verts_before = len(mesh_repaired.get_non_manifold_vertices())
    
    print(f"  Before: {nm_edges_before} non-manifold edges, {nm_verts_before} non-manifold vertices")
    
    # Remove
    mesh_repaired.remove_non_manifold_edges()
    mesh_repaired.remove_degenerate_triangles()
    mesh_repaired.remove_unreferenced_vertices()
    
    # Check sesudah
    nm_edges_after = len(mesh_repaired.get_non_manifold_edges())
    nm_verts_after = len(mesh_repaired.get_non_manifold_vertices())
    
    print(f"  After: {nm_edges_after} non-manifold edges, {nm_verts_after} non-manifold vertices")
    
    mesh_repaired.compute_vertex_normals()
    
    return mesh_repaired

def compute_mesh_quality(mesh):
    """
    Hitung metrik kualitas mesh.
    
    Args:
        mesh: Input mesh
    
    Returns:
        Quality metrics dictionary
    """
    import open3d as o3d
    
    print("\n[Quality] Computing mesh quality metrics...")
    
    triangles = np.asarray(mesh.triangles)
    vertices = np.asarray(mesh.vertices)
    
    # Compute triangle areas
    areas = []
    for tri in triangles:
        v0, v1, v2 = vertices[tri]
        area = 0.5 * np.linalg.norm(np.cross(v1-v0, v2-v0))
        areas.append(area)
    
    areas = np.array(areas)
    
    # Compute edge lengths
    edge_lengths = []
    for tri in triangles:
        v0, v1, v2 = vertices[tri]
        edge_lengths.append(np.linalg.norm(v1 - v0))
        edge_lengths.append(np.linalg.norm(v2 - v1))
        edge_lengths.append(np.linalg.norm(v0 - v2))
    
    edge_lengths = np.array(edge_lengths)
    
    # Compute aspect ratios (simplified)
    aspect_ratios = []
    for tri in triangles:
        v0, v1, v2 = vertices[tri]
        e0 = np.linalg.norm(v1 - v0)
        e1 = np.linalg.norm(v2 - v1)
        e2 = np.linalg.norm(v0 - v2)
        
        max_edge = max(e0, e1, e2)
        min_edge = min(e0, e1, e2)
        
        if min_edge > 0:
            aspect_ratios.append(max_edge / min_edge)
    
    aspect_ratios = np.array(aspect_ratios)
    
    quality = {
        'triangle_area_mean': np.mean(areas),
        'triangle_area_std': np.std(areas),
        'triangle_area_min': np.min(areas),
        'triangle_area_max': np.max(areas),
        'edge_length_mean': np.mean(edge_lengths),
        'edge_length_std': np.std(edge_lengths),
        'aspect_ratio_mean': np.mean(aspect_ratios),
        'aspect_ratio_max': np.max(aspect_ratios),
        'degenerate_triangles': np.sum(areas < 1e-10)
    }
    
    print(f"  Triangle area: {quality['triangle_area_mean']:.6f} ± {quality['triangle_area_std']:.6f}")
    print(f"  Edge length: {quality['edge_length_mean']:.6f} ± {quality['edge_length_std']:.6f}")
    print(f"  Aspect ratio (mean): {quality['aspect_ratio_mean']:.3f}")
    print(f"  Aspect ratio (max): {quality['aspect_ratio_max']:.3f}")
    print(f"  Degenerate triangles: {quality['degenerate_triangles']}")
    
    return quality

# ============================================================
# COLOR/TEXTURE MAPPING
# ============================================================

def apply_vertex_colors(mesh, color_method='height'):
    """
    Terapkan vertex colors ke mesh.
    
    Args:
        mesh: Input mesh
        color_method: 'height', 'normal', 'curvature', 'uniform'
    
    Returns:
        Colored mesh
    """
    import open3d as o3d
    
    print(f"\n[Coloring] Applying vertex colors (method={color_method})...")
    
    mesh_colored = copy.deepcopy(mesh)
    vertices = np.asarray(mesh_colored.vertices)
    
    if color_method == 'height':
        # Color by height (Z coordinate)
        z = vertices[:, 2]
        z_normalized = (z - z.min()) / (z.max() - z.min() + 1e-10)
        
        # Colormap (blue to red)
        colors = np.zeros((len(vertices), 3))
        colors[:, 0] = z_normalized            # Red
        colors[:, 2] = 1 - z_normalized        # Blue
        
    elif color_method == 'normal':
        # Color by normal direction
        if not mesh_colored.has_vertex_normals():
            mesh_colored.compute_vertex_normals()
        
        normals = np.asarray(mesh_colored.vertex_normals)
        colors = (normals + 1) / 2  # Map [-1,1] to [0,1]
        
    elif color_method == 'curvature':
        # Approximate curvature by Laplacian
        # Build adjacency
        triangles = np.asarray(mesh_colored.triangles)
        neighbors = {i: set() for i in range(len(vertices))}
        
        for tri in triangles:
            neighbors[tri[0]].update([tri[1], tri[2]])
            neighbors[tri[1]].update([tri[0], tri[2]])
            neighbors[tri[2]].update([tri[0], tri[1]])
        
        # Compute Laplacian
        laplacian = np.zeros(len(vertices))
        for i, v in enumerate(vertices):
            if neighbors[i]:
                neighbor_mean = np.mean([vertices[j] for j in neighbors[i]], axis=0)
                laplacian[i] = np.linalg.norm(v - neighbor_mean)
        
        # Normalize
        laplacian = (laplacian - laplacian.min()) / (laplacian.max() - laplacian.min() + 1e-10)
        
        # Colormap (green = low curvature, red = high)
        colors = np.zeros((len(vertices), 3))
        colors[:, 0] = laplacian               # Red
        colors[:, 1] = 1 - laplacian           # Green
        
    else:  # uniform
        colors = np.ones((len(vertices), 3)) * 0.7
    
    mesh_colored.vertex_colors = o3d.utility.Vector3dVector(colors)
    
    print(f"  ✓ Applied colors to {len(vertices)} vertices")
    
    return mesh_colored

# ============================================================
# VISUALISASI
# ============================================================

def visualize_meshes(meshes, titles, window_title="Mesh Comparison"):
    """
    Visualisasi multiple meshes side by side.
    """
    import open3d as o3d
    
    vis_meshes = []
    offset = 0
    
    for mesh, title in zip(meshes, titles):
        mesh_vis = copy.deepcopy(mesh)
        mesh_vis.translate([offset, 0, 0])
        mesh_vis.compute_vertex_normals()
        vis_meshes.append(mesh_vis)
        
        # Estimate offset
        bbox = mesh_vis.get_axis_aligned_bounding_box()
        offset += (bbox.max_bound[0] - bbox.min_bound[0]) * 1.2
    
    print(f"\n[Visualisasi] {window_title}")
    for i, t in enumerate(titles):
        print(f"  Position {i}: {t}")
    
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2)
    
    o3d.visualization.draw_geometries(
        vis_meshes + [coord],
        window_name=window_title,
        width=1400,
        height=800,
        mesh_show_back_face=True
    )

def visualize_wireframe(mesh, title="Wireframe"):
    """Visualisasi mesh dalam wireframe mode."""
    import open3d as o3d
    
    # Convert to lineset
    lineset = o3d.geometry.LineSet.create_from_triangle_mesh(mesh)
    lineset.paint_uniform_color([0.2, 0.2, 0.8])
    
    print(f"\n[Visualisasi] {title} (wireframe)")
    
    o3d.visualization.draw_geometries(
        [lineset],
        window_name=title,
        width=1024,
        height=768
    )

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_smoothing():
    """Demo berbagai teknik smoothing."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 1: Mesh Smoothing Comparison")
    print("="*60)
    
    # Create noisy mesh
    mesh = create_sample_mesh('noisy_bunny')
    print_mesh_stats(mesh, "Original (Noisy)")
    
    # Apply different smoothing
    mesh_simple = simple_smooth(mesh, iterations=5)
    mesh_laplacian = laplacian_smooth(mesh, iterations=LAPLACIAN_ITERATIONS, lambda_filter=LAPLACIAN_LAMBDA)
    mesh_taubin = taubin_smooth(mesh, iterations=TAUBIN_ITERATIONS, 
                                 lambda_filter=TAUBIN_LAMBDA, mu=TAUBIN_MU)
    
    # Save
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "smoothing_original.ply"), mesh)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "smoothing_simple.ply"), mesh_simple)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "smoothing_laplacian.ply"), mesh_laplacian)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "smoothing_taubin.ply"), mesh_taubin)
    
    return mesh, mesh_simple, mesh_laplacian, mesh_taubin

def demo_simplification():
    """Demo mesh simplification."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 2: Mesh Simplification")
    print("="*60)
    
    # Create mesh
    mesh = create_sample_mesh('sphere')
    print_mesh_stats(mesh, "Original")
    
    # Quadric decimation
    mesh_quadric = simplify_quadric_decimation(mesh, TARGET_TRIANGLES)
    print_mesh_stats(mesh_quadric, "Quadric Decimation")
    
    # Vertex clustering
    mesh_cluster = simplify_vertex_clustering(mesh, voxel_size=0.1)
    print_mesh_stats(mesh_cluster, "Vertex Clustering")
    
    # Save
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "simplify_original.ply"), mesh)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "simplify_quadric.ply"), mesh_quadric)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "simplify_cluster.ply"), mesh_cluster)
    
    return mesh, mesh_quadric, mesh_cluster

def demo_subdivision():
    """Demo mesh subdivision."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 3: Mesh Subdivision")
    print("="*60)
    
    # Create simple mesh
    mesh = o3d.geometry.TriangleMesh.create_octahedron()
    mesh.compute_vertex_normals()
    print_mesh_stats(mesh, "Original (Octahedron)")
    
    # Loop subdivision
    mesh_loop = subdivide_loop(mesh, iterations=SUBDIVISION_ITERATIONS)
    print_mesh_stats(mesh_loop, "Loop Subdivision")
    
    # Midpoint subdivision
    mesh_midpoint = subdivide_midpoint(mesh, iterations=SUBDIVISION_ITERATIONS)
    print_mesh_stats(mesh_midpoint, "Midpoint Subdivision")
    
    # Save
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "subdivide_original.ply"), mesh)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "subdivide_loop.ply"), mesh_loop)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "subdivide_midpoint.ply"), mesh_midpoint)
    
    return mesh, mesh_loop, mesh_midpoint

def demo_cleaning():
    """Demo mesh cleaning dan repair."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 4: Mesh Cleaning & Repair")
    print("="*60)
    
    # Create mesh with holes
    mesh = create_sample_mesh('with_holes')
    print_mesh_stats(mesh, "Original (with holes)")
    
    # Clean
    mesh_clean = clean_mesh(mesh)
    print_mesh_stats(mesh_clean, "Cleaned")
    
    # Remove non-manifold
    mesh_repaired = remove_non_manifold(mesh_clean)
    print_mesh_stats(mesh_repaired, "Repaired")
    
    # Quality analysis
    quality_original = compute_mesh_quality(mesh)
    quality_repaired = compute_mesh_quality(mesh_repaired)
    
    # Save
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "repair_original.ply"), mesh)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "repair_cleaned.ply"), mesh_repaired)
    
    return mesh, mesh_clean, mesh_repaired

def demo_coloring():
    """Demo vertex coloring."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 5: Vertex Coloring")
    print("="*60)
    
    # Create mesh
    mesh = create_sample_mesh('torus')
    print_mesh_stats(mesh, "Original")
    
    # Apply different coloring
    mesh_height = apply_vertex_colors(mesh, 'height')
    mesh_normal = apply_vertex_colors(mesh, 'normal')
    mesh_curvature = apply_vertex_colors(mesh, 'curvature')
    
    # Save
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "color_height.ply"), mesh_height)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "color_normal.ply"), mesh_normal)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "color_curvature.ply"), mesh_curvature)
    
    return mesh_height, mesh_normal, mesh_curvature

def demo_pipeline():
    """Demo complete mesh processing pipeline."""
    import open3d as o3d
    
    print("\n" + "="*60)
    print("DEMO 6: Complete Mesh Processing Pipeline")
    print("="*60)
    
    # 1. Create dari point cloud
    print("\n[Step 1] Point cloud to mesh...")
    pcd = create_bunny_point_cloud(30000)
    mesh_raw, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
    print_mesh_stats(mesh_raw, "Raw reconstruction")
    
    # 2. Clean
    print("\n[Step 2] Cleaning...")
    mesh_clean = clean_mesh(mesh_raw)
    print_mesh_stats(mesh_clean, "After cleaning")
    
    # 3. Smooth
    print("\n[Step 3] Smoothing...")
    mesh_smooth = taubin_smooth(mesh_clean, iterations=5)
    print_mesh_stats(mesh_smooth, "After smoothing")
    
    # 4. Simplify
    print("\n[Step 4] Simplification...")
    target = int(len(mesh_smooth.triangles) * 0.2)
    mesh_simple = simplify_quadric_decimation(mesh_smooth, target)
    print_mesh_stats(mesh_simple, "After simplification")
    
    # 5. Quality analysis
    print("\n[Step 5] Quality Analysis...")
    quality = compute_mesh_quality(mesh_simple)
    
    # 6. Color
    print("\n[Step 6] Apply colors...")
    mesh_final = apply_vertex_colors(mesh_simple, 'height')
    
    # Save pipeline results
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "pipeline_1_raw.ply"), mesh_raw)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "pipeline_2_clean.ply"), mesh_clean)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "pipeline_3_smooth.ply"), mesh_smooth)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "pipeline_4_simple.ply"), mesh_simple)
    o3d.io.write_triangle_mesh(str(OUTPUT_DIR / "pipeline_5_final.ply"), mesh_final)
    
    print("\n" + "-"*60)
    print("Pipeline Summary:")
    print(f"  Raw: {len(mesh_raw.triangles):,} triangles")
    print(f"  Clean: {len(mesh_clean.triangles):,} triangles")
    print(f"  Smooth: {len(mesh_smooth.triangles):,} triangles")
    print(f"  Simple: {len(mesh_simple.triangles):,} triangles")
    print(f"  Final: {len(mesh_final.triangles):,} triangles")
    
    return mesh_raw, mesh_clean, mesh_smooth, mesh_simple, mesh_final

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import open3d as o3d
    
    print("="*60)
    print("PRAKTIKUM 13.7: MESH PROCESSING")
    print("="*60)
    
    # Check dependencies
    if not check_open3d():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    mesh_orig, mesh_simple, mesh_lap, mesh_taubin = demo_smoothing()
    
    mesh_s_orig, mesh_quadric, mesh_cluster = demo_simplification()
    
    mesh_sub_orig, mesh_loop, mesh_midpoint = demo_subdivision()
    
    mesh_r_orig, mesh_clean, mesh_repaired = demo_cleaning()
    
    mesh_height, mesh_normal, mesh_curvature = demo_coloring()
    
    pipeline_results = demo_pipeline()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nSmoothing Methods:")
    print("  - Simple: Basic averaging, fast tapi shrinkage")
    print("  - Laplacian: Better quality, moderate shrinkage")
    print("  - Taubin: Best quality, no shrinkage")
    
    print("\nSimplification Methods:")
    print("  - Quadric Decimation: Best quality, slower")
    print("  - Vertex Clustering: Fast, lower quality")
    
    print("\nSubdivision Methods:")
    print("  - Loop: Smooth result, triangles only")
    print("  - Midpoint: Fast, preserves shape")
    
    # Visualisasi (optional)
    try:
        print("\n" + "-"*60)
        response = input("Tampilkan visualisasi? (y/n): ").strip().lower()
        if response == 'y':
            print("\n1. Smoothing comparison...")
            visualize_meshes(
                [mesh_orig, mesh_simple, mesh_lap, mesh_taubin],
                ["Original", "Simple", "Laplacian", "Taubin"],
                "Smoothing Comparison"
            )
            
            print("\n2. Simplification comparison...")
            visualize_meshes(
                [mesh_s_orig, mesh_quadric, mesh_cluster],
                ["Original", "Quadric", "Clustering"],
                "Simplification Comparison"
            )
            
            print("\n3. Pipeline result...")
            visualize_meshes(
                list(pipeline_results),
                ["Raw", "Clean", "Smooth", "Simple", "Final"],
                "Processing Pipeline"
            )
            
    except EOFError:
        print("\n[Info] Mode non-interaktif, skip visualisasi")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)
    print(f"\nFile output tersimpan di: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
