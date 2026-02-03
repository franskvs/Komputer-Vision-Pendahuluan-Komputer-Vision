# PROJECT BAB 11: STRUCTURE FROM MOTION DAN SLAM

## 🎯 Tujuan Project

Mengimplementasikan sistem rekonstruksi 3D sederhana menggunakan teknik Structure from Motion untuk membuat model 3D dari objek nyata menggunakan smartphone atau webcam.

---

## 📖 Studi Kasus: "Digitalisasi Koleksi Museum Mini"

### Latar Belakang Cerita

Anda adalah seorang mahasiswa yang magang di **Museum Sejarah Kota**. Pihak museum ingin membuat **virtual tour** agar koleksi mereka bisa dilihat secara online oleh masyarakat yang tidak bisa berkunjung langsung. 

Kurator museum meminta Anda untuk membuat **model 3D** dari beberapa artefak koleksi museum menggunakan teknik **fotogrametri** (Structure from Motion). Model 3D ini nantinya akan ditampilkan di website museum sehingga pengunjung virtual bisa melihat artefak dari berbagai sudut.

### Tantangan

Museum memiliki budget terbatas, sehingga Anda harus menggunakan:
- **Smartphone** atau **webcam laptop** untuk mengambil foto
- **Software open-source** untuk proses rekonstruksi
- Hasil harus **cukup detail** untuk ditampilkan di website

---

## 📋 Deskripsi Tugas

### Tugas Utama

Buat sistem **rekonstruksi 3D** yang dapat:
1. Menerima input berupa sekuens gambar objek dari berbagai sudut
2. Mendeteksi dan mencocokkan fitur antar gambar
3. Mengestimasi pose kamera untuk setiap gambar
4. Merekonstruksi point cloud 3D dari objek
5. Memvisualisasikan hasil dalam format yang interaktif

### Spesifikasi Teknis

| Aspek | Requirement |
|-------|-------------|
| Input | Minimal 10 gambar dari berbagai sudut (coverage 360° atau lebih) |
| Output | Point cloud 3D dalam format PLY/PCD |
| Visualisasi | Viewer 3D interaktif (Open3D) |
| Akurasi | Reprojection error < 2 pixel |
| Dokumentasi | Readme lengkap dengan instruksi penggunaan |

---

## 🔨 Langkah Pengerjaan

### Fase 1: Persiapan Data (20%)

1. **Pilih Objek untuk Direkonstruksi**
   - Pilih objek bertekstur (hindari permukaan polos mengkilap)
   - Ukuran ideal: 10-50 cm
   - Contoh: patung kecil, vas bunga, mainan, buku 3D, sepatu

2. **Pengambilan Gambar**
   - Ambil minimal 15-20 foto dari berbagai sudut
   - Jaga overlap antar foto (70-80% overlap)
   - Gunakan pencahayaan merata
   - Hindari blur dan motion
   
   ```
   Pola Pengambilan Gambar:
   
        📷 12     📷 1     📷 2
           \       |       /
            \      |      /
   📷 11 ----  [OBJEK]  ---- 📷 3
            /      |      \
           /       |       \
        📷 10    📷 9     📷 4
        
   (Ambil juga dari atas dan bawah jika memungkinkan)
   ```

3. **Organisasi Data**
   ```
   project/
   ├── images/
   │   ├── img_001.jpg
   │   ├── img_002.jpg
   │   └── ...
   ├── output/
   └── main.py
   ```

### Fase 2: Feature Detection & Matching (25%)

1. **Implementasi Feature Detection**
   ```python
   # Minimal harus mengimplementasi:
   - Deteksi keypoint (SIFT/ORB/AKAZE)
   - Deskriptor extraction
   - Feature matching dengan ratio test
   - Visualisasi hasil matching
   ```

2. **Multi-View Matching**
   - Buat graph matching antar semua pasangan gambar
   - Filter outliers dengan geometric verification
   - Output: Tabel korespondensi antar gambar

### Fase 3: Pose Estimation (25%)

1. **Estimasi Relative Pose**
   - Hitung Essential Matrix untuk setiap pasangan
   - Dekomposisi menjadi Rotation dan Translation
   - Verifikasi dengan positive depth constraint

2. **Incremental Reconstruction**
   ```python
   # Pipeline:
   1. Pilih initial pair dengan baseline terbaik
   2. Triangulasi initial points
   3. Loop: untuk setiap gambar baru
      a. Estimate pose dengan PnP
      b. Triangulasi points baru
      c. Bundle Adjustment (optional)
   ```

