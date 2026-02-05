# Jobsheet Praktikum
## Bab 3: Pemrosesan Citra (Image Processing)

---

## 📋 Informasi Praktikum

| Item | Keterangan |
|------|------------|
| **Pertemuan** | 5-6 |
| **Durasi** | 2 × 100 menit |
| **Topik** | Point Operations, Filtering, Edge Detection, Morphology |

---

## 🎯 Tujuan Praktikum

Setelah menyelesaikan praktikum ini, mahasiswa mampu:
1. Mengimplementasikan operasi titik (brightness, contrast, gamma)
2. Menerapkan histogram equalization dan CLAHE
3. Menggunakan berbagai filter untuk noise reduction dan enhancement
4. Mengimplementasikan edge detection dengan Canny
5. Menerapkan morphological operations untuk binary image processing

---

## 🔧 Alat dan Bahan

### Software
- Python 3.8+
- OpenCV (opencv-python)
- NumPy
- Matplotlib

### File yang Diperlukan
```
Bab-03-Pemrosesan-Citra/
├── praktikum/
│   ├── 01_brightness_contrast.py
│   ├── 02_gamma_correction.py
│   ├── 03_thresholding.py
│   ├── 04_histogram_equalization.py
│   ├── 05_spatial_filtering.py
│   ├── 06_edge_detection.py
│   ├── 07_morphological_operations.py
│   ├── 08_image_enhancement_pipeline.py
│   ├── 09_compositing_matting.py
│   ├── 10_fourier_transform.py
│   ├── 11_pyramids_wavelets.py
│   └── 12_geometric_transformations.py
├── data/
│   └── images/
└── Jobsheet.md
```

---

## 📝 Percobaan 1: Brightness dan Contrast Adjustment

### Tujuan
Memahami dan mengimplementasikan pengaturan brightness dan contrast.

### Teori Singkat
```
g(x,y) = α × f(x,y) + β

Di mana:
- α (alpha) = kontras (multiplier)
- β (beta) = brightness (offset)
- α > 1 meningkatkan kontras
- β > 0 menambah kecerahan
```

### Langkah Kerja

1. **Buka file** `01_brightness_contrast.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   BRIGHTNESS = 50     # Range: -255 to 255
   CONTRAST = 1.5      # Range: 0.1 to 3.0
   ```

3. **Jalankan program dan amati:**
   - Efek brightness positif vs negatif
   - Efek contrast > 1 vs < 1
   - Kombinasi brightness dan contrast

4. **Eksperimen:**
   - Set `BRIGHTNESS = -50`, `CONTRAST = 1.0`
   - Set `BRIGHTNESS = 0`, `CONTRAST = 2.0`
   - Set `BRIGHTNESS = 30`, `CONTRAST = 1.5`

### Data Pengamatan

| Parameter | Brightness | Contrast | Observasi |
|-----------|------------|----------|-----------|
| Original | 0 | 1.0 | |
| Terang | 50 | 1.0 | |
| Gelap | -50 | 1.0 | |
| High Contrast | 0 | 2.0 | |
| Low Contrast | 0 | 0.5 | |
| Combined | 30 | 1.5 | |

### Pertanyaan
1. Apa yang terjadi jika β > 255 pada gambar yang sudah terang?
2. Mengapa α < 1 membuat gambar terlihat "washed out"?
3. Bagaimana cara menghindari clipping (nilai > 255 atau < 0)?

---

## 📝 Percobaan 2: Gamma Correction

### Tujuan
Memahami gamma correction untuk penyesuaian pencahayaan non-linear.

### Teori Singkat
```
g(x,y) = c × [f(x,y)/255]^γ × 255

Di mana:
- γ < 1 → mencerahkan shadows (lift shadows)
- γ > 1 → menggelapkan highlights (compress highlights)
- γ = 1 → tidak ada perubahan
```

### Langkah Kerja

1. **Buka file** `02_gamma_correction.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   GAMMA = 2.2         # Typical display gamma
   GAMMA_VALUES = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5]
   ```

3. **Jalankan program dan amati:**
   - Efek berbagai nilai gamma
   - Perbedaan dengan linear brightness adjustment
   - Gamma pada gambar underexposed vs overexposed

4. **Eksperimen dengan gambar berbeda:**
   - Gambar gelap (underexposed) dengan gamma < 1
   - Gambar terang (overexposed) dengan gamma > 1

### Data Pengamatan

| Gamma | Efek pada Shadows | Efek pada Highlights | Use Case |
|-------|-------------------|----------------------|----------|
| 0.3 | | | |
| 0.5 | | | |
| 1.0 | | | |
| 1.5 | | | |
| 2.2 | | | |

### Pertanyaan
1. Mengapa nilai gamma 2.2 sering digunakan untuk display?
2. Apa perbedaan gamma correction dengan brightness adjustment?
3. Gambar seperti apa yang cocok menggunakan gamma < 1?

---

## 📝 Percobaan 3: Thresholding

### Tujuan
Mengimplementasikan berbagai metode thresholding untuk segmentasi.

### Teori Singkat
```
Binary Threshold:
g(x,y) = 255  jika f(x,y) > T
g(x,y) = 0    jika f(x,y) ≤ T

Adaptive Threshold:
T(x,y) dihitung berdasarkan neighborhood lokal
```

