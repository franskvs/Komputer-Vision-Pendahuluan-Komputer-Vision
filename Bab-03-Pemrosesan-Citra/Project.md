# Project: Sistem Peningkatan Kualitas Citra Otomatis
## Bab 3: Pemrosesan Citra

---

## 📖 Latar Belakang

### Skenario Industri

**Nama Perusahaan:** PhotoFix AI - Startup Editing Foto Otomatis

**Situasi:**
Di era smartphone, jutaan foto diambil setiap hari dengan kualitas yang bervariasi. PhotoFix AI adalah startup yang mengembangkan aplikasi untuk secara otomatis meningkatkan kualitas foto dengan satu klik. Tim engineering sedang mengembangkan algoritma core untuk:
- Mendeteksi masalah kualitas foto secara otomatis
- Menerapkan perbaikan yang sesuai
- Memberikan hasil yang natural tanpa over-processing

**Klien Utama:**
- Platform e-commerce (perbaikan foto produk)
- Social media apps (pre-upload enhancement)
- Arsip digital (restorasi foto lama)
- Medical imaging (enhancement untuk diagnosis)

**Tantangan:**
1. Foto dari berbagai kondisi (indoor, outdoor, low-light)
2. Berbagai jenis kamera dengan karakteristik berbeda
3. User mengharapkan hasil yang cepat dan natural
4. Harus bisa berjalan di mobile devices (efisiensi)

---

## 🎯 Tujuan Project

Mengembangkan sistem **Auto Image Enhancement** yang dapat:
1. Menganalisis kualitas gambar secara otomatis
2. Menentukan jenis enhancement yang diperlukan
3. Menerapkan enhancement dengan parameter optimal
4. Menghasilkan output yang natural dan berkualitas

---

## 📋 Spesifikasi Teknis

### Input
- Format: JPEG, PNG
- Resolusi: Minimal 640×480, maksimal 4K
- Color space: RGB (8-bit per channel)

### Output
- Gambar enhanced dengan format yang sama
- Quality metrics (before/after)
- Enhancement report (apa yang dilakukan)

### Fitur Wajib (Minimum Requirements)

1. **Image Quality Analysis**
   - Deteksi brightness level (underexposed/overexposed/normal)
   - Deteksi contrast level (low/normal/high)
   - Deteksi noise level (low/medium/high)
   - Deteksi sharpness (blurry/normal/sharp)

2. **Automatic Enhancement**
   - Brightness/exposure correction
   - Contrast enhancement (CLAHE atau adaptive)
   - Noise reduction (dengan edge preservation)
   - Sharpening (tanpa artifacts)

3. **Enhancement Pipeline**
   - Urutan operasi yang optimal
   - Parameter yang disesuaikan dengan analisis
   - Option untuk adjust intensity (0-100%)

4. **User Interface (CLI)**
   - Single image processing
   - Batch processing
   - Preview mode
   - Export settings

### Fitur Opsional (Bonus)

1. **Advanced Analysis**
   - White balance detection
   - Color cast correction
   - Shadow/highlight detail recovery
   - Skin tone preservation mode

2. **Smart Enhancement**
   - Content-aware processing (face detection untuk skin smoothing)
   - Local adjustment (different areas get different treatment)
   - Style presets (portrait, landscape, product, document)

3. **GUI Application**
   - Before/after comparison slider
   - Real-time preview
   - Manual adjustment override
   - Undo/redo

4. **Performance Optimization**
   - GPU acceleration (CUDA/OpenCL)
   - Multi-threading untuk batch
   - Progressive processing untuk preview

---

## 📐 Panduan Implementasi

### Struktur Project

```
image-enhancement-system/
├── src/
│   ├── __init__.py
│   ├── analyzer.py         # Image quality analysis
│   ├── enhancer.py         # Enhancement algorithms
│   ├── pipeline.py         # Processing pipeline
│   ├── metrics.py          # Quality metrics
│   └── utils.py            # Helper functions
├── presets/
│   ├── portrait.json
│   ├── landscape.json
│   ├── product.json
│   └── document.json
├── tests/
│   ├── test_analyzer.py
│   ├── test_enhancer.py
│   └── test_images/
├── main.py                  # CLI interface
├── gui.py                   # GUI interface (optional)
├── requirements.txt
└── README.md
```

