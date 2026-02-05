# ============================================================
# PROGRAM: 11_mrf_denoising_icm.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Denoising citra biner dengan Markov Random Field (MRF) dan ICM
# 
# Tujuan Pembelajaran:
#   1. Memahami energi data dan smoothness pada MRF
#   2. Menerapkan Iterated Conditional Modes (ICM)
#   3. Melihat efek prior smoothness pada citra biner
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
# Tentukan ukuran citra.
IMG_H = 80
# Tentukan ukuran citra.
IMG_W = 120
# Tentukan probabilitas noise (flip).
NOISE_PROB = 0.2
# Tentukan bobot data term.
DATA_WEIGHT = 2.0
# Tentukan bobot smoothness term.
SMOOTH_WEIGHT = 1.0
# Tentukan jumlah iterasi ICM.
ICM_ITERS = 10
# Tentukan seed random agar hasil konsisten.
RANDOM_SEED = 123

# ====================
# FUNGSI HELPER
# ====================
# Definisikan fungsi untuk membuat citra biner sintetis.
def create_binary_image(h, w):
    # Inisialisasi citra nol.
    img = np.zeros((h, w), dtype=np.int32)
    # Tambahkan blok putih (1) di tengah.
    img[20:60, 30:90] = 1
    # Tambahkan blok putih kecil di kanan atas.
    img[5:20, 90:110] = 1
    # Kembalikan citra biner.
    return img

# Definisikan fungsi untuk menambahkan noise flip.
def add_flip_noise(img, prob):
    # Buat mask random untuk flip.
    mask = np.random.rand(*img.shape) < prob
    # Salin citra.
    noisy = img.copy()
    # Lakukan flip pada piksel yang terkena noise.
    noisy[mask] = 1 - noisy[mask]
    # Kembalikan citra noisy.
    return noisy

# Definisikan fungsi untuk menghitung energi lokal pada piksel.
def local_energy(x, y, i, j, data_w, smooth_w):
    # Hitung energi data (kesesuaian dengan noisy).
    data_energy = data_w * (x[i, j] != y[i, j])
    # Inisialisasi energi smoothness.
    smooth_energy = 0
    # Definisikan tetangga 4-arah.
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    # Loop tetangga.
    for ni, nj in neighbors:
        # Cek batas.
        if 0 <= ni < x.shape[0] and 0 <= nj < x.shape[1]:
            # Tambahkan penalti jika berbeda.
            smooth_energy += smooth_w * (x[i, j] != x[ni, nj])
    # Kembalikan total energi lokal.
    return data_energy + smooth_energy

# Definisikan fungsi ICM untuk minimisasi energi.
def icm_denoise(noisy, data_w, smooth_w, iters):
    # Inisialisasi solusi dengan noisy.
    x = noisy.copy()
    # Lakukan iterasi ICM.
    for _ in range(iters):
        # Loop setiap piksel.
        for i in range(x.shape[0]):
            # Loop setiap kolom.
            for j in range(x.shape[1]):
                # Coba label 0.
                x[i, j] = 0
                # Hitung energi lokal untuk label 0.
                e0 = local_energy(x, noisy, i, j, data_w, smooth_w)
                # Coba label 1.
                x[i, j] = 1
                # Hitung energi lokal untuk label 1.
                e1 = local_energy(x, noisy, i, j, data_w, smooth_w)
                # Pilih label dengan energi lebih kecil.
                x[i, j] = 0 if e0 <= e1 else 1
    # Kembalikan hasil denoise.
    return x

# ====================
# PROGRAM UTAMA
# ====================
# Definisikan fungsi utama.
def main():
    # Set seed random.
    np.random.seed(RANDOM_SEED)
    # Buat citra biner bersih.
    clean = create_binary_image(IMG_H, IMG_W)
    # Tambahkan noise flip.
    noisy = add_flip_noise(clean, NOISE_PROB)
    # Denoise dengan ICM.
    denoised = icm_denoise(noisy, DATA_WEIGHT, SMOOTH_WEIGHT, ICM_ITERS)

    # Siapkan figure untuk visualisasi.
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    # Tampilkan citra bersih.
    axes[0].imshow(clean, cmap='gray')
    # Beri judul.
    axes[0].set_title("Clean")
    # Hilangkan axis.
    axes[0].axis('off')

    # Tampilkan citra noisy.
    axes[1].imshow(noisy, cmap='gray')
    # Beri judul.
    axes[1].set_title("Noisy")
    # Hilangkan axis.
    axes[1].axis('off')

    # Tampilkan hasil denoise.
    axes[2].imshow(denoised, cmap='gray')
    # Beri judul.
    axes[2].set_title("MRF + ICM")
    # Hilangkan axis.
    axes[2].axis('off')

    # Atur judul utama.
    plt.suptitle("MRF Denoising (Binary) with ICM", fontsize=14)
    # Atur layout.
    plt.tight_layout()
    # Tampilkan plot.
    plt.show()

# Jalankan program utama jika file dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