### Langkah Kerja

1. **Buka file** `03_thresholding.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   THRESHOLD_VALUE = 127       # 0-255
   BLOCK_SIZE = 11             # Untuk adaptive (ganjil)
   C_VALUE = 2                 # Konstanta dikurangi dari mean
   ```

3. **Jalankan program dan bandingkan:**
   - Binary threshold (cv2.THRESH_BINARY)
   - Otsu's automatic threshold
   - Adaptive mean threshold
   - Adaptive Gaussian threshold

4. **Eksperimen dengan gambar berbeda:**
   - Gambar dengan pencahayaan merata
   - Gambar dengan pencahayaan tidak merata

### Data Pengamatan

| Metode | Parameter | Kelebihan | Kekurangan |
|--------|-----------|-----------|------------|
| Binary | T = 127 | | |
| Otsu | Auto | | |
| Adaptive Mean | Block=11, C=2 | | |
| Adaptive Gaussian | Block=11, C=2 | | |

### Pertanyaan
1. Kapan Otsu's method tidak bekerja dengan baik?
2. Mengapa block size harus ganjil?
3. Apa pengaruh nilai C pada adaptive threshold?

---

## 📝 Percobaan 4: Histogram Equalization

### Tujuan
Menggunakan histogram equalization untuk peningkatan kontras.

### Teori Singkat
```
Histogram Equalization:
1. Hitung histogram h(k)
2. Hitung CDF: c(k) = Σ h(i) untuk i = 0 to k
3. Normalize: s(k) = (L-1) × c(k) / total_pixels
4. Map setiap piksel ke nilai baru

CLAHE (Contrast Limited AHE):
- Divide gambar menjadi tiles
- Apply histogram equalization per tile
- Clip histogram untuk membatasi amplifikasi
- Interpolasi antar tile untuk menghindari artifacts
```

### Langkah Kerja

1. **Buka file** `04_histogram_equalization.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   CLAHE_CLIP_LIMIT = 2.0      # Clip limit
   CLAHE_TILE_SIZE = (8, 8)    # Tile grid size
   ```

3. **Jalankan program dan bandingkan:**
   - Histogram original vs equalized
   - Global equalization vs CLAHE
   - Efek pada gambar dengan kontras berbeda

4. **Eksperimen dengan parameter CLAHE:**
   - clip_limit: 1.0, 2.0, 4.0, 8.0
   - tile_size: (4,4), (8,8), (16,16)

### Data Pengamatan

| Metode | Parameter | Efek pada Histogram | Kualitas Visual |
|--------|-----------|---------------------|-----------------|
| Original | - | | |
| Global Equalization | - | | |
| CLAHE | clip=2.0, tile=8x8 | | |
| CLAHE | clip=4.0, tile=8x8 | | |
| CLAHE | clip=2.0, tile=4x4 | | |

### Pertanyaan
1. Apa kekurangan global histogram equalization?
2. Apa efek clip limit yang terlalu tinggi?
3. Kapan tile size yang lebih kecil lebih baik?

---

## 📝 Percobaan 5: Spatial Filtering

### Tujuan
Mengimplementasikan berbagai filter untuk smoothing dan sharpening.

### Teori Singkat
```
Smoothing Filters:
- Mean/Box Filter: Rata-rata semua piksel dalam kernel
- Gaussian Filter: Weighted average dengan distribusi Gaussian
- Median Filter: Nilai tengah (non-linear, bagus untuk salt-pepper noise)
- Bilateral Filter: Edge-preserving (spatial + intensity weighting)

Sharpening:
- Unsharp Masking: sharp = original + α × (original - blurred)
- Laplacian: Mendeteksi perubahan cepat (second derivative)
```

### Langkah Kerja

1. **Buka file** `05_spatial_filtering.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   KERNEL_SIZE = 5           # 3, 5, 7, 9, ...
   GAUSSIAN_SIGMA = 1.5      # Standard deviation
   BILATERAL_D = 9           # Diameter
   BILATERAL_SIGMA_COLOR = 75
   BILATERAL_SIGMA_SPACE = 75
   SHARPEN_AMOUNT = 1.5      # Unsharp mask strength
   ```

3. **Eksperimen dengan gambar berisi noise:**
   - Bandingkan mean vs Gaussian vs median filter
   - Amati efek pada edge preservation

4. **Eksperimen dengan sharpening:**
   - Bandingkan berbagai nilai strength
   - Amati efek oversharpening

### Data Pengamatan (Smoothing)

| Filter | Kernel Size | Noise Reduction | Edge Preservation | Speed |
|--------|-------------|-----------------|-------------------|-------|
| Mean | 5 | | | |
| Gaussian | 5, σ=1.5 | | | |
| Median | 5 | | | |
| Bilateral | d=9 | | | |

### Data Pengamatan (Sharpening)

| Method | Parameter | Efek pada Detail | Artifacts |
|--------|-----------|------------------|-----------|
| Unsharp Mask | α = 0.5 | | |
| Unsharp Mask | α = 1.0 | | |
| Unsharp Mask | α = 2.0 | | |
| Laplacian | - | | |

