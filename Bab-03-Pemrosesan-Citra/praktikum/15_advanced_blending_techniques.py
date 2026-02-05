"""
Percobaan 15: Advanced Blending Techniques
===========================================

Materi yang dicakup:
- Section 3.5.5: Advanced Blending
- Gradient domain blending (Poisson blending)
- Laplacian pyramid blending
- Multi-band blending
- Feathering and alpha blending
- Seamless cloning (Poisson image editing)
- Exposure blending

Referensi: Szeliski "Computer Vision: Algorithms and Applications" halaman 167-170

Author: Computer Vision Course
Date: 2024
"""

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor komponen dari modul scipy.
from scipy import sparse
# Keterangan: Impor komponen dari modul scipy.sparse.linalg.
from scipy.sparse.linalg import spsolve


# Keterangan: Definisikan fungsi create_alpha_mask.
def create_alpha_mask(shape, center, radius, feather_size=20):
    """
    Membuat alpha mask dengan feathering untuk blending
    
    Parameters:
    - shape: tuple (height, width)
    - center: tuple (cx, cy) pusat mask
    - radius: radius lingkaran mask
    - feather_size: ukuran feathering di tepi
    
    Returns:
    - alpha: mask dengan nilai 0-1 (float32)
    """
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = shape
    # Keterangan: Inisialisasi beberapa variabel (y, x).
    y, x = np.ogrid[:h, :w]
    
    # Distance dari center
    # Keterangan: Inisialisasi atau perbarui variabel dist.
    dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    
    # Alpha dengan feathering
    # Keterangan: Inisialisasi array bernilai nol.
    alpha = np.zeros((h, w), dtype=np.float32)
    # Keterangan: Inisialisasi atau perbarui variabel alpha[dist <.
    alpha[dist <= radius - feather_size] = 1.0
    
    # Feather region
    # Keterangan: Inisialisasi atau perbarui variabel feather_mask.
    feather_mask = (dist > radius - feather_size) & (dist <= radius)
    # Keterangan: Inisialisasi atau perbarui variabel alpha[feather_mask].
    alpha[feather_mask] = (radius - dist[feather_mask]) / feather_size
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return alpha


# Keterangan: Definisikan fungsi alpha_blending.
def alpha_blending(src, dst, alpha):
    """
    Melakukan alpha blending antara source dan destination
    
    Formula: result = src * alpha + dst * (1 - alpha)
    
    Parameters:
    - src: source image
    - dst: destination image
    - alpha: alpha channel (0-1)
    
    Returns:
    - blended: hasil blending
    """
    # Ensure same size
    # Keterangan: Cek kondisi src.shape[2] != dst.shape[2].
    if src.shape[:2] != dst.shape[:2]:
        # Keterangan: Ubah ukuran gambar.
        src = cv2.resize(src, (dst.shape[1], dst.shape[0]))
    
    # Convert to float
    # Keterangan: Inisialisasi atau perbarui variabel src_f.
    src_f = src.astype(np.float32)
    # Keterangan: Inisialisasi atau perbarui variabel dst_f.
    dst_f = dst.astype(np.float32)
    
    # Expand alpha untuk multi-channel
    # Keterangan: Cek kondisi len(src.shape) == 3.
    if len(src.shape) == 3:
        # Keterangan: Inisialisasi atau perbarui variabel alpha.
        alpha = np.stack([alpha] * src.shape[2], axis=2)
    
    # Blending
    # Keterangan: Inisialisasi atau perbarui variabel blended.
    blended = src_f * alpha + dst_f * (1 - alpha)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return np.clip(blended, 0, 255).astype(np.uint8)


# Keterangan: Definisikan fungsi build_laplacian_pyramid.
def build_laplacian_pyramid(img, levels):
    """
    Membangun Laplacian pyramid untuk multi-scale blending
    
    Laplacian = Gaussian[i] - expand(Gaussian[i+1])
    
    Parameters:
    - img: input image
    - levels: jumlah level pyramid
    
    Returns:
    - laplacian_pyramid: list of Laplacian images
    - gaussian_top: top level Gaussian
    """
    # Keterangan: Inisialisasi atau perbarui variabel gaussian_pyramid.
    gaussian_pyramid = [img.astype(np.float32)]
    
    # Build Gaussian pyramid
    # Keterangan: Mulai loop dengan for i in range(levels).
    for i in range(levels):
        # Keterangan: Downsample gambar untuk membangun pyramid.
        img = cv2.pyrDown(img)
        # Keterangan: Jalankan perintah berikut.
        gaussian_pyramid.append(img.astype(np.float32))
    
    # Build Laplacian pyramid
    # Keterangan: Inisialisasi atau perbarui variabel laplacian_pyramid.
    laplacian_pyramid = []
    # Keterangan: Mulai loop dengan for i in range(levels).
    for i in range(levels):
        # Keterangan: Upsample gambar untuk membangun pyramid.
        expanded = cv2.pyrUp(gaussian_pyramid[i + 1])
        
        # Resize jika perlu
        # Keterangan: Cek kondisi expanded.shape != gaussian_pyramid[i].shape.
        if expanded.shape != gaussian_pyramid[i].shape:
            # Keterangan: Ubah ukuran gambar.
            expanded = cv2.resize(expanded, 
                                 # Keterangan: Jalankan perintah berikut.
                                 (gaussian_pyramid[i].shape[1], 
                                  # Keterangan: Jalankan perintah berikut.
                                  gaussian_pyramid[i].shape[0]))
        
        # Keterangan: Inisialisasi atau perbarui variabel laplacian.
        laplacian = gaussian_pyramid[i] - expanded
        # Keterangan: Jalankan perintah berikut.
        laplacian_pyramid.append(laplacian)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return laplacian_pyramid, gaussian_pyramid[-1]


