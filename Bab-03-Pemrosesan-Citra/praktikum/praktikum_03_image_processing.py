"""
PRAKTIKUM BAB 3: PEMROSESAN CITRA (IMAGE PROCESSING)
=====================================================

Tujuan:
1. Memahami dan menerapkan point operators
2. Mengimplementasikan berbagai filter linear dan non-linear
3. Melakukan transformasi Fourier dan filtering frekuensi
4. Membuat image pyramids
5. Menerapkan edge detection dan segmentasi dasar

Kebutuhan:
- Python 3.8+
- OpenCV (cv2)
- NumPy
- Matplotlib
- SciPy
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage, signal
from scipy.fft import fft2, ifft2, fftshift
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# BAGIAN 1: POINT OPERATORS
# ============================================================

print("=" * 60)
print("BAGIAN 1: POINT OPERATORS")
print("=" * 60)

def create_sample_image():
    """Buat gambar sample untuk praktek"""
    # Buat gambar dengan gradient dan beberapa fitur
    img = np.zeros((300, 400), dtype=np.uint8)
    
    # Background gradient
    for i in range(300):
        img[i, :] = int(50 + i * 0.5)
    
    # Tambahkan objek
    cv2.rectangle(img, (50, 50), (150, 150), 200, -1)
    cv2.circle(img, (300, 150), 60, 180, -1)
    cv2.ellipse(img, (200, 220), (80, 40), 0, 0, 360, 220, -1)
    
    # Tambahkan noise
    noise = np.random.normal(0, 10, img.shape).astype(np.float32)
    img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    return img

def brightness_contrast(image, alpha=1.0, beta=0):
    """
    Atur brightness dan contrast
    g(x) = alpha * f(x) + beta
    
    Parameters:
        alpha: contrast (1.0 = normal, >1 = tinggi, <1 = rendah)
        beta: brightness (-255 to 255)
    """
    result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return result

def gamma_correction(image, gamma=1.0):
    """
    Koreksi gamma
    g = c * f^gamma
    
    Parameters:
        gamma: gamma value (<1 = terang, >1 = gelap)
    """
    # Normalisasi ke 0-1
    normalized = image / 255.0
    # Terapkan gamma
    corrected = np.power(normalized, gamma)
    # Kembali ke 0-255
    return (corrected * 255).astype(np.uint8)

def histogram_equalization(image):
    """
    Equalisasi histogram untuk meningkatkan kontras
    """
    if len(image.shape) == 3:
        # Untuk gambar berwarna, convert ke LAB dan equalize L channel
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab[:,:,0] = cv2.equalizeHist(lab[:,:,0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        return cv2.equalizeHist(image)

def clahe_enhancement(image, clip_limit=2.0, tile_size=(8, 8)):
    """
    Contrast Limited Adaptive Histogram Equalization (CLAHE)
    Lebih baik dari histogram equalization biasa
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        return clahe.apply(image)

