# BAB 2: Pembentukan Citra (Image Formation)

## 🎯 Capaian Pembelajaran

Setelah menyelesaikan bab ini, mahasiswa diharapkan mampu:
1. Memahami prinsip dasar pembentukan citra digital
2. Menjelaskan model kamera pinhole dan proyeksi perspektif
3. Menerapkan transformasi geometri pada gambar
4. Memahami konsep kalibrasi kamera
5. Melakukan operasi transformasi perspektif

---

## 1️⃣ Definisi

### Apa itu Image Formation?

**Image Formation** (Pembentukan Citra) adalah proses di mana cahaya dari dunia nyata (3D) ditangkap dan dikonversi menjadi representasi 2D digital dalam bentuk gambar. Proses ini melibatkan:

1. **Cahaya** dari sumber (matahari, lampu) memantul dari objek
2. **Lensa** mengumpulkan dan memfokuskan cahaya
3. **Sensor** mengonversi cahaya menjadi sinyal digital
4. **Pemrosesan** mengubah sinyal menjadi nilai piksel

### Komponen Utama

```
Dunia 3D → Cahaya → Lensa → Sensor → Gambar Digital 2D
```

---

## 2️⃣ Konsep Utama

### A. Model Kamera Pinhole

Model paling sederhana untuk memahami pembentukan citra:

```
                    Titik di Dunia 3D (X, Y, Z)
                              |
                              | (cahaya)
                              ↓
    ══════════════════════════════════════════ Bidang Lensa
                              |
                              | (fokus f)
                              ↓
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Bidang Gambar
                         (x, y)
                    Proyeksi 2D
```

**Persamaan Proyeksi Pinhole:**
```
x = f × (X / Z)
y = f × (Y / Z)
```

Dimana:
- (X, Y, Z) = koordinat 3D di dunia nyata
- (x, y) = koordinat 2D pada gambar
- f = focal length (jarak fokus)

### B. Intrinsic Parameters (Parameter Internal Kamera)

Parameter yang menentukan karakteristik internal kamera:

| Parameter | Simbol | Deskripsi |
|-----------|--------|-----------|
| Focal Length | fx, fy | Jarak fokus dalam piksel |
| Principal Point | cx, cy | Titik pusat optik |
| Skew | s | Distorsi geser (biasanya 0) |

**Matrix Intrinsik (K):**
```
K = | fx  s   cx |
    | 0   fy  cy |
    | 0   0   1  |
```

### C. Extrinsic Parameters (Parameter Eksternal)

Parameter yang menentukan posisi dan orientasi kamera:

- **Rotasi (R)**: Matrix 3x3 menentukan arah kamera
- **Translasi (t)**: Vektor 3x1 menentukan posisi kamera

### D. Transformasi Geometri

#### 1. Translasi (Pergeseran)
```
x' = x + tx
y' = y + ty
```

#### 2. Rotasi (Pemutaran)
```
x' = x×cos(θ) - y×sin(θ)
y' = x×sin(θ) + y×cos(θ)
```

#### 3. Scaling (Penskalaan)
```
x' = sx × x
y' = sy × y
```

#### 4. Affine Transform
Kombinasi translasi, rotasi, scaling, dan shearing:
```
| x' |   | a  b  tx | | x |
| y' | = | c  d  ty | | y |
| 1  |   | 0  0  1  | | 1 |
```

#### 5. Perspective Transform
Transformasi yang mempertahankan garis lurus:
```
| x' |   | h00  h01  h02 | | x |
| y' | = | h10  h11  h12 | | y |
| w' |   | h20  h21  h22 | | 1 |

x_final = x' / w'
y_final = y' / w'
```

### E. Distorsi Lensa

Dua jenis distorsi utama:

1. **Radial Distortion**: Menyebabkan efek "barrel" atau "pincushion"
   - Barrel: Garis lurus melengkung ke luar
   - Pincushion: Garis lurus melengkung ke dalam

2. **Tangential Distortion**: Akibat lensa tidak sejajar dengan sensor