# Keterangan: Definisikan fungsi reconstruct_from_laplacian_pyramid.
def reconstruct_from_laplacian_pyramid(laplacian_pyramid, gaussian_top):
    """
    Merekonstruksi image dari Laplacian pyramid
    
    Parameters:
    - laplacian_pyramid: list of Laplacian images
    - gaussian_top: top level Gaussian
    
    Returns:
    - reconstructed: reconstructed image
    """
    # Keterangan: Inisialisasi atau perbarui variabel img.
    img = gaussian_top
    
    # Keterangan: Mulai loop dengan for laplacian in reversed(laplacian_pyramid).
    for laplacian in reversed(laplacian_pyramid):
        # Keterangan: Upsample gambar untuk membangun pyramid.
        img = cv2.pyrUp(img)
        
        # Resize jika perlu
        # Keterangan: Cek kondisi img.shape != laplacian.shape.
        if img.shape != laplacian.shape:
            # Keterangan: Ubah ukuran gambar.
            img = cv2.resize(img, (laplacian.shape[1], laplacian.shape[0]))
        
        # Keterangan: Inisialisasi atau perbarui variabel img.
        img = img + laplacian
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return np.clip(img, 0, 255).astype(np.uint8)


# Keterangan: Definisikan fungsi laplacian_pyramid_blending.
def laplacian_pyramid_blending(src, dst, mask, levels=5):
    """
    Melakukan multi-band blending menggunakan Laplacian pyramid
    
    Metode Burt & Adelson (1983) untuk seamless blending
    
    Parameters:
    - src: source image
    - dst: destination image
    - mask: binary mask (0 atau 255)
    - levels: jumlah level pyramid
    
    Returns:
    - blended: hasil blending
    """
    # Ensure same size
    # Keterangan: Cek kondisi src.shape != dst.shape.
    if src.shape != dst.shape:
        # Keterangan: Ubah ukuran gambar.
        src = cv2.resize(src, (dst.shape[1], dst.shape[0]))
    
    # Build Laplacian pyramids
    # Keterangan: Inisialisasi beberapa variabel (lap_src, gauss_src_top).
    lap_src, gauss_src_top = build_laplacian_pyramid(src, levels)
    # Keterangan: Inisialisasi beberapa variabel (lap_dst, gauss_dst_top).
    lap_dst, gauss_dst_top = build_laplacian_pyramid(dst, levels)
    
    # Build Gaussian pyramid untuk mask
    # Keterangan: Inisialisasi atau perbarui variabel mask_pyramid.
    mask_pyramid = [mask.astype(np.float32) / 255.0]
    # Keterangan: Inisialisasi atau perbarui variabel temp_mask.
    temp_mask = mask.copy()
    # Keterangan: Mulai loop dengan for i in range(levels).
    for i in range(levels):
        # Keterangan: Downsample gambar untuk membangun pyramid.
        temp_mask = cv2.pyrDown(temp_mask)
        # Keterangan: Jalankan perintah berikut.
        mask_pyramid.append(temp_mask.astype(np.float32) / 255.0)
    
    # Blend setiap level
    # Keterangan: Inisialisasi atau perbarui variabel blended_pyramid.
    blended_pyramid = []
    # Keterangan: Mulai loop dengan for ls, ld, m in zip(lap_src, lap_dst, mask_pyramid).
    for ls, ld, m in zip(lap_src, lap_dst, mask_pyramid):
        # Expand mask untuk multi-channel
        # Keterangan: Cek kondisi len(ls.shape) == 3.
        if len(ls.shape) == 3:
            # Keterangan: Inisialisasi atau perbarui variabel m.
            m = np.stack([m] * ls.shape[2], axis=2)
        
        # Keterangan: Inisialisasi atau perbarui variabel blended.
        blended = ls * m + ld * (1 - m)
        # Keterangan: Jalankan perintah berikut.
        blended_pyramid.append(blended)
    
    # Blend top level Gaussian
    # Keterangan: Inisialisasi atau perbarui variabel m_top.
    m_top = mask_pyramid[-1]
    # Keterangan: Cek kondisi len(gauss_src_top.shape) == 3.
    if len(gauss_src_top.shape) == 3:
        # Keterangan: Inisialisasi atau perbarui variabel m_top.
        m_top = np.stack([m_top] * gauss_src_top.shape[2], axis=2)
    
    # Keterangan: Inisialisasi atau perbarui variabel blended_top.
    blended_top = gauss_src_top * m_top + gauss_dst_top * (1 - m_top)
    
    # Reconstruct
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = reconstruct_from_laplacian_pyramid(blended_pyramid, blended_top)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi poisson_blending.
def poisson_blending(src, dst, mask, offset=(0, 0), method='seamless'):
    """
    Melakukan Poisson blending (gradient domain blending)
    
    Menyelesaikan persamaan Poisson: ∇²f = ∇²g
    dengan boundary condition dari destination image
    
    Parameters:
    - src: source image (region to blend)
    - dst: destination image
    - mask: binary mask (255 = source, 0 = destination)
    - offset: tuple (x, y) offset untuk source
    - method: 'seamless' atau 'mixed' gradient
    
    Returns:
    - result: blended image
    """
    # Ensure mask is single channel
    # Keterangan: Cek kondisi len(mask.shape) == 3.
    if len(mask.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # Find center of mask
    # Keterangan: Inisialisasi beberapa variabel (y_indices, x_indices).
    y_indices, x_indices = np.where(mask > 0)
    # Keterangan: Cek kondisi len(y_indices) == 0.
    if len(y_indices) == 0:
        # Keterangan: Kembalikan hasil dari fungsi.
        return dst.copy()
    
    # Keterangan: Inisialisasi atau perbarui variabel center.
    center = (int(np.mean(x_indices)) + offset[0], 
              # Keterangan: Jalankan perintah berikut.
              int(np.mean(y_indices)) + offset[1])
    
    # OpenCV Poisson blending
    # Keterangan: Cek kondisi method == 'seamless'.
    if method == 'seamless':
        # Keterangan: Inisialisasi atau perbarui variabel flags.
        flags = cv2.NORMAL_CLONE
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel flags.
        flags = cv2.MIXED_CLONE
    
    # Keterangan: Mulai blok try untuk menangani error.
    try:
        # Keterangan: Inisialisasi atau perbarui variabel result.
        result = cv2.seamlessClone(src, dst, mask, center, flags)
    # Keterangan: Tangani error pada blok except.
    except cv2.error:
        # Fallback ke alpha blending
        # Keterangan: Inisialisasi atau perbarui variabel alpha.
        alpha = mask.astype(np.float32) / 255.0
        # Keterangan: Inisialisasi atau perbarui variabel result.
        result = alpha_blending(src, dst, alpha)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result


# Keterangan: Definisikan fungsi gradient_domain_blending_manual.
def gradient_domain_blending_manual(src, dst, mask):
    """
    Implementasi manual Poisson blending untuk single channel
    
    Menyelesaikan sistem persamaan linear sparse
    
    Parameters:
    - src: source image (grayscale)
    - dst: destination image (grayscale)
    - mask: binary mask
    
    Returns:
    - result: blended image
    """
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = src.shape
    
    # Ensure mask is binary
    # Keterangan: Inisialisasi atau perbarui variabel mask.
    mask = (mask > 127).astype(np.uint8)
    
    # Compute gradients
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    grad_x_src = cv2.Sobel(src.astype(np.float32), cv2.CV_32F, 1, 0, ksize=1)
    # Keterangan: Hitung gradien Sobel untuk deteksi tepi.
    grad_y_src = cv2.Sobel(src.astype(np.float32), cv2.CV_32F, 0, 1, ksize=1)
    
    # Number pixels
    # Keterangan: Inisialisasi array bernilai nol.
    pixel_id = np.zeros((h, w), dtype=np.int32)
    # Keterangan: Buat range angka berjarak tetap.
    pixel_id[mask > 0] = np.arange(np.sum(mask > 0))
    
    # Keterangan: Inisialisasi atau perbarui variabel num_pixels.
    num_pixels = np.sum(mask > 0)
    
    # Keterangan: Cek kondisi num_pixels == 0.
    if num_pixels == 0:
        # Keterangan: Kembalikan hasil dari fungsi.
        return dst.copy()
    
    # Build sparse system: A*x = b
    # A: coefficient matrix
    # x: unknown pixel values
    # b: right-hand side (divergence + boundary)
    
    # Keterangan: Inisialisasi atau perbarui variabel A_data.
    A_data = []
    # Keterangan: Inisialisasi atau perbarui variabel A_row.
    A_row = []
    # Keterangan: Inisialisasi atau perbarui variabel A_col.
    A_col = []
    # Keterangan: Inisialisasi array bernilai nol.
    b = np.zeros(num_pixels)
    
    # Keterangan: Mulai loop dengan for y in range(h).
    for y in range(h):
        # Keterangan: Mulai loop dengan for x in range(w).
        for x in range(w):
            # Keterangan: Cek kondisi mask[y, x] == 0.
            if mask[y, x] == 0:
                # Keterangan: Jalankan perintah berikut.
                continue
            
            # Keterangan: Inisialisasi atau perbarui variabel idx.
            idx = pixel_id[y, x]
            
            # Laplacian coefficient (center)
            # Keterangan: Jalankan perintah berikut.
            A_data.append(4.0)
            # Keterangan: Jalankan perintah berikut.
            A_row.append(idx)
            # Keterangan: Jalankan perintah berikut.
            A_col.append(idx)
            
            # Right-hand side: divergence dari gradient source
            # Keterangan: Inisialisasi atau perbarui variabel div.
            div = 0.0
            
            # Neighbors
            # Keterangan: Mulai loop dengan for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)].
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Keterangan: Inisialisasi beberapa variabel (ny, nx).
                ny, nx = y + dy, x + dx
                
                # Keterangan: Cek kondisi 0 <= ny < h and 0 <= nx < w.
                if 0 <= ny < h and 0 <= nx < w:
                    # Gradient contribution
                    # Keterangan: Cek kondisi dx != 0.
                    if dx != 0:
                        # Keterangan: Inisialisasi atau perbarui variabel div +.
                        div += grad_x_src[y, x] - grad_x_src[ny, nx]
                    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
                    else:
                        # Keterangan: Inisialisasi atau perbarui variabel div +.
                        div += grad_y_src[y, x] - grad_y_src[ny, nx]
                    
                    # Keterangan: Cek kondisi mask[ny, nx] > 0.
                    if mask[ny, nx] > 0:
                        # Interior neighbor
                        # Keterangan: Inisialisasi atau perbarui variabel neighbor_idx.
                        neighbor_idx = pixel_id[ny, nx]
                        # Keterangan: Jalankan perintah berikut.
                        A_data.append(-1.0)
                        # Keterangan: Jalankan perintah berikut.
                        A_row.append(idx)
                        # Keterangan: Jalankan perintah berikut.
                        A_col.append(neighbor_idx)
                    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
                    else:
                        # Boundary: use destination value
                        # Keterangan: Inisialisasi atau perbarui variabel div +.
                        div += dst[ny, nx]
            
            # Keterangan: Inisialisasi atau perbarui variabel b[idx].
            b[idx] = div
    
    # Solve sparse system
    # Keterangan: Inisialisasi atau perbarui variabel A.
    A = sparse.csr_matrix((A_data, (A_row, A_col)), 
                          # Keterangan: Inisialisasi atau perbarui variabel shape.
                          shape=(num_pixels, num_pixels))
    
    # Keterangan: Inisialisasi atau perbarui variabel x.
    x = spsolve(A, b)
    
    # Reconstruct image
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = dst.copy().astype(np.float32)
    # Keterangan: Mulai loop dengan for y in range(h).
    for y in range(h):
        # Keterangan: Mulai loop dengan for x in range(w).
        for x in range(w):
            # Keterangan: Cek kondisi mask[y, x] > 0.
            if mask[y, x] > 0:
                # Keterangan: Inisialisasi beberapa variabel (result[y, x]).
                result[y, x] = x[pixel_id[y, x]]
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return np.clip(result, 0, 255).astype(np.uint8)


# Keterangan: Definisikan fungsi exposure_blending.
def exposure_blending(images, exposure_weights=None):
    """
    Melakukan exposure blending untuk HDR imaging
    
    Menggunakan weighted average berdasarkan exposure quality
    
    Parameters:
    - images: list of images dengan exposure berbeda
    - exposure_weights: optional list of weights
    
    Returns:
    - blended: exposure-blended image
    """
    # Keterangan: Cek kondisi len(images) == 0.
    if len(images) == 0:
        # Keterangan: Kembalikan hasil dari fungsi.
        return None
    
    # Ensure same size
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = images[0].shape[:2]
    # Keterangan: Mulai loop dengan for i in range(1, len(images)).
    for i in range(1, len(images)):
        # Keterangan: Cek kondisi images[i].shape[2] != (h, w).
        if images[i].shape[:2] != (h, w):
            # Keterangan: Ubah ukuran gambar.
            images[i] = cv2.resize(images[i], (w, h))
    
    # Compute weights berdasarkan well-exposedness
    # Keterangan: Cek kondisi exposure_weights is None.
    if exposure_weights is None:
        # Keterangan: Inisialisasi atau perbarui variabel weights.
        weights = []
        # Keterangan: Mulai loop dengan for img in images.
        for img in images:
            # Contrast weight
            # Keterangan: Konversi ruang warna gambar.
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
            # Keterangan: Hitung Laplacian untuk deteksi tepi.
            lap = cv2.Laplacian(gray.astype(np.float32), cv2.CV_32F)
            # Keterangan: Inisialisasi atau perbarui variabel contrast_weight.
            contrast_weight = np.abs(lap)
            
            # Saturation weight
            # Keterangan: Cek kondisi len(img.shape) == 3.
            if len(img.shape) == 3:
                # Keterangan: Inisialisasi atau perbarui variabel mean_rgb.
                mean_rgb = np.mean(img, axis=2)
                # Keterangan: Inisialisasi atau perbarui variabel std_rgb.
                std_rgb = np.std(img, axis=2)
                # Keterangan: Inisialisasi atau perbarui variabel saturation_weight.
                saturation_weight = std_rgb
            # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
            else:
                # Keterangan: Inisialisasi array bernilai satu.
                saturation_weight = np.ones_like(gray, dtype=np.float32)
            
            # Well-exposedness weight (Gaussian around 0.5)
            # Keterangan: Inisialisasi atau perbarui variabel normalized.
            normalized = img.astype(np.float32) / 255.0
            # Keterangan: Cek kondisi len(img.shape) == 3.
            if len(img.shape) == 3:
                # Keterangan: Inisialisasi atau perbarui variabel exposure_weight.
                exposure_weight = np.exp(-((normalized - 0.5)**2) / (2 * 0.2**2))
                # Keterangan: Inisialisasi atau perbarui variabel exposure_weight.
                exposure_weight = np.mean(exposure_weight, axis=2)
            # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
            else:
                # Keterangan: Inisialisasi atau perbarui variabel exposure_weight.
                exposure_weight = np.exp(-((normalized - 0.5)**2) / (2 * 0.2**2))
            
            # Combine weights
            # Keterangan: Inisialisasi atau perbarui variabel weight.
            weight = contrast_weight * saturation_weight * exposure_weight
            # Keterangan: Inisialisasi atau perbarui variabel weight.
            weight = weight + 1e-12  # Avoid division by zero
            # Keterangan: Jalankan perintah berikut.
            weights.append(weight)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel weights.
        weights = exposure_weights
    
    # Normalize weights
    # Keterangan: Inisialisasi atau perbarui variabel weight_sum.
    weight_sum = np.sum(weights, axis=0)
    # Keterangan: Inisialisasi atau perbarui variabel normalized_weights.
    normalized_weights = [w / weight_sum for w in weights]
    
    # Blend
    # Keterangan: Inisialisasi array bernilai nol.
    blended = np.zeros_like(images[0], dtype=np.float32)
    # Keterangan: Mulai loop dengan for img, weight in zip(images, normalized_weights).
    for img, weight in zip(images, normalized_weights):
        # Keterangan: Cek kondisi len(img.shape) == 3.
        if len(img.shape) == 3:
            # Keterangan: Inisialisasi atau perbarui variabel weight.
            weight = np.stack([weight] * img.shape[2], axis=2)
        # Keterangan: Inisialisasi atau perbarui variabel blended +.
        blended += img.astype(np.float32) * weight
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return np.clip(blended, 0, 255).astype(np.uint8)


# ==================== DEMONSTRATION FUNCTIONS ====================

# Keterangan: Definisikan fungsi demo_alpha_blending.
def demo_alpha_blending():
    """Demo 1: Alpha Blending dengan Feathering"""
    print("\n=== Demo 1: Alpha Blending dengan Feathering ===")
    
    # Create synthetic images
    img1 = np.zeros((400, 400, 3), dtype=np.uint8)
    img1[:, :200] = [255, 100, 100]  # Red
    
    img2 = np.zeros((400, 400, 3), dtype=np.uint8)
    img2[:, 200:] = [100, 100, 255]  # Blue
    
    # Create different alpha masks
    alphas = []
    
    # Hard edge
    alpha_hard = np.zeros((400, 400), dtype=np.float32)
    alpha_hard[:, :200] = 1.0
    alphas.append(('Hard Edge', alpha_hard))
    
    # Linear gradient
    alpha_linear = np.linspace(1, 0, 400).reshape(1, -1)
    alpha_linear = np.repeat(alpha_linear, 400, axis=0).astype(np.float32)
    alphas.append(('Linear Gradient', alpha_linear))
    
    # Circular feathering
    alpha_circle = create_alpha_mask((400, 400), (200, 200), 150, feather_size=50)
    alphas.append(('Circular Feathering', alpha_circle))
    
    # Visualize
    plt.figure(figsize=(15, 10))
    
    for idx, (name, alpha) in enumerate(alphas):
        blended = alpha_blending(img1, img2, alpha)
        
        plt.subplot(2, 3, idx + 1)
        plt.imshow(alpha, cmap='gray')
        plt.title(f'Alpha Mask: {name}')
        plt.axis('off')
        
        plt.subplot(2, 3, idx + 4)
        plt.imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
        plt.title(f'Blended: {name}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('15_alpha_blending.png', dpi=150, bbox_inches='tight')
    print("Saved: 15_alpha_blending.png")
    plt.close()


def demo_laplacian_pyramid_blending():
    """Demo 2: Laplacian Pyramid Multi-Band Blending"""
    # Keterangan: Jalankan perintah berikut.
    print("\n=== Demo 2: Laplacian Pyramid Blending ===")
    
    # Create two different textured images
    # Keterangan: Inisialisasi array bernilai nol.
    img1 = np.zeros((512, 512, 3), dtype=np.uint8)
    # Keterangan: Inisialisasi beberapa variabel (img1[:, :256]).
    img1[:, :256] = [200, 100, 50]
    
    # Keterangan: Inisialisasi array bernilai nol.
    img2 = np.zeros((512, 512, 3), dtype=np.uint8)
    # Keterangan: Inisialisasi beberapa variabel (img2[:, 256:]).
    img2[:, 256:] = [50, 150, 200]
    
    # Add textures
    # Keterangan: Mulai loop dengan for i in range(0, 512, 20).
    for i in range(0, 512, 20):
        # Keterangan: Jalankan perintah berikut.
        cv2.line(img1, (i, 0), (i, 512), (255, 255, 255), 2)
    
    # Keterangan: Mulai loop dengan for i in range(0, 512, 20).
    for i in range(0, 512, 20):
        # Keterangan: Jalankan perintah berikut.
        cv2.line(img2, (0, i), (512, i), (255, 255, 255), 2)
    
    # Create vertical split mask
    # Keterangan: Inisialisasi array bernilai nol.
    mask = np.zeros((512, 512), dtype=np.uint8)
    # Keterangan: Inisialisasi beberapa variabel (mask[:, :256]).
    mask[:, :256] = 255
    
    # Compare different blending methods
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = []
    
    # Direct blending (hard edge)
    # Keterangan: Inisialisasi atau perbarui variabel direct.
    direct = img1.copy()
    # Keterangan: Inisialisasi beberapa variabel (direct[:, 256:]).
    direct[:, 256:] = img2[:, 256:]
    # Keterangan: Jalankan perintah berikut.
    results.append(('Direct (Hard Edge)', direct))
    
    # Alpha blending
    # Keterangan: Inisialisasi atau perbarui variabel alpha.
    alpha = mask.astype(np.float32) / 255.0
    # Keterangan: Inisialisasi atau perbarui variabel alpha_result.
    alpha_result = alpha_blending(img1, img2, alpha)
    # Keterangan: Jalankan perintah berikut.
    results.append(('Alpha Blending', alpha_result))
    
    # Laplacian pyramid blending (different levels)
    # Keterangan: Mulai loop dengan for levels in [3, 5].
    for levels in [3, 5]:
        # Keterangan: Inisialisasi atau perbarui variabel lap_result.
        lap_result = laplacian_pyramid_blending(img1, img2, mask, levels=levels)
        # Keterangan: Jalankan perintah berikut.
        results.append((f'Laplacian ({levels} levels)', lap_result))
    
    # Visualize
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 10))
    
    # Keterangan: Mulai loop dengan for idx, (name, result) in enumerate(results).
    for idx, (name, result) in enumerate(results):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(2, 2, idx + 1)
        # Keterangan: Konversi ruang warna gambar.
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        # Keterangan: Set judul subplot.
        plt.title(name)
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('15_laplacian_pyramid_blending.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 15_laplacian_pyramid_blending.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_poisson_blending.
def demo_poisson_blending():
    """Demo 3: Poisson (Seamless) Blending"""
    print("\n=== Demo 3: Poisson Blending ===")
    
    # Create source dan destination
    h, w = 400, 600
    
    # Destination: gradient background
    dst = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        dst[i, :] = [int(255 * i / h), 100, int(255 * (1 - i / h))]
    
    # Source: circle dengan pattern
    src = np.ones((h, w, 3), dtype=np.uint8) * 255
    cv2.circle(src, (w//2, h//2), 80, (255, 0, 0), -1)
    cv2.circle(src, (w//2, h//2), 60, (0, 255, 0), -1)
    cv2.circle(src, (w//2, h//2), 40, (0, 0, 255), -1)
    
    # Mask: circular region
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w//2, h//2), 100, 255, -1)
    
    # Different blending methods
    results = []
    
    # Direct copy
    direct = dst.copy()
    direct[mask > 0] = src[mask > 0]
    results.append(('Direct Copy', direct))
    
    # Alpha blending
    alpha = mask.astype(np.float32) / 255.0
    alpha_result = alpha_blending(src, dst, alpha)
    results.append(('Alpha Blending', alpha_result))
    
    # Poisson seamless
    poisson_result = poisson_blending(src, dst, mask, offset=(0, 0), method='seamless')
    results.append(('Poisson Seamless', poisson_result))
    
    # Poisson mixed
    poisson_mixed = poisson_blending(src, dst, mask, offset=(0, 0), method='mixed')
    results.append(('Poisson Mixed', poisson_mixed))
    
    # Visualize
    plt.figure(figsize=(12, 8))
    
    for idx, (name, result) in enumerate(results):
        plt.subplot(2, 2, idx + 1)
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        plt.title(name)
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('15_poisson_blending.png', dpi=150, bbox_inches='tight')
    print("Saved: 15_poisson_blending.png")
    plt.close()


def demo_gradient_domain():
    """Demo 4: Gradient Domain Blending Manual"""
    # Keterangan: Jalankan perintah berikut.
    print("\n=== Demo 4: Gradient Domain Blending ===")
    
    # Create simple grayscale test
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = 200, 200
    
    # Destination: horizontal gradient
    # Keterangan: Buat range angka berjarak linier.
    dst = np.linspace(0, 255, w).reshape(1, -1)
    # Keterangan: Inisialisasi atau perbarui variabel dst.
    dst = np.repeat(dst, h, axis=0).astype(np.uint8)
    
    # Source: vertical gradient
    # Keterangan: Buat range angka berjarak linier.
    src = np.linspace(0, 255, h).reshape(-1, 1)
    # Keterangan: Inisialisasi atau perbarui variabel src.
    src = np.repeat(src, w, axis=1).astype(np.uint8)
    
    # Mask: central circle
    # Keterangan: Inisialisasi array bernilai nol.
    mask = np.zeros((h, w), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(mask, (w//2, h//2), 60, 255, -1)
    
    # Blending methods
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = []
    
    # Direct copy
    # Keterangan: Inisialisasi atau perbarui variabel direct.
    direct = dst.copy()
    # Keterangan: Inisialisasi atau perbarui variabel direct[mask > 0].
    direct[mask > 0] = src[mask > 0]
    # Keterangan: Jalankan perintah berikut.
    results.append(('Direct Copy', direct))
    
    # Gradient domain
    # Keterangan: Inisialisasi atau perbarui variabel gradient_result.
    gradient_result = gradient_domain_blending_manual(src, dst, mask)
    # Keterangan: Jalankan perintah berikut.
    results.append(('Gradient Domain', gradient_result))
    
    # Visualize
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(12, 4))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(src, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title('Source')
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 4, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(dst, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title('Destination')
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Mulai loop dengan for idx, (name, result) in enumerate(results).
    for idx, (name, result) in enumerate(results):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(1, 4, idx + 3)
        # Keterangan: Tampilkan gambar pada kanvas.
        plt.imshow(result, cmap='gray')
        # Keterangan: Set judul subplot.
        plt.title(name)
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('15_gradient_domain.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 15_gradient_domain.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Definisikan fungsi demo_exposure_blending.
def demo_exposure_blending():
    """Demo 5: Exposure Blending untuk HDR"""
    print("\n=== Demo 5: Exposure Blending ===")
    
    # Create synthetic exposures
    h, w = 400, 600
    
    # Base image dengan dynamic range
    base = np.zeros((h, w), dtype=np.float32)
    
    # Dark region (kiri)
    base[:, :200] = 50
    
    # Medium region (tengah)
    base[:, 200:400] = 128
    
    # Bright region (kanan)
    base[:, 400:] = 200
    
    # Add gradients
    for i in range(h):
        base[i, :] += 30 * np.sin(i * np.pi / h)
    
    # Simulate different exposures
    exposures = []
    
    # Underexposed (detail di highlight)
    under = np.clip(base * 0.5, 0, 255).astype(np.uint8)
    exposures.append(under)
    
    # Normal exposure
    normal = np.clip(base, 0, 255).astype(np.uint8)
    exposures.append(normal)
    
    # Overexposed (detail di shadow)
    over = np.clip(base * 1.5, 0, 255).astype(np.uint8)
    exposures.append(over)
    
    # Exposure blending
    blended = exposure_blending([cv2.cvtColor(e, cv2.COLOR_GRAY2BGR) for e in exposures])
    blended_gray = cv2.cvtColor(blended, cv2.COLOR_BGR2GRAY)
    
    # Visualize
    plt.figure(figsize=(15, 8))
    
    plt.subplot(2, 3, 1)
    plt.imshow(under, cmap='gray')
    plt.title('Underexposed')
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(normal, cmap='gray')
    plt.title('Normal')
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(over, cmap='gray')
    plt.title('Overexposed')
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.imshow(blended_gray, cmap='gray')
    plt.title('Exposure Blended')
    plt.axis('off')
    
    # Histogram comparison
    plt.subplot(2, 3, 5)
    plt.hist(under.ravel(), bins=50, alpha=0.5, label='Under')
    plt.hist(normal.ravel(), bins=50, alpha=0.5, label='Normal')
    plt.hist(over.ravel(), bins=50, alpha=0.5, label='Over')
    plt.title('Input Histograms')
    plt.legend()
    
    plt.subplot(2, 3, 6)
    plt.hist(blended_gray.ravel(), bins=50, color='green', alpha=0.7)
    plt.title('Blended Histogram')
    
    plt.tight_layout()
    plt.savefig('15_exposure_blending.png', dpi=150, bbox_inches='tight')
    print("Saved: 15_exposure_blending.png")
    plt.close()


def demo_multiband_comparison():
    """Demo 6: Perbandingan Multi-Band Blending"""
    # Keterangan: Jalankan perintah berikut.
    print("\n=== Demo 6: Multi-Band Blending Comparison ===")
    
    # Create two images dengan frequency content berbeda
    # Keterangan: Inisialisasi beberapa variabel (h, w).
    h, w = 512, 512
    
    # Image 1: Low frequency (smooth gradient)
    # Keterangan: Inisialisasi array bernilai nol.
    img1 = np.zeros((h, w, 3), dtype=np.uint8)
    # Keterangan: Mulai loop dengan for i in range(h).
    for i in range(h):
        # Keterangan: Mulai loop dengan for j in range(w).
        for j in range(w):
            # Keterangan: Inisialisasi beberapa variabel (img1[i, j]).
            img1[i, j] = [int(255 * i / h), int(255 * j / w), 128]
    
    # Image 2: High frequency (checkerboard)
    # Keterangan: Inisialisasi array bernilai nol.
    img2 = np.zeros((h, w, 3), dtype=np.uint8)
    # Keterangan: Inisialisasi atau perbarui variabel cell_size.
    cell_size = 32
    # Keterangan: Mulai loop dengan for i in range(0, h, cell_size).
    for i in range(0, h, cell_size):
        # Keterangan: Mulai loop dengan for j in range(0, w, cell_size).
        for j in range(0, w, cell_size):
            # Keterangan: Cek kondisi ((i // cell_size) + (j // cell_size)) % 2 == 0.
            if ((i // cell_size) + (j // cell_size)) % 2 == 0:
                # Keterangan: Inisialisasi beberapa variabel (img2[i:i+cell_size, j:j+cell_size]).
                img2[i:i+cell_size, j:j+cell_size] = [200, 50, 50]
            # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
            else:
                # Keterangan: Inisialisasi beberapa variabel (img2[i:i+cell_size, j:j+cell_size]).
                img2[i:i+cell_size, j:j+cell_size] = [50, 50, 200]
    
    # Diagonal mask
    # Keterangan: Inisialisasi array bernilai nol.
    mask = np.zeros((h, w), dtype=np.uint8)
    # Keterangan: Mulai loop dengan for i in range(h).
    for i in range(h):
        # Keterangan: Inisialisasi beberapa variabel (mask[i, :i]).
        mask[i, :i] = 255
    
    # Different pyramid levels
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = []
    
    # Keterangan: Mulai loop dengan for levels in [1, 3, 5, 7].
    for levels in [1, 3, 5, 7]:
        # Keterangan: Cek kondisi levels == 1.
        if levels == 1:
            # Alpha blending
            # Keterangan: Inisialisasi atau perbarui variabel alpha.
            alpha = mask.astype(np.float32) / 255.0
            # Keterangan: Inisialisasi atau perbarui variabel result.
            result = alpha_blending(img1, img2, alpha)
            # Keterangan: Inisialisasi atau perbarui variabel name.
            name = 'Alpha (no pyramid)'
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Keterangan: Inisialisasi atau perbarui variabel result.
            result = laplacian_pyramid_blending(img1, img2, mask, levels=levels)
            # Keterangan: Inisialisasi atau perbarui variabel name.
            name = f'{levels} levels'
        
        # Keterangan: Jalankan perintah berikut.
        results.append((name, result))
    
    # Visualize
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(12, 8))
    
    # Keterangan: Mulai loop dengan for idx, (name, result) in enumerate(results).
    for idx, (name, result) in enumerate(results):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(2, 2, idx + 1)
        # Keterangan: Konversi ruang warna gambar.
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        # Keterangan: Set judul subplot.
        plt.title(name)
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Simpan hasil visualisasi ke file.
    plt.savefig('15_multiband_comparison.png', dpi=150, bbox_inches='tight')
    # Keterangan: Jalankan perintah berikut.
    print("Saved: 15_multiband_comparison.png")
    # Keterangan: Tutup figure untuk menghemat memori.
    plt.close()


# Keterangan: Cek kondisi __name__ == "__main__".
if __name__ == "__main__":
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    # Keterangan: Jalankan perintah berikut.
    print("Percobaan 15: Advanced Blending Techniques")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Keterangan: Jalankan perintah berikut.
    demo_alpha_blending()
    # Keterangan: Jalankan perintah berikut.
    demo_laplacian_pyramid_blending()
    # Keterangan: Jalankan perintah berikut.
    demo_poisson_blending()
    # Keterangan: Jalankan perintah berikut.
    demo_gradient_domain()
    # Keterangan: Jalankan perintah berikut.
    demo_exposure_blending()
    # Keterangan: Jalankan perintah berikut.
    demo_multiband_comparison()
    
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("Semua demo selesai!")
    # Keterangan: Jalankan perintah berikut.
    print("File output:")
    # Keterangan: Jalankan perintah berikut.
    print("- 15_alpha_blending.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 15_laplacian_pyramid_blending.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 15_poisson_blending.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 15_gradient_domain.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 15_exposure_blending.png")
    # Keterangan: Jalankan perintah berikut.
    print("- 15_multiband_comparison.png")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
