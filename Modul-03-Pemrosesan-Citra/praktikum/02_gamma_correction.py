# ============================================================
# PROGRAM: 02_gamma_correction.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Program untuk menerapkan gamma correction pada gambar
# 
# Tujuan Pembelajaran:
#   1. Memahami konsep gamma correction
#   2. Perbedaan dengan linear brightness adjustment
#   3. Aplikasi gamma untuk koreksi pencahayaan
# ============================================================

# ====================
# IMPORT LIBRARY
# ====================
# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor modul os.
import os
# REFERENSI: Lihat CV2_FUNCTIONS_REFERENCE.py untuk dokumentasi lengkap cv2 functions


# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
# Keterangan: Inisialisasi atau perbarui variabel NAMA_FILE_GAMBAR.
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Nilai gamma
# Range: 0.1 sampai 3.0
# gamma < 1.0 = mencerahkan (lift shadows)
# gamma = 1.0 = tidak ada perubahan
# gamma > 1.0 = menggelapkan (compress highlights)
# Keterangan: Inisialisasi atau perbarui variabel GAMMA.
GAMMA = 0.5

# 3. Nilai gamma untuk perbandingan
# Keterangan: Inisialisasi atau perbarui variabel GAMMA_VALUES.
GAMMA_VALUES = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]

# ============================================================
# FUNGSI HELPER
# ============================================================

# Keterangan: Definisikan fungsi dapatkan_path_gambar.
def dapatkan_path_gambar(nama_file):
    """Mendapatkan path lengkap file gambar"""
    direktori_script = os.path.dirname(os.path.abspath(__file__))
    
    lokasi_potensial = [
        os.path.join(direktori_script, "data", "images", nama_file),
        os.path.join(direktori_script, "..", "..", "Bab-01-Pendahuluan", 
                     "data", "images", nama_file),
        os.path.join(direktori_script, nama_file),
    ]
    
    for path in lokasi_potensial:
        if os.path.exists(path):
            return path
    
    return lokasi_potensial[0]


def buat_gambar_underexposed():
    """Membuat gambar sample yang underexposed"""
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Gradient gelap
    # Keterangan: Mulai loop dengan for i in range(400).
    for i in range(400):
        # Keterangan: Mulai loop dengan for j in range(600).
        for j in range(600):
            # Keterangan: Inisialisasi beberapa variabel (gambar[i, j]).
            gambar[i, j] = [
                # Keterangan: Jalankan perintah berikut.
                int(20 + i/10),
                # Keterangan: Jalankan perintah berikut.
                int(30 + j/15),
                # Keterangan: Jalankan perintah berikut.
                int(40 + i/8)
            # Keterangan: Jalankan perintah berikut.
            ]
    
    # Objek
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (200, 150), (30, 40, 80), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (400, 200), 80, (60, 70, 50), -1)
    # Keterangan: Tambahkan teks ke gambar (image, text, org, font, fontScale, color, thickness, lineType).
    cv2.putText(gambar, "DARK", (220, 350), 
                # Keterangan: Jalankan perintah berikut.
                cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 80, 80), 3)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# ============================================================
# FUNGSI GAMMA CORRECTION
# ============================================================