# Demo Point Operators
def demo_point_operators():
    """Demonstrasi point operators"""
    img = create_sample_image()
    
    # Berbagai transformasi
    bright = brightness_contrast(img, alpha=1.0, beta=50)
    contrast = brightness_contrast(img, alpha=1.5, beta=0)
    gamma_low = gamma_correction(img, gamma=0.5)
    gamma_high = gamma_correction(img, gamma=2.0)
    hist_eq = histogram_equalization(img)
    clahe_img = clahe_enhancement(img)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    images = [img, bright, contrast, gamma_low, 
              gamma_high, hist_eq, clahe_img, img]
    titles = ['Original', 'Brightness +50', 'Contrast x1.5', 'Gamma=0.5',
              'Gamma=2.0', 'Histogram Eq', 'CLAHE', 'Histogram Original']
    
    for i in range(7):
        ax = axes[i//4, i%4]
        ax.imshow(images[i], cmap='gray')
        ax.set_title(titles[i])
        ax.axis('off')
    
    # Histogram
    axes[1, 3].hist(img.ravel(), 256, [0, 256], alpha=0.5, label='Original')
    axes[1, 3].hist(hist_eq.ravel(), 256, [0, 256], alpha=0.5, label='Equalized')
    axes[1, 3].set_title('Histogram Comparison')
    axes[1, 3].legend()
    
    plt.tight_layout()
    plt.savefig('output_point_operators.png', dpi=150)
    plt.show()
    
    print("✅ Point operators demo selesai!")
    print("   Output: output_point_operators.png")

# ============================================================
# BAGIAN 2: LINEAR FILTERING (CONVOLUTION)
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 2: LINEAR FILTERING (CONVOLUTION)")
print("=" * 60)

def create_kernel(kernel_type, size=3, sigma=1.0):
    """
    Buat berbagai jenis kernel
    
    Parameters:
        kernel_type: 'box', 'gaussian', 'laplacian', 'sobel_x', 'sobel_y'
        size: ukuran kernel (harus ganjil)
        sigma: sigma untuk gaussian
    """
    if kernel_type == 'box':
        return np.ones((size, size), dtype=np.float32) / (size * size)
    
    elif kernel_type == 'gaussian':
        ax = np.linspace(-(size-1)/2., (size-1)/2., size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-0.5 * (xx**2 + yy**2) / sigma**2)
        return kernel / kernel.sum()
    
    elif kernel_type == 'laplacian':
        return np.array([[0, 1, 0],
                        [1, -4, 1],
                        [0, 1, 0]], dtype=np.float32)
    
    elif kernel_type == 'laplacian_8':
        return np.array([[1, 1, 1],
                        [1, -8, 1],
                        [1, 1, 1]], dtype=np.float32)
    
    elif kernel_type == 'sobel_x':
        return np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32)
    
    elif kernel_type == 'sobel_y':
        return np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]], dtype=np.float32)
    
    elif kernel_type == 'sharpen':
        return np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]], dtype=np.float32)
    
    elif kernel_type == 'emboss':
        return np.array([[-2, -1, 0],
                        [-1, 1, 1],
                        [0, 1, 2]], dtype=np.float32)

def convolve_manual(image, kernel):
    """
    Implementasi manual konvolusi 2D
    Untuk pemahaman - gunakan cv2.filter2D untuk kecepatan
    """
    h, w = image.shape[:2]
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    
    # Padding
    if len(image.shape) == 3:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='reflect')
    else:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    
    # Output
    output = np.zeros_like(image, dtype=np.float32)
    
    # Konvolusi
    for i in range(h):
        for j in range(w):
            if len(image.shape) == 3:
                for c in range(image.shape[2]):
                    region = padded[i:i+kh, j:j+kw, c]
                    output[i, j, c] = np.sum(region * kernel)
            else:
                region = padded[i:i+kh, j:j+kw]
                output[i, j] = np.sum(region * kernel)
    
    return output

