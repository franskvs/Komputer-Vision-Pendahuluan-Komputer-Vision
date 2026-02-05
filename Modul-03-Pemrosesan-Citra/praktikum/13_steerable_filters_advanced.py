#!/usr/bin/env python3
"""
===================================================================================
Bab 03: Pemrosesan Citra - 13. Filter Steerable dan Band-Pass Advanced
===================================================================================

Topik: Filter Steerable, Oriented Filters, dan Band-Pass Filtering Advanced
         (Bagian 3.2.3 dari Szeliski: Computer Vision)

Deskripsi:
Steerable filters adalah kelas filter yang powerful yang dapat digunakan untuk 
mendeteksi fitur dengan orientasi tertentu dan perform multi-scale analysis. 
Mereka dibangun dengan smooth image menggunakan Gaussian, lalu mengambil 
directional derivatives. Keuntungan utama adalah kita bisa "steer" filter 
ke orientasi apapun dengan hanya kombinasi linear dari beberapa basis filters.

Konsep Kunci:
1. Gaussian Derivatives - fondasi untuk steerable filters
2. First-order Steerable Filters - untuk edge detection oriented
3. Second-order Steerable Filters - untuk corner dan junction detection
4. Band-Pass Filters - untuk isolate frequency ranges tertentu
5. Oriented Energy Maps - untuk extract local orientation information
6. Laplacian of Gaussian (LoG) - popular choice untuk multi-scale detection

Aplikasi Praktis:
- Deteksi edge dengan orientasi spesifik
- Texture analysis dan synthesis
- Feature extraction untuk object recognition
- Medical image analysis
- Document image processing
- Line detection dalam images

Referensi:
- Freeman & Adelson (1991) - "Design and Use of Steerable Filters"
- Witkin (1983) - Scale-space filtering
- Marr & Hildreth (1980) - Laplacian of Gaussian
- Koethe (2003) - Boundary tensor untuk edge dan corner detection
===================================================================================
"""

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor komponen dari modul scipy.
from scipy import ndimage, signal
# Keterangan: Impor komponen dari modul scipy.ndimage.
from scipy.ndimage import convolve

# ==================== PARAMETER YANG DAPAT DIKONFIGURASI ====================

# Keterangan: Inisialisasi atau perbarui variabel SIGMA_VALUES.
SIGMA_VALUES = [1.0, 2.0, 3.0, 5.0]
# Keterangan: Inisialisasi atau perbarui variabel DEFAULT_SIGMA.
DEFAULT_SIGMA = 2.0
# Keterangan: Inisialisasi atau perbarui variabel EDGE_THRESHOLD.
EDGE_THRESHOLD = 0.1
# Keterangan: Inisialisasi atau perbarui variabel CORNER_THRESHOLD.
CORNER_THRESHOLD = 0.15
# Keterangan: Inisialisasi atau perbarui variabel KERNEL_SIZE.
KERNEL_SIZE = (7, 7)
# Keterangan: Inisialisasi atau perbarui variabel NUM_ORIENTATIONS.
NUM_ORIENTATIONS = 16
# Keterangan: Inisialisasi atau perbarui variabel MAX_ANGLE.
MAX_ANGLE = 360

# ======================= GAUSSIAN DAN DERIVATIVES ===========================

# Keterangan: Definisikan fungsi gaussian_kernel.
def gaussian_kernel(size, sigma):
    """Membuat 2D Gaussian kernel"""
    x = cv2.getGaussianKernel(size, sigma)
    kernel = x @ x.T
    return kernel / kernel.sum()