# Keterangan: Definisikan fungsi gamma_correction.
def gamma_correction(gambar, gamma):
    """
    Menerapkan gamma correction pada gambar
    
    Formula: output = (input / 255)^gamma * 255
    
    Parameter:
    - gambar: input image (BGR, 0-255)
    - gamma: nilai gamma
            < 1.0 = brighten (lift shadows)
            = 1.0 = no change
            > 1.0 = darken (compress highlights)
    
    Return:
    - gambar dengan gamma correction
    """
    # Normalisasi ke range [0, 1]
    # Keterangan: Inisialisasi atau perbarui variabel gambar_normalized.
    gambar_normalized = gambar / 255.0
    
    # Terapkan gamma
    # Keterangan: Inisialisasi atau perbarui variabel gambar_gamma.
    gambar_gamma = np.power(gambar_normalized, gamma)
    
    # Kembalikan ke range [0, 255]
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = np.uint8(gambar_gamma * 255)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi gamma_correction_lut.
def gamma_correction_lut(gambar, gamma):
    """
    Gamma correction menggunakan Look-Up Table (LUT)
    Lebih cepat untuk gambar besar
    
    Parameter:
    - gambar: input image
    - gamma: nilai gamma
    
    Return:
    - gambar dengan gamma correction
    """
    # Buat LUT
    # Keterangan: Inisialisasi atau perbarui variabel inv_gamma.
    inv_gamma = 1.0 / gamma
    # Keterangan: Inisialisasi atau perbarui variabel lut.
    lut = np.array([((i / 255.0) ** inv_gamma) * 255 
                    # Keterangan: Buat range angka berjarak tetap.
                    for i in np.arange(0, 256)]).astype(np.uint8)
    
    # Terapkan LUT
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = cv2.LUT(gambar, lut)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil


