"""
Praktikum 13: 3D Reconstruction
===============================
Implementasi berbagai teknik rekonstruksi 3D.

Topik:
1. Point Cloud Processing
2. Surface Reconstruction (Marching Cubes)
3. TSDF Fusion
4. Simple MVS Pipeline
5. Shape from Silhouette

Requirements:
- opencv-contrib-python
- numpy
- matplotlib
- scipy
- (optional) open3d untuk visualisasi advanced
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Tuple, List, Optional, Dict
from scipy.spatial import Delaunay
from scipy import ndimage
import json

# ============================================================================
# BAGIAN 1: POINT CLOUD PROCESSING
# ============================================================================

class PointCloud:
    """
    Class untuk representasi dan processing point cloud.
    """
    
    def __init__(self, points: np.ndarray = None, colors: np.ndarray = None,
                 normals: np.ndarray = None):
        """
        Args:
            points: Nx3 array of 3D points
            colors: Nx3 array of RGB colors (0-255)
            normals: Nx3 array of normal vectors
        """
        self.points = points if points is not None else np.array([]).reshape(0, 3)
        self.colors = colors
        self.normals = normals
    
    def __len__(self):
        return len(self.points)
    
    def estimate_normals(self, k_neighbors: int = 20) -> np.ndarray:
        """
        Estimate point normals using PCA on k-nearest neighbors.
        
        Args:
            k_neighbors: Number of neighbors for normal estimation
            
        Returns:
            Nx3 array of normals
        """
        from scipy.spatial import KDTree
        
        n_points = len(self.points)
        normals = np.zeros((n_points, 3))
        
        # Build KD-tree
        tree = KDTree(self.points)
        
        for i in range(n_points):
            # Find k nearest neighbors
            _, idx = tree.query(self.points[i], k=k_neighbors)
            neighbors = self.points[idx]
            
            # PCA to find normal
            centered = neighbors - neighbors.mean(axis=0)
            cov = np.dot(centered.T, centered)
            eigenvalues, eigenvectors = np.linalg.eigh(cov)
            
            # Normal is eigenvector with smallest eigenvalue
            normals[i] = eigenvectors[:, 0]
        
        # Make normals consistent (point outward)
        # Simple heuristic: point away from centroid
        centroid = self.points.mean(axis=0)
        for i in range(n_points):
            to_point = self.points[i] - centroid
            if np.dot(normals[i], to_point) < 0:
                normals[i] = -normals[i]
        
        self.normals = normals
        return normals
    
    def downsample_voxel(self, voxel_size: float) -> 'PointCloud':
        """
        Voxel grid downsampling.
        
        Args:
            voxel_size: Size of voxel for downsampling
            
        Returns:
            Downsampled point cloud
        """
        # Compute voxel indices
        voxel_idx = np.floor(self.points / voxel_size).astype(int)
        
        # Use dictionary to accumulate points per voxel
        voxel_dict = {}
        for i, idx in enumerate(voxel_idx):
            key = tuple(idx)
            if key not in voxel_dict:
                voxel_dict[key] = {'points': [], 'colors': [], 'count': 0}
            voxel_dict[key]['points'].append(self.points[i])
            if self.colors is not None:
                voxel_dict[key]['colors'].append(self.colors[i])
            voxel_dict[key]['count'] += 1
        
        # Average points in each voxel
        new_points = []
        new_colors = []
        
        for key, data in voxel_dict.items():
            new_points.append(np.mean(data['points'], axis=0))
            if self.colors is not None:
                new_colors.append(np.mean(data['colors'], axis=0).astype(np.uint8))
        
        result = PointCloud(
            points=np.array(new_points),
            colors=np.array(new_colors) if self.colors is not None else None
        )
        
        return result
    
    def statistical_outlier_removal(self, k_neighbors: int = 20,
                                    std_ratio: float = 2.0) -> 'PointCloud':
        """
        Remove statistical outliers.
        
        Args:
            k_neighbors: Number of neighbors to analyze
            std_ratio: Standard deviation multiplier for threshold
            
        Returns:
            Filtered point cloud
        """
        from scipy.spatial import KDTree
        
        tree = KDTree(self.points)
        mean_distances = []
        
        for i in range(len(self.points)):
            distances, _ = tree.query(self.points[i], k=k_neighbors + 1)
            mean_distances.append(np.mean(distances[1:]))  # Exclude self
        
        mean_distances = np.array(mean_distances)
        global_mean = np.mean(mean_distances)
        global_std = np.std(mean_distances)
        
        threshold = global_mean + std_ratio * global_std
        mask = mean_distances < threshold
        
        result = PointCloud(
            points=self.points[mask],
            colors=self.colors[mask] if self.colors is not None else None,
            normals=self.normals[mask] if self.normals is not None else None
        )
        
        return result
    
    def save_ply(self, filename: str):
        """Save point cloud to PLY format."""
        with open(filename, 'w') as f:
            # Header
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(self.points)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            
            if self.colors is not None:
                f.write("property uchar red\n")
                f.write("property uchar green\n")
                f.write("property uchar blue\n")
            
            if self.normals is not None:
                f.write("property float nx\n")
                f.write("property float ny\n")
                f.write("property float nz\n")
            
            f.write("end_header\n")
            
            # Data
            for i in range(len(self.points)):
                line = f"{self.points[i, 0]} {self.points[i, 1]} {self.points[i, 2]}"
                
                if self.colors is not None:
                    line += f" {int(self.colors[i, 0])} {int(self.colors[i, 1])} {int(self.colors[i, 2])}"
                
                if self.normals is not None:
                    line += f" {self.normals[i, 0]} {self.normals[i, 1]} {self.normals[i, 2]}"
                
                f.write(line + "\n")
    
    @staticmethod
    def load_ply(filename: str) -> 'PointCloud':
        """Load point cloud from PLY format."""
        points = []
        colors = []
        has_color = False
        
        with open(filename, 'r') as f:
            # Skip header
            line = f.readline()
            while 'end_header' not in line:
                if 'property' in line and 'red' in line:
                    has_color = True
                line = f.readline()
            
            # Read data
            for line in f:
                parts = line.strip().split()
                points.append([float(parts[0]), float(parts[1]), float(parts[2])])
                if has_color and len(parts) >= 6:
                    colors.append([int(parts[3]), int(parts[4]), int(parts[5])])
        
        return PointCloud(
            points=np.array(points),
            colors=np.array(colors) if colors else None
        )


# ============================================================================
# BAGIAN 2: MESH REPRESENTATION
# ============================================================================

class TriangleMesh:
    """
    Triangle mesh representation.
    """
    
    def __init__(self, vertices: np.ndarray = None, faces: np.ndarray = None,
                 vertex_colors: np.ndarray = None, vertex_normals: np.ndarray = None):
        """
        Args:
            vertices: Vx3 array of vertex positions
            faces: Fx3 array of vertex indices (triangles)
            vertex_colors: Vx3 array of RGB colors
            vertex_normals: Vx3 array of normal vectors
        """
        self.vertices = vertices if vertices is not None else np.array([]).reshape(0, 3)
        self.faces = faces if faces is not None else np.array([]).reshape(0, 3)
        self.vertex_colors = vertex_colors
        self.vertex_normals = vertex_normals
    
    def compute_vertex_normals(self):
        """Compute vertex normals from face normals."""
        vertex_normals = np.zeros_like(self.vertices)
        
        for face in self.faces:
            v0, v1, v2 = self.vertices[face]
            normal = np.cross(v1 - v0, v2 - v0)
            norm = np.linalg.norm(normal)
            if norm > 0:
                normal /= norm
            
            vertex_normals[face[0]] += normal
            vertex_normals[face[1]] += normal
            vertex_normals[face[2]] += normal
        
        # Normalize
        norms = np.linalg.norm(vertex_normals, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vertex_normals /= norms
        
        self.vertex_normals = vertex_normals
    
    def get_bounding_box(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get axis-aligned bounding box."""
        if len(self.vertices) == 0:
            return np.zeros(3), np.zeros(3)
        return self.vertices.min(axis=0), self.vertices.max(axis=0)
    
    def save_obj(self, filename: str):
        """Save mesh to OBJ format."""
        with open(filename, 'w') as f:
            # Vertices
            for v in self.vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            
            # Normals
            if self.vertex_normals is not None:
                for n in self.vertex_normals:
                    f.write(f"vn {n[0]} {n[1]} {n[2]}\n")
            
            # Faces (1-indexed)
            for face in self.faces:
                if self.vertex_normals is not None:
                    f.write(f"f {face[0]+1}//{face[0]+1} {face[1]+1}//{face[1]+1} {face[2]+1}//{face[2]+1}\n")
                else:
                    f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