### Algoritma Analisis Kualitas

```python
class ImageAnalyzer:
    def analyze(self, image):
        """
        Analyze image quality and return metrics
        
        Returns:
        {
            'brightness': {
                'mean': float,      # 0-255
                'status': str,      # 'underexposed'/'normal'/'overexposed'
                'correction': float # suggested adjustment
            },
            'contrast': {
                'std': float,       # standard deviation
                'status': str,      # 'low'/'normal'/'high'
                'correction': float
            },
            'noise': {
                'level': float,     # estimated noise level
                'status': str,      # 'low'/'medium'/'high'
                'filter_strength': int
            },
            'sharpness': {
                'score': float,     # Laplacian variance
                'status': str,      # 'blurry'/'normal'/'sharp'
                'sharpen_amount': float
            },
            'histogram': {
                'distribution': str, # 'left-skewed'/'normal'/'right-skewed'
                'needs_equalization': bool
            }
        }
        """
```

### Algoritma Enhancement

```python
class ImageEnhancer:
    def enhance_brightness(self, image, target_mean=128):
        """Adjust brightness to target mean"""
        pass
    
    def enhance_contrast(self, image, method='clahe', clip_limit=2.0):
        """Enhance contrast using specified method"""
        pass
    
    def reduce_noise(self, image, strength=10, preserve_edges=True):
        """Reduce noise while preserving edges"""
        pass
    
    def sharpen(self, image, amount=1.0, radius=1.0, threshold=0):
        """Sharpen image using unsharp mask"""
        pass
    
    def auto_enhance(self, image, analysis=None, intensity=1.0):
        """
        Automatically enhance image based on analysis
        
        Parameters:
        - image: input image
        - analysis: pre-computed analysis (optional)
        - intensity: 0.0 to 1.0 (how strong the enhancement)
        """
        pass
```

### Pipeline Design

```python
class EnhancementPipeline:
    def __init__(self, config=None):
        self.analyzer = ImageAnalyzer()
        self.enhancer = ImageEnhancer()
        self.config = config or self.default_config()
    
    def process(self, image, preset=None):
        """
        Full processing pipeline
        
        Steps:
        1. Analyze input image
        2. Determine required enhancements
        3. Apply enhancements in optimal order:
           a. Noise reduction (if needed)
           b. Exposure/brightness correction
           c. Contrast enhancement
           d. Color correction (if needed)
           e. Sharpening (if needed)
        4. Generate quality report
        5. Return enhanced image + report
        """
        pass
```

### Quality Metrics

```python
def calculate_psnr(original, enhanced):
    """Peak Signal-to-Noise Ratio"""
    pass

def calculate_ssim(original, enhanced):
    """Structural Similarity Index"""
    pass

def calculate_brisque(image):
    """Blind/Referenceless Image Spatial Quality Evaluator"""
    pass
```

---

## 📊 Rubrik Penilaian

### Komponen Penilaian

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| Image Analysis | 25% | Akurasi deteksi masalah kualitas |
| Enhancement Quality | 30% | Hasil enhancement natural dan efektif |
| Pipeline Design | 20% | Urutan operasi optimal, kode modular |
| Dokumentasi | 15% | README, comments, API documentation |
| Bonus Features | 10% | Fitur tambahan yang berguna |

### Detail Penilaian

#### Image Analysis (25%)

| Skor | Kriteria |
|------|----------|
| 90-100 | Deteksi akurat untuk semua kondisi. Threshold yang well-tuned. Memberikan recommendations yang berguna. |
| 80-89 | Deteksi akurat untuk kebanyakan kondisi. Beberapa false positives/negatives. |
| 70-79 | Deteksi dasar bekerja. Beberapa kondisi tidak terdeteksi dengan baik. |
| 60-69 | Deteksi hanya untuk kondisi ekstrem. Banyak kesalahan klasifikasi. |
| <60 | Deteksi tidak konsisten atau tidak berfungsi. |

