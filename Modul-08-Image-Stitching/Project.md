# PROJECT BAB 8: IMAGE STITCHING DAN PANORAMA

## 🎯 SISTEM PEMBUATAN VIRTUAL TOUR INTERAKTIF

---

## 📖 LATAR BELAKANG

Sebuah agen properti **"HomeVision Property"** ingin meningkatkan penjualan dengan menyediakan virtual tour 360° untuk setiap listing properti. Riset menunjukkan bahwa listing dengan virtual tour mendapat 87% lebih banyak views dan 40% lebih cepat terjual.

**Masalah yang dihadapi:**
- Biaya menyewa fotografer profesional sangat mahal (Rp 5-10 juta per properti)
- Waktu produksi lama (1-2 minggu per properti)
- Kualitas hasil outsource tidak konsisten
- Perlu update cepat jika ada renovasi

**Solusi yang diharapkan:**
Sistem DIY yang memungkinkan agen property mengambil foto dengan smartphone dan otomatis membuat panorama 360° yang bisa di-embed ke website listing.

---

## 🎯 TUJUAN PROJECT

### Tujuan Utama:
Mengembangkan aplikasi pembuat panorama otomatis yang mudah digunakan oleh non-technical user.

### Tujuan Khusus:
1. Membuat sistem stitching yang robust untuk berbagai kondisi
2. Menghasilkan panorama berkualitas dari foto smartphone
3. Menyediakan preview dan export dalam format web-compatible
4. Menangani error dan memberikan feedback yang jelas

---

## 📋 DESKRIPSI TUGAS

### Skenario:
Anda adalah developer di **HomeVision Property**. Anda ditugaskan membuat prototype aplikasi "QuickPano" yang dapat:

1. **Input Gambar:**
   - Menerima 4-8 foto dari folder atau capture langsung
   - Validasi: overlap cukup, ukuran konsisten

2. **Processing:**
   - Otomatis detect urutan gambar
   - Stitching dengan blending yang baik
   - Progress indicator untuk user

3. **Output:**
   - Panorama dalam format JPEG dengan kualitas tinggi
   - Thumbnail untuk preview
   - HTML viewer sederhana untuk embed

4. **Error Handling:**
   - Feedback jelas jika stitching gagal
   - Suggestion untuk perbaikan

---

## 📝 SPESIFIKASI TEKNIS

### Input:
- 4-8 gambar dengan overlap 20-50%
- Format: JPG, PNG
- Resolusi minimum: 1920x1080 (Full HD)
- Ukuran file maksimum per gambar: 10MB

### Output:
1. **Panorama File:**
   - Format: JPEG
   - Quality: 90%
   - Nama: `panorama_[timestamp].jpg`

2. **Thumbnail:**
   - Resolusi: 400px width
   - Format: JPEG

3. **Metadata:**
   - Jumlah gambar sumber
   - Dimensi output
   - Processing time
   - Status (success/warning/error)

4. **HTML Viewer (bonus):**
   - Simple 360° viewer menggunakan CSS/JS
   - Responsive untuk mobile

### Kriteria Keberhasilan:
| Kriteria | Target |
|----------|--------|
| Success rate dengan foto yang baik | ≥ 95% |
| Processing time untuk 5 gambar | < 30 detik |
| Seam visibility | Tidak terlihat pada jarak normal |
| User feedback | Jelas dan actionable |

---

## 🔧 FITUR YANG HARUS DIIMPLEMENTASIKAN

### Fitur Wajib (80 poin):

1. **Image Loading & Validation** (15 poin)
   - Load multiple images dari folder
   - Validasi ukuran dan format
   - Preview gambar yang di-load

2. **Automatic Stitching** (30 poin)
   - Feature detection dan matching
   - Homography estimation dengan RANSAC
   - Robust warping dan alignment
   - Handle berbagai urutan gambar

3. **Blending** (15 poin)
   - Feather blending atau multi-band
   - Tidak ada seam yang terlihat jelas
   - Handle perbedaan exposure ringan

4. **Output Generation** (10 poin)
   - Save panorama dengan kualitas baik
   - Generate thumbnail
   - Log processing info

5. **User Interface** (10 poin)
   - CLI atau GUI sederhana
   - Progress indicator
   - Error messages yang jelas

### Fitur Tambahan (20 poin bonus):

1. **Exposure Compensation** (5 poin)
   - Otomatis adjust brightness antar gambar
   - Konsisten exposure di output

2. **Auto Crop** (5 poin)
   - Crop area hitam otomatis
   - Maximize content area

3. **HTML 360° Viewer** (5 poin)
   - Generate HTML dengan panorama viewer
   - Touch/drag untuk rotate view

4. **Batch Processing** (5 poin)
   - Process multiple folders
   - Generate report

---

## 📊 DATA YANG DIGUNAKAN

### Opsi 1: Foto Sendiri (Recommended)
**Cara mengambil foto yang baik:**
1. Berdiri di tengah ruangan
2. Putar badan (bukan kamera) dengan increment ~45°
3. Overlap 30-50% antara foto berurutan
4. Konsisten ketinggian dan tilt kamera
5. Hindari objek bergerak (orang, hewan)

