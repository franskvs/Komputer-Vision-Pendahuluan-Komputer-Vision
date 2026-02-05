# BAB 9: MOTION ESTIMATION

## 🎯 Tujuan Pembelajaran
Setelah mempelajari bab ini, mahasiswa diharapkan mampu:
1. Memahami konsep optical flow dan motion estimation
2. Mengimplementasikan algoritma Lucas-Kanade dan Farneback
3. Menerapkan motion estimation untuk tracking dan analysis
4. Memahami aplikasi motion estimation di dunia nyata

## 🌍 Aplikasi Dunia Nyata
- **Video Stabilization**: Stabilisasi video pada smartphone dan action camera
- **Object Tracking**: Pelacakan objek dalam surveillance dan autonomous vehicles
- **Video Compression**: MPEG menggunakan motion vectors untuk kompresi
- **Sports Analytics**: Analisis pergerakan pemain dan bola
- **Medical Imaging**: Tracking organ movement dalam ultrasound

---

## 1. DEFINISI

### 1.1 Apa itu Motion Estimation?
**Motion Estimation** adalah proses menentukan pergerakan piksel atau region antar frame dalam video. Teknik ini menganalisis pola perubahan intensitas untuk memperkirakan arah dan kecepatan gerakan.

### 1.2 Optical Flow
**Optical Flow** adalah representasi visual dari pergerakan apparent dalam scene, yang menunjukkan perpindahan setiap piksel antara dua frame berurutan.

**Asumsi Brightness Constancy:**
```
I(x, y, t) = I(x + dx, y + dy, t + dt)
```

Dengan Taylor expansion:
```
∂I/∂x * u + ∂I/∂y * v + ∂I/∂t = 0
```
dimana u = dx/dt dan v = dy/dt adalah komponen optical flow.

### 1.3 Jenis Motion Estimation

| Jenis | Deskripsi | Contoh Algoritma |
|-------|-----------|------------------|
| **Sparse** | Hitung flow hanya pada keypoints | Lucas-Kanade |
| **Dense** | Hitung flow untuk setiap pixel | Farneback, TVL1 |
| **Block Matching** | Cari best match untuk blok | Full Search, Diamond |

---

## 2. KONSEP UTAMA

### 2.1 Lucas-Kanade Method
Algoritma **sparse optical flow** yang efisien dan robust untuk tracking points.

**Asumsi:**
1. Brightness constancy
2. Small motion (gerakan kecil antar frame)
3. Spatial coherence (piksel tetangga bergerak sama)

**Perhitungan:**
- Gunakan window kecil di sekitar point
- Solve over-determined system dengan least squares

### 2.2 Farneback Method
Algoritma **dense optical flow** yang menghitung flow untuk setiap pixel.

**Langkah-langkah:**
1. Approximate setiap neighborhood dengan polynomial
2. Estimasi displacement dari polynomial coefficients
3. Multi-scale pyramid untuk handle large motion

### 2.3 Pyramid/Multi-scale Approach
Untuk mengatasi batasan "small motion":
1. Buat image pyramid (downscale)
2. Estimasi flow di level coarse
3. Propagate dan refine ke level lebih fine

### 2.4 Horn-Schunck Method
Metode dense flow dengan global smoothness constraint:
- Minimize:
  ```
  E = ∫∫ [(Ixu + Iyv + It)² + α²(|∇u|² + |∇v|²)] dx dy
  ```
- α mengontrol smoothness

### 2.5 Deep Learning Methods
Modern approaches menggunakan CNN:
- **FlowNet**: End-to-end learning untuk optical flow
- **PWC-Net**: Pyramid, Warping, Cost volume
- **RAFT**: Recurrent All-Pairs Field Transforms

### 2.6 Translational Alignment (Image Registration)
Penyelarasan dua frame dengan translasi sederhana:

**Error metric umum:**
$$
E_{SSD}(u)=\sum_i\left[I_1(x_i+u)-I_0(x_i)\right]^2
$$

**Alternatif:**
- **SAD (L1)** lebih robust terhadap outlier
- **NCC** tahan terhadap perbedaan intensitas
- **Phase Correlation** (FFT) cepat untuk pergeseran besar

### 2.7 Fourier/Phase Correlation
Phase correlation memanfaatkan sifat fase pada domain Fourier untuk menemukan pergeseran:

$$
E_{PC}(u)=\mathcal{F}^{-1}\left(\frac{I_0(\omega)\cdot I_1(\omega)^*}{\lVert I_0(\omega)\rVert\,\lVert I_1(\omega)\rVert}\right)
$$

Puncak maksimum pada $E_{PC}$ menunjukkan estimasi $(dx, dy)$.

