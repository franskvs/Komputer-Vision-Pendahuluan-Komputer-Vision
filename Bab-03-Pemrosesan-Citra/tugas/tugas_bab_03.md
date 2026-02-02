# TUGAS BAB 3: PEMROSESAN CITRA

## 📋 Informasi Tugas

| Aspek | Detail |
|-------|--------|
| **Deadline** | 1 minggu setelah praktikum |
| **Format** | Jupyter Notebook (.ipynb) atau Python (.py) + Laporan PDF |
| **Pengumpulan** | Melalui platform e-learning |

---

## Tugas 1: Teori (25 poin)

### Soal 1.1 (8 poin)
Diberikan gambar 5×5 berikut:
```
| 10  15  20  15  10 |
| 15  50  80  50  15 |
| 20  80  100 80  20 |
| 15  50  80  50  15 |
| 10  15  20  15  10 |
```

a) Hitung hasil konvolusi dengan kernel mean 3×3 untuk pixel tengah (2,2). Gunakan zero-padding.

b) Hitung hasil konvolusi dengan kernel Sobel-X untuk pixel (2,2).

c) Hitung gradient magnitude dan direction untuk pixel (2,2).

d) Jelaskan mengapa hasil Sobel-X untuk gambar ini adalah 0.

### Soal 1.2 (7 poin)
Jelaskan perbedaan antara:

a) Gaussian filter vs Box filter (3 poin)
   - Bagaimana kernel mereka berbeda?
   - Mengapa Gaussian lebih baik untuk smoothing?
   - Apa yang dimaksud dengan "separable filter"?

b) Median filter vs Mean filter (2 poin)
   - Kapan median filter lebih baik?
   - Berikan contoh kasus penggunaan.

c) Bilateral filter vs Gaussian filter (2 poin)
   - Apa keunggulan bilateral filter?
   - Jelaskan parameter σ_space dan σ_color.

### Soal 1.3 (5 poin)
Tentang Fourier Transform:

a) Apa yang direpresentasikan oleh low frequency dan high frequency dalam spektrum Fourier?

b) Mengapa kita menggunakan log scale untuk menampilkan magnitude spectrum?

c) Jelaskan mengapa phase lebih penting dari magnitude untuk rekonstruksi gambar.

### Soal 1.4 (5 poin)
Tentang Canny Edge Detection:

a) Jelaskan fungsi dari setiap langkah dalam algoritma Canny.

b) Apa tujuan dari double thresholding dan hysteresis?

c) Bagaimana memilih nilai threshold yang tepat?

---

## Tugas 2: Coding - Image Filter Toolkit (35 poin)

### 2.1 Custom Filter Implementation (15 poin)

