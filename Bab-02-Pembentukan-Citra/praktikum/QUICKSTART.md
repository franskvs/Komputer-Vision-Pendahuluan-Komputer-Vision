# QUICK START GUIDE - BAB 2 PEMBENTUKAN CITRA

## ⚡ LANGKAH CEPAT (5 MENIT)

### 1️⃣ Generate Images (Pertama Kali Saja)
```bash
cd "Bab-02-Pembentukan-Citra/praktikum"
python3 setup_images.py
```
✅ Output: 10 gambar di `data/images/`

---

### 2️⃣ Test Semua Program (Opsional - Verifikasi)
```bash
python3 run_all_tests.py
```
✅ Output: Verification report + 22 output files

---

### 3️⃣ Jalankan Program Individual
```bash
# Contoh program populer:

# Document Scanner (paling menarik!)
python3 06_document_scanner_auto.py

# Perspective Transform
python3 05_perspektif_transform_auto.py

# Transformasi dasar
python3 01_translasi.py
python3 02_rotasi.py
python3 03_scaling.py
```

---

## 📂 LIHAT HASIL

Semua output tersimpan di:
```
output/
├── output1/  ← Translasi
├── output2/  ← Rotasi
├── output3/  ← Scaling
├── output5/  ← Perspektif Transform
├── output6/  ← Document Scanner (4 images!)
└── ... (11 folders lagi)
```

---

## 🎯 PROGRAM FAVORIT (MUST TRY)

| Program | File | Wow Factor | Real App |
|---------|------|------------|----------|
| **Document Scanner** | `06_document_scanner_auto.py` | ⭐⭐⭐⭐⭐ | CamScanner |
| **Perspective Fix** | `05_perspektif_transform_auto.py` | ⭐⭐⭐⭐⭐ | KTP Scanner |
| **Color Spaces** | `12_color_spaces.py` | ⭐⭐⭐⭐ | Instagram |
| **Compression** | `15_compression_artifacts.py` | ⭐⭐⭐⭐ | JPEG Optimizer |
| **3D Rotation** | `08_3d_rotation.py` | ⭐⭐⭐ | Game Engine |

---

## 🔥 DEMO FAVORIT UNTUK PRESENTASI

### Demo 1: Mobile Scanner Simulation
```bash
python3 06_document_scanner_auto.py
```
**Output:** 4 images showing complete scanning pipeline
- Original → Edge Detection → Detected → Scanned (B&W)

### Demo 2: Perspective Correction
```bash
python3 05_perspektif_transform_auto.py
```
**Output:** Before/After comparison
- Miring → Lurus (Bird's eye view)

### Demo 3: Complete Transformation Suite
```bash
python3 01_translasi.py      # Translation
python3 02_rotasi.py          # Rotation
python3 03_scaling.py         # Scaling
python3 04_affine_transform.py # Combined
```
**Output:** Visual comparison of all transformation types

---

## 🎨 GAMBAR YANG TERSEDIA

| Image | Size | Best For | Description |
|-------|------|----------|-------------|
| `portrait.jpg` | 512×512 | Programs 1-4 | Realistic synthetic face |
| `document.jpg` | 600×800 | Programs 5-6 | Receipt/struk |
| `building.jpg` | 400×500 | Program 5 | Perspective demo |
| `coins.jpg` | 300×400 | Program 3 | Metallic objects |
| `peppers.jpg` | 512×512 | Program 12 | Vibrant colors |
| `checkerboard.png` | 512×512 | Program 7 | Calibration |

---

## ⚙️ EKSPERIMEN PARAMETER

Buka file program dan ubah variabel di bagian atas:

### `01_translasi.py`
```python
TX = 100  # Ubah ke: -100, 0, 50, 150
TY = 50   # Ubah ke: -50, 0, 30, 100
```

### `02_rotasi.py`
```python
SUDUT_ROTASI = 45  # Ubah ke: 15, 30, 90, 180
SKALA = 1.0        # Ubah ke: 0.5, 1.5, 2.0
```

### `03_scaling.py`
```python
SKALA_X = 2.0  # Ubah ke: 0.5, 1.0, 3.0
SKALA_Y = 2.0  # Ubah ke: 0.5, 1.0, 3.0
```

---

## ✅ CHECKLIST PRAKTIKUM

- [ ] Run `setup_images.py` untuk generate gambar
- [ ] Test dengan `run_all_tests.py` (pastikan 15/15 PASS)
- [ ] Jalankan minimal 5 program individual
- [ ] Lihat output images di folder `output/`
- [ ] Baca komentar di kode untuk pahami konsep
- [ ] Eksperimen dengan parameter berbeda
- [ ] Coba dengan gambar sendiri (opsional)

---

## 🆘 TROUBLESHOOTING

### Error: Module not found
```bash
pip install opencv-python matplotlib numpy
```

### Error: File tidak ditemukan
```bash
# Pastikan di folder yang benar
pwd
# Output harus: .../Bab-02-Pembentukan-Citra/praktikum

# Generate ulang images
python3 setup_images.py
```

### Output kosong
```bash
# Check permission folder
ls -la output/

# Recreate folder
rm -rf output/
mkdir output/
```

---

## 📊 EXPECTED RESULTS

Setelah run semua, Anda harus punya:
- ✅ 10 gambar di `data/images/`
- ✅ 15 folder di `output/` (output1 sampai output15)
- ✅ 22 output images total
- ✅ 1 verification report

---

## 💻 ONE-LINER (Run Everything)

```bash
# Setup + Test semua sekaligus
python3 setup_images.py && python3 run_all_tests.py
```

⏱️ **Total time:** ~25 detik

---

## 🎓 KONSEP KUNCI

| Program | Konsep Utama | Formula/Function |
|---------|--------------|------------------|
| 01 | Translation | `M = [[1,0,tx],[0,1,ty]]` |
| 02 | Rotation | `cv2.getRotationMatrix2D()` |
| 03 | Scaling | `cv2.resize()` + interpolation |
| 04 | Affine | `cv2.getAffineTransform()` (3 points) |
| 05 | Perspective | `cv2.getPerspectiveTransform()` (4 points) |
| 06 | Scanner | Canny + Contours + Warp |
| 07 | Calibration | `cv2.calibrateCamera()` |
| 12 | Color | `cv2.cvtColor()` RGB↔HSV↔LAB |
| 13 | Gamma | `I_out = I_in^(1/γ)` |
| 15 | JPEG | Quality parameter 0-100 |

---

**Total Reading Time:** 3 minutes  
**Setup Time:** 2 minutes  
**Hands-on Time:** 5-30 minutes (tergantung eksplorasi)

✨ **Selamat Belajar!** ✨