# ============================================================================
# BAGIAN 3: MARCHING CUBES
# ============================================================================

class MarchingCubes:
    """
    Marching Cubes algorithm untuk isosurface extraction.
    """
    
    # Edge table: untuk setiap cube configuration, edge yang diintersect
    EDGE_TABLE = [
        0x0, 0x109, 0x203, 0x30a, 0x406, 0x50f, 0x605, 0x70c,
        0x80c, 0x905, 0xa0f, 0xb06, 0xc0a, 0xd03, 0xe09, 0xf00,
        # ... (full table has 256 entries, simplified here)
    ]
    
    # Triangle table: untuk setiap configuration, vertices yang membentuk triangles
    # Simplified version - full implementation needs complete lookup tables
    
    def __init__(self, resolution: int = 64):
        """
        Args:
            resolution: Grid resolution
        """
        self.resolution = resolution
    
    def extract_surface(self, volume: np.ndarray, 
                        isovalue: float = 0.0) -> TriangleMesh:
        """
        Extract isosurface dari volumetric data.
        Simplified implementation.
        
        Args:
            volume: 3D array of values
            isovalue: Isosurface level
            
        Returns:
            Triangle mesh
        """
        vertices = []
        faces = []
        vertex_dict = {}  # untuk vertex deduplication
        
        nx, ny, nz = volume.shape
        
        # Process each cube
        for i in range(nx - 1):
            for j in range(ny - 1):
                for k in range(nz - 1):
                    # Get cube corner values
                    cube_vals = [
                        volume[i, j, k],
                        volume[i+1, j, k],
                        volume[i+1, j+1, k],
                        volume[i, j+1, k],
                        volume[i, j, k+1],
                        volume[i+1, j, k+1],
                        volume[i+1, j+1, k+1],
                        volume[i, j+1, k+1]
                    ]
                    
                    # Determine cube index
                    cube_index = 0
                    for idx, val in enumerate(cube_vals):
                        if val < isovalue:
                            cube_index |= (1 << idx)
                    
                    # Skip if entirely inside or outside
                    if cube_index == 0 or cube_index == 255:
                        continue
                    
                    # Get triangles for this configuration
                    cube_triangles = self._get_triangles(
                        cube_index, cube_vals, isovalue,
                        i, j, k
                    )
                    
                    # Add to mesh
                    for tri in cube_triangles:
                        face_indices = []
                        for v in tri:
                            v_tuple = tuple(np.round(v, 6))
                            if v_tuple not in vertex_dict:
                                vertex_dict[v_tuple] = len(vertices)
                                vertices.append(v)
                            face_indices.append(vertex_dict[v_tuple])
                        faces.append(face_indices)
        
        mesh = TriangleMesh(
            vertices=np.array(vertices) if vertices else np.array([]).reshape(0, 3),
            faces=np.array(faces) if faces else np.array([]).reshape(0, 3)
        )
        mesh.compute_vertex_normals()
        
        return mesh
    
    def _get_triangles(self, cube_index: int, cube_vals: List[float],
                       isovalue: float, i: int, j: int, k: int
                      ) -> List[List[np.ndarray]]:
        """
        Get triangles for a cube configuration.
        Simplified - uses basic interpolation.
        """
        # Cube corners
        corners = np.array([
            [i, j, k],
            [i+1, j, k],
            [i+1, j+1, k],
            [i, j+1, k],
            [i, j, k+1],
            [i+1, j, k+1],
            [i+1, j+1, k+1],
            [i, j+1, k+1]
        ], dtype=float)
        
        # Edges connect these corner pairs
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        
        # Find edge intersections
        edge_vertices = {}
        for edge_idx, (c1, c2) in enumerate(edges):
            v1, v2 = cube_vals[c1], cube_vals[c2]
            if (v1 < isovalue) != (v2 < isovalue):
                # Edge crosses isosurface
                t = (isovalue - v1) / (v2 - v1 + 1e-10)
                t = np.clip(t, 0, 1)
                vertex = corners[c1] + t * (corners[c2] - corners[c1])
                edge_vertices[edge_idx] = vertex
        
        # Create triangles (simplified - just creates triangles from edge vertices)
        # Full implementation would use lookup table
        triangles = []
        edge_list = list(edge_vertices.values())
        
        if len(edge_list) >= 3:
            # Simple triangulation
            center = np.mean(edge_list, axis=0)
            for i in range(len(edge_list)):
                v1 = edge_list[i]
                v2 = edge_list[(i + 1) % len(edge_list)]
                triangles.append([v1, v2, center])
        
        return triangles