### 2.8 Frame Interpolation
Membuat frame di antara dua frame dengan optical flow:

$$
I_t(x)= (1-t)\,I_0(x) + t\,I_1(x + u_0)
$$

Kunci: **bi-directional flow**, **occlusion handling**, dan **blending**.

### 2.9 Rolling Shutter & Wobble Removal
Sensor rolling shutter menyebabkan distorsi garis lurus saat gerakan cepat.
Perbaikan dilakukan dengan **per-pixel flow** dan re-warp per scanline.

### 2.10 Layered Motion
Gerak kompleks dapat dipecah menjadi beberapa **layer** (foreground/background):
- Tiap layer memiliki motion model sendiri
- Berguna untuk **video object segmentation** dan **tracking**

---

## 3. DIAGRAM DAN ILUSTRASI

### 3.1 Optical Flow Visualization
```
Frame t           Frame t+1         Flow Field
┌─────────┐       ┌─────────┐       ┌─────────┐
│    O    │  →    │      O  │       │  → →    │
│         │       │         │       │         │
│  □      │  →    │    □    │       │    →    │
└─────────┘       └─────────┘       └─────────┘

O bergerak ke kanan → flow vector ke kanan
□ bergerak ke kanan → flow vector ke kanan
```

### 3.2 Lucas-Kanade Window
```
     Frame t              Frame t+1
    ┌───────────┐        ┌───────────┐
    │ ┌─────┐   │        │   ┌─────┐ │
    │ │point│   │   →    │   │point│ │
    │ │ + w │   │        │   │ + w │ │
    │ └─────┘   │        │   └─────┘ │
    └───────────┘        └───────────┘
    
    Window w di sekitar point digunakan
    untuk estimasi flow
```

### 3.3 Pyramid Approach
```
    Level 2 (coarse)    ┌───┐     Small image, 
                        │   │     estimate large motion
                        └───┘
                          ↓
    Level 1 (medium)   ┌─────┐    Medium image,
                       │     │    refine flow
                       └─────┘
                          ↓
    Level 0 (fine)    ┌───────┐   Original size,
                      │       │   fine-tune flow
                      └───────┘

```

### 3.4 Translational Alignment Pipeline (Diagram)

```mermaid
flowchart LR
   A[Frame t] --> B[Feature/Block Selection]
   B --> C[Similarity Metric (SSD/NCC/PC)]
   C --> D[Best Shift (dx, dy)]
   D --> E[Warp/Align Frame]
```

### 3.5 Frame Interpolation Pipeline (Diagram)

