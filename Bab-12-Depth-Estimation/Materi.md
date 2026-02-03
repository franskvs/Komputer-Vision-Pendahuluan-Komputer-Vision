# BAB 12: DEPTH ESTIMATION (STEREO MATCHING)

## 🎯 Tujuan Pembelajaran

Setelah mempelajari materi ini, mahasiswa diharapkan mampu:
1. Memahami prinsip stereo vision untuk estimasi kedalaman (depth)
2. Mengimplementasikan berbagai algoritma stereo matching
3. Memahami konsep disparity dan hubungannya dengan depth
4. Menerapkan deep learning untuk monocular depth estimation

---

## 1. Definisi

### 1.1 Depth Estimation (Estimasi Kedalaman)

**Depth Estimation** adalah proses menghitung jarak (kedalaman) setiap piksel dalam gambar ke kamera. Ini adalah langkah fundamental untuk memahami struktur 3D scene.

**Metode Utama:**
- **Stereo Vision**: Menggunakan dua kamera (seperti mata manusia)
- **Structured Light**: Memproyeksikan pola cahaya (Kinect v1)
- **Time-of-Flight (ToF)**: Mengukur waktu pantulan cahaya
- **Monocular Depth**: Estimasi dari satu gambar menggunakan AI

### 1.2 Stereo Matching

**Stereo Matching** adalah proses menemukan korespondensi piksel antara gambar kiri dan kanan dari stereo camera. Perbedaan posisi horizontal (disparity) berbanding terbalik dengan kedalaman.

**Rumus Dasar:**
```
Depth (Z) = (Baseline × Focal Length) / Disparity

Z = (B × f) / d

dimana:
- Z = kedalaman (meter)
- B = baseline (jarak antar kamera)
- f = focal length (pixel)
- d = disparity (pixel)
```

### 1.3 Disparity Map

**Disparity Map** adalah gambar yang menyimpan nilai disparity untuk setiap piksel. Piksel dengan disparity besar berarti dekat, disparity kecil berarti jauh.

```
┌────────────────────────────────────────────────────────────────┐
│                     DISPARITY VS DEPTH                          │
│                                                                  │
│  High Disparity (terang)    ←→    Dekat ke Kamera              │
│  Low Disparity (gelap)      ←→    Jauh dari Kamera             │
│                                                                  │
│       GAMBAR ASLI              DISPARITY MAP                    │
│      ┌──────────┐              ┌──────────┐                     │
│      │   🚗    │              │ ██████   │  ← Object dekat     │
│      │         │              │ ████     │                      │
│      │ 🏔️      │              │ ░░       │  ← Object jauh      │
│      └──────────┘              └──────────┘                     │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. Konsep Utama

### 2.1 Pipeline Stereo Matching

```
┌─────────────────────────────────────────────────────────────────┐
│                  PIPELINE STEREO MATCHING                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Stereo   │───▶│ Image    │───▶│ Matching │───▶│ Disparity│  │
│  │ Rectify  │    │ Preproc  │    │ Cost     │    │ Compute  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
│       │               │               │               │          │
│       ▼               ▼               ▼               ▼          │
│   Epipolar        Grayscale/     SAD/SSD/NCC      Winner-Take  │
│   Lines Align     Normalize      Census/BT       -All/SGM      │
│                                                                  │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  Post-Processing  │                         │
│                    │  (Filtering, etc) │                         │
│                    └──────────────────┘                         │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │   Depth Map      │                         │
│                    └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Stereo Rectification

**Rectification** adalah proses transformasi gambar stereo sehingga:
- Epipolar lines menjadi horizontal
- Baris yang sama di kedua gambar mencari korespondensi yang sama
- Mempercepat pencarian matching (dari 2D ke 1D)