# ============================================================================
# BAGIAN 4: TSDF FUSION
# ============================================================================

class TSDFFusion:
    """
    Truncated Signed Distance Function fusion untuk depth map integration.
    """
    
    def __init__(self, volume_size: Tuple[float, float, float],
                 resolution: int = 128, truncation: float = 0.05):
        """
        Args:
            volume_size: Physical size of volume (meters)
            resolution: Voxel resolution per dimension
            truncation: TSDF truncation distance
        """
        self.volume_size = np.array(volume_size)
        self.resolution = resolution
        self.truncation = truncation
        
        # Initialize TSDF volume
        self.tsdf = np.ones((resolution, resolution, resolution), dtype=np.float32)
        self.weights = np.zeros((resolution, resolution, resolution), dtype=np.float32)
        self.colors = np.zeros((resolution, resolution, resolution, 3), dtype=np.float32)
        
        # Voxel size
        self.voxel_size = volume_size / resolution
        
        # Volume origin (world coordinates)
        self.origin = -self.volume_size / 2
    
    def voxel_to_world(self, voxel_coords: np.ndarray) -> np.ndarray:
        """Convert voxel coordinates to world coordinates."""
        return voxel_coords * self.voxel_size + self.origin + self.voxel_size / 2
    
    def world_to_voxel(self, world_coords: np.ndarray) -> np.ndarray:
        """Convert world coordinates to voxel coordinates."""
        return ((world_coords - self.origin) / self.voxel_size).astype(int)
    
    def integrate(self, depth_map: np.ndarray, color_image: np.ndarray,
                  intrinsics: np.ndarray, extrinsics: np.ndarray):
        """
        Integrate a depth map into the TSDF volume.
        
        Args:
            depth_map: HxW depth image
            color_image: HxWx3 color image
            intrinsics: 3x3 camera intrinsic matrix
            extrinsics: 4x4 camera-to-world transformation
        """
        h, w = depth_map.shape
        fx, fy = intrinsics[0, 0], intrinsics[1, 1]
        cx, cy = intrinsics[0, 2], intrinsics[1, 2]
        
        # Camera position
        cam_pos = extrinsics[:3, 3]
        
        # For each voxel
        for i in range(self.resolution):
            for j in range(self.resolution):
                for k in range(self.resolution):
                    # Voxel center in world coordinates
                    voxel_world = self.voxel_to_world(np.array([i, j, k]))
                    
                    # Transform to camera coordinates
                    voxel_cam = np.linalg.inv(extrinsics) @ np.append(voxel_world, 1)
                    voxel_cam = voxel_cam[:3]
                    
                    # Check if in front of camera
                    if voxel_cam[2] <= 0:
                        continue
                    
                    # Project to image
                    u = int(fx * voxel_cam[0] / voxel_cam[2] + cx)
                    v = int(fy * voxel_cam[1] / voxel_cam[2] + cy)
                    
                    # Check bounds
                    if not (0 <= u < w and 0 <= v < h):
                        continue
                    
                    # Get measured depth
                    measured_depth = depth_map[v, u]
                    if measured_depth <= 0:
                        continue
                    
                    # Compute SDF
                    sdf = measured_depth - voxel_cam[2]
                    
                    # Truncate
                    if sdf < -self.truncation:
                        continue
                    
                    tsdf_val = min(1.0, sdf / self.truncation)
                    
                    # Update TSDF (running weighted average)
                    weight = 1.0
                    
                    old_tsdf = self.tsdf[i, j, k]
                    old_weight = self.weights[i, j, k]
                    
                    new_weight = old_weight + weight
                    self.tsdf[i, j, k] = (old_tsdf * old_weight + tsdf_val * weight) / new_weight
                    self.weights[i, j, k] = min(new_weight, 100)  # Cap weight
                    
                    # Update color
                    if color_image is not None:
                        color = color_image[v, u].astype(float)
                        self.colors[i, j, k] = (self.colors[i, j, k] * old_weight + color * weight) / new_weight
    
    def extract_mesh(self) -> TriangleMesh:
        """Extract triangle mesh using Marching Cubes."""
        mc = MarchingCubes(self.resolution)
        mesh = mc.extract_surface(self.tsdf, isovalue=0.0)
        
        # Scale vertices to world coordinates
        if len(mesh.vertices) > 0:
            mesh.vertices = mesh.vertices * self.voxel_size + self.origin
        
        return mesh
    
    def extract_point_cloud(self, threshold: float = 0.0) -> PointCloud:
        """Extract point cloud from TSDF zero-crossing."""
        points = []
        colors = []
        
        for i in range(1, self.resolution - 1):
            for j in range(1, self.resolution - 1):
                for k in range(1, self.resolution - 1):
                    if self.weights[i, j, k] < 1:
                        continue
                    
                    # Check for zero crossing
                    if abs(self.tsdf[i, j, k]) < threshold:
                        world_pos = self.voxel_to_world(np.array([i, j, k]))
                        points.append(world_pos)
                        colors.append(self.colors[i, j, k])
        
        return PointCloud(
            points=np.array(points) if points else np.array([]).reshape(0, 3),
            colors=np.array(colors).astype(np.uint8) if colors else None
        )


