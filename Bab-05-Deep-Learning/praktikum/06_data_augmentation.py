"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 06 - DATA AUGMENTATION
# Assignment - set nilai ke variabel
=============================================================================
Program ini mendemonstrasikan berbagai teknik data augmentation untuk
meningkatkan performa model deep learning, terutama pada dataset kecil.

Data Augmentation adalah teknik untuk meningkatkan variasi data training
secara artifisial tanpa mengumpulkan data baru.

Konsep yang dipelajari:
1. Geometric transformations (flip, rotate, scale, translate)
2. Color augmentations (brightness, contrast, saturation)
3. Noise injection (Gaussian noise, blur)
4. Advanced techniques (Cutout, Mixup, CutMix)
5. Augmentation pipelines

Kebutuhan:
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy
- (Optional) albumentations untuk advanced augmentation

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
# Assignment - set nilai ke variabel
=============================================================================
"""

# Import library/module untuk digunakan
import cv2
# Import library/module untuk digunakan
import numpy as np
# Import library/module untuk digunakan
import os


# Definisi function dengan nama dan parameter
def create_sample_image():
    """
    Membuat sample image untuk demonstrasi.
    
    Returns:
        numpy array: BGR image
    """
    # Buat gambar dengan pattern yang jelas untuk melihat efek transformasi
    size = 256
    # Buat array numpy penuh dengan nilai 0
    image = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Background gradient
    for y in range(size):
        # Iterasi/loop melalui elemen dalam koleksi
        for x in range(size):
            # Assignment - set nilai ke variabel
            image[y, x] = [
                int(100 + 50 * np.sin(x/20)),
                int(150 + 50 * np.cos(y/20)),
                int(200 - 50 * np.sin((x+y)/30))
            ]
    
    # Add shapes untuk reference
    cv2.rectangle(image, (50, 50), (100, 100), (0, 255, 0), -1)
    # Gambar lingkaran pada gambar
    cv2.circle(image, (180, 80), 40, (255, 0, 0), -1)
    # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
    cv2.putText(image, "TEST", (80, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, (255, 255, 255), 3)
    
    # Return value dari function
    return image


# =============================================================================
# GEOMETRIC TRANSFORMATIONS
# =============================================================================

# Definisi function dengan nama dan parameter
def augment_flip(image):
    """
    Flip transformations.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of flipped images
    """
    # Return value dari function
    return {
        'original': image,
        'horizontal_flip': cv2.flip(image, 1),    # Flip horizontal
        'vertical_flip': cv2.flip(image, 0),      # Flip vertical
        'both_flip': cv2.flip(image, -1)          # Flip both
    }


# Definisi function dengan nama dan parameter
def augment_rotate(image, angles=[15, 30, 45, 90]):
    """
    Rotation transformations.
    
    Args:
        image: Input BGR image
        angles: List of rotation angles
        
    Returns:
        dict: Dictionary of rotated images
    """
    # Assignment - set nilai ke variabel
    h, w = image.shape[:2]
    # Assignment - set nilai ke variabel
    center = (w // 2, h // 2)
    
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Iterasi/loop melalui elemen dalam koleksi
    for angle in angles:
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calculate new image bounds
        cos = np.abs(M[0, 0])
        # Assignment - set nilai ke variabel
        sin = np.abs(M[0, 1])
        # Assignment - set nilai ke variabel
        new_w = int(h * sin + w * cos)
        # Assignment - set nilai ke variabel
        new_h = int(h * cos + w * sin)
        
        # Adjust rotation matrix
        M[0, 2] += (new_w - w) / 2
        # Assignment - set nilai ke variabel
        M[1, 2] += (new_h - h) / 2
        
        # Apply rotation
        rotated = cv2.warpAffine(image, M, (new_w, new_h))
        
        # Resize back to original size
        rotated = cv2.resize(rotated, (w, h))
        
        # Assignment - set nilai ke variabel
        results[f'rotate_{angle}'] = rotated
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_scale(image, scales=[0.7, 0.85, 1.15, 1.3]):
    """
    Scale/zoom transformations.
    
    Args:
        image: Input BGR image
        scales: List of scale factors
        
    Returns:
        dict: Dictionary of scaled images
    """
    # Assignment - set nilai ke variabel
    h, w = image.shape[:2]
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Iterasi/loop melalui elemen dalam koleksi
    for scale in scales:
        # New dimensions
        new_w = int(w * scale)
        # Assignment - set nilai ke variabel
        new_h = int(h * scale)
        
        # Resize
        scaled = cv2.resize(image, (new_w, new_h))
        
        # Conditional statement - eksekusi jika kondisi True
        if scale > 1:
            # Crop center jika zoom in
            start_x = (new_w - w) // 2
            # Assignment - set nilai ke variabel
            start_y = (new_h - h) // 2
            # Assignment - set nilai ke variabel
            scaled = scaled[start_y:start_y+h, start_x:start_x+w]
        else:
            # Pad jika zoom out
            pad_x = (w - new_w) // 2
            # Assignment - set nilai ke variabel
            pad_y = (h - new_h) // 2
            # Buat array numpy penuh dengan nilai 0
            padded = np.zeros_like(image)
            # Assignment - set nilai ke variabel
            padded[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = scaled
            # Assignment - set nilai ke variabel
            scaled = padded
        
        # Assignment - set nilai ke variabel
        results[f'scale_{scale}'] = scaled
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_translate(image, shifts=[(20, 0), (0, 20), (20, 20), (-20, -20)]):
    """
    Translation transformations.
    
    Args:
        image: Input BGR image
        shifts: List of (dx, dy) shift values
        
    Returns:
        dict: Dictionary of translated images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Iterasi/loop melalui elemen dalam koleksi
    for dx, dy in shifts:
        # Assignment - set nilai ke variabel
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        # Terapkan transformasi affine (rotasi, translasi, skew)
        translated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        # Assignment - set nilai ke variabel
        results[f'translate_{dx}_{dy}'] = translated
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_shear(image, shear_factors=[0.1, 0.2, -0.1]):
    """
    Shear transformations.
    
    Args:
        image: Input BGR image
        shear_factors: List of shear factors
        
    Returns:
        dict: Dictionary of sheared images
    """
    # Assignment - set nilai ke variabel
    h, w = image.shape[:2]
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Iterasi/loop melalui elemen dalam koleksi
    for factor in shear_factors:
        # Shear matrix
        M = np.float32([[1, factor, 0], [0, 1, 0]])
        # Terapkan transformasi affine (rotasi, translasi, skew)
        sheared = cv2.warpAffine(image, M, (int(w * (1 + abs(factor))), h))
        # Ubah ukuran gambar ke resolusi baru
        sheared = cv2.resize(sheared, (w, h))
        # Assignment - set nilai ke variabel
        results[f'shear_{factor}'] = sheared
    
    # Return value dari function
    return results


