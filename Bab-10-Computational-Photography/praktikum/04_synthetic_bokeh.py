"""
PRAKTIKUM BAB 10: COMPUTATIONAL PHOTOGRAPHY
============================================
Program 4: Synthetic Bokeh (Portrait Mode)

Deskripsi:
    Program ini mensimulasikan efek bokeh seperti pada smartphone
    portrait mode dengan menggunakan depth map untuk mengatur
    blur amount pada background.

Teori:
    Depth of Field (DoF) tergantung pada:
    - Aperture size (larger = shallower DoF)
    - Focal length
    - Subject distance
    
    Untuk synthetic bokeh:
    1. Estimate atau input depth map
    2. Set focus distance
    3. Calculate blur amount berdasarkan depth difference
    4. Apply variable blur
    5. Handle edge artifacts

Bokeh Types:
    - Gaussian: Smooth, natural
    - Disk (Circle of Confusion): More realistic optical bokeh
    - Hexagonal: Simulates aperture blade effect

Parameter yang dapat dimodifikasi:
    - FOCUS_DISTANCE: Depth value yang in-focus (0-1)
    - MAX_BLUR: Maximum blur radius
    - BOKEH_TYPE: 'gaussian' atau 'disk'

Output:
    - Bokeh image dengan berbagai settings
    - Depth visualization

Penulis: [Nama Mahasiswa]
NIM: [NIM]
Tanggal: [Tanggal Praktikum]
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# ============================================================
# PARAMETER YANG DAPAT DIMODIFIKASI
# ============================================================

# Focus distance (0 = closest, 1 = farthest)
FOCUS_DISTANCE = 0.3

# Maximum blur radius (pixels)
MAX_BLUR = 25

# Bokeh type: 'gaussian' atau 'disk'
BOKEH_TYPE = 'gaussian'

# Aperture setting (simulated f-number, lower = more blur)
F_NUMBER = 1.8

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data", "images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output", "output4")

# ============================================================
# FUNGSI-FUNGSI UTAMA
# ============================================================

def estimate_depth_simple(image):
    """
    Estimasi depth map sederhana berdasarkan image features.
    Ini adalah placeholder - real depth estimation memerlukan neural network.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use gradient as proxy for depth (objects with more detail closer)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient = np.sqrt(grad_x**2 + grad_y**2)
    
    # Blur untuk smoothness
    gradient = cv2.GaussianBlur(gradient, (31, 31), 0)
    
    # Invert dan normalize (more detail = closer)
    depth = 1 - cv2.normalize(gradient, None, 0, 1, cv2.NORM_MINMAX)
    
    # Add vertical gradient (lower = closer, common assumption)
    h = depth.shape[0]
    vertical = np.linspace(0.3, 0.7, h).reshape(-1, 1)
    vertical = np.tile(vertical, (1, depth.shape[1]))
    
    depth = 0.7 * depth + 0.3 * vertical
    
    return depth.astype(np.float32)

def create_disk_kernel(radius):
    """
    Buat circular (disk) kernel untuk bokeh blur.
    """
    size = 2 * radius + 1
    kernel = np.zeros((size, size), dtype=np.float32)
    
    center = radius
    for y in range(size):
        for x in range(size):
            if (x - center)**2 + (y - center)**2 <= radius**2:
                kernel[y, x] = 1
    
    kernel /= np.sum(kernel)
    return kernel

def calculate_blur_map(depth, focus_distance=FOCUS_DISTANCE, max_blur=MAX_BLUR, f_number=F_NUMBER):
    """
    Hitung blur amount berdasarkan depth.
    """
    # Blur increases with depth difference from focus
    depth_diff = np.abs(depth - focus_distance)
    
    # Scale by aperture (lower f-number = more blur)
    aperture_factor = 4.0 / f_number
    
    blur_map = depth_diff * max_blur * aperture_factor
    blur_map = np.clip(blur_map, 0, max_blur)
    
    return blur_map