### Pertanyaan
1. Filter mana yang paling baik untuk salt-and-pepper noise? Mengapa?
2. Mengapa bilateral filter lebih lambat dari Gaussian?
3. Apa yang terjadi jika kernel size terlalu besar?

---

## 📝 Percobaan 6: Edge Detection

### Tujuan
Mengimplementasikan edge detection dengan berbagai metode.

### Teori Singkat
```
Sobel Operator:
- Menghitung gradient horizontal (Gx) dan vertikal (Gy)
- Magnitude: G = √(Gx² + Gy²)
- Direction: θ = arctan(Gy/Gx)

Canny Edge Detection:
1. Gaussian smoothing
2. Gradient calculation (Sobel)
3. Non-maximum suppression (NMS)
4. Double thresholding (high & low)
5. Edge tracking by hysteresis
```

### Langkah Kerja

1. **Buka file** `06_edge_detection.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   CANNY_LOW_THRESHOLD = 50
   CANNY_HIGH_THRESHOLD = 150
   SOBEL_KERNEL_SIZE = 3     # 1, 3, 5, 7
   ```

3. **Jalankan program dan bandingkan:**
   - Sobel X vs Sobel Y vs Combined
   - Laplacian
   - Canny dengan berbagai threshold

4. **Eksperimen dengan Canny:**
   - Ratio high:low = 2:1, 3:1, 4:1
   - Efek preprocessing blur

### Data Pengamatan

| Method | Parameters | Edge Quality | Noise Sensitivity |
|--------|------------|--------------|-------------------|
| Sobel X | ksize=3 | | |
| Sobel Y | ksize=3 | | |
| Sobel Combined | ksize=3 | | |
| Laplacian | ksize=3 | | |
| Canny | low=50, high=150 | | |
| Canny | low=30, high=100 | | |
| Canny | low=100, high=200 | | |

### Pertanyaan
1. Mengapa Canny menggunakan dua threshold?
2. Apa efek preprocessing blur sebelum edge detection?
3. Bagaimana cara memilih threshold Canny yang optimal?

---

## 📝 Percobaan 7: Morphological Operations

### Tujuan
Menggunakan operasi morfologi untuk memproses binary image.

### Teori Singkat
```
Erosion:  Mengecilkan foreground, menghapus noise kecil
Dilation: Memperbesar foreground, mengisi lubang kecil
Opening:  Erosion → Dilation (menghapus noise sambil menjaga ukuran)
Closing:  Dilation → Erosion (mengisi lubang sambil menjaga ukuran)
Gradient: Dilation - Erosion (menghasilkan outline)
Top Hat:  Original - Opening (mendeteksi bright spots)
Black Hat: Closing - Original (mendeteksi dark spots)
```

### Langkah Kerja

1. **Buka file** `07_morphological_operations.py`

2. **Pahami variabel yang bisa diubah:**
   ```python
   KERNEL_SIZE = 5
   KERNEL_SHAPE = cv2.MORPH_RECT  # MORPH_ELLIPSE, MORPH_CROSS
   ITERATIONS = 1
   ```

3. **Jalankan program dan amati:**
   - Efek erosion dan dilation
   - Perbedaan opening vs closing
   - Morphological gradient untuk outline

4. **Eksperimen dengan structuring element:**
   - Rectangle vs Ellipse vs Cross
   - Berbagai ukuran kernel
   - Berbagai jumlah iterasi

### Data Pengamatan

| Operation | Kernel Shape | Size | Iterations | Efek |
|-----------|--------------|------|------------|------|
| Erosion | RECT | 5 | 1 | |
| Erosion | RECT | 5 | 2 | |
| Dilation | RECT | 5 | 1 | |
| Opening | RECT | 5 | 1 | |
| Closing | RECT | 5 | 1 | |
| Gradient | RECT | 5 | 1 | |
| Erosion | ELLIPSE | 5 | 1 | |
| Erosion | CROSS | 5 | 1 | |

### Pertanyaan
1. Kapan menggunakan opening vs closing?
2. Apa efek kernel shape yang berbeda?
3. Bagaimana menggunakan morfologi untuk deteksi kontur?

---

## 📝 Percobaan 8: Image Enhancement Pipeline

### Tujuan
Mengkombinasikan berbagai teknik untuk pipeline enhancement lengkap.

### Langkah Kerja

1. **Buka file** `08_image_enhancement_pipeline.py`

2. **Pahami pipeline yang digunakan:**
   ```
   Input → Noise Reduction → Contrast Enhancement → 
   Sharpening → Color Adjustment → Output
   ```

3. **Jalankan program dengan berbagai jenis gambar:**
   - Gambar gelap (underexposed)
   - Gambar dengan noise
   - Gambar low contrast
   - Gambar outdoor vs indoor

4. **Eksperimen dengan urutan operasi:**
   - Denoise → Enhance vs Enhance → Denoise
   - Sharpen → Contrast vs Contrast → Sharpen

### Data Pengamatan

| Input Type | Pipeline Used | Result Quality | Notes |
|------------|---------------|----------------|-------|
| Underexposed | | | |
| Noisy | | | |
| Low Contrast | | | |
| Overexposed | | | |