# Keterangan: Definisikan fungsi auto_gamma_correction.
def auto_gamma_correction(gambar, target_mean=128):
    """
    Menghitung gamma secara otomatis berdasarkan brightness target
    
    Parameter:
    - gambar: input image
    - target_mean: target mean brightness (0-255)
    
    Return:
    - gambar dengan gamma correction otomatis
    - nilai gamma yang digunakan
    """
    # Hitung mean brightness saat ini
    # Keterangan: Konversi ruang warna gambar.
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Inisialisasi atau perbarui variabel current_mean.
    current_mean = np.mean(gray)
    
    # Keterangan: Cek kondisi current_mean == 0.
    if current_mean == 0:
        # Keterangan: Inisialisasi atau perbarui variabel current_mean.
        current_mean = 1
    
    # Hitung gamma yang diperlukan
    # target = current ^ gamma
    # gamma = log(target) / log(current)
    # Keterangan: Inisialisasi atau perbarui variabel normalized_current.
    normalized_current = current_mean / 255.0
    # Keterangan: Inisialisasi atau perbarui variabel normalized_target.
    normalized_target = target_mean / 255.0
    
    # Keterangan: Cek kondisi normalized_current > 0 and normalized_target > 0.
    if normalized_current > 0 and normalized_target > 0:
        # Keterangan: Inisialisasi atau perbarui variabel gamma.
        gamma = np.log(normalized_target) / np.log(normalized_current)
        # Batasi gamma ke range yang reasonable
        # Keterangan: Inisialisasi atau perbarui variabel gamma.
        gamma = np.clip(gamma, 0.1, 3.0)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gamma.
        gamma = 1.0
    
    # Keterangan: Inisialisasi atau perbarui variabel hasil.
    hasil = gamma_correction(gambar, gamma)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return hasil, gamma


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_gamma_curve.
def demo_gamma_curve():
    """
    Visualisasi kurva transfer gamma
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("VISUALISASI KURVA GAMMA")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
GAMMA CORRECTION:
Formula: output = input^gamma (untuk input normalized ke [0,1])

├── gamma < 1 : Kurva di atas diagonal
│              → Nilai rendah dinaikkan lebih banyak
│              → Mencerahkan shadows
│
├── gamma = 1 : Diagonal (tidak ada perubahan)
│
└── gamma > 1 : Kurva di bawah diagonal
               → Nilai tinggi diturunkan lebih banyak
               → Menggelapkan highlights
    """)
    
    # Input values
    # Keterangan: Buat range angka berjarak linier.
    x = np.linspace(0, 1, 256)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot untuk berbagai gamma
    # Keterangan: Inisialisasi atau perbarui variabel gamma_values.
    gamma_values = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]
    # Keterangan: Buat range angka berjarak linier.
    colors = plt.cm.viridis(np.linspace(0, 1, len(gamma_values)))
    
    # Keterangan: Mulai loop dengan for gamma, color in zip(gamma_values, colors).
    for gamma, color in zip(gamma_values, colors):
        # Keterangan: Inisialisasi atau perbarui variabel y.
        y = np.power(x, gamma)
        # Keterangan: Jalankan perintah berikut.
        style = '--' if gamma < 1 else ('-' if gamma == 1 else ':')
        # Keterangan: Inisialisasi beberapa variabel (ax.plot(x, y, color).
        ax.plot(x, y, color=color, linewidth=2, label=f'γ = {gamma}')
    
    # Diagonal reference
    # Keterangan: Inisialisasi beberapa variabel (ax.plot([0, 1], [0, 1], 'k--', alpha).
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='γ = 1 (linear)')
    
    # Keterangan: Jalankan perintah berikut.
    ax.set_xlabel('Input Intensity (normalized)')
    # Keterangan: Jalankan perintah berikut.
    ax.set_ylabel('Output Intensity (normalized)')
    # Keterangan: Jalankan perintah berikut.
    ax.set_title('Gamma Transfer Curves')
    # Keterangan: Inisialisasi atau perbarui variabel ax.legend(loc.
    ax.legend(loc='lower right')
    # Keterangan: Inisialisasi beberapa variabel (ax.grid(True, alpha).
    ax.grid(True, alpha=0.3)
    # Keterangan: Jalankan perintah berikut.
    ax.set_aspect('equal')
    # Keterangan: Jalankan perintah berikut.
    ax.set_xlim(0, 1)
    # Keterangan: Jalankan perintah berikut.
    ax.set_ylim(0, 1)
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_berbagai_gamma.
def demo_berbagai_gamma():
    """
    Demonstrasi efek berbagai nilai gamma
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMONSTRASI BERBAGAI NILAI GAMMA")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    # Load gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Jalankan perintah berikut.
        print("[INFO] Menggunakan gambar underexposed sample...")
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_underexposed()
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    # Keterangan: Inisialisasi atau perbarui variabel axes.
    axes = axes.flatten()
    
    # Keterangan: Mulai loop dengan for i, gamma in enumerate(GAMMA_VALUES).
    for i, gamma in enumerate(GAMMA_VALUES):
        # Keterangan: Inisialisasi atau perbarui variabel hasil.
        hasil = gamma_correction(gambar, gamma)
        
        # Keterangan: Konversi ruang warna gambar.
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        # Keterangan: Inisialisasi atau perbarui variabel axes[i].set_title(f"γ.
        axes[i].set_title(f"γ = {gamma}")
        # Keterangan: Jalankan perintah berikut.
        axes[i].axis('off')
        
        # Info mean brightness
        # Keterangan: Inisialisasi atau perbarui variabel mean_val.
        mean_val = np.mean(hasil)
        # Keterangan: Jalankan perintah berikut.
        axes[i].text(0.5, -0.1, f"Mean: {mean_val:.1f}", 
                     # Keterangan: Inisialisasi atau perbarui variabel transform.
                     transform=axes[i].transAxes, ha='center')
    
    # Histogram comparison
    # Keterangan: Inisialisasi beberapa variabel (axes[7].hist(gambar.ravel(), 256, [0, 256], alpha).
    axes[7].hist(gambar.ravel(), 256, [0, 256], alpha=0.5, label='Original (γ=1)')
    # Keterangan: Jalankan perintah berikut.
    axes[7].hist(gamma_correction(gambar, 0.5).ravel(), 256, [0, 256], 
                 # Keterangan: Inisialisasi atau perbarui variabel alpha.
                 alpha=0.5, label='γ=0.5 (brighter)')
    # Keterangan: Jalankan perintah berikut.
    axes[7].hist(gamma_correction(gambar, 2.0).ravel(), 256, [0, 256], 
                 # Keterangan: Inisialisasi atau perbarui variabel alpha.
                 alpha=0.5, label='γ=2.0 (darker)')
    # Keterangan: Jalankan perintah berikut.
    axes[7].legend()
    # Keterangan: Jalankan perintah berikut.
    axes[7].set_title("Histogram Comparison")
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Efek Berbagai Nilai Gamma", fontsize).
    plt.suptitle("Efek Berbagai Nilai Gamma", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_gamma_vs_brightness.
def demo_gamma_vs_brightness():
    """
    Perbandingan gamma correction vs linear brightness adjustment
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("GAMMA CORRECTION vs LINEAR BRIGHTNESS")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
PERBEDAAN:

