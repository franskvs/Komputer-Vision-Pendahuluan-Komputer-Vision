"""
=============================================================================
PRAKTIKUM 06 - DATA AUGMENTATION
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
- opencv-python >= 4.8.0
- numpy
- (Optional) albumentations untuk advanced augmentation

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import os


def create_sample_image():
    """
    Membuat sample image untuk demonstrasi.
    
    Returns:
        numpy array: BGR image
    """
    # Buat gambar dengan pattern yang jelas untuk melihat efek transformasi
    size = 256
    image = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Background gradient
    for y in range(size):
        for x in range(size):
            image[y, x] = [
                int(100 + 50 * np.sin(x/20)),
                int(150 + 50 * np.cos(y/20)),
                int(200 - 50 * np.sin((x+y)/30))
            ]
    
    # Add shapes untuk reference
    cv2.rectangle(image, (50, 50), (100, 100), (0, 255, 0), -1)
    cv2.circle(image, (180, 80), 40, (255, 0, 0), -1)
    cv2.putText(image, "TEST", (80, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, (255, 255, 255), 3)
    
    return image


# =============================================================================
# GEOMETRIC TRANSFORMATIONS
# =============================================================================

def augment_flip(image):
    """
    Flip transformations.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of flipped images
    """
    return {
        'original': image,
        'horizontal_flip': cv2.flip(image, 1),    # Flip horizontal
        'vertical_flip': cv2.flip(image, 0),      # Flip vertical
        'both_flip': cv2.flip(image, -1)          # Flip both
    }


def augment_rotate(image, angles=[15, 30, 45, 90]):
    """
    Rotation transformations.
    
    Args:
        image: Input BGR image
        angles: List of rotation angles
        
    Returns:
        dict: Dictionary of rotated images
    """
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    results = {'original': image}
    
    for angle in angles:
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calculate new image bounds
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int(h * sin + w * cos)
        new_h = int(h * cos + w * sin)
        
        # Adjust rotation matrix
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2
        
        # Apply rotation
        rotated = cv2.warpAffine(image, M, (new_w, new_h))
        
        # Resize back to original size
        rotated = cv2.resize(rotated, (w, h))
        
        results[f'rotate_{angle}'] = rotated
    
    return results


def augment_scale(image, scales=[0.7, 0.85, 1.15, 1.3]):
    """
    Scale/zoom transformations.
    
    Args:
        image: Input BGR image
        scales: List of scale factors
        
    Returns:
        dict: Dictionary of scaled images
    """
    h, w = image.shape[:2]
    results = {'original': image}
    
    for scale in scales:
        # New dimensions
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize
        scaled = cv2.resize(image, (new_w, new_h))
        
        if scale > 1:
            # Crop center jika zoom in
            start_x = (new_w - w) // 2
            start_y = (new_h - h) // 2
            scaled = scaled[start_y:start_y+h, start_x:start_x+w]
        else:
            # Pad jika zoom out
            pad_x = (w - new_w) // 2
            pad_y = (h - new_h) // 2
            padded = np.zeros_like(image)
            padded[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = scaled
            scaled = padded
        
        results[f'scale_{scale}'] = scaled
    
    return results


def augment_translate(image, shifts=[(20, 0), (0, 20), (20, 20), (-20, -20)]):
    """
    Translation transformations.
    
    Args:
        image: Input BGR image
        shifts: List of (dx, dy) shift values
        
    Returns:
        dict: Dictionary of translated images
    """
    results = {'original': image}
    
    for dx, dy in shifts:
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        translated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        results[f'translate_{dx}_{dy}'] = translated
    
    return results


def augment_shear(image, shear_factors=[0.1, 0.2, -0.1]):
    """
    Shear transformations.
    
    Args:
        image: Input BGR image
        shear_factors: List of shear factors
        
    Returns:
        dict: Dictionary of sheared images
    """
    h, w = image.shape[:2]
    results = {'original': image}
    
    for factor in shear_factors:
        # Shear matrix
        M = np.float32([[1, factor, 0], [0, 1, 0]])
        sheared = cv2.warpAffine(image, M, (int(w * (1 + abs(factor))), h))
        sheared = cv2.resize(sheared, (w, h))
        results[f'shear_{factor}'] = sheared
    
    return results


# =============================================================================
# COLOR AUGMENTATIONS
# =============================================================================

def augment_brightness(image, factors=[0.5, 0.75, 1.25, 1.5]):
    """
    Brightness adjustments.
    
    Args:
        image: Input BGR image
        factors: List of brightness factors (1.0 = original)
        
    Returns:
        dict: Dictionary of brightness-adjusted images
    """
    results = {'original': image}
    
    for factor in factors:
        # Convert ke float, multiply, clip, convert back
        adjusted = np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        results[f'brightness_{factor}'] = adjusted
    
    return results


def augment_contrast(image, factors=[0.5, 0.75, 1.25, 1.5]):
    """
    Contrast adjustments.
    
    Args:
        image: Input BGR image
        factors: List of contrast factors
        
    Returns:
        dict: Dictionary of contrast-adjusted images
    """
    results = {'original': image}
    
    for factor in factors:
        # Convert ke float
        img_float = image.astype(np.float32)
        
        # Calculate mean per channel
        mean = img_float.mean(axis=(0, 1), keepdims=True)
        
        # Adjust contrast around mean
        adjusted = np.clip(mean + factor * (img_float - mean), 0, 255).astype(np.uint8)
        results[f'contrast_{factor}'] = adjusted
    
    return results


def augment_saturation(image, factors=[0.0, 0.5, 1.5, 2.0]):
    """
    Saturation adjustments.
    
    Args:
        image: Input BGR image
        factors: List of saturation factors (0 = grayscale, 1 = original)
        
    Returns:
        dict: Dictionary of saturation-adjusted images
    """
    results = {'original': image}
    
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    for factor in factors:
        hsv_adjusted = hsv.copy()
        hsv_adjusted[:, :, 1] = np.clip(hsv_adjusted[:, :, 1] * factor, 0, 255)
        adjusted = cv2.cvtColor(hsv_adjusted.astype(np.uint8), cv2.COLOR_HSV2BGR)
        results[f'saturation_{factor}'] = adjusted
    
    return results


def augment_hue(image, shifts=[10, 30, -10, -30]):
    """
    Hue shift transformations.
    
    Args:
        image: Input BGR image
        shifts: List of hue shift values
        
    Returns:
        dict: Dictionary of hue-shifted images
    """
    results = {'original': image}
    
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    for shift in shifts:
        hsv_adjusted = hsv.copy()
        hsv_adjusted[:, :, 0] = (hsv_adjusted[:, :, 0] + shift) % 180
        adjusted = cv2.cvtColor(hsv_adjusted.astype(np.uint8), cv2.COLOR_HSV2BGR)
        results[f'hue_{shift}'] = adjusted
    
    return results


def augment_color_jitter(image):
    """
    Random color jittering combining brightness, contrast, saturation, hue.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of color-jittered images
    """
    results = {'original': image}
    
    np.random.seed(42)  # For reproducibility in demo
    
    for i in range(4):
        img = image.copy().astype(np.float32)
        
        # Random brightness
        brightness = np.random.uniform(0.7, 1.3)
        img = img * brightness
        
        # Random contrast
        contrast = np.random.uniform(0.8, 1.2)
        mean = img.mean(axis=(0, 1), keepdims=True)
        img = mean + contrast * (img - mean)
        
        # Clip and convert
        img = np.clip(img, 0, 255).astype(np.uint8)
        
        # Random saturation in HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        saturation = np.random.uniform(0.8, 1.2)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
        
        # Random hue shift
        hue_shift = np.random.randint(-15, 15)
        hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
        
        img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        results[f'jitter_{i}'] = img
    
    return results


# =============================================================================
# NOISE AND BLUR
# =============================================================================

def augment_noise(image):
    """
    Add various types of noise.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of noisy images
    """
    results = {'original': image}
    
    # Gaussian noise
    gaussian = image.copy().astype(np.float32)
    noise = np.random.normal(0, 25, gaussian.shape)
    gaussian = np.clip(gaussian + noise, 0, 255).astype(np.uint8)
    results['gaussian_noise'] = gaussian
    
    # Salt and pepper noise
    sp = image.copy()
    # Salt
    num_salt = int(0.02 * image.size / 3)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    sp[coords[0], coords[1]] = 255
    # Pepper
    num_pepper = int(0.02 * image.size / 3)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    sp[coords[0], coords[1]] = 0
    results['salt_pepper'] = sp
    
    # Speckle noise
    speckle = image.copy().astype(np.float32)
    noise = np.random.randn(*speckle.shape) * 30
    speckle = np.clip(speckle + speckle * noise / 255, 0, 255).astype(np.uint8)
    results['speckle_noise'] = speckle
    
    return results


def augment_blur(image):
    """
    Apply various blur effects.
    
    Args:
        image: Input BGR image
        
    Returns:
        dict: Dictionary of blurred images
    """
    results = {'original': image}
    
    # Gaussian blur
    results['gaussian_blur_3'] = cv2.GaussianBlur(image, (3, 3), 0)
    results['gaussian_blur_7'] = cv2.GaussianBlur(image, (7, 7), 0)
    
    # Average blur
    results['average_blur'] = cv2.blur(image, (5, 5))
    
    # Motion blur
    kernel_size = 15
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[kernel_size // 2, :] = 1 / kernel_size
    motion = cv2.filter2D(image, -1, kernel)
    results['motion_blur'] = motion
    
    return results


# =============================================================================
# ADVANCED AUGMENTATIONS
# =============================================================================

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
    h, w = image.shape[:2]
    mask = np.ones((h, w), np.uint8) * 255
    
    for _ in range(n_holes):
        y = np.random.randint(h)
        x = np.random.randint(w)
        
        y1 = max(0, y - hole_size // 2)
        y2 = min(h, y + hole_size // 2)
        x1 = max(0, x - hole_size // 2)
        x2 = min(w, x + hole_size // 2)
        
        mask[y1:y2, x1:x2] = 0
    
    mask_3d = np.stack([mask] * 3, axis=-1)
    result = cv2.bitwise_and(image, mask_3d)
    
    return result


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
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    
    # Blend
    mixed = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
    
    return mixed


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
    h, w = image1.shape[:2]
    
    # Ensure same size
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (w, h))
    
    # Sample lambda from beta distribution
    lam = np.random.beta(beta, beta)
    
    # Calculate cut region
    cut_rat = np.sqrt(1 - lam)
    cut_w = int(w * cut_rat)
    cut_h = int(h * cut_rat)
    
    # Random center
    cx = np.random.randint(w)
    cy = np.random.randint(h)
    
    # Bounding box
    bbx1 = max(0, cx - cut_w // 2)
    bby1 = max(0, cy - cut_h // 2)
    bbx2 = min(w, cx + cut_w // 2)
    bby2 = min(h, cy + cut_h // 2)
    
    # Apply cutmix
    result = image1.copy()
    result[bby1:bby2, bbx1:bbx2] = image2[bby1:bby2, bbx1:bbx2]
    
    return result


def demo_geometric_augmentations():
    """
    Demonstrasi geometric augmentations.
    """
    print("\n" + "="*70)
    print("GEOMETRIC AUGMENTATIONS")
    print("="*70)
    
    image = create_sample_image()
    
    # Demonstrate each type
    augmentations = {
        'Flip': augment_flip(image),
        'Rotate': augment_rotate(image, [15, 45, 90]),
        'Scale': augment_scale(image, [0.7, 1.3]),
        'Translate': augment_translate(image, [(30, 0), (0, 30)]),
        'Shear': augment_shear(image, [0.15, -0.15])
    }
    
    for aug_type, results in augmentations.items():
        print(f"\n[{aug_type}]")
        
        # Combine images for display
        images_row = []
        labels = list(results.keys())
        
        for label, img in results.items():
            # Add label
            display = img.copy()
            cv2.putText(display, label[:15], (5, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
            images_row.append(cv2.resize(display, (150, 150)))
        
        # Display row
        combined = np.hstack(images_row[:5])  # Max 5 per row
        cv2.imshow(f"Geometric - {aug_type}", combined)
        
        print(f"  Variants: {', '.join(labels)}")
    
    print("\n[INFO] Tekan tombol apa saja untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_color_augmentations():
    """
    Demonstrasi color augmentations.
    """
    print("\n" + "="*70)
    print("COLOR AUGMENTATIONS")
    print("="*70)
    
    image = create_sample_image()
    
    augmentations = {
        'Brightness': augment_brightness(image, [0.5, 1.0, 1.5]),
        'Contrast': augment_contrast(image, [0.5, 1.0, 1.5]),
        'Saturation': augment_saturation(image, [0.0, 1.0, 2.0]),
        'Hue': augment_hue(image, [0, 30, -30]),
        'Color Jitter': augment_color_jitter(image)
    }
    
    for aug_type, results in augmentations.items():
        print(f"\n[{aug_type}]")
        
        images_row = []
        labels = list(results.keys())
        
        for label, img in results.items():
            display = img.copy()
            cv2.putText(display, label[:15], (5, 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
            images_row.append(cv2.resize(display, (150, 150)))
        
        combined = np.hstack(images_row[:5])
        cv2.imshow(f"Color - {aug_type}", combined)
        
        print(f"  Variants: {', '.join(labels)}")
    
    print("\n[INFO] Tekan tombol apa saja untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_noise_blur():
    """
    Demonstrasi noise dan blur augmentations.
    """
    print("\n" + "="*70)
    print("NOISE & BLUR AUGMENTATIONS")
    print("="*70)
    
    image = create_sample_image()
    
    # Noise
    noise_results = augment_noise(image)
    print("\n[Noise Types]")
    
    images_row = []
    for label, img in noise_results.items():
        display = img.copy()
        cv2.putText(display, label[:15], (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        images_row.append(cv2.resize(display, (150, 150)))
    
    combined = np.hstack(images_row)
    cv2.imshow("Noise Augmentations", combined)
    print(f"  Variants: {', '.join(noise_results.keys())}")
    
    # Blur
    blur_results = augment_blur(image)
    print("\n[Blur Types]")
    
    images_row = []
    for label, img in blur_results.items():
        display = img.copy()
        cv2.putText(display, label[:15], (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        images_row.append(cv2.resize(display, (150, 150)))
    
    combined = np.hstack(images_row)
    cv2.imshow("Blur Augmentations", combined)
    print(f"  Variants: {', '.join(blur_results.keys())}")
    
    print("\n[INFO] Tekan tombol apa saja untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_advanced_augmentations():
    """
    Demonstrasi advanced augmentations.
    """
    print("\n" + "="*70)
    print("ADVANCED AUGMENTATIONS")
    print("="*70)
    
    image1 = create_sample_image()
    
    # Create second image untuk mixup/cutmix
    image2 = np.zeros_like(image1)
    cv2.circle(image2, (128, 128), 100, (255, 0, 0), -1)
    cv2.rectangle(image2, (50, 50), (200, 200), (0, 255, 0), 3)
    
    print("\n[Cutout]")
    cutout_results = []
    cutout_results.append(('original', image1))
    for i in range(3):
        cutout = augment_cutout(image1.copy(), n_holes=2, hole_size=50)
        cutout_results.append((f'cutout_{i}', cutout))
    
    images_row = []
    for label, img in cutout_results:
        display = img.copy()
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        images_row.append(cv2.resize(display, (150, 150)))
    
    cv2.imshow("Cutout", np.hstack(images_row))
    
    print("\n[Mixup]")
    mixup_results = [
        ('image1', image1),
        ('image2', image2),
        ('mixup_0.3', augment_mixup(image1, image2, 0.3)),
        ('mixup_0.5', augment_mixup(image1, image2, 0.5)),
        ('mixup_0.7', augment_mixup(image1, image2, 0.7)),
    ]
    
    images_row = []
    for label, img in mixup_results:
        display = img.copy()
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        images_row.append(cv2.resize(display, (150, 150)))
    
    cv2.imshow("Mixup", np.hstack(images_row))
    
    print("\n[CutMix]")
    cutmix_results = [
        ('image1', image1),
        ('image2', image2),
    ]
    for i in range(3):
        cutmix = augment_cutmix(image1.copy(), image2.copy())
        cutmix_results.append((f'cutmix_{i}', cutmix))
    
    images_row = []
    for label, img in cutmix_results:
        display = img.copy()
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        images_row.append(cv2.resize(display, (150, 150)))
    
    cv2.imshow("CutMix", np.hstack(images_row))
    
    print("\n[INFO] Tekan tombol apa saja untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_augmentation_pipeline():
    """
    Demonstrasi pipeline augmentation yang mengkombinasikan berbagai teknik.
    """
    print("\n" + "="*70)
    print("AUGMENTATION PIPELINE")
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
    
    image = create_sample_image()
    
    # Apply pipeline multiple times
    print("\n[INFO] Generating augmented samples...")
    
    np.random.seed(None)  # Random seed
    
    augmented_images = [('original', image)]
    
    for i in range(7):
        aug = image.copy()
        
        # Random flip
        if np.random.random() > 0.5:
            aug = cv2.flip(aug, 1)
        
        # Random rotation
        if np.random.random() > 0.5:
            angle = np.random.uniform(-15, 15)
            h, w = aug.shape[:2]
            M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
            aug = cv2.warpAffine(aug, M, (w, h))
        
        # Random brightness
        if np.random.random() > 0.7:
            factor = np.random.uniform(0.8, 1.2)
            aug = np.clip(aug.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        
        # Random cutout
        if np.random.random() > 0.8:
            aug = augment_cutout(aug, n_holes=1, hole_size=40)
        
        augmented_images.append((f'aug_{i}', aug))
    
    # Display
    images_row = []
    for label, img in augmented_images:
        display = img.copy()
        cv2.putText(display, label, (5, 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        images_row.append(cv2.resize(display, (120, 120)))
    
    # Arrange in 2 rows
    row1 = np.hstack(images_row[:4])
    row2 = np.hstack(images_row[4:])
    combined = np.vstack([row1, row2])
    
    cv2.imshow("Augmentation Pipeline Results", combined)
    
    print("[INFO] Tekan tombol apa saja untuk keluar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM DATA AUGMENTATION")
    print("="*70)
    
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
        
        choice = input("\nPilih menu (0-6): ").strip()
        
        if choice == '1':
            demo_geometric_augmentations()
        elif choice == '2':
            demo_color_augmentations()
        elif choice == '3':
            demo_noise_blur()
        elif choice == '4':
            demo_advanced_augmentations()
        elif choice == '5':
            demo_augmentation_pipeline()
        elif choice == '6':
            demo_geometric_augmentations()
            demo_color_augmentations()
            demo_noise_blur()
            demo_advanced_augmentations()
            demo_augmentation_pipeline()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