```mermaid
flowchart LR
   A[Frame t] --> B[Flow t→t+1]
   C[Frame t+1] --> D[Flow t+1→t]
   B --> E[Warp t (t=0.5)]
   D --> F[Warp t+1 (t=0.5)]
   E --> G[Blend]
   F --> G
   G --> H[Interpolated Frame]
```
```

---

## 4. CONTOH KASUS INDUSTRI

### 4.1 📱 Video Stabilization (GoPro, Smartphone)
**Skenario:** Menstabilkan video yang goyang.

**Penerapan:**
- Estimasi global motion antar frame
- Compensate untuk unwanted camera motion
- Preserve intentional motion (panning, zoom)

**Hasil:** Video yang smooth dan profesional

### 4.2 🚗 Autonomous Vehicles
**Skenario:** Tesla menggunakan optical flow untuk scene understanding.

**Penerapan:**
- Dense optical flow untuk ego-motion estimation
- Obstacle detection dari flow discontinuities
- Time-to-collision prediction

**Hasil:** Safer self-driving dengan better perception

### 4.3 ⚽ Sports Analytics
**Skenario:** Analisis pergerakan pemain sepak bola.

**Penerapan:**
- Track setiap pemain dengan sparse flow
- Calculate speed, distance, acceleration
- Heat map generation

**Hasil:** Data analytics untuk pelatih dan broadcaster

### 4.4 🎬 Video Compression (MPEG, H.264)
**Skenario:** Kompresi video untuk streaming.

**Penerapan:**
- Block matching untuk motion compensation
- Encode residual setelah motion compensation
- P-frames dan B-frames

**Hasil:** 10-50x compression ratio dengan kualitas baik

### 4.5 🏥 Medical Ultrasound
**Skenario:** Tracking jantung dalam echocardiography.

**Penerapan:**
- Speckle tracking dengan optical flow
- Wall motion analysis
- Strain rate imaging

**Hasil:** Quantitative cardiac function assessment

### 4.6 🎞️ Frame Interpolation (TV/Streaming)
**Skenario:** TV 60/120Hz menghasilkan frame tambahan.

**Penerapan:**
- Optical flow untuk warping frame
- Blending dengan occlusion handling

**Hasil:** Video lebih halus tanpa ghosting berlebih

### 4.7 📷 Rolling Shutter Correction
**Skenario:** Kamera ponsel saat gerakan cepat.

**Penerapan:**
- Per-pixel flow per scanline
- Re-warping untuk menghapus wobble

**Hasil:** Garis lurus tidak melengkung

---

## 5. RINGKASAN

### Poin-Poin Kunci:

1. **Optical Flow** merepresentasikan apparent motion dalam video

2. **Lucas-Kanade** adalah metode sparse yang efisien untuk tracking points
   - Cocok untuk feature tracking
   - Cepat tapi hanya untuk selected points

3. **Farneback** adalah metode dense yang compute-intensive
   - Flow untuk setiap pixel
   - Lebih informatif tapi lebih lambat

4. **Pyramid approach** mengatasi batasan small motion

5. **Aplikasi** meliputi stabilization, tracking, compression, analysis

6. **Translational alignment** dan **phase correlation** efektif untuk register cepat

7. **Frame interpolation** memanfaatkan optical flow untuk frame rate up-conversion

### Tabel Perbandingan Metode:

| Metode | Tipe | Kecepatan | Akurasi | Use Case |
|--------|------|-----------|---------|----------|
| Lucas-Kanade | Sparse | Cepat | Baik | Feature tracking |
| Farneback | Dense | Medium | Baik | Motion analysis |
| Horn-Schunck | Dense | Lambat | Good | Smooth flow |
| Deep (RAFT) | Dense | GPU-dependent | Best | Research |

---

## 6. KAITAN DENGAN PRAKTIKUM

| Materi | Praktikum | Output | Aplikasi Nyata |
|--------|-----------|--------|----------------|
| Translational Alignment | 07_translational_alignment.py | Estimasi dx, dy | Registrasi frame & stabilisasi |
| Optical Flow | 01–02 | Flow sparse/dense | Tracking & analisis gerak |
| Motion Detection | 03 | Mask gerak | Surveillance |
| Object Tracking | 04 | Trajectory | Monitoring objek |
| Motion History | 05 | MHI | Gesture & aktivitas |
| Video Stabilization | 06 | Video stabil | Action cam |
| Frame Interpolation | 08_frame_interpolation.py | Frame tengah | Slow-motion |

---

## 7. REFERENSI GAMBAR (TAUTAN)

1. Optical Flow (OpenCV tutorial): https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html
2. Phase Correlation (OpenCV docs): https://docs.opencv.org/4.x/d7/df3/group__imgproc__motion.html
3. Frame Interpolation overview (Szeliski Book): https://szeliski.org/Book/
4. Middlebury Optical Flow dataset (visual examples): https://vision.middlebury.edu/flow/

---

## 8. DESKRIPSI TUGAS VIDEO

### 📹 Tugas: Membuat Video Pembelajaran Motion Estimation

**Durasi:** 15-20 menit

**Format:** Screen recording dengan narasi

### Struktur Video:

#### A. PEMBUKAAN (2-3 menit)
1. ✅ Perkenalan diri
2. ✅ Judul: "Motion Estimation dan Optical Flow"
3. ✅ Tujuan pembelajaran
4. ✅ Contoh aplikasi sehari-hari

#### B. PENJELASAN TEORI (5-6 menit)
1. ✅ Definisi optical flow
2. ✅ Brightness constancy assumption
3. ✅ Lucas-Kanade vs Farneback
4. ✅ Pyramid approach
5. ✅ Visualisasi dengan diagram

#### C. DEMO PRAKTIKUM (7-9 menit)
1. ✅ **Demo 1: Sparse Flow (Lucas-Kanade)**
   - Track features pada video
   - Tampilkan tracks

2. ✅ **Demo 2: Dense Flow (Farneback)**
   - Visualisasi dengan color coding
   - Jelaskan warna = direction

3. ✅ **Demo 3: Motion Tracking**
   - Track objek spesifik
   - Tampilkan trajectory

#### D. ANALISIS (2-3 menit)
1. ✅ Perbandingan sparse vs dense
2. ✅ Kapan menggunakan masing-masing
3. ✅ Limitasi dan cara mengatasinya

#### E. PENUTUP (1-2 menit)
1. ✅ Kesimpulan
2. ✅ Tips untuk video sendiri
3. ✅ Saran pengembangan

### Kriteria Penilaian:
| Aspek | Bobot |
|-------|-------|
| Kelengkapan materi | 25% |
| Kejelasan penjelasan | 25% |
| Demo berhasil | 25% |
| Kualitas video | 15% |
| Kreativitas | 10% |