# =============================================================================
# COLOR AUGMENTATIONS
# =============================================================================

# Definisi function dengan nama dan parameter
def augment_brightness(image, factors=[0.5, 0.75, 1.25, 1.5]):
    """
    Brightness adjustments.
    
    Args:
        image: Input BGR image
        # Assignment - set nilai ke variabel
        factors: List of brightness factors (1.0 = original)
        
    Returns:
        dict: Dictionary of brightness-adjusted images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Iterasi/loop melalui elemen dalam koleksi
    for factor in factors:
        # Convert ke float, multiply, clip, convert back
        adjusted = np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        # Assignment - set nilai ke variabel
        results[f'brightness_{factor}'] = adjusted
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_contrast(image, factors=[0.5, 0.75, 1.25, 1.5]):
    """
    Contrast adjustments.
    
    Args:
        image: Input BGR image
        factors: List of contrast factors
        
    Returns:
        dict: Dictionary of contrast-adjusted images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Iterasi/loop melalui elemen dalam koleksi
    for factor in factors:
        # Convert ke float
        img_float = image.astype(np.float32)
        
        # Calculate mean per channel
        mean = img_float.mean(axis=(0, 1), keepdims=True)
        
        # Adjust contrast around mean
        adjusted = np.clip(mean + factor * (img_float - mean), 0, 255).astype(np.uint8)
        # Assignment - set nilai ke variabel
        results[f'contrast_{factor}'] = adjusted
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_saturation(image, factors=[0.0, 0.5, 1.5, 2.0]):
    """
    Saturation adjustments.
    
    Args:
        image: Input BGR image
        # Assignment - set nilai ke variabel
        factors: List of saturation factors (0 = grayscale, 1 = original)
        
    Returns:
        dict: Dictionary of saturation-adjusted images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for factor in factors:
        # Assignment - set nilai ke variabel
        hsv_adjusted = hsv.copy()
        # Batasi nilai array antara min dan max
        hsv_adjusted[:, :, 1] = np.clip(hsv_adjusted[:, :, 1] * factor, 0, 255)
        # Konversi format warna (BGR ke RGB, dll)
        adjusted = cv2.cvtColor(hsv_adjusted.astype(np.uint8), cv2.COLOR_HSV2BGR)
        # Assignment - set nilai ke variabel
        results[f'saturation_{factor}'] = adjusted
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_hue(image, shifts=[10, 30, -10, -30]):
    """
    Hue shift transformations.
    
    Args:
        image: Input BGR image
        shifts: List of hue shift values
        
    Returns:
        dict: Dictionary of hue-shifted images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for shift in shifts:
        # Assignment - set nilai ke variabel
        hsv_adjusted = hsv.copy()
        # Assignment - set nilai ke variabel
        hsv_adjusted[:, :, 0] = (hsv_adjusted[:, :, 0] + shift) % 180
        # Konversi format warna (BGR ke RGB, dll)
        adjusted = cv2.cvtColor(hsv_adjusted.astype(np.uint8), cv2.COLOR_HSV2BGR)
        # Assignment - set nilai ke variabel
        results[f'hue_{shift}'] = adjusted
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_color_jitter(image):
    """
    Random color jittering combining brightness, contrast, saturation, hue.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of color-jittered images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    np.random.seed(42)  # For reproducibility in demo
    
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(4):
        # Assignment - set nilai ke variabel
        img = image.copy().astype(np.float32)
        
        # Random brightness
        brightness = np.random.uniform(0.7, 1.3)
        # Assignment - set nilai ke variabel
        img = img * brightness
        
        # Random contrast
        contrast = np.random.uniform(0.8, 1.2)
        # Assignment - set nilai ke variabel
        mean = img.mean(axis=(0, 1), keepdims=True)
        # Assignment - set nilai ke variabel
        img = mean + contrast * (img - mean)
        
        # Clip and convert
        img = np.clip(img, 0, 255).astype(np.uint8)
        
        # Random saturation in HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        # Assignment - set nilai ke variabel
        saturation = np.random.uniform(0.8, 1.2)
        # Batasi nilai array antara min dan max
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
        
        # Random hue shift
        hue_shift = np.random.randint(-15, 15)
        # Assignment - set nilai ke variabel
        hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
        
        # Konversi format warna (BGR ke RGB, dll)
        img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        # Assignment - set nilai ke variabel
        results[f'jitter_{i}'] = img
    
    # Return value dari function
    return results


# =============================================================================
# NOISE AND BLUR
# =============================================================================

# Definisi function dengan nama dan parameter
def augment_noise(image):
    """
    Add various types of noise.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of noisy images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Gaussian noise
    gaussian = image.copy().astype(np.float32)
    # Assignment - set nilai ke variabel
    noise = np.random.normal(0, 25, gaussian.shape)
    # Batasi nilai array antara min dan max
    gaussian = np.clip(gaussian + noise, 0, 255).astype(np.uint8)
    # Assignment - set nilai ke variabel
    results['gaussian_noise'] = gaussian
    
    # Salt and pepper noise
    sp = image.copy()
    # Salt
    num_salt = int(0.02 * image.size / 3)
    # Generate random integer dalam range tertentu
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    # Assignment - set nilai ke variabel
    sp[coords[0], coords[1]] = 255
    # Pepper
    num_pepper = int(0.02 * image.size / 3)
    # Generate random integer dalam range tertentu
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    # Assignment - set nilai ke variabel
    sp[coords[0], coords[1]] = 0
    # Assignment - set nilai ke variabel
    results['salt_pepper'] = sp
    
    # Speckle noise
    speckle = image.copy().astype(np.float32)
    # Assignment - set nilai ke variabel
    noise = np.random.randn(*speckle.shape) * 30
    # Batasi nilai array antara min dan max
    speckle = np.clip(speckle + speckle * noise / 255, 0, 255).astype(np.uint8)
    # Assignment - set nilai ke variabel
    results['speckle_noise'] = speckle
    
    # Return value dari function
    return results


