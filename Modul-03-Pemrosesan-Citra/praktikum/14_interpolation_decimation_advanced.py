#!/usr/bin/env python3
"""
===================================================================================
Bab 03: Pemrosesan Citra - 14. Interpolasi, Decimasi, dan MIP-Mapping Advanced
===================================================================================

Topik: Advanced Interpolation Methods, Decimation, dan Image Pyramids
       (Bagian 3.5.1-3.5.2 dari Szeliski: Computer Vision)

Deskripsi:
Interpolasi dan decimasi adalah operasi fundamental dalam image processing.
Interpolasi mengubah ukuran image dengan meningkatkan sample rate (upsampling),
sedangkan decimasi mengurangi sample rate (downsampling). MIP-mapping adalah teknik
untuk mengoptimalkan texture mapping dalam 3D graphics dengan pre-computing
filtered versions dari image pada berbagai resolutions.

Konsep Kunci:
1. Interpolation methods: nearest, bilinear, bicubic, Lanczos
2. Cubic kernels dan parameter tuning
3. Anti-aliasing dan prefiltering
4. Decimation dengan binomial/Gaussian filters
5. MIP-maps (Multum In Parvo)
6. Trilinear MIP-map sampling
7. Zoom sequences dan LOD (Level of Detail)

Aplikasi Praktis:
- Image resizing dan scaling
- Texture mapping dalam 3D graphics
- Progressive image loading
- Video frame interpolation
- Remote sensing image processing
- Medical image reconstruction

Referensi:
- Burt & Adelson (1983) - Laplacian pyramids
- Smith (1981) - Fast filter using FFT
- Lanczos (1950s) - Windowed sinc filters
- Williams (1983) - Pyramidal Parametrics
===================================================================================
"""

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor komponen dari modul scipy.
from scipy import ndimage, interpolate
# Keterangan: Impor komponen dari modul scipy.ndimage.
from scipy.ndimage import convolve

# ==================== PARAMETER ====================

# Keterangan: Inisialisasi atau perbarui variabel DEFAULT_SIGMA.
DEFAULT_SIGMA = 1.0
# Keterangan: Inisialisasi atau perbarui variabel KERNEL_SIZES.
KERNEL_SIZES = [3, 5, 7, 11]

# ===================== INTERPOLATION METHODS =======================

# Keterangan: Definisikan fungsi nearest_neighbor_interpolate.
def nearest_neighbor_interpolate(img, scale):
    """Nearest neighbor: simplest method, fast tapi jagged hasil"""
    h, w = img.shape[:2]
    new_h, new_w = int(h * scale), int(w * scale)
    output = np.zeros((new_h, new_w) + img.shape[2:], dtype=img.dtype)
    
    for i in range(new_h):
        for j in range(new_w):
            src_i = min(int(i / scale), h - 1)
            src_j = min(int(j / scale), w - 1)
            output[i, j] = img[src_i, src_j]
    
    return output


def bilinear_interpolation(img, scale):
    """
    # Keterangan: Jalankan perintah berikut.
    Bilinear interpolation: 4-pixel kernel
    # Keterangan: Jalankan perintah berikut.
    f(x,y) ≈ f(0,0)(1-u)(1-v) + f(1,0)u(1-v) + f(0,1)(1-u)v + f(1,1)uv
    """
    h, w = img.shape[:2]
    new_h, new_w = int(h * scale), int(w * scale)
    output = np.zeros((new_h, new_w) + img.shape[2:], dtype=np.float32)
    
    for i in range(new_h):
        for j in range(new_w):
            src_x = j / scale
            src_y = i / scale
            
            x0, y0 = int(src_x), int(src_y)
            x1 = min(x0 + 1, w - 1)
            y1 = min(y0 + 1, h - 1)
            
            u = src_x - x0
            v = src_y - y0
            
            output[i, j] = (img[y0, x0] * (1-u) * (1-v) +
                          img[y0, x1] * u * (1-v) +
                          img[y1, x0] * (1-u) * v +
                          img[y1, x1] * u * v)
    
    return np.clip(output, 0, 255).astype(img.dtype)


