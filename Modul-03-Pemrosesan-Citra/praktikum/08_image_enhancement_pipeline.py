# ============================================================
# PROGRAM: 08_image_enhancement_pipeline.py
# PRAKTIKUM COMPUTER VISION - BAB 3: PEMROSESAN CITRA
# ============================================================
# Deskripsi: Pipeline lengkap untuk image enhancement
# 
# Tujuan Pembelajaran:
#   1. Menggabungkan teknik-teknik image processing
#   2. Membangun pipeline enhancement yang efektif
#   3. Auto-enhancement dengan analisis gambar
#   4. Optimasi parameter berdasarkan karakteristik gambar
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
# Keterangan: Impor modul time.
import time

# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
# Keterangan: Inisialisasi atau perbarui variabel NAMA_FILE_GAMBAR.
NAMA_FILE_GAMBAR = "portrait.jpg"

# 2. Mode enhancement
# Opsi: 'auto', 'manual'
# Keterangan: Inisialisasi atau perbarui variabel ENHANCEMENT_MODE.
ENHANCEMENT_MODE = 'auto'

# 3. Parameter manual (digunakan jika mode='manual')
# Keterangan: Inisialisasi atau perbarui variabel MANUAL_BRIGHTNESS.
MANUAL_BRIGHTNESS = 0      # Range: -100 sampai 100
# Keterangan: Inisialisasi atau perbarui variabel MANUAL_CONTRAST.
MANUAL_CONTRAST = 1.0      # Range: 0.5 sampai 2.0
# Keterangan: Inisialisasi atau perbarui variabel MANUAL_GAMMA.
MANUAL_GAMMA = 1.0         # Range: 0.5 sampai 2.5
# Keterangan: Inisialisasi atau perbarui variabel MANUAL_SATURATION.
MANUAL_SATURATION = 1.0    # Range: 0.5 sampai 2.0
# Keterangan: Inisialisasi atau perbarui variabel MANUAL_SHARPNESS.
MANUAL_SHARPNESS = 0.0     # Range: 0.0 sampai 2.0

# 4. Enhancement presets
# Opsi: 'natural', 'vivid', 'dramatic', 'vintage', 'cinematic'
# Keterangan: Inisialisasi atau perbarui variabel PRESET.
PRESET = 'natural'

# 5. Noise reduction strength
# Range: 0 (no reduction) sampai 1.0 (strong)
# Keterangan: Inisialisasi atau perbarui variabel NOISE_REDUCTION.
NOISE_REDUCTION = 0.5

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


