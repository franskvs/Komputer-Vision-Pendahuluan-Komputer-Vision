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

### Tabel Perbandingan Metode:

| Metode | Tipe | Kecepatan | Akurasi | Use Case |
|--------|------|-----------|---------|----------|
| Lucas-Kanade | Sparse | Cepat | Baik | Feature tracking |
| Farneback | Dense | Medium | Baik | Motion analysis |
| Horn-Schunck | Dense | Lambat | Good | Smooth flow |
| Deep (RAFT) | Dense | GPU-dependent | Best | Research |

---

## 6. DESKRIPSI TUGAS VIDEO

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