def cubic_kernel(x, a=-0.5):
    """
    # Keterangan: Jalankan perintah berikut.
    Cubic spline kernel untuk bicubic interpolation
    # Keterangan: Mulai blok kode baru.
    Parameter a:
    # Keterangan: Inisialisasi atau perbarui variabel - a.
    - a = -1: Sharp (Catmull-Rom)
    # Keterangan: Inisialisasi atau perbarui variabel - a.
    - a = -0.5: Balanced (default)
    # Keterangan: Inisialisasi atau perbarui variabel - a.
    - a = 0: Linear
    """
    x = np.abs(x)
    
    if x < 1:
        return (a + 2) * x**3 - (a + 3) * x**2 + 1
    elif x < 2:
        return a * x**3 - 5*a * x**2 + 8*a * x - 4*a
    else:
        return 0


def bicubic_interpolation(img, scale, a=-0.5):
    """
    # Keterangan: Jalankan perintah berikut.
    Bicubic interpolation: 16-pixel kernel
    # Keterangan: Jalankan perintah berikut.
    Lebih smooth dibanding bilinear
    """
    h, w = img.shape[:2]
    new_h, new_w = int(h * scale), int(w * scale)
    output = np.zeros((new_h, new_w) + img.shape[2:], dtype=np.float32)
    
    for i in range(new_h):
        for j in range(new_w):
            src_x = j / scale
            src_y = i / scale
            
            x0 = int(src_x)
            y0 = int(src_y)
            
            dx = src_x - x0
            dy = src_y - y0
            
            result = 0.0
            for jj in range(-1, 3):
                for ii in range(-1, 3):
                    x = min(max(x0 + jj, 0), w - 1)
                    y = min(max(y0 + ii, 0), h - 1)
                    
                    kernel_x = cubic_kernel(jj - dx, a)
                    kernel_y = cubic_kernel(ii - dy, a)
                    
                    result += img[y, x] * kernel_x * kernel_y
            
            output[i, j] = result
    
    return np.clip(output, 0, 255).astype(img.dtype)


def windowed_sinc_kernel(x, window_size=4):
    """Sinc kernel dengan Hann window"""
    # Keterangan: Cek kondisi x == 0.
    if x == 0:
        # Keterangan: Kembalikan hasil dari fungsi.
        return 1.0
    
    # Keterangan: Inisialisasi atau perbarui variabel sinc.
    sinc = np.sin(np.pi * x) / (np.pi * x)
    
    # Keterangan: Cek kondisi abs(x) >= window_size.
    if abs(x) >= window_size:
        # Keterangan: Kembalikan hasil dari fungsi.
        return 0.0
    
    # Keterangan: Inisialisasi atau perbarui variabel hann.
    hann = 0.5 * (1 + np.cos(np.pi * x / window_size))
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return sinc * hann


# Keterangan: Definisikan fungsi lanczos_kernel.
def lanczos_kernel(x, a=3):
    """Lanczos kernel: sinc(t)*sinc(t/a) untuk |t| < a"""
    x = np.abs(x)
    
    if x < a:
        if x == 0:
            return 1.0
        sinc_x = np.sin(np.pi * x) / (np.pi * x)
        sinc_ax = np.sin(np.pi * x / a) / (np.pi * x / a)
        return sinc_x * sinc_ax
    
    return 0.0


