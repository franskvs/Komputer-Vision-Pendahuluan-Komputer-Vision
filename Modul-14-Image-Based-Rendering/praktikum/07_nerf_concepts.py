"""
Praktikum 14.7: NeRF Concepts and Visualization
===============================================

Program ini mendemonstrasikan konsep dasar NeRF:
1. Ray marching visualization
2. Volume rendering equation
3. Positional encoding
4. MLP structure visualization
5. View-dependent effects

Teori:
------
Neural Radiance Fields (NeRF) merepresentasikan scene
sebagai continuous volumetric function:
F(x, d) → (c, σ)
dimana:
- x: 3D position
- d: viewing direction
- c: RGB color
- σ: density

Volume Rendering:
C(r) = ∫ T(t)·σ(r(t))·c(r(t),d) dt
T(t) = exp(-∫ σ(r(s)) ds)

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
OUTPUT_DIR = Path(__file__).parent / "output" / "output7"

# Ray marching parameters
NUM_SAMPLES_COARSE = 64            # Samples per ray (coarse)
NUM_SAMPLES_FINE = 128             # Samples per ray (fine)
NEAR_BOUND = 0.5                   # Near clipping plane
FAR_BOUND = 5.0                    # Far clipping plane

# Positional encoding
NUM_ENCODING_FUNCS = 10            # Number of encoding functions (L)
INCLUDE_INPUT = True               # Include original input in encoding

# MLP parameters (for visualization)
MLP_HIDDEN_SIZE = 256              # Hidden layer size
MLP_NUM_LAYERS = 8                 # Number of layers

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat direktori output."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")

def check_dependencies():
    """Periksa ketersediaan dependencies."""
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV tidak terinstall!")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ Matplotlib available")
    except ImportError:
        print("⚠ Matplotlib tidak tersedia, beberapa visualisasi mungkin terbatas")
    
    return True

# ============================================================
# RAY GENERATION
# ============================================================

def get_ray_bundle(height, width, focal_length, camera_pose):
    """
    Generate ray origins dan directions untuk semua pixels.
    
    Args:
        height, width: Image dimensions
        focal_length: Camera focal length
        camera_pose: 4x4 camera-to-world matrix
    
    Returns:
        ray_origins: (H, W, 3)
        ray_directions: (H, W, 3)
    """
    # Create pixel coordinates
    i, j = np.meshgrid(np.arange(width), np.arange(height), indexing='xy')
    
    # Convert ke camera coordinates
    # x = (i - cx) / f
    # y = -(j - cy) / f  (flip y)
    # z = -1 (looking down -z axis)
    
    cx = width / 2
    cy = height / 2
    
    directions_cam = np.stack([
        (i - cx) / focal_length,
        -(j - cy) / focal_length,
        -np.ones_like(i)
    ], axis=-1)
    
    # Normalize
    directions_cam = directions_cam / np.linalg.norm(directions_cam, axis=-1, keepdims=True)
    
    # Transform ke world coordinates
    rotation = camera_pose[:3, :3]
    translation = camera_pose[:3, 3]
    
    directions_world = np.einsum('ij,hwj->hwi', rotation, directions_cam)
    
    # Ray origins (camera position)
    origins = np.broadcast_to(translation, directions_world.shape)
    
    return origins.astype(np.float32), directions_world.astype(np.float32)

def sample_along_rays(ray_origins, ray_directions, near, far, num_samples, perturb=True):
    """
    Sample points along rays.
    
    Args:
        ray_origins: (H, W, 3) ray origins
        ray_directions: (H, W, 3) ray directions
        near, far: Depth bounds
        num_samples: Number of samples per ray
        perturb: Add random perturbation
    
    Returns:
        points: (H, W, num_samples, 3) sampled 3D points
        t_vals: (H, W, num_samples) sample distances
    """
    H, W, _ = ray_origins.shape
    
    # Uniform spacing
    t_vals = np.linspace(near, far, num_samples)
    t_vals = np.broadcast_to(t_vals, (H, W, num_samples))
    
    if perturb:
        # Add noise
        mids = 0.5 * (t_vals[..., 1:] + t_vals[..., :-1])
        upper = np.concatenate([mids, t_vals[..., -1:]], axis=-1)
        lower = np.concatenate([t_vals[..., :1], mids], axis=-1)
        
        noise = np.random.uniform(size=t_vals.shape)
        t_vals = lower + (upper - lower) * noise
    
    # Compute points: p = o + t*d
    points = ray_origins[..., None, :] + ray_directions[..., None, :] * t_vals[..., :, None]
    
    return points.astype(np.float32), t_vals.astype(np.float32)

# ============================================================
# POSITIONAL ENCODING
# ============================================================

def positional_encoding(x, num_freqs, include_input=True):
    """
    Compute positional encoding.
    
    γ(p) = (p, sin(2^0·π·p), cos(2^0·π·p), ..., sin(2^(L-1)·π·p), cos(2^(L-1)·π·p))
    
    Args:
        x: Input positions (..., D)
        num_freqs: Number of frequency bands (L)
        include_input: Include original input
    
    Returns:
        Encoded positions (..., D * (1 + 2*L) or D * 2*L)
    """
    encodings = []
    
    if include_input:
        encodings.append(x)
    
    freq_bands = 2.0 ** np.arange(num_freqs) * np.pi
    
    for freq in freq_bands:
        encodings.append(np.sin(freq * x))
        encodings.append(np.cos(freq * x))
    
    return np.concatenate(encodings, axis=-1)

def visualize_positional_encoding():
    """
    Visualize positional encoding untuk 1D input.
    
    Returns:
        Visualization image
    """
    import cv2
    
    # 1D input
    x = np.linspace(-1, 1, 200)[:, np.newaxis]
    
    # Encode dengan berbagai L
    L_values = [2, 4, 6, 10]
    
    # Create figure
    h, w = 400, 800
    vis = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    colors = [
        (255, 0, 0),
        (0, 200, 0),
        (0, 0, 255),
        (200, 0, 200)
    ]
    
    # Plot each encoding
    plot_h = h // len(L_values)
    
    for idx, L in enumerate(L_values):
        encoded = positional_encoding(x, L, include_input=False)
        
        # Select beberapa dimensions untuk plot
        y_offset = idx * plot_h + plot_h // 2
        
        # Draw axis
        cv2.line(vis, (50, y_offset), (w - 50, y_offset), (200, 200, 200), 1)
        cv2.putText(vis, f"L={L}", (10, y_offset + 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Plot first few sin/cos pairs
        for i in range(min(3, L)):
            sin_vals = encoded[:, 2*i]
            cos_vals = encoded[:, 2*i + 1]
            
            # Normalize dan scale
            sin_scaled = (sin_vals * plot_h // 3).astype(int)
            cos_scaled = (cos_vals * plot_h // 3).astype(int)
            
            # Draw curves
            for j in range(len(x) - 1):
                x1 = int(50 + j * (w - 100) / len(x))
                x2 = int(50 + (j + 1) * (w - 100) / len(x))
                
                y1 = y_offset - sin_scaled[j]
                y2 = y_offset - sin_scaled[j + 1]
                
                # Sin curve
                alpha = 1.0 - i * 0.3
                color = tuple(int(c * alpha) for c in colors[idx])
                cv2.line(vis, (x1, y1), (x2, y2), color, 1)
    
    # Title
    cv2.putText(vis, "Positional Encoding: sin/cos at different frequencies", 
                (w // 2 - 200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    return vis

# ============================================================
# VOLUME RENDERING
# ============================================================

def volume_render(densities, colors, t_vals, raw=False):
    """
    Volume rendering equation.
    
    C(r) = Σ Ti * (1 - exp(-σi * δi)) * ci
    Ti = exp(-Σ_{j<i} σj * δj)
    
    Args:
        densities: (H, W, num_samples) density σ
        colors: (H, W, num_samples, 3) RGB colors
        t_vals: (H, W, num_samples) sample distances
        raw: If True, return additional outputs
    
    Returns:
        rgb: (H, W, 3) rendered color
        depth: (H, W) rendered depth
        weights: (H, W, num_samples) sample weights
    """
    # Delta distances
    dists = t_vals[..., 1:] - t_vals[..., :-1]
    # Extend last distance
    dists = np.concatenate([dists, np.full(dists[..., :1].shape, 1e10)], axis=-1)
    
    # Alpha (opacity) dari density
    # alpha = 1 - exp(-sigma * delta)
    alpha = 1.0 - np.exp(-densities * dists)
    
    # Transmittance
    # T_i = exp(-sum_{j<i} sigma_j * delta_j)
    # = prod_{j<i} (1 - alpha_j)
    transmittance = np.cumprod(1 - alpha + 1e-10, axis=-1)
    transmittance = np.concatenate([
        np.ones(transmittance[..., :1].shape),
        transmittance[..., :-1]
    ], axis=-1)
    
    # Weights
    weights = alpha * transmittance
    
    # Rendered color
    rgb = np.sum(weights[..., None] * colors, axis=-2)
    
    # Rendered depth (expected termination)
    depth = np.sum(weights * t_vals, axis=-1)
    
    # Accumulated opacity
    acc = np.sum(weights, axis=-1)
    
    if raw:
        return rgb, depth, weights, alpha, transmittance, acc
    
    return rgb, depth, weights

def create_volume_rendering_visualization():
    """
    Create visualization of volume rendering process.
    
    Returns:
        Visualization image
    """
    import cv2
    
    # Create simple 1D example
    num_samples = 20
    t = np.linspace(0, 5, num_samples)
    
    # Gaussian density distribution
    sigma = np.exp(-((t - 2.5)**2) / 0.5) * 2
    
    # Color (gradient blue to red)
    colors = np.stack([t / 5, 0.3 * np.ones(num_samples), 1 - t / 5], axis=-1)
    
    # Compute volume rendering
    dists = np.concatenate([np.diff(t), [1e10]])
    alpha = 1 - np.exp(-sigma * dists)
    
    T = np.ones(num_samples)
    for i in range(1, num_samples):
        T[i] = T[i-1] * (1 - alpha[i-1])
    
    weights = alpha * T
    
    # Create visualization
    h, w = 500, 800
    vis = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    # Plot area
    plot_x = 100
    plot_y = 80
    plot_w = w - 150
    plot_h = 100
    
    # Draw density
    cv2.putText(vis, "Density (sigma)", (plot_x, plot_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    for i in range(num_samples - 1):
        x1 = int(plot_x + i * plot_w / num_samples)
        x2 = int(plot_x + (i + 1) * plot_w / num_samples)
        y1 = int(plot_y + plot_h - sigma[i] / 2 * plot_h)
        y2 = int(plot_y + plot_h - sigma[i + 1] / 2 * plot_h)
        
        cv2.line(vis, (x1, y1), (x2, y2), (255, 0, 0), 2)
    
    cv2.rectangle(vis, (plot_x, plot_y), (plot_x + plot_w, plot_y + plot_h), (0, 0, 0), 1)
    
    # Draw transmittance
    plot_y2 = plot_y + plot_h + 50
    cv2.putText(vis, "Transmittance (T)", (plot_x, plot_y2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    for i in range(num_samples - 1):
        x1 = int(plot_x + i * plot_w / num_samples)
        x2 = int(plot_x + (i + 1) * plot_w / num_samples)
        y1 = int(plot_y2 + plot_h - T[i] * plot_h)
        y2 = int(plot_y2 + plot_h - T[i + 1] * plot_h)
        
        cv2.line(vis, (x1, y1), (x2, y2), (0, 150, 0), 2)
    
    cv2.rectangle(vis, (plot_x, plot_y2), (plot_x + plot_w, plot_y2 + plot_h), (0, 0, 0), 1)
    
    # Draw weights
    plot_y3 = plot_y2 + plot_h + 50
    cv2.putText(vis, "Weights (alpha * T)", (plot_x, plot_y3 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    bar_w = plot_w // num_samples - 2
    for i in range(num_samples):
        x = int(plot_x + i * plot_w / num_samples)
        bar_h = int(weights[i] * plot_h)
        
        # Color the bar
        color = tuple(int(c * 255) for c in colors[i][::-1])  # BGR
        cv2.rectangle(vis, (x, plot_y3 + plot_h - bar_h), (x + bar_w, plot_y3 + plot_h), color, -1)
    
    cv2.rectangle(vis, (plot_x, plot_y3), (plot_x + plot_w, plot_y3 + plot_h), (0, 0, 0), 1)
    
    # Final rendered color
    final_rgb = np.sum(weights[:, None] * colors, axis=0)
    final_color = tuple(int(c * 255) for c in final_rgb[::-1])
    
    cv2.putText(vis, "Final Rendered Color:", (plot_x, h - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.rectangle(vis, (plot_x + 150, h - 70), (plot_x + 250, h - 30), final_color, -1)
    cv2.rectangle(vis, (plot_x + 150, h - 70), (plot_x + 250, h - 30), (0, 0, 0), 1)
    
    # Title
    cv2.putText(vis, "Volume Rendering: C = sum(weight_i * color_i)", 
                (w // 2 - 180, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return vis

# ============================================================
# MLP STRUCTURE
# ============================================================

def visualize_nerf_mlp():
    """
    Visualize NeRF MLP architecture.
    
    Returns:
        Architecture visualization
    """
    import cv2
    
    h, w = 600, 900
    vis = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    # Architecture
    layers = [
        ("Input (x, d)", "60-dim (x) + 24-dim (d)"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("Skip Connection", f"+ input x"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE}"),
        ("FC (density)", "1 (σ)"),
        ("+ direction", f"+ 24-dim (d)"),
        ("FC + ReLU", f"{MLP_HIDDEN_SIZE // 2}"),
        ("FC (color)", "3 (RGB)"),
    ]
    
    # Draw layers
    layer_h = 35
    layer_w = 180
    start_y = 50
    start_x = w // 2 - layer_w // 2
    
    colors = {
        "Input": (200, 200, 255),
        "FC": (200, 255, 200),
        "Skip": (255, 220, 200),
        "density": (255, 200, 200),
        "color": (200, 255, 255),
        "direction": (255, 255, 200),
    }
    
    prev_y = None
    for i, (name, desc) in enumerate(layers):
        y = start_y + i * (layer_h + 10)
        
        # Determine color
        if "Input" in name:
            color = colors["Input"]
        elif "Skip" in name:
            color = colors["Skip"]
        elif "density" in name:
            color = colors["density"]
        elif "color" in name:
            color = colors["color"]
        elif "direction" in name:
            color = colors["direction"]
        else:
            color = colors["FC"]
        
        # Draw box
        cv2.rectangle(vis, (start_x, y), (start_x + layer_w, y + layer_h), color, -1)
        cv2.rectangle(vis, (start_x, y), (start_x + layer_w, y + layer_h), (0, 0, 0), 1)
        
        # Text
        cv2.putText(vis, name, (start_x + 10, y + 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(vis, desc, (start_x + 10, y + 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (100, 100, 100), 1)
        
        # Arrow
        if prev_y is not None:
            cv2.arrowedLine(vis, (start_x + layer_w // 2, prev_y + layer_h),
                           (start_x + layer_w // 2, y), (0, 0, 0), 1, tipLength=0.3)
        
        prev_y = y
    
    # Skip connection arrow
    skip_y = start_y + 4 * (layer_h + 10) + layer_h // 2
    cv2.line(vis, (start_x, skip_y), (start_x - 30, skip_y), (0, 0, 255), 2)
    cv2.line(vis, (start_x - 30, skip_y), (start_x - 30, start_y + layer_h // 2), (0, 0, 255), 2)
    cv2.line(vis, (start_x - 30, start_y + layer_h // 2), (start_x, start_y + layer_h // 2), (0, 0, 255), 2)
    
    # Labels
    cv2.putText(vis, "NeRF MLP Architecture", (w // 2 - 100, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Legend
    leg_x = w - 180
    leg_y = 100
    for name, color in colors.items():
        cv2.rectangle(vis, (leg_x, leg_y), (leg_x + 20, leg_y + 15), color, -1)
        cv2.rectangle(vis, (leg_x, leg_y), (leg_x + 20, leg_y + 15), (0, 0, 0), 1)
        cv2.putText(vis, name, (leg_x + 25, leg_y + 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        leg_y += 25
    
    return vis

# ============================================================
# RAY VISUALIZATION
# ============================================================

def visualize_ray_marching():
    """
    Visualize ray marching through volume.
    
    Returns:
        Visualization image
    """
    import cv2
    
    h, w = 500, 800
    vis = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    # Camera position
    cam_x, cam_y = 100, h // 2
    
    # Draw camera
    cv2.circle(vis, (cam_x, cam_y), 20, (0, 0, 200), -1)
    cv2.putText(vis, "Camera", (cam_x - 25, cam_y + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Volume bounds
    near = 150
    far = 650
    
    cv2.line(vis, (near, 50), (near, h - 50), (150, 150, 150), 2)
    cv2.line(vis, (far, 50), (far, h - 50), (150, 150, 150), 2)
    cv2.putText(vis, "Near", (near - 15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    cv2.putText(vis, "Far", (far - 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    # Draw scene (simple sphere)
    sphere_x, sphere_y = 400, h // 2
    sphere_r = 100
    cv2.circle(vis, (sphere_x, sphere_y), sphere_r, (200, 200, 255), -1)
    cv2.circle(vis, (sphere_x, sphere_y), sphere_r, (0, 0, 0), 1)
    
    # Draw rays
    num_rays = 5
    ray_ys = np.linspace(cam_y - 80, cam_y + 80, num_rays).astype(int)
    
    for ray_y in ray_ys:
        # Draw ray
        cv2.line(vis, (cam_x + 20, ray_y), (far, ray_y), (255, 200, 0), 1)
        
        # Sample points
        num_samples = 12
        for i in range(num_samples):
            t = near + (far - near) * i / (num_samples - 1)
            x = int(t)
            
            # Check if inside sphere
            dist = np.sqrt((x - sphere_x)**2 + (ray_y - sphere_y)**2)
            inside = dist < sphere_r
            
            color = (0, 200, 0) if inside else (200, 200, 200)
            cv2.circle(vis, (x, ray_y), 4, color, -1)
    
    # Annotations
    cv2.putText(vis, "Ray Marching: Sample points along each ray",
                (w // 2 - 180, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    cv2.putText(vis, "Green = inside object (high density)",
                (450, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 150, 0), 1)
    cv2.putText(vis, "Gray = empty space (low density)",
                (450, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
    
    return vis

# ============================================================
# SIMPLE NERF-LIKE RENDERING
# ============================================================

def simple_nerf_render():
    """
    Simple NeRF-like volume rendering (tanpa neural network).
    
    Menggunakan analytical scene definition.
    
    Returns:
        Rendered image, depth map
    """
    import cv2
    
    # Image size
    H, W = 256, 256
    focal = 256
    
    # Camera pose (identity = looking down -z)
    camera_pose = np.eye(4)
    camera_pose[2, 3] = 4  # Translate back
    
    # Generate rays
    origins, directions = get_ray_bundle(H, W, focal, camera_pose)
    
    # Sample points
    points, t_vals = sample_along_rays(origins, directions, NEAR_BOUND, FAR_BOUND, 
                                        NUM_SAMPLES_COARSE, perturb=False)
    
    # Define scene analytically (sphere)
    sphere_center = np.array([0, 0, 0])
    sphere_radius = 1.0
    
    # Compute density (high inside sphere)
    dist_to_center = np.linalg.norm(points - sphere_center, axis=-1)
    densities = np.exp(-((dist_to_center - sphere_radius)**2) / 0.1)
    densities = densities * 10  # Scale up
    
    # Compute colors (gradient based on position)
    colors = np.zeros((*points.shape[:-1], 3))
    colors[..., 0] = 0.5 + 0.5 * points[..., 0]  # R based on x
    colors[..., 1] = 0.5 + 0.5 * points[..., 1]  # G based on y
    colors[..., 2] = 0.8 - 0.3 * np.abs(points[..., 2])  # B
    colors = np.clip(colors, 0, 1)
    
    # Volume render
    rgb, depth, weights = volume_render(densities, colors, t_vals)
    
    # Convert to uint8
    rgb = (rgb * 255).clip(0, 255).astype(np.uint8)
    
    # Depth visualization
    depth_normalized = (depth - NEAR_BOUND) / (FAR_BOUND - NEAR_BOUND)
    depth_normalized = np.clip(depth_normalized, 0, 1)
    depth_vis = (depth_normalized * 255).astype(np.uint8)
    depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_VIRIDIS)
    
    return rgb, depth_color

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_positional_encoding():
    """Demo positional encoding."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Positional Encoding")
    print("="*60)
    
    # Example encoding
    x = np.array([[0.5, 0.3, -0.2]])  # Single 3D point
    
    print("\n  Input position: ", x.flatten())
    
    for L in [2, 4, 10]:
        encoded = positional_encoding(x, L, include_input=True)
        print(f"\n  L={L}: {encoded.shape[1]} dimensions")
        print(f"    First 10 values: {encoded[0, :10].round(3)}")
    
    # Visualize
    vis = visualize_positional_encoding()
    cv2.imwrite(str(OUTPUT_DIR / "nerf_positional_encoding.jpg"), vis)
    print(f"\n  ✓ Saved: nerf_positional_encoding.jpg")
    
    return vis