# ============================================================================
# BAGIAN 5: SHAPE FROM SILHOUETTE
# ============================================================================

class ShapeFromSilhouette:
    """
    Visual hull reconstruction from silhouettes.
    """
    
    def __init__(self, volume_size: Tuple[float, float, float],
                 resolution: int = 64):
        """
        Args:
            volume_size: Physical size of reconstruction volume
            resolution: Voxel resolution
        """
        self.volume_size = np.array(volume_size)
        self.resolution = resolution
        
        # Initialize volume (all occupied)
        self.volume = np.ones((resolution, resolution, resolution), dtype=bool)
        
        self.voxel_size = volume_size / resolution
        self.origin = -volume_size / 2
    
    def voxel_to_world(self, voxel_coords: np.ndarray) -> np.ndarray:
        """Convert voxel to world coordinates."""
        return voxel_coords * self.voxel_size + self.origin + self.voxel_size / 2
    
    def carve(self, silhouette: np.ndarray, 
              intrinsics: np.ndarray, extrinsics: np.ndarray):
        """
        Carve volume using a silhouette image.
        
        Args:
            silhouette: HxW binary mask (255 = object, 0 = background)
            intrinsics: 3x3 camera intrinsic matrix
            extrinsics: 4x4 camera-to-world transformation
        """
        h, w = silhouette.shape
        fx, fy = intrinsics[0, 0], intrinsics[1, 1]
        cx, cy = intrinsics[0, 2], intrinsics[1, 2]
        
        # Precompute all voxel centers
        for i in range(self.resolution):
            for j in range(self.resolution):
                for k in range(self.resolution):
                    if not self.volume[i, j, k]:
                        continue  # Already carved
                    
                    # Voxel center in world
                    voxel_world = self.voxel_to_world(np.array([i, j, k]))
                    
                    # Transform to camera coordinates
                    voxel_hom = np.append(voxel_world, 1)
                    voxel_cam = np.linalg.inv(extrinsics) @ voxel_hom
                    voxel_cam = voxel_cam[:3]
                    
                    # Skip if behind camera
                    if voxel_cam[2] <= 0:
                        self.volume[i, j, k] = False
                        continue
                    
                    # Project to image
                    u = int(fx * voxel_cam[0] / voxel_cam[2] + cx)
                    v = int(fy * voxel_cam[1] / voxel_cam[2] + cy)
                    
                    # Check bounds
                    if not (0 <= u < w and 0 <= v < h):
                        self.volume[i, j, k] = False
                        continue
                    
                    # Check silhouette
                    if silhouette[v, u] == 0:
                        self.volume[i, j, k] = False
    
    def get_point_cloud(self) -> PointCloud:
        """Extract point cloud from occupied voxels."""
        points = []
        
        for i in range(self.resolution):
            for j in range(self.resolution):
                for k in range(self.resolution):
                    if self.volume[i, j, k]:
                        world_pos = self.voxel_to_world(np.array([i, j, k]))
                        points.append(world_pos)
        
        return PointCloud(points=np.array(points) if points else np.array([]).reshape(0, 3))
    
    def get_volume_ratio(self) -> float:
        """Get ratio of occupied voxels."""
        return np.sum(self.volume) / self.volume.size


