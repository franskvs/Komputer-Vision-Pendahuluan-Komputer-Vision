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
│   └── 08_image_enhancement_pipeline.py
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

## 📝 Tugas Mandiri

### Tugas 1: Image Enhancement App
Buat program yang menerima gambar dan secara otomatis menentukan enhancement yang diperlukan berdasarkan analisis histogram.

### Tugas 2: Noise Comparison
1. Tambahkan berbagai jenis noise ke gambar (Gaussian, salt-pepper, speckle)
2. Terapkan berbagai filter dan bandingkan hasilnya
3. Hitung PSNR (Peak Signal-to-Noise Ratio) untuk setiap kombinasi

### Tugas 3: Edge-based Segmentation
Gunakan edge detection dan morphological operations untuk melakukan segmentasi objek sederhana (misalnya: koin pada background solid).

---

## 📎 Lampiran

### Referensi OpenCV Functions

```python
# Point Operations
cv2.convertScaleAbs(src, alpha=1, beta=0)

# Thresholding
cv2.threshold(src, thresh, maxval, type)
cv2.adaptiveThreshold(src, maxval, adaptiveMethod, thresholdType, blockSize, C)

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
```

---

*Jobsheet ini adalah bagian dari Praktikum Computer Vision*