def buat_gambar_sample():
    """Membuat gambar sample untuk testing pipeline"""
    # Gambar dengan berbagai masalah
    # Keterangan: Inisialisasi array bernilai nol.
    gambar = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Background gelap (under-exposed simulation)
    # Keterangan: Inisialisasi atau perbarui variabel gambar[:].
    gambar[:] = [40, 50, 60]
    
    # Beberapa objek
    # Keterangan: Jalankan perintah berikut.
    cv2.rectangle(gambar, (50, 50), (200, 150), (80, 100, 120), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.circle(gambar, (400, 100), 60, (100, 80, 70), -1)
    # Keterangan: Jalankan perintah berikut.
    cv2.fillPoly(gambar, [np.array([[250, 300], [350, 200], [450, 300]])], 
                 # Keterangan: Jalankan perintah berikut.
                 (90, 110, 80))
    
    # Tambah noise
    # Keterangan: Inisialisasi atau perbarui variabel noise.
    noise = np.random.normal(0, 10, gambar.shape).astype(np.float64)
    # Keterangan: Inisialisasi atau perbarui variabel gambar.
    gambar = np.clip(gambar.astype(np.float64) + noise, 0, 255).astype(np.uint8)
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return gambar


# ============================================================
# FUNGSI ANALISIS GAMBAR
# ============================================================

# Keterangan: Definisikan fungsi analisis_brightness.
def analisis_brightness(gambar):
    """
    Analisis tingkat brightness gambar
    
    Return:
    - mean_brightness: rata-rata intensitas
    - assessment: 'dark', 'normal', atau 'bright'
    - suggested_adjustment: nilai adjustment yang disarankan
    """
    # Keterangan: Cek kondisi len(gambar.shape) == 3.
    if len(gambar.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = gambar
    
    # Keterangan: Inisialisasi atau perbarui variabel mean_brightness.
    mean_brightness = np.mean(gray)
    
    # Keterangan: Cek kondisi mean_brightness < 80.
    if mean_brightness < 80:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'dark'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_adjustment.
        suggested_adjustment = int((120 - mean_brightness) * 0.5)
    # Keterangan: Cek kondisi alternatif mean_brightness > 180.
    elif mean_brightness > 180:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'bright'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_adjustment.
        suggested_adjustment = -int((mean_brightness - 130) * 0.5)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'normal'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_adjustment.
        suggested_adjustment = 0
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return mean_brightness, assessment, suggested_adjustment


# Keterangan: Definisikan fungsi analisis_contrast.
def analisis_contrast(gambar):
    """
    Analisis tingkat kontras gambar
    
    Return:
    - std_dev: standar deviasi intensitas
    - assessment: 'low', 'normal', atau 'high'
    - suggested_factor: faktor kontras yang disarankan
    """
    # Keterangan: Cek kondisi len(gambar.shape) == 3.
    if len(gambar.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = gambar
    
    # Keterangan: Inisialisasi atau perbarui variabel std_dev.
    std_dev = np.std(gray)
    
    # Keterangan: Cek kondisi std_dev < 40.
    if std_dev < 40:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'low'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_factor.
        suggested_factor = 1.3
    # Keterangan: Cek kondisi alternatif std_dev > 80.
    elif std_dev > 80:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'high'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_factor.
        suggested_factor = 0.8
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'normal'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_factor.
        suggested_factor = 1.0
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return std_dev, assessment, suggested_factor


# Keterangan: Definisikan fungsi analisis_noise.
def analisis_noise(gambar):
    """
    Estimasi tingkat noise dalam gambar
    
    Menggunakan Laplacian variance method
    """
    # Keterangan: Cek kondisi len(gambar.shape) == 3.
    if len(gambar.shape) == 3:
        # Keterangan: Konversi ruang warna gambar.
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel gray.
        gray = gambar
    
    # Laplacian variance (higher = more detail/noise)
    # Keterangan: Hitung Laplacian untuk deteksi tepi.
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Estimate noise using median filter difference
    # Keterangan: Inisialisasi atau perbarui variabel blurred.
    blurred = cv2.medianBlur(gray, 5)
    # Keterangan: Inisialisasi atau perbarui variabel noise_estimate.
    noise_estimate = np.mean(np.abs(gray.astype(np.float64) - blurred.astype(np.float64)))
    
    # Keterangan: Cek kondisi noise_estimate > 15.
    if noise_estimate > 15:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'high'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_reduction.
        suggested_reduction = 0.8
    # Keterangan: Cek kondisi alternatif noise_estimate > 8.
    elif noise_estimate > 8:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'medium'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_reduction.
        suggested_reduction = 0.5
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel assessment.
        assessment = 'low'
        # Keterangan: Inisialisasi atau perbarui variabel suggested_reduction.
        suggested_reduction = 0.2
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return noise_estimate, assessment, suggested_reduction


# Keterangan: Definisikan fungsi analisis_color_balance.
def analisis_color_balance(gambar):
    """
    Analisis keseimbangan warna
    
    Return:
    - channel_means: rata-rata setiap channel
    - color_cast: deteksi color cast
    """
    # Keterangan: Cek kondisi len(gambar.shape) != 3.
    if len(gambar.shape) != 3:
        # Keterangan: Kembalikan hasil dari fungsi.
        return None, 'grayscale'
    
    # Keterangan: Inisialisasi atau perbarui variabel b_mean.
    b_mean = np.mean(gambar[:, :, 0])
    # Keterangan: Inisialisasi atau perbarui variabel g_mean.
    g_mean = np.mean(gambar[:, :, 1])
    # Keterangan: Inisialisasi atau perbarui variabel r_mean.
    r_mean = np.mean(gambar[:, :, 2])
    
    # Keterangan: Inisialisasi atau perbarui variabel channel_means.
    channel_means = {'B': b_mean, 'G': g_mean, 'R': r_mean}
    
    # Detect color cast
    # Keterangan: Inisialisasi atau perbarui variabel avg.
    avg = (b_mean + g_mean + r_mean) / 3
    # Keterangan: Inisialisasi atau perbarui variabel deviation.
    deviation = max(abs(b_mean - avg), abs(g_mean - avg), abs(r_mean - avg))
    
    # Keterangan: Cek kondisi deviation > 20.
    if deviation > 20:
        # Keterangan: Cek kondisi b_mean > max(g_mean, r_mean).
        if b_mean > max(g_mean, r_mean):
            # Keterangan: Inisialisasi atau perbarui variabel color_cast.
            color_cast = 'blue'
        # Keterangan: Cek kondisi alternatif r_mean > max(g_mean, b_mean).
        elif r_mean > max(g_mean, b_mean):
            # Keterangan: Inisialisasi atau perbarui variabel color_cast.
            color_cast = 'red/yellow'
        # Keterangan: Cek kondisi alternatif g_mean > max(b_mean, r_mean).
        elif g_mean > max(b_mean, r_mean):
            # Keterangan: Inisialisasi atau perbarui variabel color_cast.
            color_cast = 'green'
        # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
        else:
            # Keterangan: Inisialisasi atau perbarui variabel color_cast.
            color_cast = 'mixed'
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel color_cast.
        color_cast = 'balanced'
    
    # Keterangan: Kembalikan hasil dari fungsi.
    return channel_means, color_cast


# Keterangan: Definisikan fungsi analisis_lengkap.
def analisis_lengkap(gambar):
    """Melakukan analisis lengkap gambar"""
    print("\n" + "-" * 40)
    print("ANALISIS GAMBAR")
    print("-" * 40)
    
    brightness, b_assessment, b_adjust = analisis_brightness(gambar)
    contrast, c_assessment, c_factor = analisis_contrast(gambar)
    noise, n_assessment, n_reduce = analisis_noise(gambar)
    channel_means, color_cast = analisis_color_balance(gambar)
    
    print(f"Brightness: {brightness:.1f} ({b_assessment})")
    print(f"  → Suggested adjustment: {b_adjust:+d}")
    
    print(f"Contrast (StdDev): {contrast:.1f} ({c_assessment})")
    print(f"  → Suggested factor: {c_factor:.1f}")
    
    print(f"Noise estimate: {noise:.1f} ({n_assessment})")
    print(f"  → Suggested reduction: {n_reduce:.1f}")
    
    if channel_means:
        print(f"Color Balance: R={channel_means['R']:.0f}, G={channel_means['G']:.0f}, B={channel_means['B']:.0f}")
        print(f"  → Color cast: {color_cast}")
    
    return {
        'brightness': b_adjust,
        'contrast': c_factor,
        'noise_reduction': n_reduce,
        'color_cast': color_cast
    }


# ============================================================
# FUNGSI ENHANCEMENT
# ============================================================

def adjust_brightness_contrast(gambar, brightness=0, contrast=1.0):
    """
    # Keterangan: Jalankan perintah berikut.
    Adjust brightness dan contrast
    
    # Keterangan: Inisialisasi beberapa variabel (g(x,y)).
    g(x,y) = contrast × f(x,y) + brightness
    """
    result = cv2.convertScaleAbs(gambar, alpha=contrast, beta=brightness)
    return result


def gamma_correction(gambar, gamma=1.0):
    """
    # Keterangan: Jalankan perintah berikut.
    Koreksi gamma untuk non-linear brightness adjustment
    
    # Keterangan: Inisialisasi beberapa variabel (g(x,y)).
    g(x,y) = 255 × (f(x,y)/255)^(1/gamma)
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(gambar, table)


def auto_gamma(gambar):
    """
    # Keterangan: Jalankan perintah berikut.
    Auto gamma correction berdasarkan mean intensity
    """
    if len(gambar.shape) == 3:
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    else:
        gray = gambar
    
    mean_intensity = np.mean(gray)
    
    # Target mean: 128
    gamma = np.log(128 / 255) / np.log(mean_intensity / 255)
    gamma = np.clip(gamma, 0.5, 2.5)
    
    return gamma_correction(gambar, gamma), gamma


def denoise(gambar, strength=0.5):
    """
    # Keterangan: Jalankan perintah berikut.
    Noise reduction menggunakan bilateral filter atau fastNlMeans
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - strength: 0.0 (no denoising) to 1.0 (strong denoising)
    """
    if strength <= 0:
        return gambar
    
    # Scale parameters based on strength
    h = int(3 + strength * 7)  # 3-10
    
    if len(gambar.shape) == 3:
        # Color image
        denoised = cv2.fastNlMeansDenoisingColored(gambar, None, h, h, 7, 21)
    else:
        # Grayscale
        denoised = cv2.fastNlMeansDenoising(gambar, None, h, 7, 21)
    
    return denoised


def adjust_saturation(gambar, factor=1.0):
    """
    # Keterangan: Jalankan perintah berikut.
    Adjust saturation dari gambar berwarna
    
    # Keterangan: Jalankan perintah berikut.
    factor > 1: lebih saturated
    # Keterangan: Jalankan perintah berikut.
    factor < 1: less saturated
    # Keterangan: Inisialisasi atau perbarui variabel factor.
    factor = 0: grayscale
    """
    if len(gambar.shape) != 3:
        return gambar
    
    # Convert ke HSV
    hsv = cv2.cvtColor(gambar, cv2.COLOR_BGR2HSV).astype(np.float64)
    
    # Adjust saturation
    hsv[:, :, 1] = hsv[:, :, 1] * factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    
    # Convert back
    hsv = hsv.astype(np.uint8)
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return result


def sharpen(gambar, strength=1.0):
    """
    # Keterangan: Jalankan perintah berikut.
    Sharpening dengan unsharp masking
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - strength: 0.0 (no sharpening) to 2.0 (strong sharpening)
    """
    if strength <= 0:
        return gambar
    
    blurred = cv2.GaussianBlur(gambar, (0, 0), 3)
    sharpened = cv2.addWeighted(gambar, 1 + strength, blurred, -strength, 0)
    
    return sharpened


def clahe_enhancement(gambar, clip_limit=2.0, tile_size=(8, 8)):
    """
    # Keterangan: Jalankan perintah berikut.
    CLAHE untuk contrast enhancement
    """
    if len(gambar.shape) == 3:
        # Color image - apply to L channel
        lab = cv2.cvtColor(gambar, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        result = clahe.apply(gambar)
    
    return result


def white_balance(gambar, method='gray_world'):
    """
    # Keterangan: Jalankan perintah berikut.
    Auto white balance correction
    
    # Keterangan: Mulai blok kode baru.
    Methods:
    # Keterangan: Jalankan perintah berikut.
    - 'gray_world': assumes average color should be gray
    # Keterangan: Jalankan perintah berikut.
    - 'white_patch': assumes brightest pixel should be white
    """
    if len(gambar.shape) != 3:
        return gambar
    
    if method == 'gray_world':
        # Gray World assumption
        b, g, r = cv2.split(gambar.astype(np.float64))
        b_avg, g_avg, r_avg = np.mean(b), np.mean(g), np.mean(r)
        avg = (b_avg + g_avg + r_avg) / 3
        
        b = np.clip(b * (avg / b_avg), 0, 255)
        g = np.clip(g * (avg / g_avg), 0, 255)
        r = np.clip(r * (avg / r_avg), 0, 255)
        
        result = cv2.merge([b, g, r]).astype(np.uint8)
        
    elif method == 'white_patch':
        # White Patch assumption
        b, g, r = cv2.split(gambar.astype(np.float64))
        b_max, g_max, r_max = np.max(b), np.max(g), np.max(r)
        
        b = np.clip(b * (255 / b_max), 0, 255)
        g = np.clip(g * (255 / g_max), 0, 255)
        r = np.clip(r * (255 / r_max), 0, 255)
        
        result = cv2.merge([b, g, r]).astype(np.uint8)
    else:
        result = gambar
    
    return result


# ============================================================
# ENHANCEMENT PRESETS
# ============================================================

def get_preset_parameters(preset_name):
    """
    # Keterangan: Jalankan perintah berikut.
    Mendapatkan parameter enhancement berdasarkan preset
    """
    presets = {
        'natural': {
            'brightness': 0,
            'contrast': 1.0,
            'gamma': 1.0,
            'saturation': 1.0,
            'sharpness': 0.3,
            'clahe_clip': 2.0,
            'denoise': 0.3
        },
        'vivid': {
            'brightness': 5,
            'contrast': 1.1,
            'gamma': 0.95,
            'saturation': 1.3,
            'sharpness': 0.5,
            'clahe_clip': 2.5,
            'denoise': 0.2
        },
        'dramatic': {
            'brightness': 0,
            'contrast': 1.3,
            'gamma': 0.85,
            'saturation': 1.1,
            'sharpness': 0.7,
            'clahe_clip': 3.0,
            'denoise': 0.3
        },
        'vintage': {
            'brightness': -5,
            'contrast': 0.9,
            'gamma': 1.1,
            'saturation': 0.7,
            'sharpness': 0.0,
            'clahe_clip': 1.5,
            'denoise': 0.4
        },
        'cinematic': {
            'brightness': -10,
            'contrast': 1.2,
            'gamma': 0.9,
            'saturation': 0.85,
            'sharpness': 0.3,
            'clahe_clip': 2.0,
            'denoise': 0.3
        }
    }
    
    return presets.get(preset_name, presets['natural'])


# ============================================================
# PIPELINE ENHANCEMENT
# ============================================================

def enhancement_pipeline_manual(gambar, params):
    """
    # Keterangan: Jalankan perintah berikut.
    Pipeline enhancement dengan parameter manual
    
    # Keterangan: Mulai blok kode baru.
    Parameter:
    # Keterangan: Jalankan perintah berikut.
    - brightness: -100 to 100
    # Keterangan: Jalankan perintah berikut.
    - contrast: 0.5 to 2.0
    # Keterangan: Jalankan perintah berikut.
    - gamma: 0.5 to 2.5
    # Keterangan: Jalankan perintah berikut.
    - saturation: 0.5 to 2.0
    # Keterangan: Jalankan perintah berikut.
    - sharpness: 0.0 to 2.0
    # Keterangan: Jalankan perintah berikut.
    - clahe_clip: CLAHE clip limit
    # Keterangan: Jalankan perintah berikut.
    - denoise: 0.0 to 1.0
    """
    result = gambar.copy()
    
    # 1. Denoise (dilakukan pertama untuk hasil lebih baik)
    if params.get('denoise', 0) > 0:
        result = denoise(result, params['denoise'])
    
    # 2. White balance (jika color cast terdeteksi)
    if params.get('white_balance', False):
        result = white_balance(result)
    
    # 3. CLAHE untuk contrast enhancement
    if params.get('clahe_clip', 0) > 0:
        result = clahe_enhancement(result, params['clahe_clip'])
    
    # 4. Brightness & Contrast
    brightness = params.get('brightness', 0)
    contrast = params.get('contrast', 1.0)
    if brightness != 0 or contrast != 1.0:
        result = adjust_brightness_contrast(result, brightness, contrast)
    
    # 5. Gamma correction
    gamma = params.get('gamma', 1.0)
    if gamma != 1.0:
        result = gamma_correction(result, gamma)
    
    # 6. Saturation
    saturation = params.get('saturation', 1.0)
    if saturation != 1.0:
        result = adjust_saturation(result, saturation)
    
    # 7. Sharpening (dilakukan terakhir)
    sharpness = params.get('sharpness', 0)
    if sharpness > 0:
        result = sharpen(result, sharpness)
    
    return result


def enhancement_pipeline_auto(gambar):
    """
    # Keterangan: Jalankan perintah berikut.
    Pipeline enhancement otomatis berdasarkan analisis gambar
    """
    # Analisis gambar
    analysis = analisis_lengkap(gambar)
    
    # Build parameters
    params = {
        'brightness': analysis['brightness'],
        'contrast': analysis['contrast'],
        'denoise': analysis['noise_reduction'],
        'white_balance': analysis['color_cast'] != 'balanced',
        'clahe_clip': 2.0,
        'gamma': 1.0,
        'saturation': 1.0,
        'sharpness': 0.3
    }
    
    # Auto gamma jika sangat gelap/terang
    if abs(analysis['brightness']) > 20:
        _, auto_g = auto_gamma(gambar)
        params['gamma'] = auto_g
        params['brightness'] = 0  # Gamma sudah handle brightness
    
    print("\n" + "-" * 40)
    print("AUTO-ENHANCEMENT PARAMETERS")
    print("-" * 40)
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    return enhancement_pipeline_manual(gambar, params), params


def enhancement_pipeline_preset(gambar, preset_name='natural'):
    """
    # Keterangan: Jalankan perintah berikut.
    Pipeline enhancement menggunakan preset
    """
    params = get_preset_parameters(preset_name)
    print(f"\n[INFO] Using preset: {preset_name}")
    
    return enhancement_pipeline_manual(gambar, params), params


# ============================================================
# FUNGSI DEMONSTRASI
# ============================================================

def demo_pipeline_steps():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi setiap langkah dalam pipeline
    """
    print("\n" + "=" * 60)
    print("LANGKAH-LANGKAH ENHANCEMENT PIPELINE")
    print("=" * 60)
    
    print("""
# Keterangan: Mulai blok kode baru.
URUTAN PIPELINE YANG DISARANKAN:

# Keterangan: Jalankan perintah berikut.
1. DENOISE
   # Keterangan: Jalankan perintah berikut.
   └── Kurangi noise sebelum enhancement lain
       # Keterangan: Jalankan perintah berikut.
       (Enhancement akan mengamplifikasi noise)

# Keterangan: Jalankan perintah berikut.
2. WHITE BALANCE
   # Keterangan: Jalankan perintah berikut.
   └── Koreksi color cast jika ada

# Keterangan: Jalankan perintah berikut.
3. CLAHE
   # Keterangan: Jalankan perintah berikut.
   └── Adaptive contrast enhancement
       # Keterangan: Jalankan perintah berikut.
       (Lebih natural dari global contrast)

# Keterangan: Jalankan perintah berikut.
4. BRIGHTNESS & CONTRAST
   # Keterangan: Jalankan perintah berikut.
   └── Fine-tune setelah CLAHE

# Keterangan: Jalankan perintah berikut.
5. GAMMA CORRECTION
   # Keterangan: Jalankan perintah berikut.
   └── Non-linear adjustment untuk midtones

# Keterangan: Jalankan perintah berikut.
6. SATURATION
   # Keterangan: Jalankan perintah berikut.
   └── Adjust color vibrance

# Keterangan: Jalankan perintah berikut.
7. SHARPENING
   # Keterangan: Jalankan perintah berikut.
   └── TERAKHIR! Karena akan mengamplifikasi noise
    """)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Apply setiap langkah
    steps = [
        ("Original", gambar),
        ("1. Denoise", denoise(gambar, 0.5)),
    ]
    
    current = steps[-1][1]
    current = white_balance(current)
    steps.append(("2. White Balance", current.copy()))
    
    current = clahe_enhancement(current, 2.0)
    steps.append(("3. CLAHE", current.copy()))
    
    current = adjust_brightness_contrast(current, 10, 1.1)
    steps.append(("4. Brightness/Contrast", current.copy()))
    
    current = gamma_correction(current, 0.95)
    steps.append(("5. Gamma", current.copy()))
    
    current = adjust_saturation(current, 1.1)
    steps.append(("6. Saturation", current.copy()))
    
    current = sharpen(current, 0.5)
    steps.append(("7. Sharpen", current.copy()))
    
    # Visualisasi
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    for i, (title, img) in enumerate(steps):
        axes[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[i].set_title(title)
        axes[i].axis('off')
    
    # Hide unused axes
    for i in range(len(steps), len(axes)):
        axes[i].axis('off')
    
    plt.suptitle("Enhancement Pipeline Step-by-Step", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_presets():
    """
    # Keterangan: Jalankan perintah berikut.
    Demonstrasi berbagai enhancement presets
    """
    print("\n" + "=" * 60)
    print("ENHANCEMENT PRESETS")
    print("=" * 60)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    presets = ['natural', 'vivid', 'dramatic', 'vintage', 'cinematic']
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Original
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    # Presets
    for i, preset in enumerate(presets):
        enhanced, _ = enhancement_pipeline_preset(gambar, preset)
        axes[i + 1].imshow(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
        axes[i + 1].set_title(f"Preset: {preset.upper()}")
        axes[i + 1].axis('off')
    
    plt.suptitle("Enhancement Presets", fontsize=14)
    plt.tight_layout()
    plt.show()


def demo_auto_vs_manual():
    """
    # Keterangan: Jalankan perintah berikut.
    Perbandingan auto enhancement vs manual
    """
    print("\n" + "=" * 60)
    print("AUTO vs MANUAL ENHANCEMENT")
    print("=" * 60)
    
    # Load gambar
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    if os.path.exists(path_gambar):
        gambar = cv2.imread(path_gambar)
    else:
        gambar = buat_gambar_sample()
    
    # Auto enhancement
    auto_result, auto_params = enhancement_pipeline_auto(gambar)
    
    # Manual enhancement dengan parameter kustom
    manual_params = {
        'brightness': MANUAL_BRIGHTNESS,
        'contrast': MANUAL_CONTRAST,
        'gamma': MANUAL_GAMMA,
        'saturation': MANUAL_SATURATION,
        'sharpness': MANUAL_SHARPNESS,
        'denoise': NOISE_REDUCTION,
        'clahe_clip': 2.0
    }
    manual_result = enhancement_pipeline_manual(gambar, manual_params)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(auto_result, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Auto Enhancement")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(manual_result, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Manual Enhancement")
    axes[2].axis('off')
    
    plt.suptitle("Auto vs Manual Enhancement", fontsize=14)
    plt.tight_layout()
    plt.show()


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():
    """Fungsi utama program"""
    
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("PRAKTIKUM: IMAGE ENHANCEMENT PIPELINE")
    # Keterangan: Jalankan perintah berikut.
    print("Bab 3 - Pemrosesan Citra")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    
    print("""
IMAGE ENHANCEMENT PIPELINE menggabungkan berbagai teknik
image processing dalam urutan yang optimal untuk
menghasilkan gambar dengan kualitas terbaik.

Pipeline Steps:
1. Noise Reduction (denoise)
2. White Balance (color correction)
3. CLAHE (adaptive contrast)
4. Brightness & Contrast
5. Gamma Correction
6. Saturation Adjustment
7. Sharpening

Aplikasi:
├── Photo enhancement (Instagram, Lightroom)
├── Medical image preprocessing
├── Document scanning
├── Surveillance footage improvement
└── Preprocessing untuk computer vision
    """)
    
    # Load atau buat gambar
    # Keterangan: Inisialisasi atau perbarui variabel path_gambar.
    path_gambar = dapatkan_path_gambar(NAMA_FILE_GAMBAR)
    
    # Keterangan: Cek kondisi os.path.exists(path_gambar).
    if os.path.exists(path_gambar):
        # Keterangan: Jalankan perintah berikut.
        print(f"[INFO] Memuat gambar: {path_gambar}")
        # Keterangan: Baca gambar dari file ke array.
        gambar = cv2.imread(path_gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Jalankan perintah berikut.
        print("[INFO] Membuat gambar sample...")
        # Keterangan: Inisialisasi atau perbarui variabel gambar.
        gambar = buat_gambar_sample()
    
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Ukuran gambar: {gambar.shape}")
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Enhancement Mode: {ENHANCEMENT_MODE}")
    # Keterangan: Jalankan perintah berikut.
    print(f"[INFO] Preset: {PRESET}")
    
    # Apply enhancement
    # Keterangan: Inisialisasi atau perbarui variabel start_time.
    start_time = time.time()
    
    # Keterangan: Cek kondisi ENHANCEMENT_MODE == 'auto'.
    if ENHANCEMENT_MODE == 'auto':
        # Keterangan: Inisialisasi beberapa variabel (enhanced, params).
        enhanced, params = enhancement_pipeline_auto(gambar)
    # Keterangan: Jalankan blok else jika kondisi sebelumnya tidak terpenuhi.
    else:
        # Keterangan: Inisialisasi atau perbarui variabel params.
        params = {
            # Keterangan: Jalankan perintah berikut.
            'brightness': MANUAL_BRIGHTNESS,
            # Keterangan: Jalankan perintah berikut.
            'contrast': MANUAL_CONTRAST,
            # Keterangan: Jalankan perintah berikut.
            'gamma': MANUAL_GAMMA,
            # Keterangan: Jalankan perintah berikut.
            'saturation': MANUAL_SATURATION,
            # Keterangan: Jalankan perintah berikut.
            'sharpness': MANUAL_SHARPNESS,
            # Keterangan: Jalankan perintah berikut.
            'denoise': NOISE_REDUCTION,
            # Keterangan: Jalankan perintah berikut.
            'clahe_clip': 2.0
        # Keterangan: Jalankan perintah berikut.
        }
        # Keterangan: Inisialisasi atau perbarui variabel enhanced.
        enhanced = enhancement_pipeline_manual(gambar, params)
    
    # Keterangan: Inisialisasi atau perbarui variabel elapsed_time.
    elapsed_time = time.time() - start_time
    # Keterangan: Jalankan perintah berikut.
    print(f"\n[INFO] Enhancement completed in {elapsed_time:.3f} seconds")
    
    # Tampilkan hasil
    # Keterangan: Pilih area subplot untuk menampilkan hasil.
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Keterangan: Konversi ruang warna gambar.
    axes[0].imshow(cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[0].set_title("Original")
    # Keterangan: Jalankan perintah berikut.
    axes[0].axis('off')
    
    # Keterangan: Konversi ruang warna gambar.
    axes[1].imshow(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
    # Keterangan: Jalankan perintah berikut.
    axes[1].set_title(f"Enhanced ({ENHANCEMENT_MODE.upper()})")
    # Keterangan: Jalankan perintah berikut.
    axes[1].axis('off')
    
    # Keterangan: Rapikan jarak antar subplot.
    plt.tight_layout()
    # Keterangan: Jalankan perintah berikut.
    plt.show()
    
    # Demo tambahan
    # Keterangan: Jalankan perintah berikut.
    demo_pipeline_steps()
    # Keterangan: Jalankan perintah berikut.
    demo_presets()
    # Keterangan: Jalankan perintah berikut.
    demo_auto_vs_manual()
    
    # Ringkasan
    # Keterangan: Inisialisasi atau perbarui variabel print("\n" + ".
    print("\n" + "=" * 60)
    # Keterangan: Jalankan perintah berikut.
    print("RINGKASAN IMAGE ENHANCEMENT PIPELINE")
    # Keterangan: Inisialisasi atau perbarui variabel print(".
    print("=" * 60)
    print("""
PIPELINE STRUCTURE:

# 1. DENOISE - Selalu pertama!
denoised = cv2.fastNlMeansDenoisingColored(img, None, h, h, 7, 21)

# 2. WHITE BALANCE
# Gray World assumption
b, g, r = cv2.split(img)
avg = (np.mean(b) + np.mean(g) + np.mean(r)) / 3
balanced = cv2.merge([b*(avg/b.mean()), g*(avg/g.mean()), r*(avg/r.mean())])

# 3. CLAHE
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
lab[:,:,0] = clahe.apply(lab[:,:,0])
enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# 4. BRIGHTNESS & CONTRAST
adjusted = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

# 5. GAMMA CORRECTION
table = np.array([((i/255)^(1/gamma))*255 for i in range(256)])
gamma_corrected = cv2.LUT(img, table)

# 6. SATURATION
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv[:,:,1] = hsv[:,:,1] * factor
saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 7. SHARPENING - Selalu terakhir!
blurred = cv2.GaussianBlur(img, (0, 0), 3)
sharpened = cv2.addWeighted(img, 1+strength, blurred, -strength, 0)

TIPS:
1. Selalu analisis gambar dulu sebelum enhancement
2. Urutan pipeline sangat penting!
3. Denoise harus di awal, sharpen harus di akhir
4. Gunakan presets sebagai starting point
5. Fine-tune parameter sesuai kebutuhan spesifik
""")


# Jalankan program utama
# Keterangan: Cek kondisi __name__ == "__main__".
if __name__ == "__main__":
    # Keterangan: Jalankan perintah berikut.
    main()
