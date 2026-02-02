"""
Praktikum 09: Motion Estimation
================================
Implementasi berbagai teknik motion estimation dan optical flow.

Topik:
1. Block Matching
2. Lucas-Kanade Optical Flow
3. Horn-Schunck Optical Flow
4. Dense Optical Flow (Farneback)
5. Deep Optical Flow (RAFT/PWC-Net)
6. Motion Visualization

Requirements:
- opencv-contrib-python
- numpy
- matplotlib
- torch (optional, untuk deep learning)
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
from dataclasses import dataclass

# ============================================================================
# BAGIAN 1: BLOCK MATCHING
# ============================================================================

class BlockMatcher:
    """
    Block matching untuk motion estimation.
    """
    
    def __init__(self, block_size: int = 16, search_range: int = 16):
        """
        Args:
            block_size: Ukuran block (pixel)
            search_range: Range pencarian (pixel)
        """
        self.block_size = block_size
        self.search_range = search_range
    
    def sad(self, block1: np.ndarray, block2: np.ndarray) -> float:
        """Sum of Absolute Differences."""
        return np.sum(np.abs(block1.astype(float) - block2.astype(float)))
    
    def ssd(self, block1: np.ndarray, block2: np.ndarray) -> float:
        """Sum of Squared Differences."""
        diff = block1.astype(float) - block2.astype(float)
        return np.sum(diff ** 2)
    
    def full_search(self, ref_frame: np.ndarray, curr_frame: np.ndarray,
                   metric: str = 'sad') -> np.ndarray:
        """
        Full search block matching.
        
        Args:
            ref_frame: Reference frame
            curr_frame: Current frame
            metric: 'sad' atau 'ssd'
            
        Returns:
            motion_vectors: Array of (mv_x, mv_y) per block
        """
        if len(ref_frame.shape) == 3:
            ref_frame = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        h, w = ref_frame.shape
        bs = self.block_size
        sr = self.search_range
        
        # Number of blocks
        n_blocks_y = h // bs
        n_blocks_x = w // bs
        
        motion_vectors = np.zeros((n_blocks_y, n_blocks_x, 2), dtype=np.float32)
        
        metric_func = self.sad if metric == 'sad' else self.ssd
        
        for by in range(n_blocks_y):
            for bx in range(n_blocks_x):
                # Current block position
                y = by * bs
                x = bx * bs
                
                curr_block = curr_frame[y:y+bs, x:x+bs]
                
                best_mv = (0, 0)
                best_cost = float('inf')
                
                # Search dalam range
                for dy in range(-sr, sr + 1):
                    for dx in range(-sr, sr + 1):
                        # Reference position
                        ref_y = y + dy
                        ref_x = x + dx
                        
                        # Check bounds
                        if (ref_y < 0 or ref_y + bs > h or
                            ref_x < 0 or ref_x + bs > w):
                            continue
                        
                        ref_block = ref_frame[ref_y:ref_y+bs, ref_x:ref_x+bs]
                        cost = metric_func(curr_block, ref_block)
                        
                        if cost < best_cost:
                            best_cost = cost
                            best_mv = (dx, dy)
                
                motion_vectors[by, bx] = best_mv
        
        return motion_vectors
    
    def three_step_search(self, ref_frame: np.ndarray, curr_frame: np.ndarray
                          ) -> np.ndarray:
        """
        Three Step Search algorithm.
        """
        if len(ref_frame.shape) == 3:
            ref_frame = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        h, w = ref_frame.shape
        bs = self.block_size
        
        n_blocks_y = h // bs
        n_blocks_x = w // bs
        
        motion_vectors = np.zeros((n_blocks_y, n_blocks_x, 2), dtype=np.float32)
        
        for by in range(n_blocks_y):
            for bx in range(n_blocks_x):
                y = by * bs
                x = bx * bs
                
                curr_block = curr_frame[y:y+bs, x:x+bs]
                
                # Initial step size
                step = self.search_range // 2
                center_y, center_x = 0, 0
                
                while step >= 1:
                    best_mv = (center_x, center_y)
                    best_cost = float('inf')
                    
                    # Search 9 points
                    for dy in [-step, 0, step]:
                        for dx in [-step, 0, step]:
                            mv_y = center_y + dy
                            mv_x = center_x + dx
                            
                            ref_y = y + mv_y
                            ref_x = x + mv_x
                            
                            if (ref_y < 0 or ref_y + bs > h or
                                ref_x < 0 or ref_x + bs > w):
                                continue
                            
                            ref_block = ref_frame[ref_y:ref_y+bs, ref_x:ref_x+bs]
                            cost = self.sad(curr_block, ref_block)
                            
                            if cost < best_cost:
                                best_cost = cost
                                best_mv = (mv_x, mv_y)
                    
                    center_x, center_y = best_mv
                    step //= 2
                
                motion_vectors[by, bx] = [center_x, center_y]
        
        return motion_vectors
    
    def diamond_search(self, ref_frame: np.ndarray, curr_frame: np.ndarray
                      ) -> np.ndarray:
        """
        Diamond Search algorithm.
        """
        if len(ref_frame.shape) == 3:
            ref_frame = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        h, w = ref_frame.shape
        bs = self.block_size
        
        # Large Diamond Search Pattern (LDSP)
        ldsp = [(0, -2), (-1, -1), (1, -1), (-2, 0), (2, 0),
                (-1, 1), (1, 1), (0, 2), (0, 0)]
        
        # Small Diamond Search Pattern (SDSP)
        sdsp = [(0, -1), (-1, 0), (1, 0), (0, 1), (0, 0)]
        
        n_blocks_y = h // bs
        n_blocks_x = w // bs
        
        motion_vectors = np.zeros((n_blocks_y, n_blocks_x, 2), dtype=np.float32)
        
        for by in range(n_blocks_y):
            for bx in range(n_blocks_x):
                y = by * bs
                x = bx * bs
                
                curr_block = curr_frame[y:y+bs, x:x+bs]
                
                center_x, center_y = 0, 0
                use_small = False
                
                max_iters = 50
                for _ in range(max_iters):
                    pattern = sdsp if use_small else ldsp
                    best_mv = (center_x, center_y)
                    best_cost = float('inf')
                    
                    for dx, dy in pattern:
                        mv_x = center_x + dx
                        mv_y = center_y + dy
                        
                        ref_y = y + mv_y
                        ref_x = x + mv_x
                        
                        if (ref_y < 0 or ref_y + bs > h or
                            ref_x < 0 or ref_x + bs > w):
                            continue
                        
                        ref_block = ref_frame[ref_y:ref_y+bs, ref_x:ref_x+bs]
                        cost = self.sad(curr_block, ref_block)
                        
                        if cost < best_cost:
                            best_cost = cost
                            best_mv = (mv_x, mv_y)
                    
                    if best_mv == (center_x, center_y):
                        if use_small:
                            break
                        else:
                            use_small = True
                    else:
                        center_x, center_y = best_mv
                
                motion_vectors[by, bx] = [center_x, center_y]
        
        return motion_vectors


def demo_block_matching():
    """Demo block matching motion estimation."""
    print("=" * 60)
    print("DEMO: Block Matching Motion Estimation")
    print("=" * 60)
    
    # Buat frame simulasi
    h, w = 256, 320
    
    # Frame 1: Background dengan objek
    frame1 = np.zeros((h, w), dtype=np.uint8)
    
    # Tambah texture
    for i in range(0, w, 20):
        for j in range(0, h, 20):
            cv2.circle(frame1, (i + 10, j + 10), 5, 100, -1)
    
    # Objek
    cv2.rectangle(frame1, (100, 80), (180, 160), 200, -1)
    
    # Frame 2: Objek bergerak
    frame2 = np.zeros((h, w), dtype=np.uint8)
    
    # Same texture
    for i in range(0, w, 20):
        for j in range(0, h, 20):
            cv2.circle(frame2, (i + 10, j + 10), 5, 100, -1)
    
    # Objek bergerak (+20, +15)
    cv2.rectangle(frame2, (120, 95), (200, 175), 200, -1)
    
    # Block matching
    matcher = BlockMatcher(block_size=16, search_range=32)
    
    print("Running Full Search...")
    mv_full = matcher.full_search(frame1, frame2)
    
    print("Running Three Step Search...")
    mv_tss = matcher.three_step_search(frame1, frame2)
    
    print("Running Diamond Search...")
    mv_diamond = matcher.diamond_search(frame1, frame2)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(frame1, cmap='gray')
    axes[0, 0].set_title('Frame 1 (Reference)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(frame2, cmap='gray')
    axes[0, 1].set_title('Frame 2 (Current)')
    axes[0, 1].axis('off')
    
    # Visualize motion vectors
    def draw_motion_vectors(ax, frame, mvs, title):
        ax.imshow(frame, cmap='gray')
        bs = matcher.block_size
        for by in range(mvs.shape[0]):
            for bx in range(mvs.shape[1]):
                cx = bx * bs + bs // 2
                cy = by * bs + bs // 2
                dx, dy = mvs[by, bx]
                
                if abs(dx) > 0.5 or abs(dy) > 0.5:
                    ax.arrow(cx, cy, dx * 2, dy * 2, 
                            head_width=3, head_length=2, fc='red', ec='red')
        
        ax.set_title(title)
        ax.axis('off')
    
    draw_motion_vectors(axes[0, 2], frame2, mv_full, 'Full Search')
    draw_motion_vectors(axes[1, 0], frame2, mv_tss, 'Three Step Search')
    draw_motion_vectors(axes[1, 1], frame2, mv_diamond, 'Diamond Search')
    
    # Difference image
    diff = cv2.absdiff(frame1, frame2)
    axes[1, 2].imshow(diff, cmap='hot')
    axes[1, 2].set_title('Difference')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_block_matching.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_block_matching.png")


# ============================================================================
# BAGIAN 2: LUCAS-KANADE OPTICAL FLOW
# ============================================================================

class LucasKanadeFlow:
    """
    Implementasi Lucas-Kanade optical flow dari scratch.
    """
    
    def __init__(self, window_size: int = 15):
        """
        Args:
            window_size: Size of the integration window
        """
        self.window_size = window_size
    
    def compute_gradients(self, img1: np.ndarray, img2: np.ndarray
                         ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute spatial and temporal gradients.
        """
        # Spatial gradients (Sobel)
        Ix = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize=3) / 8.0
        Iy = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize=3) / 8.0
        
        # Temporal gradient
        It = (img2.astype(float) - img1.astype(float))
        
        return Ix, Iy, It
    
    def compute_flow_at_point(self, Ix: np.ndarray, Iy: np.ndarray, It: np.ndarray,
                              x: int, y: int) -> Tuple[float, float]:
        """
        Compute flow at a single point using window.
        """
        half_w = self.window_size // 2
        h, w = Ix.shape
        
        # Extract window
        y_start = max(0, y - half_w)
        y_end = min(h, y + half_w + 1)
        x_start = max(0, x - half_w)
        x_end = min(w, x + half_w + 1)
        
        Ix_win = Ix[y_start:y_end, x_start:x_end].flatten()
        Iy_win = Iy[y_start:y_end, x_start:x_end].flatten()
        It_win = It[y_start:y_end, x_start:x_end].flatten()
        
        # Build system: A^T A u = -A^T b
        A = np.vstack([Ix_win, Iy_win]).T
        b = It_win
        
        ATA = A.T @ A
        ATb = A.T @ b
        
        # Check if solvable (eigenvalues)
        eigvals = np.linalg.eigvalsh(ATA)
        
        if eigvals.min() < 1e-6:
            return 0.0, 0.0
        
        # Solve
        try:
            flow = -np.linalg.solve(ATA, ATb)
            return flow[0], flow[1]
        except:
            return 0.0, 0.0
    
    def compute_dense_flow(self, img1: np.ndarray, img2: np.ndarray,
                           step: int = 1) -> np.ndarray:
        """
        Compute dense optical flow.
        
        Args:
            img1: First frame (grayscale)
            img2: Second frame (grayscale)
            step: Sampling step for dense computation
            
        Returns:
            flow: H x W x 2 flow field
        """
        if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        h, w = img1.shape
        
        # Compute gradients
        Ix, Iy, It = self.compute_gradients(img1, img2)
        
        # Compute flow
        flow = np.zeros((h, w, 2), dtype=np.float64)
        
        for y in range(0, h, step):
            for x in range(0, w, step):
                u, v = self.compute_flow_at_point(Ix, Iy, It, x, y)
                flow[y, x] = [u, v]
        
        return flow
    
    def compute_sparse_flow(self, img1: np.ndarray, img2: np.ndarray,
                           points: np.ndarray) -> np.ndarray:
        """
        Compute flow at specific points.
        
        Args:
            img1, img2: Input frames
            points: Nx2 array of (x, y) coordinates
            
        Returns:
            flow: Nx2 array of (u, v) flow vectors
        """
        if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        Ix, Iy, It = self.compute_gradients(img1, img2)
        
        flow = np.zeros((len(points), 2), dtype=np.float64)
        
        for i, (x, y) in enumerate(points):
            u, v = self.compute_flow_at_point(Ix, Iy, It, int(x), int(y))
            flow[i] = [u, v]
        
        return flow


