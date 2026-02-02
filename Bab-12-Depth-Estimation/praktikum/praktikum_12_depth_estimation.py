"""
Praktikum 12: Depth Estimation
==============================
Implementasi berbagai teknik estimasi kedalaman.

Topik:
1. Stereo Matching (Block Matching, SGM)
2. Disparity to Depth Conversion
3. Monocular Depth Estimation (dengan pretrained model)
4. Depth Map Processing

Requirements:
- opencv-contrib-python
- numpy
- matplotlib
- torch (untuk deep learning models)
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional, List
from scipy import ndimage
import time

# ============================================================================
# BAGIAN 1: STEREO MATCHING - LOCAL METHODS
# ============================================================================

class StereoBlockMatching:
    """
    Stereo matching menggunakan block matching algorithms.
    """
    
    def __init__(self, block_size: int = 9, num_disparities: int = 64):
        """
        Args:
            block_size: Window size untuk matching (harus ganjil)
            num_disparities: Maximum disparity (harus kelipatan 16)
        """
        self.block_size = block_size
        self.num_disparities = num_disparities
    
    def sad_matching(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """
        Sum of Absolute Differences matching.
        
        Args:
            left, right: Stereo pair (grayscale)
            
        Returns:
            Disparity map
        """
        h, w = left.shape
        half_block = self.block_size // 2
        disparity = np.zeros((h, w), dtype=np.float32)
        
        # Padding
        left_pad = np.pad(left, half_block, mode='reflect')
        right_pad = np.pad(right, half_block, mode='reflect')
        
        for y in range(half_block, h + half_block):
            for x in range(half_block + self.num_disparities, w + half_block):
                # Reference block
                block_left = left_pad[y - half_block:y + half_block + 1,
                                     x - half_block:x + half_block + 1]
                
                min_sad = float('inf')
                best_d = 0
                
                # Search along disparity range
                for d in range(self.num_disparities):
                    block_right = right_pad[y - half_block:y + half_block + 1,
                                           x - d - half_block:x - d + half_block + 1]
                    
                    sad = np.sum(np.abs(block_left.astype(float) - block_right.astype(float)))
                    
                    if sad < min_sad:
                        min_sad = sad
                        best_d = d
                
                disparity[y - half_block, x - half_block] = best_d
        
        return disparity
    
    def ncc_matching(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """
        Normalized Cross-Correlation matching.
        """
        h, w = left.shape
        half_block = self.block_size // 2
        disparity = np.zeros((h, w), dtype=np.float32)
        
        left_pad = np.pad(left.astype(float), half_block, mode='reflect')
        right_pad = np.pad(right.astype(float), half_block, mode='reflect')
        
        for y in range(half_block, h + half_block):
            for x in range(half_block + self.num_disparities, w + half_block):
                block_left = left_pad[y - half_block:y + half_block + 1,
                                     x - half_block:x + half_block + 1]
                
                mean_left = np.mean(block_left)
                std_left = np.std(block_left) + 1e-10
                
                max_ncc = -1
                best_d = 0
                
                for d in range(self.num_disparities):
                    block_right = right_pad[y - half_block:y + half_block + 1,
                                           x - d - half_block:x - d + half_block + 1]
                    
                    mean_right = np.mean(block_right)
                    std_right = np.std(block_right) + 1e-10
                    
                    ncc = np.sum((block_left - mean_left) * (block_right - mean_right))
                    ncc /= (std_left * std_right * self.block_size ** 2)
                    
                    if ncc > max_ncc:
                        max_ncc = ncc
                        best_d = d
                
                disparity[y - half_block, x - half_block] = best_d
        
        return disparity
    
    def census_matching(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """
        Census transform based matching.
        Robust terhadap illumination changes.
        """
        h, w = left.shape
        half_block = self.block_size // 2
        
        # Compute census transforms
        census_left = self._census_transform(left, half_block)
        census_right = self._census_transform(right, half_block)
        
        disparity = np.zeros((h, w), dtype=np.float32)
        
        for y in range(half_block, h - half_block):
            for x in range(half_block + self.num_disparities, w - half_block):
                min_hamming = float('inf')
                best_d = 0
                
                for d in range(self.num_disparities):
                    # Hamming distance
                    hamming = bin(census_left[y, x] ^ census_right[y, x - d]).count('1')
                    
                    if hamming < min_hamming:
                        min_hamming = hamming
                        best_d = d
                
                disparity[y, x] = best_d
        
        return disparity
    
    def _census_transform(self, img: np.ndarray, radius: int) -> np.ndarray:
        """Compute census transform."""
        h, w = img.shape
        census = np.zeros((h, w), dtype=np.uint64)
        
        for y in range(radius, h - radius):
            for x in range(radius, w - radius):
                center = img[y, x]
                bit_string = 0
                
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        if dy == 0 and dx == 0:
                            continue
                        bit_string = (bit_string << 1) | (img[y + dy, x + dx] < center)
                
                census[y, x] = bit_string
        
        return census


# ============================================================================
# BAGIAN 2: SEMI-GLOBAL MATCHING
# ============================================================================

class SemiGlobalMatching:
    """
    Semi-Global Matching (SGM) algorithm.
    """
    
    def __init__(self, num_disparities: int = 64, block_size: int = 5,
                 P1: int = 10, P2: int = 120):
        """
        Args:
            num_disparities: Number of disparity levels
            block_size: Block size untuk cost computation
            P1: Penalty untuk small disparity change
            P2: Penalty untuk large disparity change
        """
        self.num_disparities = num_disparities
        self.block_size = block_size
        self.P1 = P1
        self.P2 = P2
    
    def compute_cost_volume(self, left: np.ndarray, right: np.ndarray
                           ) -> np.ndarray:
        """
        Compute initial cost volume menggunakan SAD.
        
        Returns:
            Cost volume of shape (H, W, num_disparities)
        """
        h, w = left.shape
        cost_volume = np.full((h, w, self.num_disparities), 
                              float('inf'), dtype=np.float32)
        
        half = self.block_size // 2
        
        left_pad = np.pad(left.astype(float), half, mode='reflect')
        right_pad = np.pad(right.astype(float), half, mode='reflect')
        
        for d in range(self.num_disparities):
            for y in range(half, h + half):
                for x in range(half + d, w + half):
                    block_l = left_pad[y-half:y+half+1, x-half:x+half+1]
                    block_r = right_pad[y-half:y+half+1, x-d-half:x-d+half+1]
                    
                    cost_volume[y-half, x-half, d] = np.sum(np.abs(block_l - block_r))
        
        return cost_volume
    
    def aggregate_cost(self, cost_volume: np.ndarray, 
                       direction: Tuple[int, int]) -> np.ndarray:
        """
        Aggregate cost sepanjang satu direction.
        
        Args:
            cost_volume: Initial cost volume
            direction: (dy, dx) direction for aggregation
            
        Returns:
            Aggregated cost volume
        """
        h, w, d = cost_volume.shape
        dy, dx = direction
        
        aggregated = np.zeros_like(cost_volume)
        
        # Determine traversal order
        if dy > 0:
            y_range = range(h)
        elif dy < 0:
            y_range = range(h - 1, -1, -1)
        else:
            y_range = range(h)
        
        if dx > 0:
            x_range = range(w)
        elif dx < 0:
            x_range = range(w - 1, -1, -1)
        else:
            x_range = range(w)
        
        for y in y_range:
            for x in x_range:
                # Previous pixel
                py, px = y - dy, x - dx
                
                if 0 <= py < h and 0 <= px < w:
                    prev = aggregated[py, px, :]
                    min_prev = np.min(prev)
                    
                    for disp in range(d):
                        candidates = [
                            prev[disp],
                            prev[max(0, disp-1)] + self.P1 if disp > 0 else float('inf'),
                            prev[min(d-1, disp+1)] + self.P1 if disp < d-1 else float('inf'),
                            min_prev + self.P2
                        ]
                        aggregated[y, x, disp] = cost_volume[y, x, disp] + min(candidates) - min_prev
                else:
                    aggregated[y, x, :] = cost_volume[y, x, :]
        
        return aggregated
    
    def compute_disparity(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """
        Full SGM disparity computation.
        """
        # Initial cost volume
        cost_volume = self.compute_cost_volume(left, right)
        
        # 8 directions
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        # Aggregate along all directions
        aggregated_sum = np.zeros_like(cost_volume)
        
        for direction in directions:
            aggregated = self.aggregate_cost(cost_volume, direction)
            aggregated_sum += aggregated
        
        # Winner-take-all
        disparity = np.argmin(aggregated_sum, axis=2).astype(np.float32)
        
        return disparity


# ============================================================================
# BAGIAN 3: OPENCV STEREO METHODS
# ============================================================================

class OpenCVStereoMatcher:
    """
    Wrapper untuk OpenCV stereo matching algorithms.
    """
    
    @staticmethod
    def stereo_bm(left: np.ndarray, right: np.ndarray,
                  num_disparities: int = 64, block_size: int = 15
                 ) -> np.ndarray:
        """
        OpenCV StereoBM (Block Matching).
        """
        stereo = cv2.StereoBM_create(
            numDisparities=num_disparities,
            blockSize=block_size
        )
        disparity = stereo.compute(left, right)
        return disparity.astype(np.float32) / 16.0
    
    @staticmethod
    def stereo_sgbm(left: np.ndarray, right: np.ndarray,
                    num_disparities: int = 64, block_size: int = 5,
                    P1: int = None, P2: int = None) -> np.ndarray:
        """
        OpenCV StereoSGBM (Semi-Global Block Matching).
        """
        if P1 is None:
            P1 = 8 * 3 * block_size ** 2
        if P2 is None:
            P2 = 32 * 3 * block_size ** 2
        
        stereo = cv2.StereoSGBM_create(
            minDisparity=0,
            numDisparities=num_disparities,
            blockSize=block_size,
            P1=P1,
            P2=P2,
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32,
            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
        )
        disparity = stereo.compute(left, right)
        return disparity.astype(np.float32) / 16.0


# ============================================================================
# BAGIAN 4: DISPARITY TO DEPTH CONVERSION
# ============================================================================

class DepthEstimator:
    """
    Convert disparity to depth dan related utilities.
    """
    
    def __init__(self, focal_length: float, baseline: float):
        """
        Args:
            focal_length: Focal length in pixels
            baseline: Distance between cameras in same unit as desired depth
        """
        self.focal_length = focal_length
        self.baseline = baseline
    
    def disparity_to_depth(self, disparity: np.ndarray, 
                           min_disparity: float = 1.0) -> np.ndarray:
        """
        Convert disparity map to depth map.
        
        Z = f * B / d
        
        Args:
            disparity: Disparity map
            min_disparity: Minimum disparity to avoid division by zero
            
        Returns:
            Depth map
        """
        # Avoid division by zero
        safe_disparity = np.maximum(disparity, min_disparity)
        depth = (self.focal_length * self.baseline) / safe_disparity
        
        # Set invalid regions to 0
        depth[disparity <= 0] = 0
        
        return depth
    
    def depth_to_point_cloud(self, depth: np.ndarray, 
                             rgb: np.ndarray = None,
                             K: np.ndarray = None) -> np.ndarray:
        """
        Convert depth map to 3D point cloud.
        
        Args:
            depth: Depth map
            rgb: Optional color image
            K: Camera intrinsic matrix (3x3)
            
        Returns:
            Nx3 atau Nx6 (with colors) point cloud
        """
        h, w = depth.shape
        
        if K is None:
            cx, cy = w / 2, h / 2
            fx = fy = self.focal_length
        else:
            fx, fy = K[0, 0], K[1, 1]
            cx, cy = K[0, 2], K[1, 2]
        
        # Create meshgrid
        u, v = np.meshgrid(np.arange(w), np.arange(h))
        
        # Back-project
        Z = depth
        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy
        
        # Filter invalid points
        valid = depth > 0
        
        points = np.stack([X[valid], Y[valid], Z[valid]], axis=1)
        
        if rgb is not None:
            if len(rgb.shape) == 3:
                colors = rgb[valid]
            else:
                colors = np.stack([rgb[valid]] * 3, axis=1)
            points = np.hstack([points, colors])
        
        return points
    
    @staticmethod
    def colorize_depth(depth: np.ndarray, 
                       min_depth: float = None,
                       max_depth: float = None) -> np.ndarray:
        """
        Colorize depth map for visualization.
        
        Args:
            depth: Depth map
            min_depth, max_depth: Clipping range
            
        Returns:
            Colored depth image (H, W, 3)
        """
        if min_depth is None:
            min_depth = np.min(depth[depth > 0]) if np.any(depth > 0) else 0
        if max_depth is None:
            max_depth = np.max(depth)
        
        # Normalize
        depth_norm = (depth - min_depth) / (max_depth - min_depth + 1e-10)
        depth_norm = np.clip(depth_norm, 0, 1)
        
        # Apply colormap
        depth_colored = cv2.applyColorMap(
            (depth_norm * 255).astype(np.uint8),
            cv2.COLORMAP_MAGMA
        )
        
        # Set invalid regions to black
        depth_colored[depth <= 0] = [0, 0, 0]
        
        return depth_colored


def demo_stereo_matching():
    """Demo stereo matching algorithms."""
    print("=" * 60)
    print("DEMO: Stereo Matching")
    print("=" * 60)
    
    # Create synthetic stereo pair
    h, w = 240, 320
    
    # Create scene dengan berbagai depth
    left = np.zeros((h, w), dtype=np.uint8)
    
    # Background
    left[:] = 100
    
    # Objects at different depths
    cv2.rectangle(left, (50, 50), (150, 150), 180, -1)  # Near (large disparity)
    cv2.circle(left, (250, 120), 40, 150, -1)  # Medium depth
    cv2.rectangle(left, (180, 160), (280, 220), 120, -1)  # Far
    
    # Add texture
    noise = np.random.normal(0, 10, (h, w))
    left = np.clip(left.astype(float) + noise, 0, 255).astype(np.uint8)
    
    # Create right image (shifted)
    disparities = {
        'background': 10,
        'near': 30,
        'medium': 20,
        'far': 8
    }
    
    right = np.zeros_like(left)
    
    # Simple shift untuk demo (actual stereo would use proper projection)
    # Background
    right[:, :-disparities['background']] = left[:, disparities['background']:]
    
    # Near object with larger shift
    for y in range(50, 150):
        for x in range(50, 150):
            if x - disparities['near'] >= 0:
                right[y, x - disparities['near']] = left[y, x]
    
    # Add noise
    right = np.clip(right.astype(float) + np.random.normal(0, 5, right.shape), 0, 255).astype(np.uint8)
    
    # Apply stereo matching
    cv_matcher = OpenCVStereoMatcher()
    
    # StereoBM
    disp_bm = cv_matcher.stereo_bm(left, right, num_disparities=64, block_size=15)
    
    # StereoSGBM
    disp_sgbm = cv_matcher.stereo_sgbm(left, right, num_disparities=64, block_size=5)
    
    # Convert to depth (assume f=500, baseline=0.1m)
    depth_est = DepthEstimator(focal_length=500, baseline=0.1)
    depth_sgbm = depth_est.disparity_to_depth(disp_sgbm)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(left, cmap='gray')
    axes[0, 0].set_title('Left Image')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(right, cmap='gray')
    axes[0, 1].set_title('Right Image')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(disp_bm, cmap='jet')
    axes[0, 2].set_title('Disparity (StereoBM)')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(disp_sgbm, cmap='jet')
    axes[1, 0].set_title('Disparity (StereoSGBM)')
    axes[1, 0].axis('off')
    
    depth_colored = depth_est.colorize_depth(depth_sgbm)
    axes[1, 1].imshow(cv2.cvtColor(depth_colored, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Depth Map (colored)')
    axes[1, 1].axis('off')
    
    # Histogram of disparities
    valid_disp = disp_sgbm[disp_sgbm > 0].flatten()
    axes[1, 2].hist(valid_disp, bins=50, color='blue', alpha=0.7)
    axes[1, 2].set_xlabel('Disparity')
    axes[1, 2].set_ylabel('Count')
    axes[1, 2].set_title('Disparity Distribution')
    
    plt.tight_layout()
    plt.savefig('output_stereo_matching.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_stereo_matching.png")


# ============================================================================
# BAGIAN 5: DEPTH MAP PROCESSING
# ============================================================================

class DepthMapProcessor:
    """
    Processing dan refinement untuk depth maps.
    """
    
    @staticmethod
    def fill_holes(depth: np.ndarray, method: str = 'inpaint') -> np.ndarray:
        """
        Fill holes in depth map.
        
        Args:
            depth: Depth map dengan holes (0 atau NaN)
            method: 'inpaint', 'nearest', 'interpolate'
            
        Returns:
            Filled depth map
        """
        result = depth.copy()
        mask = (depth <= 0) | np.isnan(depth)
        
        if method == 'inpaint':
            mask_uint8 = mask.astype(np.uint8) * 255
            depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
            depth_uint8 = depth_norm.astype(np.uint8)
            
            inpainted = cv2.inpaint(depth_uint8, mask_uint8, 3, cv2.INPAINT_TELEA)
            
            # Scale back
            result = inpainted.astype(float) * (depth.max() / 255)
            
        elif method == 'nearest':
            from scipy import ndimage
            indices = ndimage.distance_transform_edt(
                mask, return_distances=False, return_indices=True
            )
            result = depth[tuple(indices)]
            
        elif method == 'interpolate':
            # Linear interpolation
            from scipy.interpolate import griddata
            h, w = depth.shape
            y, x = np.mgrid[0:h, 0:w]
            
            valid = ~mask
            points = np.stack([y[valid], x[valid]], axis=1)
            values = depth[valid]
            
            result = griddata(points, values, (y, x), method='linear')
            result[np.isnan(result)] = np.nanmean(depth)
        
        return result
    
    @staticmethod
    def bilateral_filter(depth: np.ndarray, rgb: np.ndarray = None,
                        sigma_space: float = 5, sigma_range: float = 0.1
                        ) -> np.ndarray:
        """
        Edge-preserving bilateral filtering.
        
        Args:
            depth: Depth map
            rgb: Optional guide image (for joint bilateral)
            sigma_space: Spatial sigma
            sigma_range: Range sigma
            
        Returns:
            Filtered depth map
        """
        # Normalize depth
        depth_norm = cv2.normalize(depth, None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)
        
        if rgb is not None:
            # Joint bilateral filter
            guide = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY) if len(rgb.shape) == 3 else rgb
            guide_norm = cv2.normalize(guide, None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)
            
            # Use ximgproc joint bilateral filter if available
            try:
                filtered = cv2.ximgproc.jointBilateralFilter(
                    guide_norm, depth_norm, -1, sigma_range, sigma_space
                )
            except:
                filtered = cv2.bilateralFilter(depth_norm, -1, sigma_range, sigma_space)
        else:
            filtered = cv2.bilateralFilter(depth_norm, -1, sigma_range, sigma_space)
        
        # Denormalize
        result = filtered * (depth.max() - depth.min()) + depth.min()
        
        return result
    
    @staticmethod
    def guided_filter(depth: np.ndarray, guide: np.ndarray,
                     radius: int = 4, eps: float = 0.01) -> np.ndarray:
        """
        Guided filter untuk depth refinement.
        
        Args:
            depth: Depth map to filter
            guide: Guide image (e.g., RGB)
            radius: Filter radius
            eps: Regularization parameter
            
        Returns:
            Filtered depth map
        """
        if len(guide.shape) == 3:
            guide = cv2.cvtColor(guide, cv2.COLOR_BGR2GRAY)
        
        guide = guide.astype(np.float32) / 255.0
        depth_norm = depth.astype(np.float32)
        
        # Mean filter
        mean_I = cv2.boxFilter(guide, -1, (radius, radius))
        mean_p = cv2.boxFilter(depth_norm, -1, (radius, radius))
        
        corr_I = cv2.boxFilter(guide * guide, -1, (radius, radius))
        corr_Ip = cv2.boxFilter(guide * depth_norm, -1, (radius, radius))
        
        var_I = corr_I - mean_I * mean_I
        cov_Ip = corr_Ip - mean_I * mean_p
        
        a = cov_Ip / (var_I + eps)
        b = mean_p - a * mean_I
        
        mean_a = cv2.boxFilter(a, -1, (radius, radius))
        mean_b = cv2.boxFilter(b, -1, (radius, radius))
        
        result = mean_a * guide + mean_b
        
        return result
    
    @staticmethod
    def median_filter(depth: np.ndarray, ksize: int = 5) -> np.ndarray:
        """Median filtering untuk removing outliers."""
        # Convert to uint16 untuk median filter
        depth_norm = cv2.normalize(depth, None, 0, 65535, cv2.NORM_MINMAX)
        depth_uint16 = depth_norm.astype(np.uint16)
        
        filtered = cv2.medianBlur(depth_uint16, ksize)
        
        # Convert back
        result = filtered.astype(float) * (depth.max() / 65535)
        
        return result
    
    @staticmethod
    def compute_normals(depth: np.ndarray, K: np.ndarray = None
                       ) -> np.ndarray:
        """
        Compute surface normals dari depth map.
        
        Returns:
            Normal map (H, W, 3)
        """
        h, w = depth.shape
        
        # Gradients
        dz_dx = cv2.Sobel(depth, cv2.CV_32F, 1, 0, ksize=5)
        dz_dy = cv2.Sobel(depth, cv2.CV_32F, 0, 1, ksize=5)
        
        # Normal = (-dz/dx, -dz/dy, 1) normalized
        normals = np.zeros((h, w, 3), dtype=np.float32)
        normals[:, :, 0] = -dz_dx
        normals[:, :, 1] = -dz_dy
        normals[:, :, 2] = 1
        
        # Normalize
        norm = np.linalg.norm(normals, axis=2, keepdims=True) + 1e-10
        normals = normals / norm
        
        return normals


def demo_depth_processing():
    """Demo depth map processing."""
    print("\n" + "=" * 60)
    print("DEMO: Depth Map Processing")
    print("=" * 60)
    
    # Create synthetic depth map
    h, w = 240, 320
    
    # Simulated depth dengan objects
    depth = np.ones((h, w), dtype=np.float32) * 5.0  # Background at 5m
    
    # Foreground objects
    cv2.circle(depth, (100, 120), 50, 2.0, -1)  # Close object at 2m
    cv2.rectangle(depth, (180, 80), (280, 180), 3.5, -1)  # Medium at 3.5m
    
    # Add noise
    depth += np.random.normal(0, 0.2, depth.shape)
    
    # Add holes
    hole_mask = np.random.random((h, w)) < 0.05
    depth[hole_mask] = 0
    
    # Create guide image
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[:] = [100, 120, 150]
    cv2.circle(rgb, (100, 120), 50, [200, 100, 100], -1)
    cv2.rectangle(rgb, (180, 80), (280, 180), [100, 200, 100], -1)
    
    processor = DepthMapProcessor()
    
    # Processing
    depth_filled = processor.fill_holes(depth, method='inpaint')
    depth_bilateral = processor.bilateral_filter(depth_filled, rgb)
    depth_guided = processor.guided_filter(depth_filled, rgb)
    normals = processor.compute_normals(depth_guided)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(depth, cmap='jet')
    axes[0, 0].set_title('Original Depth (with noise & holes)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(depth_filled, cmap='jet')
    axes[0, 1].set_title('Holes Filled')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(depth_bilateral, cmap='jet')
    axes[0, 2].set_title('Bilateral Filtered')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(depth_guided, cmap='jet')
    axes[1, 0].set_title('Guided Filtered')
    axes[1, 0].axis('off')
    
    # Normal map visualization
    normal_vis = (normals + 1) / 2  # Map [-1,1] to [0,1]
    axes[1, 1].imshow(normal_vis)
    axes[1, 1].set_title('Surface Normals')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('Guide Image (RGB)')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_depth_processing.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_depth_processing.png")


# ============================================================================
# BAGIAN 6: SIMPLE MONOCULAR DEPTH
# ============================================================================

class SimpleMonocularDepth:
    """
    Simple monocular depth estimation (basic approach without deep learning).
    """
    
    @staticmethod
    def depth_from_defocus(images: List[np.ndarray], 
                           focus_distances: List[float]) -> np.ndarray:
        """
        Estimate depth dari focus stack.
        
        Args:
            images: List of images dengan different focus
            focus_distances: Focus distance untuk setiap image
            
        Returns:
            Depth map (in same unit as focus_distances)
        """
        # Compute sharpness at each pixel untuk setiap image
        sharpness_stack = []
        
        for img in images:
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # Laplacian variance sebagai sharpness measure
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = cv2.GaussianBlur(np.abs(laplacian), (11, 11), 0)
            sharpness_stack.append(sharpness)
        
        sharpness_stack = np.array(sharpness_stack)
        
        # Find best focus untuk setiap pixel
        best_idx = np.argmax(sharpness_stack, axis=0)
        
        # Map ke depth
        h, w = images[0].shape[:2]
        depth = np.zeros((h, w), dtype=np.float32)
        
        for i, dist in enumerate(focus_distances):
            depth[best_idx == i] = dist
        
        return depth
    
    @staticmethod
    def depth_cues(image: np.ndarray) -> dict:
        """
        Extract monocular depth cues.
        
        Returns:
            Dict of different cue maps
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        h, w = gray.shape
        
        # 1. Vertical position cue (ground plane assumption)
        y_coords = np.tile(np.arange(h).reshape(-1, 1), (1, w))
        vertical_cue = 1 - y_coords / h  # Higher = further
        
        # 2. Texture gradient
        # Compute local variance
        mean = cv2.blur(gray.astype(float), (11, 11))
        sqr_mean = cv2.blur(gray.astype(float)**2, (11, 11))
        variance = sqr_mean - mean**2
        texture_cue = cv2.normalize(variance, None, 0, 1, cv2.NORM_MINMAX)
        
        # 3. Blur/defocus (sharper = closer, typically)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = cv2.GaussianBlur(np.abs(laplacian), (21, 21), 0)
        blur_cue = cv2.normalize(sharpness, None, 0, 1, cv2.NORM_MINMAX)
        
        # 4. Relative size (need object detection, skip for now)
        
        return {
            'vertical': vertical_cue,
            'texture': texture_cue,
            'blur': blur_cue
        }


