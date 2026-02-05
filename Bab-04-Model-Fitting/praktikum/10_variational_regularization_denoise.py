# ============================================================
# PROGRAM: 10_variational_regularization_denoise.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Variational regularization (Tikhonov & Total Variation) untuk denoising
# 
# Tujuan Pembelajaran:
#   1. Memahami energi data + smoothness
#   2. Menerapkan regularisasi L2 (Tikhonov)
#   3. Menerapkan Total Variation (TV) sederhana
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
# Import numpy untuk operasi numerik.
import numpy as np
# Import matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# ====================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ====================
# Tentukan ukuran gambar sintetis.
IMG_H = 120
# Tentukan ukuran gambar sintetis.
IMG_W = 160
# Tentukan noise level.
NOISE_STD = 0.15
# Tentukan parameter regularisasi L2.
LAMBDA_L2 = 0.2
# Tentukan parameter regularisasi TV.
LAMBDA_TV = 0.1
# Tentukan jumlah iterasi optimasi.
NUM_ITERS = 60
# Tentukan step size gradient descent.
STEP_SIZE = 0.2
# Tentukan epsilon stabilisasi TV.
TV_EPS = 1e-3

# ====================
# FUNGSI HELPER
# ====================
# Definisikan fungsi untuk membuat gambar sintetis piecewise smooth.
def create_synthetic_image(h, w):
    # Inisialisasi gambar kosong.
    img = np.zeros((h, w), dtype=np.float32)
    # Buat blok terang di kiri atas.
    img[10:60, 15:80] = 0.8
    # Buat blok sedang di kanan bawah.
    img[70:110, 90:150] = 0.5
    # Buat gradien horizontal di tengah.
    for i in range(h):
        # Atur nilai gradien di baris i.
        img[i, :] += (np.linspace(0, 0.2, w))
    # Kembalikan gambar sintetis.
    return img

# Definisikan fungsi untuk menghitung laplacian (discrete) gambar.
def laplacian(u):
    # Hitung laplacian menggunakan perbedaan tetangga 4-arah.
    return (
        -4 * u
        + np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=1)
        + np.roll(u, -1, axis=1)
    )

# Definisikan fungsi untuk denoising L2 (Tikhonov) via gradient descent.
def denoise_l2(noisy, lam, iters, step):
    # Inisialisasi hasil dengan gambar noisy.
    u = noisy.copy()
    # Lakukan iterasi gradient descent.
    for _ in range(iters):
        # Hitung gradien energi data.
        data_grad = (u - noisy)
        # Hitung gradien energi smoothness (laplacian).
        smooth_grad = -laplacian(u)
        # Update solusi.
        u = u - step * (data_grad + lam * smooth_grad)
    # Kembalikan hasil denoise.
    return u

# Definisikan fungsi untuk denoising TV sederhana.
def denoise_tv(noisy, lam, iters, step, eps):
    # Inisialisasi hasil dengan gambar noisy.
    u = noisy.copy()
    # Lakukan iterasi gradient descent.
    for _ in range(iters):
        # Hitung gradien di sumbu x.
        ux = np.roll(u, -1, axis=1) - u
        # Hitung gradien di sumbu y.
        uy = np.roll(u, -1, axis=0) - u
        # Hitung magnitudo gradien.
        mag = np.sqrt(ux ** 2 + uy ** 2 + eps ** 2)
        # Hitung divergence dari gradien ter-normalisasi.
        div = (
            (ux / mag) - np.roll(ux / mag, 1, axis=1)
            + (uy / mag) - np.roll(uy / mag, 1, axis=0)
        )
        # Hitung gradien energi data.
        data_grad = (u - noisy)
        # Update solusi.
        u = u - step * (data_grad - lam * div)
    # Kembalikan hasil denoise.
    return u

# ====================
# PROGRAM UTAMA
# ====================
# Definisikan fungsi utama.
def main():
    # Buat gambar sintetis bersih.
    clean = create_synthetic_image(IMG_H, IMG_W)
    # Tambahkan noise Gaussian.
    noisy = clean + np.random.normal(0, NOISE_STD, size=clean.shape)
    # Clip nilai agar tetap di [0,1].
    noisy = np.clip(noisy, 0, 1)

    # Denoise dengan L2 regularization.
    denoised_l2 = denoise_l2(noisy, LAMBDA_L2, NUM_ITERS, STEP_SIZE)
    # Denoise dengan TV regularization.
    denoised_tv = denoise_tv(noisy, LAMBDA_TV, NUM_ITERS, STEP_SIZE, TV_EPS)

    # Siapkan figure untuk visualisasi.
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    # Tampilkan gambar bersih.
    axes[0].imshow(clean, cmap='gray', vmin=0, vmax=1)
    # Beri judul.
    axes[0].set_title("Clean (Ground Truth)")
    # Hilangkan axis.
    axes[0].axis('off')

    # Tampilkan gambar noisy.
    axes[1].imshow(noisy, cmap='gray', vmin=0, vmax=1)
    # Beri judul.
    axes[1].set_title("Noisy Input")
    # Hilangkan axis.
    axes[1].axis('off')

    # Tampilkan hasil L2.
    axes[2].imshow(denoised_l2, cmap='gray', vmin=0, vmax=1)
    # Beri judul.
    axes[2].set_title(f"L2 (λ={LAMBDA_L2})")
    # Hilangkan axis.
    axes[2].axis('off')

    # Tampilkan hasil TV.
    axes[3].imshow(denoised_tv, cmap='gray', vmin=0, vmax=1)
    # Beri judul.
    axes[3].set_title(f"TV (λ={LAMBDA_TV})")
    # Hilangkan axis.
    axes[3].axis('off')

    # Atur judul utama.
    plt.suptitle("Variational Regularization: L2 vs TV", fontsize=14)
    # Atur layout.
    plt.tight_layout()
    # Tampilkan plot.
    plt.show()

# Jalankan program utama jika file dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