def lanczos_interpolation(img, scale, a=3):
    """Lanczos interpolation: high-quality resampling"""
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = img.shape[:2]
    # Keterangan: Inisialisasi beberapa variabel (new_h, new_w).
    new_h, new_w = int(h * scale), int(w * scale)
    # Keterangan: Inisialisasi array bernilai nol.
    output = np.zeros((new_h, new_w) + img.shape[2:], dtype=np.float32)
    
    # Keterangan: Mulai loop dengan for i in range(new_h).
    for i in range(new_h):
        # Keterangan: Mulai loop dengan for j in range(new_w).
        for j in range(new_w):
            # Keterangan: Inisialisasi atau perbarui variabel src_x.
            src_x = j / scale
            # Keterangan: Inisialisasi atau perbarui variabel src_y.
            src_y = i / scale
            
            # Keterangan: Inisialisasi atau perbarui variabel x0.
            x0 = int(src_x)
            # Keterangan: Inisialisasi atau perbarui variabel y0.
            y0 = int(src_y)
            
            # Keterangan: Inisialisasi atau perbarui variabel dx.
            dx = src_x - x0
            # Keterangan: Inisialisasi atau perbarui variabel dy.
            dy = src_y - y0
            
            # Keterangan: Inisialisasi atau perbarui variabel result.
            result = 0.0
            # Keterangan: Inisialisasi atau perbarui variabel kernel_sum.
            kernel_sum = 0.0
            
            # Keterangan: Mulai loop dengan for yy in range(-a, a + 1).
            for yy in range(-a, a + 1):
                # Keterangan: Mulai loop dengan for xx in range(-a, a + 1).
                for xx in range(-a, a + 1):
                    # Keterangan: Inisialisasi atau perbarui variabel x.
                    x = min(max(x0 + xx, 0), w - 1)
                    # Keterangan: Inisialisasi atau perbarui variabel y.
                    y = min(max(y0 + yy, 0), h - 1)
                    
                    # Keterangan: Inisialisasi atau perbarui variabel k_x.
                    k_x = lanczos_kernel(xx - dx, a)
                    # Keterangan: Inisialisasi atau perbarui variabel k_y.
                    k_y = lanczos_kernel(yy - dy, a)
                    # Keterangan: Inisialisasi atau perbarui variabel k.
                    k = k_x * k_y
                    
                    # Keterangan: Inisialisasi atau perbarui variabel result +.
                    result += img[y, x] * k
                    # Keterangan: Inisialisasi atau perbarui variabel kernel_sum +.
                    kernel_sum += k
            
            # Keterangan: Cek kondisi kernel_sum > 0.
            if kernel_sum > 0:
                # Keterangan: Inisialisasi atau perbarui variabel result /.
                result /= kernel_sum
            
            # Keterangan: Inisialisasi beberapa variabel (output[i, j]).
            output[i, j] = result
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return np.clip(output, 0, 255).astype(img.dtype)


# ===================== DECIMATION =======================

# Keterangan: Definisikan fungsi decimate_with_prefilter.
def decimate_with_prefilter(img, factor=2):
    """Decimation dengan Gaussian prefilter untuk anti-aliasing"""
    sigma = factor / 2.0
    
    blurred = ndimage.gaussian_filter(img.astype(float), sigma=sigma)
    decimated = blurred[::factor, ::factor]
    
    return decimated.astype(img.dtype)


def decimate_with_binomial_filter(img, factor=2):
    """Decimation dengan Burt & Adelson binomial filter"""
    # Keterangan: Inisialisasi atau perbarui variabel kernel.
    kernel = np.array([1, 4, 6, 4, 1], dtype=np.float32) / 16.0
    
    # Keterangan: Inisialisasi atau perbarui variabel blurred.
    blurred = convolve(img.astype(float), kernel[np.newaxis, :], mode='constant')
    # Keterangan: Inisialisasi atau perbarui variabel blurred.
    blurred = convolve(blurred, kernel[:, np.newaxis], mode='constant')
    
    # Keterangan: Inisialisasi atau perbarui variabel decimated.
    decimated = blurred[::factor, ::factor]
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return decimated.astype(img.dtype)


# ===================== MIP-MAPPING =======================

# Keterangan: Definisikan fungsi build_mipmap.
def build_mipmap(img, levels=None):
    """
    Build MIP-map pyramid
    MIP = Multum In Parvo (many things in a small place)
    """
    # Keterangan: Cek kondisi levels is None.
    if levels is None:
        # Keterangan: Inisialisasi beberapa variabel (h, w).
        h, w = img.shape[:2]
        # Keterangan: Inisialisasi atau perbarui variabel levels.
        levels = int(np.log2(max(h, w))) + 1
    
    # Keterangan: Inisialisasi atau perbarui variabel mipmap.
    mipmap = [img]
    
    # Keterangan: Mulai loop dengan for i in range(levels - 1).
    for i in range(levels - 1):
        # Keterangan: Inisialisasi atau perbarui variabel current.
        current = mipmap[-1]
        # Keterangan: Inisialisasi beberapa variabel (h, w).
        h, w = current.shape[:2]
        
        # Keterangan: Cek kondisi h < 2 or w < 2.
        if h < 2 or w < 2:
            # Keterangan: Jalankan perintah berikut.
            break
        
        # Keterangan: Inisialisasi beberapa variabel (next_h, next_w).
        next_h, next_w = h // 2, w // 2
        # Keterangan: Inisialisasi atau perbarui variabel next_level.
        next_level = ndimage.gaussian_filter(current.astype(float), sigma=1.0)
        # Keterangan: Inisialisasi atau perbarui variabel next_level.
        next_level = next_level[::2, ::2]
        
        # Keterangan: Jalankan perintah berikut.
        mipmap.append(next_level.astype(img.dtype))
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return mipmap