def demo_monocular_depth_cues():
    """Demo monocular depth cues."""
    print("\n" + "=" * 60)
    print("DEMO: Monocular Depth Cues")
    print("=" * 60)
    
    # Create test image
    h, w = 300, 400
    image = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Sky (far)
    image[:100, :] = [200, 180, 150]
    
    # Ground with gradient (ground plane)
    for y in range(100, h):
        intensity = 50 + (y - 100) * 0.5
        image[y, :] = [int(intensity), int(intensity + 20), int(intensity)]
    
    # Near object (large, low in image)
    cv2.rectangle(image, (50, 200), (150, 290), [100, 150, 100], -1)
    
    # Far object (small, high in image)
    cv2.rectangle(image, (280, 80), (320, 120), [150, 100, 150], -1)
    
    # Add texture
    for i in range(0, w, 30):
        for j in range(100, h, 20):
            cv2.circle(image, (i + 15, j + 10), 2, [50, 80, 50], -1)
    
    mono_depth = SimpleMonocularDepth()
    cues = mono_depth.depth_cues(image)
    
    # Combine cues (simple weighted average)
    combined = 0.4 * cues['vertical'] + 0.3 * cues['texture'] + 0.3 * cues['blur']
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Input Image')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cues['vertical'], cmap='jet')
    axes[0, 1].set_title('Vertical Position Cue')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cues['texture'], cmap='jet')
    axes[0, 2].set_title('Texture Gradient Cue')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cues['blur'], cmap='jet')
    axes[1, 0].set_title('Blur/Sharpness Cue')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(combined, cmap='jet')
    axes[1, 1].set_title('Combined Depth Estimate')
    axes[1, 1].axis('off')
    
    # Placeholder untuk deep learning
    axes[1, 2].text(0.5, 0.5, 'Deep Learning Depth\n(requires pretrained model)',
                    ha='center', va='center', fontsize=12, transform=axes[1, 2].transAxes)
    axes[1, 2].set_title('Neural Network (placeholder)')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_monocular_cues.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_monocular_cues.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function."""
    print("=" * 70)
    print("PRAKTIKUM 12: DEPTH ESTIMATION")
    print("=" * 70)
    
    demos = [
        ("1. Stereo Matching", demo_stereo_matching),
        ("2. Depth Map Processing", demo_depth_processing),
        ("3. Monocular Depth Cues", demo_monocular_depth_cues),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for i, (name, _) in enumerate(demos):
        print(f"  {name}")
    print("  4. Jalankan Semua")
    print("  0. Keluar")
    
    while True:
        try:
            choice = input("\nMasukkan pilihan (0-4): ").strip()
            
            if choice == '0':
                print("Terima kasih!")
                break
            elif choice == '4':
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
