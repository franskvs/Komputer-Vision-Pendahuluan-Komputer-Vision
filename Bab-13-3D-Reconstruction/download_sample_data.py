"""
Download Sample Data untuk Bab 13: 3D Reconstruction
=====================================================

Script ini mengunduh dan menyiapkan data sample untuk praktikum
3D reconstruction termasuk point cloud dan mesh files.

Author: Praktikum Computer Vision
Tanggal: 2024
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path
import numpy as np

# ============================================================
# KONFIGURASI - Sesuaikan path sesuai kebutuhan
# ============================================================

# Direktori output untuk data
DATA_DIR = Path(__file__).parent / "data"
POINT_CLOUD_DIR = DATA_DIR / "point_clouds"
MESH_DIR = DATA_DIR / "meshes"
DEPTH_DIR = DATA_DIR / "depth_images"

# URL untuk sample data
SAMPLE_URLS = {
    "bunny": "http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz",
    # Alternative sources jika Stanford tidak tersedia
}

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def create_directories():
    """Membuat struktur direktori yang diperlukan."""
    directories = [DATA_DIR, POINT_CLOUD_DIR, MESH_DIR, DEPTH_DIR]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Direktori dibuat: {dir_path}")

def download_file(url, destination):
    """
    Mengunduh file dari URL.
    
    Args:
        url: URL sumber file
        destination: Path tujuan penyimpanan
    """
    try:
        print(f"Mengunduh dari {url}...")
        urllib.request.urlretrieve(url, destination)
        print(f"✓ Berhasil mengunduh ke {destination}")
        return True
    except Exception as e:
        print(f"✗ Gagal mengunduh: {e}")
        return False

def generate_synthetic_point_cloud(name, num_points=10000):
    """
    Generate point cloud sintetis untuk testing.
    
    Args:
        name: Nama shape ('sphere', 'cube', 'cylinder', 'bunny_approx')
        num_points: Jumlah titik
    
    Returns:
        points: numpy array (N, 3)
        colors: numpy array (N, 3) normalized 0-1
    """
    if name == 'sphere':
        # Sphere menggunakan fibonacci sampling
        phi = np.pi * (3. - np.sqrt(5.))  # golden angle
        indices = np.arange(num_points)
        y = 1 - (indices / float(num_points - 1)) * 2  # y goes from 1 to -1
        radius_at_y = np.sqrt(1 - y * y)
        theta = phi * indices
        
        x = np.cos(theta) * radius_at_y
        z = np.sin(theta) * radius_at_y
        
        points = np.stack([x, y, z], axis=1)
        # Warna berdasarkan posisi
        colors = (points - points.min()) / (points.max() - points.min())
        
    elif name == 'cube':
        # Cube dengan sampling pada permukaan
        points_per_face = num_points // 6
        points_list = []
        
        for face in range(6):
            if face == 0:  # front
                x = np.random.uniform(-1, 1, points_per_face)
                y = np.random.uniform(-1, 1, points_per_face)
                z = np.ones(points_per_face)
            elif face == 1:  # back
                x = np.random.uniform(-1, 1, points_per_face)
                y = np.random.uniform(-1, 1, points_per_face)
                z = -np.ones(points_per_face)
            elif face == 2:  # top
                x = np.random.uniform(-1, 1, points_per_face)
                y = np.ones(points_per_face)
                z = np.random.uniform(-1, 1, points_per_face)
            elif face == 3:  # bottom
                x = np.random.uniform(-1, 1, points_per_face)
                y = -np.ones(points_per_face)
                z = np.random.uniform(-1, 1, points_per_face)
            elif face == 4:  # right
                x = np.ones(points_per_face)
                y = np.random.uniform(-1, 1, points_per_face)
                z = np.random.uniform(-1, 1, points_per_face)
            else:  # left
                x = -np.ones(points_per_face)
                y = np.random.uniform(-1, 1, points_per_face)
                z = np.random.uniform(-1, 1, points_per_face)
            
            points_list.append(np.stack([x, y, z], axis=1))
        
        points = np.vstack(points_list)
        colors = (points - points.min()) / (points.max() - points.min())
        
    elif name == 'cylinder':
        # Cylinder
        theta = np.random.uniform(0, 2*np.pi, num_points)
        h = np.random.uniform(-1, 1, num_points)
        r = np.ones(num_points)
        
        x = r * np.cos(theta)
        y = h
        z = r * np.sin(theta)
        
        points = np.stack([x, y, z], axis=1)
        colors = np.zeros_like(points)
        colors[:, 0] = (theta / (2*np.pi))  # Red based on angle
        colors[:, 1] = (h + 1) / 2  # Green based on height
        colors[:, 2] = 0.5
        
    elif name == 'bunny_approx':
        # Approximasi bunny shape dengan ellipsoids
        # Body
        body_points = num_points * 2 // 3
        theta = np.random.uniform(0, 2*np.pi, body_points)
        phi = np.random.uniform(0, np.pi, body_points)
        
        x = 0.5 * np.sin(phi) * np.cos(theta)
        y = 0.3 * np.sin(phi) * np.sin(theta)
        z = 0.4 * np.cos(phi)
        
        body = np.stack([x, y, z], axis=1)
        
        # Head (smaller sphere offset)
        head_points = num_points // 6
        theta = np.random.uniform(0, 2*np.pi, head_points)
        phi = np.random.uniform(0, np.pi, head_points)
        
        x = 0.2 * np.sin(phi) * np.cos(theta)
        y = 0.2 * np.sin(phi) * np.sin(theta) + 0.35
        z = 0.2 * np.cos(phi) + 0.3
        
        head = np.stack([x, y, z], axis=1)
        
        # Ears (two elongated ellipsoids)
        ear_points = num_points // 12
        for ear_offset in [-0.1, 0.1]:
            theta = np.random.uniform(0, 2*np.pi, ear_points)
            phi = np.random.uniform(0, np.pi, ear_points)
            
            x = 0.05 * np.sin(phi) * np.cos(theta) + ear_offset
            y = 0.05 * np.sin(phi) * np.sin(theta) + 0.5
            z = 0.15 * np.cos(phi) + 0.5
            
            ear = np.stack([x, y, z], axis=1)
            head = np.vstack([head, ear])
        
        points = np.vstack([body, head])
        
        # Normalize to unit sphere
        center = points.mean(axis=0)
        points = points - center
        scale = np.abs(points).max()
        points = points / scale
        
        colors = np.ones_like(points) * 0.8  # Light gray
        colors[:, 1] = 0.7  # Slight brown tint
        colors[:, 2] = 0.6
        
    else:
        raise ValueError(f"Unknown shape: {name}")
    
    # Add small noise for realism
    noise = np.random.normal(0, 0.005, points.shape)
    points = points + noise
    
    return points.astype(np.float32), colors.astype(np.float32)

def save_point_cloud_ply(points, colors, filepath):
    """
    Simpan point cloud ke format PLY.
    
    Args:
        points: numpy array (N, 3)
        colors: numpy array (N, 3) normalized 0-1
        filepath: path output
    """
    num_points = len(points)
    
    # Convert colors to uint8
    colors_uint8 = (colors * 255).astype(np.uint8)
    
    with open(filepath, 'w') as f:
        # Header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {num_points}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        # Data
        for i in range(num_points):
            f.write(f"{points[i,0]:.6f} {points[i,1]:.6f} {points[i,2]:.6f} ")
            f.write(f"{colors_uint8[i,0]} {colors_uint8[i,1]} {colors_uint8[i,2]}\n")
    
    print(f"✓ Point cloud disimpan: {filepath} ({num_points} points)")

def save_point_cloud_xyz(points, filepath):
    """
    Simpan point cloud ke format XYZ.
    
    Args:
        points: numpy array (N, 3)
        filepath: path output
    """
    np.savetxt(filepath, points, fmt='%.6f', delimiter=' ')
    print(f"✓ Point cloud disimpan: {filepath}")

def save_point_cloud_pcd(points, colors, filepath):
    """
    Simpan point cloud ke format PCD (Point Cloud Data).
    
    Args:
        points: numpy array (N, 3)
        colors: numpy array (N, 3) normalized 0-1
        filepath: path output
    """
    num_points = len(points)
    
    with open(filepath, 'w') as f:
        # Header
        f.write("# .PCD v0.7 - Point Cloud Data file format\n")
        f.write("VERSION 0.7\n")
        f.write("FIELDS x y z rgb\n")
        f.write("SIZE 4 4 4 4\n")
        f.write("TYPE F F F F\n")
        f.write("COUNT 1 1 1 1\n")
        f.write(f"WIDTH {num_points}\n")
        f.write("HEIGHT 1\n")
        f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        f.write(f"POINTS {num_points}\n")
        f.write("DATA ascii\n")
        
        # Convert colors to packed RGB float
        colors_uint8 = (colors * 255).astype(np.uint8)
        
        for i in range(num_points):
            # Pack RGB into single float
            rgb = (int(colors_uint8[i,0]) << 16) | (int(colors_uint8[i,1]) << 8) | int(colors_uint8[i,2])
            rgb_float = float(rgb)
            
            f.write(f"{points[i,0]:.6f} {points[i,1]:.6f} {points[i,2]:.6f} {rgb_float}\n")
    
    print(f"✓ Point cloud disimpan: {filepath}")

def generate_depth_image(shape, width=640, height=480):
    """
    Generate depth image sintetis.
    
    Args:
        shape: 'sphere', 'cube', 'plane'
        width, height: ukuran image
    
    Returns:
        depth: numpy array (H, W) uint16
    """
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)
    
    if shape == 'sphere':
        # Depth of sphere centered at z=2
        R2 = X**2 + Y**2
        mask = R2 < 1
        Z = np.zeros_like(R2)
        Z[mask] = np.sqrt(1 - R2[mask])
        depth = 2 - Z  # Closer = smaller depth value
        depth[~mask] = 0  # Background
        
    elif shape == 'cube':
        # Simplified cube front face
        mask = (np.abs(X) < 0.5) & (np.abs(Y) < 0.5)
        depth = np.ones_like(X) * 2
        depth[mask] = 1.5
        depth[~mask] = 0
        
    elif shape == 'plane':
        # Tilted plane
        depth = 2 - 0.3 * X - 0.2 * Y
        
    elif shape == 'room':
        # Simple room with floor and back wall
        depth = np.ones_like(X) * 5  # Back wall
        
        # Floor (lower half)
        floor_mask = Y > 0
        depth[floor_mask] = 3 - Y[floor_mask]
        
        # Add some objects
        obj1_mask = (X > -0.3) & (X < 0) & (Y > 0) & (Y < 0.5)
        depth[obj1_mask] = 1.5
        
        obj2_mask = (X > 0.2) & (X < 0.5) & (Y > 0.2) & (Y < 0.6)
        depth[obj2_mask] = 2.0
    
    else:
        depth = np.random.uniform(1, 3, (height, width))
    
    # Normalize to uint16 (0-65535)
    depth_normalized = (depth / depth.max() * 65535).astype(np.uint16)
    
    return depth_normalized

def save_depth_image_png(depth, filepath):
    """
    Simpan depth image ke PNG 16-bit.
    
    Args:
        depth: numpy array uint16
        filepath: path output
    """
    try:
        import cv2
        cv2.imwrite(str(filepath), depth)
        print(f"✓ Depth image disimpan: {filepath}")
    except ImportError:
        # Fallback menggunakan raw save
        depth.tofile(str(filepath).replace('.png', '.raw'))
        print(f"✓ Depth image disimpan (raw): {filepath}")

def generate_simple_mesh(name):
    """
    Generate mesh sederhana.
    
    Args:
        name: 'cube', 'tetrahedron', 'pyramid'
    
    Returns:
        vertices: list of (x, y, z)
        faces: list of (v1, v2, v3)
    """
    if name == 'cube':
        vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),  # Back
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)       # Front
        ]
        faces = [
            (0, 1, 2), (0, 2, 3),  # Back
            (4, 6, 5), (4, 7, 6),  # Front
            (0, 4, 5), (0, 5, 1),  # Bottom
            (2, 6, 7), (2, 7, 3),  # Top
            (0, 3, 7), (0, 7, 4),  # Left
            (1, 5, 6), (1, 6, 2)   # Right
        ]
    elif name == 'tetrahedron':
        vertices = [
            (1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)
        ]
        faces = [
            (0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)
        ]
    elif name == 'pyramid':
        vertices = [
            (0, 1, 0),      # Top
            (-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)  # Base
        ]
        faces = [
            (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1),  # Sides
            (1, 4, 3), (1, 3, 2)  # Base
        ]
    else:
        raise ValueError(f"Unknown mesh: {name}")
    
    return vertices, faces

def save_mesh_obj(vertices, faces, filepath):
    """
    Simpan mesh ke format OBJ.
    
    Args:
        vertices: list of (x, y, z)
        faces: list of (v1, v2, v3) - 0-indexed
        filepath: path output
    """
    with open(filepath, 'w') as f:
        f.write("# OBJ file generated by download_sample_data.py\n")
        
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        
        for face in faces:
            # OBJ uses 1-indexed
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
    
    print(f"✓ Mesh disimpan: {filepath}")

def save_mesh_stl(vertices, faces, filepath):
    """
    Simpan mesh ke format STL (ASCII).
    
    Args:
        vertices: list of (x, y, z)
        faces: list of (v1, v2, v3) - 0-indexed
        filepath: path output
    """
    vertices = np.array(vertices)
    
    with open(filepath, 'w') as f:
        f.write("solid mesh\n")
        
        for face in faces:
            v0 = vertices[face[0]]
            v1 = vertices[face[1]]
            v2 = vertices[face[2]]
            
            # Calculate normal
            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = np.cross(edge1, edge2)
            normal = normal / np.linalg.norm(normal)
            
            f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {v0[0]:.6f} {v0[1]:.6f} {v0[2]:.6f}\n")
            f.write(f"      vertex {v1[0]:.6f} {v1[1]:.6f} {v1[2]:.6f}\n")
            f.write(f"      vertex {v2[0]:.6f} {v2[1]:.6f} {v2[2]:.6f}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        
        f.write("endsolid mesh\n")
    
    print(f"✓ Mesh disimpan: {filepath}")

# ============================================================
# FUNGSI UTAMA
# ============================================================

def main():
    """Fungsi utama untuk mengunduh dan generate sample data."""
    
    print("=" * 60)
    print("Download Sample Data - Bab 13: 3D Reconstruction")
    print("=" * 60)
    
    # 1. Buat direktori
    print("\n[1/4] Membuat struktur direktori...")
    create_directories()
    
    # 2. Generate synthetic point clouds
    print("\n[2/4] Generating synthetic point clouds...")
    
    shapes = ['sphere', 'cube', 'cylinder', 'bunny_approx']
    
    for shape in shapes:
        print(f"\n  Generating {shape}...")
        points, colors = generate_synthetic_point_cloud(shape, num_points=50000)
        
        # Save in multiple formats
        save_point_cloud_ply(points, colors, POINT_CLOUD_DIR / f"{shape}.ply")
        save_point_cloud_xyz(points, POINT_CLOUD_DIR / f"{shape}.xyz")
        save_point_cloud_pcd(points, colors, POINT_CLOUD_DIR / f"{shape}.pcd")
    
    # Generate noisy version for testing
    print("\n  Generating noisy point cloud...")
    points, colors = generate_synthetic_point_cloud('sphere', num_points=30000)
    noise = np.random.normal(0, 0.02, points.shape)  # More noise
    points_noisy = points + noise.astype(np.float32)
    
    # Add outliers
    num_outliers = 500
    outliers = np.random.uniform(-1.5, 1.5, (num_outliers, 3)).astype(np.float32)
    outlier_colors = np.zeros((num_outliers, 3), dtype=np.float32)
    
    points_with_outliers = np.vstack([points_noisy, outliers])
    colors_with_outliers = np.vstack([colors, outlier_colors])
    
    save_point_cloud_ply(points_with_outliers, colors_with_outliers, 
                         POINT_CLOUD_DIR / "sphere_noisy.ply")
    
    # 3. Generate depth images
    print("\n[3/4] Generating synthetic depth images...")
    
    depth_shapes = ['sphere', 'cube', 'plane', 'room']
    
    for shape in depth_shapes:
        depth = generate_depth_image(shape)
        save_depth_image_png(depth, DEPTH_DIR / f"depth_{shape}.png")
        
        # Also save as numpy
        np.save(DEPTH_DIR / f"depth_{shape}.npy", depth)
    
    # 4. Generate simple meshes
    print("\n[4/4] Generating simple meshes...")
    
    mesh_names = ['cube', 'tetrahedron', 'pyramid']
    
    for mesh_name in mesh_names:
        vertices, faces = generate_simple_mesh(mesh_name)
        save_mesh_obj(vertices, faces, MESH_DIR / f"{mesh_name}.obj")
        save_mesh_stl(vertices, faces, MESH_DIR / f"{mesh_name}.stl")
    
    # Print summary
    print("\n" + "=" * 60)
    print("RINGKASAN DATA YANG DIGENERATE")
    print("=" * 60)
    
    print(f"\n📁 Point Clouds ({POINT_CLOUD_DIR}):")
    for f in POINT_CLOUD_DIR.glob("*"):
        size = f.stat().st_size / 1024
        print(f"   • {f.name}: {size:.1f} KB")
    
    print(f"\n📁 Depth Images ({DEPTH_DIR}):")
    for f in DEPTH_DIR.glob("*"):
        size = f.stat().st_size / 1024
        print(f"   • {f.name}: {size:.1f} KB")
    
    print(f"\n📁 Meshes ({MESH_DIR}):")
    for f in MESH_DIR.glob("*"):
        size = f.stat().st_size / 1024
        print(f"   • {f.name}: {size:.1f} KB")
    
    print("\n✅ Sample data berhasil digenerate!")
    print("\nCatatan:")
    print("  - Point clouds tersedia dalam format PLY, PCD, dan XYZ")
    print("  - Depth images tersedia dalam format PNG dan NPY")
    print("  - Meshes tersedia dalam format OBJ dan STL")
    print("  - sphere_noisy.ply berisi noise dan outlier untuk testing filtering")

if __name__ == "__main__":
    main()