#### Enhancement Quality (30%)

| Skor | Kriteria |
|------|----------|
| 90-100 | Hasil sangat natural. Tidak ada artifacts. Efektif untuk berbagai jenis gambar. Before/after improvement jelas. |
| 80-89 | Hasil natural dengan minor artifacts pada kasus edge. Improvement terlihat jelas. |
| 70-79 | Hasil cukup baik. Beberapa gambar terlihat over-processed. |
| 60-69 | Enhancement terlihat tidak natural. Sering over-processed atau under-processed. |
| <60 | Hasil lebih buruk dari original atau banyak artifacts. |

#### Pipeline Design (20%)

| Skor | Kriteria |
|------|----------|
| 90-100 | Arsitektur sangat modular. Urutan operasi optimal dengan justifikasi. Easy to extend. Config-driven. |
| 80-89 | Arsitektur modular. Urutan operasi baik. Mudah di-maintain. |
| 70-79 | Struktur cukup terorganisir. Beberapa hardcoded values. |
| 60-69 | Struktur kurang modular. Sulit untuk dimodifikasi. |
| <60 | Tidak ada struktur jelas. Semua dalam satu function. |

---

## 📝 Deliverables

### 1. Source Code
- Repository dengan struktur yang jelas
- Code yang well-documented
- Unit tests untuk fungsi utama

### 2. Documentation
- README.md dengan:
  - Installation instructions
  - Usage examples
  - API documentation
  - Sample results

### 3. Report (PDF)
- Penjelasan algoritma yang digunakan
- Justifikasi design decisions
- Test results dengan berbagai jenis gambar
- Analisis kelebihan dan kekurangan

### 4. Demo
- Working demonstration
- Before/after comparisons
- Handling edge cases

---

## 📅 Timeline

| Minggu | Aktivitas |
|--------|-----------|
| 1 | Requirements analysis, design pipeline |
| 2 | Implement image analyzer |
| 3 | Implement enhancement algorithms |
| 4 | Integrate pipeline, testing |
| 5 | Documentation, final testing, demo |

---

## 💡 Tips Pengerjaan

### 1. Start with Analysis
- Buat analyzer yang akurat dulu
- Test dengan berbagai jenis gambar
- Fine-tune thresholds

### 2. Enhancement Order Matters
```
Recommended order:
1. Denoise (karena noise akan di-amplify oleh operasi lain)
2. Exposure correction (setelah noise berkurang)
3. Contrast enhancement (setelah exposure benar)
4. Color correction (pada gambar yang sudah balanced)
5. Sharpening (terakhir, setelah semua koreksi)
```

### 3. Avoid Over-processing
- Gunakan intensity parameter
- Blend dengan original jika perlu
- Test dengan gambar yang sudah bagus (shouldn't change much)

### 4. Edge Cases
- Gambar yang sangat gelap/terang
- Gambar dengan area berbeda (shadow & highlight)
- Gambar monochrome
- Gambar dengan noise tinggi

### 5. Performance
- Process pada resolusi lebih kecil untuk preview
- Cache intermediate results
- Use NumPy vectorization

---

## 📚 Referensi

1. **Automatic Color Equalization (ACE)**
   - Paper: Rizzi et al., "A New Algorithm for Unsupervised Global and Local Color Correction"

2. **Retinex Theory**
   - Paper: Land & McCann, "Lightness and Retinex Theory"

3. **Bilateral Filter**
   - Paper: Tomasi & Manduchi, "Bilateral Filtering for Gray and Color Images"

4. **CLAHE**
   - Paper: Zuiderveld, "Contrast Limited Adaptive Histogram Equalization"

5. **Unsharp Masking**
   - Book: Gonzalez & Woods, "Digital Image Processing"

---

*Project ini adalah bagian dari Praktikum Computer Vision*