### Opsi 2: Dataset dari Internet
- Gunakan dataset panorama dari OpenCV samples
- Download dari image stitching datasets

### Opsi 3: Simulasi
- Crop bagian-bagian dari panorama yang sudah jadi
- Berguna untuk testing algoritma

---

## 📁 STRUKTUR PROJECT

```
project_quickpano/
├── main.py                 # Entry point aplikasi
├── stitcher.py            # Core stitching module
├── blender.py             # Blending algorithms
├── validator.py           # Input validation
├── utils.py               # Helper functions
├── viewer_generator.py    # HTML viewer generator
├── input/
│   ├── set1/              # Contoh set pertama
│   ├── set2/              # Contoh set kedua
│   └── ...
├── output/
│   ├── panoramas/         # Hasil panorama
│   ├── thumbnails/        # Thumbnail
│   └── viewers/           # HTML viewers
├── tests/
│   ├── test_stitcher.py
│   └── test_data/
└── README.md
```

---

## 📝 LANGKAH PENGERJAAN

### Tahap 1: Persiapan (Hari 1)
1. Buat struktur folder project
2. Kumpulkan minimal 3 set foto (masing-masing 5+ foto)
3. Buat modul validator untuk cek input
4. Setup basic logging

### Tahap 2: Core Stitching (Hari 2-3)
1. Implementasi feature detection & matching
2. Implementasi homography estimation
3. Implementasi warping
4. Testing dengan 2 gambar

### Tahap 3: Blending & Enhancement (Hari 4)
1. Implementasi feather blending
2. Tambah exposure compensation (jika waktu cukup)
3. Implementasi auto-crop
4. Testing dengan multiple gambar

### Tahap 4: UI & Output (Hari 5)
1. Buat interface (CLI/GUI)
2. Implementasi output generation
3. Generate HTML viewer (bonus)
4. Documentation & testing final

---

## 🎥 DEMO YANG HARUS DITUNJUKKAN

Buat video demo (3-5 menit) yang menunjukkan:

1. **Load gambar**
   - Tunjukkan folder dengan 5 foto ruangan
   - Tunjukkan validasi berhasil

2. **Processing**
   - Tunjukkan progress indicator
   - Jelaskan step yang sedang berjalan

3. **Hasil sukses**
   - Tampilkan panorama output
   - Zoom ke area seam, tunjukkan tidak terlihat
   - Buka di viewer (jika ada)

4. **Error handling**
   - Coba dengan gambar yang overlap kurang
   - Tunjukkan error message yang informatif

---

## 📊 RUBRIK PENILAIAN

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| **Fungsionalitas** | 40% | Stitching berhasil, output benar |
| **Kualitas Hasil** | 20% | Seam tidak terlihat, exposure consistent |
| **Kode** | 20% | Clean, modular, documented |
| **Dokumentasi** | 10% | README jelas, mudah diikuti |
| **Demo Video** | 10% | Lengkap, profesional |

### Detail Penilaian Fungsionalitas:
| Fitur | Poin |
|-------|------|
| Load & validate images | 10 |
| Feature matching berhasil | 10 |
| Homography estimation | 10 |
| Warping benar | 10 |
| Blending baik | 15 |
| Output tersimpan | 5 |
| Error handling | 10 |
| Fitur bonus | +20 |

---

## ⚠️ CATATAN PENTING

1. **Testing:** Test dengan berbagai kondisi:
   - Foto indoor dan outdoor
   - Berbagai level overlap
   - Berbagai resolusi

2. **Robustness:** Program tidak boleh crash:
   - Handle file not found
   - Handle insufficient matches
   - Handle memory issues

3. **Performance:** Optimasi jika terlalu lambat:
   - Resize gambar sebelum processing
   - Gunakan ORB untuk kecepatan

---

## 💡 HINTS DAN TIPS

### Tip 1: Ordering Gambar
```python
# Jika urutan tidak diketahui, bisa heuristic berdasarkan match count
def find_order(images):
    # Gambar dengan paling banyak match ke gambar lain = tengah
    # Build chain dari sana
```

### Tip 2: Robust Stitching
```python
# Minimal parameters untuk hasil baik
MIN_MATCH_COUNT = 10
RANSAC_THRESHOLD = 5.0
RATIO_TEST = 0.7
```

### Tip 3: Feather Blending
```python
# Feather mask generation
def create_feather_mask(width, height, blend_width):
    mask = np.ones((height, width), np.float32)
    # Gradient di edges
    for i in range(blend_width):
        alpha = i / blend_width
        mask[:, i] = alpha
        mask[:, width-1-i] = alpha
    return mask
```

### Tip 4: Auto Crop
```python
# Crop area hitam
def auto_crop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    return image[y:y+h, x:x+w]
```

---

## 📚 REFERENSI

1. OpenCV Stitcher documentation
2. "Automatic Panoramic Image Stitching using Invariant Features" - Matthew Brown
3. Materi Praktikum Bab 8
4. OpenCV samples: stitching.py

---

**Selamat mengerjakan! 🏠📷**

*"Create stunning virtual tours, one stitch at a time."*