# Keterangan: Definisikan fungsi trilinear_mipmap_sampling.
def trilinear_mipmap_sampling(mipmap, x, y, lod):
    """
    Trilinear sampling dari MIP-map
    lod: Level of Detail (fractional)
    """
    # Keterangan: Inisialisasi atau perbarui variabel level_low.
    level_low = int(lod)
    # Keterangan: Inisialisasi atau perbarui variabel level_high.
    level_high = min(level_low + 1, len(mipmap) - 1)
    # Keterangan: Inisialisasi atau perbarui variabel frac.
    frac = lod - level_low
    
    # Keterangan: Cek kondisi level_low >= len(mipmap).
    if level_low >= len(mipmap):
        # Keterangan: Inisialisasi atau perbarui variabel level_low.
        level_low = len(mipmap) - 1
    
    # Keterangan: Inisialisasi atau perbarui variabel img_low.
    img_low = mipmap[level_low]
    # Keterangan: Inisialisasi atau perbarui variabel img_high.
    img_high = mipmap[level_high]
    
    # Keterangan: Inisialisasi atau perbarui variabel scale_low.
    scale_low = 1.0 / (2 ** level_low)
    # Keterangan: Inisialisasi atau perbarui variabel scale_high.
    scale_high = 1.0 / (2 ** level_high)
    
    # Keterangan: Inisialisasi atau perbarui variabel x_low.
    x_low = x * scale_low
    # Keterangan: Inisialisasi atau perbarui variabel y_low.
    y_low = y * scale_low
    # Keterangan: Inisialisasi atau perbarui variabel x_high.
    x_high = x * scale_high
    # Keterangan: Inisialisasi atau perbarui variabel y_high.
    y_high = y * scale_high
    
    # Keterangan: Inisialisasi beberapa variabel (h_low, w_low).
    h_low, w_low = img_low.shape[:2]
    # Keterangan: Inisialisasi beberapa variabel (h_high, w_high).
    h_high, w_high = img_high.shape[:2]
    
    # Keterangan: Inisialisasi atau perbarui variabel x_low.
    x_low = np.clip(int(x_low), 0, w_low - 1)
    # Keterangan: Inisialisasi atau perbarui variabel y_low.
    y_low = np.clip(int(y_low), 0, h_low - 1)
    # Keterangan: Inisialisasi atau perbarui variabel x_high.
    x_high = np.clip(int(x_high), 0, w_high - 1)
    # Keterangan: Inisialisasi atau perbarui variabel y_high.
    y_high = np.clip(int(y_high), 0, h_high - 1)
    
    # Keterangan: Inisialisasi atau perbarui variabel sample_low.
    sample_low = img_low[y_low, x_low]
    # Keterangan: Inisialisasi atau perbarui variabel sample_high.
    sample_high = img_high[y_high, x_high]
    
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = sample_low * (1 - frac) + sample_high * frac
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# ==================== DEMONSTRASI ====================

# Keterangan: Definisikan fungsi demo_1_interpolation_comparison.
def demo_1_interpolation_comparison():
    """Demo 1: Bandingkan berbagai interpolation methods"""
    print("\nDemo 1: Interpolation Methods Comparison")
    print("="*70)
    
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    scale = 2.0
    
    nn = nearest_neighbor_interpolate(img, scale)
    bl = bilinear_interpolation(img, scale)
    bc = bicubic_interpolation(img, scale, a=-0.5)
    lz = lanczos_interpolation(img, scale, a=3)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f'Interpolation Methods (Scale {scale}x)', fontsize=14, fontweight='bold')
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(nn, cmap='gray')
    axes[0, 1].set_title('Nearest Neighbor')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(bl, cmap='gray')
    axes[0, 2].set_title('Bilinear')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(bc, cmap='gray')
    axes[1, 0].set_title('Bicubic')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(lz, cmap='gray')
    axes[1, 1].set_title('Lanczos-3')
    axes[1, 1].axis('off')
    
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('14_demo1_interpolation_comparison.png', dpi=150, bbox_inches='tight')
    print("Saved: 14_demo1_interpolation_comparison.png")
    plt.close()