# ============================================================================
# BAGIAN 6: DEMOS
# ============================================================================

def demo_point_cloud():
    """Demo point cloud processing."""
    print("=" * 60)
    print("DEMO: Point Cloud Processing")
    print("=" * 60)
    
    # Create synthetic point cloud (sphere dengan noise)
    n_points = 5000
    
    # Spherical coordinates
    phi = np.random.uniform(0, 2 * np.pi, n_points)
    theta = np.random.uniform(0, np.pi, n_points)
    r = 1 + np.random.normal(0, 0.05, n_points)  # Radius with noise
    
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    
    points = np.stack([x, y, z], axis=1)
    
    # Add some outliers
    n_outliers = 100
    outliers = np.random.uniform(-2, 2, (n_outliers, 3))
    points = np.vstack([points, outliers])
    
    # Generate colors based on height
    colors = np.zeros((len(points), 3), dtype=np.uint8)
    z_norm = (points[:, 2] - points[:, 2].min()) / (points[:, 2].max() - points[:, 2].min())
    colors[:, 0] = (z_norm * 255).astype(np.uint8)  # Red channel
    colors[:, 2] = ((1 - z_norm) * 255).astype(np.uint8)  # Blue channel
    
    # Create point cloud
    pc = PointCloud(points=points, colors=colors)
    print(f"Original point cloud: {len(pc)} points")
    
    # Estimate normals
    pc.estimate_normals(k_neighbors=15)
    print("Normals estimated")
    
    # Remove outliers
    pc_filtered = pc.statistical_outlier_removal(k_neighbors=20, std_ratio=2.0)
    print(f"After outlier removal: {len(pc_filtered)} points")
    
    # Downsample
    pc_down = pc_filtered.downsample_voxel(voxel_size=0.1)
    print(f"After downsampling: {len(pc_down)} points")
    
    # Save
    pc_down.save_ply('output_point_cloud.ply')
    print("Saved: output_point_cloud.ply")
    
    # Visualize
    fig = plt.figure(figsize=(15, 5))
    
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(pc.points[::10, 0], pc.points[::10, 1], pc.points[::10, 2], 
                c=pc.colors[::10]/255, s=1)
    ax1.set_title('Original (with outliers)')
    ax1.set_xlabel('X'); ax1.set_ylabel('Y'); ax1.set_zlabel('Z')
    
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(pc_filtered.points[::10, 0], pc_filtered.points[::10, 1], 
                pc_filtered.points[::10, 2], 
                c=pc_filtered.colors[::10]/255 if pc_filtered.colors is not None else 'b', s=1)
    ax2.set_title('Outliers Removed')
    ax2.set_xlabel('X'); ax2.set_ylabel('Y'); ax2.set_zlabel('Z')
    
    ax3 = fig.add_subplot(133, projection='3d')
    if len(pc_down.points) > 0:
        ax3.scatter(pc_down.points[:, 0], pc_down.points[:, 1], pc_down.points[:, 2],
                    c=pc_down.colors/255 if pc_down.colors is not None else 'b', s=5)
    ax3.set_title('Downsampled')
    ax3.set_xlabel('X'); ax3.set_ylabel('Y'); ax3.set_zlabel('Z')
    
    plt.tight_layout()
    plt.savefig('output_point_cloud_demo.png', dpi=150)
    plt.show()
    
    print("Visualisasi disimpan: output_point_cloud_demo.png")


