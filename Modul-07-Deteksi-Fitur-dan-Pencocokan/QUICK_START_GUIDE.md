# 🚀 QUICK START GUIDE - BAB 07 DETEKSI FITUR DAN PENCOCOKAN

## Untuk Menjalankan Praktikum

### Option 1: Jalankan Satu Program Spesifik
```bash
cd /home/sirobo/Documents/Praktikum\ Komputer\ Vision/Bab-07-Deteksi-Fitur-dan-Pencocokan/praktikum

# Contoh: Jalankan Harris Corner Detection
python3 01_harris_corner.py

# Atau: Jalankan SIFT
python3 03_sift_detection.py

# Atau: Jalankan FAST (New)
python3 10_fast_detection.py
```

### Option 2: Jalankan Semua Program (Test Suite)
```bash
cd /home/sirobo/Documents/Praktikum\ Komputer\ Vision/Bab-07-Deteksi-Fitur-dan-Pencocokan/praktikum
python3 run_all_praktikum.py
```

---

## 📖 Daftar 10 Program Praktikum

| No | Program | Topik | Durasi | Output |
|----|---------|-------|--------|---------|
| 01 | `01_harris_corner.py` | Harris Corner Detection | ~1s | 3 images |
| 02 | `02_shi_tomasi.py` | Shi-Tomasi Good Features | ~2s | 4 images |
| 03 | `03_sift_detection.py` | SIFT Feature Detection | ~2s | 4 images |
| 04 | `04_orb_detection.py` | ORB Fast Features | ~1s | 5 images |
| 05 | `05_bf_matching.py` | Brute-Force Matching | ~2s | 4 images |
| 06 | `06_flann_matching.py` | FLANN Matching | ~2s | 3 images |
| 07 | `07_homography_ransac.py` | Homography RANSAC | ~2s | 3 images |
| 08 | `08_real_world_example.py` | Document Scanner | ~3s | 2 images |
| 09 | `09_akaze_detection.py` | AKAZE Detection ⭐ | ~1s | 3 images |
| 10 | `10_fast_detection.py` | FAST Detection ⭐ | ~1s | 4 images |

**⭐ NEW** = Algoritma baru yang ditambahkan

---

## 🎯 Topik Pembelajaran Berdasarkan Waktu

### Pendek (Untuk Demo) - 15 menit
1. **01_harris_corner.py** (1 min) → Konsep dasar corner detection
2. **03_sift_detection.py** (2 min) → Scale-invariant features
3. **05_bf_matching.py** (2 min) → Feature matching concept
4. **10_fast_detection.py** (1 min) → Real-time detection

### Menengah (Session Praktikum) - 45 menit
1. **01_harris_corner.py** (5 min) → Corner detection
2. **02_shi_tomasi.py** (5 min) → Improvement from Harris
3. **03_sift_detection.py** (5 min) → Scale/rotation invariance
4. **04_orb_detection.py** (5 min) → Fast & compact features
5. **05_bf_matching.py** (5 min) → Matching algorithm
6. **07_homography_ransac.py** (5 min) → RANSAC robustness
7. **08_real_world_example.py** (10 min) → Application example

### Lengkap (Full Course) - 90+ menit
Jalankan semua 10 program secara berurutan dengan eksperimen parameter.

---

## 🔬 Eksperimen Cepat (Parameter Tweaking)

Setiap program memiliki parameter yang bisa diubah di bagian atas:

### 01_harris_corner.py
```python
BLOCK_SIZE = 2       # Ubah ke 3, 5, 7 untuk hasil berbeda
K_VALUE = 0.04       # Ubah ke 0.02 atau 0.08
THRESHOLD_PERCENT = 0.01  # Ubah ke 0.005 atau 0.1
```

### 03_sift_detection.py
```python
N_FEATURES = 500     # Ubah ke 2000 untuk lebih banyak features
CONTRAST_THRESHOLD = 0.04  # Ubah ke 0.08 untuk lebih ketat
```

### 10_fast_detection.py
```python
FAST_THRESHOLD = 20  # Ubah ke 5 (banyak) atau 40 (sedikit)
```

---

## 📊 Hasil Output yang Diharapkan

Setelah menjalankan semua program, folder `output/` akan berisi:

```
output/
├── harris_*.jpg              (3 files)
├── shi_tomasi_*.jpg          (4 files)
├── sift_*.jpg                (4 files)
├── orb_*.jpg                 (5 files)
├── bf_match_*.jpg            (4 files)
├── flann_match_*.jpg         (3 files)
├── homography_*.jpg          (3 files)
├── demo_document.jpg         (1 file)
├── document_scanner_demo.jpg (1 file)
├── akaze_*.jpg               (3 files)
└── fast_*.jpg                (4 files)
```