def demo_2_cubic_parameter_effects():
    """Demo 2: Efek dari cubic kernel parameter"""
    # Keterangan: Jalankan perintah berikut.
    print("\nDemo 2: Cubic Kernel Parameter Effects")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Baca gambar dari file ke array.
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    # Keterangan: Cek kondisi img is None.
    if img is None:
        # Keterangan: Inisialisasi atau perbarui variabel img.
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    # Keterangan: Inisialisasi atau perbarui variabel a_values.
    a_values = [-1.0, -0.5, 0.0, 0.25]
    # Keterangan: Inisialisasi atau perbarui variabel scale.
    scale = 1.5
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    # Keterangan: Inisialisasi beberapa variabel (fig.suptitle('Bicubic Interpolation - Parameter a Effects', fontsize).
    fig.suptitle('Bicubic Interpolation - Parameter a Effects', fontsize=14, fontweight='bold')
    
    # Keterangan: Mulai loop dengan for idx, a in enumerate(a_values).
    for idx, a in enumerate(a_values):
        # Keterangan: Inisialisasi atau perbarui variabel result.
        result = bicubic_interpolation(img, scale, a=a)
        # Keterangan: Inisialisasi atau perbarui variabel ax.
        ax = axes[idx // 2, idx % 2]
        # Keterangan: Inisialisasi beberapa variabel (ax.imshow(result, cmap).
        ax.imshow(result, cmap='gray')
        # Keterangan: Inisialisasi atau perbarui variabel ax.set_title(f'a.
        ax.set_title(f'a = {a}')
        # Keterangan: Jalankan perintah berikut.
        ax.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('14_demo2_cubic_parameter_effects.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 14_demo2_cubic_parameter_effects.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_3_decimation_comparison.
def demo_3_decimation_comparison():
    """Demo 3: Bandingkan decimation methods"""
    print("\nDemo 3: Decimation Methods Comparison")
    print("="*70)
    
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    naive = img[::2, ::2]
    gaussian = decimate_with_prefilter(img, factor=2)
    binomial = decimate_with_binomial_filter(img, factor=2)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Decimation Methods (2x downsampling)', fontsize=14, fontweight='bold')
    
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(naive, cmap='gray')
    axes[0, 1].set_title('Naive (no filter)')
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(gaussian, cmap='gray')
    axes[1, 0].set_title('Gaussian Prefilter')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(binomial, cmap='gray')
    axes[1, 1].set_title('Binomial Filter')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('14_demo3_decimation_comparison.png', dpi=150, bbox_inches='tight')
    print("Saved: 14_demo3_decimation_comparison.png")
    plt.close()


def demo_4_mip_mapping():
    """Demo 4: MIP-map pyramid construction"""
    # Keterangan: Jalankan perintah berikut.
    print("\nDemo 4: MIP-Map Pyramid Construction")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Baca gambar dari file ke array.
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    # Keterangan: Cek kondisi img is None.
    if img is None:
        # Keterangan: Inisialisasi atau perbarui variabel img.
        img = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
    
    # Keterangan: Inisialisasi atau perbarui variabel mipmap.
    mipmap = build_mipmap(img, levels=5)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    # Keterangan: Inisialisasi beberapa variabel (fig.suptitle('MIP-Map Pyramid (Multum In Parvo)', fontsize).
    fig.suptitle('MIP-Map Pyramid (Multum In Parvo)', fontsize=14, fontweight='bold')
    
    # Keterangan: Mulai loop dengan for idx in range(min(6, len(mipmap))).
    for idx in range(min(6, len(mipmap))):
        # Keterangan: Inisialisasi atau perbarui variabel ax.
        ax = axes[idx // 3, idx % 3]
        # Keterangan: Inisialisasi atau perbarui variabel level.
        level = mipmap[idx]
        # Keterangan: Inisialisasi beberapa variabel (ax.imshow(level, cmap).
        ax.imshow(level, cmap='gray')
        # Keterangan: Inisialisasi beberapa variabel (h, w).
        h, w = level.shape[:2]
        # Keterangan: Jalankan perintah berikut.
        ax.set_title(f'Level {idx} ({w}x{h})')
        # Keterangan: Jalankan perintah berikut.
        ax.axis('off')
    
    # Keterangan: Mulai loop dengan for idx in range(len(mipmap), 6).
    for idx in range(len(mipmap), 6):
        # Keterangan: Inisialisasi atau perbarui variabel ax.
        ax = axes[idx // 3, idx % 3]
        # Keterangan: Jalankan perintah berikut.
        ax.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('14_demo4_mip_mapping.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 14_demo4_mip_mapping.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_5_zoom_sequence.
def demo_5_zoom_sequence():
    """Demo 5: Zoom sequence menggunakan interpolation"""
    print("\nDemo 5: Zoom Sequence with Interpolation")
    print("="*70)
    
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    
    scales = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Progressive Zoom Sequence (Bicubic)', fontsize=14, fontweight='bold')
    
    for idx, scale in enumerate(scales):
        result = bicubic_interpolation(img, scale, a=-0.5)
        ax = axes[idx // 3, idx % 3]
        ax.imshow(result, cmap='gray')
        ax.set_title(f'{scale}x Zoom')
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('14_demo5_zoom_sequence.png', dpi=150, bbox_inches='tight')
    print("Saved: 14_demo5_zoom_sequence.png")
    plt.close()


def demo_6_decimation_ratio_effects():
    """Demo 6: Efek dari berbagai decimation ratios"""
    # Keterangan: Jalankan perintah berikut.
    print("\nDemo 6: Decimation Ratio Effects")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Baca gambar dari file ke array.
    img = cv2.imread('../../sample_images/lena.jpg', cv2.IMREAD_GRAYSCALE)
    # Keterangan: Cek kondisi img is None.
    if img is None:
        # Keterangan: Inisialisasi array bernilai satu.
        img = np.ones((512, 512), dtype=np.uint8) * 100
        # Keterangan: Jalankan perintah berikut.
        cv2.circle(img, (256, 256), 100, 255, -1)
    
    # Keterangan: Inisialisasi atau perbarui variabel factors.
    factors = [1, 2, 4, 8]
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    # Keterangan: Inisialisasi beberapa variabel (fig.suptitle('Decimation with Different Factors (Gaussian)', fontsize).
    fig.suptitle('Decimation with Different Factors (Gaussian)', fontsize=14, fontweight='bold')
    
    # Keterangan: Mulai loop dengan for idx, factor in enumerate(factors).
    for idx, factor in enumerate(factors):
        # Keterangan: Inisialisasi atau perbarui variabel result.
        result = decimate_with_prefilter(img, factor=factor)
        # Keterangan: Inisialisasi atau perbarui variabel ax.
        ax = axes[idx // 2, idx % 2]
        # Keterangan: Inisialisasi beberapa variabel (ax.imshow(result, cmap).
        ax.imshow(result, cmap='gray')
        # Keterangan: Inisialisasi beberapa variabel (h, w).
        h, w = result.shape[:2]
        # Keterangan: Jalankan perintah berikut.
        ax.set_title(f'Factor {factor} ({w}x{h})')
        # Keterangan: Jalankan perintah berikut.
        ax.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('14_demo6_decimation_ratio_effects.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 14_demo6_decimation_ratio_effects.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# ===================== MAIN =======================

# Keterangan: Cek kondisi __name__ == "__main__".
if __name__ == "__main__":
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*70)
    # Keterangan: Jalankan perintah berikut.
    print("INTERPOLASI, DECIMASI, DAN MIP-MAPPING ADVANCED")
    # Keterangan: Jalankan perintah berikut.
    print("Praktikum Bab 03: Pemrosesan Citra")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    
    # Keterangan: Jalankan perintah berikut.
    print("\nKeterangan:")
    # Keterangan: Jalankan perintah berikut.
    print("- Interpolasi: mengubah ukuran dengan meningkatkan sample rate")
    # Keterangan: Jalankan perintah berikut.
    print("- Decimasi: mengurangi sample rate dengan prefiltering")
    # Keterangan: Jalankan perintah berikut.
    print("- MIP-mapping: pre-computed pyramids untuk texture mapping")
    # Keterangan: Jalankan perintah berikut.
    print("- Trade-off: kualitas vs kecepatan komputasi")
    
    # Keterangan: Jalankan perintah berikut.
    demo_1_interpolation_comparison()
    # Keterangan: Jalankan perintah berikut.
    demo_2_cubic_parameter_effects()
    # Keterangan: Jalankan perintah berikut.
    demo_3_decimation_comparison()
    # Keterangan: Jalankan perintah berikut.
    demo_4_mip_mapping()
    # Keterangan: Jalankan perintah berikut.
    demo_5_zoom_sequence()
    # Keterangan: Jalankan perintah berikut.
    demo_6_decimation_ratio_effects()
    
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*70)
    # Keterangan: Jalankan perintah berikut.
    print("SEMUA DEMONSTRASI SELESAI")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70)
    # Keterangan: Jalankan perintah berikut.
    print("\nFile output: 14_demoX_*.png")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*70 + "\n")