### Fase 4: Rekonstruksi 3D (20%)

1. **Triangulasi**
   - Implementasi triangulasi untuk semua titik yang di-match
   - Filter outliers berdasarkan reprojection error

2. **Bundle Adjustment** (Bonus)
   - Optimasi posisi 3D points dan camera poses
   - Gunakan library scipy.optimize

3. **Point Cloud Generation**
   - Export ke format PLY
   - Tambahkan warna dari gambar asli (optional)

### Fase 5: Visualisasi & Dokumentasi (10%)

1. **Visualisasi Interaktif**
   ```python
   # Tampilkan:
   - Point cloud hasil rekonstruksi
   - Posisi kamera dalam koordinat 3D
   - Trajectory kamera
   ```

2. **Dokumentasi**
   - README dengan instruksi lengkap
   - Contoh hasil
   - Troubleshooting guide

---

## 📊 Deliverables

### Yang Harus Dikumpulkan:

1. **Source Code** (`/src/`)
   - `feature_matching.py` - Modul feature detection & matching
   - `pose_estimation.py` - Modul estimasi pose kamera
   - `triangulation.py` - Modul triangulasi
   - `reconstruction.py` - Main pipeline
   - `visualization.py` - Modul visualisasi

2. **Data & Output** (`/data/` dan `/output/`)
   - Gambar input yang digunakan
   - Point cloud hasil (`.ply`)
   - Screenshot hasil visualisasi

3. **Dokumentasi**
   - `README.md` - Instruksi penggunaan
   - `REPORT.md` - Laporan proses dan hasil

4. **Video Demo** (3-5 menit)
   - Demo program berjalan
   - Penjelasan hasil

---

## 📝 Kriteria Evaluasi

### Rubrik Penilaian

| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| **Fungsionalitas** | 40% | Program berjalan dan menghasilkan output 3D |
| **Kualitas Hasil** | 25% | Keakuratan rekonstruksi, visual yang baik |
| **Kode** | 20% | Clean code, modular, dokumentasi |
| **Laporan** | 10% | Kelengkapan, analisis, kesimpulan |
| **Bonus** | 5% | Bundle adjustment, dense reconstruction |

### Detail Penilaian Fungsionalitas

| Fitur | Poin |
|-------|------|
| Feature matching berjalan | 10 |
| Fundamental/Essential Matrix correct | 10 |
| Pose estimation berjalan | 10 |
| Triangulasi menghasilkan 3D points | 10 |
| Visualisasi 3D berjalan | 5 |
| Export ke PLY | 5 |
| **Subtotal** | **50** |

---

## 💡 Tips dan Hints

### Tips Pengambilan Gambar
- Gunakan tripod atau permukaan stabil
- Rotasi objek daripada kamera jika memungkinkan
- Background polos (putih/hitam) membantu segmentasi
- Pencahayaan diffuse (tidak direct sunlight)

### Tips Programming
- Mulai dari 2 gambar, baru scale ke banyak gambar
- Visualisasi intermediate results untuk debugging
- Log reprojection error untuk setiap step

### Common Pitfalls
- Objek terlalu glossy → tidak ada fitur
- Overlap terlalu sedikit → matching gagal
- Scale ambiguity → 3D tidak ter-scale absolut

---

## 📅 Timeline Pengerjaan

| Minggu | Target |
|--------|--------|
| 1 | Pengambilan gambar, setup project |
| 2 | Feature detection & matching |
| 3 | Pose estimation & triangulasi |
| 4 | Integrasi, testing, dokumentasi |

---

## 🌟 Challenge Tambahan (Bonus)

Untuk nilai maksimal, implementasikan salah satu fitur tambahan:

1. **Dense Reconstruction**
   - Gunakan stereo matching untuk membuat dense point cloud

2. **Mesh Generation**
   - Convert point cloud ke mesh menggunakan Poisson reconstruction

3. **Real-time SfM**
   - Implementasi dengan webcam streaming

4. **AR Overlay**
   - Tampilkan model 3D di posisi yang benar menggunakan AR

---

## 📚 Referensi Pendukung

1. OpenCV Camera Calibration Tutorial
2. Open3D Documentation
3. "Multiple View Geometry" - Hartley & Zisserman
4. OpenSfM (implementasi reference)

---

**Selamat mengerjakan! Jika ada pertanyaan, silakan hubungi asisten praktikum.**
