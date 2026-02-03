# BAB 11: STRUCTURE FROM MOTION DAN SLAM

## 🎯 Tujuan Pembelajaran

Setelah mempelajari materi ini, mahasiswa diharapkan mampu:
1. Memahami konsep Structure from Motion (SfM) untuk rekonstruksi 3D dari gambar 2D
2. Mengimplementasikan estimasi pose kamera dan triangulasi titik 3D
3. Memahami dan menerapkan Visual SLAM (Simultaneous Localization and Mapping)
4. Menerapkan Bundle Adjustment untuk optimasi rekonstruksi 3D

---

## 1. Definisi

### 1.1 Structure from Motion (SfM)

**Structure from Motion (SfM)** adalah teknik dalam computer vision untuk merekonstruksi struktur 3D dari serangkaian gambar 2D yang diambil dari berbagai sudut pandang. SfM bekerja dengan cara:
- Mendeteksi dan mencocokkan fitur antar gambar
- Mengestimasi pose kamera (posisi dan orientasi)
- Melakukan triangulasi untuk menghitung posisi 3D titik-titik di dunia nyata

**Analogi Sederhana:** Bayangkan Anda mengambil banyak foto sebuah patung dari berbagai sudut. SfM adalah proses komputer yang dapat "merekonstruksi" bentuk 3D patung tersebut hanya dari foto-foto 2D yang Anda ambil.

### 1.2 SLAM (Simultaneous Localization and Mapping)

**SLAM** adalah teknik untuk membangun peta lingkungan sekaligus melacak posisi agen (robot/kamera) secara bersamaan dalam waktu nyata. Visual SLAM menggunakan kamera sebagai sensor utama.

**Perbedaan SfM dan SLAM:**
| Aspek | SfM | SLAM |
|-------|-----|------|
| Mode | Offline (batch processing) | Online (real-time) |
| Fokus | Rekonstruksi 3D | Lokalisasi + Mapping |
| Data | Koleksi gambar | Stream video |
| Aplikasi | Fotogrametri, Film | Robot, AR/VR |

---

## 2. Konsep Utama

### 2.1 Pipeline Structure from Motion

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PIPELINE STRUCTURE FROM MOTION                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Feature  │───▶│ Feature  │───▶│ Camera   │───▶│  Point   │      │
│  │Detection │    │ Matching │    │Pose Est. │    │Triangul. │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │               │               │               │              │
│       ▼               ▼               ▼               ▼              │
│   SIFT/ORB      Brute-Force/    Essential/     DLT/Midpoint        │
│   SURF/AKAZE    FLANN           Fundamental                        │
│                                                                      │
│                              │                                       │
│                              ▼                                       │
│                    ┌──────────────────┐                             │
│                    │ Bundle Adjustment │                             │
│                    │  (Optimization)   │                             │
│                    └──────────────────┘                             │
│                              │                                       │
│                              ▼                                       │
│                    ┌──────────────────┐                             │
│                    │  Dense 3D Point  │                             │
│                    │      Cloud       │                             │
│                    └──────────────────┘                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Essential Matrix dan Fundamental Matrix

**Fundamental Matrix (F):**
- Menghubungkan titik korespondensi antara dua gambar
- Persamaan epipolar: `x'ᵀ F x = 0`
- Tidak memerlukan kalibrasi kamera

**Essential Matrix (E):**
- Versi "terkalibrasi" dari Fundamental Matrix
- `E = K'ᵀ F K` (K = matriks intrinsik kamera)
- Dapat didekomposisi menjadi Rotasi (R) dan Translasi (t)

```
┌─────────────────────────────────────────────────────────────┐
│                    EPIPOLAR GEOMETRY                         │
│                                                              │
│         Kamera 1 (C1)              Kamera 2 (C2)            │
│              ●                          ●                    │
│             /│\                        /│\                   │
│            / │ \                      / │ \                  │
│           /  │  \                    /  │  \                 │
│          /   │   \                  /   │   \                │
│         /    │    \                /    │    \               │
│        /     │     \              /     │     \              │
│       ●──────●──────●            ●──────●──────●             │
│     Image    │    Epipolar      Epipolar │   Image          │
│     Plane    │     Line          Line    │   Plane          │
│              │                           │                   │
│              └───────────────────────────┘                   │
│                     Epipolar Plane                           │
│                          │                                   │
│                          ● P (3D Point)                      │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Triangulasi

Triangulasi adalah proses menghitung posisi 3D titik dari proyeksi 2D-nya di beberapa gambar.

**Metode Triangulasi:**
1. **Direct Linear Transform (DLT):** Memecahkan sistem linear Ax = 0
2. **Midpoint Method:** Mencari titik tengah antara dua ray
3. **Optimal Triangulation:** Minimisasi error reprojeksi

### 2.4 Bundle Adjustment

**Bundle Adjustment** adalah optimasi non-linear untuk menyempurnakan:
- Posisi 3D titik-titik
- Pose kamera (rotasi dan translasi)
- Parameter intrinsik kamera

```
Minimize: Σᵢ Σⱼ ||xᵢⱼ - π(Pⱼ, Xᵢ)||²