```python
"""
Implementasikan class ImageFilterToolkit dengan berbagai filter
"""

import numpy as np
import cv2

class ImageFilterToolkit:
    def __init__(self, image):
        """
        Initialize dengan gambar
        
        Parameters:
            image: numpy array (dapat grayscale atau BGR)
        """
        self.original = image.copy()
        self.current = image.copy()
        self.history = []  # Menyimpan history untuk undo
    
    def reset(self):
        """Reset ke gambar original"""
        # Implementasi Anda
        pass
    
    def undo(self):
        """Undo operasi terakhir"""
        # Implementasi Anda
        pass
    
    def _save_state(self):
        """Save current state to history"""
        # Implementasi Anda
        pass
    
    # ===== POINT OPERATORS =====
    
    def adjust_brightness_contrast(self, alpha=1.0, beta=0):
        """
        Atur brightness dan contrast
        g(x) = alpha * f(x) + beta
        """
        # Implementasi Anda
        pass
    
    def apply_gamma(self, gamma=1.0):
        """Gamma correction"""
        # Implementasi Anda
        pass
    
    def histogram_equalize(self, method='standard'):
        """
        Histogram equalization
        
        Parameters:
            method: 'standard' atau 'clahe'
        """
        # Implementasi Anda
        pass
    
    def invert(self):
        """Invert image (negative)"""
        # Implementasi Anda
        pass
    
    # ===== SMOOTHING FILTERS =====
    
    def blur_box(self, ksize=5):
        """Box (mean) blur"""
        # Implementasi Anda
        pass
    
    def blur_gaussian(self, ksize=5, sigma=1.0):
        """Gaussian blur"""
        # Implementasi Anda
        pass
    
    def blur_median(self, ksize=5):
        """Median blur"""
        # Implementasi Anda
        pass
    
    def blur_bilateral(self, d=9, sigma_color=75, sigma_space=75):
        """Bilateral filter"""
        # Implementasi Anda
        pass
    
    # ===== SHARPENING FILTERS =====
    
    def sharpen(self, strength=1.0):
        """
        Unsharp masking
        sharpened = original + strength * (original - blurred)
        """
        # Implementasi Anda
        pass
    
    def apply_laplacian(self, return_edges=False):
        """
        Laplacian sharpening atau edge detection
        """
        # Implementasi Anda
        pass
    
    # ===== EDGE DETECTION =====
    
    def detect_edges_sobel(self, direction='both'):
        """
        Sobel edge detection
        
        Parameters:
            direction: 'x', 'y', atau 'both'
        
        Returns:
            gradient magnitude (and direction if 'both')
        """
        # Implementasi Anda
        pass
    
    def detect_edges_canny(self, low_thresh=50, high_thresh=150):
        """Canny edge detection"""
        # Implementasi Anda
        pass
    
    # ===== MORPHOLOGICAL OPERATIONS =====
    
    def morphology(self, operation, kernel_size=5, kernel_shape='rect', iterations=1):
        """
        Morphological operations
        
        Parameters:
            operation: 'erode', 'dilate', 'open', 'close', 'gradient'
            kernel_shape: 'rect', 'ellipse', 'cross'
        """
        # Implementasi Anda
        pass
    
    # ===== FREQUENCY DOMAIN =====
    
    def frequency_filter(self, filter_type='lowpass', cutoff=30):
        """
        Filtering in frequency domain
        
        Parameters:
            filter_type: 'lowpass' atau 'highpass'
            cutoff: frequency cutoff
        """
        # Implementasi Anda
        pass
    
    def get_spectrum(self):
        """
        Get magnitude and phase spectrum
        
        Returns:
            magnitude, phase
        """
        # Implementasi Anda
        pass
    
    # ===== UTILITY =====
    
    def apply_custom_kernel(self, kernel):
        """Apply custom convolution kernel"""
        # Implementasi Anda
        pass
    
    def get_histogram(self):
        """Get histogram of current image"""
        # Implementasi Anda
        pass
    
    def compare_with_original(self, title="Comparison"):
        """Visualize side-by-side comparison with original"""
        # Implementasi Anda
        pass
    
    def get_statistics(self):
        """Get image statistics (min, max, mean, std)"""
        # Implementasi Anda
        pass


# Contoh penggunaan
if __name__ == "__main__":
    # Load gambar
    img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
    
    # Buat toolkit
    toolkit = ImageFilterToolkit(img)
    
    # Chain operations
    toolkit.blur_gaussian(sigma=1.5)
    toolkit.sharpen(strength=1.2)
    toolkit.adjust_brightness_contrast(alpha=1.1, beta=10)
    
    # Visualisasi
    toolkit.compare_with_original()
    
    # Undo
    toolkit.undo()
    
    # Edge detection
    toolkit.reset()
    toolkit.detect_edges_canny(50, 150)
```

### 2.2 Fourier Domain Filter (10 poin)

