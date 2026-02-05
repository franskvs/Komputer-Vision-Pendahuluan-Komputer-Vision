# 🚀 QUICK START GUIDE - BAB 11: STRUCTURE FROM MOTION

## ⚡ Cara Cepat Mulai

### 1. Persiapan (5 menit)

```bash
# Masuk ke direktori
cd "~/Documents/Praktikum Komputer Vision/Bab-11-Structure-from-Motion/praktikum"

# Download/Generate sample data
python3 download_sample_data.py

# Test semua program (opsional)
python3 test_all_programs.py
```

### 2. Jalankan Program Per Program

#### Program 1: Feature Matching (3 detik)
```bash
python3 01_feature_matching_multiview.py
```
**Output**: Keypoints dan matches visualization

#### Program 2: Fundamental Matrix (4 detik)
```bash
python3 02_fundamental_matrix.py
```
**Output**: Epipolar lines dan error distribution

#### Program 3: Essential Matrix (3 detik)
```bash
python3 03_essential_matrix.py
```
**Output**: Camera pose estimation

#### Program 4: Triangulasi 3D (4 detik)
```bash
python3 04_triangulasi_3d.py
```
**Output**: 3D point cloud

#### Program 5: Visual Odometry (3 detik)
```bash
python3 05_visual_odometry.py
```
**Output**: Camera trajectory

#### Program 6: Bundle Adjustment (4 detik)
```bash
python3 06_bundle_adjustment.py
```
**Output**: Optimized reconstruction

#### Program 7: Simple SLAM (4 detik)
```bash
python3 07_simple_slam.py
```
**Output**: SLAM map dan trajectory

### 3. Lihat Hasil

```bash
# Buka folder output
cd output/
ls -lh

# Atau buka dengan file manager
xdg-open .
```

## 📊 Struktur Direktori

```
Bab-11-Structure-from-Motion/
├── Jobsheet.md              ← Panduan praktikum
├── Materi.md                ← Teori pembelajaran
├── Project.md               ← Studi kasus project
├── SUMMARY.md               ← Ringkasan lengkap
├── VERIFICATION_REPORT.md   ← Laporan verifikasi
├── praktikum/
│   ├── 01_feature_matching_multiview.py
│   ├── 02_fundamental_matrix.py
│   ├── 03_essential_matrix.py
│   ├── 04_triangulasi_3d.py
│   ├── 05_visual_odometry.py
│   ├── 06_bundle_adjustment.py
│   ├── 07_simple_slam.py
│   ├── download_sample_data.py
│   ├── test_all_programs.py
│   ├── data/
│   │   └── images/          ← Sample images
│   └── output/              ← Hasil visualisasi
└── PDF/
    └── Bab-11-Structure from motion and SLAM.pdf
```

## 🎯 Tips Praktikum

### Untuk Mahasiswa:
1. **Baca Materi.md** terlebih dahulu untuk memahami konsep
2. **Ikuti Jobsheet.md** step-by-step
3. **Jalankan program** dan amati output
4. **Catat hasil** di tabel pengamatan
5. **Analisis** perbedaan parameter dan hasilnya

### Untuk Dosen/Instruktur:
1. Semua program **auto-run** tanpa perlu manual intervention
2. Output **tersimpan otomatis** di folder output/
3. Bisa running di **headless server** untuk automated grading
4. Test report tersedia di `output/test_report.txt`

## ⚙️ Konfigurasi Program

### Setiap program punya variabel konfigurasi di bagian atas:

**Contoh (01_feature_matching_multiview.py)**:
```python
DETECTOR_TYPE = 'SIFT'     # Ganti: 'ORB', 'AKAZE', 'BRISK'
MAX_FEATURES = 2000        # Sesuaikan jumlah fitur
RATIO_THRESHOLD = 0.75     # Lowe's ratio test
```

