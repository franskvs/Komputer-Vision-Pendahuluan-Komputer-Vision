"""
Download Sample Data untuk Bab 14: Image-Based Rendering
=========================================================

Script ini menghasilkan sample data sintetis untuk praktikum IBR:
1. Sequential images untuk panorama stitching
2. Stereo image pairs untuk view interpolation
3. Equirectangular panorama samples
4. Multi-view images untuk view synthesis

Author: Praktikum Computer Vision
"""

import numpy as np
from pathlib import Path
import json
import struct

# ============================================================
# KONFIGURASI
# ============================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Subdirectories
PANORAMA_DIR = DATA_DIR / "panorama_sequences"
STEREO_DIR = DATA_DIR / "stereo_pairs"
EQUIRECT_DIR = DATA_DIR / "equirectangular"
MULTIVIEW_DIR = DATA_DIR / "multiview"

# Image parameters
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
EQUIRECT_WIDTH = 2048
EQUIRECT_HEIGHT = 1024

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def setup_directories():
    """Membuat struktur direktori untuk data."""
    directories = [
        DATA_DIR,
        PANORAMA_DIR,
        STEREO_DIR,
        EQUIRECT_DIR,
        MULTIVIEW_DIR
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")

def check_dependencies():
    """Periksa dependencies yang diperlukan."""
    dependencies = {
        'numpy': False,
        'PIL': False,
        'cv2': False
    }
    
    try:
        import numpy
        dependencies['numpy'] = True
    except ImportError:
        pass
    
    try:
        from PIL import Image
        dependencies['PIL'] = True
    except ImportError:
        pass
    
    try:
        import cv2
        dependencies['cv2'] = True
    except ImportError:
        pass
    
    print("\nDependency Check:")
    for dep, available in dependencies.items():
        status = "✓" if available else "✗"
        print(f"  {status} {dep}")
    
    return dependencies

# ============================================================
# SYNTHETIC IMAGE GENERATION
# ============================================================

def create_gradient_image(width, height, color1, color2, direction='horizontal'):
    """
    Buat gradient image.
    
    Args:
        width, height: Dimensi gambar
        color1, color2: RGB tuples (0-255)
        direction: 'horizontal' atau 'vertical'
    
    Returns:
        numpy array RGB
    """
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    if direction == 'horizontal':
        for x in range(width):
            t = x / (width - 1)
            color = tuple(int(c1 * (1 - t) + c2 * t) for c1, c2 in zip(color1, color2))
            image[:, x] = color
    else:
        for y in range(height):
            t = y / (height - 1)
            color = tuple(int(c1 * (1 - t) + c2 * t) for c1, c2 in zip(color1, color2))
            image[y, :] = color
    
    return image

def create_checkerboard(width, height, square_size=50, color1=(255, 255, 255), color2=(0, 0, 0)):
    """Buat checkerboard pattern."""
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            if ((x // square_size) + (y // square_size)) % 2 == 0:
                image[y, x] = color1
            else:
                image[y, x] = color2
    
    return image

def create_scene_with_depth(width, height, scene_type='room'):
    """
    Buat synthetic scene dengan depth information.
    
    Returns:
        image: RGB image
        depth: Depth map (float, 0-1)
    """
    image = np.zeros((height, width, 3), dtype=np.uint8)
    depth = np.ones((height, width), dtype=np.float32)
    
    if scene_type == 'room':
        # Floor
        for y in range(height // 2, height):
            t = (y - height // 2) / (height // 2)
            d = 0.3 + 0.7 * t  # Closer at bottom
            color = int(100 + 50 * t)
            image[y, :] = [color, color - 20, color - 30]
            depth[y, :] = d
        
        # Back wall
        image[:height // 2, :] = [180, 175, 170]
        depth[:height // 2, :] = 0.2
        
        # Objects (simplified boxes)
        # Left box
        for y in range(height // 2 - 50, height // 2 + 50):
            for x in range(50, 150):
                if 0 <= y < height and 0 <= x < width:
                    image[y, x] = [200, 50, 50]
                    depth[y, x] = 0.5
        
        # Right box
        for y in range(height // 2 - 30, height // 2 + 70):
            for x in range(width - 180, width - 80):
                if 0 <= y < height and 0 <= x < width:
                    image[y, x] = [50, 50, 200]
                    depth[y, x] = 0.6
        
        # Center sphere approximation
        cx, cy = width // 2, height // 2
        for y in range(height):
            for x in range(width):
                dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                if dist < 60:
                    intensity = int(255 * (1 - dist / 60))
                    image[y, x] = [intensity, intensity, 50]
                    depth[y, x] = 0.4 + 0.1 * (dist / 60)
    
    elif scene_type == 'outdoor':
        # Sky
        for y in range(height // 3):
            t = y / (height // 3)
            image[y, :] = [int(100 + 100 * t), int(150 + 50 * t), 255]
            depth[y, :] = 0.01
        
        # Mountains
        for x in range(width):
            mountain_height = int(height // 3 + 50 * np.sin(x * 0.01) + 30 * np.sin(x * 0.03))
            for y in range(height // 3, min(mountain_height, height)):
                image[y, x] = [80, 100, 70]
                depth[y, x] = 0.1
        
        # Ground
        for y in range(height // 2, height):
            t = (y - height // 2) / (height // 2)
            color = int(50 + 100 * t)
            image[y, :] = [color - 20, color, color - 30]
            depth[y, :] = 0.3 + 0.7 * t
    
    return image, depth

def add_features_to_image(image, num_features=50):
    """Tambahkan features (dots/corners) untuk stitching."""
    h, w = image.shape[:2]
    
    for _ in range(num_features):
        x = np.random.randint(20, w - 20)
        y = np.random.randint(20, h - 20)
        color = tuple(np.random.randint(0, 255, 3).tolist())
        
        # Draw small cross
        for dx in range(-3, 4):
            if 0 <= x + dx < w:
                image[y, x + dx] = color
        for dy in range(-3, 4):
            if 0 <= y + dy < h:
                image[y + dy, x] = color
    
    return image

# ============================================================
# PANORAMA SEQUENCE GENERATION
# ============================================================

def generate_panorama_sequence(num_images=6, output_dir=None, overlap_ratio=0.3):
    """
    Generate sequence of images untuk panorama stitching.
    
    Args:
        num_images: Jumlah images dalam sequence
        output_dir: Output directory
        overlap_ratio: Overlap antara images (0-0.5)
    """
    if output_dir is None:
        output_dir = PANORAMA_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[Panorama Sequence] Generating {num_images} images...")
    
    # Create wide panoramic scene
    total_width = int(IMAGE_WIDTH * num_images * (1 - overlap_ratio))
    full_scene = create_gradient_image(
        total_width, IMAGE_HEIGHT,
        (255, 100, 100),  # Red
        (100, 100, 255)   # Blue
    )
    
    # Add features
    full_scene = add_features_to_image(full_scene, num_features=200)
    
    # Add some patterns for matching
    for i in range(0, total_width, 100):
        color = [(i * 37) % 255, (i * 73) % 255, (i * 113) % 255]
        y = IMAGE_HEIGHT // 2 + int(50 * np.sin(i * 0.05))
        for dy in range(-10, 11):
            for dx in range(-10, 11):
                if 0 <= y + dy < IMAGE_HEIGHT and 0 <= i + dx < total_width:
                    full_scene[y + dy, i + dx] = color
    
    # Extract overlapping images
    step = int(IMAGE_WIDTH * (1 - overlap_ratio))
    
    try:
        from PIL import Image
        use_pil = True
    except ImportError:
        use_pil = False
    
    for i in range(num_images):
        start_x = i * step
        end_x = start_x + IMAGE_WIDTH
        
        if end_x > total_width:
            # Pad if necessary
            img = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
            available = total_width - start_x
            img[:, :available] = full_scene[:, start_x:total_width]
        else:
            img = full_scene[:, start_x:end_x]
        
        # Save
        filename = f"panorama_{i:03d}.png"
        filepath = output_dir / filename
        
        if use_pil:
            Image.fromarray(img).save(filepath)
        else:
            # Save as PPM (always works)
            filepath = output_dir / f"panorama_{i:03d}.ppm"
            save_ppm(img, filepath)
        
        print(f"  ✓ Saved: {filepath.name}")
    
    # Save metadata
    metadata = {
        'num_images': num_images,
        'image_size': [IMAGE_WIDTH, IMAGE_HEIGHT],
        'overlap_ratio': overlap_ratio,
        'description': 'Synthetic panorama sequence for stitching practice'
    }
    
    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  ✓ Metadata saved")
    
    return output_dir

def save_ppm(image, filepath):
    """Save image as PPM format (no dependencies)."""
    h, w, c = image.shape
    with open(filepath, 'wb') as f:
        f.write(f"P6\n{w} {h}\n255\n".encode())
        f.write(image.tobytes())

# ============================================================
# STEREO PAIR GENERATION
# ============================================================

def generate_stereo_pair(baseline=30, output_dir=None):
    """
    Generate stereo image pair dengan known disparity.
    
    Args:
        baseline: Baseline dalam pixels
        output_dir: Output directory
    """
    if output_dir is None:
        output_dir = STEREO_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[Stereo Pair] Generating with baseline={baseline}px...")
    
    # Create scene with depth
    image_left, depth = create_scene_with_depth(IMAGE_WIDTH, IMAGE_HEIGHT, 'room')
    
    # Compute disparity from depth
    disparity = (baseline / (depth + 0.1)).astype(np.float32)
    disparity = np.clip(disparity, 0, baseline * 2)
    
    # Warp to create right image (simplified)
    image_right = np.zeros_like(image_left)
    
    for y in range(IMAGE_HEIGHT):
        for x in range(IMAGE_WIDTH):
            x_right = int(x - disparity[y, x])
            if 0 <= x_right < IMAGE_WIDTH:
                image_right[y, x_right] = image_left[y, x]
    
    # Fill holes dengan simple interpolation
    for y in range(IMAGE_HEIGHT):
        for x in range(1, IMAGE_WIDTH - 1):
            if np.all(image_right[y, x] == 0):
                image_right[y, x] = (image_right[y, x-1].astype(int) + 
                                     image_right[y, x+1].astype(int)) // 2
    
    # Save images
    try:
        from PIL import Image
        Image.fromarray(image_left).save(output_dir / 'left.png')
        Image.fromarray(image_right).save(output_dir / 'right.png')
        
        # Save depth as grayscale
        depth_vis = (depth * 255).astype(np.uint8)
        Image.fromarray(depth_vis).save(output_dir / 'depth.png')
        
        # Save disparity
        disp_vis = (disparity / disparity.max() * 255).astype(np.uint8)
        Image.fromarray(disp_vis).save(output_dir / 'disparity.png')
    except ImportError:
        save_ppm(image_left, output_dir / 'left.ppm')
        save_ppm(image_right, output_dir / 'right.ppm')
    
    # Save metadata
    metadata = {
        'baseline': baseline,
        'image_size': [IMAGE_WIDTH, IMAGE_HEIGHT],
        'focal_length': IMAGE_WIDTH,  # Approximate
        'description': 'Synthetic stereo pair for view interpolation'
    }
    
    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  ✓ Left image saved")
    print(f"  ✓ Right image saved")
    print(f"  ✓ Depth map saved")
    print(f"  ✓ Disparity map saved")
    
    return output_dir

# ============================================================
# EQUIRECTANGULAR PANORAMA
# ============================================================

def generate_equirectangular(output_dir=None):
    """
    Generate synthetic equirectangular panorama.
    
    Args:
        output_dir: Output directory
    """
    if output_dir is None:
        output_dir = EQUIRECT_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[Equirectangular] Generating {EQUIRECT_WIDTH}x{EQUIRECT_HEIGHT} panorama...")
    
    # Create equirectangular image
    image = np.zeros((EQUIRECT_HEIGHT, EQUIRECT_WIDTH, 3), dtype=np.uint8)
    
    for y in range(EQUIRECT_HEIGHT):
        for x in range(EQUIRECT_WIDTH):
            # Convert to spherical coordinates
            theta = (x / EQUIRECT_WIDTH) * 2 * np.pi - np.pi  # -pi to pi
            phi = (y / EQUIRECT_HEIGHT) * np.pi - np.pi / 2   # -pi/2 to pi/2
            
            # Create simple environment
            if phi > 0.3:
                # Ground
                t = (phi - 0.3) / (np.pi / 2 - 0.3)
                image[y, x] = [int(80 + 40 * t), int(120 + 30 * t), int(60 + 20 * t)]
            elif phi < -0.2:
                # Sky
                t = (-phi - 0.2) / (np.pi / 2 - 0.2)
                image[y, x] = [int(135 - 50 * t), int(180 - 30 * t), 255]
            else:
                # Horizon / buildings
                building_height = 0.3 * np.sin(theta * 5) * np.sin(theta * 3)
                if phi < building_height:
                    gray = int(100 + 50 * np.sin(theta * 10))
                    image[y, x] = [gray, gray - 10, gray - 20]
                else:
                    # Mountains
                    gray = int(70 + 30 * np.sin(theta * 2))
                    image[y, x] = [gray, gray + 20, gray]
    
    # Add sun
    sun_theta, sun_phi = 0.5, -0.3
    sun_x = int((sun_theta + np.pi) / (2 * np.pi) * EQUIRECT_WIDTH)
    sun_y = int((sun_phi + np.pi / 2) / np.pi * EQUIRECT_HEIGHT)
    
    for dy in range(-30, 31):
        for dx in range(-30, 31):
            if dx**2 + dy**2 < 30**2:
                nx, ny = sun_x + dx, sun_y + dy
                if 0 <= nx < EQUIRECT_WIDTH and 0 <= ny < EQUIRECT_HEIGHT:
                    t = 1 - np.sqrt(dx**2 + dy**2) / 30
                    image[ny, nx] = [255, int(255 - 50 * (1-t)), int(200 * t)]
    
    # Save
    try:
        from PIL import Image
        Image.fromarray(image).save(output_dir / 'equirectangular.jpg', quality=95)
        print(f"  ✓ Saved: equirectangular.jpg")
    except ImportError:
        save_ppm(image, output_dir / 'equirectangular.ppm')
        print(f"  ✓ Saved: equirectangular.ppm")
    
    # Save metadata
    metadata = {
        'width': EQUIRECT_WIDTH,
        'height': EQUIRECT_HEIGHT,
        'projection': 'equirectangular',
        'fov_horizontal': 360,
        'fov_vertical': 180,
        'description': 'Synthetic equirectangular panorama for view rendering'
    }
    
    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return output_dir

# ============================================================
# MULTI-VIEW GENERATION
# ============================================================

def generate_multiview_dataset(num_views=8, output_dir=None):
    """
    Generate multi-view images of a synthetic scene.
    
    Args:
        num_views: Jumlah views
        output_dir: Output directory
    """
    if output_dir is None:
        output_dir = MULTIVIEW_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[Multi-view] Generating {num_views} views...")
    
    # Camera positions around a central point
    camera_positions = []
    camera_angles = []
    
    for i in range(num_views):
        angle = i * 2 * np.pi / num_views
        camera_positions.append({
            'x': np.cos(angle) * 2,
            'y': 0.5,
            'z': np.sin(angle) * 2
        })
        camera_angles.append({
            'yaw': -angle + np.pi,  # Look at center
            'pitch': -0.1,
            'roll': 0
        })
    
    # Generate views (simplified - just shifted versions)
    for i in range(num_views):
        image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
        
        # Background gradient based on view angle
        angle = i * 2 * np.pi / num_views
        r = int(128 + 127 * np.cos(angle))
        g = int(128 + 127 * np.cos(angle + 2*np.pi/3))
        b = int(128 + 127 * np.cos(angle + 4*np.pi/3))
        
        for y in range(IMAGE_HEIGHT):
            t = y / IMAGE_HEIGHT
            image[y, :] = [
                int(r * (1 - 0.3 * t)),
                int(g * (1 - 0.3 * t)),
                int(b * (1 - 0.3 * t))
            ]
        
        # Add central object (appears different from each view)
        cx = IMAGE_WIDTH // 2 + int(50 * np.sin(angle))
        cy = IMAGE_HEIGHT // 2
        
        for dy in range(-40, 41):
            for dx in range(-40, 41):
                if dx**2 + dy**2 < 40**2:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < IMAGE_WIDTH and 0 <= ny < IMAGE_HEIGHT:
                        # View-dependent color
                        side_factor = 0.5 + 0.5 * np.cos(np.arctan2(dy, dx) - angle)
                        gray = int(200 * side_factor)
                        image[ny, nx] = [gray, gray, int(gray * 0.8)]
        
        # Save
        try:
            from PIL import Image as PILImage
            PILImage.fromarray(image).save(output_dir / f'view_{i:03d}.png')
        except ImportError:
            save_ppm(image, output_dir / f'view_{i:03d}.ppm')
        
        print(f"  ✓ View {i}: angle={np.degrees(angle):.1f}°")
    
    # Save camera parameters
    cameras = {
        'num_views': num_views,
        'cameras': []
    }
    
    for i in range(num_views):
        cameras['cameras'].append({
            'id': i,
            'position': camera_positions[i],
            'rotation': camera_angles[i],
            'focal_length': IMAGE_WIDTH,
            'image_size': [IMAGE_WIDTH, IMAGE_HEIGHT]
        })
    
    with open(output_dir / 'cameras.json', 'w') as f:
        json.dump(cameras, f, indent=2)
    
    print(f"  ✓ Camera parameters saved")
    
    return output_dir

# ============================================================
# MAIN
# ============================================================

def main():
    """Generate semua sample data."""
    print("="*60)
    print("DOWNLOAD SAMPLE DATA: BAB 14 - IMAGE-BASED RENDERING")
    print("="*60)
    
    # Check dependencies
    deps = check_dependencies()
    
    # Setup directories
    setup_directories()
    
    # Generate data
    print("\n" + "-"*60)
    print("Generating Sample Data...")
    print("-"*60)
    
    # 1. Panorama sequence
    generate_panorama_sequence(num_images=6, overlap_ratio=0.3)
    
    # 2. Stereo pair
    generate_stereo_pair(baseline=30)
    
    # 3. Equirectangular
    generate_equirectangular()
    
    # 4. Multi-view
    generate_multiview_dataset(num_views=8)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\nData tersimpan di: {DATA_DIR}")
    print("\nStruktur direktori:")
    print(f"  {PANORAMA_DIR.relative_to(BASE_DIR)}/")
    print(f"    - panorama_*.png (6 images)")
    print(f"    - metadata.json")
    print(f"  {STEREO_DIR.relative_to(BASE_DIR)}/")
    print(f"    - left.png, right.png")
    print(f"    - depth.png, disparity.png")
    print(f"    - metadata.json")
    print(f"  {EQUIRECT_DIR.relative_to(BASE_DIR)}/")
    print(f"    - equirectangular.jpg")
    print(f"    - metadata.json")
    print(f"  {MULTIVIEW_DIR.relative_to(BASE_DIR)}/")
    print(f"    - view_*.png (8 images)")
    print(f"    - cameras.json")
    
    print("\n" + "="*60)
    print("SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