dimana:
- xᵢⱼ = titik 2D terukur
- π = fungsi proyeksi
- Pⱼ = parameter kamera j
- Xᵢ = koordinat 3D titik i
```

### 2.5 Visual SLAM

```
┌─────────────────────────────────────────────────────────────────┐
│                     VISUAL SLAM PIPELINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                                               │
│   │ Camera      │                                               │
│   │ Input       │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│          ▼                                                       │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│   │  Tracking   │────▶│   Mapping   │────▶│   Loop      │      │
│   │             │◀────│             │◀────│  Closure    │      │
│   └─────────────┘     └─────────────┘     └─────────────┘      │
│         │                    │                   │               │
│         ▼                    ▼                   ▼               │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│   │ Camera Pose │     │  3D Map     │     │ Drift       │      │
│   │ Estimation  │     │  Points     │     │ Correction  │      │
│   └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                  │
│   Frontend (Real-time)           Backend (Optimization)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Diagram dan Ilustrasi

### 3.1 Proses Rekonstruksi 3D dari Multiple Views

```
        Gambar 1          Gambar 2          Gambar 3
     ┌───────────┐     ┌───────────┐     ┌───────────┐
     │   📷      │     │    📷     │     │     📷    │
     │  ┌───┐    │     │  ┌───┐    │     │  ┌───┐    │
     │  │🏠 │    │     │  │🏠 │    │     │  │🏠 │    │
     │  └───┘    │     │  └───┘    │     │  └───┘    │
     └───────────┘     └───────────┘     └───────────┘
           │                 │                 │
           └────────────────┬┴─────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  Feature Detection &    │
              │  Matching               │
              └───────────┬─────────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │  Camera Pose            │
              │  Estimation             │
              └───────────┬─────────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │  Triangulation &        │
              │  3D Reconstruction      │
              └───────────┬─────────────┘
                          │
                          ▼
                    ┌───────────┐
                    │   🏠 3D   │
                    │  Model    │
                    └───────────┘
```

### 3.2 Keyframe Selection dalam SLAM

```
┌─────────────────────────────────────────────────────────────┐
│                   KEYFRAME SELECTION                         │
│                                                              │
│  Frame 1    Frame 2    Frame 3    Frame 4    Frame 5        │
│     ★          ○          ○          ★          ○           │
│   [Key]      [Skip]    [Skip]     [Key]      [Skip]         │
│                                                              │
│  Kriteria Keyframe:                                          │
│  ✓ Pergerakan signifikan                                    │
│  ✓ Jumlah fitur baru cukup                                  │
│  ✓ Overlap yang cukup dengan keyframe sebelumnya            │
│  ✓ Tidak terlalu dekat dengan keyframe sebelumnya           │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Contoh Kasus Industri dan Dunia Nyata

### 4.1 Fotogrametri untuk Survei dan Pemetaan

**Aplikasi:** DJI Terra, Pix4D, Agisoft Metashape

**Kasus:** Perusahaan konstruksi menggunakan drone untuk memotret lokasi proyek dari udara. Software SfM memproses ratusan foto menjadi:
- Peta ortofoto resolusi tinggi
- Model 3D terrain
- Pengukuran volume tanah yang akurat

```
Input: 500+ foto drone → SfM → Output: Peta 3D akurat (cm precision)
```

### 4.2 Film dan Visual Effects

**Aplikasi:** Match-moving untuk CGI integration

**Kasus:** Dalam pembuatan film superhero, kamera tracking menggunakan SfM untuk:
- Merekonstruksi gerakan kamera
- Menentukan posisi 3D di set
- Menyisipkan karakter CGI dengan perspektif yang benar

### 4.3 Augmented Reality (AR)

**Aplikasi:** ARCore (Google), ARKit (Apple)

**Kasus:** Aplikasi IKEA Place menggunakan Visual SLAM untuk:
- Mendeteksi permukaan lantai
- Melacak posisi perangkat
- Menempatkan furniture virtual dengan akurat

### 4.4 Robot Navigasi Otonom

**Aplikasi:** Robot vacuum (Roomba i7+), Self-driving cars

**Kasus:** Robot vacuum menggunakan SLAM untuk:
- Memetakan layout rumah
- Menghindari hambatan
- Merencanakan jalur pembersihan efisien

### 4.5 Preservasi Warisan Budaya

**Aplikasi:** Digitalisasi museum dan situs arkeologi

**Kasus:** Tim arkeolog menggunakan SfM untuk membuat replika digital dari artefak kuno yang rapuh, memungkinkan studi tanpa menyentuh objek asli.

---

## 5. Ringkasan

```
┌─────────────────────────────────────────────────────────────────┐
│                         RINGKASAN                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📌 STRUCTURE FROM MOTION (SfM)                                 │
│     • Rekonstruksi 3D dari gambar 2D multiple views             │
│     • Pipeline: Detection → Matching → Pose → Triangulation     │
│     • Optimasi dengan Bundle Adjustment                          │
│     • Aplikasi: Fotogrametri, Film VFX, Arsitektur              │
│                                                                  │
│  📌 EPIPOLAR GEOMETRY                                           │
│     • Fundamental Matrix: Tanpa kalibrasi                       │
│     • Essential Matrix: Dengan kalibrasi                        │
│     • Digunakan untuk estimasi pose kamera                      │
│                                                                  │
│  📌 VISUAL SLAM                                                 │
│     • Real-time localization + mapping                          │
│     • Frontend: Tracking                                        │
│     • Backend: Optimization                                      │
│     • Loop Closure: Koreksi drift                               │
│     • Aplikasi: Robot, AR/VR, Self-driving                      │
│                                                                  │
│  📌 KEY CONCEPTS                                                │
│     • Triangulasi: 2D → 3D dari multiple views                  │
│     • Bundle Adjustment: Optimasi global                        │
│     • Keyframe: Frame penting untuk mapping                     │
│     • Point Cloud: Hasil rekonstruksi 3D                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Deskripsi Tugas Video

