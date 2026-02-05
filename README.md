# Praktikum Computer Vision

> Kurikulum praktikum berbasis buku **Computer Vision: Algorithms and Applications (2nd ed.)** oleh Richard Szeliski. Repo ini berisi 14 modul pembelajaran lengkap dengan teori, jobsheet, project, rubrik, dan program praktikum yang sudah diverifikasi pada banyak bab.

---

## ✨ Highlight

- ✅ **14 modul lengkap** dari dasar hingga 3D reconstruction & image-based rendering
- ✅ **Materi + Jobsheet + Project + Referensi** di setiap modul
- ✅ **Program praktikum nyata** dengan output visual dan contoh aplikasi industri
- ✅ **Auto-close & test reports** tersedia pada banyak modul yang sudah diverifikasi
- ✅ **Satu paket dependensi** via requirements

---

## 📚 Daftar Modul (Ringkas)

| Modul | Topik Utama | Ringkas Isi |
|---|---|---|
| 01 | Pendahuluan Komputer Vision | konsep dasar, pipeline, pengantar tools |
| 02 | Pembentukan Citra | kamera, pembentukan citra, representasi |
| 03 | Pemrosesan Citra | filtering, Fourier, wavelet, transformasi geometrik |
| 04 | Model Fitting | fitting model & estimasi parameter |
| 05 | Deep Learning | CNN, transfer learning, YOLO, segmentasi |
| 06 | Recognition | pengenalan objek/wajah & evaluasi |
| 07 | Deteksi Fitur & Pencocokan | SIFT/ORB/AKAZE/FAST, matching, homography |
| 08 | Image Stitching | panorama, blending, cylindrical projection |
| 09 | Motion Estimation | optical flow & motion analysis |
| 10 | Computational Photography | HDR, denoising, bokeh, enhancement |
| 11 | Structure from Motion & SLAM | F/E matrix, triangulasi, VO, BA, SLAM |
| 12 | Depth Estimation | stereo & depth pipeline |
| 13 | 3D Reconstruction | point cloud, ICP, Poisson, mesh processing |
| 14 | Image-Based Rendering | warping, view synthesis, MPI, NeRF concepts |

---

## 🧭 Struktur Repo (Pola Umum)

Setiap modul biasanya memiliki struktur seperti ini:

```
Modul-XX-<Nama> /
├── Jobsheet.md
├── Materi.md
├── Project.md
├── Referensi.md
├── Rubrik_Penilaian_*.md
└── praktikum/
    ├── *.py
    ├── data/ (jika ada)
    └── output/ (jika ada)
```

Contoh modul dengan dokumentasi ekstensif:
- Modul 05 (Deep Learning) memiliki panduan cepat, jobsheet terperinci, dan laporan verifikasi.
- Modul 08 (Image Stitching) memiliki ringkasan kerja, auto-close, dan skrip run-all.
- Modul 11, 13, 14 memiliki ringkasan verifikasi lengkap dan struktur output yang rapi.

---

## ✅ Dokumen Penting (Entry Points)

- [requirements.txt](requirements.txt) — daftar dependency utama
- Modul dengan ringkasan/verification report yang kuat:
  - [Modul-07-Deteksi-Fitur-dan-Pencocokan/FINAL_COMPLETION_REPORT.md](Modul-07-Deteksi-Fitur-dan-Pencocokan/FINAL_COMPLETION_REPORT.md)
  - [Modul-08-Image-Stitching/SUMMARY.md](Modul-08-Image-Stitching/SUMMARY.md)
  - [Modul-10-Computational-Photography/SUMMARY.md](Modul-10-Computational-Photography/SUMMARY.md)
  - [Modul-11-Structure-from-Motion/SUMMARY.md](Modul-11-Structure-from-Motion/SUMMARY.md)
  - [Modul-13-3D-Reconstruction/COMPLETION_SUMMARY.md](Modul-13-3D-Reconstruction/COMPLETION_SUMMARY.md)
  - [Modul-14-Image-Based-Rendering/COMPLETION_SUMMARY.md](Modul-14-Image-Based-Rendering/COMPLETION_SUMMARY.md)

---

## ⚙️ Instalasi Singkat

1. Pastikan Python 3.8+ tersedia.
2. Install dependency dari [requirements.txt](requirements.txt).
3. Masuk ke folder modul yang diinginkan dan ikuti Jobsheet.

---

## ▶️ Cara Belajar yang Disarankan

1. **Baca Materi.md** untuk teori.
2. **Ikuti Jobsheet.md** untuk langkah praktikum.
3. **Jalankan program di praktikum/** dan amati output.
4. **Kerjakan Project.md** untuk integrasi konsep.

---

## 🧪 Verifikasi & Output

Beberapa modul memiliki skrip verifikasi dan laporan hasil (contoh modul 05, 08, 10, 11, 13, 14). Gunakan laporan tersebut untuk memastikan seluruh program berhasil dan output tersimpan pada folder output.

---

## 🎓 Target Pembelajaran

Repo ini dirancang agar mahasiswa mampu:
- Memahami konsep inti computer vision (citra, fitur, transformasi)
- Mengimplementasikan algoritma klasik (filtering, matching, stitching)
- Menerapkan deep learning untuk visi komputer
- Membangun pipeline 3D (SfM, depth, reconstruction, IBR)

---

## 📌 Catatan Penting

- Beberapa modul menyediakan sample data dan skrip download.
- Beberapa program menggunakan auto-close agar mudah di-run otomatis.
- Untuk modul 3D (mis. 13), sebagian eksperimen bersifat komputasional berat.

---

## 📖 Referensi Utama

- **Computer Vision: Algorithms and Applications (2nd ed.) — Richard Szeliski**

---

## 🙌 Kontribusi

Kontribusi sangat terbuka untuk perbaikan materi, program, atau dokumentasi. Silakan tambah modul atau perbaiki program yang belum terverifikasi.

---

**Status Repo:** Aktif dan terus disempurnakan per modul.