def demo_marching_cubes():
    """Demo marching cubes isosurface extraction."""
    print("\n" + "=" * 60)
    print("DEMO: Marching Cubes")
    print("=" * 60)
    
    # Create volumetric data (sphere SDF)
    resolution = 32
    volume = np.zeros((resolution, resolution, resolution))
    
    center = resolution // 2
    radius = resolution // 3
    
    for i in range(resolution):
        for j in range(resolution):
            for k in range(resolution):
                # Signed distance to sphere
                dist = np.sqrt((i - center)**2 + (j - center)**2 + (k - center)**2)
                volume[i, j, k] = dist - radius
    
    # Extract surface
    mc = MarchingCubes(resolution)
    mesh = mc.extract_surface(volume, isovalue=0.0)
    
    print(f"Extracted mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    
    # Normalize vertices to [-1, 1]
    if len(mesh.vertices) > 0:
        mesh.vertices = (mesh.vertices - resolution/2) / (resolution/2)
    
    # Save mesh
    mesh.save_obj('output_marching_cubes.obj')
    print("Saved: output_marching_cubes.obj")
    
    # Visualize
    fig = plt.figure(figsize=(12, 5))
    
    # Volume slice
    ax1 = fig.add_subplot(121)
    slice_idx = resolution // 2
    ax1.imshow(volume[:, :, slice_idx], cmap='RdBu')
    ax1.contour(volume[:, :, slice_idx], levels=[0], colors='black')
    ax1.set_title(f'Volume Slice (z={slice_idx})')
    ax1.set_xlabel('X'); ax1.set_ylabel('Y')
    
    # Mesh visualization
    ax2 = fig.add_subplot(122, projection='3d')
    
    if len(mesh.faces) > 0 and len(mesh.vertices) > 0:
        # Plot vertices
        ax2.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2],
                    c='blue', s=1, alpha=0.5)
        
        # Plot some faces
        for face in mesh.faces[:min(500, len(mesh.faces))]:
            triangle = mesh.vertices[face]
            tri = Poly3DCollection([triangle], alpha=0.3)
            tri.set_facecolor('cyan')
            tri.set_edgecolor('blue')
            ax2.add_collection3d(tri)
    
    ax2.set_title('Extracted Mesh')
    ax2.set_xlabel('X'); ax2.set_ylabel('Y'); ax2.set_zlabel('Z')
    
    plt.tight_layout()
    plt.savefig('output_marching_cubes_demo.png', dpi=150)
    plt.show()
    
    print("Visualisasi disimpan: output_marching_cubes_demo.png")