class HornSchunckFlow:
    """
    Implementasi Horn-Schunck optical flow.
    """
    
    def __init__(self, alpha: float = 1.0, num_iterations: int = 100):
        """
        Args:
            alpha: Smoothness weight
            num_iterations: Number of iterations
        """
        self.alpha = alpha
        self.num_iterations = num_iterations
    
    def compute_flow(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        Compute dense optical flow using Horn-Schunck method.
        """
        if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        h, w = img1.shape
        
        # Compute gradients
        Ix = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize=3) / 8.0
        Iy = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize=3) / 8.0
        It = img2 - img1
        
        # Initialize flow
        u = np.zeros((h, w), dtype=np.float64)
        v = np.zeros((h, w), dtype=np.float64)
        
        # Averaging kernel for Laplacian approximation
        kernel = np.array([[0, 1/4, 0],
                          [1/4, 0, 1/4],
                          [0, 1/4, 0]], dtype=np.float64)
        
        # Iterative update
        for _ in range(self.num_iterations):
            # Compute averages (Laplacian approximation)
            u_avg = cv2.filter2D(u, -1, kernel)
            v_avg = cv2.filter2D(v, -1, kernel)
            
            # Update
            denom = self.alpha**2 + Ix**2 + Iy**2
            common = (Ix * u_avg + Iy * v_avg + It) / denom
            
            u = u_avg - Ix * common
            v = v_avg - Iy * common
        
        flow = np.dstack([u, v])
        return flow


def demo_optical_flow():
    """Demo Lucas-Kanade dan Horn-Schunck optical flow."""
    print("\n" + "=" * 60)
    print("DEMO: Optical Flow (Lucas-Kanade & Horn-Schunck)")
    print("=" * 60)
    
    # Buat synthetic sequence dengan known motion
    h, w = 200, 250
    
    # Frame 1: Circle
    frame1 = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(frame1, (100, 100), 40, 200, -1)
    
    # Add texture
    for i in range(0, w, 15):
        for j in range(0, h, 15):
            cv2.circle(frame1, (i + 7, j + 7), 3, 100, -1)
    
    # Frame 2: Circle moved
    true_motion = (8, 5)  # Known motion
    frame2 = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(frame2, (100 + true_motion[0], 100 + true_motion[1]), 40, 200, -1)
    
    # Same texture
    for i in range(0, w, 15):
        for j in range(0, h, 15):
            cv2.circle(frame2, (i + 7, j + 7), 3, 100, -1)
    
    print(f"True motion: {true_motion}")
    
    # Lucas-Kanade (custom implementation)
    print("Computing Lucas-Kanade flow...")
    lk = LucasKanadeFlow(window_size=21)
    flow_lk = lk.compute_dense_flow(frame1, frame2, step=5)
    
    # Horn-Schunck
    print("Computing Horn-Schunck flow...")
    hs = HornSchunckFlow(alpha=1.0, num_iterations=200)
    flow_hs = hs.compute_flow(frame1, frame2)
    
    # OpenCV Farneback
    print("Computing Farneback flow...")
    flow_fb = cv2.calcOpticalFlowFarneback(
        frame1, frame2, None, 0.5, 3, 15, 3, 5, 1.2, 0
    )
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(frame1, cmap='gray')
    axes[0, 0].set_title('Frame 1')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(frame2, cmap='gray')
    axes[0, 1].set_title(f'Frame 2\n(True motion: {true_motion})')
    axes[0, 1].axis('off')
    
    # Flow visualization dengan color wheel
    def flow_to_color(flow):
        h, w = flow.shape[:2]
        hsv = np.zeros((h, w, 3), dtype=np.uint8)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    axes[0, 2].imshow(flow_to_color(flow_lk))
    axes[0, 2].set_title('Lucas-Kanade (Custom)')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(flow_to_color(flow_hs))
    axes[1, 0].set_title('Horn-Schunck')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(flow_to_color(flow_fb))
    axes[1, 1].set_title('Farneback (OpenCV)')
    axes[1, 1].axis('off')
    
    # Flow arrows
    step = 10
    Y, X = np.mgrid[0:h:step, 0:w:step]
    
    axes[1, 2].imshow(frame2, cmap='gray', alpha=0.5)
    axes[1, 2].quiver(X, Y, flow_fb[::step, ::step, 0], 
                     -flow_fb[::step, ::step, 1], color='red')
    axes[1, 2].set_title('Flow Arrows (Farneback)')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_optical_flow.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_optical_flow.png")


# ============================================================================
# BAGIAN 3: OPENCV OPTICAL FLOW METHODS
# ============================================================================

class OpticalFlowMethods:
    """
    Wrapper untuk berbagai metode optical flow di OpenCV.
    """
    
    @staticmethod
    def lucas_kanade_sparse(prev_gray: np.ndarray, curr_gray: np.ndarray,
                           prev_pts: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sparse Lucas-Kanade optical flow.
        
        Args:
            prev_gray: Previous frame (grayscale)
            curr_gray: Current frame (grayscale)
            prev_pts: Points to track (Nx1x2 atau Nx2)
            
        Returns:
            curr_pts: Tracked points
            status: Status (1=success, 0=fail)
        """
        if prev_pts.ndim == 2:
            prev_pts = prev_pts.reshape(-1, 1, 2).astype(np.float32)
        
        lk_params = dict(
            winSize=(21, 21),
            maxLevel=3,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01)
        )
        
        curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(
            prev_gray, curr_gray, prev_pts, None, **lk_params
        )
        
        return curr_pts, status.ravel()
    
    @staticmethod
    def farneback_dense(prev_gray: np.ndarray, curr_gray: np.ndarray) -> np.ndarray:
        """
        Dense optical flow menggunakan Farneback's algorithm.
        """
        return cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray, None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )
    
    @staticmethod
    def dis_dense(prev_gray: np.ndarray, curr_gray: np.ndarray) -> np.ndarray:
        """
        Dense Inverse Search optical flow.
        """
        dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        return dis.calc(prev_gray, curr_gray, None)
    
    @staticmethod
    def tvl1_dense(prev_gray: np.ndarray, curr_gray: np.ndarray) -> np.ndarray:
        """
        TV-L1 optical flow (robust).
        """
        try:
            tvl1 = cv2.optflow.DualTVL1OpticalFlow_create()
            return tvl1.calc(prev_gray, curr_gray, None)
        except:
            print("TV-L1 not available, using Farneback")
            return OpticalFlowMethods.farneback_dense(prev_gray, curr_gray)


