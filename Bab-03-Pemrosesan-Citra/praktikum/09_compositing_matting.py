# ============================================================
# PROGRAM: 09_compositing_matting.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Compositing dan Alpha Matting
# 
# Tujuan Pembelajaran:
#   1. Memahami alpha channel dan transparency
#   2. Mengimplementasikan image compositing (over operator)
#   3. Melakukan blue/green screen matting
#   4. Aplikasi: mengganti background
# 
# Teori:
#   Compositing equation: C = (1-α)B + αF
#   - C: composite result
#   - B: background image
#   - F: foreground image  
#   - α: alpha matte (0=transparent, 1=opaque)
# ============================================================

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor modul os.
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# File gambar
# Keterangan: Inisialisasi atau perbarui variabel FOREGROUND_IMAGE.
FOREGROUND_IMAGE = "person.jpg"       # Gambar orang dengan green screen
# Keterangan: Inisialisasi atau perbarui variabel BACKGROUND_IMAGE.
BACKGROUND_IMAGE = "nature.jpg"       # Background baru

# Green screen parameters
# Keterangan: Inisialisasi atau perbarui variabel GREEN_LOWER.
GREEN_LOWER = np.array([40, 40, 40])     # HSV lower bound
# Keterangan: Inisialisasi atau perbarui variabel GREEN_UPPER.
GREEN_UPPER = np.array([80, 255, 255])   # HSV upper bound

# Matting refinement
# Keterangan: Inisialisasi atau perbarui variabel FEATHER_AMOUNT.
FEATHER_AMOUNT = 5         # Smoothing edge alpha matte
# Keterangan: Inisialisasi atau perbarui variabel ERODE_ITERATIONS.
ERODE_ITERATIONS = 1       # Erode untuk cleanup
# Keterangan: Inisialisasi atau perbarui variabel DILATE_ITERATIONS.
DILATE_ITERATIONS = 1      # Dilate untuk recover edge

# Foreground adjustment
# Keterangan: Inisialisasi atau perbarui variabel FG_BRIGHTNESS.
FG_BRIGHTNESS = 0          # Brightness adjustment untuk match BG
# Keterangan: Inisialisasi atau perbarui variabel FG_CONTRAST.
FG_CONTRAST = 1.0          # Contrast adjustment

# ============================================================
# FUNGSI HELPER
# ============================================================