def demo_shape_from_silhouette():
    """Demo shape from silhouette reconstruction."""
    print("\n" + "=" * 60)
    print("DEMO: Shape from Silhouette")
    print("=" * 60)
    
    # Create synthetic silhouettes of a cube
    image_size = 256
    n_views = 8
    
    # Cube vertices
    cube_size = 0.5
    cube_vertices = cube_size * np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ])
    
    # Cube faces (for rendering silhouette)
    cube_faces = [
        [0, 1, 2, 3], [4, 5, 6, 7],
        [0, 1, 5, 4], [2, 3, 7, 6],
        [0, 3, 7, 4], [1, 2, 6, 5]
    ]
    
    # Camera intrinsics
    fx = fy = 300
    cx = cy = image_size / 2
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    
    # Initialize shape from silhouette
    sfs = ShapeFromSilhouette(
        volume_size=(2.0, 2.0, 2.0),
        resolution=64
    )
    
    silhouettes = []
    
    # Generate views around object
    for i in range(n_views):
        angle = 2 * np.pi * i / n_views
        
        # Camera position (looking at origin)
        cam_dist = 3.0
        cam_pos = np.array([
            cam_dist * np.cos(angle),
            cam_dist * np.sin(angle),
            0.5  # Slight elevation
        ])
        
        # Look-at matrix
        forward = -cam_pos / np.linalg.norm(cam_pos)
        right = np.cross([0, 0, 1], forward)
        right /= np.linalg.norm(right) + 1e-10
        up = np.cross(forward, right)
        
        R = np.stack([right, up, forward], axis=1)
        
        extrinsics = np.eye(4)
        extrinsics[:3, :3] = R
        extrinsics[:3, 3] = cam_pos
        
        # Render silhouette
        silhouette = np.zeros((image_size, image_size), dtype=np.uint8)
        
        # Project cube vertices
        for face in cube_faces:
            points_2d = []
            for vi in face:
                v = cube_vertices[vi]
                v_cam = np.linalg.inv(extrinsics) @ np.append(v, 1)
                v_cam = v_cam[:3]
                
                if v_cam[2] > 0:
                    u = int(fx * v_cam[0] / v_cam[2] + cx)
                    v_2d = int(fy * v_cam[1] / v_cam[2] + cy)
                    points_2d.append([u, v_2d])
            
            if len(points_2d) >= 3:
                pts = np.array(points_2d, dtype=np.int32)
                cv2.fillPoly(silhouette, [pts], 255)
        
        silhouettes.append(silhouette)
        
        # Carve volume
        sfs.carve(silhouette, K, extrinsics)
    
    print(f"Processed {n_views} views")
    print(f"Volume occupancy: {sfs.get_volume_ratio()*100:.1f}%")
    
    # Extract point cloud
    pc = sfs.get_point_cloud()
    print(f"Extracted {len(pc)} points")
    
    # Visualize
    fig = plt.figure(figsize=(15, 5))
    
    # Show some silhouettes
    for i, idx in enumerate([0, 2, 4, 6]):
        ax = fig.add_subplot(2, 4, i + 1)
        ax.imshow(silhouettes[idx], cmap='gray')
        ax.set_title(f'View {idx}')
        ax.axis('off')
    
    # Show reconstruction
    ax = fig.add_subplot(2, 4, (5, 8), projection='3d')
    
    if len(pc.points) > 0:
        # Subsample for visualization
        idx = np.random.choice(len(pc.points), min(5000, len(pc.points)), replace=False)
        ax.scatter(pc.points[idx, 0], pc.points[idx, 1], pc.points[idx, 2],
                   c='blue', s=1, alpha=0.5)
    
    ax.set_title('Reconstructed Visual Hull')
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    
    plt.tight_layout()
    plt.savefig('output_shape_from_silhouette.png', dpi=150)
    plt.show()
    
    print("Visualisasi disimpan: output_shape_from_silhouette.png")