### Eksperimen yang Bisa Dicoba:
1. Ganti detector type (SIFT/ORB/AKAZE)
2. Ubah parameter threshold
3. Bandingkan akurasi vs kecepatan
4. Coba dengan gambar sendiri

## 📝 Output yang Dihasilkan

### Total: ~15 file visualisasi

```
output/
├── 01_feature_matches_SIFT.png       (3.7 MB)
├── 01_keypoints_img1_SIFT.png        (2.7 MB)
├── 01_keypoints_img2_SIFT.png        (2.7 MB)
├── 02_epipolar_lines.png             (294 KB)
├── 02_epipolar_error_dist.png        (54 KB)
├── 03_camera_poses.png               (180 KB)
├── 03_essential_matrix.png           (49 KB)
├── 04_triangulated_points.png        (179 KB)
├── 04_reprojection_error.png         (40 KB)
├── 05_vo_trajectory.png              (181 KB)
├── 05_feature_count.png              (38 KB)
├── 06_ba_reconstruction.png          (417 KB)
├── 06_ba_error_comparison.png        (63 KB)
├── 07_slam_result.png                (186 KB)
└── test_report.txt                   (8.5 KB)
```

## 🔧 Troubleshooting

### Problem: "Module not found"
```bash
pip install opencv-python opencv-contrib-python numpy scipy matplotlib open3d
```

### Problem: "File not found"
```bash
# Jalankan download script
python3 download_sample_data.py
```

### Problem: Program tidak menghasilkan output
```bash
# Check folder output ada
ls output/

# Jika tidak ada, buat manual
mkdir output
```

### Problem: Permission denied
```bash
chmod +x *.py
```

## 📚 Dokumentasi Lengkap

- **Teori**: Lihat [Materi.md](Materi.md)
- **Praktikum**: Lihat [Jobsheet.md](Jobsheet.md)
- **Project**: Lihat [Project.md](Project.md)
- **Verifikasi**: Lihat [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)
- **Ringkasan**: Lihat [SUMMARY.md](SUMMARY.md)

## ✅ Checklist Sebelum Mulai

- [ ] Python 3.8+ terinstall
- [ ] Library installed (OpenCV, NumPy, etc.)
- [ ] Sample data downloaded
- [ ] Sudah baca Materi.md (minimal overview)
- [ ] Punya waktu 3-4 jam untuk praktikum penuh

## 🎯 Learning Path Recommended

1. **Week 1**: Theory (Materi.md) + Program 1-3
2. **Week 2**: Program 4-5 + Analisis
3. **Week 3**: Program 6-7 + Project
4. **Week 4**: Finalisasi project + Laporan

## 🌟 Real-World Applications

Setelah selesai praktikum, Anda akan bisa:

- ✅ Memahami cara kerja **Google Photos** (3D dari foto)
- ✅ Memahami **smartphone AR** (ARKit, ARCore)
- ✅ Memahami **robot vacuum** (SLAM untuk mapping)
- ✅ Memahami **self-driving cars** (visual odometry)
- ✅ Memahami **drone mapping** (fotogrametri)
- ✅ Memahami **film VFX** (match-move, camera tracking)

## 📊 Estimated Time

| Task | Time |
|------|------|
| Setup | 5 min |
| Program 1-3 | 1-1.5 hours |
| Program 4-5 | 1 hour |
| Program 6-7 | 1 hour |
| Analysis | 30 min |
| **Total Practical** | **3-4 hours** |
| Project | 4-6 hours |
| **Grand Total** | **7-10 hours** |

## 🎓 Support

### Jika Ada Pertanyaan:
1. Cek VERIFICATION_REPORT.md untuk detail teknis
2. Lihat test_report.txt untuk hasil testing
3. Baca comments di dalam kode program
4. Konsultasi dengan instruktur

---

**Ready to Start?** 🚀

```bash
cd praktikum/
python3 download_sample_data.py
python3 01_feature_matching_multiview.py
```

**Happy Learning!** 🎓✨
