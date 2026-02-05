# QUICK START GUIDE - BAB 3 PEMROSESAN CITRA

## ⚡ LANGKAH CEPAT (5 MENIT)

### 1️⃣ Setup Images (Pertama Kali Saja)
```bash
cd "Bab-03-Pemrosesan-Citra/praktikum"
python3 setup_images.py
```
✅ Output: Gambar di `data/images/`

---

### 2️⃣ Test Semua Program (Opsional - Verifikasi)
```bash
python3 run_all_tests.py
```
✅ Output: Verification report + output files

---

### 3️⃣ Jalankan Program Individual
```bash
# Program populer:

# Brightness & Contrast (paling dasar)
python3 01_brightness_contrast.py

# Edge Detection (paling menarik!)
python3 06_edge_detection.py

# Morphological Operations
python3 07_morphological_operations.py

# Fourier Transform (frequency domain)
python3 10_fourier_transform.py
```

---

## 📂 LIHAT HASIL

Semua output tersimpan di:
```
output/
├── output1/   ← Brightness & Contrast
├── output2/   ← Gamma Correction
├── output3/   ← Thresholding
├── output4/   ← Histogram Equalization
├── output5/   ← Spatial Filtering
├── output6/   ← Edge Detection (MUST SEE!)
├── output7/   ← Morphological Operations
├── output8/   ← Enhancement Pipeline
├── output9/   ← Compositing & Matting
├── output10/  ← Fourier Transform
├── output11/  ← Pyramids & Wavelets
├── output12/  ← Geometric Transformations
├── output13/  ← Steerable Filters
├── output14/  ← Interpolation & Decimation
├── output15/  ← Advanced Blending
└── output16/  ← Mesh Warping & Morphing
```

---

## 🎯 PROGRAM FAVORIT (MUST TRY)

| Program | File | Wow Factor | Real App |
|---------|------|------------|----------|
| **Edge Detection** | `06_edge_detection.py` | ⭐⭐⭐⭐⭐ | Object Detection |
| **Fourier Transform** | `10_fourier_transform.py` | ⭐⭐⭐⭐⭐ | Signal Processing |
| **Morphological Ops** | `07_morphological_operations.py` | ⭐⭐⭐⭐ | Shape Analysis |
| **Histogram Eq** | `04_histogram_equalization.py` | ⭐⭐⭐⭐ | Photo Enhancement |
| **Mesh Warping** | `16_mesh_warping_morphing.py` | ⭐⭐⭐⭐ | Face Morphing |

---

## 🔥 DEMO UNTUK PRESENTASI

### Demo 1: Edge Detection Pipeline
```bash
python3 06_edge_detection.py
```
**Output:** Sobel, Laplacian, Canny edge detection comparison

### Demo 2: Frequency Domain Analysis
```bash
python3 10_fourier_transform.py
```
**Output:** FFT, frequency filtering, magnitude spectrum

### Demo 3: Morphological Operations
```bash
python3 07_morphological_operations.py
```
**Output:** Erosion, dilation, opening, closing comparison

### Demo 4: Face Morphing
```bash
python3 16_mesh_warping_morphing.py
```
**Output:** Image warping and morphing animation

---

## 🎨 GAMBAR YANG TERSEDIA

| Image | Ukuran | Best For | Deskripsi |
|-------|--------|----------|-----------|
| `portrait.jpg` | 512×512 | Programs 1-8 | Face image |
| `text_document.jpg` | 600×800 | Program 3 | OCR preprocessing |
| `noise_sample.jpg` | 400×400 | Programs 5,7 | Denoising demo |
| `edges_demo.png` | 400×400 | Program 6 | Edge detection |

---

## ⚠️ TROUBLESHOOTING

### Error "No module named cv2"
```bash
pip install opencv-python numpy matplotlib scipy
```

### Gambar tidak ditemukan
```bash
python3 setup_images.py
```

### Program lambat
Beberapa program (10-16) memerlukan waktu lebih lama karena algoritma kompleks.