```
┌─────────────────────────────────────────────────────────────────┐
│                    STEREO RECTIFICATION                          │
│                                                                  │
│     SEBELUM RECTIFICATION          SETELAH RECTIFICATION        │
│                                                                  │
│     Kamera Kiri    Kamera Kanan    Kamera Kiri    Kamera Kanan  │
│     ┌────────┐     ┌────────┐      ┌────────┐     ┌────────┐   │
│     │  ●     │     │     ●  │      │  ●     │     │  ●     │   │
│     │   \    │     │    /   │      │────────│     │────────│   │
│     │    \   │     │   /    │      │  ●     │     │  ●     │   │
│     │     ●  │     │  ●     │      │────────│     │────────│   │
│     └────────┘     └────────┘      └────────┘     └────────┘   │
│                                                                  │
│     Epipolar lines miring         Epipolar lines horizontal     │
│     → Pencarian 2D                → Pencarian 1D (lebih cepat)  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Cost Functions untuk Matching

| Metode | Formula | Karakteristik |
|--------|---------|---------------|
| **SAD** (Sum of Absolute Differences) | Σ\|I₁(x,y) - I₂(x+d,y)\| | Sederhana, cepat |
| **SSD** (Sum of Squared Differences) | Σ(I₁(x,y) - I₂(x+d,y))² | Lebih sensitif terhadap outlier |
| **NCC** (Normalized Cross-Correlation) | Normalisasi korelasi | Robust terhadap pencahayaan |
| **Census** | Bit string comparison | Robust terhadap variasi illuminasi |

### 2.4 Algoritma Stereo Matching Populer

**1. Block Matching (BM)**
- Sederhana: bandingkan window/block piksel
- Cepat tapi kurang akurat di area homogen

**2. Semi-Global Matching (SGM)**
- Agregasi cost dari multiple directions
- Lebih smooth, mengurangi noise
- Balance antara akurasi dan kecepatan

**3. Graph Cuts / Belief Propagation**
- Optimasi global menggunakan MRF
- Sangat akurat tapi lambat

### 2.5 Monocular Depth Estimation

```
┌─────────────────────────────────────────────────────────────────┐
│             MONOCULAR DEPTH ESTIMATION (DEEP LEARNING)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│     ┌──────────────┐                                            │
│     │  RGB Image   │                                            │
│     │  (Single)    │                                            │
│     └──────┬───────┘                                            │
│            │                                                     │
│            ▼                                                     │
│     ┌──────────────┐                                            │
│     │   Encoder    │  ← ResNet, EfficientNet, ViT              │
│     │  (Features)  │                                            │
│     └──────┬───────┘                                            │
│            │                                                     │
│            ▼                                                     │
│     ┌──────────────┐                                            │
│     │   Decoder    │  ← Upsampling, Skip Connections           │
│     │  (Upsample)  │                                            │
│     └──────┬───────┘                                            │
│            │                                                     │
│            ▼                                                     │
│     ┌──────────────┐                                            │
│     │  Depth Map   │                                            │
│     └──────────────┘                                            │
│                                                                  │
│   Model Populer: MiDaS, DPT, AdaBins, DepthAnything            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Diagram dan Ilustrasi

### 3.1 Geometri Stereo Vision

```
                          Object Point (P)
                               ●
                              /│\
                             / │ \
                            /  │  \
                           /   │Z  \
                          /    │    \
                         /     │     \
                        /      │      \
            Kamera     /       │       \     Kamera
            Kiri      ●────────┼────────●    Kanan
                      │   B    │        │
                      │<------>│        │
                      │        │        │
                      │  xL    │    xR  │
                      
    Disparity (d) = xL - xR
    Depth (Z) = (B × f) / d
```

### 3.2 Perbandingan Hasil Algoritma

