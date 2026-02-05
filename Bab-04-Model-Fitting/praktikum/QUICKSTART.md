# QUICK START GUIDE - BAB 4 MODEL FITTING

## ⚡ LANGKAH CEPAT (5 MENIT)

### 1️⃣ Setup Images (Pertama Kali Saja)
```bash
cd "Bab-04-Model-Fitting/praktikum"
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

# Feature Detection (dasar!)
python3 01_feature_detection.py

# Feature Matching
python3 02_feature_matching.py

# RANSAC (paling penting!)
python3 03_ransac.py

# Hough Lines
python3 04_hough_lines.py

# Optical Flow
python3 08_optical_flow.py
```

---

## 📂 LIHAT HASIL

Semua output tersimpan di:
```
output/
├── output1/   ← Feature Detection (MUST SEE!)
├── output2/   ← Feature Matching
├── output3/   ← RANSAC
├── output4/   ← Hough Lines
├── output5/   ← Hough Circles
├── output6/   ← Homography
├── output7/   ← Perspective Correction
├── output8/   ← Optical Flow
├── output9/   ← Scattered Interpolation
├── output10/  ← Variational Regularization
└── output11/  ← MRF Denoising
```

---

## 🎯 PROGRAM FAVORIT (MUST TRY)

| Program | File | Wow Factor | Real App |
|---------|------|------------|----------|
| **Feature Detection** | `01_feature_detection.py` | ⭐⭐⭐⭐⭐ | Object Recognition |
| **RANSAC** | `03_ransac.py` | ⭐⭐⭐⭐⭐ | Robust Estimation |
| **Hough Lines** | `04_hough_lines.py` | ⭐⭐⭐⭐⭐ | Lane Detection |
| **Homography** | `06_homography.py` | ⭐⭐⭐⭐ | Image Stitching |
| **Optical Flow** | `08_optical_flow.py` | ⭐⭐⭐⭐ | Motion Tracking |

---

## 🔥 DEMO UNTUK PRESENTASI

### Demo 1: Feature Detection Comparison
```bash
python3 01_feature_detection.py
```
**Output:** Harris, ORB, SIFT, AKAZE keypoints comparison

### Demo 2: RANSAC Line Fitting
```bash
python3 03_ransac.py
```
**Output:** Robust line fitting with outlier rejection

### Demo 3: Hough Transform for Lines
```bash
python3 04_hough_lines.py
```
**Output:** Line detection in images

### Demo 4: Homography Estimation
```bash
python3 06_homography.py
```
**Output:** Perspective transformation between images

---

## 🎨 GAMBAR YANG TERSEDIA

| Image | Ukuran | Best For | Deskripsi |
|-------|--------|----------|-----------|
| `portrait.jpg` | 512×512 | Programs 1-2 | Feature detection |
| `building.jpg` | 400×500 | Programs 4,6,7 | Lines & perspective |
| `coins.jpg` | 400×400 | Program 5 | Circle detection |
| `road.jpg` | 640×480 | Program 4 | Lane detection |

---

## ⚠️ TROUBLESHOOTING

### Error "No module named cv2"
```bash
pip install opencv-python opencv-contrib-python numpy matplotlib scipy
```

### SIFT tidak tersedia
```bash
pip install opencv-contrib-python
```

### Gambar tidak ditemukan
```bash
python3 setup_images.py
```