class FlowVisualizer:
    """
    Visualisasi optical flow.
    """
    
    @staticmethod
    def flow_to_color(flow: np.ndarray, max_flow: float = None) -> np.ndarray:
        """
        Convert flow ke color image (HSV color wheel).
        
        Args:
            flow: Optical flow field (HxWx2)
            max_flow: Maximum flow untuk normalisasi
            
        Returns:
            RGB image
        """
        u = flow[..., 0]
        v = flow[..., 1]
        
        mag, ang = cv2.cartToPolar(u, v)
        
        if max_flow is None:
            max_flow = np.max(mag)
        
        if max_flow > 0:
            mag = mag / max_flow
        
        hsv = np.zeros(flow.shape[:2] + (3,), dtype=np.uint8)
        hsv[..., 0] = (ang * 180 / np.pi / 2).astype(np.uint8)
        hsv[..., 1] = 255
        hsv[..., 2] = (mag * 255).clip(0, 255).astype(np.uint8)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    @staticmethod
    def draw_flow_arrows(img: np.ndarray, flow: np.ndarray, 
                        step: int = 16, scale: float = 1.0) -> np.ndarray:
        """
        Draw flow sebagai arrows.
        """
        h, w = img.shape[:2]
        
        if len(img.shape) == 2:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            vis = img.copy()
        
        for y in range(0, h, step):
            for x in range(0, w, step):
                fx, fy = flow[y, x]
                
                if abs(fx) > 0.5 or abs(fy) > 0.5:
                    cv2.arrowedLine(vis, 
                                   (x, y),
                                   (int(x + fx * scale), int(y + fy * scale)),
                                   (0, 255, 0), 1, tipLength=0.3)
        
        return vis
    
    @staticmethod
    def draw_flow_streamlines(flow: np.ndarray, density: float = 1) -> np.ndarray:
        """
        Draw flow sebagai streamlines menggunakan matplotlib.
        """
        h, w = flow.shape[:2]
        
        Y, X = np.mgrid[0:h, 0:w]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        speed = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        
        strm = ax.streamplot(X, Y, flow[..., 0], -flow[..., 1],
                            color=speed, cmap='jet', density=density,
                            linewidth=1)
        
        ax.set_xlim(0, w)
        ax.set_ylim(h, 0)
        ax.set_aspect('equal')
        plt.colorbar(strm.lines)
        
        return fig