```
┌─────────────────────────────────────────────────────────────────┐
│           PERBANDINGAN ALGORITMA STEREO MATCHING                 │
│                                                                  │
│   Block Matching    Semi-Global (SGM)    Deep Learning          │
│   ┌────────────┐    ┌────────────┐       ┌────────────┐         │
│   │░░▓▓████░░░│    │░░▓▓████░░░│       │░░▓▓████░░░│         │
│   │░░▓▓████░░░│    │░░▓▓████░░░│       │░░▓▓████░░░│         │
│   │░░▓▓▓▓▓▓░░░│    │░░▓▓████░░░│       │░░▓▓████░░░│         │
│   │░░░░░░░░░░░│    │░░░░░░░░░░░│       │░░░░░░░░░░░│         │
│   └────────────┘    └────────────┘       └────────────┘         │
│        Noisy          Smoother            Best Quality          │
│      Fast (50ms)     Medium (200ms)      GPU Required           │
│                                                                  │
│   ★☆☆☆☆ Quality    ★★★☆☆ Quality       ★★★★★ Quality          │
│   ★★★★★ Speed      ★★★☆☆ Speed         ★★☆☆☆ Speed           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Contoh Kasus Industri dan Dunia Nyata

### 4.1 Self-Driving Cars

**Aplikasi:** Tesla Autopilot, Waymo, comma.ai

**Detail:**
- Stereo camera untuk depth estimation
- Mendeteksi jarak ke kendaraan lain, pejalan kaki, rambu
- Fusion dengan LIDAR dan radar untuk redundansi

```
Kamera Depan → Depth Estimation → Obstacle Detection → Path Planning
```

### 4.2 Robot Navigation

**Aplikasi:** Boston Dynamics Spot, warehouse robots

**Detail:**
- Stereo vision untuk obstacle avoidance
- Real-time depth untuk navigasi otonom
- Mapping lingkungan 3D

### 4.3 Augmented Reality

**Aplikasi:** Apple ARKit, Google ARCore, Meta Quest

**Detail:**
- Depth sensing untuk occlusion (objek virtual di belakang objek nyata)
- Surface detection untuk menempatkan objek AR
- Hand tracking menggunakan depth

### 4.4 Medical Imaging

**Aplikasi:** Surgical robots, 3D endoscopy

**Detail:**
- Stereo endoscope untuk operasi minimal invasif
- Depth estimation untuk panduan instrumen
- Rekonstruksi 3D organ internal

### 4.5 Smartphone Photography

**Aplikasi:** Portrait mode, bokeh effect

**Detail:**
- Dual camera atau ToF sensor untuk depth
- Segmentasi foreground/background
- Synthetic bokeh berdasarkan depth map

---

## 5. Ringkasan

```
┌─────────────────────────────────────────────────────────────────┐
│                         RINGKASAN                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📌 STEREO VISION                                               │
│     • Menggunakan dua kamera (baseline B)                       │
│     • Depth = (B × f) / disparity                               │
│     • Memerlukan rectification untuk efisiensi                  │
│     • Akurat untuk jarak dekat-menengah                         │
│                                                                  │
│  📌 STEREO MATCHING ALGORITHMS                                  │
│     • Block Matching (BM): Cepat, kurang akurat                 │
│     • Semi-Global Matching (SGM): Balance speed/accuracy        │
│     • Graph Cuts: Akurat tapi lambat                            │
│     • Deep Learning: State-of-the-art accuracy                  │
│                                                                  │
│  📌 MONOCULAR DEPTH                                             │
│     • Estimasi depth dari satu gambar                           │
│     • Berbasis deep learning (CNN, Transformer)                 │
│     • Tidak ada scale absolut (relative depth)                  │
│     • Model: MiDaS, DPT, DepthAnything                         │
│                                                                  │
│  📌 APLIKASI                                                    │
│     • Self-driving cars (obstacle detection)                    │
│     • AR/VR (occlusion, placement)                              │
│     • Robotics (navigation, manipulation)                       │
│     • Photography (portrait mode)                               │
│                                                                  │
│  📌 CHALLENGES                                                  │
│     • Occlusion (area tertutup)                                 │
│     • Textureless regions (sulit match)                         │
│     • Reflective/transparent surfaces                           │
│     • Real-time performance                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Deskripsi Tugas Video

### 📹 Tugas Video Pembelajaran: "Memahami Depth Estimation dan Stereo Matching"

**Durasi:** 15-20 menit

**Format:** Screen recording dengan narasi + face camera (picture-in-picture)

### Struktur Video yang Harus Dibuat:

#### **PEMBUKAAN (2-3 menit)**
- [ ] Perkenalan diri (nama, NIM, kelas)
- [ ] Judul materi: "Depth Estimation dan Stereo Matching"
- [ ] Tujuan pembelajaran yang akan dicapai
- [ ] Overview singkat tentang apa yang akan dibahas

#### **BAGIAN 1: Teori dan Konsep (5-7 menit)**
- [ ] Jelaskan apa itu depth estimation dan mengapa penting
- [ ] Jelaskan prinsip stereo vision dengan analogi mata manusia
- [ ] Gambarkan/tunjukkan rumus disparity-to-depth
- [ ] Jelaskan perbedaan Block Matching vs SGM
- [ ] Jelaskan konsep monocular depth estimation
- [ ] Berikan minimal 2 contoh aplikasi di dunia nyata

#### **BAGIAN 2: Demonstrasi Praktikum (7-10 menit)**
- [ ] Tunjukkan environment setup (library yang digunakan)
- [ ] Demo program stereo calibration (jika tersedia)
- [ ] Demo program stereo rectification
- [ ] Demo program stereo matching (BM dan SGM)
- [ ] Demo program monocular depth dengan MiDaS
- [ ] Bandingkan hasil berbagai metode
- [ ] Jelaskan setiap parameter penting dalam kode

#### **BAGIAN 3: Analisis dan Diskusi (2-3 menit)**
- [ ] Analisis kualitas depth map dari berbagai metode
- [ ] Diskusikan trade-off antara akurasi dan kecepatan
- [ ] Identifikasi area yang sulit (textureless, occlusion)
- [ ] Jelaskan limitasi dan kapan menggunakan metode tertentu

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