```python
"""
Implementasikan berbagai filter di domain frekuensi
"""

def create_filter(shape, filter_type, cutoff, order=2):
    """
    Create frequency domain filter
    
    Parameters:
        shape: (rows, cols) - ukuran gambar
        filter_type: 'ideal_lpf', 'ideal_hpf', 
                     'butterworth_lpf', 'butterworth_hpf',
                     'gaussian_lpf', 'gaussian_hpf'
        cutoff: cutoff frequency D0
        order: order untuk Butterworth filter
    
    Returns:
        H: filter dalam domain frekuensi (sudah di-shift)
    """
    # Implementasi Anda
    pass


def apply_frequency_filter(image, filter_type, cutoff, order=2):
    """
    Apply filter in frequency domain
    
    Parameters:
        image: input grayscale image
        filter_type: jenis filter
        cutoff: cutoff frequency
        order: order (untuk Butterworth)
    
    Returns:
        filtered_image: hasil filtering
        spectrum_before: magnitude spectrum sebelum filter
        spectrum_after: magnitude spectrum setelah filter
    """
    # Implementasi Anda
    pass


def visualize_frequency_filtering(image, filter_type, cutoff, order=2):
    """
    Visualisasi lengkap proses filtering frekuensi
    - Original image
    - Spectrum before
    - Filter
    - Spectrum after
    - Filtered image
    """
    # Implementasi Anda
    pass


# Test berbagai filter
if __name__ == "__main__":
    img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
    
    # Bandingkan berbagai low-pass filter
    cutoffs = [10, 30, 50, 80]
    
    for D0 in cutoffs:
        visualize_frequency_filtering(img, 'gaussian_lpf', D0)
    
    # Bandingkan Butterworth dengan berbagai order
    orders = [1, 2, 5, 10]
    for n in orders:
        visualize_frequency_filtering(img, 'butterworth_lpf', 30, n)
```

### 2.3 Noise Reduction Comparison (10 poin)

```python
"""
Bandingkan berbagai metode noise reduction
"""

def add_noise(image, noise_type, params):
    """
    Add noise to image
    
    Parameters:
        noise_type: 'gaussian', 'salt_pepper', 'poisson', 'speckle'
        params: dictionary dengan parameter noise
    
    Returns:
        noisy_image
    """
    # Implementasi Anda
    pass


def evaluate_denoising(original, denoised):
    """
    Evaluate denoising quality
    
    Returns:
        psnr: Peak Signal-to-Noise Ratio
        ssim: Structural Similarity Index
        mse: Mean Squared Error
    """
    # Implementasi Anda
    pass


def compare_denoising_methods(image, noise_type, noise_params):
    """
    Compare multiple denoising methods on same noisy image
    
    Methods to compare:
    1. Gaussian blur (berbagai sigma)
    2. Median filter (berbagai size)
    3. Bilateral filter (berbagai parameter)
    4. Non-local means (jika tersedia)
    
    Visualize:
    - Original
    - Noisy
    - All denoised results with metrics
    """
    # Implementasi Anda
    pass


# Test
if __name__ == "__main__":
    img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
    
    # Test untuk berbagai jenis noise
    noise_types = [
        ('gaussian', {'sigma': 25}),
        ('salt_pepper', {'amount': 0.05}),
    ]
    
    for noise_type, params in noise_types:
        compare_denoising_methods(img, noise_type, params)
```

---

## Tugas 3: Mini Project - Image Enhancement Tool (40 poin)

### Deskripsi
Buat aplikasi Image Enhancement Tool yang lengkap dengan GUI atau command-line interface.

### Requirements