def demo_opencv_flow():
    """Demo berbagai metode optical flow di OpenCV."""
    print("\n" + "=" * 60)
    print("DEMO: OpenCV Optical Flow Methods")
    print("=" * 60)
    
    # Buat synthetic frames
    h, w = 240, 320
    
    # Frame 1
    frame1 = np.zeros((h, w), dtype=np.uint8)
    
    # Background
    for i in range(0, w, 20):
        for j in range(0, h, 20):
            cv2.circle(frame1, (i + 10, j + 10), 4, 80, -1)
    
    # Moving objects
    cv2.rectangle(frame1, (50, 60), (120, 130), 200, -1)
    cv2.circle(frame1, (230, 120), 35, 180, -1)
    
    # Frame 2 (objects moved)
    frame2 = np.zeros((h, w), dtype=np.uint8)
    
    # Same background
    for i in range(0, w, 20):
        for j in range(0, h, 20):
            cv2.circle(frame2, (i + 10, j + 10), 4, 80, -1)
    
    # Objects dengan motion berbeda
    cv2.rectangle(frame2, (65, 70), (135, 140), 200, -1)  # (+15, +10)
    cv2.circle(frame2, (215, 130), 35, 180, -1)  # (-15, +10)
    
    # Compute flow dengan berbagai metode
    methods = [
        ('Farneback', OpticalFlowMethods.farneback_dense(frame1, frame2)),
        ('DIS', OpticalFlowMethods.dis_dense(frame1, frame2)),
    ]
    
    # Try TV-L1 if available
    try:
        flow_tvl1 = cv2.optflow.DualTVL1OpticalFlow_create().calc(frame1, frame2, None)
        methods.append(('TV-L1', flow_tvl1))
    except:
        pass
    
    # Visualize
    n_methods = len(methods)
    fig, axes = plt.subplots(2, n_methods + 1, figsize=(5 * (n_methods + 1), 10))
    
    # Input frames
    axes[0, 0].imshow(frame1, cmap='gray')
    axes[0, 0].set_title('Frame 1')
    axes[0, 0].axis('off')
    
    axes[1, 0].imshow(frame2, cmap='gray')
    axes[1, 0].set_title('Frame 2')
    axes[1, 0].axis('off')
    
    # Flow results
    visualizer = FlowVisualizer()
    
    for idx, (name, flow) in enumerate(methods):
        # Color visualization
        flow_color = visualizer.flow_to_color(flow)
        axes[0, idx + 1].imshow(flow_color)
        axes[0, idx + 1].set_title(f'{name}\n(Color)')
        axes[0, idx + 1].axis('off')
        
        # Arrow visualization
        flow_arrows = visualizer.draw_flow_arrows(frame2, flow, step=12, scale=2)
        axes[1, idx + 1].imshow(cv2.cvtColor(flow_arrows, cv2.COLOR_BGR2RGB))
        axes[1, idx + 1].set_title(f'{name}\n(Arrows)')
        axes[1, idx + 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_opencv_flow.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_opencv_flow.png")


# ============================================================================
# BAGIAN 4: MOTION SEGMENTATION
# ============================================================================

class MotionSegmentation:
    """
    Segmentasi berdasarkan motion.
    """
    
    def __init__(self, flow_method: str = 'farneback'):
        """
        Args:
            flow_method: 'farneback', 'dis', atau 'tvl1'
        """
        self.flow_method = flow_method
    
    def compute_flow(self, prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
        """Compute optical flow."""
        if len(prev.shape) == 3:
            prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
            curr = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
        
        if self.flow_method == 'farneback':
            return OpticalFlowMethods.farneback_dense(prev, curr)
        elif self.flow_method == 'dis':
            return OpticalFlowMethods.dis_dense(prev, curr)
        else:
            return OpticalFlowMethods.farneback_dense(prev, curr)
    
    def segment_by_magnitude(self, flow: np.ndarray, 
                            threshold: float = 2.0) -> np.ndarray:
        """
        Segment berdasarkan magnitude flow.
        
        Args:
            flow: Optical flow field
            threshold: Minimum magnitude untuk motion
            
        Returns:
            Binary mask (255 = motion)
        """
        mag = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        mask = (mag > threshold).astype(np.uint8) * 255
        
        # Clean up dengan morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        return mask
    
    def segment_by_direction(self, flow: np.ndarray, 
                            n_clusters: int = 3) -> np.ndarray:
        """
        Segment berdasarkan direction flow menggunakan clustering.
        
        Args:
            flow: Optical flow field
            n_clusters: Number of motion clusters
            
        Returns:
            Label map
        """
        h, w = flow.shape[:2]
        
        # Prepare features (magnitude, angle)
        mag = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        ang = np.arctan2(flow[..., 1], flow[..., 0])
        
        # Stack features
        features = np.dstack([mag, np.cos(ang), np.sin(ang)])
        features = features.reshape(-1, 3)
        
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, _ = cv2.kmeans(features.astype(np.float32), n_clusters, None,
                                  criteria, 10, cv2.KMEANS_PP_CENTERS)
        
        return labels.reshape(h, w)


def demo_motion_segmentation():
    """Demo motion segmentation."""
    print("\n" + "=" * 60)
    print("DEMO: Motion Segmentation")
    print("=" * 60)
    
    # Create frames dengan multiple moving objects
    h, w = 240, 320
    
    # Frame 1
    frame1 = np.ones((h, w, 3), dtype=np.uint8) * 50
    
    # Background texture
    for i in range(0, w, 25):
        for j in range(0, h, 25):
            cv2.circle(frame1, (i + 12, j + 12), 5, (70, 70, 70), -1)
    
    # Object 1 (moving right)
    cv2.rectangle(frame1, (40, 50), (100, 110), (0, 200, 0), -1)
    
    # Object 2 (moving left)
    cv2.circle(frame1, (250, 150), 30, (200, 0, 0), -1)
    
    # Object 3 (moving down)
    cv2.ellipse(frame1, (160, 60), (25, 15), 0, 0, 360, (0, 0, 200), -1)
    
    # Frame 2 (objects moved)
    frame2 = np.ones((h, w, 3), dtype=np.uint8) * 50
    
    # Same background
    for i in range(0, w, 25):
        for j in range(0, h, 25):
            cv2.circle(frame2, (i + 12, j + 12), 5, (70, 70, 70), -1)
    
    # Moved objects
    cv2.rectangle(frame2, (60, 50), (120, 110), (0, 200, 0), -1)  # +20, 0
    cv2.circle(frame2, (230, 150), 30, (200, 0, 0), -1)  # -20, 0
    cv2.ellipse(frame2, (160, 80), (25, 15), 0, 0, 360, (0, 0, 200), -1)  # 0, +20
    
    # Convert to grayscale untuk flow
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Compute flow
    segmenter = MotionSegmentation(flow_method='farneback')
    flow = segmenter.compute_flow(gray1, gray2)
    
    # Segmentation
    mask_mag = segmenter.segment_by_magnitude(flow, threshold=1.5)
    labels_dir = segmenter.segment_by_direction(flow, n_clusters=4)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Frame 1')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Frame 2')
    axes[0, 1].axis('off')
    
    # Flow color
    flow_color = FlowVisualizer.flow_to_color(flow)
    axes[0, 2].imshow(flow_color)
    axes[0, 2].set_title('Optical Flow')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(mask_mag, cmap='gray')
    axes[1, 0].set_title('Motion Mask\n(Magnitude Threshold)')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(labels_dir, cmap='tab10')
    axes[1, 1].set_title('Motion Clusters\n(Direction-based)')
    axes[1, 1].axis('off')
    
    # Overlay motion on frame
    overlay = frame2.copy()
    overlay[mask_mag > 0] = [0, 255, 255]
    result = cv2.addWeighted(frame2, 0.7, overlay, 0.3, 0)
    
    axes[1, 2].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('Motion Overlay')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_motion_segmentation.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_motion_segmentation.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function untuk menjalankan semua demo."""
    print("=" * 70)
    print("PRAKTIKUM 09: MOTION ESTIMATION")
    print("=" * 70)
    
    demos = [
        ("1. Block Matching", demo_block_matching),
        ("2. Optical Flow (LK & HS)", demo_optical_flow),
        ("3. OpenCV Flow Methods", demo_opencv_flow),
        ("4. Motion Segmentation", demo_motion_segmentation),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for i, (name, _) in enumerate(demos):
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