# Definisi function dengan nama dan parameter
def augment_blur(image):
    """
    Apply various blur effects.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of blurred images
    """
    # Assignment - set nilai ke variabel
    results = {'original': image}
    
    # Gaussian blur
    results['gaussian_blur_3'] = cv2.GaussianBlur(image, (3, 3), 0)
    # Blur gambar untuk mengurangi noise
    results['gaussian_blur_7'] = cv2.GaussianBlur(image, (7, 7), 0)
    
    # Average blur
    results['average_blur'] = cv2.blur(image, (5, 5))
    
    # Motion blur
    kernel_size = 15
    # Buat array numpy penuh dengan nilai 0
    kernel = np.zeros((kernel_size, kernel_size))
    # Assignment - set nilai ke variabel
    kernel[kernel_size // 2, :] = 1 / kernel_size
    # Assignment - set nilai ke variabel
    motion = cv2.filter2D(image, -1, kernel)
    # Assignment - set nilai ke variabel
    results['motion_blur'] = motion
    
    # Return value dari function
    return results


# =============================================================================
# ADVANCED AUGMENTATIONS
# =============================================================================

# Definisi function dengan nama dan parameter
def augment_cutout(image, n_holes=3, hole_size=40):
    """
    Cutout augmentation - randomly mask out square regions.
    
    Reference: "Improved Regularization of CNNs with Cutout" (2017)
    
    Args:
        image: Input BGR image
        n_holes: Number of holes to cut
        hole_size: Size of each hole
        
    Returns:
        numpy array: Image with cutout applied
    """
    # Assignment - set nilai ke variabel
    h, w = image.shape[:2]
    # Buat array numpy penuh dengan nilai 1
    mask = np.ones((h, w), np.uint8) * 255
    
    # Iterasi/loop melalui elemen dalam koleksi
    for _ in range(n_holes):
        # Generate random integer dalam range tertentu
        y = np.random.randint(h)
        # Generate random integer dalam range tertentu
        x = np.random.randint(w)
        
        # Assignment - set nilai ke variabel
        y1 = max(0, y - hole_size // 2)
        # Assignment - set nilai ke variabel
        y2 = min(h, y + hole_size // 2)
        # Assignment - set nilai ke variabel
        x1 = max(0, x - hole_size // 2)
        # Assignment - set nilai ke variabel
        x2 = min(w, x + hole_size // 2)
        
        # Assignment - set nilai ke variabel
        mask[y1:y2, x1:x2] = 0
    
    # Assignment - set nilai ke variabel
    mask_3d = np.stack([mask] * 3, axis=-1)
    # Assignment - set nilai ke variabel
    result = cv2.bitwise_and(image, mask_3d)
    
    # Return value dari function
    return result


# Definisi function dengan nama dan parameter
def augment_mixup(image1, image2, alpha=0.5):
    """
    Mixup augmentation - blend two images.
    
    Reference: "mixup: Beyond Empirical Risk Minimization" (2017)
    
    Args:
        image1, image2: Input BGR images (same size)
        alpha: Blend factor (0-1)
        
    Returns:
        numpy array: Mixed image
    """
    # Ensure same size
    if image1.shape != image2.shape:
        # Ubah ukuran gambar ke resolusi baru
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    
    # Blend
    mixed = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
    
    # Return value dari function
    return mixed


# Definisi function dengan nama dan parameter
def augment_cutmix(image1, image2, beta=1.0):
    """
    CutMix augmentation - cut and paste regions between images.
    
    Reference: "CutMix: Regularization Strategy" (2019)
    
    Args:
        image1, image2: Input BGR images (same size)
        beta: Beta distribution parameter
        
    Returns:
        numpy array: CutMix result
    """
    # Assignment - set nilai ke variabel
    h, w = image1.shape[:2]
    
    # Ensure same size
    if image1.shape != image2.shape:
        # Ubah ukuran gambar ke resolusi baru
        image2 = cv2.resize(image2, (w, h))
    
    # Sample lambda from beta distribution
    lam = np.random.beta(beta, beta)
    
    # Calculate cut region
    cut_rat = np.sqrt(1 - lam)
    # Assignment - set nilai ke variabel
    cut_w = int(w * cut_rat)
    # Assignment - set nilai ke variabel
    cut_h = int(h * cut_rat)
    
    # Random center
    cx = np.random.randint(w)
    # Generate random integer dalam range tertentu
    cy = np.random.randint(h)
    
    # Bounding box
    bbx1 = max(0, cx - cut_w // 2)
    # Assignment - set nilai ke variabel
    bby1 = max(0, cy - cut_h // 2)
    # Assignment - set nilai ke variabel
    bbx2 = min(w, cx + cut_w // 2)
    # Assignment - set nilai ke variabel
    bby2 = min(h, cy + cut_h // 2)
    
    # Apply cutmix
    result = image1.copy()
    # Assignment - set nilai ke variabel
    result[bby1:bby2, bbx1:bbx2] = image2[bby1:bby2, bbx1:bbx2]
    
    # Return value dari function
    return result


# Definisi function dengan nama dan parameter
def demo_geometric_augmentations():
    """
    Demonstrasi geometric augmentations.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("GEOMETRIC AUGMENTATIONS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Assignment - set nilai ke variabel
    image = create_sample_image()
    
    # Demonstrate each type
    augmentations = {
        'Flip': augment_flip(image),
        'Rotate': augment_rotate(image, [15, 45, 90]),
        'Scale': augment_scale(image, [0.7, 1.3]),
        'Translate': augment_translate(image, [(30, 0), (0, 30)]),
        'Shear': augment_shear(image, [0.15, -0.15])
    }
    
    # Iterasi/loop melalui elemen dalam koleksi
    for aug_type, results in augmentations.items():
        print(f"\n[{aug_type}]")
        
        # Combine images for display
        images_row = []
        # Assignment - set nilai ke variabel
        labels = list(results.keys())
        
        # Iterasi/loop melalui elemen dalam koleksi
        for label, img in results.items():
            # Add label
            display = img.copy()
            # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
            cv2.putText(display, label[:15], (5, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
            # Ubah ukuran gambar ke resolusi baru
            images_row.append(cv2.resize(display, (150, 150)))
        
        # Display row
        combined = np.hstack(images_row[:5])  # Max 5 per row
        # Tampilkan gambar di window
        cv2.imshow(f"Geometric - {aug_type}", combined)
        
        print(f"  Variants: {', '.join(labels)}")
    
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_color_augmentations():
    """
    Demonstrasi color augmentations.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("COLOR AUGMENTATIONS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Assignment - set nilai ke variabel
    image = create_sample_image()
    
    # Assignment - set nilai ke variabel
    augmentations = {
        'Brightness': augment_brightness(image, [0.5, 1.0, 1.5]),
        'Contrast': augment_contrast(image, [0.5, 1.0, 1.5]),
        'Saturation': augment_saturation(image, [0.0, 1.0, 2.0]),
        'Hue': augment_hue(image, [0, 30, -30]),
        'Color Jitter': augment_color_jitter(image)
    }
    
    # Iterasi/loop melalui elemen dalam koleksi
    for aug_type, results in augmentations.items():
        print(f"\n[{aug_type}]")
        
        # Assignment - set nilai ke variabel
        images_row = []
        # Assignment - set nilai ke variabel
        labels = list(results.keys())
        
        # Iterasi/loop melalui elemen dalam koleksi
        for label, img in results.items():
            # Assignment - set nilai ke variabel
            display = img.copy()
            # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
            cv2.putText(display, label[:15], (5, 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
            # Ubah ukuran gambar ke resolusi baru
            images_row.append(cv2.resize(display, (150, 150)))
        
        # Assignment - set nilai ke variabel
        combined = np.hstack(images_row[:5])
        # Tampilkan gambar di window
        cv2.imshow(f"Color - {aug_type}", combined)
        
        print(f"  Variants: {', '.join(labels)}")
    
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_noise_blur():
    """
    Demonstrasi noise dan blur augmentations.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("NOISE & BLUR AUGMENTATIONS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Assignment - set nilai ke variabel
    image = create_sample_image()
    
    # Noise
    noise_results = augment_noise(image)
    print("\n[Noise Types]")
    
    # Assignment - set nilai ke variabel
    images_row = []
    # Iterasi/loop melalui elemen dalam koleksi
    for label, img in noise_results.items():
        # Assignment - set nilai ke variabel
        display = img.copy()
        # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
        cv2.putText(display, label[:15], (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        # Ubah ukuran gambar ke resolusi baru
        images_row.append(cv2.resize(display, (150, 150)))
    
    # Assignment - set nilai ke variabel
    combined = np.hstack(images_row)
    # Tampilkan gambar di window
    cv2.imshow("Noise Augmentations", combined)
    print(f"  Variants: {', '.join(noise_results.keys())}")
    
    # Blur
    blur_results = augment_blur(image)
    print("\n[Blur Types]")
    
    # Assignment - set nilai ke variabel
    images_row = []
    # Iterasi/loop melalui elemen dalam koleksi
    for label, img in blur_results.items():
        # Assignment - set nilai ke variabel
        display = img.copy()
        # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
        cv2.putText(display, label[:15], (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        # Ubah ukuran gambar ke resolusi baru
        images_row.append(cv2.resize(display, (150, 150)))
    
    # Assignment - set nilai ke variabel
    combined = np.hstack(images_row)
    # Tampilkan gambar di window
    cv2.imshow("Blur Augmentations", combined)
    print(f"  Variants: {', '.join(blur_results.keys())}")
    
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_advanced_augmentations():
    """
    Demonstrasi advanced augmentations.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("ADVANCED AUGMENTATIONS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Assignment - set nilai ke variabel
    image1 = create_sample_image()
    
    # Create second image untuk mixup/cutmix
    image2 = np.zeros_like(image1)
    # Gambar lingkaran pada gambar
    cv2.circle(image2, (128, 128), 100, (255, 0, 0), -1)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(image2, (50, 50), (200, 200), (0, 255, 0), 3)
    
    print("\n[Cutout]")
    # Assignment - set nilai ke variabel
    cutout_results = []
    cutout_results.append(('original', image1))
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(3):
        # Assignment - set nilai ke variabel
        cutout = augment_cutout(image1.copy(), n_holes=2, hole_size=50)
        cutout_results.append((f'cutout_{i}', cutout))
    
    # Assignment - set nilai ke variabel
    images_row = []
    # Iterasi/loop melalui elemen dalam koleksi
    for label, img in cutout_results:
        # Assignment - set nilai ke variabel
        display = img.copy()
        # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        # Ubah ukuran gambar ke resolusi baru
        images_row.append(cv2.resize(display, (150, 150)))
    
    # Tampilkan gambar di window
    cv2.imshow("Cutout", np.hstack(images_row))
    
    print("\n[Mixup]")
    # Assignment - set nilai ke variabel
    mixup_results = [
        ('image1', image1),
        ('image2', image2),
        ('mixup_0.3', augment_mixup(image1, image2, 0.3)),
        ('mixup_0.5', augment_mixup(image1, image2, 0.5)),
        ('mixup_0.7', augment_mixup(image1, image2, 0.7)),
    ]
    
    # Assignment - set nilai ke variabel
    images_row = []
    # Iterasi/loop melalui elemen dalam koleksi
    for label, img in mixup_results:
        # Assignment - set nilai ke variabel
        display = img.copy()
        # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        # Ubah ukuran gambar ke resolusi baru
        images_row.append(cv2.resize(display, (150, 150)))
    
    # Tampilkan gambar di window
    cv2.imshow("Mixup", np.hstack(images_row))
    
    print("\n[CutMix]")
    # Assignment - set nilai ke variabel
    cutmix_results = [
        ('image1', image1),
        ('image2', image2),
    ]
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(3):
        # Assignment - set nilai ke variabel
        cutmix = augment_cutmix(image1.copy(), image2.copy())
        cutmix_results.append((f'cutmix_{i}', cutmix))
    
    # Assignment - set nilai ke variabel
    images_row = []
    # Iterasi/loop melalui elemen dalam koleksi
    for label, img in cutmix_results:
        # Assignment - set nilai ke variabel
        display = img.copy()
        # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        # Ubah ukuran gambar ke resolusi baru
        images_row.append(cv2.resize(display, (150, 150)))
    
    # Tampilkan gambar di window
    cv2.imshow("CutMix", np.hstack(images_row))
    
    print("\n[INFO] Tekan 'q' untuk menutup gambar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_augmentation_pipeline():
    """
    Demonstrasi pipeline augmentation yang mengkombinasikan berbagai teknik.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("AUGMENTATION PIPELINE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFO] Typical Augmentation Pipeline:
    
    1. Geometric transforms (50% chance each):
       - Random horizontal flip
       - Random rotation (-15° to +15°)
       - Random scale (0.9 to 1.1)
    
    2. Color transforms (30% chance each):
       - Brightness adjustment (0.8 to 1.2)
       - Contrast adjustment (0.8 to 1.2)
       - Saturation adjustment (0.8 to 1.2)
    
    3. Optional regularization (20% chance):
       - Cutout / Random erasing
       - Gaussian noise
    
    4. Normalization:
       - Subtract mean, divide by std
    """)
    
    # Assignment - set nilai ke variabel
    image = create_sample_image()
    
    # Apply pipeline multiple times
    print("\n[INFO] Generating augmented samples...")
    
    np.random.seed(None)  # Random seed
    
    # Assignment - set nilai ke variabel
    augmented_images = [('original', image)]
    
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(7):
        # Assignment - set nilai ke variabel
        aug = image.copy()
        
        # Random flip
        if np.random.random() > 0.5:
            # Assignment - set nilai ke variabel
            aug = cv2.flip(aug, 1)
        
        # Random rotation
        if np.random.random() > 0.5:
            # Assignment - set nilai ke variabel
            angle = np.random.uniform(-15, 15)
            # Assignment - set nilai ke variabel
            h, w = aug.shape[:2]
            # Hitung matriks rotasi 2D
            M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
            # Terapkan transformasi affine (rotasi, translasi, skew)
            aug = cv2.warpAffine(aug, M, (w, h))
        
        # Random brightness
        if np.random.random() > 0.7:
            # Assignment - set nilai ke variabel
            factor = np.random.uniform(0.8, 1.2)
            # Batasi nilai array antara min dan max
            aug = np.clip(aug.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        
        # Random cutout
        if np.random.random() > 0.8:
            # Assignment - set nilai ke variabel
            aug = augment_cutout(aug, n_holes=1, hole_size=40)
        
        augmented_images.append((f'aug_{i}', aug))
    
    # Display
    images_row = []
    # Iterasi/loop melalui elemen dalam koleksi
    for label, img in augmented_images:
        # Assignment - set nilai ke variabel
        display = img.copy()
        # Tambahkan teks pada gambar (image, text, position, font, scale, color, thickness)
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        # Ubah ukuran gambar ke resolusi baru
        images_row.append(cv2.resize(display, (120, 120)))
    
    # Arrange in 2 rows
    row1 = np.hstack(images_row[:4])
    # Assignment - set nilai ke variabel
    row2 = np.hstack(images_row[4:])
    # Assignment - set nilai ke variabel
    combined = np.vstack([row1, row2])
    
    # Tampilkan gambar di window
    cv2.imshow("Augmentation Pipeline Results", combined)
    
    print("[INFO] Tekan 'q' untuk keluar...")
    # Loop berulang selama kondisi bernilai True
    while True:
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(1) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:  # 'q' atau ESC
            break
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM DATA AUGMENTATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Geometric Augmentations (Flip, Rotate, Scale, etc.)")
        print("2. Color Augmentations (Brightness, Contrast, etc.)")
        print("3. Noise & Blur Augmentations")
        print("4. Advanced Augmentations (Cutout, Mixup, CutMix)")
        print("5. Augmentation Pipeline")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-6): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_geometric_augmentations()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_color_augmentations()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_noise_blur()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_advanced_augmentations()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_augmentation_pipeline()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_geometric_augmentations()
            demo_color_augmentations()
            demo_noise_blur()
            demo_advanced_augmentations()
            demo_augmentation_pipeline()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