LINEAR BRIGHTNESS (additive):
├── Formula: output = input + beta
├── Menambah nilai yang sama ke semua piksel
├── Shadows dan highlights bergeser sama
└── Dapat menyebabkan clipping

GAMMA CORRECTION (multiplicative/power):
├── Formula: output = input^gamma
├── Efek berbeda pada nilai berbeda
├── Mempertahankan relative differences
└── Tidak ada clipping pada range [0,1]
    """)
    
    # Buat gambar gradient untuk perbandingan
    # Keterangan: Inisialisasi array bernilai nol.
    gradient = np.zeros((100, 400, 3), dtype=np.uint8)
    # Keterangan: Mulai loop dengan for j in range(400).
    for j in range(400):
        # Keterangan: Inisialisasi beberapa variabel (gradient[:, j]).
        gradient[:, j] = [int(j * 255 / 400)] * 3
    
    # Original
    # Keterangan: Inisialisasi atau perbarui variabel original.
    original = gradient.copy()
    
    # Gamma 0.5 (brighten)
    # Keterangan: Inisialisasi atau perbarui variabel gamma_bright.
    gamma_bright = gamma_correction(gradient, 0.5)
    
    # Linear brightness +50
    # Keterangan: Inisialisasi atau perbarui variabel linear_bright.
    linear_bright = cv2.convertScaleAbs(gradient, alpha=1.0, beta=50)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # Baris 1: Gambar
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title("Original Gradient")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(gamma_bright, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].set_title("Gamma γ).
    axes[0, 1].set_title("Gamma γ=0.5")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 2].imshow(cv2.cvtColor(linear_bright, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title("Linear +50")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Baris 2: Profile plot
    # Keterangan: Buat range angka berjarak tetap.
    x = np.arange(400)
    # Keterangan: Inisialisasi atau perbarui variabel orig_profile.
    orig_profile = original[50, :, 0]
    # Keterangan: Inisialisasi atau perbarui variabel gamma_profile.
    gamma_profile = gamma_bright[50, :, 0]
    # Keterangan: Inisialisasi atau perbarui variabel linear_profile.
    linear_profile = linear_bright[50, :, 0]
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].plot(x, orig_profile, 'b-', label).
    axes[1, 0].plot(x, orig_profile, 'b-', label='Original')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Original Profile")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_ylim(0, 280)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].legend()
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].plot(x, orig_profile, 'b-', alpha).
    axes[1, 1].plot(x, orig_profile, 'b-', alpha=0.3, label='Original')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].plot(x, gamma_profile, 'r-', label).
    axes[1, 1].plot(x, gamma_profile, 'r-', label='Gamma')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Gamma: Shadows lifted more")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_ylim(0, 280)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].legend()
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].plot(x, orig_profile, 'b-', alpha).
    axes[1, 2].plot(x, orig_profile, 'b-', alpha=0.3, label='Original')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].plot(x, linear_profile, 'g-', label).
    axes[1, 2].plot(x, linear_profile, 'g-', label='Linear')
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].axhline(y).
    axes[1, 2].axhline(y=255, color='red', linestyle='--', alpha=0.5, label='Clip')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Linear: Uniform shift, clipping")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_ylim(0, 280)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].legend()
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Perbandingan Gamma vs Linear Brightness", fontsize).
    plt.suptitle("Perbandingan Gamma vs Linear Brightness", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_auto_gamma.
def demo_auto_gamma():
    """
    Demonstrasi auto gamma correction
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("AUTO GAMMA CORRECTION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
Auto gamma secara otomatis menghitung nilai gamma
yang diperlukan untuk mencapai target brightness.

Berguna untuk:
├── Menormalkan gambar dari berbagai sumber
├── Batch processing gambar dengan exposure berbeda
└── Preprocessing untuk algoritma CV
    """)
    
    # Buat gambar dengan berbagai exposure
    # Keterangan: Inisialisasi atau perbarui variabel gambar_gelap.
    gambar_gelap = buat_gambar_underexposed()
    
    # Gambar terang (overexposed simulation)
    # Keterangan: Inisialisasi atau perbarui variabel gambar_terang.
    gambar_terang = cv2.convertScaleAbs(gambar_gelap, alpha=3.0, beta=50)
    
    # Auto gamma
    # Keterangan: Inisialisasi beberapa variabel (hasil_gelap, gamma_gelap).
    hasil_gelap, gamma_gelap = auto_gamma_correction(gambar_gelap, target_mean=128)
    # Keterangan: Inisialisasi beberapa variabel (hasil_terang, gamma_terang).
    hasil_terang, gamma_terang = auto_gamma_correction(gambar_terang, target_mean=128)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 0].imshow(cv2.cvtColor(gambar_gelap, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi atau perbarui variabel mean_orig.
    mean_orig = np.mean(gambar_gelap)
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].set_title(f"Underexposed\nMean: {mean_orig:.1f}")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0, 1].imshow(cv2.cvtColor(hasil_gelap, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi atau perbarui variabel mean_corr.
    mean_corr = np.mean(hasil_gelap)
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].set_title(f"Auto Corrected (γ).
    axes[0, 1].set_title(f"Auto Corrected (γ={gamma_gelap:.2f})\nMean: {mean_corr:.1f}")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 0].imshow(cv2.cvtColor(gambar_terang, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi atau perbarui variabel mean_orig2.
    mean_orig2 = np.mean(gambar_terang)
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title(f"Overexposed\nMean: {mean_orig2:.1f}")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1, 1].imshow(cv2.cvtColor(hasil_terang, cv2.COLOR_BGR2RGB))
    # Keterangan: Inisialisasi atau perbarui variabel mean_corr2.
    mean_corr2 = np.mean(hasil_terang)
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].set_title(f"Auto Corrected (γ).
    axes[1, 1].set_title(f"Auto Corrected (γ={gamma_terang:.2f})\nMean: {mean_corr2:.1f}")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi atau perbarui variabel plt.suptitle("Auto Gamma Correction (Target Mean.
    plt.suptitle("Auto Gamma Correction (Target Mean = 128)", fontsize=14)
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_lut_performance.
def demo_lut_performance():
    """
    Perbandingan performa implementasi gamma
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PERBANDINGAN PERFORMA IMPLEMENTASI")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    # Keterangan: Impor modul time.
    import time
    
    # Buat gambar besar
    # Keterangan: Inisialisasi atau perbarui variabel gambar.
    gambar = np.random.randint(0, 256, (1000, 1000, 3), dtype=np.uint8)
    
    # Test direct implementation
    # Keterangan: Inisialisasi atau perbarui variabel start.
    start = time.time()
    # Keterangan: Mulai loop dengan for _ in range(10).
    for _ in range(10):
        # Keterangan: Inisialisasi atau perbarui variabel _.
        _ = gamma_correction(gambar, 0.5)
    # Keterangan: Inisialisasi atau perbarui variabel time_direct.
    time_direct = (time.time() - start) / 10
    
    # Test LUT implementation
    # Keterangan: Inisialisasi atau perbarui variabel start.
    start = time.time()
    # Keterangan: Mulai loop dengan for _ in range(10).
    for _ in range(10):
        # Keterangan: Inisialisasi atau perbarui variabel _.
        _ = gamma_correction_lut(gambar, 0.5)
    # Keterangan: Inisialisasi atau perbarui variabel time_lut.
    time_lut = (time.time() - start) / 10
    
    print(f"""
Ukuran gambar: 1000×1000×3

Waktu rata-rata (10 iterasi):
├── Direct implementation: {time_direct*1000:.2f} ms
└── LUT implementation:    {time_lut*1000:.2f} ms

Speed up: {time_direct/time_lut:.2f}x
    
KESIMPULAN:
LUT (Look-Up Table) jauh lebih cepat karena:
├── Pre-compute semua transformasi untuk 256 nilai
└── Hanya melakukan table lookup per piksel
    """)


# ============================================================
# PROGRAM UTAMA
# ============================================================

# Keterangan: Definisikan fungsi main.
def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: GAMMA CORRECTION")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
# Keterangan: Jalankan perintah berikut.
GAMMA CORRECTION adalah teknik non-linear untuk
# Keterangan: Jalankan perintah berikut.
menyesuaikan brightness gambar dengan mempertahankan
# Keterangan: Jalankan perintah berikut.
relative differences antar piksel.

# Keterangan: Mulai blok kode baru.
Aplikasi:
# Keterangan: Jalankan perintah berikut.
├── Koreksi pencahayaan (exposure correction)
# Keterangan: Jalankan perintah berikut.
├── Display calibration (gamma 2.2)
# Keterangan: Jalankan perintah berikut.
├── HDR tone mapping
# Keterangan: Jalankan perintah berikut.
└── Medical imaging enhancement
    """)
    
    # Load atau buat gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    if os.path.exists(path_gambar):
        print(f"[INFO] Memuat gambar: {path_gambar}")
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Membuat gambar underexposed sample...")
        gambar = buat_gambar_underexposed()
    
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    print(f"[INFO] Gamma value: {GAMMA}")
    
    # Terapkan gamma correction
    hasil = gamma_correction(gambar, GAMMA)
    
    # Tampilkan hasil
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"Original\nMean: {np.mean(gambar):.1f}")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Gamma Corrected (γ={GAMMA})\nMean: {np.mean(hasil):.1f}")
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Demo tambahan
    demo_gamma_curve()
    demo_berbagai_gamma()
    demo_gamma_vs_brightness()
    demo_auto_gamma()
    demo_lut_performance()
    
    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN GAMMA CORRECTION")
    print("=" * 60)
    print("""
# Keterangan: Mulai blok kode baru.
FORMULA:
    # Keterangan: Inisialisasi atau perbarui variabel output.
    output = (input / 255)^gamma * 255
    
    # Keterangan: Mulai blok kode baru.
    atau untuk inverse gamma:
    # Keterangan: Inisialisasi atau perbarui variabel output.
    output = (input / 255)^(1/gamma) * 255

# Keterangan: Mulai blok kode baru.
IMPLEMENTASI OPENCV:
    # Menggunakan LUT untuk performa optimal
    # Keterangan: Inisialisasi atau perbarui variabel inv_gamma.
    inv_gamma = 1.0 / gamma
    # Keterangan: Inisialisasi atau perbarui variabel lut.
    lut = np.array([((i/255.0)**inv_gamma)*255 for i in range(256)])
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = cv2.LUT(image, lut.astype(np.uint8))

# Keterangan: Mulai blok kode baru.
NILAI GAMMA UMUM:
# Keterangan: Inisialisasi atau perbarui variabel ├── γ.
├── γ = 0.45 : sRGB encoding (compress for storage)
# Keterangan: Inisialisasi atau perbarui variabel ├── γ.
├── γ = 2.2  : sRGB decoding (expand for display)
# Keterangan: Jalankan perintah berikut.
├── γ < 1    : Brighten (lift shadows)
# Keterangan: Jalankan perintah berikut.
└── γ > 1    : Darken (compress highlights)

# Keterangan: Mulai blok kode baru.
TIPS:
# Keterangan: Jalankan perintah berikut.
1. Gunakan LUT untuk gambar besar
# Keterangan: Jalankan perintah berikut.
2. Gamma 0.4-0.7 untuk brighten underexposed images
# Keterangan: Jalankan perintah berikut.
3. Gamma 1.5-2.5 untuk darken overexposed images
# Keterangan: Jalankan perintah berikut.
4. Kombinasikan dengan contrast adjustment untuk hasil optimal
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
