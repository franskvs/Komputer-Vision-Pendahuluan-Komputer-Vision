# ============================================================
# PROGRAM: 09_scattered_interpolation_rbf.py
# PRAKTIKUM COMPUTER VISION - BAB 4: MODEL FITTING
# ============================================================
# Deskripsi: Scattered data interpolation dengan Radial Basis Function (RBF)
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep scattered data interpolation
#   2. Menerapkan RBF untuk fitting data tak beraturan
#   3. Melihat efek overfitting dan underfitting (regularisasi)
#   4. Menerapkan robust fitting (Huber loss dengan IRLS)
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
# Import numpy untuk operasi numerik dan array.
import numpy as np
# Import matplotlib untuk visualisasi hasil.
import matplotlib.pyplot as plt

# ====================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ====================
# Tentukan jumlah sampel data acak.
NUM_SAMPLES = 40
# Tentukan jumlah titik evaluasi pada grid.
NUM_GRID = 200
# Tentukan parameter lebar kernel Gaussian.
RBF_SIGMA = 0.3
# Tentukan daftar regularisasi untuk melihat under/overfitting.
LAMBDA_LIST = [0.0, 0.01, 0.1, 1.0]
# Tentukan nilai delta untuk Huber loss.
HUBER_DELTA = 0.3
# Tentukan jumlah iterasi IRLS untuk robust fitting.
IRLS_ITER = 10
# Tentukan level noise pada data.
NOISE_STD = 0.15
# Tentukan jumlah outlier yang ditambahkan.
NUM_OUTLIERS = 6
# Tentukan seed random agar hasil konsisten.
RANDOM_SEED = 42

# ====================
# FUNGSI HELPER
# ====================
# Definisikan fungsi ground truth yang akan di-sample.
def ground_truth(x):
    # Kembalikan kombinasi sin dan polinomial agar bentuk kaya.
    return np.sin(2 * np.pi * x) + 0.3 * x

# Definisikan fungsi kernel Gaussian RBF.
def rbf_kernel(x1, x2, sigma):
    # Hitung jarak kuadrat antar titik.
    dist2 = (x1[:, None] - x2[None, :]) ** 2
    # Kembalikan kernel Gaussian berdasarkan dist2.
    return np.exp(-dist2 / (2 * sigma ** 2))

# Definisikan fungsi untuk membangun model RBF dengan regularisasi L2.
def fit_rbf_l2(x_train, y_train, x_centers, sigma, lam):
    # Bangun matriks basis (Phi).
    phi = rbf_kernel(x_train, x_centers, sigma)
    # Bangun matriks regularisasi (lambda * I).
    reg = lam * np.eye(phi.shape[1])
    # Selesaikan sistem linear untuk bobot.
    weights = np.linalg.solve(phi.T @ phi + reg, phi.T @ y_train)
    # Kembalikan bobot model.
    return weights

# Definisikan fungsi untuk fitting RBF dengan Huber loss via IRLS.
def fit_rbf_huber_irls(x_train, y_train, x_centers, sigma, lam, delta, iters):
    # Bangun matriks basis (Phi).
    phi = rbf_kernel(x_train, x_centers, sigma)
    # Inisialisasi bobot dengan solusi L2.
    weights = fit_rbf_l2(x_train, y_train, x_centers, sigma, lam)
    # Lakukan iterasi IRLS.
    for _ in range(iters):
        # Hitung residual untuk tiap sampel.
        residual = phi @ weights - y_train
        # Hitung bobot IRLS berbasis Huber.
        w = np.ones_like(residual)
        # Identifikasi residual besar (outlier).
        mask = np.abs(residual) > delta
        # Terapkan bobot robust untuk residual besar.
        w[mask] = delta / (np.abs(residual[mask]) + 1e-12)
        # Bentuk matriks bobot diagonal.
        W = np.diag(w)
        # Selesaikan sistem weighted least squares.
        weights = np.linalg.solve(phi.T @ W @ phi + lam * np.eye(phi.shape[1]), phi.T @ W @ y_train)
    # Kembalikan bobot robust.
    return weights

# Definisikan fungsi untuk prediksi nilai dengan model RBF.
def predict_rbf(x_query, x_centers, sigma, weights):
    # Bangun matriks basis untuk query.
    phi = rbf_kernel(x_query, x_centers, sigma)
    # Hitung prediksi y.
    y_pred = phi @ weights
    # Kembalikan hasil prediksi.
    return y_pred

