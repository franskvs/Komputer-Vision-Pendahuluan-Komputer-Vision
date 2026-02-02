# BAB 1: PENDAHULUAN COMPUTER VISION

## 🎯 Tujuan Pembelajaran

Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Menjelaskan definisi dan ruang lingkup computer vision
2. Memahami sejarah perkembangan computer vision
3. Mengetahui berbagai aplikasi computer vision di dunia nyata
4. Memahami pendekatan-pendekatan dalam menyelesaikan masalah computer vision

---

## 1.1 Apa Itu Computer Vision?

### Definisi
**Computer Vision** adalah bidang ilmu yang mempelajari bagaimana membuat komputer dapat "melihat" dan memahami konten visual dari gambar atau video digital. Tujuan utamanya adalah mengekstrak informasi bermakna dari data visual secara otomatis.

### Perbandingan dengan Penglihatan Manusia
Sebagai manusia, kita dapat dengan mudah:
- Mengenali objek dan wajah dalam sekejap
- Memahami struktur 3D dari pemandangan 2D
- Membedakan objek dari latar belakang
- Memperkirakan jarak dan ukuran objek

Kemampuan yang tampak sederhana ini ternyata **sangat sulit** untuk direplikasi pada komputer!

### Mengapa Computer Vision Sulit?

1. **Masalah Invers (Inverse Problem)**
   - Kita berusaha merekonstruksi dunia 3D dari proyeksi 2D
   - Informasi kedalaman hilang saat proyeksi
   - Banyak kemungkinan solusi untuk satu citra

2. **Variasi dalam Data**
   - Perubahan pencahayaan
   - Sudut pandang berbeda
   - Oklusi (sebagian objek tertutup)
   - Deformasi objek

3. **Kompleksitas Dunia Nyata**
   - Variasi tak terbatas dalam bentuk, warna, tekstur
   - Noise dan distorsi pada citra

---

## 1.2 Sejarah Singkat Computer Vision

### Era 1960-an: Awal Mula
- **1966**: Marvin Minsky di MIT meminta mahasiswanya untuk "menghubungkan kamera ke komputer dan membuat komputer mendeskripsikan apa yang dilihatnya" sebagai proyek musim panas
- Asumsi awal: vision adalah masalah yang mudah dibandingkan logika dan perencanaan
- Kenyataan: masalah vision jauh lebih kompleks!

### Era 1970-an: Fondasi
- **Blocks World**: Analisis pemandangan sederhana berisi balok-balok geometris
- **Generalized Cylinders**: Representasi objek menggunakan silinder umum
- Pengembangan algoritma deteksi tepi awal

### Era 1980-an: Pendekatan Ilmiah
- **David Marr** (1982): Kerangka komputasional untuk vision
  - Level Komputasi: Apa yang dihitung?
  - Level Algoritma: Bagaimana menghitungnya?
  - Level Implementasi: Bagaimana diimplementasikan di hardware?
- Pengembangan **stereo vision** dan **optical flow**
- **Shape from X**: shape from shading, texture, focus

### Era 1990-an: Pendekatan Statistik
- Penggunaan **probabilitas** dan **machine learning**
- **Eigenfaces** untuk pengenalan wajah (1991)
- Algoritma **RANSAC** untuk robust fitting
- Pengembangan **Scale-Invariant Feature Transform (SIFT)**

### Era 2000-an: Feature-Based Methods
- **SIFT** (2004): Detektor dan deskriptor fitur yang robust
- **Histogram of Oriented Gradients (HOG)** untuk deteksi objek
- **Bag of Words** untuk klasifikasi citra

### Era 2010-an - Sekarang: Era Deep Learning
- **2012**: AlexNet memenangkan ImageNet dengan margin besar
- **CNN (Convolutional Neural Networks)** mendominasi
- Kemajuan dramatis dalam:
  - Klasifikasi citra
  - Deteksi objek
  - Segmentasi semantik
  - Generative models (GANs)

---

## 1.3 Aplikasi Computer Vision

### Aplikasi Industri

| Bidang | Aplikasi | Deskripsi |
|--------|----------|-----------|
| **OCR** | Membaca kode pos | Otomatisasi sortir surat |
| **Inspeksi** | Quality control | Mendeteksi cacat produksi |
| **Retail** | Automated checkout | Pengenalan produk tanpa barcode |
| **Logistik** | Warehouse robots | Navigasi dan picking barang |
| **Medis** | Medical imaging | Analisis CT scan, MRI |
| **Otomotif** | Self-driving cars | Persepsi lingkungan |

### Aplikasi Konsumer

1. **Image Stitching**: Membuat panorama dari beberapa foto
2. **Face Detection/Recognition**: Membuka kunci smartphone, tag foto
3. **Augmented Reality**: Filter Instagram/Snapchat
4. **Photo Enhancement**: Auto-enhance, HDR
5. **3D Reconstruction**: Membuat model 3D dari foto