def demo_volume_rendering():
    """Demo volume rendering equation."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: Volume Rendering Equation")
    print("="*60)
    
    print("\n  Volume Rendering Formula:")
    print("  C(r) = Σ Ti · αi · ci")
    print("  where:")
    print("    Ti = Π(1 - αj) for j < i (transmittance)")
    print("    αi = 1 - exp(-σi · δi) (opacity)")
    
    # Create visualization
    vis = create_volume_rendering_visualization()
    cv2.imwrite(str(OUTPUT_DIR / "nerf_volume_rendering.jpg"), vis)
    print(f"\n  ✓ Saved: nerf_volume_rendering.jpg")
    
    return vis

def demo_ray_marching():
    """Demo ray marching visualization."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: Ray Marching")
    print("="*60)
    
    print("\n  Ray marching steps:")
    print("  1. Generate rays from camera through each pixel")
    print("  2. Sample N points along each ray")
    print("  3. Query MLP at each point for (σ, c)")
    print("  4. Integrate using volume rendering")
    
    # Visualize
    vis = visualize_ray_marching()
    cv2.imwrite(str(OUTPUT_DIR / "nerf_ray_marching.jpg"), vis)
    print(f"\n  ✓ Saved: nerf_ray_marching.jpg")
    
    return vis

def demo_mlp_structure():
    """Demo MLP architecture."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: NeRF MLP Architecture")
    print("="*60)
    
    print("\n  MLP Structure:")
    print(f"  - Input: 60-dim (3D pos × 2L with L=10)")
    print(f"  - Hidden: {MLP_NUM_LAYERS} layers × {MLP_HIDDEN_SIZE} units")
    print("  - Skip connection at layer 5")
    print("  - Output: 1 density + 3 RGB")
    print("  - Direction added before color output")
    
    # Visualize
    vis = visualize_nerf_mlp()
    cv2.imwrite(str(OUTPUT_DIR / "nerf_mlp_architecture.jpg"), vis)
    print(f"\n  ✓ Saved: nerf_mlp_architecture.jpg")
    
    return vis

def demo_simple_rendering():
    """Demo simple NeRF-like rendering."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 5: Simple Volume Rendering")
    print("="*60)
    
    print("\n  Rendering analytical scene...")
    print(f"  - Image size: 256×256")
    print(f"  - Samples per ray: {NUM_SAMPLES_COARSE}")
    
    start = time.time()
    rgb, depth = simple_nerf_render()
    elapsed = time.time() - start
    
    print(f"\n  Render time: {elapsed:.2f}s")
    
    cv2.imwrite(str(OUTPUT_DIR / "nerf_simple_rgb.jpg"), rgb)
    cv2.imwrite(str(OUTPUT_DIR / "nerf_simple_depth.jpg"), depth)
    
    # Combined
    combined = np.hstack([rgb, depth])
    cv2.imwrite(str(OUTPUT_DIR / "nerf_simple_combined.jpg"), combined)
    
    print(f"  ✓ Saved: nerf_simple_rgb.jpg")
    print(f"  ✓ Saved: nerf_simple_depth.jpg")
    print(f"  ✓ Saved: nerf_simple_combined.jpg")
    
    return rgb, depth