def demo_tsdf_fusion():
    """Demo TSDF fusion."""
    print("\n" + "=" * 60)
    print("DEMO: TSDF Fusion")
    print("=" * 60)
    
    # Create synthetic depth maps of a sphere
    image_size = 128
    n_views = 4
    
    # Camera intrinsics
    fx = fy = 100
    cx = cy = image_size / 2
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    
    # Initialize TSDF
    tsdf = TSDFFusion(
        volume_size=(2.0, 2.0, 2.0),
        resolution=32,
        truncation=0.1
    )
    
    # Sphere parameters
    sphere_center = np.array([0, 0, 0])
    sphere_radius = 0.3
    
    depth_maps = []
    
    for view_idx in range(n_views):
        angle = 2 * np.pi * view_idx / n_views
        
        # Camera position
        cam_dist = 1.5
        cam_pos = np.array([
            cam_dist * np.cos(angle),
            cam_dist * np.sin(angle),
            0.2
        ])
        
        # Look-at matrix
        forward = -cam_pos / np.linalg.norm(cam_pos)
        right = np.cross([0, 0, 1], forward)
        right /= np.linalg.norm(right) + 1e-10
        up = np.cross(forward, right)
        
        R = np.stack([right, up, forward], axis=1)
        
        extrinsics = np.eye(4)
        extrinsics[:3, :3] = R
        extrinsics[:3, 3] = cam_pos
        
        # Render depth map (ray-sphere intersection)
        depth_map = np.zeros((image_size, image_size), dtype=np.float32)
        color_image = np.zeros((image_size, image_size, 3), dtype=np.uint8)
        
        for v in range(image_size):
            for u in range(image_size):
                # Ray direction in camera coords
                ray_dir = np.array([
                    (u - cx) / fx,
                    (v - cy) / fy,
                    1.0
                ])
                ray_dir /= np.linalg.norm(ray_dir)
                
                # Transform to world coords
                ray_dir_world = R @ ray_dir
                ray_origin = cam_pos
                
                # Ray-sphere intersection
                oc = ray_origin - sphere_center
                a = np.dot(ray_dir_world, ray_dir_world)
                b = 2 * np.dot(oc, ray_dir_world)
                c = np.dot(oc, oc) - sphere_radius ** 2
                
                discriminant = b ** 2 - 4 * a * c
                
                if discriminant > 0:
                    t = (-b - np.sqrt(discriminant)) / (2 * a)
                    if t > 0:
                        # Compute depth in camera coordinates
                        hit_point = ray_origin + t * ray_dir_world
                        hit_cam = np.linalg.inv(extrinsics) @ np.append(hit_point, 1)
                        depth_map[v, u] = hit_cam[2]
                        
                        # Simple color based on normal
                        normal = (hit_point - sphere_center) / sphere_radius
                        color = ((normal + 1) / 2 * 255).astype(np.uint8)
                        color_image[v, u] = color
        
        depth_maps.append(depth_map)
        
        # Integrate into TSDF
        tsdf.integrate(depth_map, color_image, K, extrinsics)
    
    print(f"Integrated {n_views} depth maps")
    
    # Extract point cloud
    pc = tsdf.extract_point_cloud(threshold=0.2)
    print(f"Extracted {len(pc)} points")
    
    # Visualize
    fig = plt.figure(figsize=(15, 5))
    
    # Show depth maps
    for i in range(min(4, n_views)):
        ax = fig.add_subplot(2, 4, i + 1)
        im = ax.imshow(depth_maps[i], cmap='jet')
        ax.set_title(f'Depth Map {i}')
        ax.axis('off')
        plt.colorbar(im, ax=ax, fraction=0.046)
    
    # Show TSDF slice
    ax = fig.add_subplot(2, 4, 5)
    slice_idx = tsdf.resolution // 2
    ax.imshow(tsdf.tsdf[:, :, slice_idx], cmap='RdBu', vmin=-1, vmax=1)
    ax.set_title(f'TSDF Slice (z={slice_idx})')
    ax.axis('off')
    
    # Show weight slice
    ax = fig.add_subplot(2, 4, 6)
    ax.imshow(tsdf.weights[:, :, slice_idx], cmap='hot')
    ax.set_title('Weight Slice')
    ax.axis('off')
    
    # Show reconstruction
    ax = fig.add_subplot(2, 4, (7, 8), projection='3d')
    
    if len(pc.points) > 0:
        ax.scatter(pc.points[:, 0], pc.points[:, 1], pc.points[:, 2],
                   c=pc.colors/255 if pc.colors is not None else 'blue',
                   s=5, alpha=0.7)
    
    ax.set_title('TSDF Reconstruction')
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    
    plt.tight_layout()
    plt.savefig('output_tsdf_fusion.png', dpi=150)
    plt.show()
    
    print("Visualisasi disimpan: output_tsdf_fusion.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function."""
    print("=" * 70)
    print("PRAKTIKUM 13: 3D RECONSTRUCTION")
    print("=" * 70)
    
    demos = [
        ("1. Point Cloud Processing", demo_point_cloud),
        ("2. Marching Cubes", demo_marching_cubes),
        ("3. Shape from Silhouette", demo_shape_from_silhouette),
        ("4. TSDF Fusion", demo_tsdf_fusion),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for name, _ in demos:
        print(f"  {name}")
    print("  5. Jalankan Semua")
    print("  0. Keluar")
    
    while True:
        try:
            choice = input("\nMasukkan pilihan (0-5): ").strip()
            
            if choice == '0':
                print("Terima kasih!")
                break
            elif choice == '5':
                for name, func in demos:
                    print(f"\n>>> Menjalankan {name}...")
                    func()
                break
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(demos):
                    demos[idx][1]()
                else:
                    print("Pilihan tidak valid!")
        except ValueError:
            print("Input tidak valid!")
        except KeyboardInterrupt:
            print("\nDibatalkan.")
            break


if __name__ == "__main__":
    main()