def demo_linear_filters():
    """Demonstrasi berbagai linear filter"""
    img = create_sample_image()
    
    # Buat gambar dengan noise untuk demo smoothing
    noisy = img.copy()
    noise = np.random.normal(0, 25, img.shape)
    noisy = np.clip(noisy.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    # Terapkan berbagai filter
    box_filtered = cv2.blur(noisy, (5, 5))
    gaussian_filtered = cv2.GaussianBlur(noisy, (5, 5), 1.5)
    
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)
    
    sharpen_kernel = create_kernel('sharpen')
    sharpened = cv2.filter2D(img, -1, sharpen_kernel)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    images = [noisy, box_filtered, gaussian_filtered, sharpened,
              np.abs(laplacian), sobel_x, sobel_y, sobel_mag]
    titles = ['Noisy Image', 'Box Filter 5x5', 'Gaussian σ=1.5', 'Sharpened',
              'Laplacian', 'Sobel X', 'Sobel Y', 'Sobel Magnitude']
    
    for i, (img_show, title) in enumerate(zip(images, titles)):
        ax = axes[i//4, i%4]
        ax.imshow(img_show, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_linear_filters.png', dpi=150)
    plt.show()
    
    print("✅ Linear filters demo selesai!")
    print("   Output: output_linear_filters.png")

# ============================================================
# BAGIAN 3: NON-LINEAR FILTERING
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 3: NON-LINEAR FILTERING")
print("=" * 60)

def add_salt_pepper_noise(image, amount=0.05):
    """Tambahkan salt and pepper noise"""
    noisy = image.copy()
    
    # Salt
    num_salt = int(amount * image.size * 0.5)
    coords = [np.random.randint(0, i-1, num_salt) for i in image.shape]
    noisy[coords[0], coords[1]] = 255
    
    # Pepper
    num_pepper = int(amount * image.size * 0.5)
    coords = [np.random.randint(0, i-1, num_pepper) for i in image.shape]
    noisy[coords[0], coords[1]] = 0
    
    return noisy

def bilateral_filter_demo(image, d=9, sigma_color=75, sigma_space=75):
    """
    Bilateral filter - edge preserving smoothing
    
    Parameters:
        d: diameter of pixel neighborhood
        sigma_color: filter sigma in color space
        sigma_space: filter sigma in coordinate space
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def demo_nonlinear_filters():
    """Demonstrasi filter non-linear"""
    img = create_sample_image()
    
    # Salt and pepper noise
    sp_noisy = add_salt_pepper_noise(img, amount=0.05)
    
    # Gaussian noise
    gaussian_noisy = img.copy()
    noise = np.random.normal(0, 25, img.shape)
    gaussian_noisy = np.clip(gaussian_noisy.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    # Filter pada salt-pepper noise
    sp_gaussian = cv2.GaussianBlur(sp_noisy, (5, 5), 1.5)
    sp_median = cv2.medianBlur(sp_noisy, 5)
    
    # Filter pada gaussian noise - bilateral vs gaussian
    g_gaussian = cv2.GaussianBlur(gaussian_noisy, (9, 9), 2)
    g_bilateral = cv2.bilateralFilter(gaussian_noisy, 9, 75, 75)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original')
    
    axes[0, 1].imshow(sp_noisy, cmap='gray')
    axes[0, 1].set_title('Salt & Pepper Noise')
    
    axes[0, 2].imshow(sp_gaussian, cmap='gray')
    axes[0, 2].set_title('Gaussian (S&P)')
    
    axes[0, 3].imshow(sp_median, cmap='gray')
    axes[0, 3].set_title('Median Filter (S&P)')
    
    axes[1, 0].imshow(img, cmap='gray')
    axes[1, 0].set_title('Original')
    
    axes[1, 1].imshow(gaussian_noisy, cmap='gray')
    axes[1, 1].set_title('Gaussian Noise')
    
    axes[1, 2].imshow(g_gaussian, cmap='gray')
    axes[1, 2].set_title('Gaussian Blur')
    
    axes[1, 3].imshow(g_bilateral, cmap='gray')
    axes[1, 3].set_title('Bilateral Filter')
    
    for ax in axes.flat:
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_nonlinear_filters.png', dpi=150)
    plt.show()
    
    print("✅ Non-linear filters demo selesai!")
    print("   Median filter lebih efektif untuk salt-pepper noise")
    print("   Bilateral filter mempertahankan edge lebih baik")

# ============================================================
# BAGIAN 4: MORPHOLOGICAL OPERATIONS
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 4: MORPHOLOGICAL OPERATIONS")
print("=" * 60)

def demo_morphology():
    """Demonstrasi operasi morfologi"""
    # Buat gambar biner dengan noise
    img = np.zeros((200, 300), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)
    cv2.circle(img, (220, 100), 40, 255, -1)
    
    # Tambahkan noise
    noise = np.random.random(img.shape) < 0.02
    img[noise] = 255
    noise = np.random.random(img.shape) < 0.02
    img[noise] = 0
    
    # Structuring element
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    
    # Operasi morfologi
    eroded = cv2.erode(img, kernel, iterations=1)
    dilated = cv2.dilate(img, kernel, iterations=1)
    opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    images = [img, eroded, dilated, opened,
              closed, gradient, tophat, blackhat]
    titles = ['Original (Noisy)', 'Erosion', 'Dilation', 'Opening',
              'Closing', 'Gradient', 'Top Hat', 'Black Hat']
    
    for i, (img_show, title) in enumerate(zip(images, titles)):
        ax = axes[i//4, i%4]
        ax.imshow(img_show, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_morphology.png', dpi=150)
    plt.show()
    
    print("✅ Morphological operations demo selesai!")
    print("   Opening: menghilangkan noise putih kecil")
    print("   Closing: mengisi lubang hitam kecil")

# ============================================================
# BAGIAN 5: FOURIER TRANSFORM
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 5: FOURIER TRANSFORM")
print("=" * 60)

def demo_fourier_transform():
    """Demonstrasi transformasi Fourier"""
    img = create_sample_image()
    
    # DFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    
    # Magnitude spectrum (log scale untuk visualisasi)
    magnitude = 20 * np.log(np.abs(fshift) + 1)
    
    # Phase spectrum
    phase = np.angle(fshift)
    
    # Low-pass filter (Gaussian)
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    
    # Buat filter
    def create_gaussian_filter(shape, cutoff):
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2
        x = np.arange(cols) - ccol
        y = np.arange(rows) - crow
        xx, yy = np.meshgrid(x, y)
        d = np.sqrt(xx**2 + yy**2)
        h = np.exp(-(d**2) / (2 * cutoff**2))
        return h
    
    # Low-pass filter
    lpf = create_gaussian_filter(img.shape, 30)
    filtered_lpf = fshift * lpf
    img_lpf = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_lpf)))
    
    # High-pass filter
    hpf = 1 - lpf
    filtered_hpf = fshift * hpf
    img_hpf = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_hpf)))
    
    # Visualisasi
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original Image')
    
    axes[0, 1].imshow(magnitude, cmap='gray')
    axes[0, 1].set_title('Magnitude Spectrum')
    
    axes[0, 2].imshow(phase, cmap='gray')
    axes[0, 2].set_title('Phase Spectrum')
    
    axes[0, 3].imshow(lpf, cmap='gray')
    axes[0, 3].set_title('Low-pass Filter')
    
    axes[1, 0].imshow(img_lpf, cmap='gray')
    axes[1, 0].set_title('Low-pass Result')
    
    axes[1, 1].imshow(hpf, cmap='gray')
    axes[1, 1].set_title('High-pass Filter')
    
    axes[1, 2].imshow(img_hpf, cmap='gray')
    axes[1, 2].set_title('High-pass Result')
    
    # Rekonstruksi hanya dari magnitude vs phase
    # Magnitude saja (random phase)
    random_phase = np.exp(1j * np.random.uniform(-np.pi, np.pi, img.shape))
    mag_only = np.abs(fshift) * random_phase
    img_mag_only = np.abs(np.fft.ifft2(np.fft.ifftshift(mag_only)))
    
    # Phase saja (uniform magnitude)
    phase_only = np.exp(1j * phase)
    img_phase_only = np.abs(np.fft.ifft2(np.fft.ifftshift(phase_only)))
    
    axes[1, 3].imshow(img_phase_only, cmap='gray')
    axes[1, 3].set_title('Phase Only Reconstruction')
    
    for ax in axes.flat:
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_fourier.png', dpi=150)
    plt.show()
    
    print("✅ Fourier Transform demo selesai!")
    print("   Phase lebih penting dari magnitude untuk struktur gambar")

# ============================================================
# BAGIAN 6: IMAGE PYRAMIDS
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 6: IMAGE PYRAMIDS")
print("=" * 60)

def build_gaussian_pyramid(image, levels=4):
    """Buat Gaussian pyramid"""
    pyramid = [image]
    current = image
    
    for i in range(levels - 1):
        current = cv2.pyrDown(current)
        pyramid.append(current)
    
    return pyramid

def build_laplacian_pyramid(image, levels=4):
    """Buat Laplacian pyramid"""
    gaussian_pyr = build_gaussian_pyramid(image, levels)
    laplacian_pyr = []
    
    for i in range(levels - 1):
        # Upsample level berikutnya
        expanded = cv2.pyrUp(gaussian_pyr[i + 1], 
                           dstsize=(gaussian_pyr[i].shape[1], gaussian_pyr[i].shape[0]))
        # Laplacian = perbedaan
        laplacian = cv2.subtract(gaussian_pyr[i], expanded)
        laplacian_pyr.append(laplacian)
    
    # Level terakhir adalah gaussian
    laplacian_pyr.append(gaussian_pyr[-1])
    
    return laplacian_pyr

def reconstruct_from_laplacian(laplacian_pyr):
    """Rekonstruksi gambar dari Laplacian pyramid"""
    current = laplacian_pyr[-1]
    
    for i in range(len(laplacian_pyr) - 2, -1, -1):
        expanded = cv2.pyrUp(current, 
                           dstsize=(laplacian_pyr[i].shape[1], laplacian_pyr[i].shape[0]))
        current = cv2.add(expanded, laplacian_pyr[i])
    
    return current

def demo_pyramids():
    """Demonstrasi image pyramids"""
    img = create_sample_image()
    levels = 4
    
    # Build pyramids
    gaussian_pyr = build_gaussian_pyramid(img, levels)
    laplacian_pyr = build_laplacian_pyramid(img, levels)
    
    # Rekonstruksi
    reconstructed = reconstruct_from_laplacian(laplacian_pyr)
    
    # Visualisasi Gaussian Pyramid
    fig, axes = plt.subplots(2, levels, figsize=(16, 8))
    
    for i in range(levels):
        axes[0, i].imshow(gaussian_pyr[i], cmap='gray')
        axes[0, i].set_title(f'Gaussian Level {i}\n{gaussian_pyr[i].shape}')
        axes[0, i].axis('off')
        
        # Untuk laplacian, normalize untuk visualisasi
        lap_vis = laplacian_pyr[i].astype(np.float32)
        lap_vis = (lap_vis - lap_vis.min()) / (lap_vis.max() - lap_vis.min() + 1e-6)
        axes[1, i].imshow(lap_vis, cmap='gray')
        axes[1, i].set_title(f'Laplacian Level {i}\n{laplacian_pyr[i].shape}')
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_pyramids.png', dpi=150)
    plt.show()
    
    # Cek rekonstruksi
    error = np.mean(np.abs(img.astype(float) - reconstructed.astype(float)))
    print(f"✅ Image pyramids demo selesai!")
    print(f"   Reconstruction error: {error:.4f}")

# ============================================================
# BAGIAN 7: CANNY EDGE DETECTION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 7: CANNY EDGE DETECTION")
print("=" * 60)

def canny_edge_manual(image, low_thresh=50, high_thresh=150, sigma=1.0):
    """
    Implementasi manual Canny edge detection untuk pemahaman
    
    Langkah:
    1. Gaussian smoothing
    2. Gradient computation
    3. Non-maximum suppression
    4. Double thresholding
    5. Edge tracking by hysteresis
    """
    # 1. Gaussian smoothing
    smoothed = cv2.GaussianBlur(image, (5, 5), sigma)
    
    # 2. Gradient computation (Sobel)
    gx = cv2.Sobel(smoothed, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(smoothed, cv2.CV_64F, 0, 1, ksize=3)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx) * 180 / np.pi
    direction[direction < 0] += 180
    
    # 3. Non-maximum suppression
    h, w = image.shape
    nms = np.zeros_like(magnitude)
    
    for i in range(1, h-1):
        for j in range(1, w-1):
            angle = direction[i, j]
            
            # Determine neighbors to compare
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                neighbors = [magnitude[i, j-1], magnitude[i, j+1]]
            elif 22.5 <= angle < 67.5:
                neighbors = [magnitude[i-1, j+1], magnitude[i+1, j-1]]
            elif 67.5 <= angle < 112.5:
                neighbors = [magnitude[i-1, j], magnitude[i+1, j]]
            else:
                neighbors = [magnitude[i-1, j-1], magnitude[i+1, j+1]]
            
            if magnitude[i, j] >= max(neighbors):
                nms[i, j] = magnitude[i, j]
    
    # 4. Double thresholding
    strong = (nms >= high_thresh)
    weak = (nms >= low_thresh) & (nms < high_thresh)
    
    # 5. Edge tracking by hysteresis
    edges = np.zeros_like(image)
    edges[strong] = 255
    
    # Sederhana: iterasi untuk connect weak edges ke strong
    for _ in range(10):
        for i in range(1, h-1):
            for j in range(1, w-1):
                if weak[i, j]:
                    # Check if connected to strong edge
                    if edges[i-1:i+2, j-1:j+2].max() == 255:
                        edges[i, j] = 255
                        weak[i, j] = False
    
    return edges.astype(np.uint8)

def demo_canny():
    """Demonstrasi Canny edge detection"""
    img = create_sample_image()
    
    # Different threshold combinations
    edges_low = cv2.Canny(img, 30, 100)
    edges_mid = cv2.Canny(img, 50, 150)
    edges_high = cv2.Canny(img, 100, 200)
    
    # Different sigma (blur before Canny)
    blurred = cv2.GaussianBlur(img, (5, 5), 2.0)
    edges_smooth = cv2.Canny(blurred, 50, 150)
    
    # Our manual implementation
    edges_manual = canny_edge_manual(img, 50, 150, 1.0)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original')
    
    axes[0, 1].imshow(edges_low, cmap='gray')
    axes[0, 1].set_title('Canny (30, 100)')
    
    axes[0, 2].imshow(edges_mid, cmap='gray')
    axes[0, 2].set_title('Canny (50, 150)')
    
    axes[1, 0].imshow(edges_high, cmap='gray')
    axes[1, 0].set_title('Canny (100, 200)')
    
    axes[1, 1].imshow(edges_smooth, cmap='gray')
    axes[1, 1].set_title('Canny with More Blur')
    
    axes[1, 2].imshow(edges_manual, cmap='gray')
    axes[1, 2].set_title('Manual Implementation')
    
    for ax in axes.flat:
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_canny.png', dpi=150)
    plt.show()
    
    print("✅ Canny edge detection demo selesai!")
    print("   Low threshold: lebih banyak edge (termasuk noise)")
    print("   High threshold: hanya edge yang kuat")

# ============================================================
# BAGIAN 8: THRESHOLDING & SEGMENTATION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 8: THRESHOLDING & SEGMENTATION")
print("=" * 60)

def demo_thresholding():
    """Demonstrasi berbagai metode thresholding"""
    img = create_sample_image()
    
    # Global thresholding
    _, thresh_binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    _, thresh_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Adaptive thresholding
    thresh_adapt_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                              cv2.THRESH_BINARY, 11, 2)
    thresh_adapt_gauss = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, 11, 2)
    
    # Visualisasi
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original')
    
    axes[0, 1].hist(img.ravel(), 256, [0, 256])
    axes[0, 1].set_title('Histogram')
    axes[0, 1].axvline(x=127, color='r', linestyle='--', label='Manual T=127')
    axes[0, 1].legend()
    
    axes[0, 2].imshow(thresh_binary, cmap='gray')
    axes[0, 2].set_title('Binary (T=127)')
    
    axes[1, 0].imshow(thresh_otsu, cmap='gray')
    axes[1, 0].set_title("Otsu's Method")
    
    axes[1, 1].imshow(thresh_adapt_mean, cmap='gray')
    axes[1, 1].set_title('Adaptive Mean')
    
    axes[1, 2].imshow(thresh_adapt_gauss, cmap='gray')
    axes[1, 2].set_title('Adaptive Gaussian')
    
    for ax in axes.flat:
        if ax != axes[0, 1]:
            ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('output_thresholding.png', dpi=150)
    plt.show()
    
    print("✅ Thresholding demo selesai!")
    print("   Otsu: automatic threshold selection")
    print("   Adaptive: berbeda threshold untuk tiap region")

# ============================================================
# BAGIAN 9: CONNECTED COMPONENTS
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 9: CONNECTED COMPONENTS")
print("=" * 60)

def demo_connected_components():
    """Demonstrasi connected components labeling"""
    # Buat gambar dengan beberapa objek
    img = np.zeros((300, 400), dtype=np.uint8)
    
    # Beberapa shapes
    cv2.rectangle(img, (30, 30), (100, 100), 255, -1)
    cv2.circle(img, (200, 70), 40, 255, -1)
    cv2.ellipse(img, (320, 80), (50, 30), 0, 0, 360, 255, -1)
    cv2.rectangle(img, (50, 180), (120, 250), 255, -1)
    cv2.circle(img, (200, 220), 50, 255, -1)
    cv2.rectangle(img, (280, 180), (380, 280), 255, -1)
    
    # Connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
    
    # Warnai setiap komponen
    colored = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    colors = plt.cm.rainbow(np.linspace(0, 1, num_labels))[:, :3] * 255
    
    for i in range(1, num_labels):  # Skip background (label 0)
        colored[labels == i] = colors[i]
    
    # Visualisasi
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original Binary')
    axes[0].axis('off')
    
    axes[1].imshow(labels, cmap='tab10')
    axes[1].set_title(f'Labels ({num_labels-1} objects)')
    axes[1].axis('off')
    
    axes[2].imshow(colored.astype(np.uint8))
    axes[2].set_title('Colored Components')
    # Add centroids and stats
    for i in range(1, num_labels):
        cx, cy = centroids[i]
        area = stats[i, cv2.CC_STAT_AREA]
        axes[2].plot(cx, cy, 'w+', markersize=10, markeredgewidth=2)
        axes[2].text(cx, cy-10, f'A={area}', color='white', fontsize=8, ha='center')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_connected_components.png', dpi=150)
    plt.show()
    
    print("✅ Connected components demo selesai!")
    print(f"   Ditemukan {num_labels - 1} objek")

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PRAKTIKUM BAB 3: PEMROSESAN CITRA")
    print("=" * 60)
    
    # Run all demos
    print("\n🚀 Menjalankan semua demo...\n")
    
    demo_point_operators()
    demo_linear_filters()
    demo_nonlinear_filters()
    demo_morphology()
    demo_fourier_transform()
    demo_pyramids()
    demo_canny()
    demo_thresholding()
    demo_connected_components()
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM SELESAI!")
    print("=" * 60)
    print("\nFile output yang dihasilkan:")
    print("  - output_point_operators.png")
    print("  - output_linear_filters.png")
    print("  - output_nonlinear_filters.png")
    print("  - output_morphology.png")
    print("  - output_fourier.png")
    print("  - output_pyramids.png")
    print("  - output_canny.png")
    print("  - output_thresholding.png")
    print("  - output_connected_components.png")
    print("\n📝 Tugas: Lihat file tugas/tugas_bab_03.md")
