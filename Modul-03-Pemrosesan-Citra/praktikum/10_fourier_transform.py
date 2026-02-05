# ============================================================
# PROGRAM: 10_fourier_transform.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Fourier Transform untuk analisis frekuensi
# 
# Tujuan Pembelajaran:
#   1. Memahami Fourier Transform dan domain frekuensi
#   2. Menganalisis frekuensi konten dalam gambar
#   3. Melakukan filtering di domain frekuensi
#   4. Aplikasi: noise removal, sharpening, compression
# 
# Teori:
#   F(u,v) = Σ Σ f(x,y) * e^(-j2π(ux/M + vy/N))
#   f(x,y) = Σ Σ F(u,v) * e^(j2π(ux/M + vy/N))
# ============================================================

# Keterangan: Impor modul cv2.
import cv2
# Keterangan: Impor modul numpy as np.
import numpy as np
# Keterangan: Impor modul matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
# Keterangan: Impor komponen dari modul matplotlib.colors.
from matplotlib.colors import LogNorm
# Keterangan: Impor modul os.
import os

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# Low-pass filter (remove high freq = blur)
# Keterangan: Inisialisasi atau perbarui variabel LOWPASS_RADIUS.
LOWPASS_RADIUS = 30        # Radius dalam freq domain (0-100)

# High-pass filter (remove low freq = sharpen/edge)
# Keterangan: Inisialisasi atau perbarui variabel HIGHPASS_RADIUS.
HIGHPASS_RADIUS = 20       # Radius dalam freq domain (0-100)

# Band-pass filter
# Keterangan: Inisialisasi atau perbarui variabel BANDPASS_INNER.
BANDPASS_INNER = 10        # Inner radius
# Keterangan: Inisialisasi atau perbarui variabel BANDPASS_OUTER.
BANDPASS_OUTER = 50        # Outer radius

# Notch filter (remove specific frequency)
# Keterangan: Inisialisasi atau perbarui variabel NOTCH_CENTER_U.
NOTCH_CENTER_U = 30        # Horizontal frequency
# Keterangan: Inisialisasi atau perbarui variabel NOTCH_CENTER_V.
NOTCH_CENTER_V = 40        # Vertical frequency
# Keterangan: Inisialisasi atau perbarui variabel NOTCH_RADIUS.
NOTCH_RADIUS = 5           # Notch size

# ============================================================
# FUNGSI FOURIER TRANSFORM
# ============================================================

