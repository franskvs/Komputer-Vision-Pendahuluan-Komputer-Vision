# BAB 8: IMAGE STITCHING DAN PEMBUATAN PANORAMA

## 🎯 Tujuan Pembelajaran
Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami konsep dan algoritma image stitching
2. Mengimplementasikan pembuatan panorama dari multiple images
3. Menerapkan teknik blending untuk hasil yang seamless
4. Memahami transformasi perspektif dan warping

## 🌍 Aplikasi Dunia Nyata
- **Fotografi Panorama**: Smartphone membuat panorama 360°
- **Virtual Tour**: Real estate dan museum menggunakan foto panoramik
- **Satellite Imagery**: Menggabungkan foto satelit menjadi peta besar
- **Surveillance**: Menggabungkan view dari multiple CCTV
- **Medical Imaging**: Menggabungkan scan untuk visualisasi organ lengkap

---

## 1. DEFINISI

### 1.1 Apa itu Image Stitching?
**Image Stitching** adalah proses menggabungkan beberapa gambar yang memiliki area overlap menjadi satu gambar panorama yang lebih besar. Proses ini melibatkan:
- Deteksi fitur dan pencocokan antar gambar
- Estimasi transformasi geometris (homography)
- Warping gambar ke bidang proyeksi yang sama
- Blending untuk transisi yang mulus

### 1.2 Jenis-jenis Panorama
| Jenis | Deskripsi | Contoh Penggunaan |
|-------|-----------|-------------------|
| **Horizontal** | Gambar berjajar horizontal | Landscape photography |
| **Vertical** | Gambar berjajar vertikal | Foto gedung tinggi |
| **Cylindrical** | Proyeksi silinder 360° | Virtual tour |
| **Spherical** | Proyeksi bola penuh | VR/360° photo |

### 1.3 Komponen Utama Image Stitching
1. **Registration**: Menentukan transformasi antar gambar
2. **Warping**: Mentransformasi gambar ke koordinat bersama
3. **Blending**: Menggabungkan gambar dengan transisi halus
4. **Cropping**: Memotong area tidak valid

---

## 2. KONSEP UTAMA

### 2.1 Pipeline Image Stitching
```
Input Images → Feature Detection → Feature Matching → 
Homography Estimation → Warping → Blending → Panorama Output
```

### 2.2 Feature Detection dan Matching
Menggunakan algoritma dari Bab 7:
- **SIFT/ORB** untuk deteksi keypoint
- **FLANN/BF Matcher** untuk pencocokan fitur
- **RANSAC** untuk estimasi homography yang robust

### 2.3 Homography dan Warping
**Homography** adalah transformasi proyektif yang memetakan titik-titik dari satu gambar ke gambar lain.

**Warping** adalah proses mentransformasi gambar menggunakan homography:
```python
warped = cv2.warpPerspective(image, H, (width, height))
```

### 2.4 Teknik Blending

#### A. Direct Blending (No Blending)
- Gambar langsung ditumpuk
- Terlihat seam/garis batas yang jelas
- Paling cepat tapi kualitas buruk

#### B. Alpha Blending
- Menggunakan weighted average di area overlap
- `output = α * img1 + (1-α) * img2`
- Sederhana tapi bisa ghosting

#### C. Feather Blending
- Alpha berubah gradual dari 0 ke 1
- Transisi lebih halus
- Cocok untuk kebanyakan kasus

#### D. Multi-band Blending
- Memisahkan gambar ke berbagai frekuensi
- Blend low-frequency dan high-frequency terpisah
- Hasil paling bagus tapi lebih lambat

#### E. Laplacian Pyramid Blending
- Menggunakan Laplacian pyramid
- Excellent untuk perbedaan exposure
- Digunakan di software profesional

### 2.5 Cylindrical dan Spherical Projection

**Mengapa Diperlukan?**
- Untuk panorama > 180°, proyeksi planar tidak cukup
- Proyeksi silinder/bola menghindari distorsi besar

