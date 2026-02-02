"""
Praktikum 14: Image-Based Rendering
===================================
Implementasi berbagai teknik image-based rendering.

Topik:
1. View Interpolation / Morphing
2. Light Field Rendering (simplified)
3. Depth Image-Based Rendering
4. Panoramic Stitching
5. Simple Neural View Synthesis

Requirements:
- opencv-contrib-python
- numpy
- matplotlib
- scipy
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional, Dict
from scipy import interpolate
from scipy.spatial import Delaunay
import time

# ============================================================================
# BAGIAN 1: VIEW INTERPOLATION / MORPHING
# ============================================================================

class ViewMorphing:
    """
    View morphing dan interpolation antara dua gambar.
    """
    
    @staticmethod
    def find_correspondences(img1: np.ndarray, img2: np.ndarray,
                            n_points: int = 50) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find corresponding points menggunakan ORB + matching.
        
        Returns:
            pts1, pts2: Corresponding points
        """
        # Convert to grayscale
        if len(img1.shape) == 3:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            gray1, gray2 = img1, img2
        
        # ORB detector
        orb = cv2.ORB_create(n_points * 2)
        kp1, des1 = orb.detectAndCompute(gray1, None)
        kp2, des2 = orb.detectAndCompute(gray2, None)
        
        if des1 is None or des2 is None:
            return np.array([]), np.array([])
        
        # Match
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)[:n_points]
        
        pts1 = np.array([kp1[m.queryIdx].pt for m in matches])
        pts2 = np.array([kp2[m.trainIdx].pt for m in matches])
        
        return pts1, pts2
    
    @staticmethod
    def compute_triangulation(points: np.ndarray, 
                              img_shape: Tuple[int, int]) -> np.ndarray:
        """
        Compute Delaunay triangulation termasuk corner points.
        """
        h, w = img_shape[:2]
        
        # Add corner points
        corners = np.array([
            [0, 0], [w-1, 0], [0, h-1], [w-1, h-1],
            [w//2, 0], [w//2, h-1], [0, h//2], [w-1, h//2]
        ])
        
        all_points = np.vstack([points, corners])
        
        # Delaunay triangulation
        tri = Delaunay(all_points)
        
        return tri.simplices, all_points
    
    @staticmethod
    def warp_triangle(img: np.ndarray, src_tri: np.ndarray, 
                      dst_tri: np.ndarray) -> np.ndarray:
        """
        Warp triangular region.
        """
        # Bounding box
        src_rect = cv2.boundingRect(src_tri.astype(np.float32))
        dst_rect = cv2.boundingRect(dst_tri.astype(np.float32))
        
        # Offset triangle vertices
        src_tri_offset = src_tri - src_rect[:2]
        dst_tri_offset = dst_tri - dst_rect[:2]
        
        # Get affine transform
        M = cv2.getAffineTransform(src_tri_offset.astype(np.float32),
                                    dst_tri_offset.astype(np.float32))
        
        # Extract and warp
        src_patch = img[src_rect[1]:src_rect[1]+src_rect[3],
                       src_rect[0]:src_rect[0]+src_rect[2]]
        
        if src_patch.size == 0:
            return None, None
        
        warped = cv2.warpAffine(src_patch, M, (dst_rect[2], dst_rect[3]),
                                flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_REFLECT101)
        
        # Create mask
        mask = np.zeros((dst_rect[3], dst_rect[2]), dtype=np.uint8)
        cv2.fillConvexPoly(mask, dst_tri_offset.astype(np.int32), 255)
        
        return warped, mask, dst_rect
    
    def morph(self, img1: np.ndarray, img2: np.ndarray,
              pts1: np.ndarray, pts2: np.ndarray,
              t: float) -> np.ndarray:
        """
        Morph between two images.
        
        Args:
            img1, img2: Source images
            pts1, pts2: Corresponding points
            t: Interpolation factor (0 = img1, 1 = img2)
            
        Returns:
            Morphed image
        """
        if len(pts1) < 3:
            # Fallback: simple blending
            return ((1 - t) * img1 + t * img2).astype(np.uint8)
        
        # Interpolate points
        pts_mid = ((1 - t) * pts1 + t * pts2).astype(np.float32)
        
        # Triangulation on middle points
        h, w = img1.shape[:2]
        triangles, all_pts_mid = self.compute_triangulation(pts_mid, (h, w))
        
        # All points for both images
        corners = all_pts_mid[len(pts1):]
        all_pts1 = np.vstack([pts1, corners])
        all_pts2 = np.vstack([pts2, corners])
        
        # Output image
        result = np.zeros_like(img1, dtype=np.float32)
        
        for tri_idx in triangles:
            tri1 = all_pts1[tri_idx]
            tri2 = all_pts2[tri_idx]
            tri_mid = all_pts_mid[tri_idx]
            
            # Warp from img1
            warp1 = self.warp_triangle(img1, tri1, tri_mid)
            if warp1[0] is not None:
                warped1, mask1, rect1 = warp1
                
                # Warp from img2
                warp2 = self.warp_triangle(img2, tri2, tri_mid)
                if warp2[0] is not None:
                    warped2, mask2, rect2 = warp2
                    
                    # Blend
                    mask = mask1.astype(float) / 255
                    if len(img1.shape) == 3:
                        mask = mask[:, :, np.newaxis]
                    
                    blended = ((1 - t) * warped1 + t * warped2)
                    
                    # Paste to result
                    y1, y2 = rect1[1], rect1[1] + rect1[3]
                    x1, x2 = rect1[0], rect1[0] + rect1[2]
                    
                    if y2 <= h and x2 <= w:
                        region = result[y1:y2, x1:x2]
                        result[y1:y2, x1:x2] = region * (1 - mask) + blended * mask
        
        return np.clip(result, 0, 255).astype(np.uint8)


def demo_view_morphing():
    """Demo view morphing."""
    print("=" * 60)
    print("DEMO: View Morphing")
    print("=" * 60)
    
    # Create two synthetic images (views of the same "face")
    h, w = 300, 400
    
    img1 = np.zeros((h, w, 3), dtype=np.uint8)
    img1[:] = [50, 100, 150]  # Background
    
    # Face 1 (slightly left)
    cv2.ellipse(img1, (180, 150), (80, 100), 0, 0, 360, [200, 180, 160], -1)
    cv2.circle(img1, (150, 130), 15, [50, 50, 50], -1)  # Left eye
    cv2.circle(img1, (210, 130), 15, [50, 50, 50], -1)  # Right eye
    cv2.ellipse(img1, (180, 180), (30, 15), 0, 0, 180, [150, 100, 100], -1)  # Mouth
    
    img2 = np.zeros((h, w, 3), dtype=np.uint8)
    img2[:] = [50, 100, 150]
    
    # Face 2 (slightly right, different expression)
    cv2.ellipse(img2, (220, 150), (80, 100), 0, 0, 360, [200, 180, 160], -1)
    cv2.circle(img2, (190, 130), 15, [50, 50, 50], -1)
    cv2.circle(img2, (250, 130), 15, [50, 50, 50], -1)
    cv2.ellipse(img2, (220, 180), (40, 20), 0, 20, 160, [150, 100, 100], -1)  # Smile
    
    # Define correspondences manually (for demo)
    pts1 = np.array([
        [180, 80],   # Top of head
        [100, 150],  # Left edge
        [260, 150],  # Right edge
        [180, 250],  # Chin
        [150, 130],  # Left eye
        [210, 130],  # Right eye
        [180, 180],  # Mouth center
    ], dtype=np.float32)
    
    pts2 = np.array([
        [220, 80],
        [140, 150],
        [300, 150],
        [220, 250],
        [190, 130],
        [250, 130],
        [220, 180],
    ], dtype=np.float32)
    
    morpher = ViewMorphing()
    
    # Generate morph sequence
    n_frames = 5
    frames = []
    
    for i, t in enumerate(np.linspace(0, 1, n_frames)):
        morphed = morpher.morph(img1, img2, pts1, pts2, t)
        frames.append(morphed)
    
    # Visualize
    fig, axes = plt.subplots(2, n_frames, figsize=(15, 6))
    
    for i, frame in enumerate(frames):
        axes[0, i].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        axes[0, i].set_title(f't = {i/(n_frames-1):.2f}')
        axes[0, i].axis('off')
    
    # Show simple cross-fade comparison
    for i, t in enumerate(np.linspace(0, 1, n_frames)):
        crossfade = ((1-t) * img1 + t * img2).astype(np.uint8)
        axes[1, i].imshow(cv2.cvtColor(crossfade, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f'Cross-fade t={t:.2f}')
        axes[1, i].axis('off')
    
    axes[0, 0].set_ylabel('View Morphing', fontsize=12)
    axes[1, 0].set_ylabel('Simple Blend', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('output_view_morphing.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_view_morphing.png")


# ============================================================================
# BAGIAN 2: SIMPLE LIGHT FIELD RENDERING
# ============================================================================

class SimpleLightField:
    """
    Simplified light field capture dan rendering.
    """
    
    def __init__(self):
        self.images = []  # List of (image, position) tuples
        self.positions = []  # Camera positions (2D for simplicity)
    
    def add_view(self, image: np.ndarray, position: Tuple[float, float]):
        """Add a view to the light field."""
        self.images.append(image.copy())
        self.positions.append(np.array(position))
    
    def render_view(self, target_position: Tuple[float, float],
                    method: str = 'nearest') -> np.ndarray:
        """
        Render view at target position.
        
        Args:
            target_position: (x, y) position
            method: 'nearest', 'bilinear', 'weighted'
            
        Returns:
            Rendered image
        """
        if len(self.images) == 0:
            raise ValueError("No views added")
        
        target = np.array(target_position)
        
        if method == 'nearest':
            # Find nearest view
            distances = [np.linalg.norm(pos - target) for pos in self.positions]
            nearest_idx = np.argmin(distances)
            return self.images[nearest_idx].copy()
        
        elif method == 'weighted':
            # Distance-weighted blending
            result = np.zeros_like(self.images[0], dtype=np.float64)
            total_weight = 0
            
            for img, pos in zip(self.images, self.positions):
                dist = np.linalg.norm(pos - target) + 1e-10
                weight = 1.0 / (dist ** 2)
                result += weight * img
                total_weight += weight
            
            result /= total_weight
            return np.clip(result, 0, 255).astype(np.uint8)
        
        elif method == 'bilinear':
            # Find 4 nearest views untuk bilinear interpolation
            # Simplified: just use weighted average of 4 closest
            distances = [(i, np.linalg.norm(pos - target)) 
                        for i, pos in enumerate(self.positions)]
            distances.sort(key=lambda x: x[1])
            
            # Use top 4
            result = np.zeros_like(self.images[0], dtype=np.float64)
            total_weight = 0
            
            for idx, dist in distances[:4]:
                weight = 1.0 / (dist + 0.1) ** 2
                result += weight * self.images[idx]
                total_weight += weight
            
            result /= total_weight
            return np.clip(result, 0, 255).astype(np.uint8)
        
        return self.images[0].copy()
    
    def visualize_views(self):
        """Visualize captured views."""
        n = len(self.images)
        cols = min(4, n)
        rows = (n + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
        axes = np.atleast_2d(axes)
        
        for i, (img, pos) in enumerate(zip(self.images, self.positions)):
            r, c = i // cols, i % cols
            if len(img.shape) == 3:
                axes[r, c].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            else:
                axes[r, c].imshow(img, cmap='gray')
            axes[r, c].set_title(f'Pos: ({pos[0]:.1f}, {pos[1]:.1f})')
            axes[r, c].axis('off')
        
        # Hide empty subplots
        for i in range(n, rows * cols):
            r, c = i // cols, i % cols
            axes[r, c].axis('off')
        
        plt.tight_layout()
        return fig


def demo_light_field():
    """Demo simple light field rendering."""
    print("\n" + "=" * 60)
    print("DEMO: Simple Light Field")
    print("=" * 60)
    
    # Create synthetic light field (images of a cube dari berbagai sudut)
    h, w = 200, 200
    lf = SimpleLightField()
    
    # 3x3 grid of views
    for xi, x in enumerate([-0.5, 0, 0.5]):
        for yi, y in enumerate([-0.5, 0, 0.5]):
            img = np.zeros((h, w, 3), dtype=np.uint8)
            img[:] = [100, 120, 140]  # Background
            
            # Draw a simple "cube" yang shift berdasarkan position
            center_x = int(w/2 + x * 30)
            center_y = int(h/2 + y * 30)
            
            # Front face
            pts = np.array([
                [center_x - 40, center_y - 40],
                [center_x + 40, center_y - 40],
                [center_x + 40, center_y + 40],
                [center_x - 40, center_y + 40]
            ])
            cv2.fillPoly(img, [pts], [200, 150, 150])
            
            # Top face (parallelogram)
            top_pts = np.array([
                [center_x - 40, center_y - 40],
                [center_x + 40, center_y - 40],
                [center_x + 50 + int(x*10), center_y - 60 + int(y*10)],
                [center_x - 30 + int(x*10), center_y - 60 + int(y*10)]
            ])
            cv2.fillPoly(img, [top_pts], [150, 200, 150])
            
            # Right face
            right_pts = np.array([
                [center_x + 40, center_y - 40],
                [center_x + 50 + int(x*10), center_y - 60 + int(y*10)],
                [center_x + 50 + int(x*10), center_y + 20 + int(y*10)],
                [center_x + 40, center_y + 40]
            ])
            cv2.fillPoly(img, [right_pts], [150, 150, 200])
            
            lf.add_view(img, (x, y))
    
    print(f"Light field created with {len(lf.images)} views")
    
    # Render novel views
    novel_positions = [
        (0.25, 0.25),
        (-0.25, 0.25),
        (0.25, -0.25),
        (-0.25, -0.25),
        (0.1, 0.1),
        (-0.1, -0.1)
    ]
    
    # Visualize
    fig = plt.figure(figsize=(15, 10))
    
    # Original views (3x3 grid)
    for i, (img, pos) in enumerate(zip(lf.images, lf.positions)):
        ax = fig.add_subplot(4, 5, i + 1)
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.set_title(f'({pos[0]:.1f}, {pos[1]:.1f})')
        ax.axis('off')
    
    # Novel views
    for i, pos in enumerate(novel_positions):
        for j, method in enumerate(['nearest', 'weighted']):
            rendered = lf.render_view(pos, method=method)
            ax = fig.add_subplot(4, 5, 10 + i * 2 + j + 1)
            ax.imshow(cv2.cvtColor(rendered, cv2.COLOR_BGR2RGB))
            ax.set_title(f'{method}\n({pos[0]:.2f}, {pos[1]:.2f})')
            ax.axis('off')
    
    plt.suptitle('Light Field: Original Views (top) and Novel Views (bottom)', y=1.02)
    plt.tight_layout()
    plt.savefig('output_light_field.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_light_field.png")


# ============================================================================
# BAGIAN 3: DEPTH IMAGE-BASED RENDERING (DIBR)
# ============================================================================

class DIBR:
    """
    Depth Image-Based Rendering.
    """
    
    def __init__(self, intrinsics: np.ndarray):
        """
        Args:
            intrinsics: 3x3 camera intrinsic matrix
        """
        self.K = intrinsics
        self.K_inv = np.linalg.inv(intrinsics)
    
    def warp_forward(self, rgb: np.ndarray, depth: np.ndarray,
                     R: np.ndarray, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Forward warp RGB-D image ke novel view.
        
        Args:
            rgb: Source RGB image
            depth: Source depth map
            R: 3x3 rotation matrix (source to target)
            t: 3x1 translation vector
            
        Returns:
            warped_rgb, warped_depth
        """
        h, w = depth.shape
        
        # Create meshgrid
        u, v = np.meshgrid(np.arange(w), np.arange(h))
        
        # Homogeneous coordinates
        ones = np.ones_like(u)
        uv1 = np.stack([u, v, ones], axis=2)  # (H, W, 3)
        
        # Backproject to 3D
        points_3d = np.zeros((h, w, 3))
        for y in range(h):
            for x in range(w):
                if depth[y, x] > 0:
                    p = self.K_inv @ np.array([x, y, 1]) * depth[y, x]
                    points_3d[y, x] = p
        
        # Transform to new view
        points_transformed = np.zeros_like(points_3d)
        for y in range(h):
            for x in range(w):
                if depth[y, x] > 0:
                    p_new = R @ points_3d[y, x] + t.flatten()
                    points_transformed[y, x] = p_new
        
        # Project to new image
        warped_rgb = np.zeros_like(rgb)
        warped_depth = np.zeros_like(depth)
        
        for y in range(h):
            for x in range(w):
                if depth[y, x] > 0 and points_transformed[y, x, 2] > 0:
                    p_proj = self.K @ points_transformed[y, x]
                    u_new = int(p_proj[0] / p_proj[2])
                    v_new = int(p_proj[1] / p_proj[2])
                    
                    if 0 <= u_new < w and 0 <= v_new < h:
                        z_new = points_transformed[y, x, 2]
                        
                        # Z-buffer test
                        if warped_depth[v_new, u_new] == 0 or z_new < warped_depth[v_new, u_new]:
                            warped_rgb[v_new, u_new] = rgb[y, x]
                            warped_depth[v_new, u_new] = z_new
        
        return warped_rgb, warped_depth
    
    def inpaint_holes(self, image: np.ndarray, depth: np.ndarray) -> np.ndarray:
        """
        Inpaint holes in warped image.
        """
        # Create mask dari holes
        if len(image.shape) == 3:
            mask = np.all(image == 0, axis=2).astype(np.uint8) * 255
        else:
            mask = (image == 0).astype(np.uint8) * 255
        
        # Erode mask sedikit untuk menghindari edge artifacts
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        # Inpaint
        result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        
        return result


def demo_dibr():
    """Demo Depth Image-Based Rendering."""
    print("\n" + "=" * 60)
    print("DEMO: Depth Image-Based Rendering (DIBR)")
    print("=" * 60)
    
    # Create synthetic RGB-D image
    h, w = 240, 320
    
    # RGB image dengan objects
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[:] = [100, 150, 200]  # Sky/background
    
    # Ground plane
    rgb[h//2:, :] = [50, 100, 50]
    
    # Some objects
    cv2.rectangle(rgb, (50, 80), (120, 180), [200, 100, 100], -1)  # Red box (near)
    cv2.circle(rgb, (250, 140), 40, [100, 200, 100], -1)  # Green sphere (far)
    
    # Depth map
    depth = np.ones((h, w), dtype=np.float32) * 10.0  # Background at 10m
    
    # Ground plane (closer at bottom)
    for y in range(h//2, h):
        depth[y, :] = 5.0 + (y - h//2) * 0.02
    
    # Objects
    depth[80:180, 50:120] = 3.0  # Red box at 3m
    cv2.circle(depth, (250, 140), 40, 5.0, -1)  # Green sphere at 5m
    
    # Camera intrinsics
    fx = fy = 200
    cx, cy = w/2, h/2
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    
    dibr = DIBR(K)
    
    # Create different viewpoints
    translations = [
        np.array([[0.0], [0.0], [0.0]]),  # Original
        np.array([[0.3], [0.0], [0.0]]),  # Move right
        np.array([[-0.3], [0.0], [0.0]]), # Move left
        np.array([[0.0], [0.2], [0.0]]),  # Move up
    ]
    
    R = np.eye(3)  # No rotation untuk simplicity
    
    # Render novel views
    rendered_views = []
    for t in translations:
        warped_rgb, warped_depth = dibr.warp_forward(rgb, depth, R, t)
        inpainted = dibr.inpaint_holes(warped_rgb, warped_depth)
        rendered_views.append((warped_rgb, inpainted, t))
    
    # Visualize
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    
    # Row 1: Original RGB dan Depth
    axes[0, 0].imshow(cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original RGB')
    axes[0, 0].axis('off')
    
    im = axes[0, 1].imshow(depth, cmap='jet')
    axes[0, 1].set_title('Depth Map')
    axes[0, 1].axis('off')
    plt.colorbar(im, ax=axes[0, 1], fraction=0.046)
    
    axes[0, 2].axis('off')
    axes[0, 3].axis('off')
    
    # Row 2: Warped images (with holes)
    labels = ['Original', 'Right (+0.3)', 'Left (-0.3)', 'Up (+0.2)']
    for i, (warped, inpainted, t) in enumerate(rendered_views):
        axes[1, i].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f'Warped: {labels[i]}')
        axes[1, i].axis('off')
    
    # Row 3: Inpainted images
    for i, (warped, inpainted, t) in enumerate(rendered_views):
        axes[2, i].imshow(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
        axes[2, i].set_title(f'Inpainted: {labels[i]}')
        axes[2, i].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_dibr.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_dibr.png")


# ============================================================================
# BAGIAN 4: PANORAMIC STITCHING
# ============================================================================

class PanoramaStitcher:
    """
    Panoramic image stitching.
    """
    
    def __init__(self):
        self.detector = cv2.SIFT_create()
        self.matcher = cv2.BFMatcher()
    
    def find_homography(self, img1: np.ndarray, img2: np.ndarray
                       ) -> Optional[np.ndarray]:
        """
        Find homography between two images.
        
        Returns:
            3x3 homography matrix or None
        """
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Detect keypoints
        kp1, des1 = self.detector.detectAndCompute(gray1, None)
        kp2, des2 = self.detector.detectAndCompute(gray2, None)
        
        if des1 is None or des2 is None:
            return None
        
        # Match
        matches = self.matcher.knnMatch(des1, des2, k=2)
        
        # Ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        
        if len(good_matches) < 4:
            return None
        
        # Get corresponding points
        pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
        pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])
        
        # Find homography
        H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
        
        return H
    
    def stitch(self, images: List[np.ndarray]) -> np.ndarray:
        """
        Stitch multiple images into panorama.
        
        Args:
            images: List of images (left to right order)
            
        Returns:
            Stitched panorama
        """
        if len(images) < 2:
            return images[0] if images else None
        
        # Start with first image
        result = images[0]
        
        for i in range(1, len(images)):
            # Find homography
            H = self.find_homography(images[i], result)
            
            if H is None:
                print(f"Could not find homography for image {i}")
                continue
            
            # Warp and blend
            result = self._warp_and_blend(images[i], result, H)
        
        return result
    
    def _warp_and_blend(self, img: np.ndarray, canvas: np.ndarray,
                        H: np.ndarray) -> np.ndarray:
        """Warp image and blend with canvas."""
        h1, w1 = img.shape[:2]
        h2, w2 = canvas.shape[:2]
        
        # Find corners of warped image
        corners = np.float32([
            [0, 0], [w1, 0], [w1, h1], [0, h1]
        ]).reshape(-1, 1, 2)
        
        warped_corners = cv2.perspectiveTransform(corners, H)
        
        # Find bounding box
        all_corners = np.concatenate([
            warped_corners,
            np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
        ])
        
        x_min = int(min(all_corners[:, 0, 0]))
        y_min = int(min(all_corners[:, 0, 1]))
        x_max = int(max(all_corners[:, 0, 0]))
        y_max = int(max(all_corners[:, 0, 1]))
        
        # Adjust homography for translation
        T = np.array([
            [1, 0, -x_min],
            [0, 1, -y_min],
            [0, 0, 1]
        ], dtype=float)
        
        # Warp image
        new_w = x_max - x_min
        new_h = y_max - y_min
        
        result = cv2.warpPerspective(img, T @ H, (new_w, new_h))
        
        # Paste canvas
        x_offset = -x_min
        y_offset = -y_min
        
        # Create mask for blending
        mask = np.zeros((new_h, new_w), dtype=np.uint8)
        
        # Paste canvas onto result dengan simple blending
        roi = result[y_offset:y_offset+h2, x_offset:x_offset+w2]
        
        # Simple overlay (canvas overwrites where non-zero)
        gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Create blending mask
        canvas_mask = (gray_canvas > 0).astype(np.float32)
        roi_mask = (gray_roi > 0).astype(np.float32)
        
        # Blend where both have content
        overlap = canvas_mask * roi_mask
        
        for c in range(3):
            blended = np.where(overlap > 0,
                              0.5 * canvas[:, :, c] + 0.5 * roi[:, :, c],
                              np.where(canvas_mask > 0, canvas[:, :, c], roi[:, :, c]))
            result[y_offset:y_offset+h2, x_offset:x_offset+w2, c] = blended
        
        return result


def demo_panorama():
    """Demo panoramic stitching."""
    print("\n" + "=" * 60)
    print("DEMO: Panoramic Stitching")
    print("=" * 60)
    
    # Create synthetic images (overlapping views)
    h, w = 200, 300
    
    # Create a wide "scene"
    scene_w = 600
    scene = np.zeros((h, scene_w, 3), dtype=np.uint8)
    
    # Background gradient
    for x in range(scene_w):
        scene[:, x] = [100 + x//6, 150, 200 - x//6]
    
    # Some objects
    cv2.circle(scene, (100, 100), 40, [200, 100, 100], -1)
    cv2.rectangle(scene, (250, 80), (350, 180), [100, 200, 100], -1)
    cv2.ellipse(scene, (500, 120), (50, 30), 0, 0, 360, [100, 100, 200], -1)
    
    # Add texture
    for i in range(0, scene_w, 40):
        cv2.line(scene, (i, 0), (i, h), [80, 80, 80], 1)
    
    # Extract overlapping crops (simulating camera captures)
    images = []
    offsets = [0, 150, 300]
    
    for offset in offsets:
        crop = scene[:, offset:offset+w].copy()
        images.append(crop)
    
    print(f"Created {len(images)} overlapping images")
    
    # Stitch
    stitcher = PanoramaStitcher()
    
    try:
        panorama = stitcher.stitch(images)
        
        # Visualize
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        
        # Individual images
        for i, img in enumerate(images):
            axes[0, i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[0, i].set_title(f'Image {i+1}')
            axes[0, i].axis('off')
        
        # Panorama
        axes[1, 0].imshow(cv2.cvtColor(scene, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('Original Scene')
        axes[1, 0].axis('off')
        
        if panorama is not None:
            axes[1, 1].imshow(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
            axes[1, 1].set_title('Stitched Panorama')
        else:
            axes[1, 1].text(0.5, 0.5, 'Stitching failed', ha='center', va='center')
        axes[1, 1].axis('off')
        
        # OpenCV stitcher comparison
        try:
            cv_stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
            status, cv_pano = cv_stitcher.stitch(images)
            if status == cv2.Stitcher_OK:
                axes[1, 2].imshow(cv2.cvtColor(cv_pano, cv2.COLOR_BGR2RGB))
                axes[1, 2].set_title('OpenCV Stitcher')
            else:
                axes[1, 2].text(0.5, 0.5, f'OpenCV failed: {status}', ha='center', va='center')
        except:
            axes[1, 2].text(0.5, 0.5, 'OpenCV Stitcher\nnot available', ha='center', va='center')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.savefig('output_panorama.png', dpi=150)
        plt.show()
        
        print("Hasil disimpan: output_panorama.png")
        
    except Exception as e:
        print(f"Error during stitching: {e}")


# ============================================================================
# BAGIAN 5: SIMPLE IMAGE BLENDING
# ============================================================================

class ImageBlender:
    """
    Various image blending techniques untuk IBR.
    """
    
    @staticmethod
    def alpha_blend(img1: np.ndarray, img2: np.ndarray, 
                    alpha: float) -> np.ndarray:
        """Simple alpha blending."""
        return cv2.addWeighted(img1, 1-alpha, img2, alpha, 0)
    
    @staticmethod
    def laplacian_blend(img1: np.ndarray, img2: np.ndarray,
                        mask: np.ndarray, levels: int = 4) -> np.ndarray:
        """
        Laplacian pyramid blending.
        """
        # Build Gaussian pyramids
        gp1 = [img1.astype(float)]
        gp2 = [img2.astype(float)]
        gm = [mask.astype(float) / 255]
        
        for i in range(levels):
            gp1.append(cv2.pyrDown(gp1[-1]))
            gp2.append(cv2.pyrDown(gp2[-1]))
            gm.append(cv2.pyrDown(gm[-1]))
        
        # Build Laplacian pyramids
        lp1 = [gp1[-1]]
        lp2 = [gp2[-1]]
        
        for i in range(levels, 0, -1):
            size = (gp1[i-1].shape[1], gp1[i-1].shape[0])
            lp1.append(gp1[i-1] - cv2.pyrUp(gp1[i], dstsize=size))
            lp2.append(gp2[i-1] - cv2.pyrUp(gp2[i], dstsize=size))
        
        # Blend
        blended = []
        for l1, l2, m in zip(lp1, lp2, gm[::-1]):
            if len(m.shape) == 2:
                m = m[:, :, np.newaxis]
            
            # Resize mask if needed
            if m.shape[:2] != l1.shape[:2]:
                m = cv2.resize(m, (l1.shape[1], l1.shape[0]))
                if len(m.shape) == 2:
                    m = m[:, :, np.newaxis]
            
            blended.append(l1 * (1 - m) + l2 * m)
        
        # Reconstruct
        result = blended[0]
        for i in range(1, len(blended)):
            size = (blended[i].shape[1], blended[i].shape[0])
            result = cv2.pyrUp(result, dstsize=size) + blended[i]
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    @staticmethod
    def poisson_blend(src: np.ndarray, dst: np.ndarray,
                      mask: np.ndarray, center: Tuple[int, int]) -> np.ndarray:
        """
        Poisson (seamless) blending.
        """
        return cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)


def demo_blending():
    """Demo image blending techniques."""
    print("\n" + "=" * 60)
    print("DEMO: Image Blending Techniques")
    print("=" * 60)
    
    h, w = 200, 300
    
    # Create two images
    img1 = np.zeros((h, w, 3), dtype=np.uint8)
    img1[:] = [200, 100, 100]  # Red-ish
    cv2.circle(img1, (100, 100), 60, [255, 200, 200], -1)
    
    img2 = np.zeros((h, w, 3), dtype=np.uint8)
    img2[:] = [100, 100, 200]  # Blue-ish
    cv2.rectangle(img2, (150, 50), (250, 150), [200, 200, 255], -1)
    
    # Create mask (gradient for blending)
    mask = np.zeros((h, w), dtype=np.uint8)
    for x in range(w):
        mask[:, x] = int(255 * x / w)
    
    blender = ImageBlender()
    
    # Various blends
    alpha_blend = blender.alpha_blend(img1, img2, 0.5)
    laplacian_blend = blender.laplacian_blend(img1, img2, mask)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Image 1')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Image 2')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(mask, cmap='gray')
    axes[0, 2].set_title('Blend Mask')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(alpha_blend, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Alpha Blend (50%)')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(laplacian_blend, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Laplacian Pyramid Blend')
    axes[1, 1].axis('off')
    
    # Simple gradient blend
    gradient_blend = img1.copy().astype(float)
    mask_3d = mask[:, :, np.newaxis] / 255.0
    gradient_blend = (gradient_blend * (1 - mask_3d) + img2 * mask_3d).astype(np.uint8)
    
    axes[1, 2].imshow(cv2.cvtColor(gradient_blend, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('Simple Gradient Blend')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_blending.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_blending.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function."""
    print("=" * 70)
    print("PRAKTIKUM 14: IMAGE-BASED RENDERING")
    print("=" * 70)
    
    demos = [
        ("1. View Morphing", demo_view_morphing),
        ("2. Light Field", demo_light_field),
        ("3. Depth Image-Based Rendering", demo_dibr),
        ("4. Panoramic Stitching", demo_panorama),
        ("5. Image Blending", demo_blending),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for name, _ in demos:
        print(f"  {name}")
    print("  6. Jalankan Semua")
    print("  0. Keluar")
    
    while True:
        try:
            choice = input("\nMasukkan pilihan (0-6): ").strip()
            
            if choice == '0':
                print("Terima kasih!")
                break
            elif choice == '6':
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