# Keterangan: Definisikan fungsi create_sample_images.
def create_sample_images():
    """Membuat sample images jika file tidak ditemukan"""
    # Foreground: lingkaran merah di green background
    fg = np.zeros((400, 400, 3), dtype=np.uint8)
    fg[:, :] = (0, 200, 0)  # Green screen (BGR)
    cv2.circle(fg, (200, 200), 100, (0, 0, 255), -1)  # Red circle
    cv2.putText(fg, "FG", (170, 220), cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, (255, 255, 255), 3)
    
    # Background: gradient blue
    bg = np.zeros((400, 400, 3), dtype=np.uint8)
    for i in range(400):
        for j in range(400):
            bg[i, j] = (200 - i//2, 100, i//2)
    cv2.putText(bg, "BACKGROUND", (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2)
    
    return fg, bg


# ============================================================
# FUNGSI COMPOSITING DAN MATTING
# ============================================================

def create_alpha_matte_from_green_screen(image, lower_bound, upper_bound):
    """
    # Keterangan: Jalankan perintah berikut.
    Membuat alpha matte dari green screen
    
    # Keterangan: Mulai blok kode baru.
    Langkah:
    # Keterangan: Jalankan perintah berikut.
    1. Convert RGB ke HSV
    # Keterangan: Jalankan perintah berikut.
    2. Threshold untuk green color range
    # Keterangan: Inisialisasi atau perbarui variabel 3. Invert mask (green.
    3. Invert mask (green=0/transparent, non-green=1/opaque)
    # Keterangan: Jalankan perintah berikut.
    4. Refinement dengan morphology
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - image: input BGR image
    # Keterangan: Jalankan perintah berikut.
    - lower_bound: HSV lower bound untuk green
    # Keterangan: Jalankan perintah berikut.
    - upper_bound: HSV upper bound untuk green
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - alpha_matte: grayscale mask (0-255)
    """
    print("🎭 Membuat alpha matte dari green screen...")
    
    # Convert BGR ke HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Threshold untuk deteksi green
    mask_green = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Invert: green jadi 0 (transparent), non-green jadi 255 (opaque)
    alpha_matte = cv2.bitwise_not(mask_green)
    
    print(f"   ✓ Green pixels detected: {np.sum(mask_green > 0)}")
    print(f"   ✓ Foreground pixels: {np.sum(alpha_matte > 0)}")
    
    return alpha_matte


def refine_alpha_matte(alpha_matte, erode_iter=1, dilate_iter=1, feather=5):
    """
    # Keterangan: Jalankan perintah berikut.
    Memperbaiki kualitas alpha matte
    
    # Keterangan: Mulai blok kode baru.
    Langkah:
    # Keterangan: Jalankan perintah berikut.
    1. Erosion untuk remove noise kecil
    # Keterangan: Jalankan perintah berikut.
    2. Dilation untuk recover edges
    # Keterangan: Jalankan perintah berikut.
    3. Gaussian blur untuk soft edges (feathering)
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - alpha_matte: binary mask (0-255)
    # Keterangan: Jalankan perintah berikut.
    - erode_iter: jumlah iterasi erosion
    # Keterangan: Jalankan perintah berikut.
    - dilate_iter: jumlah iterasi dilation
    # Keterangan: Jalankan perintah berikut.
    - feather: kernel size untuk blur (smoothing edge)
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - refined alpha matte (0-255)
    """
    print("🔧 Refining alpha matte...")
    
    # Morphological operations untuk cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    # Erosion untuk hapus noise
    if erode_iter > 0:
        alpha_refined = cv2.erode(alpha_matte, kernel, iterations=erode_iter)
        print(f"   ✓ Eroded {erode_iter}x")
    else:
        alpha_refined = alpha_matte.copy()
    
    # Dilation untuk recover edges
    if dilate_iter > 0:
        alpha_refined = cv2.dilate(alpha_refined, kernel, iterations=dilate_iter)
        print(f"   ✓ Dilated {dilate_iter}x")
    
    # Gaussian blur untuk soft edges (anti-aliasing)
    if feather > 0:
        if feather % 2 == 0:
            feather += 1  # Harus ganjil
        alpha_refined = cv2.GaussianBlur(alpha_refined, (feather, feather), 0)
        print(f"   ✓ Feathered with kernel size {feather}")
    
    return alpha_refined


def composite_over(foreground, background, alpha_matte):
    """
    # Keterangan: Jalankan perintah berikut.
    Composite foreground over background menggunakan alpha matte
    
    # Keterangan: Inisialisasi atau perbarui variabel Formula: C.
    Formula: C = (1-α)B + αF
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - foreground: foreground image (BGR)
    # Keterangan: Jalankan perintah berikut.
    - background: background image (BGR)
    # Keterangan: Jalankan perintah berikut.
    - alpha_matte: alpha channel (0-255, single channel)
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - composite: hasil composite (BGR)
    """
    print("🎨 Compositing foreground over background...")
    
    # Ensure dimensions match
    h, w = alpha_matte.shape
    if background.shape[:2] != (h, w):
        background = cv2.resize(background, (w, h))
        print(f"   ℹ Background resized to {w}×{h}")
    
    # Normalize alpha ke range [0, 1]
    alpha = alpha_matte.astype(float) / 255.0
    
    # Convert ke 3 channels untuk broadcasting
    alpha_3ch = np.stack([alpha, alpha, alpha], axis=2)
    
    # Convert images to float
    fg_float = foreground.astype(float)
    bg_float = background.astype(float)
    
    # Compositing equation: C = (1-α)B + αF
    composite = (1.0 - alpha_3ch) * bg_float + alpha_3ch * fg_float
    
    # Convert back to uint8
    composite = np.clip(composite, 0, 255).astype(np.uint8)
    
    # Calculate statistics
    foreground_ratio = (np.sum(alpha_matte > 0) / (h * w)) * 100
    print(f"   ✓ Foreground coverage: {foreground_ratio:.1f}%")
    
    return composite


def extract_foreground_with_alpha(image, alpha_matte):
    """
    # Keterangan: Jalankan perintah berikut.
    Ekstrak foreground dengan alpha channel (untuk saving sebagai PNG)
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - image: input BGR image
    # Keterangan: Jalankan perintah berikut.
    - alpha_matte: alpha channel (0-255)
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - foreground_rgba: BGRA image
    """
    # Merge BGR dengan alpha channel
    bgra = cv2.merge([image[:,:,0], image[:,:,1], image[:,:,2], alpha_matte])
    return bgra


# ============================================================
# FUNGSI ADVANCED MATTING
# ============================================================

def create_distance_transform_alpha(binary_mask, max_distance=10):
    """
    # Keterangan: Jalankan perintah berikut.
    Membuat alpha matte dengan soft edge menggunakan distance transform
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - binary_mask: binary mask (0 atau 255)
    # Keterangan: Jalankan perintah berikut.
    - max_distance: jarak maksimal untuk soft edge
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - alpha matte dengan soft edges
    """
    print("📏 Creating soft alpha matte dengan distance transform...")
    
    # Distance transform dari edge
    # Threshold dulu untuk pastikan binary
    _, binary = cv2.threshold(binary_mask, 127, 255, cv2.THRESH_BINARY)
    
    # Erode untuk create margin
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    eroded = cv2.erode(binary, kernel, iterations=2)
    
    # Distance transform dari eroded mask
    dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    
    # Normalize distance dalam range [0, max_distance]
    alpha_soft = np.clip(dist_transform / max_distance, 0, 1) * 255
    alpha_soft = alpha_soft.astype(np.uint8)
    
    return alpha_soft


def color_based_matting(image, bg_color, tolerance=30):
    """
    # Keterangan: Jalankan perintah berikut.
    Simple color-based matting untuk solid color background
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - image: input BGR image
    # Keterangan: Jalankan perintah berikut.
    - bg_color: background color dalam BGR tuple
    # Keterangan: Jalankan perintah berikut.
    - tolerance: color tolerance
    
    # Keterangan: Mulai blok kode baru.
    Return:
    # Keterangan: Jalankan perintah berikut.
    - alpha_matte
    """
    print(f"🎨 Color-based matting untuk background {bg_color}...")
    
    # Calculate color distance
    color_diff = np.abs(image.astype(float) - np.array(bg_color))
    color_distance = np.sqrt(np.sum(color_diff**2, axis=2))
    
    # Threshold based on tolerance
    alpha_matte = np.where(color_distance > tolerance, 255, 0).astype(np.uint8)
    
    print(f"   ✓ Detected {np.sum(alpha_matte > 0)} foreground pixels")
    
    return alpha_matte


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_simple_compositing():
    """
    # Keterangan: Jalankan perintah berikut.
    Demo 1: Simple compositing dengan alpha shapes
    """
    print("\n" + "="*60)
    print("DEMO 1: SIMPLE COMPOSITING")
    print("="*60)
    
    # Create background
    bg = np.zeros((400, 600, 3), dtype=np.uint8)
    for i in range(400):
        bg[i, :] = (200 - i//2, 100, 50)  # Gradient
    
    # Create foreground shape
    fg = np.full((400, 600, 3), (0, 200, 200), dtype=np.uint8)
    
    # Create alpha matte - circle
    alpha = np.zeros((400, 600), dtype=np.uint8)
    cv2.circle(alpha, (300, 200), 150, 255, -1)
    
    # Create soft edge using Gaussian blur
    alpha_soft = cv2.GaussianBlur(alpha, (21, 21), 10)
    
    # Composite
    composite_hard = composite_over(fg, bg, alpha)
    composite_soft = composite_over(fg, bg, alpha_soft)
    
    # Display
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(bg, cv2.COLOR_BGR2RGB))
    plt.title("Background")
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(cv2.cvtColor(fg, cv2.COLOR_BGR2RGB))
    plt.title("Foreground")
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(alpha, cmap='gray')
    plt.title("Alpha Matte (Hard Edge)")
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.imshow(cv2.cvtColor(composite_hard, cv2.COLOR_BGR2RGB))
    plt.title("Composite (Hard Edge)")
    plt.axis('off')
    
    plt.subplot(2, 3, 5)
    plt.imshow(alpha_soft, cmap='gray')
    plt.title("Alpha Matte (Soft Edge)")
    plt.axis('off')
    
    plt.subplot(2, 3, 6)
    plt.imshow(cv2.cvtColor(composite_soft, cv2.COLOR_BGR2RGB))
    plt.title("Composite (Soft Edge - No Jaggies!)")
    plt.axis('off')
    
    plt.suptitle("Image Compositing: Hard vs Soft Alpha", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Analisis:")
    print("   - Hard edge menghasilkan 'jaggies' (aliasing)")
    print("   - Soft edge menghasilkan blend yang smooth")
    print("   - Gaussian blur pada alpha menciptakan anti-aliasing")


def demo_green_screen_matting():
    """
    # Keterangan: Jalankan perintah berikut.
    Demo 2: Green screen matting
    """
    print("\n" + "="*60)
    print("DEMO 2: GREEN SCREEN MATTING")
    print("="*60)
    
    # Create sample green screen image
    print("📸 Membuat sample green screen image...")
    
    # Green background
    fg_image = np.zeros((480, 640, 3), dtype=np.uint8)
    fg_image[:, :] = (0, 200, 0)  # Green background
    
    # Add foreground object (person silhouette simulation)
    # Head
    cv2.ellipse(fg_image, (320, 150), (80, 100), 0, 0, 360, (120, 80, 50), -1)
    # Body
    pts = np.array([[320, 250], [250, 450], [390, 450]], np.int32)
    cv2.fillPoly(fg_image, [pts], (80, 100, 180))
    # Arms
    cv2.ellipse(fg_image, (280, 300), (40, 80), -30, 0, 360, (150, 120, 100), -1)
    cv2.ellipse(fg_image, (360, 300), (40, 80), 30, 0, 360, (150, 120, 100), -1)
    
    # Create beautiful background
    bg_image = np.zeros((480, 640, 3), dtype=np.uint8)
    for i in range(480):
        for j in range(640):
            bg_image[i, j] = (
                int(200 - i * 0.2),      # B
                int(150 + j * 0.05),     # G
                int(100 + i * 0.1)       # R
            )
    cv2.putText(bg_image, "NEW BACKGROUND", (150, 400), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    
    # Step 1: Create alpha matte dari green screen
    alpha_raw = create_alpha_matte_from_green_screen(
        fg_image, GREEN_LOWER, GREEN_UPPER
    )
    
    # Step 2: Refine alpha matte
    alpha_refined = refine_alpha_matte(
        alpha_raw, ERODE_ITERATIONS, DILATE_ITERATIONS, FEATHER_AMOUNT
    )
    
    # Step 3: Composite
    composite = composite_over(fg_image, bg_image, alpha_refined)
    
    # Display hasil
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(fg_image, cv2.COLOR_BGR2RGB))
    plt.title("Foreground (Green Screen)")
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB))
    plt.title("New Background")
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(alpha_raw, cmap='gray')
    plt.title(f"Alpha Matte (Raw)\nForeground: {np.sum(alpha_raw>0)} px")
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.imshow(alpha_refined, cmap='gray')
    plt.title(f"Alpha Matte (Refined)\nFeather={FEATHER_AMOUNT}")
    plt.axis('off')
    
    plt.subplot(2, 3, 5)
    plt.imshow(cv2.cvtColor(composite, cv2.COLOR_BGR2RGB))
    plt.title("Final Composite")
    plt.axis('off')
    
    # Show alpha comparison
    plt.subplot(2, 3, 6)
    edge_raw = cv2.Canny(alpha_raw, 50, 150)
    edge_refined = cv2.Canny(alpha_refined, 50, 150)
    comparison = np.hstack([edge_raw, edge_refined])
    plt.imshow(comparison, cmap='gray')
    plt.title("Edge Comparison: Raw (left) vs Refined (right)")
    plt.axis('off')
    
    plt.suptitle("Green Screen Matting Pipeline", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Hasil:")
    print(f"   - Original alpha: {np.sum(alpha_raw > 0)} foreground pixels")
    print(f"   - Refined alpha: {np.sum(alpha_refined > 0)} foreground pixels")
    print(f"   - Alpha range: {alpha_refined.min()} - {alpha_refined.max()}")


def demo_alpha_blending_comparison():
    """
    # Keterangan: Jalankan perintah berikut.
    Demo 3: Membandingkan berbagai metode blending
    """
    print("\n" + "="*60)
    print("DEMO 3: ALPHA BLENDING COMPARISON")
    print("="*60)
    
    # Create images
    fg = np.full((300, 300, 3), (0, 0, 200), dtype=np.uint8)  # Red
    bg = np.full((300, 300, 3), (200, 0, 0), dtype=np.uint8)  # Blue
    
    # Different alpha shapes
    # 1. Linear gradient (left to right)
    alpha_gradient = np.zeros((300, 300), dtype=np.uint8)
    for j in range(300):
        alpha_gradient[:, j] = int((j / 299) * 255)
    
    # 2. Radial gradient (center to edge)
    alpha_radial = np.zeros((300, 300), dtype=np.uint8)
    center = (150, 150)
    for i in range(300):
        for j in range(300):
            dist = np.sqrt((i - center[0])**2 + (j - center[1])**2)
            alpha_val = max(0, 1 - dist / 150) * 255
            alpha_radial[i, j] = int(alpha_val)
    
    # 3. Checkerboard pattern
    alpha_checker = np.zeros((300, 300), dtype=np.uint8)
    block_size = 30
    for i in range(0, 300, block_size):
        for j in range(0, 300, block_size):
            if ((i // block_size) + (j // block_size)) % 2 == 0:
                alpha_checker[i:i+block_size, j:j+block_size] = 255
    
    # Composite
    comp_gradient = composite_over(fg, bg, alpha_gradient)
    comp_radial = composite_over(fg, bg, alpha_radial)
    comp_checker = composite_over(fg, bg, alpha_checker)
    
    # Display
    plt.figure(figsize=(15, 10))
    
    # Row 1: Alpha mattes
    plt.subplot(2, 3, 1)
    plt.imshow(alpha_gradient, cmap='gray')
    plt.title("Linear Gradient Alpha")
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(alpha_radial, cmap='gray')
    plt.title("Radial Gradient Alpha")
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(alpha_checker, cmap='gray')
    plt.title("Checkerboard Alpha")
    plt.axis('off')
    
    # Row 2: Composites
    plt.subplot(2, 3, 4)
    plt.imshow(cv2.cvtColor(comp_gradient, cv2.COLOR_BGR2RGB))
    plt.title("Linear Blend: Red → Blue")
    plt.axis('off')
    
    plt.subplot(2, 3, 5)
    plt.imshow(cv2.cvtColor(comp_radial, cv2.COLOR_BGR2RGB))
    plt.title("Radial Blend: Red (center)")
    plt.axis('off')
    
    plt.subplot(2, 3, 6)
    plt.imshow(cv2.cvtColor(comp_checker, cv2.COLOR_BGR2RGB))
    plt.title("Checkerboard Blend")
    plt.axis('off')
    
    plt.suptitle("Different Alpha Blending Patterns", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def demo_pre_multiplied_alpha():
    """
    # Keterangan: Jalankan perintah berikut.
    Demo 4: Pre-multiplied alpha (αF representation)
    """
    print("\n" + "="*60)
    print("DEMO 4: PRE-MULTIPLIED ALPHA")
    print("="*60)
    
    # Create foreground and alpha
    fg = np.full((200, 200, 3), (0, 255, 0), dtype=np.uint8)  # Green
    bg = np.full((200, 200, 3), (100, 100, 100), dtype=np.uint8)  # Gray
    
    # Create circular alpha with gradient
    alpha = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(alpha, (100, 100), 80, 255, -1)
    alpha = cv2.GaussianBlur(alpha, (41, 41), 20)
    
    # Method 1: Standard compositing
    comp_standard = composite_over(fg, bg, alpha)
    
    # Method 2: Pre-multiplied
    alpha_norm = alpha.astype(float) / 255.0
    alpha_3ch = np.stack([alpha_norm] * 3, axis=2)
    
    # Pre-multiply foreground dengan alpha
    fg_premult = (fg.astype(float) * alpha_3ch).astype(np.uint8)
    
    # Composite: C = B(1-α) + premultiplied_F
    # (ini sama dengan formula standard, tapi lebih efisien untuk multiple composites)
    comp_premult = (bg.astype(float) * (1 - alpha_3ch) + fg_premult.astype(float)).astype(np.uint8)
    
    # Display
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(fg, cv2.COLOR_BGR2RGB))
    plt.title("Foreground (F)")
    plt.axis('off')
    
    plt.subplot(1, 4, 2)
    plt.imshow(alpha, cmap='gray')
    plt.title("Alpha (α)")
    plt.axis('off')
    
    plt.subplot(1, 4, 3)
    plt.imshow(cv2.cvtColor(fg_premult, cv2.COLOR_BGR2RGB))
    plt.title("Pre-multiplied (αF)")
    plt.axis('off')
    
    plt.subplot(1, 4, 4)
    plt.imshow(cv2.cvtColor(comp_premult, cv2.COLOR_BGR2RGB))
    plt.title("Composite Result")
    plt.axis('off')
    
    plt.suptitle("Pre-multiplied Alpha Representation", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Info:")
    print("   Pre-multiplied alpha berguna untuk:")
    print("   - Multiple compositing layers (lebih efisien)")
    print("   - Blur/resample alpha-matted images")
    print("   - Graphics API (OpenGL, Direct3D)")


def demo_real_world_application():
    """
    # Keterangan: Jalankan perintah berikut.
    Demo 5: Aplikasi nyata - Portrait dengan background blur
    """
    print("\n" + "="*60)
    print("DEMO 5: PORTRAIT BACKGROUND BLUR (BOKEH EFFECT)")
    print("="*60)
    
    # Create sample portrait
    image = np.full((480, 640, 3), (100, 120, 80), dtype=np.uint8)
    
    # Add noise/texture
    noise = np.random.randint(-20, 20, (480, 640, 3), dtype=np.int16)
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add person silhouette  
    cv2.ellipse(image, (320, 200), (100, 130), 0, 0, 360, (200, 150, 130), -1)
    cv2.ellipse(image, (320, 340), (80, 140), 0, 0, 360, (180, 140, 120), -1)
    
    # Create simple segmentation mask (in practice, use ML model)
    alpha = np.zeros((480, 640), dtype=np.uint8)
    cv2.ellipse(alpha, (320, 200), (100, 130), 0, 0, 360, 255, -1)
    cv2.ellipse(alpha, (320, 340), (80, 140), 0, 0, 360, 255, -1)
    alpha_soft = cv2.GaussianBlur(alpha, (21, 21), 10)
    
    # Blur background
    bg_blurred = cv2.GaussianBlur(image, (51, 51), 30)
    
    # Composite: sharp foreground + blurred background
    # Foreground contribution
    alpha_norm = alpha_soft.astype(float) / 255.0
    alpha_3ch = np.stack([alpha_norm] * 3, axis=2)
    
    result = (alpha_3ch * image.astype(float) + 
              (1 - alpha_3ch) * bg_blurred.astype(float)).astype(np.uint8)
    
    # Display
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis('off')
    
    plt.subplot(1, 4, 2)
    plt.imshow(alpha_soft, cmap='gray')
    plt.title("Subject Mask (Alpha)")
    plt.axis('off')
    
    plt.subplot(1, 4, 3)
    plt.imshow(cv2.cvtColor(bg_blurred, cv2.COLOR_BGR2RGB))
    plt.title("Blurred Background")
    plt.axis('off')
    
    plt.subplot(1, 4, 4)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Result: Portrait Mode Effect")
    plt.axis('off')
    
    plt.suptitle("Real-World Application: Bokeh/Portrait Mode", 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n🏆 Aplikasi Nyata:")
    print("   📱 Smartphone portrait mode")
    print("   📸 DSLR bokeh simulation")
    print("   🎬 Video conferencing background blur")
    print("   🖼️  Product photography focus effect")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Program utama"""
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("      PRAKTIKUM COMPUTER VISION - BAB 3")
    # Keterangan: Jalankan perintah berikut.
    print("     COMPOSITING DAN ALPHA MATTING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📚 Konsep yang akan dipelajari:")
    # Keterangan: Jalankan perintah berikut.
    print("   1. Alpha channel dan transparency")
    # Keterangan: Jalankan perintah berikut.
    print("   2. Over operator untuk compositing")
    # Keterangan: Jalankan perintah berikut.
    print("   3. Green screen matting")
    # Keterangan: Jalankan perintah berikut.
    print("   4. Pre-multiplied alpha")
    # Keterangan: Jalankan perintah berikut.
    print("   5. Aplikasi: background replacement, bokeh effect")
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🎯 Teori Dasar:")
    # Keterangan: Inisialisasi atau perbarui variabel print(" Compositing Formula: C.
    print("   Compositing Formula: C = (1-α)B + αF")
    # Keterangan: Jalankan perintah berikut.
    print("   - C: Composite result")
    # Keterangan: Jalankan perintah berikut.
    print("   - B: Background")
    # Keterangan: Jalankan perintah berikut.
    print("   - F: Foreground")
    # Keterangan: Inisialisasi atau perbarui variabel print(" - α: Alpha matte (0.
    print("   - α: Alpha matte (0=transparent, 1=opaque)")
    
    # Keterangan: Mulai blok try untuk menangani error.
    try:
        # Demo 1: Simple compositing
        # Keterangan: Jalankan perintah berikut.
        demo_simple_compositing()
        
        # Demo 2: Green screen matting
        # Keterangan: Jalankan perintah berikut.
        demo_green_screen_matting()
        
        # Demo 3: Alpha blending patterns
        # Keterangan: Jalankan perintah berikut.
        demo_alpha_blending_comparison()
        
        # Demo 4: Pre-multiplied alpha
        # Keterangan: Jalankan perintah berikut.
        demo_pre_multiplied_alpha()
        
        # Demo 5: Real-world application
        # Keterangan: Jalankan perintah berikut.
        demo_real_world_application()
        
        # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
        print("\n" + "="*60)
        # Keterangan: Jalankan perintah berikut.
        print("✅ SEMUA DEMO SELESAI")
        # Keterangan: Inisialisasi atau perbarui variabel print(".
        print("="*60)
        
        # Keterangan: Jalankan perintah berikut.
        print("\n💡 Kesimpulan:")
        # Keterangan: Jalankan perintah berikut.
        print("   1. Alpha channel mengontrol transparency (0-255)")
        # Keterangan: Jalankan perintah berikut.
        print("   2. Soft edges (feathered) penting untuk menghindari jaggies")
        # Keterangan: Jalankan perintah berikut.
        print("   3. Green/blue screen matting: threshold HSV color range")
        # Keterangan: Jalankan perintah berikut.
        print("   4. Morphology + blur untuk refine alpha matte")
        # Keterangan: Jalankan perintah berikut.
        print("   5. Aplikasi: video effects, portrait mode, AR/VR")
        
        # Keterangan: Jalankan perintah berikut.
        print("\n🔬 Eksperimen Lanjutan:")
        # Keterangan: Jalankan perintah berikut.
        print("   - Ubah GREEN_LOWER dan GREEN_UPPER untuk toleransi berbeda")
        # Keterangan: Jalankan perintah berikut.
        print("   - Coba FEATHER_AMOUNT berbeda (5, 10, 20)")
        # Keterangan: Jalankan perintah berikut.
        print("   - Eksperimen dengan blue screen (ubah HSV range)")
        # Keterangan: Jalankan perintah berikut.
        print("   - Tambahkan color correction untuk matching lighting")
        
    # Keterangan: Tangani error pada blok except.
    except Exception as e:
        # Keterangan: Jalankan perintah berikut.
        print(f"\n❌ Error: {e}")
        # Keterangan: Impor modul traceback.
        import traceback
        # Keterangan: Jalankan perintah berikut.
        traceback.print_exc()


# Keterangan: Cek kondisi __name__ == "__main__".
if __name__ == "__main__":
    # Keterangan: Jalankan perintah berikut.
    main()