```python
"""
Image Enhancement Tool
======================

Fitur yang harus ada:
1. Load dan save gambar (berbagai format)
2. Point operations (brightness, contrast, gamma, histogram eq)
3. Smoothing filters (Gaussian, median, bilateral)
4. Sharpening (unsharp masking, Laplacian)
5. Edge detection (Sobel, Canny)
6. Frequency domain filtering
7. Preset enhancement profiles
8. Batch processing
9. Real-time preview
10. Before/After comparison
"""

import numpy as np
import cv2
import argparse
from pathlib import Path

class ImageEnhancer:
    """Main class untuk image enhancement"""
    
    # Preset profiles
    PRESETS = {
        'auto_enhance': {
            'clahe': {'clip_limit': 2.0},
            'sharpen': {'strength': 0.5}
        },
        'portrait': {
            'bilateral': {'d': 9, 'sigma_color': 75, 'sigma_space': 75},
            'brightness': {'alpha': 1.05, 'beta': 5}
        },
        'landscape': {
            'clahe': {'clip_limit': 3.0},
            'saturation': {'factor': 1.2},
            'sharpen': {'strength': 0.3}
        },
        'vintage': {
            'sepia': True,
            'vignette': {'strength': 0.3},
            'contrast': {'alpha': 0.9}
        },
        'sharpen_only': {
            'unsharp_mask': {'sigma': 1.5, 'strength': 1.5}
        },
        'denoise_light': {
            'bilateral': {'d': 5, 'sigma_color': 50, 'sigma_space': 50}
        },
        'denoise_heavy': {
            'nlm': {'h': 10, 'template_window': 7, 'search_window': 21}
        }
    }
    
    def __init__(self, image_path=None):
        """Initialize enhancer"""
        self.original = None
        self.current = None
        self.history = []
        
        if image_path:
            self.load(image_path)
    
    def load(self, path):
        """Load image from file"""
        # Implementasi Anda
        pass
    
    def save(self, path, quality=95):
        """Save current image"""
        # Implementasi Anda
        pass
    
    def reset(self):
        """Reset ke original"""
        # Implementasi Anda
        pass
    
    def undo(self):
        """Undo last operation"""
        # Implementasi Anda
        pass
    
    # ===== Enhancement Methods =====
    
    def auto_enhance(self):
        """Automatic enhancement using multiple techniques"""
        # Implementasi Anda
        pass
    
    def apply_preset(self, preset_name):
        """Apply preset enhancement profile"""
        # Implementasi Anda
        pass
    
    def adjust_levels(self, black_point=0, white_point=255, gamma=1.0):
        """Levels adjustment like Photoshop"""
        # Implementasi Anda
        pass
    
    def adjust_curves(self, curve_points):
        """
        Curves adjustment
        
        Parameters:
            curve_points: list of (input, output) tuples
        """
        # Implementasi Anda
        pass
    
    def adjust_hsl(self, hue=0, saturation=1.0, lightness=0):
        """HSL adjustment"""
        # Implementasi Anda
        pass
    
    def add_vignette(self, strength=0.5):
        """Add vignette effect"""
        # Implementasi Anda
        pass
    
    def apply_sepia(self, strength=1.0):
        """Apply sepia tone"""
        # Implementasi Anda
        pass
    
    def smart_sharpen(self, amount=1.0, radius=1.0, threshold=0):
        """
        Smart sharpen dengan edge preservation
        
        Parameters:
            amount: strength of sharpening
            radius: Gaussian radius
            threshold: threshold untuk edge detection
        """
        # Implementasi Anda
        pass
    
    def reduce_noise(self, method='bilateral', strength='medium'):
        """
        Noise reduction
        
        Parameters:
            method: 'bilateral', 'nlm', 'wavelet'
            strength: 'light', 'medium', 'heavy'
        """
        # Implementasi Anda
        pass
    
    def local_contrast(self, clip_limit=2.0, tile_size=8):
        """Enhance local contrast using CLAHE"""
        # Implementasi Anda
        pass
    
    def dehaze(self, strength=1.0):
        """
        Remove haze from image
        Hint: Dark channel prior
        """
        # Implementasi Anda
        pass
    
    # ===== Batch Processing =====
    
    @staticmethod
    def batch_process(input_folder, output_folder, operations):
        """
        Process multiple images
        
        Parameters:
            input_folder: path to input images
            output_folder: path for output
            operations: list of (operation_name, params) tuples
        """
        # Implementasi Anda
        pass
    
    # ===== Analysis =====
    
    def analyze(self):
        """
        Analyze image and suggest enhancements
        
        Returns:
            dict with analysis results and suggestions
        """
        # Implementasi Anda
        # - Check brightness (suggest gamma/brightness adjustment)
        # - Check contrast (suggest histogram eq/CLAHE)
        # - Check noise level (suggest denoising)
        # - Check sharpness (suggest sharpening)
        pass
    
    def compare(self, title="Before / After"):
        """Show before/after comparison"""
        # Implementasi Anda
        pass
    
    def export_report(self, path):
        """Export enhancement report with all settings"""
        # Implementasi Anda
        pass


def create_cli():
    """Create command-line interface"""
    parser = argparse.ArgumentParser(description='Image Enhancement Tool')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('-o', '--output', help='Output path')
    parser.add_argument('-p', '--preset', choices=ImageEnhancer.PRESETS.keys(),
                        help='Apply preset')
    parser.add_argument('--auto', action='store_true', help='Auto enhance')
    parser.add_argument('--brightness', type=float, help='Brightness adjustment')
    parser.add_argument('--contrast', type=float, help='Contrast adjustment')
    parser.add_argument('--sharpen', type=float, help='Sharpen strength')
    parser.add_argument('--denoise', choices=['light', 'medium', 'heavy'],
                        help='Denoise strength')
    parser.add_argument('--batch', help='Batch process folder')
    parser.add_argument('--analyze', action='store_true', help='Analyze image')
    
    return parser


if __name__ == "__main__":
    # CLI mode
    parser = create_cli()
    args = parser.parse_args()
    
    enhancer = ImageEnhancer(args.input)
    
    if args.analyze:
        analysis = enhancer.analyze()
        print("Image Analysis:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")
    
    if args.auto:
        enhancer.auto_enhance()
    
    if args.preset:
        enhancer.apply_preset(args.preset)
    
    if args.brightness:
        enhancer.adjust_brightness_contrast(beta=args.brightness)
    
    if args.contrast:
        enhancer.adjust_brightness_contrast(alpha=args.contrast)
    
    if args.sharpen:
        enhancer.smart_sharpen(amount=args.sharpen)
    
    if args.denoise:
        enhancer.reduce_noise(strength=args.denoise)
    
    if args.output:
        enhancer.save(args.output)
        print(f"Saved to {args.output}")
    else:
        enhancer.compare()
```