### Pertanyaan
1. Mengapa urutan operasi penting?
2. Pipeline apa yang terbaik untuk gambar medis?
3. Bagaimana menghindari over-processing?

---

## ✏️ Analisis Hasil

### Bandingkan Metode Enhancement

Lengkapi tabel berikut berdasarkan eksperimen:

| Teknik | Kelebihan | Kekurangan | Best For |
|--------|-----------|------------|----------|
| Brightness Adjustment | | | |
| Gamma Correction | | | |
| Histogram Equalization | | | |
| CLAHE | | | |
| Unsharp Masking | | | |

### Bandingkan Filter Noise Reduction

| Filter | Gaussian Noise | Salt-Pepper | Edge Preservation | Speed |
|--------|----------------|-------------|-------------------|-------|
| Mean | | | | |
| Gaussian | | | | |
| Median | | | | |
| Bilateral | | | | |

---

## 📊 Kesimpulan

Tuliskan kesimpulan dari praktikum ini:

1. **Point Operations:**
   ```
   _______________________________________________
   _______________________________________________
   ```

2. **Histogram Operations:**
   ```
   _______________________________________________
   _______________________________________________
   ```

3. **Spatial Filtering:**
   ```
   _______________________________________________
   _______________________________________________
   ```

4. **Edge Detection:**
   ```
   _______________________________________________
   _______________________________________________
   ```

5. **Morphological Operations:**
   ```
   _______________________________________________
   _______________________________________________
   ```

---

## 📝 Percobaan 9: Compositing dan Matting

### Tujuan
Memahami dan mengimplementasikan alpha compositing dan green screen matting.

### Teori Singkat
```
Alpha Compositing (Over Operator):
C = (1 - α)B + αF

Di mana:
- F = Foreground
- B = Background
- α = Alpha matte (0 = transparan, 1 = opak)
- C = Composited result
```

### Langkah Kerja

1. **Buka file** `09_compositing_matting.py`

2. **Pahami konsep:**
   - Alpha channel: transparansi per-pixel
   - Green screen: isolasi warna hijau
   - Matte refinement: morphology untuk smooth edges

3. **Jalankan setiap demo dan amati:**
   - `demo_alpha_channel_basics()`: konsep alpha 0-1
   - `demo_green_screen_matting()`: chroma keying
   - `demo_over_operator()`: compositing formula
   - `demo_bokeh_effect()`: aplikasi portrait mode

4. **Eksperimen:**
   - Ubah `GREEN_LOWER`, `GREEN_UPPER` untuk chroma key range
   - Ubah `MATTE_MORPH_ITERATIONS` untuk edge quality
   - Coba berbagai `BACKGROUND_BLUR_AMOUNT`

### Data Pengamatan

| Eksperimen | Green Range (HSV) | Matte Quality | Observasi |
|------------|-------------------|---------------|-----------|
| Default | (40,40,40)-(80,255,255) | | |
| Narrow range | (50,50,50)-(70,255,255) | | |
| Wide range | (30,30,30)-(90,255,255) | | |
| +Morphology | Default + 3 iterations | | |

### Pertanyaan
1. Mengapa green screen lebih populer daripada blue screen?
2. Apa efek pre-multiplied alpha terhadap quality?
3. Bagaimana cara handling hair/fur edges dalam matting?

---

## 📝 Percobaan 10: Fourier Transform

### Tujuan
Memahami representasi frequency domain dan filtering.

### Teori Singkat
```
DFT (Discrete Fourier Transform):
F(u,v) = ∑∑ f(x,y) e^(-2πi(ux/M + vy/N))

Magnitude spectrum: |F(u,v)|
Phase spectrum: φ(u,v) = arctan(Im/Re)
```

### Langkah Kerja

1. **Buka file** `10_fourier_transform.py`

2. **Jalankan setiap demo:**
   - `demo_fft_basics()`: visualisasi magnitude & phase
   - `demo_frequency_filtering()`: low/high/band-pass
   - `demo_periodic_noise_removal()`: notch filtering
   - `demo_dct_compression()`: simulasi JPEG

3. **Eksperimen parameter:**
   - Ubah `LOWPASS_CUTOFF` (10-100) untuk blur amount
   - Ubah `HIGHPASS_CUTOFF` (5-50) untuk edge sharpness
   - Ubah `DCT_QUALITY` (10-90) untuk compression

### Data Pengamatan

| Filter Type | Cutoff | Visual Effect | Aplikasi |
|-------------|--------|---------------|----------|
| Low-pass | 30 | | Noise reduction |
| High-pass | 10 | | Edge enhancement |
| Band-pass | 10-30 | | Texture extraction |
| Notch | Specific freq | | Periodic noise removal |

### Pertanyaan
1. Mengapa DC component (0,0) selalu paling terang?
2. Apa perbedaan ideal vs Gaussian filter di frequency domain?
3. Bagaimana JPEG menggunakan DCT untuk compression?

---

## 📝 Percobaan 11: Pyramids dan Wavelets

### Tujuan
Memahami multi-resolution representation dan aplikasinya.

### Teori Singkat
```
Gaussian Pyramid:
G_i+1 = Downsample(GaussianBlur(G_i))

Laplacian Pyramid:
L_i = G_i - Upsample(G_i+1)

Reconstruction:
G_i = L_i + Upsample(G_i+1)
```