### 📹 Tugas Video Pembelajaran: "Memahami Structure from Motion dan SLAM"

**Durasi:** 15-20 menit

**Format:** Screen recording dengan narasi + face camera (picture-in-picture)

### Struktur Video yang Harus Dibuat:

#### **PEMBUKAAN (2-3 menit)**
- [ ] Perkenalan diri (nama, NIM, kelas)
- [ ] Judul materi: "Structure from Motion dan SLAM"
- [ ] Tujuan pembelajaran yang akan dicapai
- [ ] Overview singkat tentang apa yang akan dibahas

#### **BAGIAN 1: Teori dan Konsep (5-7 menit)**
- [ ] Jelaskan definisi Structure from Motion dengan bahasa sendiri
- [ ] Jelaskan perbedaan SfM dan SLAM
- [ ] Gambarkan/tunjukkan diagram pipeline SfM
- [ ] Jelaskan konsep epipolar geometry (gunakan ilustrasi)
- [ ] Jelaskan proses triangulasi secara sederhana
- [ ] Berikan minimal 2 contoh aplikasi di dunia nyata

#### **BAGIAN 2: Demonstrasi Praktikum (7-10 menit)**
- [ ] Tunjukkan environment setup (library yang digunakan)
- [ ] Demo program feature matching antar gambar
- [ ] Demo program estimasi Essential/Fundamental Matrix
- [ ] Demo program triangulasi titik 3D
- [ ] Demo program visual odometry sederhana
- [ ] Jelaskan setiap parameter penting dalam kode
- [ ] Tunjukkan dan jelaskan hasil output (visualisasi 3D)

#### **BAGIAN 3: Analisis dan Diskusi (2-3 menit)**
- [ ] Analisis hasil eksperimen
- [ ] Bandingkan hasil dengan variasi parameter berbeda
- [ ] Diskusikan tantangan/limitasi yang ditemukan
- [ ] Jelaskan bagaimana teknik ini diterapkan di industri

#### **PENUTUP (1-2 menit)**
- [ ] Rangkuman poin-poin penting
- [ ] Kesimpulan pembelajaran
- [ ] Refleksi: Apa yang telah dipelajari
- [ ] Saran untuk pengembangan lebih lanjut

### Kriteria Penilaian Video:
| Aspek | Poin |
|-------|------|
| Kejelasan penjelasan konsep | 25 |
| Demonstrasi program berjalan | 25 |
| Analisis hasil | 20 |
| Kualitas presentasi | 15 |
| Kreativitas dan insight | 15 |
| **Total** | **100** |

### Tips Membuat Video yang Baik:
1. Gunakan mikrofon yang jelas
2. Pastikan layar terlihat dengan baik (resolusi minimal 720p)
3. Bicara dengan tempo yang tidak terlalu cepat
4. Gunakan highlight/annotation untuk menunjukkan bagian penting
5. Latihan sebelum merekam untuk mengurangi kesalahan