### Contoh Aplikasi Nyata

```
┌─────────────────────────────────────────────────────────┐
│                    SELF-DRIVING CAR                      │
├─────────────────────────────────────────────────────────┤
│  Input: Kamera, LiDAR, Radar                            │
│  ↓                                                       │
│  [Object Detection] → Mobil, pejalan kaki, rambu        │
│  [Lane Detection] → Batas jalur                         │
│  [Depth Estimation] → Jarak ke objek                    │
│  ↓                                                       │
│  Output: Keputusan mengemudi                            │
└─────────────────────────────────────────────────────────┘
```

---

## 1.4 Pendekatan dalam Computer Vision

### 1. Pendekatan Ilmiah (Scientific)
- Membangun model matematis dari proses pembentukan citra
- Mengembangkan teknik untuk membalikkan proses tersebut
- Contoh: Model kamera pinhole, persamaan reflectance

### 2. Pendekatan Statistik (Statistical)
- Menggunakan model probabilistik
- Memodelkan prior distribution dari unknowns
- Melakukan inferensi Bayesian
- Contoh: MAP estimation, MRF

### 3. Pendekatan Engineering
- Fokus pada solusi yang bekerja dalam praktik
- Evaluasi performa pada data nyata
- Trade-off antara akurasi dan efisiensi

### 4. Pendekatan Data-Driven
- Mengumpulkan dataset besar
- Melatih model dari data
- Evaluasi dan validasi performa
- Contoh: Deep Learning

### Filosofi Pengujian Algoritma

```
┌─────────────────────────────────────────────────────────┐
│              STRATEGI PENGUJIAN 3 BAGIAN                 │
├─────────────────────────────────────────────────────────┤
│  1. Data Sintetis Bersih                                │
│     → Verifikasi kebenaran algoritma                    │
│     → Ground truth diketahui persis                     │
│                                                          │
│  2. Data Sintetis + Noise                               │
│     → Evaluasi degradasi performa                       │
│     → Analisis sensitivitas terhadap noise              │
│                                                          │
│  3. Data Dunia Nyata                                    │
│     → Tes pada kondisi sesungguhnya                     │
│     → Berbagai sumber (foto web, video, dll)            │
└─────────────────────────────────────────────────────────┘
```

---

## 1.5 Gambaran Umum Buku

### Struktur Materi

1. **Bab 2-3**: Fondasi (Pembentukan Citra, Pemrosesan Citra)
2. **Bab 4**: Optimisasi dan Model Fitting
3. **Bab 5-6**: Machine Learning dan Recognition
4. **Bab 7**: Deteksi dan Matching Fitur
5. **Bab 8-9**: Alignment dan Motion
6. **Bab 10**: Computational Photography
7. **Bab 11-12**: 3D Reconstruction dan Depth
8. **Bab 13-14**: 3D Modeling dan Rendering

### Prasyarat

- **Matematika**: Aljabar linear, kalkulus, probabilitas
- **Pemrograman**: Python, NumPy, library image processing
- **Dasar**: Image processing atau computer graphics

---

## 1.6 Notasi Matematika

### Vektor dan Matriks
- **Vektor**: huruf kecil tebal, misal **x**, **p**
- **Matriks**: huruf kapital, misal **A**, **R**
- **Skalar**: huruf biasa, misal *x*, *y*

### Koordinat
- **Koordinat citra**: (u, v) atau (x, y)
- **Koordinat 3D**: (X, Y, Z)
- **Koordinat homogen**: menambah dimensi 1

### Transformasi
- **R**: Matriks rotasi
- **t**: Vektor translasi
- **K**: Matriks intrinsik kamera
- **P**: Matriks proyeksi

---

## Ringkasan

| Konsep | Poin Utama |
|--------|------------|
| Definisi | Computer vision = membuat komputer "melihat" dan memahami citra |
| Kesulitan | Masalah invers, variasi data, kompleksitas dunia nyata |
| Sejarah | Dari blocks world (1960s) hingga deep learning (2010s+) |
| Pendekatan | Scientific, Statistical, Engineering, Data-driven |
| Aplikasi | Self-driving, medis, AR, pengenalan wajah, dll |

---

## Pertanyaan Diskusi

1. Mengapa penglihatan manusia jauh lebih baik daripada computer vision untuk banyak tugas?
2. Apa keuntungan dan kerugian pendekatan deep learning dibandingkan metode tradisional?
3. Sebutkan 3 aplikasi computer vision yang paling berdampak menurut Anda dan jelaskan alasannya!

---

## Referensi Bab Ini

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, Chapter 1
2. Marr, D. (1982). Vision: A Computational Investigation
3. LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444.