# ====================
# PROGRAM UTAMA
# ====================
# Definisikan fungsi utama.
def main():
    # Set seed random agar hasil konsisten.
    np.random.seed(RANDOM_SEED)

    # Buat sampel x acak di rentang [0, 1].
    x_train = np.sort(np.random.rand(NUM_SAMPLES))
    # Hitung nilai ground truth pada x_train.
    y_true = ground_truth(x_train)
    # Tambahkan noise Gaussian pada data.
    y_train = y_true + np.random.normal(0, NOISE_STD, size=y_true.shape)

    # Tambahkan outlier secara acak.
    outlier_idx = np.random.choice(NUM_SAMPLES, NUM_OUTLIERS, replace=False)
    # Tambahkan gangguan besar pada titik outlier.
    y_train[outlier_idx] += np.random.normal(0, 1.0, size=NUM_OUTLIERS)

    # Tentukan centers RBF di grid yang sama dengan x_train.
    x_centers = x_train.copy()

    # Buat grid halus untuk evaluasi model.
    x_grid = np.linspace(0, 1, NUM_GRID)
    # Hitung ground truth pada grid.
    y_grid_true = ground_truth(x_grid)

    # Siapkan figure untuk perbandingan regularisasi.
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    # Flatten axes agar mudah diiterasi.
    axes = axes.flatten()

    # Loop untuk setiap nilai regularisasi.
    for i, lam in enumerate(LAMBDA_LIST):
        # Fit model RBF dengan L2.
        w_l2 = fit_rbf_l2(x_train, y_train, x_centers, RBF_SIGMA, lam)
        # Prediksi pada grid.
        y_pred = predict_rbf(x_grid, x_centers, RBF_SIGMA, w_l2)
        # Plot ground truth dan hasil fitting.
        axes[i].plot(x_grid, y_grid_true, 'g--', label='Ground Truth')
        # Plot hasil prediksi.
        axes[i].plot(x_grid, y_pred, 'b-', label=f'RBF L2 (λ={lam})')
        # Plot titik data dengan noise.
        axes[i].scatter(x_train, y_train, c='r', s=25, label='Samples', alpha=0.7)
        # Tandai outlier dengan warna berbeda.
        axes[i].scatter(x_train[outlier_idx], y_train[outlier_idx], c='k', s=40, label='Outliers')
        # Atur judul subplot.
        axes[i].set_title(f'Regularisasi λ = {lam}')
        # Atur legenda.
        axes[i].legend()
        # Atur grid untuk visualisasi.
        axes[i].grid(True, alpha=0.3)

    # Atur judul utama.
    plt.suptitle('Scattered Data Interpolation dengan RBF (L2 Regularization)', fontsize=14)
    # Atur layout agar rapi.
    plt.tight_layout()
    # Tampilkan plot.
    plt.show()

    # Fit model robust dengan Huber loss.
    w_huber = fit_rbf_huber_irls(x_train, y_train, x_centers, RBF_SIGMA, 0.01, HUBER_DELTA, IRLS_ITER)
    # Prediksi pada grid menggunakan model robust.
    y_pred_huber = predict_rbf(x_grid, x_centers, RBF_SIGMA, w_huber)

    # Siapkan figure perbandingan robust vs L2.
    plt.figure(figsize=(10, 6))
    # Plot ground truth.
    plt.plot(x_grid, y_grid_true, 'g--', label='Ground Truth')
    # Plot hasil L2 (λ kecil).
    w_l2 = fit_rbf_l2(x_train, y_train, x_centers, RBF_SIGMA, 0.01)
    # Prediksi dengan L2.
    y_pred_l2 = predict_rbf(x_grid, x_centers, RBF_SIGMA, w_l2)
    # Plot L2.
    plt.plot(x_grid, y_pred_l2, 'b-', label='RBF L2 (λ=0.01)')
    # Plot Huber IRLS.
    plt.plot(x_grid, y_pred_huber, 'm-', label='RBF Huber (IRLS)')
    # Plot data sampel.
    plt.scatter(x_train, y_train, c='r', s=25, label='Samples', alpha=0.7)
    # Plot outlier.
    plt.scatter(x_train[outlier_idx], y_train[outlier_idx], c='k', s=40, label='Outliers')
    # Atur judul plot.
    plt.title('Robust Fitting: Huber vs L2')
    # Atur legenda.
    plt.legend()
    # Atur grid.
    plt.grid(True, alpha=0.3)
    # Tampilkan plot.
    plt.show()

# Jalankan program utama jika file dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