def gaussian_derivative_x(size, sigma):
    """Gaussian derivative dalam arah X: partial G / partial x"""
    # Keterangan: Buat range angka berjarak linier.
    x = np.linspace(-size//2, size//2, size)
    # Keterangan: Inisialisasi atau perbarui variabel derivative.
    derivative = -x / (sigma**2) * np.exp(-x**2 / (2*sigma**2))
    # Keterangan: Inisialisasi atau perbarui variabel derivative.
    derivative = derivative / np.sum(np.abs(derivative))
    # Keterangan: Inisialisasi atau perbarui variabel kernel.
    kernel = np.exp(-x**2 / (2*sigma**2))
    # Keterangan: Inisialisasi atau perbarui variabel gx.
    gx = np.outer(derivative, kernel)
    # Keterangan: Kembalikan hasil dari fungsi.
    return gx


# Keterangan: Definisikan fungsi gaussian_derivative_y.
def gaussian_derivative_y(size, sigma):
    """Gaussian derivative dalam arah Y: partial G / partial y"""
    return gaussian_derivative_x(size, sigma).T


def gaussian_derivative_xx(size, sigma):
    """Second-order Gaussian derivative: partial^2 G / partial x^2"""
    # Keterangan: Buat range angka berjarak linier.
    x = np.linspace(-size//2, size//2, size)
    # Keterangan: Inisialisasi atau perbarui variabel second_deriv.
    second_deriv = (x**2 - sigma**2) / (sigma**4) * np.exp(-x**2 / (2*sigma**2))
    # Keterangan: Inisialisasi atau perbarui variabel second_deriv.
    second_deriv = second_deriv / np.max(np.abs(second_deriv))
    # Keterangan: Inisialisasi atau perbarui variabel kernel.
    kernel = np.exp(-x**2 / (2*sigma**2))
    # Keterangan: Inisialisasi atau perbarui variabel gxx.
    gxx = np.outer(second_deriv, kernel)
    # Keterangan: Kembalikan hasil dari fungsi.
    return gxx


# Keterangan: Definisikan fungsi gaussian_derivative_yy.
def gaussian_derivative_yy(size, sigma):
    """Second-order Gaussian derivative: partial^2 G / partial y^2"""
    return gaussian_derivative_xx(size, sigma).T


def gaussian_derivative_xy(size, sigma):
    """Mixed second-order derivative: partial^2 G / partial x partial y"""
    # Keterangan: Buat range angka berjarak linier.
    x = np.linspace(-size//2, size//2, size)
    # Keterangan: Inisialisasi atau perbarui variabel deriv_x.
    deriv_x = -x / (sigma**2) * np.exp(-x**2 / (2*sigma**2))
    # Keterangan: Inisialisasi atau perbarui variabel deriv_y.
    deriv_y = -x / (sigma**2) * np.exp(-x**2 / (2*sigma**2))
    # Keterangan: Inisialisasi atau perbarui variabel gxy.
    gxy = np.outer(deriv_x, deriv_y)
    # Keterangan: Inisialisasi atau perbarui variabel gxy.
    gxy = gxy / np.max(np.abs(gxy))
    # Keterangan: Kembalikan hasil dari fungsi.
    return gxy


# ===================== FIRST-ORDER STEERABLE FILTERS =======================

# Keterangan: Definisikan fungsi first_order_directional_derivative.
def first_order_directional_derivative(img, angle_degrees, sigma=DEFAULT_SIGMA, 
                                       # Keterangan: Inisialisasi atau perbarui variabel kernel_size.
                                       kernel_size=KERNEL_SIZE[0]):
    """
    Compute first-order directional derivative pada angle tertentu.
    Output: grad_u f = u*Gx + v*Gy
    dimana u = (cos theta, sin theta)
    """
    # Keterangan: Inisialisasi atau perbarui variabel angle_rad.
    angle_rad = np.radians(angle_degrees)
    # Keterangan: Inisialisasi atau perbarui variabel u.
    u = np.cos(angle_rad)
    # Keterangan: Inisialisasi atau perbarui variabel v.
    v = np.sin(angle_rad)
    
    # Keterangan: Inisialisasi atau perbarui variabel gx.
    gx = gaussian_derivative_x(kernel_size, sigma)
    # Keterangan: Inisialisasi atau perbarui variabel gy.
    gy = gaussian_derivative_y(kernel_size, sigma)
    
    # Keterangan: Inisialisasi atau perbarui variabel steerable_kernel.
    steerable_kernel = u * gx + v * gy
    # Keterangan: Inisialisasi atau perbarui variabel output.
    output = convolve(img.astype(float), steerable_kernel, mode='constant')
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return output


# Keterangan: Definisikan fungsi compute_directional_edges.
def compute_directional_edges(img, sigma=DEFAULT_SIGMA):
    """Compute edges dalam multiple orientations menggunakan steerable filters."""
    angles = np.linspace(0, 360, NUM_ORIENTATIONS, endpoint=False)
    responses = []
    
    for angle in angles:
        response = first_order_directional_derivative(img, angle, sigma)
        responses.append(np.abs(response))
    
    responses = np.array(responses)
    magnitude = np.max(responses, axis=0)
    dominant_angle = angles[np.argmax(responses, axis=0)]
    
    return magnitude, dominant_angle, responses


# ================== SECOND-ORDER STEERABLE FILTERS =========================

def second_order_directional_derivative(img, angle_degrees, sigma=DEFAULT_SIGMA,
                                       kernel_size=KERNEL_SIZE[0]):
    """
    # Keterangan: Jalankan perintah berikut.
    Second-order directional derivative: partial^2 f / partial u^2
    # Keterangan: Inisialisasi atau perbarui variabel Formula: partial^2 f / partial u^2.
    Formula: partial^2 f / partial u^2 = u^2*Gxx + 2uv*Gxy + v^2*Gyy
    """
    angle_rad = np.radians(angle_degrees)
    u = np.cos(angle_rad)
    v = np.sin(angle_rad)
    
    gxx = gaussian_derivative_xx(kernel_size, sigma)
    gxy = gaussian_derivative_xy(kernel_size, sigma)
    gyy = gaussian_derivative_yy(kernel_size, sigma)
    
    kernel = u**2 * gxx + 2*u*v * gxy + v**2 * gyy
    output = convolve(img.astype(float), kernel, mode='constant')
    
    return output


def compute_corner_edges(img, sigma=DEFAULT_SIGMA):
    """Detect corners menggunakan second-order steerable filters."""
    # Keterangan: Buat range angka berjarak linier.
    angles = np.linspace(0, 180, NUM_ORIENTATIONS//2, endpoint=False)
    # Keterangan: Inisialisasi atau perbarui variabel responses.
    responses = []
    
    # Keterangan: Mulai loop dengan for angle in angles.
    for angle in angles:
        # Keterangan: Inisialisasi atau perbarui variabel response.
        response = second_order_directional_derivative(img, angle, sigma)
        # Keterangan: Jalankan perintah berikut.
        responses.append(np.abs(response)**2)
    
    # Keterangan: Inisialisasi atau perbarui variabel responses.
    responses = np.array(responses)
    # Keterangan: Inisialisasi atau perbarui variabel corner_strength.
    corner_strength = np.sum(responses, axis=0)
    # Keterangan: Inisialisasi atau perbarui variabel dominant_angle.
    dominant_angle = angles[np.argmax(responses, axis=0)]
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return corner_strength, dominant_angle, responses


# ====================== LAPLACIAN OF GAUSSIAN (LoG) =========================

# Keterangan: Definisikan fungsi laplacian_of_gaussian.
def laplacian_of_gaussian(img, sigma=DEFAULT_SIGMA, kernel_size=KERNEL_SIZE[0]):
    """Laplacian of Gaussian: Laplacian(G * f)"""
    smoothed = ndimage.gaussian_filter(img.astype(float), sigma=sigma)
    laplacian = ndimage.laplace(smoothed)
    return laplacian


def difference_of_gaussians(img, sigma1=1.0, sigma2=2.0):
    """Difference of Gaussians: G(sigma1) - G(sigma2)"""
    # Keterangan: Inisialisasi atau perbarui variabel gaussian1.
    gaussian1 = ndimage.gaussian_filter(img.astype(float), sigma=sigma1)
    # Keterangan: Inisialisasi atau perbarui variabel gaussian2.
    gaussian2 = ndimage.gaussian_filter(img.astype(float), sigma=sigma2)
    # Keterangan: Inisialisasi atau perbarui variabel dog.
    dog = gaussian1 - gaussian2
    # Keterangan: Kembalikan hasil dari fungsi.
    return dog


# ====================== BAND-PASS FILTERS ===================================

# Keterangan: Definisikan fungsi bandpass_filter_frequency.
def bandpass_filter_frequency(img, min_freq=0.1, max_freq=0.5):
    """Band-pass filter dalam frequency domain."""
    f_transform = np.fft.fft2(img.astype(float))
    f_shift = np.fft.fftshift(f_transform)
    
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    
    u = np.arange(rows) - crow
    v = np.arange(cols) - ccol
    U, V = np.meshgrid(u, v, indexing='ij')
    
    distance = np.sqrt(U**2 + V**2)
    max_distance = np.sqrt(crow**2 + ccol**2)
    distance_normalized = distance / max_distance
    
    mask = np.logical_and(distance_normalized >= min_freq, 
                         distance_normalized <= max_freq).astype(float)
    
    f_filtered = f_shift * mask
    f_ishift = np.fft.ifftshift(f_filtered)
    output = np.fft.ifft2(f_ishift)
    output = np.abs(output)
    
    return output


# ==================== DEMONSTRASI PRAKTIKUM ====================

def demo_1_steerable_filters_basics():
    """Demo 1: Basics dari first-order steerable filters."""
    # Keterangan: Jalankan perintah berikut.
    print("\nDemo 1: First-Order Steerable Filters Basics")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Baca gambar dari file ke array.
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    # Keterangan: Cek kondisi img is None.
    if img is None:
        # Keterangan: Inisialisasi atau perbarui variabel img.
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    # Keterangan: Inisialisasi beberapa variabel (magnitude, dominant_angle, responses).
    magnitude, dominant_angle, responses = compute_directional_edges(img, SIGMA_VALUES[1])
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    # Keterangan: Inisialisasi beberapa variabel (fig.suptitle('First-Order Steerable Filters', fontsize).
    fig.suptitle('First-Order Steerable Filters', fontsize=14, fontweight='bold')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(img, cmap).
    axes[0, 0].imshow(img, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title('Original Image')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(magnitude, cmap).
    axes[0, 1].imshow(magnitude, cmap='hot')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].set_title('Edge Magnitude')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(dominant_angle / 360, cmap).
    axes[0, 2].imshow(dominant_angle / 360, cmap='hsv')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title('Dominant Orientation')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Inisialisasi atau perbarui variabel angles_to_show.
    angles_to_show = [0, 45, 90, 135]
    # Keterangan: Mulai loop dengan for idx, angle in enumerate(angles_to_show).
    for idx, angle in enumerate(angles_to_show):
        # Keterangan: Inisialisasi atau perbarui variabel ax.
        ax = axes[1, idx] if idx < 3 else None
        # Keterangan: Cek kondisi ax is not None.
        if ax is not None:
            # Keterangan: Inisialisasi atau perbarui variabel angle_idx.
            angle_idx = (angle * len(responses)) // 360
            # Keterangan: Inisialisasi beberapa variabel (ax.imshow(np.abs(responses[angle_idx]), cmap).
            ax.imshow(np.abs(responses[angle_idx]), cmap='hot')
            # Keterangan: Jalankan perintah berikut.
            ax.set_title(f'Response at {angle}°')
            # Keterangan: Jalankan perintah berikut.
            ax.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('13_demo1_steerable_filters_basics.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 13_demo1_steerable_filters_basics.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_2_second_order_steerable_filters.
def demo_2_second_order_steerable_filters():
    """Demo 2: Second-order steerable filters untuk corner detection."""
    print("\nDemo 2: Second-Order Steerable Filters (Corner Detection)")
    print("="*70)
    
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.ones((256, 256), dtype=np.uint8) * 255
        img[100:200, 100:200] = 0
    
    corner_strength, corner_orientation, responses = compute_corner_edges(img, SIGMA_VALUES[1])
    corner_strength = (corner_strength - corner_strength.min()) / (corner_strength.max() - corner_strength.min() + 1e-8)
    corner_mask = corner_strength > CORNER_THRESHOLD
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Second-Order Steerable Filters - Corner Detection', fontsize=14, fontweight='bold')
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(corner_strength, cmap='hot')
    axes[0, 1].set_title('Corner Strength')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(img, cmap='gray')
    corner_points = np.where(corner_mask)
    if len(corner_points[0]) > 0:
        axes[0, 2].scatter(corner_points[1], corner_points[0], c='red', s=20)
    axes[0, 2].set_title(f'Detected Corners')
    axes[0, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('13_demo2_second_order_steerable.png', dpi=150, bbox_inches='tight')
    print("Saved: 13_demo2_second_order_steerable.png")
    plt.close()


def demo_3_laplacian_of_gaussian():
    """Demo 3: Laplacian of Gaussian (LoG) untuk multi-scale analysis."""
    # Keterangan: Jalankan perintah berikut.
    print("\nDemo 3: Laplacian of Gaussian (LoG) - Multi-Scale Analysis")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Baca gambar dari file ke array.
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    # Keterangan: Cek kondisi img is None.
    if img is None:
        # Keterangan: Inisialisasi atau perbarui variabel img.
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, len(SIGMA_VALUES), figsize=(16, 8))
    # Keterangan: Inisialisasi beberapa variabel (fig.suptitle('Laplacian of Gaussian at Multiple Scales', fontsize).
    fig.suptitle('Laplacian of Gaussian at Multiple Scales', fontsize=14, fontweight='bold')
    
    # Keterangan: Mulai loop dengan for idx, sigma in enumerate(SIGMA_VALUES).
    for idx, sigma in enumerate(SIGMA_VALUES):
        # Keterangan: Inisialisasi atau perbarui variabel log_img.
        log_img = laplacian_of_gaussian(img, sigma=sigma)
        # Keterangan: Inisialisasi atau perbarui variabel log_img.
        log_img = (log_img - log_img.min()) / (log_img.max() - log_img.min() + 1e-8)
        
        # Keterangan: Inisialisasi beberapa variabel (axes[0, idx].imshow(log_img, cmap).
        axes[0, idx].imshow(log_img, cmap='RdBu_r')
        # Keterangan: Inisialisasi beberapa variabel (axes[0, idx].set_title(f'LoG (sigma).
        axes[0, idx].set_title(f'LoG (sigma={sigma})')
        # Keterangan: Jalankan perintah berikut.
        axes[0, idx].axis('off')
        
        # Keterangan: Inisialisasi atau perbarui variabel zero_crossings.
        zero_crossings = np.abs(np.gradient(log_img)[0]) > 0.1
        # Keterangan: Inisialisasi beberapa variabel (axes[1, idx].imshow(zero_crossings, cmap).
        axes[1, idx].imshow(zero_crossings, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[1, idx].set_title(f'Zero-crossings')
        # Keterangan: Jalankan perintah berikut.
        axes[1, idx].axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('13_demo3_laplacian_of_gaussian.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 13_demo3_laplacian_of_gaussian.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_4_difference_of_gaussians.
def demo_4_difference_of_gaussians():
    """Demo 4: Difference of Gaussians (DoG) - efficient approximation dari LoG."""
    print("\nDemo 4: Difference of Gaussians (DoG)")
    print("="*70)
    
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    sigma_pairs = [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (5.0, 10.0)]
    
    fig, axes = plt.subplots(2, len(sigma_pairs), figsize=(16, 8))
    fig.suptitle('Difference of Gaussians (DoG)', fontsize=14, fontweight='bold')
    
    for idx, (sigma1, sigma2) in enumerate(sigma_pairs):
        dog_img = difference_of_gaussians(img, sigma1, sigma2)
        dog_img = (dog_img - dog_img.min()) / (dog_img.max() - dog_img.min() + 1e-8)
        
        axes[0, idx].imshow(dog_img, cmap='RdBu_r')
        axes[0, idx].set_title(f'DoG (s1={sigma1}, s2={sigma2})')
        axes[0, idx].axis('off')
        
        blob_mask = np.abs(dog_img) > 0.2
        axes[1, idx].imshow(blob_mask, cmap='gray')
        axes[1, idx].set_title('Blob Regions')
        axes[1, idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('13_demo4_difference_of_gaussians.png', dpi=150, bbox_inches='tight')
    print("Saved: 13_demo4_difference_of_gaussians.png")
    plt.close()


def demo_5_bandpass_filtering():
    """Demo 5: Band-pass filtering dalam frequency domain."""
    # Keterangan: Jalankan perintah berikut.
    print("\nDemo 5: Band-Pass Filtering in Frequency Domain")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Baca gambar dari file ke array.
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    # Keterangan: Cek kondisi img is None.
    if img is None:
        # Keterangan: Inisialisasi atau perbarui variabel img.
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    # Keterangan: Inisialisasi atau perbarui variabel bands.
    bands = [
        # Keterangan: Jalankan perintah berikut.
        (0.0, 0.1, 'Low-Frequency'),
        # Keterangan: Jalankan perintah berikut.
        (0.1, 0.3, 'Low-Mid'),
        # Keterangan: Jalankan perintah berikut.
        (0.3, 0.5, 'Mid-Frequency'),
        # Keterangan: Jalankan perintah berikut.
        (0.5, 0.8, 'High-Frequency')
    # Keterangan: Jalankan perintah berikut.
    ]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, len(bands), figsize=(16, 8))
    # Keterangan: Inisialisasi beberapa variabel (fig.suptitle('Band-Pass Filtering', fontsize).
    fig.suptitle('Band-Pass Filtering', fontsize=14, fontweight='bold')
    
    # Keterangan: Mulai loop dengan for idx, (min_freq, max_freq, label) in enumerate(bands).
    for idx, (min_freq, max_freq, label) in enumerate(bands):
        # Keterangan: Inisialisasi atau perbarui variabel filtered.
        filtered = bandpass_filter_frequency(img, min_freq, max_freq)
        # Keterangan: Inisialisasi atau perbarui variabel filtered.
        filtered = (filtered - filtered.min()) / (filtered.max() - filtered.min() + 1e-8)
        
        # Keterangan: Inisialisasi atau perbarui variabel f_transform.
        f_transform = np.fft.fft2(img.astype(float))
        # Keterangan: Inisialisasi atau perbarui variabel spectrum.
        spectrum = np.abs(np.fft.fftshift(f_transform))
        # Keterangan: Inisialisasi atau perbarui variabel spectrum_log.
        spectrum_log = np.log1p(spectrum)
        
        # Keterangan: Inisialisasi beberapa variabel (axes[0, idx].imshow(spectrum_log, cmap).
        axes[0, idx].imshow(spectrum_log, cmap='hot')
        # Keterangan: Jalankan perintah berikut.
        axes[0, idx].set_title(f'{label} Band')
        # Keterangan: Jalankan perintah berikut.
        axes[0, idx].axis('off')
        
        # Keterangan: Inisialisasi beberapa variabel (axes[1, idx].imshow(filtered, cmap).
        axes[1, idx].imshow(filtered, cmap='gray')
        # Keterangan: Jalankan perintah berikut.
        axes[1, idx].set_title('Filtered Image')
        # Keterangan: Jalankan perintah berikut.
        axes[1, idx].axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('13_demo5_bandpass_filtering.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 13_demo5_bandpass_filtering.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_6_oriented_texture_analysis.
def demo_6_oriented_texture_analysis():
    """Demo 6: Oriented texture analysis menggunakan steerable filters."""
    print("\nDemo 6: Oriented Texture Analysis")
    print("="*70)
    
    img = np.ones((256, 256), dtype=np.uint8) * 128
    
    y, x = np.meshgrid(np.arange(256), np.arange(256))
    
    img[0:85, :] += 50 * np.sin(0.1 * x[0:85, :])
    
    pattern_45 = np.sin(0.1 * (x + y)[85:170, :])
    img[85:170, :] += 50 * (pattern_45 - pattern_45.min()) / (pattern_45.max() - pattern_45.min() + 1e-8)
    
    img[170:, :] += 50 * np.sin(0.1 * y[170:, :])
    
    img = np.clip(img, 0, 255).astype(np.uint8)
    
    magnitude, dominant_angle, responses = compute_directional_edges(img, sigma=1.0)
    magnitude = (magnitude - magnitude.min()) / (magnitude.max() - magnitude.min() + 1e-8)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Oriented Texture Analysis', fontsize=14, fontweight='bold')
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Synthetic Oriented Texture')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(magnitude, cmap='hot')
    axes[0, 1].set_title('Edge/Texture Magnitude')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(dominant_angle, cmap='hsv')
    axes[0, 2].set_title('Dominant Orientation')
    axes[0, 2].axis('off')
    
    axes[1, 0].hist(dominant_angle.flatten(), bins=36, range=(0, 360))
    axes[1, 0].set_xlabel('Orientation (degrees)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Orientation Distribution')
    axes[1, 0].grid(True, alpha=0.3)
    
    for dir_idx, direction in enumerate([0, 45, 90]):
        dir_angle_idx = (direction * len(responses)) // 360
        ax = axes[1, dir_idx + 1]
        response = np.abs(responses[dir_angle_idx])
        response = (response - response.min()) / (response.max() - response.min() + 1e-8)
        ax.imshow(response, cmap='hot')
        ax.set_title(f'Response @ {direction}°')
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('13_demo6_oriented_texture_analysis.png', dpi=150, bbox_inches='tight')
    print("Saved: 13_demo6_oriented_texture_analysis.png")
    plt.close()


# ===================== MAIN PROGRAM =======================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("STEERABLE FILTERS DAN BAND-PASS FILTERING ADVANCED")
    print("Praktikum Bab 03: Pemrosesan Citra")
    print("="*70)
    
    print("\nKeterangan:")
    print("- Steerable filters dapat diatur ke orientasi apapun")
    print("- Berguna untuk mendeteksi fitur dengan orientasi tertentu")
    print("- First-order: untuk edge detection dengan orientasi")
    print("- Second-order: untuk corner dan junction detection")
    print("- LoG/DoG: untuk multi-scale blob detection")
    print("- Band-pass: untuk isolasi frequency ranges tertentu")
    
    demo_1_steerable_filters_basics()
    demo_2_second_order_steerable_filters()
    demo_3_laplacian_of_gaussian()
    demo_4_difference_of_gaussians()
    demo_5_bandpass_filtering()
    demo_6_oriented_texture_analysis()
    
    print("\n" + "="*70)
    print("SEMUA DEMONSTRASI SELESAI")
    print("="*70)
    print("\nHasil disimpan sebagai gambar PNG di folder praktikum.")
    print("\nLanjutan eksplorasi:")
    print("1. Coba gunakan steerable filters untuk extract line features")
    print("2. Implementasikan SIFT feature detector")
    print("3. Gunakan untuk texture classification tasks")
    print("4. Explore aplikasi dalam medical image analysis")
    print("="*70 + "\n")