### Langkah Kerja

1. **Buka file** `11_pyramids_wavelets.py`

2. **Jalankan demo:**
   - `demo_gaussian_pyramid()`: multi-scale representation
   - `demo_laplacian_pyramid()`: perfect reconstruction
   - `demo_pyramid_blending()`: seamless blend (apple-orange)
   - `demo_wavelet_basics()`: wavelet decomposition
   - `demo_wavelet_denoising()`: noise removal

3. **Eksperimen:**
   - Ubah `PYRAMID_LEVELS` (2-6) untuk granularity
   - Ubah `BLEND_MASK_FEATHER` untuk seam quality
   - Coba `WAVELET_TYPE`: 'haar', 'db4', 'sym4'

### Data Pengamatan

| Pyramid Type | Levels | Overhead | Properties |
|--------------|--------|----------|------------|
| Gaussian | 4 | ~33% | Multi-scale, overcomplete |
| Laplacian | 4 | ~33% | Band-pass, perfect recon |
| Wavelet | 3 | 0% | Tight frame, oriented |

### Pertanyaan
1. Mengapa Laplacian pyramid bisa perfect reconstruction?
2. Apa keuntungan pyramid blending vs direct blend?
3. Bagaimana wavelet digunakan dalam JPEG 2000?

---

## 📝 Percobaan 12: Geometric Transformations

### Tujuan
Memahami dan mengimplementasikan berbagai transformasi geometrik.

### Teori Singkat
```
Transformation Hierarchy:
Translation (2 DoF) ⊂ Euclidean (3 DoF) ⊂ 
Similarity (4 DoF) ⊂ Affine (6 DoF) ⊂ 
Perspective (8 DoF)

Affine: x' = Ax + t (needs 3 points)
Perspective: x' = Hx (needs 4 points)
```

### Langkah Kerja

1. **Buka file** `12_geometric_transformations.py`

2. **Jalankan demo:**
   - `demo_basic_transformations()`: translation, rotation
   - `demo_affine_transformation()`: 6-DoF warp
   - `demo_perspective_transformation()`: homography
   - `demo_interpolation_comparison()`: NEAREST vs CUBIC
   - `demo_mesh_warping()`: radial, wave, swirl effects
   - `demo_real_world_application()`: document scanner

3. **Eksperimen:**
   - Ubah `ROTATION_ANGLE` (-180 to 180)
   - Compare `INTERP_METHOD`: NEAREST, LINEAR, CUBIC, LANCZOS4
   - Modifikasi radial distortion `strength`

### Data Pengamatan

| Transform Type | DoF | Points Needed | Preserves |
|----------------|-----|---------------|-----------|
| Translation | 2 | - | Everything |
| Euclidean | 3 | 2 | Distances, angles |
| Similarity | 4 | 2 | Angles, ratios |
| Affine | 6 | 3 | Parallel lines |
| Perspective | 8 | 4 | Straight lines only |

### Pertanyaan
1. Mengapa perspective transform bisa simulate 3D view?
2. Kapan menggunakan affine vs perspective?
3. Bagaimana document scanner apps mendeteksi corners?

---

## 📝 Tugas Mandiri

### Tugas 1: Image Enhancement App
Buat program yang menerima gambar dan secara otomatis menentukan enhancement yang diperlukan berdasarkan analisis histogram.

### Tugas 2: Noise Comparison
1. Tambahkan berbagai jenis noise ke gambar (Gaussian, salt-pepper, speckle)
2. Terapkan berbagai filter dan bandingkan hasilnya
3. Hitung PSNR (Peak Signal-to-Noise Ratio) untuk setiap kombinasi

### Tugas 3: Edge-based Segmentation
Gunakan edge detection dan morphological operations untuk melakukan segmentasi objek sederhana (misalnya: koin pada background solid).

### Tugas 4: Green Screen Compositing
1. Buat video green screen sederhana
2. Implementasikan chroma keying
3. Replace background dengan gambar/video lain
4. Handle edge quality dengan matte refinement

### Tugas 5: Frequency Domain Filtering
1. Buat gambar dengan periodic noise (grid pattern)
2. Implementasikan notch filter untuk remove noise
3. Compare hasil dengan spatial domain filtering
4. Analyze trade-offs

### Tugas 6: Panorama Blending
1. Ambil 2-3 foto dengan overlap
2. Align images menggunakan homography
3. Blend dengan pyramid blending untuk seamless seam
4. Compare dengan direct blending

### Tugas 7: Document Scanner App
1. Capture foto dokumen dari angle
2. Detect 4 corners menggunakan edge + contour
3. Apply perspective transform untuk rectification
4. Enhance dengan thresholding + sharpening

---

## 📎 Lampiran

### Referensi OpenCV Functions

