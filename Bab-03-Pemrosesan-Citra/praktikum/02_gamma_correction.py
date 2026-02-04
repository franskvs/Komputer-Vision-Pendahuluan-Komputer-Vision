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
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Nilai gamma
# Range: 0.1 sampai 3.0
# gamma < 1.0 = mencerahkan (lift shadows)
# gamma = 1.0 = tidak ada perubahan
# gamma > 1.0 = menggelapkan (compress highlights)
GAMMA = 0.5

# 3. Nilai gamma untuk perbandingan
GAMMA_VALUES = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]

# ============================================================
# FUNGSI HELPER
# ============================================================

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
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Gradient gelap
    for i in range(400):
        for j in range(600):
            gambar[i, j] = [
                int(20 + i/10),
                int(30 + j/15),
                int(40 + i/8)
            ]
    
    # Objek
    cv2.rectangle(gambar, (50, 50), (200, 150), (30, 40, 80), -1)
    cv2.circle(gambar, (400, 200), 80, (60, 70, 50), -1)
    cv2.putText(gambar, "DARK", (220, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (80, 80, 80), 3)
    
    return gambar


# ============================================================
# FUNGSI GAMMA CORRECTION
# ============================================================

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
    gambar_normalized = gambar / 255.0
    
    # Terapkan gamma
    gambar_gamma = np.power(gambar_normalized, gamma)
    
    # Kembalikan ke range [0, 255]
    hasil = np.uint8(gambar_gamma * 255)
    
    return hasil


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
    inv_gamma = 1.0 / gamma
    lut = np.array([((i / 255.0) ** inv_gamma) * 255 
                    for i in np.arange(0, 256)]).astype(np.uint8)
    
    # Terapkan LUT
    hasil = cv2.LUT(gambar, lut)
    
    return hasil


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
    gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    current_mean = np.mean(gray)
    
    if current_mean == 0:
        current_mean = 1
    
    # Hitung gamma yang diperlukan
    # target = current ^ gamma
    # gamma = log(target) / log(current)
    normalized_current = current_mean / 255.0
    normalized_target = target_mean / 255.0
    
    if normalized_current > 0 and normalized_target > 0:
        gamma = np.log(normalized_target) / np.log(normalized_current)
        # Batasi gamma ke range yang reasonable
        gamma = np.clip(gamma, 0.1, 3.0)
    else:
        gamma = 1.0
    
    hasil = gamma_correction(gambar, gamma)
    
    return hasil, gamma


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_gamma_curve():
    """
    Visualisasi kurva transfer gamma
    """
    print("\n" + "=" * 60)
    print("VISUALISASI KURVA GAMMA")
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
    x = np.linspace(0, 1, 256)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot untuk berbagai gamma
    gamma_values = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]
    colors = plt.cm.viridis(np.linspace(0, 1, len(gamma_values)))
    
    for gamma, color in zip(gamma_values, colors):
        y = np.power(x, gamma)
        style = '--' if gamma < 1 else ('-' if gamma == 1 else ':')
        ax.plot(x, y, color=color, linewidth=2, label=f'γ = {gamma}')
    
    # Diagonal reference
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='γ = 1 (linear)')
    
    ax.set_xlabel('Input Intensity (normalized)')
    ax.set_ylabel('Output Intensity (normalized)')
    ax.set_title('Gamma Transfer Curves')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.show()


