"""
Praktikum 14.3: Cylindrical and Spherical Projection
=====================================================

Program ini mendemonstrasikan proyeksi gambar:
1. Cylindrical projection
2. Spherical (equirectangular) projection
3. Inverse projection
4. 360-degree panorama

Teori:
------
Projection transforms planar images ke curved surfaces
untuk membuat panorama yang lebih natural.

Cylindrical: x' = f * atan(x/f), y' = f * y / sqrt(x² + f²)
Spherical: longitude θ = atan(x/f), latitude φ = atan(y/sqrt(x² + f²))

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
OUTPUT_DIR = Path(__file__).parent / "output" / "output3"

# Projection parameters
DEFAULT_FOV = 60                    # Field of view dalam derajat
EQUIRECTANGULAR_WIDTH = 2048        # Width panorama output
EQUIRECTANGULAR_HEIGHT = 1024       # Height panorama output (2:1 ratio)

# Sampling parameters
INTERPOLATION = 'bilinear'          # 'nearest', 'bilinear', 'bicubic'

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

def load_image(filename=None):
    """Load gambar untuk projection."""
    import cv2
    
    if filename:
        filepath = DATA_DIR / filename
        if filepath.exists():
            return cv2.imread(str(filepath))
    
    # Create sample image
    print("  Membuat sample image...")
    return create_sample_image()

def create_sample_image():
    """Buat sample image dengan grid dan features."""
    import cv2
    
    h, w = 600, 800
    img = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Background gradient
    for y in range(h):
        for x in range(w):
            b = int(200 * (1 - y / h))
            g = int(100 + 100 * np.sin(x / w * np.pi))
            r = int(50 + 150 * x / w)
            img[y, x] = [b, g, r]
    
    # Grid lines
    for x in range(0, w, 50):
        cv2.line(img, (x, 0), (x, h), (255, 255, 255), 1)
    for y in range(0, h, 50):
        cv2.line(img, (0, y), (w, y), (255, 255, 255), 1)
    
    # Features
    np.random.seed(42)
    for _ in range(30):
        x = np.random.randint(50, w-50)
        y = np.random.randint(50, h-50)
        size = np.random.randint(10, 30)
        color = [np.random.randint(0, 255) for _ in range(3)]
        cv2.circle(img, (x, y), size, color, -1)
    
    # Text
    cv2.putText(img, "Sample Image for Projection", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

def load_equirectangular(filename=None):
    """Load equirectangular panorama."""
    import cv2
    
    if filename:
        filepath = DATA_DIR / "equirectangular" / filename
        if filepath.exists():
            return cv2.imread(str(filepath))
    
    # Try default
    default_path = DATA_DIR / "equirectangular"
    if default_path.exists():
        files = list(default_path.glob("*.jpg")) + list(default_path.glob("*.png"))
        if files:
            return cv2.imread(str(files[0]))
    
    # Create sample
    print("  Membuat sample equirectangular...")
    return create_sample_equirectangular()

def create_sample_equirectangular():
    """Buat sample equirectangular panorama."""
    import cv2
    
    h, w = EQUIRECTANGULAR_HEIGHT, EQUIRECTANGULAR_WIDTH
    img = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Create environment
    for y in range(h):
        for x in range(w):
            # Convert to spherical coordinates
            theta = (x / w) * 2 * np.pi - np.pi  # longitude
            phi = (y / h) * np.pi - np.pi/2       # latitude
            
            # Sky/ground gradient
            if phi < 0:  # Above horizon
                # Sky
                t = -phi / (np.pi/2)
                b = int(255 * t)
                g = int(150 * t)
                r = int(100 * t)
            else:  # Below horizon
                # Ground
                t = phi / (np.pi/2)
                b = int(50 + 50 * t)
                g = int(100 + 50 * t)
                r = int(80 + 50 * t)
            
            img[y, x] = [b, g, r]
    
    # Add features
    # Sun
    sun_theta = 0
    sun_phi = -0.3
    sun_x = int((sun_theta + np.pi) / (2 * np.pi) * w)
    sun_y = int((sun_phi + np.pi/2) / np.pi * h)
    cv2.circle(img, (sun_x, sun_y), 50, (0, 200, 255), -1)
    
    # Buildings at different positions
    for i in range(8):
        theta = i * np.pi / 4
        x = int((theta + np.pi) / (2 * np.pi) * w) % w
        
        # Simple building
        building_h = np.random.randint(100, 200)
        y_start = h // 2
        y_end = min(y_start + building_h, h)
        width = np.random.randint(40, 80)
        
        color = [np.random.randint(50, 150) for _ in range(3)]
        cv2.rectangle(img, (x - width//2, y_start), (x + width//2, y_end), color, -1)
    
    # Grid lines untuk longitude/latitude
    for lon in range(-180, 180, 30):
        x = int((lon + 180) / 360 * w)
        cv2.line(img, (x, 0), (x, h), (100, 100, 100), 1)
    for lat in range(-60, 61, 30):
        y = int((lat + 90) / 180 * h)
        cv2.line(img, (0, y), (w, y), (100, 100, 100), 1)
    
    # Labels
    cv2.putText(img, "FRONT", (w//2 - 40, h//2 + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, "BACK", (w - 80, h//2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, "BACK", (10, h//2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

# ============================================================
# CYLINDRICAL PROJECTION
# ============================================================

def cylindrical_projection(img, focal_length=None):
    """
    Project planar image ke cylindrical surface.
    
    Args:
        img: Input image (planar)
        focal_length: Focal length dalam pixels (default: image width)
    
    Returns:
        Cylindrical projected image, mask
    """
    import cv2
    
    h, w = img.shape[:2]
    
    if focal_length is None:
        focal_length = w
    
    # Create output coordinates
    y_i, x_i = np.indices((h, w))
    
    # Center
    xc = w / 2
    yc = h / 2
    
    # Convert to cylindrical (normalized coordinates)
    # theta = arctan((x - xc) / f)
    # y_cyl = (y - yc) / sqrt((x - xc)² + f²)
    
    theta = np.arctan((x_i - xc) / focal_length)
    
    # Pada cylindrical projection, y di-scale berdasarkan cos(theta)
    denominator = np.sqrt((x_i - xc)**2 + focal_length**2)
    y_cyl = (y_i - yc) * focal_length / denominator
    
    # Convert back ke image coordinates
    x_proj = focal_length * theta + xc
    y_proj = y_cyl + yc
    
    # Remap
    x_proj = x_proj.astype(np.float32)
    y_proj = y_proj.astype(np.float32)
    
    # Create warped image
    warped = cv2.remap(img, x_proj, y_proj, cv2.INTER_LINEAR, 
                       borderMode=cv2.BORDER_CONSTANT)
    
    # Create mask
    mask = cv2.remap(np.ones((h, w), dtype=np.uint8) * 255,
                     x_proj, y_proj, cv2.INTER_LINEAR)
    
    return warped, mask

def inverse_cylindrical_projection(img, focal_length=None):
    """
    Project dari cylindrical kembali ke planar.
    
    Args:
        img: Cylindrical image
        focal_length: Focal length
    
    Returns:
        Planar image
    """
    import cv2
    
    h, w = img.shape[:2]
    
    if focal_length is None:
        focal_length = w
    
    # Center
    xc = w / 2
    yc = h / 2
    
    # Create coordinate grid
    y_i, x_i = np.indices((h, w))
    
    # theta dari cylindrical x coordinate
    theta = (x_i - xc) / focal_length
    
    # Original x
    x_orig = focal_length * np.tan(theta) + xc
    
    # Original y (inverse of cylindrical y transform)
    cos_theta = np.cos(theta)
    y_orig = (y_i - yc) / cos_theta + yc
    
    # Remap
    x_orig = x_orig.astype(np.float32)
    y_orig = y_orig.astype(np.float32)
    
    result = cv2.remap(img, x_orig, y_orig, cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_CONSTANT)
    
    return result

# ============================================================
# SPHERICAL PROJECTION
# ============================================================

def spherical_projection(img, focal_length=None):
    """
    Project planar image ke spherical surface.
    
    Args:
        img: Input planar image
        focal_length: Focal length dalam pixels
    
    Returns:
        Spherical projected image, mask
    """
    import cv2
    
    h, w = img.shape[:2]
    
    if focal_length is None:
        focal_length = w
    
    # Center
    xc = w / 2
    yc = h / 2
    
    # Create coordinate grid
    y_i, x_i = np.indices((h, w))
    
    # Spherical coordinates
    # theta (longitude) = arctan((x - xc) / f)
    # phi (latitude) = arctan((y - yc) / sqrt((x - xc)² + f²))
    
    theta = np.arctan((x_i - xc) / focal_length)
    
    denominator = np.sqrt((x_i - xc)**2 + focal_length**2)
    phi = np.arctan((y_i - yc) / denominator)
    
    # Convert back to image coordinates
    x_proj = focal_length * theta + xc
    y_proj = focal_length * phi + yc
    
    # Remap
    x_proj = x_proj.astype(np.float32)
    y_proj = y_proj.astype(np.float32)
    
    warped = cv2.remap(img, x_proj, y_proj, cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_CONSTANT)
    
    mask = cv2.remap(np.ones((h, w), dtype=np.uint8) * 255,
                     x_proj, y_proj, cv2.INTER_LINEAR)
    
    return warped, mask

# ============================================================
# EQUIRECTANGULAR PROJECTION
# ============================================================

def equirectangular_to_perspective(equirect, fov, theta, phi, output_size=(640, 480)):
    """
    Extract perspective view dari equirectangular panorama.
    
    Args:
        equirect: Equirectangular panorama (2:1 aspect ratio)
        fov: Field of view dalam degrees
        theta: Horizontal rotation (yaw) dalam degrees
        phi: Vertical rotation (pitch) dalam degrees
        output_size: Output image size (width, height)
    
    Returns:
        Perspective view
    """
    import cv2
    
    h_eq, w_eq = equirect.shape[:2]
    out_w, out_h = output_size
    
    # Convert angles ke radians
    fov_rad = np.radians(fov)
    theta_rad = np.radians(theta)
    phi_rad = np.radians(phi)
    
    # Focal length dari FOV
    f = out_w / (2 * np.tan(fov_rad / 2))
    
    # Create output coordinate grid
    y_i, x_i = np.indices((out_h, out_w))
    
    # Center
    xc = out_w / 2
    yc = out_h / 2
    
    # Direction vectors dalam camera space
    x_cam = (x_i - xc)
    y_cam = (y_i - yc)
    z_cam = np.ones((out_h, out_w)) * f
    
    # Normalize
    norm = np.sqrt(x_cam**2 + y_cam**2 + z_cam**2)
    x_cam /= norm
    y_cam /= norm
    z_cam /= norm
    
    # Rotation matrices
    # Rotate around Y (yaw - theta)
    Ry = np.array([
        [np.cos(theta_rad), 0, np.sin(theta_rad)],
        [0, 1, 0],
        [-np.sin(theta_rad), 0, np.cos(theta_rad)]
    ])
    
    # Rotate around X (pitch - phi)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(phi_rad), -np.sin(phi_rad)],
        [0, np.sin(phi_rad), np.cos(phi_rad)]
    ])
    
    # Combined rotation
    R = Ry @ Rx
    
    # Apply rotation
    dirs = np.stack([x_cam, y_cam, z_cam], axis=-1)
    dirs_rot = np.einsum('ij,hwj->hwi', R, dirs)
    
    x_world = dirs_rot[:, :, 0]
    y_world = dirs_rot[:, :, 1]
    z_world = dirs_rot[:, :, 2]
    
    # Convert ke spherical coordinates
    lon = np.arctan2(x_world, z_world)  # -pi to pi
    lat = np.arcsin(np.clip(y_world, -1, 1))  # -pi/2 to pi/2
    
    # Map ke equirectangular coordinates
    u = ((lon + np.pi) / (2 * np.pi) * w_eq).astype(np.float32)
    v = ((np.pi/2 - lat) / np.pi * h_eq).astype(np.float32)
    
    # Handle wrap-around
    u = u % w_eq
    
    # Remap
    result = cv2.remap(equirect, u, v, cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_WRAP)
    
    return result

def perspective_to_equirectangular(images, fovs, orientations, output_size=(2048, 1024)):
    """
    Combine multiple perspective images ke equirectangular.
    
    Args:
        images: List of perspective images
        fovs: List of FOV untuk setiap image
        orientations: List of (theta, phi) untuk setiap image
        output_size: Output equirectangular size
    
    Returns:
        Equirectangular panorama
    """
    import cv2
    
    out_w, out_h = output_size
    result = np.zeros((out_h, out_w, 3), dtype=np.float32)
    weight_sum = np.zeros((out_h, out_w), dtype=np.float32)
    
    for img, fov, (theta, phi) in zip(images, fovs, orientations):
        # Project setiap image
        h_img, w_img = img.shape[:2]
        
        # Create coordinate grid
        y_i, x_i = np.indices((out_h, out_w))
        
        # Convert ke spherical
        lon = (x_i / out_w * 2 - 1) * np.pi
        lat = (0.5 - y_i / out_h) * np.pi
        
        # Direction vectors
        x_world = np.cos(lat) * np.sin(lon)
        y_world = np.sin(lat)
        z_world = np.cos(lat) * np.cos(lon)
        
        # Inverse rotation
        theta_rad = np.radians(theta)
        phi_rad = np.radians(phi)
        
        Ry_inv = np.array([
            [np.cos(theta_rad), 0, -np.sin(theta_rad)],
            [0, 1, 0],
            [np.sin(theta_rad), 0, np.cos(theta_rad)]
        ])
        
        Rx_inv = np.array([
            [1, 0, 0],
            [0, np.cos(phi_rad), np.sin(phi_rad)],
            [0, -np.sin(phi_rad), np.cos(phi_rad)]
        ])
        
        R_inv = Rx_inv @ Ry_inv
        
        dirs = np.stack([x_world, y_world, z_world], axis=-1)
        dirs_cam = np.einsum('ij,hwj->hwi', R_inv, dirs)
        
        x_cam = dirs_cam[:, :, 0]
        y_cam = dirs_cam[:, :, 1]
        z_cam = dirs_cam[:, :, 2]
        
        # Only points in front of camera
        mask = z_cam > 0
        
        # Project to image plane
        fov_rad = np.radians(fov)
        f = w_img / (2 * np.tan(fov_rad / 2))
        
        x_img = (x_cam / z_cam * f + w_img / 2)
        y_img = (y_cam / z_cam * f + h_img / 2)
        
        # Check bounds
        valid = mask & (x_img >= 0) & (x_img < w_img) & (y_img >= 0) & (y_img < h_img)
        
        # Sample image
        x_img = np.clip(x_img, 0, w_img - 1).astype(np.float32)
        y_img = np.clip(y_img, 0, h_img - 1).astype(np.float32)
        
        sampled = cv2.remap(img.astype(np.float32), x_img, y_img, cv2.INTER_LINEAR)
        
        # Add with weight
        weight = valid.astype(np.float32)
        
        for c in range(3):
            result[:, :, c] += sampled[:, :, c] * weight
        weight_sum += weight
    
    # Normalize
    weight_sum = np.maximum(weight_sum, 1e-10)
    for c in range(3):
        result[:, :, c] /= weight_sum
    
    return result.astype(np.uint8)

# ============================================================
# CUBEMAP
# ============================================================

def equirectangular_to_cubemap(equirect, face_size=512):
    """
    Convert equirectangular ke cubemap (6 faces).
    
    Args:
        equirect: Equirectangular panorama
        face_size: Size of each cube face
    
    Returns:
        Dictionary dengan 6 faces
    """
    import cv2
    
    faces = {}
    
    # Orientations untuk setiap face
    face_orientations = {
        'front':  (0, 0),
        'right':  (90, 0),
        'back':   (180, 0),
        'left':   (-90, 0),
        'top':    (0, 90),
        'bottom': (0, -90)
    }
    
    for name, (theta, phi) in face_orientations.items():
        face = equirectangular_to_perspective(equirect, 90, theta, phi, 
                                               (face_size, face_size))
        faces[name] = face
    
    return faces

def cubemap_to_equirectangular(faces, output_size=(2048, 1024)):
    """
    Convert cubemap ke equirectangular.
    
    Args:
        faces: Dictionary dengan 6 faces
        output_size: Output size (width, height)
    
    Returns:
        Equirectangular panorama
    """
    images = []
    fovs = []
    orientations = []
    
    face_orientations = {
        'front':  (0, 0),
        'right':  (90, 0),
        'back':   (180, 0),
        'left':   (-90, 0),
        'top':    (0, 90),
        'bottom': (0, -90)
    }
    
    for name, (theta, phi) in face_orientations.items():
        if name in faces:
            images.append(faces[name])
            fovs.append(90)
            orientations.append((theta, phi))
    
    return perspective_to_equirectangular(images, fovs, orientations, output_size)

# ============================================================
# VISUALISASI
# ============================================================

def visualize_projection_difference(original, projected, title="Projection"):
    """Visualisasi perbedaan original dan projected image."""
    import cv2
    
    # Resize jika perlu
    h1, w1 = original.shape[:2]
    h2, w2 = projected.shape[:2]
    
    target_h = min(h1, h2, 400)
    scale1 = target_h / h1
    scale2 = target_h / h2
    
    img1 = cv2.resize(original, None, fx=scale1, fy=scale1)
    img2 = cv2.resize(projected, None, fx=scale2, fy=scale2)
    
    # Gabungkan
    h = img1.shape[0]
    w1 = img1.shape[1]
    w2 = img2.shape[1]
    
    combined = np.zeros((h, w1 + w2 + 20, 3), dtype=np.uint8)
    combined[:, :w1] = img1
    combined[:, w1+20:w1+20+w2] = img2
    
    # Labels
    cv2.putText(combined, "Original", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(combined, title, (w1 + 30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return combined

# ============================================================
# DEMONSTRASI
# ============================================================

def demo_cylindrical_projection():
    """Demo cylindrical projection."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 1: Cylindrical Projection")
    print("="*60)
    
    # Load image
    img = load_image()
    print(f"\n  Input: {img.shape}")
    
    # Test dengan berbagai focal lengths
    focal_lengths = [img.shape[1] * 0.5, img.shape[1], img.shape[1] * 2]
    
    results = []
    for f in focal_lengths:
        print(f"\n  Focal length: {f:.0f}")
        
        warped, mask = cylindrical_projection(img, f)
        results.append(warped)
        
        # Save
        filename = f"cylindrical_f{int(f)}.jpg"
        cv2.imwrite(str(OUTPUT_DIR / filename), warped)
        print(f"  ✓ Saved: {filename}")
    
    return results

