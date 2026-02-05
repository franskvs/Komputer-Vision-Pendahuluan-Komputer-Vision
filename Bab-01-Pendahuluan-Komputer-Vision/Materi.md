# BAB 1: PENDAHULUAN COMPUTER VISION

## 📚 1. DEFINISI

### Apa itu Computer Vision?
**Computer Vision** (Visi Komputer) adalah cabang ilmu kecerdasan buatan (AI) yang memungkinkan komputer untuk "melihat" dan memahami konten visual dari dunia nyata melalui gambar digital atau video.

Secara teknis, Computer Vision adalah:
> "Bidang ilmu yang mempelajari bagaimana komputer dapat memperoleh pemahaman tingkat tinggi dari gambar atau video digital - mulai dari akuisisi, pemrosesan, analisis, hingga pemahaman visual."

### Perbedaan dengan Image Processing
| Aspek | Image Processing | Computer Vision |
|-------|------------------|-----------------|
| **Tujuan** | Meningkatkan kualitas gambar | Memahami konten gambar |
| **Input** | Gambar | Gambar |
| **Output** | Gambar yang lebih baik | Informasi/keputusan |
| **Contoh** | Filter, enhancement | Deteksi objek, klasifikasi |

---

## 🎯 2. KONSEP UTAMA

### 2.1 Pipeline Computer Vision
```
Akuisisi Citra → Pre-processing → Feature Extraction → Analisis → Interpretasi
     ↓               ↓                  ↓                ↓           ↓
  Kamera/       Filter, resize,     Deteksi tepi,   Klasifikasi,  Keputusan/
  Sensor        normalisasi         corner, SIFT    deteksi       aksi
```

### 2.2 Level Pemrosesan Visual

1. **Low-level Vision** (Visi Tingkat Rendah)
   - Pemrosesan piksel-piksel dasar
   - Contoh: Edge detection, filtering, thresholding

2. **Mid-level Vision** (Visi Tingkat Menengah)
   - Ekstraksi fitur dan segmentasi
   - Contoh: Feature matching, motion estimation

3. **High-level Vision** (Visi Tingkat Tinggi)
   - Pemahaman semantik
   - Contoh: Object recognition, scene understanding

### 2.3 Representasi Gambar Digital

```
Gambar = Matriks 2D dari piksel
       = f(x, y) dimana x, y adalah koordinat

Gambar Grayscale: 1 channel (0-255)
Gambar RGB: 3 channel (R, G, B masing-masing 0-255)

Contoh matriks gambar 3x3:
[[ 45,  89, 120],
 [100, 150, 200],
 [ 30,  75, 180]]
```

### 2.4 Color Spaces
- **RGB**: Red, Green, Blue - standar untuk display
- **BGR**: Blue, Green, Red - format OpenCV
- **HSV**: Hue, Saturation, Value - lebih intuitif untuk analisis warna
- **Grayscale**: Single channel untuk simplifikasi

---

## 📊 3. DIAGRAM & ILUSTRASI

### 3.1 Arsitektur Sistem Computer Vision
```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEM COMPUTER VISION                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌──────────────┐    ┌─────────────┐        │
│  │  INPUT  │───▶│  PROCESSING  │───▶│   OUTPUT    │        │
│  │ (Citra) │    │  (Algoritma) │    │ (Informasi) │        │
│  └─────────┘    └──────────────┘    └─────────────┘        │
│       │               │                    │                │
│       ▼               ▼                    ▼                │
│   - Kamera        - Filtering         - Klasifikasi        │
│   - Scanner       - Segmentation      - Deteksi            │
│   - Video         - Feature Ext.      - Tracking           │
│   - Sensor        - Deep Learning     - Rekonstruksi       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Representasi Piksel
```
    Koordinat Gambar            Channel RGB
    
    (0,0)──────▶ x             R Channel  G Channel  B Channel
      │                         ┌───┐      ┌───┐      ┌───┐
      │  ┌───┬───┬───┐         │255│      │  0│      │  0│  = Merah
      │  │ P │ P │ P │         └───┘      └───┘      └───┘
      ▼  ├───┼───┼───┤
      y  │ P │ P │ P │         ┌───┐      ┌───┐      ┌───┐
         ├───┼───┼───┤         │  0│      │255│      │  0│  = Hijau
         │ P │ P │ P │         └───┘      └───┘      └───┘
         └───┴───┴───┘