**Cylindrical Projection:**
```
x' = f * arctan(x/f)
y' = f * y / sqrt(x² + f²)
```
dimana f adalah focal length

### 2.6 Bundle Adjustment
- Optimisasi global untuk menyesuaikan semua homography
- Meminimalkan reprojection error
- Penting untuk panorama dengan banyak gambar

---

## 3. DIAGRAM DAN ILUSTRASI

### 3.1 Pipeline Image Stitching
```
┌─────────────────────────────────────────────────────────────────┐
│                    IMAGE STITCHING PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ Image 1 │     │ Image 2 │     │ Image 3 │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
         └───────────────┴───────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  FEATURE DETECTION  │
              │   (SIFT/ORB/AKAZE)  │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  FEATURE MATCHING   │
              │    + RATIO TEST     │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    HOMOGRAPHY       │
              │    ESTIMATION       │
              │    (RANSAC)         │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │      WARPING        │
              │  (Perspective/      │
              │   Cylindrical)      │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     BLENDING        │
              │ (Feather/Multiband) │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  PANORAMA OUTPUT    │
              └─────────────────────┘
```

### 3.2 Ilustrasi Blending Techniques
```
    No Blending          Feather Blending      Multi-band Blending
    
    ┌─────┬─────┐       ┌─────────────┐       ┌─────────────┐
    │  A  │  B  │       │ A  ░░░░  B  │       │ A   :::  B  │
    │     │     │       │    ░░░░     │       │     :::     │
    │─────│─────│       │    ░░░░     │       │     :::     │
    │  A  │  B  │       │ A  ░░░░  B  │       │ A   :::  B  │
    └─────┴─────┘       └─────────────┘       └─────────────┘
    
    Visible seam        Gradual blend         Seamless blend
```

### 3.3 Perbandingan Proyeksi
```
    Planar                Cylindrical           Spherical
    
    ┌───────────────┐    ╭───────────────╮     ╭─────────────╮
    │               │    │               │    ╱             ╲
    │   Max ~90°    │    │   Max ~360°   │   │   Full 360° │
    │               │    │               │    ╲             ╱
    └───────────────┘    ╰───────────────╯     ╰─────────────╯
```

---

## 4. CONTOH KASUS INDUSTRI DAN DUNIA NYATA

### 4.1 📱 Google Street View
**Skenario:** Google mengambil jutaan foto untuk Street View.

**Penerapan:**
- Kamera dengan 15 lensa untuk capture 360°
- Stitching otomatis menggunakan GPU cluster
- Multi-band blending untuk hasil seamless
- Bundle adjustment untuk akurasi posisi

**Hasil:** Coverage peta street-level di 87 negara

### 4.2 🏠 Real Estate Virtual Tour
**Skenario:** Agen properti membuat tour virtual rumah.

**Penerapan:**
- Foto panorama setiap ruangan
- Stitching menjadi 360° interactive view
- Web-based viewer dengan navigasi

**Hasil:** Leads dari virtual tour 87% lebih tinggi

### 4.3 🏥 Medical Imaging - Ophthalmology
**Skenario:** Dokter mata perlu melihat seluruh retina.

**Penerapan:**
- Multiple foto fundus dari sudut berbeda
- Stitching menjadi montage retina
- Analisis AI untuk deteksi penyakit

**Hasil:** Deteksi diabetic retinopathy lebih akurat

### 4.4 🛰️ Satellite Image Mosaicking
**Skenario:** Membuat peta dari foto satelit.

**Penerapan:**
- Ribuan foto satelit dengan overlap
- Geometric correction untuk Earth curvature
- Color balancing untuk konsistensi
- Mosaic menjadi peta kontinu

**Hasil:** Google Maps, Bing Maps, dll.

### 4.5 🎬 Film VFX - Set Extension
**Skenario:** Memperluas latar belakang studio.

**Penerapan:**
- Foto high-res dari lokasi nyata
- Stitching menjadi panorama HDRI
- Compositing dengan footage studio

**Hasil:** Background realistis dengan budget lebih rendah

---

## 5. RINGKASAN