def demo_spherical_projection():
    """Demo spherical projection."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 2: Spherical Projection")
    print("="*60)
    
    # Load image
    img = load_image()
    print(f"\n  Input: {img.shape}")
    
    # Project
    f = img.shape[1]
    warped, mask = spherical_projection(img, f)
    
    cv2.imwrite(str(OUTPUT_DIR / "spherical_projection.jpg"), warped)
    print(f"\n  ✓ Saved: spherical_projection.jpg")
    
    # Compare
    comparison = visualize_projection_difference(img, warped, "Spherical")
    cv2.imwrite(str(OUTPUT_DIR / "spherical_comparison.jpg"), comparison)
    
    return warped

def demo_equirectangular_extraction():
    """Demo extracting views dari equirectangular panorama."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 3: Equirectangular View Extraction")
    print("="*60)
    
    # Load equirectangular
    equirect = load_equirectangular()
    print(f"\n  Equirectangular: {equirect.shape}")
    
    cv2.imwrite(str(OUTPUT_DIR / "equirectangular_building.jpg"), equirect)
    
    # Extract views di berbagai orientasi
    views = [
        ("front", 0, 0),
        ("right", 90, 0),
        ("back", 180, 0),
        ("left", -90, 0),
        ("up", 0, 45),
        ("down", 0, -45),
    ]
    
    extracted = {}
    for name, theta, phi in views:
        print(f"\n  Extracting {name} (θ={theta}°, φ={phi}°)...")
        
        view = equirectangular_to_perspective(equirect, 90, theta, phi)
        extracted[name] = view
        
        filename = f"view_{name}.jpg"
        cv2.imwrite(str(OUTPUT_DIR / filename), view)
        print(f"  ✓ Saved: {filename}")
    
    return extracted