```

---

## 🏭 4. CONTOH KASUS INDUSTRI & DUNIA NYATA

### 4.1 Industri Manufaktur
**Quality Control (Pengendalian Mutu)**
- Deteksi cacat produk secara otomatis
- Inspeksi komponen elektronik
- Pengecekan packaging

### 4.2 Kesehatan/Medis
**Medical Imaging**
- Deteksi tumor dari CT scan/MRI
- Analisis retina untuk deteksi diabetes
- Counting sel darah

### 4.3 Otomotif
**Self-Driving Cars**
- Deteksi pejalan kaki
- Lane detection (deteksi jalur)
- Traffic sign recognition

### 4.4 Keamanan
**Surveillance System**
- Face recognition untuk akses kontrol
- Deteksi anomali/suspicious behavior
- License plate recognition (ANPR)

### 4.5 Retail
**Smart Retail**
- Automated checkout (Amazon Go)
- Inventory management
- Customer behavior analysis

### 4.6 Pertanian
**Precision Agriculture**
- Deteksi penyakit tanaman
- Estimasi hasil panen
- Monitoring tanaman dengan drone

### 4.7 Smartphone
**Camera Features**
- Portrait mode (depth estimation)
- Face detection untuk fokus
- AR filters (Instagram, Snapchat)

---

## 📝 5. RINGKASAN

### Poin-Poin Penting:

1. **Computer Vision** memungkinkan komputer memahami konten visual seperti manusia

2. **Tiga level pemrosesan**: Low-level (piksel), Mid-level (fitur), High-level (semantik)

3. **Representasi gambar digital**: Matriks 2D dengan nilai intensitas per piksel

4. **Library utama**: OpenCV (Python/C++), TensorFlow, PyTorch

5. **Aplikasi luas**: Dari industri manufaktur hingga smartphone sehari-hari

### Formula Penting:
```
# Resolusi gambar
Total Piksel = Width × Height

# Ukuran file (tanpa kompresi)
File Size = Width × Height × Channels × Bit Depth / 8 (bytes)

# Contoh: Gambar RGB 1920x1080
= 1920 × 1080 × 3 × 8 / 8 = 6,220,800 bytes ≈ 6 MB
```

---

## 🎬 6. DESKRIPSI TUGAS VIDEO

### Instruksi Pembuatan Video Penjelasan

**Durasi**: 15-25 menit

**Format**: Screen recording + webcam (picture-in-picture)

### Struktur Video yang WAJIB Diikuti:

#### A. PEMBUKAAN (2-3 menit)
1. ✅ Perkenalan diri (nama, NIM, kelas)
2. ✅ Judul materi: "Pendahuluan Computer Vision"
3. ✅ Sebutkan tujuan pembelajaran
4. ✅ Overview singkat apa yang akan dipelajari

#### B. PENJELASAN MATERI (5-8 menit)
1. ✅ Jelaskan definisi Computer Vision dengan bahasa sendiri
2. ✅ Gambarkan diagram pipeline CV (bisa pakai whiteboard/drawing tool)
3. ✅ Jelaskan perbedaan Low/Mid/High level vision
4. ✅ Berikan minimal 3 contoh aplikasi nyata di sekitar Anda
5. ✅ Jelaskan representasi gambar digital (matriks piksel)

#### C. PRAKTIKUM & DEMONSTRASI (8-12 menit)
1. ✅ Tunjukkan environment Python yang sudah di-setup
2. ✅ **Percobaan 1**: Loading dan menampilkan gambar
   - Jalankan program, jelaskan setiap baris kode
3. ✅ **Percobaan 2**: Membaca properti gambar
   - Tunjukkan dimensi, tipe data, dll
4. ✅ **Percobaan 3**: Konversi color space
   - Demo RGB ke Grayscale, RGB ke HSV
5. ✅ **Percobaan 4**: Manipulasi piksel dasar
   - Tunjukkan akses dan modifikasi piksel
6. ✅ **Percobaan 5**: Menggambar bentuk pada gambar
   - Line, rectangle, circle, text
7. ✅ **Percobaan 6**: Menyimpan output
   - Save dengan berbagai format

#### D. ANALISIS HASIL (2-3 menit)
1. ✅ Tunjukkan dan jelaskan output dari setiap percobaan
2. ✅ Bandingkan hasil dengan ekspektasi
3. ✅ Jelaskan apa yang dipelajari dari masing-masing percobaan

#### E. PENUTUP (1-2 menit)
1. ✅ Rangkum poin-poin penting
2. ✅ Sebutkan kesulitan yang dihadapi (jika ada)
3. ✅ Kesimpulan pembelajaran
4. ✅ Ucapan terima kasih dan salam penutup

### Kriteria Penilaian Video:
- **Kejelasan penjelasan**: 25%
- **Kelengkapan materi**: 25%
- **Demonstrasi praktikum**: 30%
- **Kualitas video & audio**: 10%
- **Struktur & flow**: 10%

---

## 📖 REFERENSI

1. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications*, 2nd Edition
2. OpenCV Documentation: https://docs.opencv.org/
3. Python Official Documentation: https://docs.python.org/