### Kriteria Penilaian Mini Project

| Kriteria | Poin |
|----------|------|
| Point operations lengkap | 8 |
| Filters lengkap | 8 |
| Preset system bekerja | 5 |
| Batch processing | 5 |
| Image analysis | 5 |
| Code quality & documentation | 5 |
| GUI/CLI interface | 4 |
| **Bonus: GUI dengan preview** | +10 |

---

## Rubrik Penilaian Total

| Komponen | Poin |
|----------|------|
| Tugas 1: Teori | 25 |
| Tugas 2: Coding | 35 |
| Tugas 3: Mini Project | 40 |
| **Total** | **100** |
| Bonus | +10 |

---

## Ketentuan Pengumpulan

1. **Nama file**: `Tugas3_NIM_Nama.zip`
2. **Isi ZIP**:
   - `tugas1_teori.pdf` - Jawaban teori
   - `tugas2_filter_toolkit.py`
   - `tugas2_frequency_filter.py`
   - `tugas2_noise_comparison.py`
   - `mini_project/` - Folder mini project
   - `README.md` - Dokumentasi
   - `sample_outputs/` - Contoh output
3. **Keterlambatan**: -10 poin per hari

---

## Tips

1. Untuk konvolusi manual, pastikan handling border dengan benar
2. Gunakan `cv2.filter2D()` untuk kecepatan, implementasi manual untuk pemahaman
3. Test dengan gambar sederhana (gradien, edge) untuk validasi
4. Gunakan PSNR dan SSIM untuk evaluasi kuantitatif
5. Dokumentasikan parameter yang digunakan

---

**Selamat mengerjakan!** 🎉
