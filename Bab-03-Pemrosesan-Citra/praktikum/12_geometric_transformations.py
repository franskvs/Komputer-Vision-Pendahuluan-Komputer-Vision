# ============================================================
# PROGRAM: 12_geometric_transformations.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Geometric Transformations dan Image Warping
# 
# Tujuan Pembelajaran:
#   1. Memahami parametric transformations (2D, 3D, projective)
#   2. Implementasi forward dan inverse warping
#   3. Aplikasi: image rectification, registration, morphing
#   4. Memahami interpolation methods
# 
# Teori Transformasi:
#   - Translation: x' = x + t
#   - Rotation: [x', y'] = R * [x, y]
#   - Similarity: scale + rotate + translate (4 DoF)
#   - Affine: parallel lines stay parallel (6 DoF)
#   - Perspective: simulate 3D projection (8 DoF)
# 
# Formula Umum:
#   Affine: x' = Ax + t
#   Perspective: x' = Hx (homogeneous coordinates)
# ============================================================

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor komponen dari modul matplotlib.patches.
from matplotlib.patches import Rectangle, Circle
# Keterangan: Impor modul math.
import math

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# Rotation parameters
# Keterangan: Inisialisasi atau perbarui variabel ROTATION_ANGLE.
ROTATION_ANGLE = 30        # Derajat
# Keterangan: Inisialisasi atau perbarui variabel ROTATION_SCALE.
ROTATION_SCALE = 1.0       # Scale factor

# Translation parameters
# Keterangan: Inisialisasi atau perbarui variabel TRANSLATE_X.
TRANSLATE_X = 50           # Pixels kanan
# Keterangan: Inisialisasi atau perbarui variabel TRANSLATE_Y.
TRANSLATE_Y = 30           # Pixels bawah

# Perspective parameters
# Keterangan: Inisialisasi atau perbarui variabel PERSP_INTENSITY.
PERSP_INTENSITY = 0.0003   # Perspective distortion amount

# Interpolation method
# Keterangan: Inisialisasi atau perbarui variabel INTERP_METHOD.
INTERP_METHOD = cv2.INTER_LINEAR  # INTER_NEAREST, INTER_LINEAR, INTER_CUBIC

# Border handling
# Keterangan: Inisialisasi atau perbarui variabel BORDER_MODE.
BORDER_MODE = cv2.BORDER_CONSTANT  # BORDER_REPLICATE, BORDER_REFLECT, BORDER_WRAP
# Keterangan: Inisialisasi atau perbarui variabel BORDER_VALUE.
BORDER_VALUE = 0

# ============================================================
# FUNGSI TRANSFORMASI DASAR
# ============================================================