def apply_variable_blur_gaussian(image, blur_map):
    """
    Apply variable Gaussian blur berdasarkan blur map.
    Optimized version using pre-computed blur levels.
    """
    result = np.zeros_like(image, dtype=np.float32)
    
    # Quantize blur levels untuk efficiency
    max_blur = int(np.max(blur_map))
    blur_levels = {}
    
    for blur_radius in range(0, max_blur + 1, 2):  # Step by 2 for speed
        if blur_radius == 0:
            blur_levels[blur_radius] = image.astype(np.float32)
        else:
            ksize = blur_radius * 2 + 1
            blur_levels[blur_radius] = cv2.GaussianBlur(
                image.astype(np.float32), (ksize, ksize), 0
            )
    
    # Create output by selecting from blur levels
    h, w = blur_map.shape
    for y in range(h):
        for x in range(w):
            blur_r = int(blur_map[y, x])
            blur_r = (blur_r // 2) * 2  # Round to nearest even
            blur_r = min(blur_r, max_blur)
            result[y, x] = blur_levels.get(blur_r, blur_levels[0])[y, x]
    
    return result.astype(np.uint8)

def apply_variable_blur_fast(image, blur_map, num_levels=5):
    """
    Faster variable blur using alpha blending between blur levels.
    """
    max_blur = int(np.max(blur_map))
    
    # Generate blur levels
    levels = []
    blur_values = np.linspace(0, max_blur, num_levels)
    
    for blur_radius in blur_values:
        if blur_radius < 1:
            levels.append(image.astype(np.float32))
        else:
            ksize = int(blur_radius) * 2 + 1
            if ksize % 2 == 0:
                ksize += 1
            levels.append(cv2.GaussianBlur(image.astype(np.float32), (ksize, ksize), 0))
    
    # Blend between levels based on blur_map
    result = np.zeros_like(image, dtype=np.float32)
    
    for i in range(num_levels - 1):
        lower_blur = blur_values[i]
        upper_blur = blur_values[i + 1]
        
        # Mask for this range
        in_range = (blur_map >= lower_blur) & (blur_map < upper_blur)
        
        if np.any(in_range):
            # Interpolation weight
            alpha = (blur_map - lower_blur) / (upper_blur - lower_blur + 1e-6)
            alpha = np.clip(alpha, 0, 1)
            alpha = np.expand_dims(alpha, axis=2)
            
            # Blend
            blended = (1 - alpha) * levels[i] + alpha * levels[i + 1]
            result = np.where(np.expand_dims(in_range, axis=2), blended, result)
    
    # Handle maximum level
    in_max = blur_map >= blur_values[-1]
    result = np.where(np.expand_dims(in_max, axis=2), levels[-1], result)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def refine_edges(image, original, depth, threshold=0.1):
    """
    Refine edges to reduce artifacts di foreground/background boundary.
    """
    # Detect edges in depth
    depth_edges = cv2.Canny((depth * 255).astype(np.uint8), 50, 150)
    depth_edges = cv2.dilate(depth_edges, None, iterations=2)
    
    # Create mask for edge regions
    edge_mask = depth_edges / 255.0
    edge_mask = cv2.GaussianBlur(edge_mask, (5, 5), 0)
    edge_mask = np.expand_dims(edge_mask, axis=2)
    
    # Blend original with bokeh at edges
    result = image * (1 - edge_mask * 0.5) + original * (edge_mask * 0.5)
    
    return result.astype(np.uint8)

def main():
    """
    Fungsi utama untuk synthetic bokeh demo.
    """
    print("=" * 60)
    print("SYNTHETIC BOKEH (PORTRAIT MODE)")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load image dan depth
    image_path = os.path.join(DATA_DIR, "portrait.jpg")
    depth_path = os.path.join(DATA_DIR, "portrait_depth.png")
    
    if not os.path.exists(image_path):
        print("Portrait image tidak ditemukan!")
        print("Mencoba dengan gambar lain...")
        image_path = os.path.join(DATA_DIR, "lena.png")
        depth_path = None
    
    if not os.path.exists(image_path):
        print("Image tidak ditemukan! Jalankan download_sample_data.py")
        return
    
    print(f"\nLoading image: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print("Failed to load image!")
        return
    
    print(f"Image size: {image.shape}")
    
    # Load atau estimate depth
    if depth_path and os.path.exists(depth_path):
        print(f"Loading depth map: {depth_path}")
        depth = cv2.imread(depth_path, cv2.IMREAD_GRAYSCALE)
        depth = depth.astype(np.float32) / 255.0
    else:
        print("Estimating depth from image...")
        depth = estimate_depth_simple(image)
    
    # Save depth visualization
    depth_vis = cv2.applyColorMap((depth * 255).astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "04_depth_map.png"), depth_vis)
    
    # Calculate blur map
    print(f"\nCalculating blur map...")
    print(f"  Focus distance: {FOCUS_DISTANCE}")
    print(f"  Max blur: {MAX_BLUR}")
    print(f"  F-number: {F_NUMBER}")
    
    blur_map = calculate_blur_map(depth, FOCUS_DISTANCE, MAX_BLUR, F_NUMBER)
    
    # Save blur map
    blur_vis = cv2.applyColorMap((blur_map / MAX_BLUR * 255).astype(np.uint8), cv2.COLORMAP_HOT)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "04_blur_map.png"), blur_vis)
    
    # Apply bokeh
    print("\nApplying bokeh effect...")
    bokeh = apply_variable_blur_fast(image, blur_map, num_levels=8)
    
    # Refine edges
    bokeh = refine_edges(bokeh, image, depth)
    
    cv2.imwrite(os.path.join(OUTPUT_DIR, "04_bokeh_result.jpg"), bokeh)
    
    # Try different focus distances
    print("\nGenerating bokeh dengan berbagai focus distances...")
    focus_distances = [0.2, 0.4, 0.6, 0.8]
    bokeh_results = {}
    
    for fd in focus_distances:
        blur_map_fd = calculate_blur_map(depth, fd, MAX_BLUR, F_NUMBER)
        bokeh_fd = apply_variable_blur_fast(image, blur_map_fd, num_levels=8)
        bokeh_results[f"Focus={fd}"] = bokeh_fd
        cv2.imwrite(os.path.join(OUTPUT_DIR, f"04_bokeh_focus{int(fd*10)}.jpg"), bokeh_fd)
    
    # Create comparison figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(depth, cmap='jet')
    axes[0, 1].set_title("Depth Map")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(blur_map / MAX_BLUR, cmap='hot')
    axes[0, 2].set_title("Blur Map")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(bokeh_results["Focus=0.2"], cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title("Focus=0.2 (Close)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(bokeh_results["Focus=0.4"], cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title("Focus=0.4 (Mid)")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(bokeh_results["Focus=0.8"], cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title("Focus=0.8 (Far)")
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "04_bokeh_comparison.png"), dpi=150)
    plt.close()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"""
Synthetic bokeh complete!

Files generated:
  - 04_depth_map.png: Depth visualization
  - 04_blur_map.png: Blur amount visualization
  - 04_bokeh_result.jpg: Main result
  - 04_bokeh_focus*.jpg: Various focus distances
  - 04_bokeh_comparison.png: Side-by-side comparison

Tips:
  - Lower F-number = stronger bokeh effect
  - Adjust focus distance untuk foreground/background blur
  - Edge refinement penting untuk natural look
""")
    
    # Display
    cv2.imshow("Original", image)
    cv2.imshow("Depth Map", depth_vis)
    cv2.imshow("Bokeh Result", bokeh)
    print("\nMenampilkan hasil (akan otomatis tertutup dalam 2 detik)...")
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