```python
# Point Operations
cv2.convertScaleAbs(src, alpha=1, beta=0)

# Thresholding
cv2.threshold(src, thresh, maxval, type)
cv2.adaptiveThreshold(src, maxval, adaptiveMethod, thresholdType, blockSize, C)

---

## Percobaan 13: Steerable Filters dan Band-Pass Filtering

**Tujuan:**
- Memahami konsep steerable filters (Freeman & Adelson)
- Mengimplementasikan Laplacian of Gaussian (LoG)
- Menerapkan band-pass filtering untuk texture analysis
- Mendeteksi oriented edges dan fitur dengan arbitrary direction

**File Praktikum:**
```
praktikum/13_steerable_filters_advanced.py
```

**Tugas Praktik:**

1. **Percobaan 13.1: Directional Edge Detection**
   - Implementasikan first-order steerable filters
   - Deteksi edges di 8 orientasi berbeda (0°, 45°, 90°, 135°, dll)
   - Tampilkan magnitude dan dominant orientation
   - Parameter: σ = 1.5 untuk Gaussian
   - **Pertanyaan:** Bandingkan hasil dengan Sobel standard, apa keunggulannya?

2. **Percobaan 13.2: Corner/Junction Detection**
   - Implementasikan second-order steerable filters
   - Deteksi corners sebagai local maxima dari corner strength
   - Visualisasikan corner response pada berbagai orientasi
   - **Tugas Mandiri:** Implementasikan Harris corner detector menggunakan steerable filters

3. **Percobaan 13.3: Multi-Scale Blob Detection (LoG)**
   - Build scale-space dari Laplacian of Gaussian
   - Deteksi blobs sebagai scale-space extrema
   - Tampilkan detected circles dengan radius = σ√2
   - Variance σ: 1.0, 1.5, 2.0, 2.5, 3.0
   - **Aplikasi:** Coin detection, bubble detection

4. **Percobaan 13.4: Efficient DoG (Difference of Gaussians)**
   - Approksimasi LoG menggunakan DoG (LoG ≈ σ²·DoG)
   - Bandingkan kecepatan dan accuracy vs true LoG
   - Gunakan adjacent scales dalam pyramid
   - **Optimisasi:** Percepatan deteksi dengan DoG vs LoG

5. **Percobaan 13.5: Frequency Band-Pass Filtering**
   - Implementasikan band-pass filter di frequency domain
   - Design dengan low-pass dan high-pass dalam FFT
   - Isolasi specific frequency ranges (misal, 0.1-0.3 × N_y)
   - **Aplikasi:** Texture frequency analysis, periodic noise removal

6. **Percobaan 13.6: Oriented Texture Analysis**
   - Kombinasikan steerable filters dengan band-pass
   - Analisis texture dengan specific orientation AND frequency
   - Deteksi oriented patterns (rip, weave, tiles)
   - Create orientation histogram dari responses
   - **Real-World App:** Fabric inspection, quality control

**Checklist Selesai:**
- [ ] Semua 6 demonstrasi berjalan tanpa error
- [ ] Visualisasi untuk setiap percobaan jelas dan informatif
- [ ] Jelaskan konsep steerable filters dengan formula
- [ ] Bandingkan dengan filter konvensional (Sobel, Laplacian)
- [ ] Simpulkan kapan steerable filters lebih berguna

---

## Percobaan 14: Advanced Interpolation, Decimation, dan MIP-Mapping

**Tujuan:**
- Memahami interpolasi berkualitas tinggi (bicubic, Lanczos)
- Implementasikan downsampling dengan anti-aliasing prefilter
- Build dan gunakan MIP-maps untuk multi-resolution
- Menerapkan dalam image zoom dengan lossless quality

**File Praktikum:**
```
praktikum/14_interpolation_decimation_advanced.py
```

**Tugas Praktik:**

1. **Percobaan 14.1: Interpolation Quality Comparison**
   - Implementasikan: nearest neighbor, bilinear, bicubic, Lanczos
   - Upsampling dengan faktor 4× pada test image
   - Metrik: MSE vs original high-res, visual quality
   - Parameter bicubic: a = -1, -0.5, -0.75 (compare)
   - **Hasil:** Kurva MSE vs upsampling factor untuk setiap method

2. **Percobaan 14.2: Cubic Parameter Effects**
   - Variasikan parameter 'a' dalam cubic kernel: a = -1 to 0
   - Analisis tradeoff antara smoothness vs sharpness
   - a = -1 (Catmull-Rom): sharp dengan ringing
   - a = -0.5: balanced
   - **Tugas Mandiri:** Find optimal 'a' untuk natural-looking images

3. **Percobaan 14.3: Decimation Filter Comparison**
   - Downsampling dengan Gaussian vs Binomial vs Lanczos prefilter
   - Lakukan 2× downsampling, analisis MSE vs original
   - Visualisasi frequency spectrum sebelum/sesudah
   - **Deteksi Aliasing:** Identifikasi moire patterns tanpa prefilter

4. **Percobaan 14.4: MIP-Map Construction & Sampling**
   - Build Gaussian pyramid dengan 5-6 levels
   - Implementasikan trilinear MIP-map sampling
   - Zoom in/out pada region dengan smooth quality transitions
   - Tampilkan level-of-detail (LOD) selection
   - **Benchmark:** Storage overhead vs quality improvement

5. **Percobaan 14.5: Zoom Sequence Animation**
   - Create smooth zoom-in/zoom-out sequence
   - Gunakan MIP-maps untuk consistent quality di semua zoom levels
   - Save hasil sebagai video frames
   - Compare vs naive interpolation (flickering/aliasing)
   - **Aplikasi:** Virtual camera zoom, progressive image loading

6. **Percobaan 14.6: Decimation Ratio Effects**
   - Systematically downsample dengan ratio 2, 3, 4, 5 ...
   - Deteksi degradation point (aliasing artifacts appear)
   - Analisis spatial/frequency domain untuk setiap ratio
   - **Teori Nyquist:** Frequency content vs decimation ratio
   - **Pertanyaan:** Berapa ratio maksimal tanpa aliasing terlihat?

**Checklist Selesai:**
- [ ] Semua interpolation methods implemented & tested
- [ ] Cubic parameter effects dengan visualisasi
- [ ] Anti-aliasing prefilter comparison jelas
- [ ] MIP-map construction & trilinear sampling kerja
- [ ] Zoom sequences smooth tanpa artifacts
- [ ] Dokumentasi tentang when to use each method

---

## Percobaan 15: Advanced Image Blending dan Seamless Composition

**Tujuan:**
- Memahami gradient-domain image compositing (Poisson blending)
- Implementasikan multi-band blending untuk seamless transitions
- Menerapkan feathering dan distance-transform masking
- Create seamless cloning dan exposure blending

**File Praktikum:**
```
praktikum/15_advanced_blending_techniques.py
```

**Tugas Praktik:**

1. **Percobaan 15.1: Laplacian Pyramid Blending dengan Mask**
   - Build Laplacian pyramids untuk 2 images
   - Blend setiap pyramid level dengan binary mask
   - Reconstruct final image dari blended bands
   - Bandingkan dengan linear blending (hasil seamless?)
   - **Contoh:** Composite landscape dengan sky
   - **Metrik:** Visual quality, no visible seams

2. **Percobaan 15.2: Feathering Effects**
   - Implementasikan Gaussian feathering pada mask edges
   - Variasikan feather radius: 10, 20, 50, 100 pixels
   - Visualisasikan blending gradient
   - **Aplikasi:** Soft transparency transitions
   - **Tugas Mandiri:** Custom feather shapes (radial, linear)

3. **Percobaan 15.3: Multi-Band Blending Comparison**
   - Implement steerable pyramid atau multi-band decomposition
   - Blend frequencies independently
   - Bandingkan hasil vs Laplacian pyramid
   - **Keunggulan:** Lebih better color separation, less color fringing
   - **Analisis:** Frequency content di different bands

4. **Percobaan 15.4: Gradient Domain Visualization**
   - Compute gradient (∂I/∂x, ∂I/∂y) dari 2 images
   - Visualisasikan sebagai vector field
   - Implementasikan Poisson blending untuk seamless cloning
   - Iterative solver (Jacobi method) untuk Laplace equation
   - **Debug:** Convergence analysis, iteration count vs accuracy

5. **Percobaan 15.5: Seamless Cloning (3 Methods)**
   - Implementasikan 3 methods: Poisson, multiband, feather
   - Clone object dari source ke destination
   - Bandingkan boundary blending quality
   - **Metrics:** MSE, SSIM di boundary region
   - **Real-World:** Face swapping, object insertion

6. **Percobaan 15.6: Exposure Blending (HDR-like)**
   - Implement exposure fusion dari multiple exposures
   - Weight setiap exposure berdasarkan quality (contrast, saturation)
   - Combine dengan Laplacian pyramid untuk natural look
   - **Hasil:** High dynamic range dalam single image
   - **Aplikasi:** HDR tone mapping, smartphone night mode

**Checklist Selesai:**
- [ ] Laplacian pyramid blending seamless
- [ ] Feathering dengan smooth transitions
- [ ] Multi-band blending implemented & compared
- [ ] Gradient visualization & Poisson solver working
- [ ] Seamless cloning di 3 methods tested
- [ ] Exposure blending menghasilkan natural HDR
- [ ] Dokumentasi tentang method selection strategy

---

## Percobaan 16: Mesh Warping dan Feature-Based Morphing

**Tujuan:**
- Memahami thin-plate spline (TPS) untuk smooth image warping
- Implementasikan line-based warping (Beier-Neely algorithm)
- Menerapkan triangular mesh deformation effects
- Create feature-based morphing animations antara images

**File Praktikum:**
```
praktikum/16_mesh_warping_morphing.py
```

**Tugas Praktik:**

1. **Percobaan 16.1: Thin-Plate Spline (TPS) Warping**
   - Implementasikan TPS dari control points
   - Solve linear system untuk interpolation coefficients
   - Warp image menggunakan forward/backward mapping
   - Test dengan 5-20 control points
   - **Visualisasi:** Control points, displacement vectors, result
   - **Property:** Passes through control points exactly, smooth elsewhere

2. **Percobaan 16.2: Line-Based Warping (Beier-Neely)**
   - Define source & target line correspondences
   - Implementasikan line-based displacement calculation
   - Weight displacement dari multiple lines
   - **Advantage:** More intuitive than point-based warping
   - **Tugas Mandiri:** Interactive interface untuk specify lines

3. **Percobaan 16.3: Triangular Mesh Warping**
   - Delaunay triangulation dari control points
   - Affine warp per triangle
   - Smooth blending across triangle boundaries
   - Visualisasikan mesh deformation
   - **Comparison:** TPS vs mesh - speed vs quality

4. **Percobaan 16.4: Mesh Deformation Effects (Bulge, Pinch, Twist)**
   - Implementasikan 3 effects: bulge, pinch, twist
   - Deform mesh points dengan mathematical transformations
   - Visualisasikan mesh grid sebelum/sesudah
   - **Parameters:** Effect center, radius, strength
   - **Aplikasi:** Digital makeup, face beautification

5. **Percobaan 16.5: Feature-Based Morphing Sequence**
   - Define corresponding feature points antara 2 images
   - Interpolate points di 10-20 frames
   - Warp both images ke intermediate shape
   - Cross-dissolve antara warped images
   - Create smooth morphing video
   - **Smoothness:** Easing functions untuk frame timing

6. **Percobaan 16.6: Advanced Morphing Techniques**
   - Implement morphing dengan automatic feature matching (SIFT/SURF)
   - Or: line correspondences dari user
   - Optimize untuk visual quality (avoid discontinuities)
   - Create multi-image morphing (chain A→B→C)
   - **Challenge:** Face morphing dengan feature preservation
   - **Video Output:** Save morph sequence sebagai MP4

**Checklist Selesai:**
- [ ] TPS warping smooth dengan proper interpolation
- [ ] Line-based warping untuk intuitive control
- [ ] Mesh triangulation & deformation working
- [ ] Bulge/pinch/twist effects natural looking
- [ ] Feature-based morphing smooth transitions
- [ ] Automatic feature matching integrated
- [ ] Video output quality baik (no flickering)
- [ ] Dokumentasi tentang practical morphing pipeline

---

## 📝 Template Laporan Praktikum

Untuk setiap kelompok praktikum, buat laporan dengan struktur:

```
├── 1. Tujuan & Teori
│   ├── Jelaskan tujuan setiap percobaan
│   ├── Konsep dasar (TPS, line-based warping, dll)
│   └── Rumus dan algoritma
│
├── 2. Metodologi
│   ├── Langkah-langkah eksperimen
│   ├── Parameter yang digunakan
│   └── Dataset/sample images
│
├── 3. Hasil Eksperimen
│   ├── Screenshot output untuk setiap percobaan
│   ├── Tabel perbandingan (jika ada)
│   ├── Analisis visual quality
│   └── Performance metrics (jika relevan)
│
├── 4. Analisis & Kesimpulan
│   ├── Interpretasi hasil
│   ├── Keunggulan & kelemahan setiap method
│   ├── Ketika menggunakan mana method
│   └── Rekomendasi improvements
│
├── 5. Tugas Mandiri
│   ├── Modify salah satu percobaan
│   ├── Combine 2+ techniques
│   └── Real-world application
│
└── 6. Referensi & Appendix
    ├── Code snippets penting
    ├── Additional plots
    └── Error handling notes