def demo_view_dependence():
    """Demo view-dependent effects."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 6: View-Dependent Effects")
    print("="*60)
    
    print("\n  NeRF models view-dependent effects:")
    print("  - Specular highlights")
    print("  - Reflections")
    print("  - Anisotropic materials")
    
    print("\n  Direction encoding allows MLP to learn:")
    print("  - Different colors dari different viewing angles")
    print("  - Realistic material appearances")
    
    # Create visualization showing view dependence
    h, w = 400, 600
    vis = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    # Draw sphere with specular highlight from different views
    views = [
        ("Front", 0),
        ("Left", -45),
        ("Right", 45),
    ]
    
    for i, (name, angle) in enumerate(views):
        cx = 100 + i * 200
        cy = h // 2
        r = 60
        
        # Draw sphere
        cv2.circle(vis, (cx, cy), r, (200, 200, 255), -1)
        
        # Specular highlight (position depends on view)
        highlight_x = int(cx + r * 0.4 * np.cos(np.radians(angle + 45)))
        highlight_y = int(cy - r * 0.4)
        cv2.circle(vis, (highlight_x, highlight_y), 15, (255, 255, 255), -1)
        
        cv2.putText(vis, name, (cx - 25, cy + r + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    cv2.putText(vis, "View-Dependent Effects: Specular highlights change with viewing angle",
                (w // 2 - 270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    cv2.imwrite(str(OUTPUT_DIR / "nerf_view_dependence.jpg"), vis)
    print(f"\n  ✓ Saved: nerf_view_dependence.jpg")
    
    return vis

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import cv2
    
    print("="*60)
    print("PRAKTIKUM 14.7: NERF CONCEPTS AND VISUALIZATION")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_positional_encoding()
    
    demo_volume_rendering()
    
    demo_ray_marching()
    
    demo_mlp_structure()
    
    demo_simple_rendering()
    
    demo_view_dependence()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nNeRF Key Concepts:")
    print("  1. Positional Encoding:")
    print("     γ(p) = [sin(2^k·π·p), cos(2^k·π·p)]")
    print("     Memungkinkan MLP belajar high-frequency details")
    
    print("\n  2. Volume Rendering:")
    print("     C = Σ Ti·αi·ci")
    print("     Differentiable integration untuk training")
    
    print("\n  3. MLP Architecture:")
    print("     - 8 layers × 256 units")
    print("     - Skip connection di tengah")
    print("     - Separate density dan color outputs")
    
    print("\n  4. View Dependence:")
    print("     - Direction encoding untuk specular/reflection")
    print("     - Enables realistic material appearance")
    
    print("\nApplications:")
    print("  - Novel view synthesis")
    print("  - 3D reconstruction dari images")
    print("  - VR/AR content creation")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
