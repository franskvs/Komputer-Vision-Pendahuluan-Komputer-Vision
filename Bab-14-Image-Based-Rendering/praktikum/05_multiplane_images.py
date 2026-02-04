"""
Praktikum 14.5: Multiplane Images (MPI)
=======================================

Program ini mendemonstrasikan Multiplane Images:
1. MPI representation
2. Alpha compositing
3. Novel view rendering
4. Depth-aware layering

Teori:
------
Multiplane Images merepresentasikan scene sebagai
stack of RGBA layers pada berbagai depth planes.

MPI = { (Ci, αi, di) } dimana:
- Ci: RGB color
- αi: Alpha (transparency)
- di: Depth plane

Rendering: Over operator untuk compositing layers.

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import time

# ============================================================
# KONFIGURASI - Sesuaikan parameter sesuai kebutuhan
# ============================================================

# Path data
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output" / "output5"

# MPI parameters
NUM_DEPTH_PLANES = 32              # Jumlah depth planes
NEAR_DEPTH = 0.5                   # Depth terdekat
FAR_DEPTH = 100.0                  # Depth terjauh
DEPTH_SAMPLING = 'linear_disparity'  # 'linear', 'linear_disparity', 'log'

# Rendering parameters
DEFAULT_FOV = 60                   # Field of view
BASELINE_RANGE = 0.1               # Range untuk view synthesis

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat direktori output."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")

def check_opencv():
    """Periksa ketersediaan OpenCV."""
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        return True
    except ImportError:
        print("✗ OpenCV tidak terinstall!")
        return False

def generate_depth_planes(near, far, num_planes, method='linear_disparity'):
    """
    Generate depth values untuk MPI planes.
    
    Args:
        near, far: Depth range
        num_planes: Jumlah planes
        method: 'linear', 'linear_disparity', 'log'
    
    Returns:
        Array of depth values
    """
    if method == 'linear':
        depths = np.linspace(near, far, num_planes)
    elif method == 'linear_disparity':
        # Disparity linear (better untuk nearby objects)
        disparities = np.linspace(1/near, 1/far, num_planes)
        depths = 1 / disparities
    elif method == 'log':
        depths = np.logspace(np.log10(near), np.log10(far), num_planes)
    else:
        depths = np.linspace(near, far, num_planes)
    
    return depths

def create_sample_scene():
    """Buat sample scene untuk MPI."""
    import cv2
    
    h, w = 480, 640
    
    # Scene image
    image = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Background
    for y in range(h):
        gradient = int(50 + 150 * y / h)
        image[y, :] = [gradient, gradient // 2, gradient // 4]
    
    # Depth map
    depth = np.full((h, w), 50.0, dtype=np.float32)  # Background
    
    # Objects di berbagai depth
    objects = [
        # (x, y, w, h, depth, color)
        (50, 100, 150, 200, 10.0, (255, 100, 100)),    # Foreground
        (250, 150, 180, 220, 20.0, (100, 255, 100)),   # Middle
        (450, 80, 140, 300, 15.0, (100, 100, 255)),    # Middle-front
        (100, 350, 200, 100, 30.0, (255, 255, 100)),   # Mid-back
    ]
    
    for x, y, ow, oh, d, color in objects:
        x2 = min(x + ow, w)
        y2 = min(y + oh, h)
        
        image[y:y2, x:x2] = color
        depth[y:y2, x:x2] = d
        
        # Add texture
        np.random.seed(int(d * 100))
        for _ in range(50):
            tx = np.random.randint(x, x2)
            ty = np.random.randint(y, y2)
            tr = np.random.randint(3, 8)
            tc = [np.random.randint(50, 200) for _ in range(3)]
            cv2.circle(image, (tx, ty), tr, tc, -1)
    
    return image, depth

# ============================================================
# MPI REPRESENTATION
# ============================================================

def create_mpi_from_rgbd(image, depth, num_planes=32, near=0.5, far=100.0):
    """
    Create MPI dari RGBD image.
    
    Args:
        image: RGB image (H, W, 3)
        depth: Depth map (H, W)
        num_planes: Jumlah depth planes
        near, far: Depth range
    
    Returns:
        mpi: (num_planes, H, W, 4) RGBA layers
        depths: Array of depth values
    """
    h, w = image.shape[:2]
    
    # Generate depth planes
    depths = generate_depth_planes(near, far, num_planes, DEPTH_SAMPLING)
    
    # Initialize MPI
    mpi = np.zeros((num_planes, h, w, 4), dtype=np.float32)
    
    # Assign pixels ke nearest depth plane
    for i in range(num_planes):
        if i == 0:
            depth_near = 0
        else:
            depth_near = (depths[i-1] + depths[i]) / 2
        
        if i == num_planes - 1:
            depth_far = far * 2
        else:
            depth_far = (depths[i] + depths[i+1]) / 2
        
        # Mask untuk depth range ini
        mask = (depth >= depth_near) & (depth < depth_far)
        
        # Set RGBA
        mpi[i, :, :, :3][mask] = image[mask] / 255.0
        mpi[i, :, :, 3][mask] = 1.0  # Opaque
    
    return mpi, depths

def create_soft_mpi(image, depth, num_planes=32, near=0.5, far=100.0, sigma=0.5):
    """
    Create MPI dengan soft depth assignment.
    
    Args:
        image, depth, num_planes, near, far: Same as create_mpi_from_rgbd
        sigma: Smoothness of depth assignment
    
    Returns:
        mpi, depths
    """
    h, w = image.shape[:2]
    depths = generate_depth_planes(near, far, num_planes, DEPTH_SAMPLING)
    
    mpi = np.zeros((num_planes, h, w, 4), dtype=np.float32)
    
    # Soft assignment berdasarkan Gaussian
    for i, d in enumerate(depths):
        # Weight berdasarkan distance ke depth plane
        weight = np.exp(-((depth - d) ** 2) / (2 * sigma**2 * d**2))
        
        # RGBA
        mpi[i, :, :, :3] = image / 255.0 * weight[:, :, np.newaxis]
        mpi[i, :, :, 3] = weight
    
    # Normalize alpha
    total_alpha = mpi[:, :, :, 3].sum(axis=0, keepdims=True)
    total_alpha = np.maximum(total_alpha, 1e-10)
    mpi[:, :, :, 3] /= total_alpha[0]
    
    return mpi, depths

# ============================================================
# MPI RENDERING
# ============================================================

def render_mpi_view(mpi, depths, translation, focal_length=640, image_size=(640, 480)):
    """
    Render novel view dari MPI.
    
    Args:
        mpi: (num_planes, H, W, 4) MPI layers
        depths: Depth values untuk setiap plane
        translation: Camera translation [tx, ty, tz]
        focal_length: Focal length
        image_size: Output image size (w, h)
    
    Returns:
        Rendered RGB image
    """
    import cv2
    
    out_w, out_h = image_size
    num_planes = len(depths)
    
    tx, ty, tz = translation
    
    # Initialize output
    accumulated = np.zeros((out_h, out_w, 4), dtype=np.float32)
    
    # Render from back to front (far to near)
    for i in range(num_planes - 1, -1, -1):
        d = depths[i]
        layer = mpi[i]  # (H, W, 4)
        
        h_in, w_in = layer.shape[:2]
        
        # Homography untuk plane di depth d
        # H = K * [R | t] * K_inv dimana R = I untuk translation only
        
        # Simplified: shearing based on translation dan depth
        # Untuk translation tx, pixel shift = tx * f / d
        
        shift_x = tx * focal_length / d
        shift_y = ty * focal_length / d
        
        # Translation matrix
        H = np.array([
            [1, 0, shift_x],
            [0, 1, shift_y],
            [0, 0, 1]
        ], dtype=np.float32)
        
        # Warp layer
        warped = cv2.warpPerspective(layer, H, (out_w, out_h),
                                     flags=cv2.INTER_LINEAR,
                                     borderMode=cv2.BORDER_CONSTANT)
        
        # Over compositing (back to front)
        # C_out = C_layer * alpha_layer + C_accum * (1 - alpha_layer)
        alpha = warped[:, :, 3:4]
        color = warped[:, :, :3]
        
        accumulated[:, :, :3] = color * alpha + accumulated[:, :, :3] * (1 - alpha)
        accumulated[:, :, 3:4] = alpha + accumulated[:, :, 3:4] * (1 - alpha)
    
    # Convert ke uint8
    result = (accumulated[:, :, :3] * 255).clip(0, 255).astype(np.uint8)
    
    return result

def render_mpi_sweep(mpi, depths, direction='horizontal', num_frames=20):
    """
    Render view sweep dari MPI.
    
    Args:
        mpi: MPI representation
        depths: Depth values
        direction: 'horizontal' atau 'vertical'
        num_frames: Jumlah frames
    
    Returns:
        List of rendered frames
    """
    frames = []
    
    # Translation range
    max_translation = BASELINE_RANGE * 10
    
    for i in range(num_frames):
        t = (i / (num_frames - 1) - 0.5) * 2 * max_translation
        
        if direction == 'horizontal':
            translation = [t, 0, 0]
        else:
            translation = [0, t, 0]
        
        frame = render_mpi_view(mpi, depths, translation)
        frames.append(frame)
    
    return frames

# ============================================================
# MPI VISUALIZATION
# ============================================================

def visualize_mpi_layers(mpi, depths, num_display=8):
    """
    Visualisasi selected MPI layers.
    
    Args:
        mpi: MPI representation
        depths: Depth values
        num_display: Jumlah layers untuk display
    
    Returns:
        Visualization image
    """
    import cv2
    
    num_planes = len(depths)
    
    # Select evenly spaced layers
    indices = np.linspace(0, num_planes - 1, num_display).astype(int)
    
    # Resize factor
    h, w = mpi.shape[1:3]
    scale = min(200 / h, 300 / w)
    new_h, new_w = int(h * scale), int(w * scale)
    
    # Create visualization
    rows = []
    cols_per_row = 4
    
    for row_start in range(0, len(indices), cols_per_row):
        row_layers = []
        
        for idx in indices[row_start:row_start + cols_per_row]:
            layer = mpi[idx]
            
            # Create RGBA visualization
            rgb = layer[:, :, :3]
            alpha = layer[:, :, 3]
            
            # Composite over checkerboard (untuk show transparency)
            checker = np.zeros((h, w, 3), dtype=np.float32)
            for y in range(h):
                for x in range(w):
                    if (x // 20 + y // 20) % 2 == 0:
                        checker[y, x] = [0.3, 0.3, 0.3]
                    else:
                        checker[y, x] = [0.6, 0.6, 0.6]
            
            vis = rgb * alpha[:, :, np.newaxis] + checker * (1 - alpha[:, :, np.newaxis])
            vis = (vis * 255).clip(0, 255).astype(np.uint8)
            
            # Resize
            vis = cv2.resize(vis, (new_w, new_h))
            
            # Add depth label
            cv2.putText(vis, f"d={depths[idx]:.1f}", (5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            row_layers.append(vis)
        
        # Pad if needed
        while len(row_layers) < cols_per_row:
            row_layers.append(np.zeros((new_h, new_w, 3), dtype=np.uint8))
        
        rows.append(np.hstack(row_layers))
    
    visualization = np.vstack(rows)
    
    return visualization

def visualize_alpha_distribution(mpi, depths):
    """
    Visualisasi distribusi alpha across depth.
    
    Args:
        mpi: MPI representation
        depths: Depth values
    
    Returns:
        Distribution plot image
    """
    import cv2
    
    num_planes = len(depths)
    h, w = mpi.shape[1:3]
    
    # Compute total alpha per plane
    alpha_per_plane = mpi[:, :, :, 3].sum(axis=(1, 2)) / (h * w)
    
    # Create plot
    plot_h, plot_w = 300, 600
    plot = np.ones((plot_h, plot_w, 3), dtype=np.uint8) * 255
    
    # Draw bars
    bar_width = plot_w // num_planes
    max_alpha = alpha_per_plane.max() if alpha_per_plane.max() > 0 else 1
    
    for i, alpha in enumerate(alpha_per_plane):
        bar_height = int((alpha / max_alpha) * (plot_h - 50))
        x = i * bar_width
        y = plot_h - 30 - bar_height
        
        # Color berdasarkan depth
        t = i / (num_planes - 1)
        color = (int(255 * (1-t)), int(255 * t), 100)
        
        cv2.rectangle(plot, (x + 2, y), (x + bar_width - 2, plot_h - 30), color, -1)
    
    # Axis labels
    cv2.putText(plot, "Depth Plane", (plot_w // 2 - 50, plot_h - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(plot, "Alpha", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Near/Far labels
    cv2.putText(plot, "Near", (5, plot_h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    cv2.putText(plot, "Far", (plot_w - 30, plot_h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    return plot

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_basic_mpi():
    """Demo basic MPI creation dan visualization."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Basic MPI Creation")
    print("="*60)
    
    # Create sample scene
    print("\n  Creating sample scene...")
    image, depth = create_sample_scene()
    
    cv2.imwrite(str(OUTPUT_DIR / "mpi_input_image.jpg"), image)
    
    depth_vis = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_input_depth.jpg"), depth_vis)
    
    print(f"  ✓ Input image: {image.shape}")
    print(f"  ✓ Depth range: {depth.min():.1f} - {depth.max():.1f}")
    
    # Create MPI
    print(f"\n  Creating MPI with {NUM_DEPTH_PLANES} planes...")
    mpi, depths = create_mpi_from_rgbd(image, depth, NUM_DEPTH_PLANES, NEAR_DEPTH, FAR_DEPTH)
    
    print(f"  ✓ MPI shape: {mpi.shape}")
    print(f"  ✓ Depth planes: {depths[0]:.2f} - {depths[-1]:.2f}")
    
    # Visualize layers
    print("\n  Visualizing MPI layers...")
    layer_vis = visualize_mpi_layers(mpi, depths, 8)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_layers.jpg"), layer_vis)
    print(f"  ✓ Saved: mpi_layers.jpg")
    
    # Alpha distribution
    alpha_plot = visualize_alpha_distribution(mpi, depths)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_alpha_distribution.jpg"), alpha_plot)
    print(f"  ✓ Saved: mpi_alpha_distribution.jpg")
    
    return mpi, depths