# Keterangan: Definisikan fungsi apply_translation.
def apply_translation(image, tx, ty):
    """
    Translation: geser image
    
    Formula: x' = x + tx, y' = y + ty
    
    Parameter:
    - image: input image
    - tx, ty: translation vector
    
    Return:
    - translated image
    """
    # Keterangan: Jalankan perintah berikut.
    print(f"➡️  Translation: ({tx}, {ty})")
    
    # Translation matrix (affine 2×3)
    # Keterangan: Inisialisasi atau perbarui variabel M.
    M = np.float32([
        # Keterangan: Jalankan perintah berikut.
        [1, 0, tx],
        # Keterangan: Jalankan perintah berikut.
        [0, 1, ty]
    # Keterangan: Jalankan perintah berikut.
    ])
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    
    # Apply warpAffine
    # Keterangan: Terapkan transformasi affine pada gambar.
    result = cv2.warpAffine(image, M, (w, h), 
                           # Keterangan: Inisialisasi atau perbarui variabel flags.
                           flags=INTERP_METHOD,
                           # Keterangan: Inisialisasi atau perbarui variabel borderMode.
                           borderMode=BORDER_MODE,
                           # Keterangan: Inisialisasi atau perbarui variabel borderValue.
                           borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi apply_rotation.
def apply_rotation(image, angle, center=None, scale=1.0):
    """
    Rotation: putar image
    
    Formula: 
    [x']   [cos(θ)  -sin(θ)] [x - cx]   [cx]
    [y'] = [sin(θ)   cos(θ)] [y - cy] + [cy]
    
    Parameter:
    - image: input image
    - angle: rotation angle (degrees, counter-clockwise)
    - center: rotation center (cx, cy), default = image center
    - scale: scale factor
    
    Return:
    - rotated image
    """
    # Keterangan: Inisialisasi atau perbarui variabel print(f"🔄 Rotation: {angle}° @ scale.
    print(f"🔄 Rotation: {angle}° @ scale={scale}")
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    
    # Keterangan: Cek kondisi center is None.
    if center is None:
        # Keterangan: Inisialisasi atau perbarui variabel center.
        center = (w // 2, h // 2)
    
    # Get rotation matrix
    # Keterangan: Inisialisasi atau perbarui variabel M.
    M = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Apply warpAffine
    # Keterangan: Terapkan transformasi affine pada gambar.
    result = cv2.warpAffine(image, M, (w, h),
                           # Keterangan: Inisialisasi atau perbarui variabel flags.
                           flags=INTERP_METHOD,
                           # Keterangan: Inisialisasi atau perbarui variabel borderMode.
                           borderMode=BORDER_MODE,
                           # Keterangan: Inisialisasi atau perbarui variabel borderValue.
                           borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi apply_affine.
def apply_affine(image, src_pts, dst_pts):
    """
    Affine transformation menggunakan 3 point pairs
    
    Affine: parallel lines stay parallel
    - Translation, rotation, scale, shear
    - 6 degrees of freedom
    - Needs 3 point correspondences
    
    Parameter:
    - image: input image
    - src_pts: 3 source points np.array([[x1,y1], [x2,y2], [x3,y3]])
    - dst_pts: 3 destination points
    
    Return:
    - warped image
    """
    # Keterangan: Jalankan perintah berikut.
    print("🔷 Affine transformation (3 points)...")
    
    # Get affine matrix
    # Keterangan: Inisialisasi atau perbarui variabel M.
    M = cv2.getAffineTransform(src_pts.astype(np.float32), 
                               # Keterangan: Jalankan perintah berikut.
                               dst_pts.astype(np.float32))
    
    # Keterangan: Jalankan perintah berikut.
    print(f"   Affine matrix:\n{M}")
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    
    # Apply warpAffine
    # Keterangan: Terapkan transformasi affine pada gambar.
    result = cv2.warpAffine(image, M, (w, h),
                           # Keterangan: Inisialisasi atau perbarui variabel flags.
                           flags=INTERP_METHOD,
                           # Keterangan: Inisialisasi atau perbarui variabel borderMode.
                           borderMode=BORDER_MODE,
                           # Keterangan: Inisialisasi atau perbarui variabel borderValue.
                           borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi apply_perspective.
def apply_perspective(image, src_pts, dst_pts):
    """
    Perspective transformation menggunakan 4 point pairs
    
    Perspective (Homography): simulate 3D viewing
    - Can represent rotation, translation, scale, shear, perspective
    - 8 degrees of freedom
    - Needs 4 point correspondences
    
    Formula: x' = Hx (homogeneous coords)
    [x']   [h11 h12 h13] [x]
    [y'] ~ [h21 h22 h23] [y]
    [w']   [h31 h32 h33] [1]
    
    Then: x = x'/w', y = y'/w'
    
    Parameter:
    - image: input image
    - src_pts: 4 source points
    - dst_pts: 4 destination points
    
    Return:
    - warped image
    """
    # Keterangan: Jalankan perintah berikut.
    print("🔶 Perspective transformation (4 points)...")
    
    # Get perspective matrix (homography)
    # Keterangan: Inisialisasi atau perbarui variabel H.
    H = cv2.getPerspectiveTransform(src_pts.astype(np.float32),
                                    # Keterangan: Jalankan perintah berikut.
                                    dst_pts.astype(np.float32))
    
    # Keterangan: Jalankan perintah berikut.
    print(f"   Homography matrix:\n{H}")
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    
    # Apply warpPerspective
    # Keterangan: Terapkan transformasi perspektif pada gambar.
    result = cv2.warpPerspective(image, H, (w, h),
                                 # Keterangan: Inisialisasi atau perbarui variabel flags.
                                 flags=INTERP_METHOD,
                                 # Keterangan: Inisialisasi atau perbarui variabel borderMode.
                                 borderMode=BORDER_MODE,
                                 # Keterangan: Inisialisasi atau perbarui variabel borderValue.
                                 borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# ============================================================
# FUNGSI INTERPOLATION
# ============================================================

# Keterangan: Definisikan fungsi compare_interpolation_methods.
def compare_interpolation_methods(image):
    """
    Bandingkan berbagai interpolation methods
    
    Methods:
    - INTER_NEAREST: closest pixel (fastest, blocky)
    - INTER_LINEAR: bilinear (fast, smooth)
    - INTER_CUBIC: bicubic (slower, smoother)
    - INTER_LANCZOS4: 8×8 neighborhood (slowest, sharpest)
    
    Parameter:
    - image: input image
    
    Return:
    - dictionary of results
    """
    # Keterangan: Jalankan perintah berikut.
    print("\n🔍 Comparing interpolation methods...")
    
    # Create small image untuk clear comparison
    # Keterangan: Ubah ukuran gambar.
    small = cv2.resize(image, (64, 64))
    
    # Rotate dengan berbagai interpolation
    # Keterangan: Inisialisasi atau perbarui variabel center.
    center = (32, 32)
    # Keterangan: Inisialisasi atau perbarui variabel angle.
    angle = 45
    # Keterangan: Inisialisasi atau perbarui variabel M.
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Keterangan: Inisialisasi atau perbarui variabel methods.
    methods = {
        # Keterangan: Jalankan perintah berikut.
        'NEAREST': cv2.INTER_NEAREST,
        # Keterangan: Jalankan perintah berikut.
        'LINEAR': cv2.INTER_LINEAR,
        # Keterangan: Jalankan perintah berikut.
        'CUBIC': cv2.INTER_CUBIC,
        # Keterangan: Jalankan perintah berikut.
        'LANCZOS4': cv2.INTER_LANCZOS4,
    # Keterangan: Jalankan perintah berikut.
    }
    
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = {}
    
    # Keterangan: Mulai loop dengan for name, method in methods.items().
    for name, method in methods.items():
        # Keterangan: Terapkan transformasi affine pada gambar.
        result = cv2.warpAffine(small, M, (64, 64), flags=method)
        
        # Upscale untuk visualization
        # Keterangan: Ubah ukuran gambar.
        result_large = cv2.resize(result, (256, 256), interpolation=cv2.INTER_NEAREST)
        
        # Keterangan: Inisialisasi atau perbarui variabel results[name].
        results[name] = result_large
        
        # Keterangan: Jalankan perintah berikut.
        print(f"   ✓ {name}")
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return results


# ============================================================
# FUNGSI IMAGE MORPHING
# ============================================================

# Keterangan: Definisikan fungsi simple_morph.
def simple_morph(img1, img2, alpha):
    """
    Simple morphing: linear blend
    
    Morph(α) = (1-α)·img1 + α·img2
    
    Parameter:
    - img1, img2: source images
    - alpha: blend factor (0=img1, 1=img2)
    
    Return:
    - morphed image
    """
    # Ensure same size
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = img1.shape[:2]
    # Keterangan: Cek kondisi img2.shape[2] != (h, w).
    if img2.shape[:2] != (h, w):
        # Keterangan: Ubah ukuran gambar.
        img2 = cv2.resize(img2, (w, h))
    
    # Linear blend
    # Keterangan: Inisialisasi atau perbarui variabel morphed.
    morphed = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return morphed


# ============================================================
# FUNGSI MESH-BASED WARPING
# ============================================================

# Keterangan: Definisikan fungsi mesh_warp_radial.
def mesh_warp_radial(image, center, strength=0.5):
    """
    Radial distortion: barrel/pincushion effect
    
    Formula:
    r = sqrt((x - cx)² + (y - cy)²)
    r' = r * (1 + k * r²)
    
    Parameter:
    - image: input image
    - center: distortion center (cx, cy)
    - strength: distortion strength (+ = barrel, - = pincushion)
    
    Return:
    - warped image
    """
    # Keterangan: Inisialisasi atau perbarui variabel print(f"🌀 Radial warp (strength.
    print(f"🌀 Radial warp (strength={strength})...")
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    # Keterangan: Inisialisasi beberapa variabel (cx, cy).
    cx, cy = center
    
    # Create coordinate grid
    # Keterangan: Inisialisasi beberapa variabel (y_coords, x_coords).
    y_coords, x_coords = np.mgrid[0:h, 0:w]
    
    # Center coordinates
    # Keterangan: Inisialisasi atau perbarui variabel x_c.
    x_c = x_coords - cx
    # Keterangan: Inisialisasi atau perbarui variabel y_c.
    y_c = y_coords - cy
    
    # Polar coordinates
    # Keterangan: Inisialisasi atau perbarui variabel r.
    r = np.sqrt(x_c**2 + y_c**2)
    # Keterangan: Inisialisasi atau perbarui variabel theta.
    theta = np.arctan2(y_c, x_c)
    
    # Radial distortion
    # Keterangan: Inisialisasi atau perbarui variabel r_distorted.
    r_distorted = r * (1 + strength * (r / max(h, w))**2)
    
    # Back to Cartesian
    # Keterangan: Inisialisasi atau perbarui variabel x_new.
    x_new = cx + r_distorted * np.cos(theta)
    # Keterangan: Inisialisasi atau perbarui variabel y_new.
    y_new = cy + r_distorted * np.sin(theta)
    
    # Remap
    # Keterangan: Remap koordinat piksel untuk warping.
    result = cv2.remap(image, x_new.astype(np.float32), y_new.astype(np.float32),
                       # Keterangan: Inisialisasi beberapa variabel (INTERP_METHOD, borderMode).
                       INTERP_METHOD, borderMode=BORDER_MODE, borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi mesh_warp_wave.
def mesh_warp_wave(image, amplitude=20, frequency=0.05, direction='horizontal'):
    """
    Wave distortion effect
    
    Parameter:
    - image: input image
    - amplitude: wave amplitude (pixels)
    - frequency: wave frequency
    - direction: 'horizontal' or 'vertical'
    
    Return:
    - warped image
    """
    # Keterangan: Inisialisasi beberapa variabel (print(f"🌊 Wave warp ({direction}, amp).
    print(f"🌊 Wave warp ({direction}, amp={amplitude}, freq={frequency})...")
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    
    # Create coordinate maps
    # Keterangan: Inisialisasi array bernilai nol.
    map_x = np.zeros((h, w), dtype=np.float32)
    # Keterangan: Inisialisasi array bernilai nol.
    map_y = np.zeros((h, w), dtype=np.float32)
    
    # Keterangan: Mulai loop dengan for y in range(h).
    for y in range(h):
        # Keterangan: Mulai loop dengan for x in range(w).
        for x in range(w):
            # Keterangan: Cek kondisi direction == 'horizontal'.
            if direction == 'horizontal':
                # Horizontal wave (x varies with y)
                # Keterangan: Inisialisasi beberapa variabel (map_x[y, x]).
                map_x[y, x] = x + amplitude * np.sin(y * frequency)
                # Keterangan: Inisialisasi beberapa variabel (map_y[y, x]).
                map_y[y, x] = y
            # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
            else:
                # Vertical wave (y varies with x)
                # Keterangan: Inisialisasi beberapa variabel (map_x[y, x]).
                map_x[y, x] = x
                # Keterangan: Inisialisasi beberapa variabel (map_y[y, x]).
                map_y[y, x] = y + amplitude * np.sin(x * frequency)
    
    # Remap
    # Keterangan: Remap koordinat piksel untuk warping.
    result = cv2.remap(image, map_x, map_y, INTERP_METHOD,
                       # Keterangan: Inisialisasi atau perbarui variabel borderMode.
                       borderMode=BORDER_MODE, borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi mesh_warp_swirl.
def mesh_warp_swirl(image, center, strength=0.01, radius=200):
    """
    Swirl effect: rotasi yang depend on radius
    
    Parameter:
    - image: input image
    - center: swirl center (cx, cy)
    - strength: swirl strength
    - radius: maximum affected radius
    
    Return:
    - warped image
    """
    # Keterangan: Inisialisasi atau perbarui variabel print(f"🌀 Swirl warp (strength.
    print(f"🌀 Swirl warp (strength={strength}, radius={radius})...")
    
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = image.shape[:2]
    # Keterangan: Inisialisasi beberapa variabel (cx, cy).
    cx, cy = center
    
    # Create coordinate maps
    # Keterangan: Inisialisasi beberapa variabel (y_coords, x_coords).
    y_coords, x_coords = np.mgrid[0:h, 0:w].astype(np.float32)
    
    # Distance dari center
    # Keterangan: Inisialisasi atau perbarui variabel dx.
    dx = x_coords - cx
    # Keterangan: Inisialisasi atau perbarui variabel dy.
    dy = y_coords - cy
    # Keterangan: Inisialisasi atau perbarui variabel r.
    r = np.sqrt(dx**2 + dy**2)
    
    # Swirl angle (depends on radius)
    # θ' = θ + strength * (radius - r) untuk r < radius
    # Keterangan: Inisialisasi atau perbarui variabel theta.
    theta = np.arctan2(dy, dx)
    
    # Apply swirl only within radius
    # Keterangan: Inisialisasi atau perbarui variabel mask.
    mask = r < radius
    # Keterangan: Inisialisasi array bernilai nol.
    swirl_amount = np.zeros_like(r)
    # Keterangan: Inisialisasi atau perbarui variabel swirl_amount[mask].
    swirl_amount[mask] = strength * (radius - r[mask])
    
    # Keterangan: Inisialisasi atau perbarui variabel theta_new.
    theta_new = theta + swirl_amount
    
    # Convert back to Cartesian
    # Keterangan: Inisialisasi atau perbarui variabel map_x.
    map_x = cx + r * np.cos(theta_new)
    # Keterangan: Inisialisasi atau perbarui variabel map_y.
    map_y = cy + r * np.sin(theta_new)
    
    # Remap
    # Keterangan: Remap koordinat piksel untuk warping.
    result = cv2.remap(image, map_x, map_y, INTERP_METHOD,
                       # Keterangan: Inisialisasi atau perbarui variabel borderMode.
                       borderMode=BORDER_MODE, borderValue=BORDER_VALUE)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_basic_transformations.
def demo_basic_transformations():
    """
    Demo 1: Basic transformations (translation, rotation)
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 1: BASIC TRANSFORMATIONS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi array bernilai satu.
    image = np.ones((300, 400, 3), dtype=np.uint8) * 200
    
    # Draw reference grid
    # Keterangan: Mulai loop dengan for i in range(0, 400, 50).
    for i in range(0, 400, 50):
        # Keterangan: Jalankan perintah berikut.
        cv2.line(image, (i, 0), (i, 300), (150, 150, 150), 1)
    # Keterangan: Mulai loop dengan for i in range(0, 300, 50).
    for i in range(0, 300, 50):
        # Keterangan: Jalankan perintah berikut.
        cv2.line(image, (0, i), (400, i), (150, 150, 150), 1)
    
    # Draw object
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (100, 80), (250, 220), (0, 0, 255), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (175, 150), 40, (0, 255, 0), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "PENS", (135, 165), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1, (255, 255, 255), 2)
    
    # Apply transformations
    # Keterangan: Inisialisasi atau perbarui variabel translated.
    translated = apply_translation(image, TRANSLATE_X, TRANSLATE_Y)
    # Keterangan: Inisialisasi atau perbarui variabel rotated.
    rotated = apply_rotation(image, ROTATION_ANGLE, scale=ROTATION_SCALE)
    
    # Combined: rotate then translate
    # Keterangan: Inisialisasi atau perbarui variabel temp.
    temp = apply_rotation(image, ROTATION_ANGLE, scale=ROTATION_SCALE)
    # Keterangan: Inisialisasi atau perbarui variabel combined.
    combined = apply_translation(temp, TRANSLATE_X, TRANSLATE_Y)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(16, 4))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 1)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Original")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 2)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(translated, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title(f"Translation\n({TRANSLATE_X}, {TRANSLATE_Y})")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 3)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title(f"Rotation\n{ROTATION_ANGLE}° @ scale={ROTATION_SCALE}")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 4)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title(f"Combined\nRotate + Translate")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Basic 2D Transformations", fontsize).
    plt.suptitle("Basic 2D Transformations", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n💡 Properties:")
    # Keterangan: Jalankan perintah berikut.
    print("   Translation: 2 DoF (tx, ty)")
    # Keterangan: Jalankan perintah berikut.
    print("   Rotation: 1 DoF (angle) + 2 for center")
    # Keterangan: Jalankan perintah berikut.
    print("   Similarity: 4 DoF (tx, ty, angle, scale)")


# Keterangan: Definisikan fungsi demo_affine_transformation.
def demo_affine_transformation():
    """
    Demo 2: Affine transformation dengan point correspondences
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 2: AFFINE TRANSFORMATION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create image
    # Keterangan: Inisialisasi array bernilai satu.
    image = np.ones((400, 400, 3), dtype=np.uint8) * 220
    
    # Draw square
    # Keterangan: Inisialisasi atau perbarui variabel pts.
    pts = np.array([[100, 100], [300, 100], [300, 300], [100, 300]], np.int32)
    # Keterangan: Jalankan perintah berikut.
    cv2.polylines(image, [pts], True, (0, 0, 255), 2)
    # Keterangan: Jalankan perintah berikut.
    cv2.fillPoly(image, [pts], (200, 200, 255))
    
    # Draw circles at corners
    # Keterangan: Mulai loop dengan for pt in pts[3]  # Only 3 points needed untuk affine.
    for pt in pts[:3]:  # Only 3 points needed untuk affine
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(image, tuple(pt), 8, (0, 255, 0), -1)
    
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "AFFINE", (150, 210), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1.2, (0, 0, 0), 2)
    
    # Define affine: shear + scale
    # Keterangan: Inisialisasi atau perbarui variabel src_pts.
    src_pts = np.array([
        # Keterangan: Jalankan perintah berikut.
        [100, 100],
        # Keterangan: Jalankan perintah berikut.
        [300, 100],
        # Keterangan: Jalankan perintah berikut.
        [100, 300]
    # Keterangan: Inisialisasi beberapa variabel (], dtype).
    ], dtype=np.float32)
    
    # Keterangan: Inisialisasi atau perbarui variabel dst_pts.
    dst_pts = np.array([
        # Keterangan: Jalankan perintah berikut.
        [120, 80],   # Move top-left
        # Keterangan: Jalankan perintah berikut.
        [320, 120],  # Move top-right (shear)
        # Keterangan: Jalankan perintah berikut.
        [80, 320]    # Move bottom-left (shear)
    # Keterangan: Inisialisasi beberapa variabel (], dtype).
    ], dtype=np.float32)
    
    # Apply
    # Keterangan: Inisialisasi atau perbarui variabel warped.
    warped = apply_affine(image, src_pts, dst_pts)
    
    # Draw destination points on warped
    # Keterangan: Inisialisasi atau perbarui variabel warped_viz.
    warped_viz = warped.copy()
    # Keterangan: Mulai loop dengan for pt in dst_pts.
    for pt in dst_pts:
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(warped_viz, tuple(pt.astype(int)), 8, (255, 0, 0), -1)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 5))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 1)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (plt.plot(src_pts[:, 0], src_pts[:, 1], 'go', markersize).
    plt.plot(src_pts[:, 0], src_pts[:, 1], 'go', markersize=10, label='Source points')
    # Keterangan: Set judul subplot.
    plt.title("Source Image\n(3 green points)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    # Keterangan: Jalankan perintah berikut.
    plt.legend()
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 2)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(warped_viz, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (plt.plot(dst_pts[:, 0], dst_pts[:, 1], 'ro', markersize).
    plt.plot(dst_pts[:, 0], dst_pts[:, 1], 'ro', markersize=10, label='Dest points')
    # Keterangan: Set judul subplot.
    plt.title("Affine Warped\n(3 red points)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    # Keterangan: Jalankan perintah berikut.
    plt.legend()
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 3)
    # Keterangan: Inisialisasi atau perbarui variabel overlay.
    overlay = cv2.addWeighted(image, 0.5, warped, 0.5, 0)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Overlay\n(Source + Warped)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Affine Transformation (6 DoF)", fontsize).
    plt.suptitle("Affine Transformation (6 DoF)", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📐 Affine Properties:")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Parallel lines stay parallel")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Ratios preserved along lines")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Needs 3 point correspondences")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Cannot simulate perspective depth")


# Keterangan: Definisikan fungsi demo_perspective_transformation.
def demo_perspective_transformation():
    """
    Demo 3: Perspective transformation (homography)
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 3: PERSPECTIVE TRANSFORMATION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create card-like image
    # Keterangan: Inisialisasi array bernilai satu.
    image = np.ones((400, 300, 3), dtype=np.uint8) * 240
    
    # Draw border
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (20, 20), (280, 380), (100, 100, 100), 3)
    
    # Draw content
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "COMPUTER", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                0.8, (0, 0, 200), 2)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "VISION", (70, 140), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1.2, (200, 0, 0), 3)
    # Keterangan: Jalankan perintah berikut.
    cv2.line(image, (40, 160), (260, 160), (0, 0, 0), 2)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "PENS 2024", (80, 220), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                0.7, (0, 0, 0), 2)
    
    # Draw corners
    # Keterangan: Inisialisasi atau perbarui variabel corners_src.
    corners_src = np.array([
        # Keterangan: Jalankan perintah berikut.
        [20, 20],
        # Keterangan: Jalankan perintah berikut.
        [280, 20],
        # Keterangan: Jalankan perintah berikut.
        [280, 380],
        # Keterangan: Jalankan perintah berikut.
        [20, 380]
    # Keterangan: Jalankan perintah berikut.
    ])
    
    # Keterangan: Mulai loop dengan for pt in corners_src.
    for pt in corners_src:
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(image, tuple(pt), 6, (0, 255, 0), -1)
    
    # Define perspective transform: simulate viewing dari angle
    # Keterangan: Inisialisasi atau perbarui variabel corners_dst.
    corners_dst = np.array([
        # Keterangan: Jalankan perintah berikut.
        [60, 40],    # Top-left (lebih dalam)
        # Keterangan: Jalankan perintah berikut.
        [280, 20],   # Top-right
        # Keterangan: Jalankan perintah berikut.
        [300, 380],  # Bottom-right
        # Keterangan: Jalankan perintah berikut.
        [40, 360]    # Bottom-left
    # Keterangan: Inisialisasi beberapa variabel (], dtype).
    ], dtype=np.float32)
    
    # Apply perspective
    # Keterangan: Inisialisasi atau perbarui variabel warped.
    warped = apply_perspective(image, corners_src.astype(np.float32), corners_dst)
    
    # Inverse perspective (rectification)
    # Goal: bring tilted card back to frontal view
    # Create tilted card first
    # Keterangan: Inisialisasi atau perbarui variabel tilted_corners_src.
    tilted_corners_src = corners_dst.copy()
    # Keterangan: Inisialisasi atau perbarui variabel tilted_corners_dst.
    tilted_corners_dst = corners_src.astype(np.float32)
    
    # Simulate scanned document
    # Keterangan: Inisialisasi atau perbarui variabel tilted_image.
    tilted_image = apply_perspective(image, corners_src.astype(np.float32), tilted_corners_src)
    
    # Rectify it
    # Keterangan: Inisialisasi atau perbarui variabel rectified.
    rectified = apply_perspective(tilted_image, tilted_corners_src, tilted_corners_dst)
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Row 1: Forward perspective
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Keterangan: Mulai loop dengan for pt in corners_src.
    for pt in corners_src:
        # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].plot(pt[0], pt[1], 'go', markersize).
        axes[0, 0].plot(pt[0], pt[1], 'go', markersize=8)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original (Frontal View)\nGreen: source corners")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    # Keterangan: Mulai loop dengan for pt in corners_dst.
    for pt in corners_dst:
        # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].plot(pt[0], pt[1], 'ro', markersize).
        axes[0, 1].plot(pt[0], pt[1], 'ro', markersize=8)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Perspective Warp\nRed: destination corners")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].text(0.1, 0.7, "Perspective Transform:", fontsize).
    axes[0, 2].text(0.1, 0.7, "Perspective Transform:", fontsize=11, fontweight='bold',
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[0, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].text(0.1, 0.55, "• 8 DoF (homography)", fontsize).
    axes[0, 2].text(0.1, 0.55, "• 8 DoF (homography)", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[0, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].text(0.1, 0.45, "• Parallel lines NOT preserved", fontsize).
    axes[0, 2].text(0.1, 0.45, "• Parallel lines NOT preserved", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[0, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].text(0.1, 0.35, "• Simulates 3D viewing", fontsize).
    axes[0, 2].text(0.1, 0.35, "• Simulates 3D viewing", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[0, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].text(0.1, 0.25, "• Needs 4 point pairs", fontsize).
    axes[0, 2].text(0.1, 0.25, "• Needs 4 point pairs", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[0, 2].transAxes)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Row 2: Document rectification
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(tilted_image, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Tilted Document\n(Captured at angle)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(rectified, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Rectified\n(Frontal view restored)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.7, "Document Rectification:", fontsize).
    axes[1, 2].text(0.1, 0.7, "Document Rectification:", fontsize=11, fontweight='bold',
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.55, "1. Detect document corners", fontsize).
    axes[1, 2].text(0.1, 0.55, "1. Detect document corners", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.45, "2. Compute homography", fontsize).
    axes[1, 2].text(0.1, 0.45, "2. Compute homography", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.35, "3. Warp to frontal view", fontsize).
    axes[1, 2].text(0.1, 0.35, "3. Warp to frontal view", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.25, "4. OCR-ready!", fontsize).
    axes[1, 2].text(0.1, 0.25, "4. OCR-ready!", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Perspective Transformation & Document Rectification", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🎯 Real-World Applications:")
    # Keterangan: Jalankan perintah berikut.
    print("   📄 Document scanning (perspective correction)")
    # Keterangan: Jalankan perintah berikut.
    print("   🏢 Architecture photography (keystone correction)")
    # Keterangan: Jalankan perintah berikut.
    print("   🎨 Augmented reality (planar marker tracking)")
    # Keterangan: Jalankan perintah berikut.
    print("   🗺️  Aerial image rectification")


# Keterangan: Definisikan fungsi demo_interpolation_comparison.
def demo_interpolation_comparison():
    """
    Demo 4: Comparison of interpolation methods
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 4: INTERPOLATION METHODS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create image with sharp edges
    # Keterangan: Inisialisasi array bernilai nol.
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (20, 20), (80, 80), (255, 0, 0), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (50, 50), 20, (0, 255, 0), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.line(image, (10, 10), (90, 90), (255, 255, 255), 2)
    
    # Compare interpolation
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = compare_interpolation_methods(image)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(16, 4))
    
    # Keterangan: Mulai loop dengan for i, (name, result) in enumerate(results.items(), 1).
    for i, (name, result) in enumerate(results.items(), 1):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(1, 4, i)
        # Keterangan: Konversi ruang warna gambar.
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        # Keterangan: Set judul subplot.
        plt.title(f"{name}\n(rotated 45°, upscaled)")
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Interpolation Methods Comparison", fontsize).
    plt.suptitle("Interpolation Methods Comparison", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Interpolation Characteristics:")
    # Keterangan: Jalankan perintah berikut.
    print("   NEAREST: Fastest, blocky artifacts")
    # Keterangan: Jalankan perintah berikut.
    print("   LINEAR: Fast, smooth, slight blur")
    # Keterangan: Jalankan perintah berikut.
    print("   CUBIC: Slower, smoother, slight ringing")
    # Keterangan: Jalankan perintah berikut.
    print("   LANCZOS4: Slowest, sharpest, best quality")
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🎯 Usage Guidelines:")
    # Keterangan: Jalankan perintah berikut.
    print("   • Real-time: NEAREST or LINEAR")
    # Keterangan: Jalankan perintah berikut.
    print("   • Image resizing: CUBIC or LANCZOS4")
    # Keterangan: Jalankan perintah berikut.
    print("   • Downsampling: INTER_AREA (not shown)")
    # Keterangan: Jalankan perintah berikut.
    print("   • Scientific: LANCZOS4")


# Keterangan: Definisikan fungsi demo_mesh_warping.
def demo_mesh_warping():
    """
    Demo 5: Mesh-based warping effects
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 5: MESH-BASED WARPING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi array bernilai satu.
    image = np.ones((400, 400, 3), dtype=np.uint8) * 220
    
    # Draw checkerboard
    # Keterangan: Mulai loop dengan for i in range(0, 400, 50).
    for i in range(0, 400, 50):
        # Keterangan: Mulai loop dengan for j in range(0, 400, 50).
        for j in range(0, 400, 50):
            # Keterangan: Cek kondisi (i // 50 + j // 50) % 2 == 0.
            if (i // 50 + j // 50) % 2 == 0:
                # Keterangan: Jalankan perintah berikut.
                cv2.rectangle(image, (i, j), (i + 50, j + 50), (100, 100, 100), -1)
    
    # Draw center object
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (200, 200), 80, (0, 0, 200), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "WARP", (140, 215), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1, (255, 255, 255), 2)
    
    # Apply various warps
    # Keterangan: Inisialisasi atau perbarui variabel radial_barrel.
    radial_barrel = mesh_warp_radial(image, (200, 200), strength=0.8)
    # Keterangan: Inisialisasi atau perbarui variabel radial_pincushion.
    radial_pincushion = mesh_warp_radial(image, (200, 200), strength=-0.5)
    # Keterangan: Inisialisasi atau perbarui variabel wave_h.
    wave_h = mesh_warp_wave(image, amplitude=20, frequency=0.05, direction='horizontal')
    # Keterangan: Inisialisasi atau perbarui variabel swirl.
    swirl = mesh_warp_swirl(image, (200, 200), strength=0.02, radius=150)
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(radial_barrel, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Barrel Distortion\n(+strength)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 2].imshow(cv2.cvtColor(radial_pincushion, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Pincushion Distortion\n(-strength)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(wave_h, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Wave Distortion\n(horizontal)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(swirl, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Swirl Effect\n(rotation varies with r)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.8, "Mesh Warping:", fontsize).
    axes[1, 2].text(0.1, 0.8, "Mesh Warping:", fontsize=11, fontweight='bold',
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.65, "• Define warp field", fontsize).
    axes[1, 2].text(0.1, 0.65, "• Define warp field", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.55, "• Inverse mapping", fontsize).
    axes[1, 2].text(0.1, 0.55, "• Inverse mapping", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.45, "• Interpolation", fontsize).
    axes[1, 2].text(0.1, 0.45, "• Interpolation", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.3, "Applications:", fontsize).
    axes[1, 2].text(0.1, 0.3, "Applications:", fontsize=10, fontweight='bold',
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.2, "• Lens distortion fix", fontsize).
    axes[1, 2].text(0.1, 0.2, "• Lens distortion fix", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.1, "• Creative effects", fontsize).
    axes[1, 2].text(0.1, 0.1, "• Creative effects", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Mesh-Based Warping Effects", fontsize).
    plt.suptitle("Mesh-Based Warping Effects", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_image_morphing.
def demo_image_morphing():
    """
    Demo 6: Simple image morphing
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 6: IMAGE MORPHING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create two faces
    # Keterangan: Inisialisasi array bernilai satu.
    img1 = np.ones((300, 300, 3), dtype=np.uint8) * 220
    # Face 1: Circle
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img1, (150, 150), 80, (200, 180, 150), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img1, (120, 130), 10, (0, 0, 0), -1)  # Left eye
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(img1, (180, 130), 10, (0, 0, 0), -1)  # Right eye
    # Keterangan: Jalankan perintah berikut.
    cv2.ellipse(img1, (150, 170), (30, 15), 0, 0, 180, (0, 0, 0), 2)  # Smile
    
    # Keterangan: Inisialisasi array bernilai satu.
    img2 = np.ones((300, 300, 3), dtype=np.uint8) * 220
    # Face 2: Square
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(img2, (70, 70), (230, 230), (150, 200, 200), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(img2, (110, 120), (130, 140), (0, 0, 0), -1)  # Left eye
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(img2, (170, 120), (190, 140), (0, 0, 0), -1)  # Right eye
    # Keterangan: Jalankan perintah berikut.
    cv2.line(img2, (120, 190), (180, 190), (0, 0, 0), 3)  # Mouth
    
    # Create morph sequence
    # Keterangan: Inisialisasi atau perbarui variabel n_frames.
    n_frames = 5
    # Keterangan: Inisialisasi atau perbarui variabel morph_sequence.
    morph_sequence = []
    
    # Keterangan: Jalankan perintah berikut.
    print(f"   Creating {n_frames} morph frames...")
    
    # Keterangan: Mulai loop dengan for i in range(n_frames).
    for i in range(n_frames):
        # Keterangan: Inisialisasi atau perbarui variabel alpha.
        alpha = i / (n_frames - 1)
        # Keterangan: Inisialisasi atau perbarui variabel morphed.
        morphed = simple_morph(img1, img2, alpha)
        # Keterangan: Jalankan perintah berikut.
        morph_sequence.append(morphed)
        # Keterangan: Inisialisasi atau perbarui variabel print(f" Frame {i + 1}: α.
        print(f"   Frame {i + 1}: α={alpha:.2f}")
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(1, n_frames, figsize=(15, 3))
    
    # Keterangan: Mulai loop dengan for i, frame in enumerate(morph_sequence).
    for i, frame in enumerate(morph_sequence):
        # Keterangan: Konversi ruang warna gambar.
        axes[i].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # Keterangan: Inisialisasi atau perbarui variabel alpha.
        alpha = i / (n_frames - 1)
        # Keterangan: Inisialisasi atau perbarui variabel axes[i].set_title(f"Frame {i + 1}\nα.
        axes[i].set_title(f"Frame {i + 1}\nα={alpha:.2f}")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Simple Image Morphing Sequence", fontsize).
    plt.suptitle("Simple Image Morphing Sequence", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n💡 Simple vs Advanced Morphing:")
    # Keterangan: Jalankan perintah berikut.
    print("   Simple (shown here):")
    # Keterangan: Jalankan perintah berikut.
    print("   - Only color/intensity blending")
    # Keterangan: Jalankan perintah berikut.
    print("   - No shape deformation")
    # Keterangan: Inisialisasi atau perbarui variabel print(" - Formula: M(α).
    print("   - Formula: M(α) = (1-α)I₁ + αI₂")
    # Keterangan: Jalankan perintah berikut.
    print("   Advanced (field morph, mesh warp):")
    # Keterangan: Jalankan perintah berikut.
    print("   - Control point correspondences")
    # Keterangan: Jalankan perintah berikut.
    print("   - Shape interpolation")
    # Keterangan: Jalankan perintah berikut.
    print("   - Cross-dissolve dengan warping")
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🎬 Applications:")
    # Keterangan: Jalankan perintah berikut.
    print("   • Video transitions")
    # Keterangan: Jalankan perintah berikut.
    print("   • Face morphing (aging, gender swap)")
    # Keterangan: Jalankan perintah berikut.
    print("   • Visual effects")


# Keterangan: Definisikan fungsi demo_lens_distortion_correction.
def demo_lens_distortion_correction():
    """
    Demo 7: Lens distortion correction (calibration application)
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 7: LENS DISTORTION CORRECTION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create perfect grid
    # Keterangan: Inisialisasi array bernilai satu.
    image = np.ones((400, 400, 3), dtype=np.uint8) * 240
    
    # Draw grid
    # Keterangan: Mulai loop dengan for i in range(0, 400, 40).
    for i in range(0, 400, 40):
        # Keterangan: Jalankan perintah berikut.
        cv2.line(image, (i, 0), (i, 400), (100, 100, 100), 1)
        # Keterangan: Jalankan perintah berikut.
        cv2.line(image, (0, i), (400, i), (100, 100, 100), 1)
    
    # Highlight center
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (200, 200), 5, (255, 0, 0), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(image, "Grid", (160, 210), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1, (0, 0, 200), 2)
    
    # Simulate lens distortion (barrel)
    # Keterangan: Inisialisasi atau perbarui variabel distorted.
    distorted = mesh_warp_radial(image, (200, 200), strength=1.2)
    
    # Correct (inverse barrel = pincushion)
    # Keterangan: Inisialisasi atau perbarui variabel corrected.
    corrected = mesh_warp_radial(distorted, (200, 200), strength=-1.0)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 5))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 1)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Perfect Grid\n(No distortion)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 2)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(distorted, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Barrel Distortion\n(Wide-angle lens effect)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 3)
    # Keterangan: Konversi ruang warna gambar.
    plt.imshow(cv2.cvtColor(corrected, cv2.COLOR_BGR2RGB))
    # Keterangan: Set judul subplot.
    plt.title("Corrected\n(After calibration)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Lens Distortion Correction", fontsize).
    plt.suptitle("Lens Distortion Correction", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📷 Lens Distortion Types:")
    # Keterangan: Jalankan perintah berikut.
    print("   • Barrel: straight lines bow outward (wide-angle)")
    # Keterangan: Jalankan perintah berikut.
    print("   • Pincushion: straight lines bow inward (telephoto)")
    # Keterangan: Jalankan perintah berikut.
    print("   • Mustache: combination of both")
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🔧 Correction Process:")
    # Keterangan: Jalankan perintah berikut.
    print("   1. Calibration: find distortion coefficients (k1, k2, ...)")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 2. Model: r'.
    print("   2. Model: r' = r(1 + k₁r² + k₂r⁴ + ...)")
    # Keterangan: Jalankan perintah berikut.
    print("   3. Undistort: apply inverse transform")
    # Keterangan: Jalankan perintah berikut.
    print("   4. Applications: measurement, 3D reconstruction, AR")


# Keterangan: Definisikan fungsi demo_transformation_hierarchy.
def demo_transformation_hierarchy():
    """
    Demo 8: Visualization of transformation hierarchy
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 8: TRANSFORMATION HIERARCHY")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create base image
    # Keterangan: Inisialisasi array bernilai satu.
    base = np.ones((200, 300, 3), dtype=np.uint8) * 230
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(base, (50, 50), (250, 150), (100, 150, 200), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(base, "BASE", (110, 115), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1.2, (255, 255, 255), 2)
    
    # 1. Translation (2 DoF)
    # Keterangan: Inisialisasi atau perbarui variabel M_trans.
    M_trans = np.float32([[1, 0, 30], [0, 1, 20]])
    # Keterangan: Terapkan transformasi affine pada gambar.
    trans = cv2.warpAffine(base, M_trans, (300, 200))
    
    # 2. Euclidean/Rigid (3 DoF: tx, ty, θ)
    # Keterangan: Inisialisasi atau perbarui variabel angle.
    angle = 15
    # Keterangan: Inisialisasi atau perbarui variabel M_rigid.
    M_rigid = cv2.getRotationMatrix2D((150, 100), angle, 1.0)
    # Keterangan: Inisialisasi beberapa variabel (M_rigid[0, 2] +).
    M_rigid[0, 2] += 30  # Add translation
    # Keterangan: Inisialisasi beberapa variabel (M_rigid[1, 2] +).
    M_rigid[1, 2] += 20
    # Keterangan: Terapkan transformasi affine pada gambar.
    rigid = cv2.warpAffine(base, M_rigid, (300, 200))
    
    # 3. Similarity (4 DoF: tx, ty, θ, s)
    # Keterangan: Inisialisasi atau perbarui variabel M_sim.
    M_sim = cv2.getRotationMatrix2D((150, 100), angle, 1.2)
    # Keterangan: Inisialisasi beberapa variabel (M_sim[0, 2] +).
    M_sim[0, 2] += 30
    # Keterangan: Inisialisasi beberapa variabel (M_sim[1, 2] +).
    M_sim[1, 2] += 20
    # Keterangan: Terapkan transformasi affine pada gambar.
    similarity = cv2.warpAffine(base, M_sim, (300, 200))
    
    # 4. Affine (6 DoF)
    # Keterangan: Inisialisasi atau perbarui variabel src_pts.
    src_pts = np.float32([[50, 50], [250, 50], [50, 150]])
    # Keterangan: Inisialisasi atau perbarui variabel dst_pts.
    dst_pts = np.float32([[70, 40], [260, 70], [40, 160]])
    # Keterangan: Inisialisasi atau perbarui variabel M_affine.
    M_affine = cv2.getAffineTransform(src_pts, dst_pts)
    # Keterangan: Terapkan transformasi affine pada gambar.
    affine = cv2.warpAffine(base, M_affine, (300, 200))
    
    # 5. Perspective (8 DoF)
    # Keterangan: Inisialisasi atau perbarui variabel src_quad.
    src_quad = np.float32([[50, 50], [250, 50], [250, 150], [50, 150]])
    # Keterangan: Inisialisasi atau perbarui variabel dst_quad.
    dst_quad = np.float32([[70, 40], [270, 60], [260, 160], [40, 140]])
    # Keterangan: Inisialisasi atau perbarui variabel H.
    H = cv2.getPerspectiveTransform(src_quad, dst_quad)
    # Keterangan: Terapkan transformasi perspektif pada gambar.
    perspective = cv2.warpPerspective(base, H, (300, 200))
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(base, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(trans, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Translation\n2 DoF (tx, ty)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 2].imshow(cv2.cvtColor(rigid, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Euclidean (Rigid)\n3 DoF (tx, ty, θ)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(similarity, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Similarity\n4 DoF (tx, ty, θ, s)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(affine, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Affine\n6 DoF (shear allowed)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 2].imshow(cv2.cvtColor(perspective, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Perspective\n8 DoF (3D projection)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("2D Transformation Hierarchy", fontsize).
    plt.suptitle("2D Transformation Hierarchy", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Transformation Hierarchy:")
    # Keterangan: Jalankan perintah berikut.
    print("   Translation ⊂ Euclidean ⊂ Similarity ⊂ Affine ⊂ Perspective")
    # Keterangan: Jalankan perintah berikut.
    print()
    # Keterangan: Jalankan perintah berikut.
    print("   Properties preserved:")
    # Keterangan: Jalankan perintah berikut.
    print("   • Translation: distances, angles, areas")
    # Keterangan: Jalankan perintah berikut.
    print("   • Euclidean: distances, angles")
    # Keterangan: Jalankan perintah berikut.
    print("   • Similarity: angles, ratios")
    # Keterangan: Jalankan perintah berikut.
    print("   • Affine: parallel lines, ratios on lines")
    # Keterangan: Jalankan perintah berikut.
    print("   • Perspective: straight lines (that's it!)")
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🎯 Choosing the Right Transform:")
    # Keterangan: Jalankan perintah berikut.
    print("   • Image registration (same scene): Euclidean/Similarity")
    # Keterangan: Jalankan perintah berikut.
    print("   • Panorama stitching: Perspective")
    # Keterangan: Jalankan perintah berikut.
    print("   • Document scanning: Perspective")
    # Keterangan: Jalankan perintah berikut.
    print("   • Medical imaging alignment: Affine")


# Keterangan: Definisikan fungsi demo_real_world_application.
def demo_real_world_application():
    """
    Demo 9: Real-world application - Document scanner
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 9: DOCUMENT SCANNER SIMULATION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create document
    # Keterangan: Inisialisasi array bernilai satu.
    document = np.ones((400, 300, 3), dtype=np.uint8) * 255
    
    # Add content
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(document, (20, 20), (280, 380), (0, 0, 0), 2)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(document, "SCAN ME", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                # Keterangan: Jalankan perintah berikut.
                1.2, (0, 0, 200), 3)
    # Keterangan: Jalankan perintah berikut.
    cv2.line(document, (30, 100), (270, 100), (0, 0, 0), 1)
    
    # Add text lines
    # Keterangan: Mulai loop dengan for i in range(5).
    for i in range(5):
        # Keterangan: Inisialisasi atau perbarui variabel y.
        y = 140 + i * 35
        # Keterangan: Jalankan perintah berikut.
        cv2.line(document, (30, y), (270, y), (100, 100, 100), 1)
        # Keterangan: Cek kondisi i < 4.
        if i < 4:
            # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
            cv2.putText(document, f"Line {i+1} text...", (40, y - 5), 
                       # Keterangan: Jalankan perintah berikut.
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
    
    # Simulate camera capture: add perspective + noise
    # Define "camera view" corners (tilted)
    # Keterangan: Inisialisasi atau perbarui variabel src_corners.
    src_corners = np.float32([
        # Keterangan: Jalankan perintah berikut.
        [20, 20],
        # Keterangan: Jalankan perintah berikut.
        [280, 20],
        # Keterangan: Jalankan perintah berikut.
        [280, 380],
        # Keterangan: Jalankan perintah berikut.
        [20, 380]
    # Keterangan: Jalankan perintah berikut.
    ])
    
    # Tilted view (as captured by camera)
    # Keterangan: Inisialisasi atau perbarui variabel dst_corners.
    dst_corners = np.float32([
        # Keterangan: Jalankan perintah berikut.
        [60, 50],
        # Keterangan: Jalankan perintah berikut.
        [280, 30],
        # Keterangan: Jalankan perintah berikut.
        [290, 370],
        # Keterangan: Jalankan perintah berikut.
        [40, 350]
    # Keterangan: Jalankan perintah berikut.
    ])
    
    # Apply perspective to simulate camera
    # Keterangan: Inisialisasi atau perbarui variabel H_camera.
    H_camera = cv2.getPerspectiveTransform(src_corners, dst_corners)
    # Keterangan: Terapkan transformasi perspektif pada gambar.
    captured = cv2.warpPerspective(document, H_camera, (300, 400))
    
    # Add realistic camera effects
    # 1. Slight blur
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    captured = cv2.GaussianBlur(captured, (3, 3), 0.5)
    
    # 2. Brightness/contrast variation
    # Keterangan: Inisialisasi atau perbarui variabel captured.
    captured = cv2.convertScaleAbs(captured, alpha=0.9, beta=10)
    
    # 3. Slight noise
    # Keterangan: Inisialisasi atau perbarui variabel noise.
    noise = np.random.normal(0, 5, captured.shape)
    # Keterangan: Inisialisasi atau perbarui variabel captured.
    captured = np.clip(captured.astype(float) + noise, 0, 255).astype(np.uint8)
    
    # RECTIFICATION PIPELINE
    # Keterangan: Jalankan perintah berikut.
    print("\n📱 Document Scanner Pipeline:")
    # Keterangan: Jalankan perintah berikut.
    print("   1. Edge detection untuk find document")
    
    # Edge detection
    # Keterangan: Konversi ruang warna gambar.
    gray = cv2.cvtColor(captured, cv2.COLOR_BGR2GRAY)
    # Keterangan: Inisialisasi atau perbarui variabel edges.
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    # Keterangan: Inisialisasi beberapa variabel (contours, _).
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # For demo, manually use known corners (in real app: detect automatically)
    # Keterangan: Inisialisasi atau perbarui variabel detected_corners.
    detected_corners = dst_corners.copy()
    
    # Keterangan: Jalankan perintah berikut.
    print("   2. Detect document corners")
    # Keterangan: Jalankan perintah berikut.
    print(f"      Found corners: {detected_corners.tolist()}")
    
    # Rectify: warp back to frontal
    # Target: standard A4 aspect ratio
    # Keterangan: Inisialisasi beberapa variabel (target_w, target_h).
    target_w, target_h = 300, 400
    # Keterangan: Inisialisasi atau perbarui variabel target_corners.
    target_corners = np.float32([
        # Keterangan: Jalankan perintah berikut.
        [0, 0],
        # Keterangan: Jalankan perintah berikut.
        [target_w - 1, 0],
        # Keterangan: Jalankan perintah berikut.
        [target_w - 1, target_h - 1],
        # Keterangan: Jalankan perintah berikut.
        [0, target_h - 1]
    # Keterangan: Jalankan perintah berikut.
    ])
    
    # Keterangan: Jalankan perintah berikut.
    print("   3. Compute homography")
    # Keterangan: Inisialisasi atau perbarui variabel H_rectify.
    H_rectify = cv2.getPerspectiveTransform(detected_corners, target_corners)
    
    # Keterangan: Jalankan perintah berikut.
    print("   4. Warp to frontal view")
    # Keterangan: Terapkan transformasi perspektif pada gambar.
    scanned = cv2.warpPerspective(captured, H_rectify, (target_w, target_h))
    
    # Keterangan: Jalankan perintah berikut.
    print("   5. Enhance (optional)")
    # Enhance contrast
    # Keterangan: Inisialisasi atau perbarui variabel scanned_enhanced.
    scanned_enhanced = cv2.convertScaleAbs(scanned, alpha=1.2, beta=-20)
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(document, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original Document\n(Perfect frontal)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(captured, cv2.COLOR_BGR2RGB))
    # Keterangan: Mulai loop dengan for pt in detected_corners.
    for pt in detected_corners:
        # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].plot(pt[0], pt[1], 'ro', markersize).
        axes[0, 1].plot(pt[0], pt[1], 'ro', markersize=8)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title("Camera Capture\n(Tilted + noise)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(edges, cmap).
    axes[0, 2].imshow(edges, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Edge Detection\n(Find document)")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(scanned, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Rectified\n(Perspective corrected)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(scanned_enhanced, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Enhanced\n(Ready for OCR)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Comparison
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.85, "Scanner Pipeline:", fontsize).
    axes[1, 2].text(0.1, 0.85, "Scanner Pipeline:", fontsize=11, fontweight='bold',
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.72, "1. Capture tilted image", fontsize).
    axes[1, 2].text(0.1, 0.72, "1. Capture tilted image", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.62, "2. Detect corners (edge)", fontsize).
    axes[1, 2].text(0.1, 0.62, "2. Detect corners (edge)", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.52, "3. Compute homography", fontsize).
    axes[1, 2].text(0.1, 0.52, "3. Compute homography", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.42, "4. Warp to frontal", fontsize).
    axes[1, 2].text(0.1, 0.42, "4. Warp to frontal", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.32, "5. Enhance quality", fontsize).
    axes[1, 2].text(0.1, 0.32, "5. Enhance quality", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.15, "Apps: CamScanner,", fontsize).
    axes[1, 2].text(0.1, 0.15, "Apps: CamScanner,", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].text(0.1, 0.05, "Adobe Scan, etc.", fontsize).
    axes[1, 2].text(0.1, 0.05, "Adobe Scan, etc.", fontsize=9,
                    # Keterangan: Inisialisasi atau perbarui variabel transform.
                    transform=axes[1, 2].transAxes)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Real-World: Document Scanner", fontsize).
    plt.suptitle("Real-World: Document Scanner", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🏆 Document Scanner adalah Perfect Example:")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Perspective transform (homography)")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Corner detection")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Image enhancement")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Millions use it daily!")


# ============================================================
# MAIN PROGRAM
# ============================================================

# Keterangan: Definisikan fungsi main.
def main():
    """Program utama"""
    print("\n" + "="*60)
    print("      PRAKTIKUM COMPUTER VISION - BAB 3")
    print("      GEOMETRIC TRANSFORMATIONS")
    print("="*60)
    
    print("\n📚 Konsep yang akan dipelajari:")
    print("   1. Basic 2D transforms: translation, rotation")
    print("   2. Transformation hierarchy (Translation → Perspective)")
    print("   3. Affine vs Perspective")
    print("   4. Interpolation methods")
    print("   5. Mesh-based warping")
    print("   6. Real applications: document scanning, lens correction")
    
    print("\n🔑 Key Formulas:")
    print("   Affine:       x' = Ax + t    (6 DoF, 3 points)")
    print("   Perspective:  x' ~ Hx        (8 DoF, 4 points)")
    print("   Radial:       r' = r(1+kr²)  (lens distortion)")
    
    try:
        # Demo 1: Basic transformations
        demo_basic_transformations()
        
        # Demo 2: Affine
        demo_affine_transformation()
        
        # Demo 3: Perspective
        demo_perspective_transformation()
        
        # Demo 4: Interpolation
        demo_interpolation_comparison()
        
        # Demo 5: Mesh warping
        demo_mesh_warping()
        
        # Demo 6: Image morphing
        demo_image_morphing()
        
        # Demo 7: Lens distortion
        demo_lens_distortion_correction()
        
        # Demo 8: Hierarchy
        demo_transformation_hierarchy()
        
        # Demo 9: Real-world
        demo_real_world_application()
        
        print("\n" + "="*60)
        print("✅ SEMUA DEMO SELESAI")
        print("="*60)
        
        print("\n💡 Key Takeaways:")
        print("   1. Transform hierarchy: Translation ⊂ ... ⊂ Perspective")
        print("   2. More DoF = more flexible, but need more points")
        print("   3. Interpolation crucial for quality")
        print("   4. Inverse warping prevents holes")
        print("   5. Used in: registration, stitching, AR, scanning")
        
        print("\n🔬 Eksperimen Lanjutan:")
        print("   - Ubah ROTATION_ANGLE untuk see edge artifacts")
        print("   - Compare INTERP_METHOD untuk quality/speed")
        print("   - Implement panorama stitching dengan homography")
        print("   - Try camera calibration dengan checkerboard")
        
        print("\n📱 Real-World Impact:")
        print("   • Document scanners (CamScanner, Adobe Scan)")
        print("   • Photo editing (Photoshop warp tools)")
        print("   • AR filters (Snapchat, Instagram)")
        print("   • Medical imaging (MRI registration)")
        print("   • Satellite imagery (orthorectification)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