```

---

# Histogram
cv2.equalizeHist(src)
clahe = cv2.createCLAHE(clipLimit, tileGridSize)
clahe.apply(src)

# Filtering
cv2.blur(src, ksize)
cv2.GaussianBlur(src, ksize, sigmaX)
cv2.medianBlur(src, ksize)
cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)
cv2.filter2D(src, ddepth, kernel)

# Edge Detection
cv2.Sobel(src, ddepth, dx, dy, ksize)
cv2.Laplacian(src, ddepth)
cv2.Canny(src, threshold1, threshold2)

# Morphology
kernel = cv2.getStructuringElement(shape, ksize)
cv2.erode(src, kernel, iterations)
cv2.dilate(src, kernel, iterations)
cv2.morphologyEx(src, op, kernel)

# Compositing
cv2.addWeighted(src1, alpha, src2, beta, gamma)
# Alpha blending: manual calculation

# Fourier Transform
cv2.dft(src, flags=cv2.DFT_COMPLEX_OUTPUT)
cv2.idft(src, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
cv2.dct(src)
cv2.idct(src)

# Pyramids
cv2.pyrDown(src)
cv2.pyrUp(src, dstsize)

# Geometric Transforms
cv2.getRotationMatrix2D(center, angle, scale)
cv2.getAffineTransform(src_pts, dst_pts)  # 3 points
cv2.getPerspectiveTransform(src_pts, dst_pts)  # 4 points
cv2.warpAffine(src, M, dsize)
cv2.warpPerspective(src, M, dsize)
cv2.remap(src, map_x, map_y, interpolation)

# Wavelets (PyWavelets)
import pywt
coeffs = pywt.wavedec2(data, wavelet, level)
data_rec = pywt.waverec2(coeffs, wavelet)

# Steerable Filters (Custom)
# See praktikum/13_steerable_filters_advanced.py for implementations

# Interpolation & Decimation (Custom)
# See praktikum/14_interpolation_decimation_advanced.py

# Image Blending (Custom)
# See praktikum/15_advanced_blending_techniques.py

# Warping & Morphing (Custom)
# See praktikum/16_mesh_warping_morphing.py for TPS, line-based, mesh deformation
```

---

*Jobsheet ini adalah bagian dari Praktikum Computer Vision*