def demo_mpi_rendering():
    """Demo rendering novel views dari MPI."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: MPI Novel View Rendering")
    print("="*60)
    
    # Create MPI
    image, depth = create_sample_scene()
    mpi, depths = create_mpi_from_rgbd(image, depth, NUM_DEPTH_PLANES, NEAR_DEPTH, FAR_DEPTH)
    
    # Render original view
    print("\n  Rendering original view...")
    original = render_mpi_view(mpi, depths, [0, 0, 0])
    cv2.imwrite(str(OUTPUT_DIR / "mpi_render_original.jpg"), original)
    
    # Render shifted views
    print("\n  Rendering shifted views...")
    
    translations = [
        ("left", [-3, 0, 0]),
        ("right", [3, 0, 0]),
        ("up", [0, -2, 0]),
        ("down", [0, 2, 0]),
    ]
    
    rendered_views = [original]
    
    for name, trans in translations:
        view = render_mpi_view(mpi, depths, trans)
        cv2.imwrite(str(OUTPUT_DIR / f"mpi_render_{name}.jpg"), view)
        rendered_views.append(view)
        print(f"  ✓ Rendered: {name} view")
    
    # Create comparison
    comparison = np.hstack(rendered_views)
    comparison = cv2.resize(comparison, None, fx=0.4, fy=0.4)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_views_comparison.jpg"), comparison)
    print(f"\n  ✓ Saved: mpi_views_comparison.jpg")
    
    return rendered_views

def demo_view_sweep():
    """Demo view sweep animation."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: View Sweep Animation")
    print("="*60)
    
    # Create MPI
    image, depth = create_sample_scene()
    mpi, depths = create_mpi_from_rgbd(image, depth, NUM_DEPTH_PLANES, NEAR_DEPTH, FAR_DEPTH)
    
    # Horizontal sweep
    print("\n  Generating horizontal sweep...")
    h_frames = render_mpi_sweep(mpi, depths, 'horizontal', 20)
    
    for i, frame in enumerate(h_frames):
        cv2.imwrite(str(OUTPUT_DIR / f"sweep_h_{i:02d}.jpg"), frame)
    
    print(f"  ✓ Saved {len(h_frames)} horizontal frames")
    
    # Vertical sweep
    print("\n  Generating vertical sweep...")
    v_frames = render_mpi_sweep(mpi, depths, 'vertical', 20)
    
    for i, frame in enumerate(v_frames):
        cv2.imwrite(str(OUTPUT_DIR / f"sweep_v_{i:02d}.jpg"), frame)
    
    print(f"  ✓ Saved {len(v_frames)} vertical frames")
    
    # Create montage
    h_montage = np.hstack([f for f in h_frames[::4]])
    h_montage = cv2.resize(h_montage, None, fx=0.3, fy=0.3)
    cv2.imwrite(str(OUTPUT_DIR / "sweep_horizontal_montage.jpg"), h_montage)
    
    v_montage = np.hstack([f for f in v_frames[::4]])
    v_montage = cv2.resize(v_montage, None, fx=0.3, fy=0.3)
    cv2.imwrite(str(OUTPUT_DIR / "sweep_vertical_montage.jpg"), v_montage)
    
    print(f"\n  ✓ Saved sweep montages")
    
    return h_frames, v_frames