def demo_berbagai_gamma():
    """
    Demonstrasi efek berbagai nilai gamma
    """
    print("\n" + "=" * 60)
    print("DEMONSTRASI BERBAGAI NILAI GAMMA")
    print("=" * 60)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        print("[INFO] Menggunakan gambar underexposed sample...")
        gambar = buat_gambar_underexposed()
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    for i, gamma in enumerate(GAMMA_VALUES):
        hasil = gamma_correction(gambar, gamma)
        
        axes[i].imshow(cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"γ = {gamma}")
        axes[i].axis('off')
        
        # Info mean brightness
        mean_val = np.mean(hasil)
        axes[i].text(0.5, -0.1, f"Mean: {mean_val:.1f}", 
                     transform=axes[i].transAxes, ha='center')
    
    # Histogram comparison
    axes[7].hist(gambar.ravel(), 256, [0, 256], alpha=0.5, label='Original (γ=1)')
    axes[7].hist(gamma_correction(gambar, 0.5).ravel(), 256, [0, 256], 
                 alpha=0.5, label='γ=0.5 (brighter)')
    axes[7].hist(gamma_correction(gambar, 2.0).ravel(), 256, [0, 256], 
                 alpha=0.5, label='γ=2.0 (darker)')
    axes[7].legend()
    axes[7].set_title("Histogram Comparison")
    
    plt.suptitle("Efek Berbagai Nilai Gamma", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_gamma_vs_brightness():
    """
    Perbandingan gamma correction vs linear brightness adjustment
    """
    print("\n" + "=" * 60)
    print("GAMMA CORRECTION vs LINEAR BRIGHTNESS")
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
    gradient = np.zeros((100, 400, 3), dtype=np.uint8)
    for j in range(400):
        gradient[:, j] = [int(j * 255 / 400)] * 3
    
    # Original
    original = gradient.copy()
    
    # Gamma 0.5 (brighten)
    gamma_bright = gamma_correction(gradient, 0.5)
    
    # Linear brightness +50
    linear_bright = cv2.convertScaleAbs(gradient, alpha=1.0, beta=50)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # Baris 1: Gambar
    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original Gradient")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(gamma_bright, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Gamma γ=0.5")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(linear_bright, cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title("Linear +50")
    axes[0, 2].axis('off')
    
    # Baris 2: Profile plot
    x = np.arange(400)
    orig_profile = original[50, :, 0]
    gamma_profile = gamma_bright[50, :, 0]
    linear_profile = linear_bright[50, :, 0]
    
    axes[1, 0].plot(x, orig_profile, 'b-', label='Original')
    axes[1, 0].set_title("Original Profile")
    axes[1, 0].set_ylim(0, 280)
    axes[1, 0].legend()
    
    axes[1, 1].plot(x, orig_profile, 'b-', alpha=0.3, label='Original')
    axes[1, 1].plot(x, gamma_profile, 'r-', label='Gamma')
    axes[1, 1].set_title("Gamma: Shadows lifted more")
    axes[1, 1].set_ylim(0, 280)
    axes[1, 1].legend()
    
    axes[1, 2].plot(x, orig_profile, 'b-', alpha=0.3, label='Original')
    axes[1, 2].plot(x, linear_profile, 'g-', label='Linear')
    axes[1, 2].axhline(y=255, color='red', linestyle='--', alpha=0.5, label='Clip')
    axes[1, 2].set_title("Linear: Uniform shift, clipping")
    axes[1, 2].set_ylim(0, 280)
    axes[1, 2].legend()
    
    plt.suptitle("Perbandingan Gamma vs Linear Brightness", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_auto_gamma():
    """
    Demonstrasi auto gamma correction
    """
    print("\n" + "=" * 60)
    print("AUTO GAMMA CORRECTION")
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
    gambar_gelap = buat_gambar_underexposed()
    
    # Gambar terang (overexposed simulation)
    gambar_terang = cv2.convertScaleAbs(gambar_gelap, alpha=3.0, beta=50)
    
    # Auto gamma
    hasil_gelap, gamma_gelap = auto_gamma_correction(gambar_gelap, target_mean=128)
    hasil_terang, gamma_terang = auto_gamma_correction(gambar_terang, target_mean=128)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(gambar_gelap, cv2.COLOR_BGR2RGB))
    mean_orig = np.mean(gambar_gelap)
    axes[0, 0].set_title(f"Underexposed\nMean: {mean_orig:.1f}")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(hasil_gelap, cv2.COLOR_BGR2RGB))
    mean_corr = np.mean(hasil_gelap)
    axes[0, 1].set_title(f"Auto Corrected (γ={gamma_gelap:.2f})\nMean: {mean_corr:.1f}")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(gambar_terang, cv2.COLOR_BGR2RGB))
    mean_orig2 = np.mean(gambar_terang)
    axes[1, 0].set_title(f"Overexposed\nMean: {mean_orig2:.1f}")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(hasil_terang, cv2.COLOR_BGR2RGB))
    mean_corr2 = np.mean(hasil_terang)
    axes[1, 1].set_title(f"Auto Corrected (γ={gamma_terang:.2f})\nMean: {mean_corr2:.1f}")
    axes[1, 1].axis('off')
    
    plt.suptitle("Auto Gamma Correction (Target Mean = 128)", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_lut_performance():
    """
    Perbandingan performa implementasi gamma
    """
    print("\n" + "=" * 60)
    print("PERBANDINGAN PERFORMA IMPLEMENTASI")
    print("=" * 60)
    
    import time
    
    # Buat gambar besar
    gambar = np.random.randint(0, 256, (1000, 1000, 3), dtype=np.uint8)
    
    # Test direct implementation
    start = time.time()
    for _ in range(10):
        _ = gamma_correction(gambar, 0.5)
    time_direct = (time.time() - start) / 10
    
    # Test LUT implementation
    start = time.time()
    for _ in range(10):
        _ = gamma_correction_lut(gambar, 0.5)
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

def main():
    """Fungsi utama program"""
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM: GAMMA CORRECTION")
    print("Bab 3 - Pemrosesan Citra")
    print("=" * 60)
    
    print("""
GAMMA CORRECTION adalah teknik non-linear untuk
menyesuaikan brightness gambar dengan mempertahankan
relative differences antar piksel.

Aplikasi:
├── Koreksi pencahayaan (exposure correction)
├── Display calibration (gamma 2.2)
├── HDR tone mapping
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
FORMULA:
    output = (input / 255)^gamma * 255
    
    atau untuk inverse gamma:
    output = (input / 255)^(1/gamma) * 255

IMPLEMENTASI OPENCV:
    # Menggunakan LUT untuk performa optimal
    inv_gamma = 1.0 / gamma
    lut = np.array([((i/255.0)**inv_gamma)*255 for i in range(256)])
    result = cv2.LUT(image, lut.astype(np.uint8))

NILAI GAMMA UMUM:
├── γ = 0.45 : sRGB encoding (compress for storage)
├── γ = 2.2  : sRGB decoding (expand for display)
├── γ < 1    : Brighten (lift shadows)
└── γ > 1    : Darken (compress highlights)

TIPS:
1. Gunakan LUT untuk gambar besar
2. Gamma 0.4-0.7 untuk brighten underexposed images
3. Gamma 1.5-2.5 untuk darken overexposed images
4. Kombinasikan dengan contrast adjustment untuk hasil optimal
""")


# Jalankan program utama
if __name__ == "__main__":
    main()