**Koreksi Distorsi:**
```
x_corrected = x(1 + k1×r² + k2×r⁴ + k3×r⁶) + ...
y_corrected = y(1 + k1×r² + k2×r⁴ + k3×r⁶) + ...
```

---

## 3️⃣ Diagram dan Ilustrasi

### Pipeline Pembentukan Citra

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE PEMBENTUKAN CITRA                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │  DUNIA   │    │  SISTEM  │    │  SENSOR  │    │  GAMBAR  │ │
│   │   3D     │───▶│  OPTIK   │───▶│  KAMERA  │───▶│   2D     │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │               │               │               │        │
│        │               │               │               │        │
│   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐   │
│   │Geometri │    │Proyeksi │    │Sampling │    │Digital  │   │
│   │Objek    │    │Perspektif│    │Kuantisasi│    │Image   │   │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Jenis-jenis Transformasi Geometri

```
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│   TRANSLASI    │   │    ROTASI      │   │    SCALING     │
│                │   │                │   │                │
│    □ → □       │   │    □           │   │    □    →  □   │
│        ↘       │   │     ↺         │   │              ↗  │
│         □      │   │       ◇       │   │               □ │
│                │   │                │   │               □ │
└────────────────┘   └────────────────┘   └────────────────┘

┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│    SHEARING    │   │    AFFINE      │   │  PERSPECTIVE   │
│                │   │                │   │                │
│    □           │   │    □           │   │    □           │
│    ▱           │   │      ◇        │   │      ⬡        │
│                │   │                │   │                │
└────────────────┘   └────────────────┘   └────────────────┘
```

---

## 4️⃣ Contoh Kasus di Industri

### 1. 🚗 Autonomous Vehicle - Tesla Autopilot

**Masalah**: Kamera kendaraan otonom perlu memahami jarak dan posisi objek di jalan.

**Solusi Image Formation**:
- Menggunakan multiple kamera dengan kalibrasi presisi
- Menggabungkan data dari berbagai sudut pandang
- Transformasi perspektif untuk bird's-eye view
- Estimasi kedalaman dari stereo vision

**Hasil**: Sistem dapat mendeteksi pedestrian, kendaraan, dan marka jalan dengan akurat.

### 2. 📱 Google Maps - Street View

**Masalah**: Membangun panorama 360° dari multiple kamera.

**Solusi Image Formation**:
- Kalibrasi presisi untuk array 15+ kamera
- Koreksi distorsi lensa fisheye
- Image stitching dengan homography
- Color correction dan blending

**Hasil**: Panorama seamless yang dapat dijelajahi secara virtual.

### 3. 🏭 Automated Optical Inspection (AOI)

**Masalah**: Inspeksi PCB untuk mendeteksi defect pada produksi elektronik.

**Solusi Image Formation**:
- Telecentric lens untuk menghilangkan distorsi perspektif
- Precise calibration untuk pengukuran akurat
- Multi-angle imaging untuk mendeteksi 3D defects
- Sub-pixel measurement accuracy

**Hasil**: Deteksi defect hingga 10 mikrometer.

### 4. 📸 Adobe Photoshop - Perspective Correction

**Masalah**: Foto bangunan seringkali memiliki garis yang tidak lurus (converging verticals).

**Solusi Image Formation**:
- Automatic perspective detection
- Homography estimation dari vanishing points
- Perspective transform untuk koreksi

**Hasil**: Foto arsitektur dengan garis vertikal yang lurus.

### 5. 🎮 Augmented Reality - Pokemon GO

**Masalah**: Menempatkan objek virtual pada dunia nyata.

**Solusi Image Formation**:
- Real-time camera pose estimation
- Plane detection untuk penempatan objek
- Perspective-correct rendering

**Hasil**: Pokemon yang tampak "ada" di dunia nyata melalui kamera smartphone.

---

## 5️⃣ Ringkasan

### Poin Penting yang Harus Diingat:

| Konsep | Deskripsi | Fungsi OpenCV |
|--------|-----------|---------------|
| Kamera Pinhole | Model dasar proyeksi 3D→2D | - |
| Intrinsic Matrix | Parameter internal kamera | `cv2.calibrateCamera()` |
| Extrinsic Matrix | Posisi & orientasi kamera | `cv2.solvePnP()` |
| Transformasi Affine | Kombinasi transformasi linear | `cv2.warpAffine()` |
| Transformasi Perspektif | Proyeksi antar bidang | `cv2.warpPerspective()` |
| Koreksi Distorsi | Menghilangkan distorsi lensa | `cv2.undistort()` |
| Homography | Mapping antar bidang | `cv2.findHomography()` |

### Flowchart Penggunaan:

```
┌─────────────────────────────────────────────────────────────┐
│              KAPAN MENGGUNAKAN TRANSFORMASI?                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Rotasi gambar? ────────────────▶ cv2.getRotationMatrix2D() │
│                                   cv2.warpAffine()           │
│                                                              │
│  Resize gambar? ────────────────▶ cv2.resize()              │
│                                                              │
│  Crop perspektif? ──────────────▶ cv2.getPerspectiveTransform()
│  (misal: dokumen)                 cv2.warpPerspective()     │
│                                                              │
│  Kalibrasi kamera? ─────────────▶ cv2.calibrateCamera()     │
│                                   cv2.undistort()            │
│                                                              │
│  Menggabungkan gambar? ─────────▶ cv2.findHomography()      │
│  (panorama)                       cv2.warpPerspective()     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6️⃣ Tugas Video

### 📹 Deskripsi Tugas Video

**Judul**: "Transformasi Geometri dan Kalibrasi Kamera dalam Computer Vision"

**Durasi**: 5-7 menit

**Format**: Tutorial/Demonstrasi dengan penjelasan

### Checklist Konten Video:

#### A. Pembukaan (30-60 detik)
- [ ] Perkenalan diri
- [ ] Menjelaskan topik yang akan dibahas
- [ ] Menyebutkan tujuan pembelajaran

#### B. Penjelasan Teori (1-2 menit)
- [ ] Menjelaskan apa itu Image Formation
- [ ] Membedakan transformasi Affine vs Perspektif
- [ ] Menjelaskan kapan menggunakan masing-masing

#### C. Demonstrasi Praktis (2-3 menit)
- [ ] Demo rotasi gambar dengan berbagai sudut
- [ ] Demo resize dengan interpolasi berbeda
- [ ] Demo perspective transform (contoh: document scanner)
- [ ] Menunjukkan kode dan hasilnya

#### D. Contoh Aplikasi Nyata (1 menit)
- [ ] Menjelaskan salah satu use case industri
- [ ] Menghubungkan dengan program yang dibuat

#### E. Penutup (30-60 detik)
- [ ] Ringkasan poin penting
- [ ] Saran untuk eksplorasi lebih lanjut
- [ ] Call-to-action (coba sendiri!)

### Poin Penilaian Video:

| Aspek | Bobot | Deskripsi |
|-------|-------|-----------|
| Kejelasan Penjelasan | 25% | Mudah dipahami, tidak membingungkan |
| Kebenaran Materi | 25% | Informasi akurat dan relevan |
| Kualitas Demonstrasi | 25% | Kode berjalan, hasil ditunjukkan |
| Kualitas Produksi | 15% | Audio jelas, video tidak blur |
| Kreativitas | 10% | Contoh menarik, penyampaian engaging |

### Tips Membuat Video:

1. **Persiapan**: Test semua kode sebelum merekam
2. **Rekam layar**: Gunakan OBS Studio atau Loom
3. **Narasi**: Jelaskan apa yang sedang dilakukan
4. **Edit**: Potong bagian yang tidak perlu
5. **Review**: Tonton ulang sebelum submit

---

## 📚 Referensi

1. Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Edition. Chapter 2.
2. Hartley, R. & Zisserman, A. (2003). Multiple View Geometry in Computer Vision.
3. OpenCV Documentation: Camera Calibration and 3D Reconstruction
4. Zhang, Z. (2000). A Flexible New Technique for Camera Calibration.

---

*Bab ini adalah bagian dari Praktikum Computer Vision berdasarkan buku "Computer Vision: Algorithms and Applications" oleh Richard Szeliski.*