def demo_soft_mpi():
    """Demo soft MPI dengan gradual alpha."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: Soft MPI Assignment")
    print("="*60)
    
    # Create scene
    image, depth = create_sample_scene()
    
    # Compare hard vs soft MPI
    print("\n  Creating hard MPI...")
    mpi_hard, depths = create_mpi_from_rgbd(image, depth, 16, NEAR_DEPTH, FAR_DEPTH)
    
    print("  Creating soft MPI...")
    mpi_soft, _ = create_soft_mpi(image, depth, 16, NEAR_DEPTH, FAR_DEPTH, sigma=0.2)
    
    # Visualize layers
    hard_vis = visualize_mpi_layers(mpi_hard, depths, 8)
    soft_vis = visualize_mpi_layers(mpi_soft, depths, 8)
    
    cv2.imwrite(str(OUTPUT_DIR / "mpi_hard_layers.jpg"), hard_vis)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_soft_layers.jpg"), soft_vis)
    
    # Compare renders
    view_hard = render_mpi_view(mpi_hard, depths, [2, 0, 0])
    view_soft = render_mpi_view(mpi_soft, depths, [2, 0, 0])
    
    cv2.imwrite(str(OUTPUT_DIR / "mpi_hard_render.jpg"), view_hard)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_soft_render.jpg"), view_soft)
    
    # Comparison
    comparison = np.hstack([view_hard, view_soft])
    cv2.putText(comparison, "Hard MPI", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(comparison, "Soft MPI", (view_hard.shape[1] + 10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite(str(OUTPUT_DIR / "mpi_hard_vs_soft.jpg"), comparison)
    
    print(f"\n  ✓ Saved comparison: mpi_hard_vs_soft.jpg")
    
    return mpi_hard, mpi_soft

def demo_depth_plane_effect():
    """Demo efek jumlah depth planes."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 5: Depth Plane Count Effect")
    print("="*60)
    
    # Create scene
    image, depth = create_sample_scene()
    
    plane_counts = [4, 8, 16, 32, 64]
    results = []
    
    translation = [3, 0, 0]
    
    for num_planes in plane_counts:
        print(f"\n  MPI with {num_planes} planes...")
        
        start = time.time()
        mpi, depths = create_mpi_from_rgbd(image, depth, num_planes, NEAR_DEPTH, FAR_DEPTH)
        create_time = time.time() - start
        
        start = time.time()
        rendered = render_mpi_view(mpi, depths, translation)
        render_time = time.time() - start
        
        results.append(rendered)
        
        cv2.imwrite(str(OUTPUT_DIR / f"mpi_planes_{num_planes}.jpg"), rendered)
        print(f"    Create: {create_time:.3f}s, Render: {render_time:.3f}s")
    
    # Create comparison
    comparison = np.hstack([cv2.resize(r, (320, 240)) for r in results])
    
    for i, num in enumerate(plane_counts):
        cv2.putText(comparison, f"P={num}", (i * 320 + 10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imwrite(str(OUTPUT_DIR / "mpi_plane_count_comparison.jpg"), comparison)
    print(f"\n  ✓ Saved: mpi_plane_count_comparison.jpg")
    
    return results

def demo_depth_sampling():
    """Demo berbagai depth sampling methods."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 6: Depth Sampling Methods")
    print("="*60)
    
    near, far = 1, 100
    num = 16
    
    methods = ['linear', 'linear_disparity', 'log']
    
    print("\n  Depth Plane Values:")
    print("-" * 50)
    
    for method in methods:
        depths = generate_depth_planes(near, far, num, method)
        print(f"\n  {method}:")
        print(f"    First 5: {depths[:5].round(2)}")
        print(f"    Last 5:  {depths[-5:].round(2)}")
    
    # Visual comparison
    image, depth = create_sample_scene()
    
    results = []
    for method in methods:
        depths = generate_depth_planes(NEAR_DEPTH, FAR_DEPTH, 16, method)
        mpi, _ = create_mpi_from_rgbd(image, depth, 16, NEAR_DEPTH, FAR_DEPTH)
        
        rendered = render_mpi_view(mpi, depths, [3, 0, 0])
        results.append(rendered)
    
    comparison = np.hstack([cv2.resize(r, (320, 240)) for r in results])
    
    for i, method in enumerate(methods):
        cv2.putText(comparison, method, (i * 320 + 10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imwrite(str(OUTPUT_DIR / "mpi_depth_sampling.jpg"), comparison)
    print(f"\n  ✓ Saved: mpi_depth_sampling.jpg")
    
    return results

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import cv2
    
    print("="*60)
    print("PRAKTIKUM 14.5: MULTIPLANE IMAGES (MPI)")
    print("="*60)
    
    # Check dependencies
    if not check_opencv():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_basic_mpi()
    
    demo_mpi_rendering()
    
    demo_view_sweep()
    
    demo_soft_mpi()
    
    demo_depth_plane_effect()
    
    demo_depth_sampling()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nMPI Concepts:")
    print("  1. Representasi: Stack of RGBA layers at depths")
    print("  2. Creation: Assign pixels ke depth planes")
    print("  3. Rendering: Homography warp + Over compositing")
    
    print("\nKey Parameters:")
    print(f"  - Num planes: {NUM_DEPTH_PLANES}")
    print(f"  - Depth range: {NEAR_DEPTH} - {FAR_DEPTH}")
    print(f"  - Sampling: {DEPTH_SAMPLING}")
    
    print("\nApplications:")
    print("  - Novel view synthesis")
    print("  - 3D photos (Facebook 3D)")
    print("  - Real-time view interpolation")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
