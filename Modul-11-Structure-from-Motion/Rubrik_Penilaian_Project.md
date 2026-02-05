# RUBRIK PENILAIAN PROJECT
# BAB 11: STRUCTURE FROM MOTION DAN SLAM

---

## 📊 Komponen Penilaian

| No | Komponen | Bobot |
|----|----------|-------|
| 1 | Fungsionalitas Program | 40% |
| 2 | Kualitas Hasil Rekonstruksi | 25% |
| 3 | Kualitas Kode | 20% |
| 4 | Dokumentasi dan Laporan | 10% |
| 5 | Bonus Features | 5% |

---

## 📋 Detail Rubrik Penilaian

### 1. Fungsionalitas Program (40%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Feature Detection** | Mendeteksi keypoints dengan akurat pada semua gambar, menggunakan >1 detector | Deteksi berjalan baik dengan 1 detector | Deteksi berjalan tapi ada error minor | Tidak berjalan atau banyak error |
| **Feature Matching** | Matching akurat dengan outlier filtering (RANSAC), visualisasi lengkap | Matching berjalan dengan ratio test | Matching basic tanpa filtering | Matching tidak berjalan |
| **Pose Estimation** | Essential/Fundamental matrix benar, dekomposisi R,t akurat | Estimasi berjalan dengan error kecil | Estimasi berjalan tapi tidak konsisten | Tidak dapat mengestimasi pose |
| **Triangulasi** | Point cloud 3D akurat, reprojection error <2px | Point cloud bagus, error <5px | Point cloud terbentuk tapi noisy | Triangulasi gagal |
| **Visualisasi** | 3D viewer interaktif, camera poses ditampilkan | Visualisasi 3D static berjalan | Visualisasi 2D saja | Tidak ada visualisasi |

**Skor Maksimal: 20 poin × 2 = 40 poin**

---

### 2. Kualitas Hasil Rekonstruksi (25%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Akurasi Geometri** | Bentuk 3D sangat mirip objek asli, proporsi tepat | Bentuk mirip dengan deformasi minor | Bentuk dapat dikenali tapi ada distorsi | Bentuk tidak menyerupai objek |
| **Kelengkapan Point Cloud** | Coverage >80% permukaan objek | Coverage 60-80% | Coverage 40-60% | Coverage <40% |
| **Noise Level** | Point cloud bersih, outlier minimal | Sedikit noise, dapat diterima | Noise cukup banyak | Sangat noisy |
| **Konsistensi Multi-View** | Semua view terintegrasi dengan baik | Sebagian besar view konsisten | Beberapa view tidak konsisten | Banyak inkonsistensi |

**Skor Maksimal: 16 poin × 1.5625 = 25 poin**

---

### 3. Kualitas Kode (20%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Struktur & Modularitas** | Kode terorganisir dalam modul terpisah, class-based | Fungsi terpisah dengan baik | Kode dalam satu file tapi terstruktur | Kode tidak terstruktur |
| **Readability** | Nama variabel/fungsi deskriptif, formatting konsisten | Sebagian besar readable | Ada bagian yang sulit dibaca | Sulit dipahami |
| **Dokumentasi Kode** | Docstring lengkap, komentar informatif | Docstring ada, komentar cukup | Minimal komentar | Tidak ada dokumentasi |
| **Error Handling** | Exception handling lengkap, pesan error informatif | Error handling untuk kasus utama | Minimal error handling | Tidak ada error handling |
| **Efisiensi** | Algoritma optimal, memory efficient | Efisien untuk skala project | Ada redundansi minor | Tidak efisien |

**Skor Maksimal: 20 poin × 1 = 20 poin**

---

### 4. Dokumentasi dan Laporan (10%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **README** | Instruksi lengkap, dependencies jelas, contoh penggunaan | Instruksi cukup lengkap | Instruksi basic | README tidak ada/tidak lengkap |
| **Laporan Teknis** | Analisis mendalam, grafik/tabel lengkap | Analisis baik, visualisasi cukup | Laporan basic | Tidak ada laporan |
| **Screenshot/Demo** | Video demo + screenshot lengkap | Screenshot hasil lengkap | Beberapa screenshot | Tidak ada bukti visual |

**Skor Maksimal: 12 poin × 0.833 = 10 poin**

---

### 5. Bonus Features (5%)

| Fitur Bonus | Poin |
|-------------|------|
| Bundle Adjustment implementation | +2 |
| Dense reconstruction | +2 |
| Mesh generation dari point cloud | +1 |
| Real-time processing | +2 |
| GUI interface | +1 |
| Color point cloud | +1 |
| Export ke format standar (PLY, OBJ) | +1 |

**Skor Maksimal: 5 poin (kelebihan tidak dihitung)**

---

## 📈 Konversi Nilai

| Range Skor | Nilai Huruf | Predikat |
|------------|-------------|----------|
| 85-100 | A | Sangat Baik |
| 75-84 | B+ | Baik Sekali |
| 70-74 | B | Baik |
| 65-69 | C+ | Cukup Baik |
| 55-64 | C | Cukup |
| 45-54 | D | Kurang |
| <45 | E | Sangat Kurang |

---

## ⚠️ Penalti

| Pelanggaran | Pengurangan |
|-------------|-------------|
| Terlambat mengumpulkan (per hari) | -5 poin |
| Plagiarisme kode (>50% similarity) | -50% total nilai |
| Program tidak bisa dijalankan | -20 poin |
| Tidak ada dokumentasi sama sekali | -10 poin |
| Tidak menggunakan gambar sendiri | -10 poin |

---

## 📝 Catatan Penilaian

1. **Penilaian dilakukan berdasarkan demonstrasi** - Program harus bisa dijalankan saat presentasi
2. **Originalitas sangat dihargai** - Pendekatan kreatif mendapat nilai tambah
3. **Proses juga dinilai** - Commit history di git menunjukkan progres pengerjaan
4. **Kolaborasi diperbolehkan** - Tapi setiap mahasiswa harus mengerjakan project sendiri
5. **Plagiarisme tidak ditoleransi** - Menggunakan kode orang lain tanpa atribusi = nilai E

---

## 🗓️ Jadwal Pengumpulan

- **Soft Deadline**: Minggu ke-3 (konsultasi dan feedback)
- **Hard Deadline**: Minggu ke-4 (pengumpulan final)
- **Presentasi/Demo**: Minggu ke-4/5 (sesuai jadwal)