### Poin-Poin Kunci:
1. **Image Stitching** menggabungkan gambar overlap menjadi panorama

2. **Pipeline** melibatkan: feature detection → matching → homography → warping → blending

3. **Homography** adalah transformasi proyektif untuk mapping antar gambar

4. **Blending** penting untuk hasil yang seamless:
   - Feather blending untuk kebanyakan kasus
   - Multi-band untuk perbedaan exposure

5. **Proyeksi** yang tepat diperlukan untuk panorama lebar:
   - Planar untuk < 90°
   - Cylindrical untuk 360° horizontal
   - Spherical untuk full 360°

### Tabel Pemilihan Teknik:
| Situasi | Rekomendasi |
|---------|-------------|
| 2-3 gambar sederhana | OpenCV Stitcher simple |
| Panorama horizontal | Cylindrical projection |
| Indoor 360° | Spherical projection |
| Perbedaan exposure | Multi-band blending |
| Real-time | ORB + direct blending |

### Formula Penting:
- **Homography**: p' = H * p
- **Feather blend**: output = α₁I₁ + α₂I₂, α₁ + α₂ = 1

---

## 6. DESKRIPSI TUGAS VIDEO

### 📹 Tugas: Membuat Video Pembelajaran Image Stitching

**Durasi:** 15-20 menit

**Format:** Screen recording dengan narasi

### Struktur Video yang Harus Dibuat:

#### A. PEMBUKAAN (2-3 menit)
1. ✅ Perkenalan diri (nama, NIM, kelas)
2. ✅ Judul materi: "Image Stitching dan Pembuatan Panorama"
3. ✅ Tujuan pembelajaran yang akan dicapai
4. ✅ Overview: apa itu panorama dan mengapa penting

#### B. PENJELASAN TEORI (5-6 menit)
1. ✅ Definisi image stitching
2. ✅ Komponen utama: registration, warping, blending
3. ✅ Jelaskan pipeline stitching dengan diagram
4. ✅ Jenis-jenis blending dan perbedaannya
5. ✅ Jelaskan kapan menggunakan proyeksi tertentu
6. ✅ Berikan contoh aplikasi dunia nyata

#### C. DEMO PRAKTIKUM (7-9 menit)
1. ✅ **Demo 1: Simple Stitching**
   - Tunjukkan 2 gambar dengan overlap
   - Jalankan program stitching
   - Tunjukkan hasil panorama

2. ✅ **Demo 2: OpenCV Stitcher**
   - Gunakan Stitcher class bawaan OpenCV
   - Bandingkan dengan manual implementation

3. ✅ **Demo 3: Blending Comparison**
   - Tunjukkan perbedaan no blending vs feather blending
   - Highlight seam yang terlihat

4. ✅ **Demo 4: Multi-image Panorama**
   - Gunakan 3+ gambar
   - Tunjukkan proses step by step

#### D. ANALISIS HASIL (2-3 menit)
1. ✅ Analisis kualitas stitching
2. ✅ Identifikasi masalah umum (ghosting, seam, parallax)
3. ✅ Diskusikan cara mengatasi masalah tersebut
4. ✅ Bandingkan berbagai teknik

#### E. PENUTUP (1-2 menit)
1. ✅ Kesimpulan materi
2. ✅ Tips untuk hasil panorama terbaik
3. ✅ Saran pengembangan: mencoba dengan gambar sendiri
4. ✅ Ucapan terima kasih

### Kriteria Penilaian Video:
| Aspek | Bobot |
|-------|-------|
| Kelengkapan materi | 25% |
| Kejelasan penjelasan | 25% |
| Demo praktikum berhasil | 25% |
| Kualitas video dan audio | 15% |
| Kreativitas dan insight | 10% |

### Tips untuk Demo yang Baik:
1. Siapkan foto sendiri dari smartphone (lebih relatable)
2. Ambil 3-5 foto dengan 30-50% overlap
3. Tunjukkan masalah umum dan solusinya
4. Bandingkan hasil dengan panorama smartphone