def demo_cubemap_conversion():
    """Demo cubemap conversion."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 4: Cubemap Conversion")
    print("="*60)
    
    # Load equirectangular
    equirect = load_equirectangular()
    print(f"\n  Input: {equirect.shape}")
    
    # Convert ke cubemap
    print("\n  Converting to cubemap...")
    faces = equirectangular_to_cubemap(equirect, 512)
    
    # Save faces
    for name, face in faces.items():
        filename = f"cubemap_{name}.jpg"
        cv2.imwrite(str(OUTPUT_DIR / filename), face)
        print(f"  ✓ Saved: {filename}")
    
    # Create cubemap cross layout
    face_size = 512
    cross = np.zeros((face_size * 3, face_size * 4, 3), dtype=np.uint8)
    
    # Layout:
    #       [top]
    # [left][front][right][back]
    #       [bottom]
    
    positions = {
        'top':    (1, 0),
        'left':   (0, 1),
        'front':  (1, 1),
        'right':  (2, 1),
        'back':   (3, 1),
        'bottom': (1, 2)
    }
    
    for name, (col, row) in positions.items():
        y = row * face_size
        x = col * face_size
        cross[y:y+face_size, x:x+face_size] = faces[name]
    
    cv2.imwrite(str(OUTPUT_DIR / "cubemap_cross.jpg"), cross)
    print(f"\n  ✓ Saved: cubemap_cross.jpg")
    
    return faces

def demo_interactive_view():
    """Demo interactive view dengan keyboard."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 5: Interactive 360° View")
    print("="*60)
    
    # Load equirectangular
    equirect = load_equirectangular()
    
    # Initial orientation
    theta = 0  # yaw
    phi = 0    # pitch
    fov = 90
    
    print("\n  Controls:")
    print("    Arrow keys: Rotate view")
    print("    +/-: Zoom in/out")
    print("    q: Quit")
    
    # Generate beberapa frame untuk demo
    frames = []
    for t in range(0, 360, 30):
        view = equirectangular_to_perspective(equirect, fov, t, 0)
        
        # Add info
        info_text = f"Theta: {t}°, Phi: 0°, FOV: {fov}°"
        cv2.putText(view, info_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        frames.append(view)
    
    # Create animation strip
    strip_h = frames[0].shape[0] // 2
    strip = []
    for frame in frames[::2]:  # Setiap 60 derajat
        resized = cv2.resize(frame, (frame.shape[1] // 2, strip_h))
        strip.append(resized)
    
    animation = np.hstack(strip)
    cv2.imwrite(str(OUTPUT_DIR / "interactive_360_demo.jpg"), animation)
    print(f"\n  ✓ Saved: interactive_360_demo.jpg")
    
    return frames

def demo_panorama_types():
    """Demo berbagai jenis panorama projections."""
    import cv2
    
    print("\n" + "="*60)
    print("DEMO 6: Panorama Projection Types")
    print("="*60)
    
    # Load equirectangular
    equirect = load_equirectangular()
    
    print("\n  Creating different projection views...")
    
    results = {
        'equirectangular': equirect
    }
    
    # Little planet (stereographic)
    print("\n  1. Little Planet projection...")
    planet_size = 800
    
    # Create coordinate grid
    y, x = np.indices((planet_size, planet_size))
    
    # Center
    xc = planet_size / 2
    yc = planet_size / 2
    r_max = planet_size / 2
    
    # Polar coordinates
    r = np.sqrt((x - xc)**2 + (y - yc)**2)
    angle = np.arctan2(y - yc, x - xc)
    
    # Stereographic projection (bottom = center)
    lat = np.pi/2 - 2 * np.arctan(r / (planet_size * 0.5))
    lon = angle
    
    # Map ke equirectangular
    h_eq, w_eq = equirect.shape[:2]
    u = ((lon + np.pi) / (2 * np.pi) * w_eq).astype(np.float32)
    v = ((np.pi/2 - lat) / np.pi * h_eq).astype(np.float32)
    
    u = u % w_eq
    v = np.clip(v, 0, h_eq - 1)
    
    little_planet = cv2.remap(equirect, u, v, cv2.INTER_LINEAR)
    
    # Mask outside circle
    mask = r > r_max
    little_planet[mask] = 0
    
    results['little_planet'] = little_planet
    cv2.imwrite(str(OUTPUT_DIR / "little_planet.jpg"), little_planet)
    print(f"  ✓ Saved: little_planet.jpg")
    
    # Crystal ball (reverse stereographic)
    print("\n  2. Crystal Ball projection...")
    
    lat = -np.pi/2 + 2 * np.arctan(r / (planet_size * 0.5))
    u = ((lon + np.pi) / (2 * np.pi) * w_eq).astype(np.float32)
    v = ((np.pi/2 - lat) / np.pi * h_eq).astype(np.float32)
    
    u = u % w_eq
    v = np.clip(v, 0, h_eq - 1)
    
    crystal_ball = cv2.remap(equirect, u, v, cv2.INTER_LINEAR)
    crystal_ball[mask] = 0
    
    results['crystal_ball'] = crystal_ball
    cv2.imwrite(str(OUTPUT_DIR / "crystal_ball.jpg"), crystal_ball)
    print(f"  ✓ Saved: crystal_ball.jpg")
    
    return results

# ============================================================
# MAIN
# ============================================================

def main():
    """Fungsi utama program."""
    import cv2
    
    print("="*60)
    print("PRAKTIKUM 14.3: CYLINDRICAL & SPHERICAL PROJECTION")
    print("="*60)
    
    # Check dependencies
    if not check_opencv():
        return
    
    # Setup
    setup_directories()
    
    # Run demos
    demo_cylindrical_projection()
    
    demo_spherical_projection()
    
    demo_equirectangular_extraction()
    
    demo_cubemap_conversion()
    
    demo_interactive_view()
    
    demo_panorama_types()
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN")
    print("="*60)
    
    print("\nProjection Types:")
    print("  1. Cylindrical: x' = f·arctan(x/f)")
    print("  2. Spherical: Uses both θ (longitude) dan φ (latitude)")
    print("  3. Equirectangular: 2:1 full 360° representation")
    print("  4. Cubemap: 6 faces of 90° FOV")
    print("  5. Little Planet: Stereographic dari bawah")
    
    print("\nApplications:")
    print("  - Panorama stitching (cylindrical)")
    print("  - VR/360° video (equirectangular)")
    print("  - Game environments (cubemap)")
    print("  - Artistic effects (little planet)")
    
    print(f"\nOutput tersimpan di: {OUTPUT_DIR}")
    
    print("\n" + "="*60)
    print("PRAKTIKUM SELESAI")
    print("="*60)

if __name__ == "__main__":
    main()