**Total: 42 file gambar hasil visualisasi**

---

## 💡 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'cv2'"
```bash
# Install OpenCV
pip install opencv-python numpy
```

### Error: "Data files not found"
```bash
# Pastikan sudah di folder praktikum
cd /home/sirobo/Documents/Praktikum\ Komputer\ Vision/Bab-07-Deteksi-Fitur-dan-Pencocokan/praktikum

# Download sample data jika belum ada
python3 download_sample_data.py
```

### Output folder kosong
```bash
# Cek permission dan buat folder output
mkdir -p output/
chmod 777 output/
```

---

## 📚 Materi Pendukung

- **Materi.md** → Penjelasan teori & konsep algoritma
- **Jobsheet.md** → Daftar percobaan & soal untuk mahasiswa
- **Referensi.md** → 50+ paper, tutorial, dataset links
- **FINAL_COMPLETION_REPORT.md** → Laporan lengkap work completion

---

## 🎓 Learning Path Rekomendasi

**Minggu 1: Foundation (Corner Detection)**
- Baca: Materi.md Section 2.1 (Harris)
- Jalankan: 01_harris_corner.py
- Eksperimen: Ubah BLOCK_SIZE, K_VALUE
- Soal: Jobsheet.md Percobaan 1

**Minggu 2: Advanced Corner Detection**
- Baca: Materi.md Section 2.2 (Shi-Tomasi)
- Jalankan: 02_shi_tomasi.py
- Bandingkan: Hasil Harris vs Shi-Tomasi
- Soal: Jobsheet.md Percobaan 2

**Minggu 3: Scale-Invariant Features**
- Baca: Materi.md Section 2.3 (SIFT)
- Jalankan: 03_sift_detection.py
- Perhatikan: sift_invariance_demo.jpg
- Soal: Jobsheet.md Percobaan 3

**Minggu 4: Fast Features**
- Baca: Materi.md Section 2.5-2.6 (AKAZE, ORB, FAST)
- Jalankan: 04_orb_detection.py, 09_akaze_detection.py, 10_fast_detection.py
- Bandingkan: Speed vs accuracy
- Soal: Jobsheet.md Percobaan 4, 9, 10

**Minggu 5: Feature Matching**
- Baca: Materi.md Section 3 (Matching)
- Jalankan: 05_bf_matching.py, 06_flann_matching.py
- Analisis: BF vs FLANN performance
- Soal: Jobsheet.md Percobaan 5, 6

**Minggu 6: Robust Matching & Homography**
- Baca: Materi.md Section 4 (Homography, RANSAC)
- Jalankan: 07_homography_ransac.py
- Perhatikan: Inlier vs outlier filtering
- Soal: Jobsheet.md Percobaan 7

**Minggu 7: Real-World Application**
- Baca: Materi.md Section 5
- Jalankan: 08_real_world_example.py
- Proyek: Buat aplikasi sendiri
- Soal: Jobsheet.md Percobaan 8

---

## ✅ Checklist Sebelum Presentasi

- [ ] Semua 10 program sudah dijalankan
- [ ] Output folder berisi 42 gambar
- [ ] Setiap program sudah diuji parameter variations
- [ ] Membaca & memahami Materi.md
- [ ] Mengerjakan semua soal di Jobsheet.md
- [ ] Membaca 5+ paper dari Referensi.md
- [ ] Siap menjawab pertanyaan tentang setiap algoritma

---

## 📞 Quick Reference Commands

```bash
# Masuk ke folder praktikum
cd "/home/sirobo/Documents/Praktikum Komputer Vision/Bab-07-Deteksi-Fitur-dan-Pencocokan/praktikum"

# Jalankan 1 program tertentu
python3 01_harris_corner.py

# Jalankan 2-3 program sekaligus
for prog in 01 03 05; do python3 ${prog}_*.py; done

# Check hasil output
ls output/ | wc -l      # Count total files
ls output/*.jpg | head   # List first files

# Clean output folder (jika perlu restart)
rm output/*.jpg

# View hasil gambar (dari VSCode atau file explorer)
# File ada di: praktikum/output/
```

---

## 🌟 Pro Tips

1. **Jalankan program dalam urutan:** Dari simple (Harris) → Complex (Homography)
2. **Eksperimen parameter:** Ubah nilai, lihat perbedaan
3. **Baca dokumentasi di kode:** Setiap function dijelaskan dengan cv2.putText() parameter
4. **Gunakan output images:** Bandingkan hasil berbagai algoritma
5. **Catat observasi:** Saat eksperimen, catat perubahan yang terlihat

---

**Last Updated:** February 5, 2026  
**Status:** ✅ All 10 programs tested & working