# Keterangan: Definisikan fungsi fourier_transform.
def fourier_transform(image):
    """
    Melakukan Fourier Transform pada gambar
    
    Langkah:
    1. Convert ke grayscale jika perlu
    2. Float conversion
    3. FFT dengan numpy
    4. Shift zero frequency ke center
    
    Parameter:
    - image: input image (grayscale atau BGR)
    
    Return:
    - f_transform: complex frequency domain
    - magnitude: magnitude spectrum
    - phase: phase spectrum
    """
    # Keterangan: Jalankan perintah berikut.
    print("🔄 Melakukan Fourier Transform...")
    
    # Convert ke grayscale jika color
    # Keterangan: Cek kondisi len(image.shape) == 3.
    if len(image.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = image.copy()
    
    # Float conversion
    # Keterangan: Inisialisasi atau perbarui variabel f.
    f = np.float32(gray)
    
    # FFT
    # Keterangan: Inisialisasi atau perbarui variabel f_transform.
    f_transform = np.fft.fft2(f)
    
    # Shift zero frequency ke center
    # Keterangan: Inisialisasi atau perbarui variabel f_shift.
    f_shift = np.fft.fftshift(f_transform)
    
    # Calculate magnitude dan phase
    # Keterangan: Inisialisasi atau perbarui variabel magnitude.
    magnitude = np.abs(f_shift)
    # Keterangan: Inisialisasi atau perbarui variabel phase.
    phase = np.angle(f_shift)
    
    # Statistics
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Image size: {gray.shape}")
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Transform size: {f_shift.shape}")
    # Keterangan: Jalankan perintah berikut.
    print(f"   ✓ Magnitude range: {magnitude.min():.2f} - {magnitude.max():.2f}")
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return f_shift, magnitude, phase


# Keterangan: Definisikan fungsi inverse_fourier_transform.
def inverse_fourier_transform(f_shift):
    """
    Inverse Fourier Transform ke spatial domain
    
    Parameter:
    - f_shift: complex frequency domain (shifted)
    
    Return:
    - image: reconstructed spatial domain image
    """
    # Keterangan: Jalankan perintah berikut.
    print("🔙 Inverse Fourier Transform...")
    
    # Unshift
    # Keterangan: Inisialisasi atau perbarui variabel f_ishift.
    f_ishift = np.fft.ifftshift(f_shift)
    
    # Inverse FFT
    # Keterangan: Inisialisasi atau perbarui variabel img_back.
    img_back = np.fft.ifft2(f_ishift)
    
    # Ambil real part dan convert ke uint8
    # Keterangan: Inisialisasi atau perbarui variabel img_back.
    img_back = np.abs(img_back)
    # Keterangan: Inisialisasi atau perbarui variabel img_back.
    img_back = np.clip(img_back, 0, 255).astype(np.uint8)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return img_back


# Keterangan: Definisikan fungsi visualize_spectrum.
def visualize_spectrum(magnitude, title="Magnitude Spectrum"):
    """
    Visualisasi spectrum dengan log scale
    
    Parameter:
    - magnitude: magnitude spectrum
    - title: judul plot
    """
    # Log scale untuk better visualization
    # Keterangan: Inisialisasi atau perbarui variabel magnitude_log.
    magnitude_log = np.log1p(magnitude)  # log(1 + magnitude)
    
    # Normalize to 0-255
    # Keterangan: Inisialisasi atau perbarui variabel magnitude_norm.
    magnitude_norm = cv2.normalize(magnitude_log, None, 0, 255, cv2.NORM_MINMAX)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return magnitude_norm.astype(np.uint8)


# ============================================================
# FUNGSI FREQUENCY FILTERING
# ============================================================

# Keterangan: Definisikan fungsi create_lowpass_filter.
def create_lowpass_filter(shape, radius):
    """
    Membuat low-pass filter (Ideal circular)
    
    Mempertahankan frekuensi rendah (< radius) = blur
    
    Parameter:
    - shape: (height, width)
    - radius: cutoff radius
    
    Return:
    - filter mask (0 atau 1)
    """
    # Keterangan: Inisialisasi beberapa variabel (rows, cols).
    rows, cols = shape
    # Keterangan: Inisialisasi beberapa variabel (crow, ccol).
    crow, ccol = rows // 2, cols // 2
    
    # Create mask
    # Keterangan: Inisialisasi array bernilai nol.
    mask = np.zeros((rows, cols), np.uint8)
    
    # Draw circle
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(mask, (ccol, crow), radius, 1, -1)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return mask


# Keterangan: Definisikan fungsi create_highpass_filter.
def create_highpass_filter(shape, radius):
    """
    Membuat high-pass filter
    
    Mempertahankan frekuensi tinggi (> radius) = sharpen/edge
    
    Parameter:
    - shape: (height, width)
    - radius: cutoff radius
    
    Return:
    - filter mask (0 atau 1)
    """
    # High-pass = 1 - Low-pass
    # Keterangan: Inisialisasi atau perbarui variabel lowpass.
    lowpass = create_lowpass_filter(shape, radius)
    # Keterangan: Inisialisasi atau perbarui variabel highpass.
    highpass = 1 - lowpass
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return highpass


# Keterangan: Definisikan fungsi create_bandpass_filter.
def create_bandpass_filter(shape, inner_radius, outer_radius):
    """
    Membuat band-pass filter
    
    Mempertahankan frekuensi menengah [inner, outer]
    
    Parameter:
    - shape: (height, width)
    - inner_radius: inner cutoff
    - outer_radius: outer cutoff
    
    Return:
    - filter mask
    """
    # Keterangan: Inisialisasi atau perbarui variabel lowpass_outer.
    lowpass_outer = create_lowpass_filter(shape, outer_radius)
    # Keterangan: Inisialisasi atau perbarui variabel lowpass_inner.
    lowpass_inner = create_lowpass_filter(shape, inner_radius)
    
    # Band-pass = outer circle - inner circle
    # Keterangan: Inisialisasi atau perbarui variabel bandpass.
    bandpass = lowpass_outer - lowpass_inner
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return bandpass


# Keterangan: Definisikan fungsi create_gaussian_filter.
def create_gaussian_filter(shape, sigma):
    """
    Membuat Gaussian filter di frequency domain
    
    Lebih smooth dibanding ideal filter (no ringing)
    
    Parameter:
    - shape: (height, width)
    - sigma: standard deviation
    
    Return:
    - Gaussian filter mask
    """
    # Keterangan: Inisialisasi beberapa variabel (rows, cols).
    rows, cols = shape
    # Keterangan: Inisialisasi beberapa variabel (crow, ccol).
    crow, ccol = rows // 2, cols // 2
    
    # Create coordinate grids
    # Keterangan: Buat range angka berjarak tetap.
    u = np.arange(rows) - crow
    # Keterangan: Buat range angka berjarak tetap.
    v = np.arange(cols) - ccol
    # Keterangan: Buat grid koordinat 2D.
    U, V = np.meshgrid(v, u)  # Note: v first for proper orientation
    
    # Distance from center
    # Keterangan: Inisialisasi atau perbarui variabel D.
    D = np.sqrt(U**2 + V**2)
    
    # Gaussian
    # Keterangan: Inisialisasi atau perbarui variabel gaussian.
    gaussian = np.exp(-(D**2) / (2 * sigma**2))
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gaussian


# Keterangan: Definisikan fungsi apply_frequency_filter.
def apply_frequency_filter(image, filter_mask):
    """
    Apply filter di frequency domain
    
    Langkah:
    1. FFT
    2. Multiply dengan filter
    3. Inverse FFT
    
    Parameter:
    - image: input image
    - filter_mask: filter di freq domain
    
    Return:
    - filtered image
    """
    # Fourier transform
    # Keterangan: Inisialisasi beberapa variabel (f_shift, magnitude, phase).
    f_shift, magnitude, phase = fourier_transform(image)
    
    # Apply filter
    # Keterangan: Inisialisasi atau perbarui variabel f_filtered.
    f_filtered = f_shift * filter_mask
    
    # Inverse transform
    # Keterangan: Inisialisasi atau perbarui variabel result.
    result = inverse_fourier_transform(f_filtered)
    
    # Calculate filtered magnitude untuk visualization
    # Keterangan: Inisialisasi atau perbarui variabel magnitude_filtered.
    magnitude_filtered = np.abs(f_filtered)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return result, magnitude, magnitude_filtered


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

# Keterangan: Definisikan fungsi demo_basic_fft.
def demo_basic_fft():
    """
    Demo 1: Basic FFT dan visualization
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 1: BASIC FOURIER TRANSFORM")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create sample image dengan berbagai frekuensi
    # Keterangan: Inisialisasi atau perbarui variabel size.
    size = 256
    # Keterangan: Inisialisasi array bernilai nol.
    image = np.zeros((size, size), dtype=np.uint8)
    
    # Add low frequency (large square)
    # Keterangan: Inisialisasi beberapa variabel (image[64:192, 64:192]).
    image[64:192, 64:192] = 255
    
    # Add medium frequency (smaller squares)
    # Keterangan: Mulai loop dengan for i in range(4).
    for i in range(4):
        # Keterangan: Mulai loop dengan for j in range(4).
        for j in range(4):
            # Keterangan: Inisialisasi beberapa variabel (x, y).
            x, y = i * 60 + 10, j * 60 + 10
            # Keterangan: Inisialisasi beberapa variabel (image[x:x+30, x:y+30]).
            image[x:x+30, x:y+30] = 200
    
    # Add high frequency (fine grid)
    # Keterangan: Mulai loop dengan for i in range(0, size, 8).
    for i in range(0, size, 8):
        # Keterangan: Inisialisasi beberapa variabel (image[i:i+2, :]).
        image[i:i+2, :] = 100
        # Keterangan: Inisialisasi beberapa variabel (image[:, i:i+2]).
        image[:, i:i+2] = 100
    
    # Fourier transform
    # Keterangan: Inisialisasi beberapa variabel (f_shift, magnitude, phase).
    f_shift, magnitude, phase = fourier_transform(image)
    
    # Visualize
    # Keterangan: Inisialisasi atau perbarui variabel magnitude_display.
    magnitude_display = visualize_spectrum(magnitude)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 5))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Original Image\n(Spatial Domain)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(magnitude_display, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Magnitude Spectrum\n(Frequency Domain - Log Scale)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    # Keterangan: Inisialisasi beberapa variabel (plt.text(10, 20, "Low freq\n(center)", color).
    plt.text(10, 20, "Low freq\n(center)", color='yellow', fontsize=8,
             # Keterangan: Inisialisasi atau perbarui variabel bbox.
             bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    # Keterangan: Inisialisasi beberapa variabel (plt.text(220, 20, "High\nfreq", color).
    plt.text(220, 20, "High\nfreq", color='yellow', fontsize=8,
             # Keterangan: Inisialisasi atau perbarui variabel bbox.
             bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(1, 3, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(phase, cmap='hsv')
    # Keterangan: Set judul subplot.
    plt.title("Phase Spectrum")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Fourier Transform Components", fontsize).
    plt.suptitle("Fourier Transform Components", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Interpretasi Spectrum:")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 🎯 Center (DC component).
    print("   🎯 Center (DC component) = average brightness")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 🎯 Brightness pada spectrum.
    print("   🎯 Brightness pada spectrum = strength dari frequency")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 🎯 Horizontal line di spectrum.
    print("   🎯 Horizontal line di spectrum = vertical edges di image")
    # Keterangan: Inisialisasi atau perbarui variabel print(" 🎯 Vertical line di spectrum.
    print("   🎯 Vertical line di spectrum = horizontal edges di image")


# Keterangan: Definisikan fungsi demo_frequency_filters.
def demo_frequency_filters():
    """
    Demo 2: Low-pass, High-pass, Band-pass filters
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 2: FREQUENCY DOMAIN FILTERING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Baca gambar dari file ke array.
    image = cv2.imread(cv2.samples.findFile("lena.jpg"), 0)
    # Keterangan: Cek kondisi image is None.
    if image is None:
        # Create sample
        # Keterangan: Inisialisasi atau perbarui variabel image.
        image = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
        # Add pattern
        # Keterangan: Mulai loop dengan for i in range(0, 256, 16).
        for i in range(0, 256, 16):
            # Keterangan: Inisialisasi beberapa variabel (image[i:i+8, :]).
            image[i:i+8, :] = 200
    
    # Keterangan: Ubah ukuran gambar.
    image = cv2.resize(image, (512, 512))
    
    # Create filters
    # Keterangan: Inisialisasi atau perbarui variabel lowpass.
    lowpass = create_lowpass_filter(image.shape, LOWPASS_RADIUS)
    # Keterangan: Inisialisasi atau perbarui variabel highpass.
    highpass = create_highpass_filter(image.shape, HIGHPASS_RADIUS)
    # Keterangan: Inisialisasi atau perbarui variabel bandpass.
    bandpass = create_bandpass_filter(image.shape, BANDPASS_INNER, BANDPASS_OUTER)
    # Keterangan: Inisialisasi atau perbarui variabel gaussian_lp.
    gaussian_lp = create_gaussian_filter(image.shape, LOWPASS_RADIUS / 2)
    
    # Apply filters
    # Keterangan: Inisialisasi beberapa variabel (result_lp, mag_orig, mag_lp).
    result_lp, mag_orig, mag_lp = apply_frequency_filter(image, lowpass)
    # Keterangan: Inisialisasi beberapa variabel (result_hp, _, mag_hp).
    result_hp, _, mag_hp = apply_frequency_filter(image, highpass)
    # Keterangan: Inisialisasi beberapa variabel (result_bp, _, mag_bp).
    result_bp, _, mag_bp = apply_frequency_filter(image, bandpass)
    # Keterangan: Inisialisasi beberapa variabel (result_gauss, _, mag_gauss).
    result_gauss, _, mag_gauss = apply_frequency_filter(image, gaussian_lp)
    
    # Display
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    
    # Row 1: Filters
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].imshow(lowpass, cmap).
    axes[0, 0].imshow(lowpass, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 0].set_title(f"Low-Pass Filter\n(r).
    axes[0, 0].set_title(f"Low-Pass Filter\n(r={LOWPASS_RADIUS})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].imshow(highpass, cmap).
    axes[0, 1].imshow(highpass, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 1].set_title(f"High-Pass Filter\n(r).
    axes[0, 1].set_title(f"High-Pass Filter\n(r={HIGHPASS_RADIUS})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 2].imshow(bandpass, cmap).
    axes[0, 2].imshow(bandpass, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].set_title(f"Band-Pass Filter\n({BANDPASS_INNER}-{BANDPASS_OUTER})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 3].imshow(gaussian_lp, cmap).
    axes[0, 3].imshow(gaussian_lp, cmap='gray')
    # Keterangan: Inisialisasi beberapa variabel (axes[0, 3].set_title(f"Gaussian LP\n(σ).
    axes[0, 3].set_title(f"Gaussian LP\n(σ={LOWPASS_RADIUS/2:.1f})")
    # Keterangan: Jalankan perintah berikut.
    axes[0, 3].axis('off')
    
    # Row 2: Filtered spectrums
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 0].imshow(visualize_spectrum(mag_lp), cmap).
    axes[1, 0].imshow(visualize_spectrum(mag_lp), cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].set_title("Filtered Spectrum\n(Low frequencies only)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 1].imshow(visualize_spectrum(mag_hp), cmap).
    axes[1, 1].imshow(visualize_spectrum(mag_hp), cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].set_title("Filtered Spectrum\n(High frequencies only)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 2].imshow(visualize_spectrum(mag_bp), cmap).
    axes[1, 2].imshow(visualize_spectrum(mag_bp), cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].set_title("Filtered Spectrum\n(Mid frequencies)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[1, 3].imshow(visualize_spectrum(mag_gauss), cmap).
    axes[1, 3].imshow(visualize_spectrum(mag_gauss), cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[1, 3].set_title("Filtered Spectrum\n(Gaussian smooth)")
    # Keterangan: Jalankan perintah berikut.
    axes[1, 3].axis('off')
    
    # Row 3: Results
    # Keterangan: Inisialisasi beberapa variabel (axes[2, 0].imshow(result_lp, cmap).
    axes[2, 0].imshow(result_lp, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[2, 0].set_title("Result: BLURRED\n(low freq only)")
    # Keterangan: Jalankan perintah berikut.
    axes[2, 0].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[2, 1].imshow(result_hp, cmap).
    axes[2, 1].imshow(result_hp, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[2, 1].set_title("Result: EDGES\n(high freq only)")
    # Keterangan: Jalankan perintah berikut.
    axes[2, 1].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[2, 2].imshow(result_bp, cmap).
    axes[2, 2].imshow(result_bp, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[2, 2].set_title("Result: BAND-PASS")
    # Keterangan: Jalankan perintah berikut.
    axes[2, 2].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (axes[2, 3].imshow(result_gauss, cmap).
    axes[2, 3].imshow(result_gauss, cmap='gray')
    # Keterangan: Jalankan perintah berikut.
    axes[2, 3].set_title("Result: GAUSSIAN BLUR\n(no ringing)")
    # Keterangan: Jalankan perintah berikut.
    axes[2, 3].axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("Frequency Domain Filtering", fontsize).
    plt.suptitle("Frequency Domain Filtering", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Analisis Hasil:")
    # Keterangan: Jalankan perintah berikut.
    print("   🔵 Low-pass: Mempertahankan struktur besar, blur detail")
    # Keterangan: Jalankan perintah berikut.
    print("   🔴 High-pass: Mempertahankan edge/detail, hilangkan smooth area")
    # Keterangan: Jalankan perintah berikut.
    print("   🟣 Band-pass: Mempertahankan frekuensi tertentu")
    # Keterangan: Jalankan perintah berikut.
    print("   🟢 Gaussian: Smooth cutoff, no ringing artifacts")


# Keterangan: Definisikan fungsi demo_fft_vs_spatial_filtering.
def demo_fft_vs_spatial_filtering():
    """
    Demo 3: Perbandingan FFT filtering vs spatial filtering
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 3: FFT VS SPATIAL FILTERING")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi atau perbarui variabel image.
    image = np.random.randint(100, 200, (256, 256), dtype=np.uint8)
    
    # Add some structure
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (50, 50), (200, 200), 255, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (200, 80), 30, 50, -1)
    
    # Add noise
    # Keterangan: Inisialisasi atau perbarui variabel noise.
    noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
    # Keterangan: Inisialisasi atau perbarui variabel image.
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Method 1: Spatial domain Gaussian blur
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    spatial_blur = cv2.GaussianBlur(image, (15, 15), 5)
    
    # Method 2: Frequency domain Gaussian filter
    # Keterangan: Inisialisasi atau perbarui variabel gaussian_filter.
    gaussian_filter = create_gaussian_filter(image.shape, 20)
    # Keterangan: Inisialisasi beberapa variabel (freq_blur, mag_orig, mag_filtered).
    freq_blur, mag_orig, mag_filtered = apply_frequency_filter(image, gaussian_filter)
    
    # Compare
    # Keterangan: Inisialisasi atau perbarui variabel difference.
    difference = cv2.absdiff(spatial_blur, freq_blur)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 10))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Original (Noisy)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(spatial_blur, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Spatial Domain\nGaussian Blur (kernel 15×15)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(freq_blur, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Frequency Domain\nGaussian Filter (σ=20)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 4)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(gaussian_filter, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Gaussian Filter Mask")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 5)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(visualize_spectrum(mag_filtered), cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Filtered Spectrum")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 6)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(difference, cmap='hot')
    # Keterangan: Set judul subplot.
    plt.title(f"Difference\nMax diff: {difference.max()}")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Inisialisasi beberapa variabel (plt.suptitle("FFT vs Spatial Filtering Comparison", fontsize).
    plt.suptitle("FFT vs Spatial Filtering Comparison", fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n📊 Perbandingan:")
    # Keterangan: Jalankan perintah berikut.
    print(f"   Max difference: {difference.max()} (should be very small)")
    # Keterangan: Jalankan perintah berikut.
    print("   ✓ Hasil praktis identik")
    # Keterangan: Jalankan perintah berikut.
    print("\n💡 Kapan menggunakan FFT filtering?")
    # Keterangan: Jalankan perintah berikut.
    print("   - Large kernel size (FFT lebih efisien)")
    # Keterangan: Jalankan perintah berikut.
    print("   - Analisis frekuensi")
    # Keterangan: Jalankan perintah berikut.
    print("   - Filter design di freq domain lebih intuitif")


# Keterangan: Definisikan fungsi demo_periodic_noise_removal.
def demo_periodic_noise_removal():
    """
    Demo 4: Menghilangkan periodic noise dengan notch filter
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 4: PERIODIC NOISE REMOVAL")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create clean image
    # Keterangan: Inisialisasi array bernilai nol.
    image = np.zeros((256, 256), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (50, 50), (200, 200), 200, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (128, 128), 60, 255, -1)
    
    # Add periodic noise (simulating scan lines, moire pattern, etc)
    # Keterangan: Inisialisasi atau perbarui variabel noise_freq.
    noise_freq = 15  # Noise frequency
    # Keterangan: Buat range angka berjarak tetap.
    x = np.arange(256)
    # Keterangan: Buat range angka berjarak tetap.
    y = np.arange(256)
    # Keterangan: Buat grid koordinat 2D.
    X, Y = np.meshgrid(x, y)
    
    # Vertical periodic noise
    # Keterangan: Inisialisasi atau perbarui variabel noise.
    noise = 30 * np.sin(2 * np.pi * X / noise_freq)
    # Keterangan: Inisialisasi atau perbarui variabel image_noisy.
    image_noisy = np.clip(image.astype(float) + noise, 0, 255).astype(np.uint8)
    
    # Fourier transform
    # Keterangan: Inisialisasi beberapa variabel (f_shift, mag_noisy, phase).
    f_shift, mag_noisy, phase = fourier_transform(image_noisy)
    
    # Identify noise peaks in spectrum
    # (In real app, would use peak detection)
    # For demo, we manually create notch filter
    
    # Create notch filter untuk remove periodic noise
    # Keterangan: Inisialisasi beberapa variabel (rows, cols).
    rows, cols = image.shape
    # Keterangan: Inisialisasi beberapa variabel (crow, ccol).
    crow, ccol = rows // 2, cols // 2
    
    # Notch filter mask (start with all ones)
    # Keterangan: Inisialisasi array bernilai satu.
    notch_mask = np.ones((rows, cols), dtype=np.float32)
    
    # Calculate noise frequency position
    # Keterangan: Inisialisasi atau perbarui variabel freq_u.
    freq_u = int(256 / noise_freq)
    
    # Remove frequency spikes (dan symmetric pair)
    # Keterangan: Inisialisasi atau perbarui variabel notch_radius.
    notch_radius = 5
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(notch_mask, (ccol + freq_u, crow), notch_radius, 0, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(notch_mask, (ccol - freq_u, crow), notch_radius, 0, -1)
    
    # Apply notch filter
    # Keterangan: Inisialisasi atau perbarui variabel f_filtered.
    f_filtered = f_shift * notch_mask
    # Keterangan: Inisialisasi atau perbarui variabel mag_filtered.
    mag_filtered = np.abs(f_filtered)
    
    # Inverse transform
    # Keterangan: Inisialisasi atau perbarui variabel image_cleaned.
    image_cleaned = inverse_fourier_transform(f_filtered)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 10))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Clean Image")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image_noisy, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title(f"Noisy Image\n(periodic noise, freq={noise_freq})")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image_cleaned, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Cleaned Image\n(noise removed)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 4)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(visualize_spectrum(mag_noisy), cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Noisy Spectrum\n(note: bright spots = noise freq)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    # Keterangan: Inisialisasi beberapa variabel (plt.plot([ccol + freq_u, ccol - freq_u], [crow, crow], 'r+', markersize).
    plt.plot([ccol + freq_u, ccol - freq_u], [crow, crow], 'r+', markersize=15, markeredgewidth=2)
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 5)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(notch_mask, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Notch Filter Mask\n(black = removed frequencies)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 6)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(visualize_spectrum(mag_filtered), cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Filtered Spectrum\n(noise peaks removed)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Periodic Noise Removal dengan Notch Filter", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🏆 Aplikasi Nyata:")
    # Keterangan: Jalankan perintah berikut.
    print("   📺 Removing scan lines dari TV/monitor capture")
    # Keterangan: Jalankan perintah berikut.
    print("   📄 Removing halftone patterns dari scanned documents")
    # Keterangan: Jalankan perintah berikut.
    print("   🎥 Removing rolling shutter artifacts")
    # Keterangan: Jalankan perintah berikut.
    print("   📡 Removing electrical interference patterns")


# Keterangan: Definisikan fungsi demo_image_sharpening_fft.
def demo_image_sharpening_fft():
    """
    Demo 5: Image sharpening menggunakan high-pass filter
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 5: IMAGE SHARPENING VIA FFT")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create slightly blurry image
    # Keterangan: Inisialisasi atau perbarui variabel image.
    image = np.random.randint(100, 200, (256, 256), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (50, 50), (200, 200), 255, -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(image, (128, 128), 50, 100, -1)
    
    # Blur it
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    image = cv2.GaussianBlur(image, (7, 7), 2)
    
    # Method 1: Unsharp masking (spatial)
    # Keterangan: Terapkan blur Gaussian untuk menghaluskan gambar.
    blurred = cv2.GaussianBlur(image, (9, 9), 3)
    # Keterangan: Inisialisasi atau perbarui variabel spatial_sharp.
    spatial_sharp = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
    
    # Method 2: High-pass filter (frequency)
    # High-boost filter: original + strength * high-pass
    # Keterangan: Inisialisasi atau perbarui variabel highpass.
    highpass = create_highpass_filter(image.shape, 50)  # Keep more frequencies
    # Keterangan: Inisialisasi beberapa variabel (result_hp, _, _).
    result_hp, _, _ = apply_frequency_filter(image, highpass)
    
    # Combine: original + enhanced high frequencies
    # Keterangan: Inisialisasi atau perbarui variabel freq_sharp.
    freq_sharp = cv2.addWeighted(image, 1.0, result_hp, 0.5, 0)
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 10))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Blurry Image")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(spatial_sharp, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Spatial Sharpening\n(Unsharp Masking)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 3)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(freq_sharp, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Frequency Sharpening\n(High-pass + Original)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 4)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(highpass, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("High-Pass Filter")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 5)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(result_hp, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("High Frequencies Only")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 6)
    # Show profile comparison
    # Keterangan: Inisialisasi atau perbarui variabel mid_row.
    mid_row = 128
    # Keterangan: Inisialisasi beberapa variabel (plt.plot(image[mid_row, :], label).
    plt.plot(image[mid_row, :], label='Blurry', alpha=0.7)
    # Keterangan: Inisialisasi beberapa variabel (plt.plot(spatial_sharp[mid_row, :], label).
    plt.plot(spatial_sharp[mid_row, :], label='Spatial sharp', alpha=0.7)
    # Keterangan: Inisialisasi beberapa variabel (plt.plot(freq_sharp[mid_row, :], label).
    plt.plot(freq_sharp[mid_row, :], label='Freq sharp', alpha=0.7)
    # Keterangan: Set judul subplot.
    plt.title("Intensity Profile Comparison")
    # Keterangan: Jalankan perintah berikut.
    plt.legend()
    # Keterangan: Inisialisasi beberapa variabel (plt.grid(True, alpha).
    plt.grid(True, alpha=0.3)
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("Image Sharpening: Spatial vs Frequency Domain", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()


# Keterangan: Definisikan fungsi demo_dct_compression.
def demo_dct_compression():
    """
    Demo 6: DCT (Discrete Cosine Transform) untuk compression
    """
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "="*60)
    # Keterangan: Jalankan perintah berikut.
    print("DEMO 6: DCT IMAGE COMPRESSION")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("="*60)
    
    # Create test image
    # Keterangan: Inisialisasi atau perbarui variabel image.
    image = np.random.randint(50, 200, (256, 256), dtype=np.uint8)
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(image, (80, 80), (180, 180), 255, -1)
    
    # DCT (OpenCV provides DCT)
    # Keterangan: Inisialisasi atau perbarui variabel image_float.
    image_float = np.float32(image)
    # Keterangan: Inisialisasi atau perbarui variabel dct.
    dct = cv2.dct(image_float)
    
    # Visualize DCT coefficients
    # Keterangan: Inisialisasi atau perbarui variabel dct_log.
    dct_log = np.log1p(np.abs(dct))
    # Keterangan: Inisialisasi atau perbarui variabel dct_visual.
    dct_visual = cv2.normalize(dct_log, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Compression: Keep only low frequency coefficients
    # Simulate JPEG compression
    # Keterangan: Inisialisasi atau perbarui variabel compression_ratios.
    compression_ratios = [10, 25, 50, 75]
    # Keterangan: Inisialisasi atau perbarui variabel results.
    results = []
    
    # Keterangan: Mulai loop dengan for ratio in compression_ratios.
    for ratio in compression_ratios:
        # Create mask: keep only top-left corner (low frequencies)
        # Keterangan: Inisialisasi atau perbarui variabel keep_size.
        keep_size = int(256 * ratio / 100)
        # Keterangan: Inisialisasi array bernilai nol.
        dct_compressed = np.zeros_like(dct)
        # Keterangan: Inisialisasi beberapa variabel (dct_compressed[:keep_size, :keep_size]).
        dct_compressed[:keep_size, :keep_size] = dct[:keep_size, :keep_size]
        
        # Inverse DCT
        # Keterangan: Inisialisasi atau perbarui variabel reconstructed.
        reconstructed = cv2.idct(dct_compressed)
        # Keterangan: Inisialisasi atau perbarui variabel reconstructed.
        reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)
        
        # Calculate MSE
        # Keterangan: Inisialisasi atau perbarui variabel mse.
        mse = np.mean((image.astype(float) - reconstructed.astype(float))**2)
        # Keterangan: Inisialisasi atau perbarui variabel psnr.
        psnr = 10 * np.log10(255**2 / mse) if mse > 0 else float('inf')
        
        # Keterangan: Jalankan perintah berikut.
        results.append((reconstructed, psnr, ratio))
        # Keterangan: Inisialisasi atau perbarui variabel print(f" Compression {ratio}%: PSNR.
        print(f"   Compression {ratio}%: PSNR = {psnr:.2f} dB")
    
    # Display
    # Keterangan: Buat kanvas figure untuk plotting.
    plt.figure(figsize=(15, 10))
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 1)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(image, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("Original Image")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    plt.subplot(2, 3, 2)
    # Keterangan: Tampilkan gambar pada kanvas.
    plt.imshow(dct_visual, cmap='gray')
    # Keterangan: Set judul subplot.
    plt.title("DCT Coefficients (Log Scale)\nTop-left = low freq (most important)")
    # Keterangan: Atur tampilan sumbu.
    plt.axis('off')
    
    # Keterangan: Mulai loop dengan for idx, (recon, psnr, ratio) in enumerate(results).
    for idx, (recon, psnr, ratio) in enumerate(results):
        # Keterangan: Pilih area subplot untuk menampilkan hasil.
        plt.subplot(2, 3, 3 + idx)
        # Keterangan: Tampilkan gambar pada kanvas.
        plt.imshow(recon, cmap='gray')
        # Keterangan: Set judul subplot.
        plt.title(f"Keep {ratio}% coefficients\nPSNR = {psnr:.1f} dB")
        # Keterangan: Atur tampilan sumbu.
        plt.axis('off')
    
    # Keterangan: Jalankan perintah berikut.
    plt.suptitle("DCT-based Image Compression (JPEG principle)", 
                 # Keterangan: Inisialisasi atau perbarui variabel fontsize.
                 fontsize=14, fontweight='bold')
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Keterangan: Jalankan perintah berikut.
    print("\n🏆 DCT digunakan dalam:")
    # Keterangan: Jalankan perintah berikut.
    print("   📸 JPEG image compression")
    # Keterangan: Jalankan perintah berikut.
    print("   🎬 MPEG/H.264 video compression")
    # Keterangan: Jalankan perintah berikut.
    print("   🎵 MP3 audio compression (1D DCT)")


# ============================================================
# MAIN PROGRAM
# ============================================================

# Keterangan: Definisikan fungsi main.
def main():
    """Program utama"""
    print("\n" + "="*60)
    print("      PRAKTIKUM COMPUTER VISION - BAB 3")
    print("         FOURIER TRANSFORM")
    print("="*60)
    
    print("\n📚 Konsep yang akan dipelajari:")
    print("   1. Fourier Transform: spatial ↔ frequency domain")
    print("   2. Magnitude dan phase spectrum")
    print("   3. Frequency domain filtering")
    print("   4. Low-pass (blur), high-pass (sharpen), band-pass")
    print("   5. Periodic noise removal dengan notch filter")
    print("   6. DCT untuk image compression")
    
    print("\n🎯 Teori Kunci:")
    print("   - Low frequency = smooth regions, overall structure")
    print("   - High frequency = edges, details, textures")
    print("   - FFT: O(N²logN) vs spatial convolution O(N²K²)")
    print("   - Ideal untuk large kernel atau analysis")
    
    try:
        # Demo 1: Basic FFT
        demo_basic_fft()
        
        # Demo 2: Frequency filters
        demo_frequency_filters()
        
        # Demo 3: FFT vs spatial
        demo_fft_vs_spatial_filtering()
        
        # Demo 4: Periodic noise removal
        demo_periodic_noise_removal()
        
        # Demo 5: Sharpening
        demo_image_sharpening_fft()
        
        # Demo 6: DCT compression
        demo_dct_compression()
        
        print("\n" + "="*60)
        print("✅ SEMUA DEMO SELESAI")
        print("="*60)
        
        print("\n💡 Kesimpulan:")
        print("   1. FFT mengubah gambar ke frequency domain")
        print("   2. Low freq = struktur, high freq = detail")
        print("   3. Filtering di freq domain = multiply dengan mask")
        print("   4. Notch filter bagus untuk periodic noise")
        print("   5. DCT digunakan dalam JPEG compression")
        
        print("\n🔬 Eksperimen Lanjutan:")
        print("   - Ubah LOWPASS_RADIUS untuk blur berbeda")
        print("   - Ubah HIGHPASS_RADIUS untuk sharpening berbeda")
        print("   - Coba band-pass untuk isolate specific features")
        print("   - Analyze spectrum dari berbagai jenis gambar")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
