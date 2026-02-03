# JOBSHEET PRAKTIKUM
# BAB 8: IMAGE STITCHING DAN PEMBUATAN PANORAMA

---

## 📋 INFORMASI PRAKTIKUM
| Item | Keterangan |
|------|------------|
| Mata Kuliah | Praktikum Computer Vision |
| Materi | Image Stitching dan Pembuatan Panorama |
| Pertemuan | Bab 8 |
| Waktu | 150 menit |

---

## 1. TUJUAN PRAKTIKUM

### 1.1 Tujuan Umum
Mahasiswa mampu memahami dan mengimplementasikan teknik image stitching untuk membuat gambar panorama dari multiple images.

### 1.2 Tujuan Khusus per Percobaan

| No | Percobaan | Tujuan |
|----|-----------|--------|
| 1 | Simple Image Stitching | Menggabungkan 2 gambar menggunakan homography manual |
| 2 | OpenCV Stitcher Class | Menggunakan high-level API OpenCV untuk stitching |
| 3 | Blending Techniques | Membandingkan berbagai teknik blending |
| 4 | Multi-Image Panorama | Membuat panorama dari 3+ gambar |
| 5 | Cylindrical Projection | Mengimplementasikan proyeksi silinder |
| 6 | Real-time Stitching | Melakukan stitching dari video/webcam |

---

## 2. ALAT DAN BAHAN

### 2.1 Perangkat Keras
| No | Alat | Spesifikasi Minimum |
|----|------|---------------------|
| 1 | Komputer/Laptop | RAM 8GB, Processor i5 atau setara |
| 2 | Webcam (opsional) | Resolusi 720p |
| 3 | Smartphone | Untuk mengambil foto |

### 2.2 Perangkat Lunak
| No | Software | Versi |
|----|----------|-------|
| 1 | Python | 3.8+ |
| 2 | OpenCV | 4.5+ |
| 3 | NumPy | 1.19+ |
| 4 | Matplotlib | 3.3+ |
| 5 | imutils | 0.5+ |

### 2.3 Bahan Praktikum
| No | Bahan | Keterangan |
|----|-------|------------|
| 1 | Gambar panorama set 1 | 2 gambar dengan overlap |
| 2 | Gambar panorama set 2 | 3+ gambar untuk multi-image |
| 3 | Foto sendiri (recommended) | Foto dari smartphone dengan overlap |

---

## 3. LANGKAH KERJA

### 3.1 Persiapan Environment

#### Langkah 1: Instalasi Dependencies
```bash
cd "Praktikum Komputer Vision"
pip install -r requirements.txt
```

#### Langkah 2: Download Data Sampel
```bash
cd Bab-08-Image-Stitching
python download_sample_data.py
```

#### Langkah 3: Struktur Folder
```
Bab-08-Image-Stitching/
├── praktikum/
│   ├── 01_simple_stitching.py
│   ├── 02_opencv_stitcher.py
│   ├── 03_blending_comparison.py
│   ├── 04_multi_image_panorama.py
│   ├── 05_cylindrical_projection.py
│   ├── 06_realtime_stitching.py
│   └── output/
├── data/
│   └── images/
└── download_sample_data.py
```

### 3.2 Mengambil Foto Sendiri (Recommended)

**Tips untuk foto panorama yang baik:**
1. Gunakan mode manual pada kamera HP (jika ada)
2. Ambil foto dengan overlap 30-50%
3. Jangan bergerak maju/mundur, hanya rotasi
4. Pastikan exposure konsisten
5. Hindari objek bergerak di area overlap

---

### 3.3 Pelaksanaan Percobaan

#### PERCOBAAN 1: Simple Image Stitching

**Tujuan:** Memahami dasar stitching dengan homography manual

**Langkah-langkah:**
1. Buka file `01_simple_stitching.py`
2. Pelajari alur: feature detection → matching → homography → warping
3. Jalankan program:
   ```bash
   python praktikum/01_simple_stitching.py
   ```
4. Amati output dan perhatikan seam di area overlap
5. **Variasi:**
   - Ubah `MIN_MATCH_COUNT` dari 10 ke 20
   - Ubah detector dari ORB ke SIFT
   - Coba dengan gambar yang overlap sedikit

#### PERCOBAAN 2: OpenCV Stitcher Class

**Tujuan:** Menggunakan high-level API yang lebih robust

**Langkah-langkah:**
1. Buka file `02_opencv_stitcher.py`
2. Bandingkan kode dengan simple stitching (jauh lebih singkat!)
3. Jalankan program:
   ```bash
   python praktikum/02_opencv_stitcher.py
   ```
4. **Variasi:**
   - Ubah mode dari `PANORAMA` ke `SCANS`
   - Coba dengan jumlah gambar berbeda

#### PERCOBAAN 3: Blending Techniques

**Tujuan:** Membandingkan berbagai teknik blending

**Langkah-langkah:**
1. Buka file `03_blending_comparison.py`
2. Jalankan program:
   ```bash
   python praktikum/03_blending_comparison.py
   ```
3. Perhatikan perbedaan:
   - No blending: seam terlihat jelas
   - Alpha blending: transisi lebih halus
   - Feather blending: hampir tidak terlihat
4. **Variasi:**
   - Ubah `BLEND_WIDTH` dari 50 ke 10, 100
   - Coba dengan gambar yang berbeda exposure

#### PERCOBAAN 4: Multi-Image Panorama

**Tujuan:** Membuat panorama dari 3+ gambar

**Langkah-langkah:**
1. Buka file `04_multi_image_panorama.py`
2. Jalankan program:
   ```bash
   python praktikum/04_multi_image_panorama.py
   ```
3. Amati proses incremental stitching
4. **Variasi:**
   - Coba dengan 5+ gambar
   - Gunakan foto sendiri

#### PERCOBAAN 5: Cylindrical Projection

**Tujuan:** Membuat panorama dengan proyeksi silinder

**Langkah-langkah:**
1. Buka file `05_cylindrical_projection.py`
2. Jalankan program:
   ```bash
   python praktikum/05_cylindrical_projection.py
   ```
3. Bandingkan dengan proyeksi planar
4. **Variasi:**
   - Ubah focal length
   - Coba dengan panorama lebih dari 180°

#### PERCOBAAN 6: Real-time Stitching

**Tujuan:** Melakukan stitching dari webcam/video

**Langkah-langkah:**
1. Buka file `06_realtime_stitching.py`
2. Jalankan program:
   ```bash
   python praktikum/06_realtime_stitching.py
   ```
3. Arahkan webcam ke scene dan capture frames
4. Tekan 'c' untuk capture, 's' untuk stitch

---

## 4. DATA PENGAMATAN

### 4.1 Tabel Pengamatan Percobaan 1 (Simple Stitching)

| Parameter | Nilai | Good Matches | Inliers | Waktu (ms) | Kualitas Visual |
|-----------|-------|--------------|---------|------------|-----------------|
| ORB, MIN=10 | Default | ... | ... | ... | ... |
| ORB, MIN=20 | Variasi 1 | ... | ... | ... | ... |
| SIFT, MIN=10 | Variasi 2 | ... | ... | ... | ... |
| SIFT, MIN=20 | Variasi 3 | ... | ... | ... | ... |

### 4.2 Tabel Pengamatan Percobaan 2 (OpenCV Stitcher)

| Mode | Jumlah Gambar | Status | Waktu (ms) | Kualitas |
|------|---------------|--------|------------|----------|
| PANORAMA | 2 | ... | ... | ... |
| PANORAMA | 3 | ... | ... | ... |
| PANORAMA | 5 | ... | ... | ... |
| SCANS | 2 | ... | ... | ... |

### 4.3 Tabel Pengamatan Percobaan 3 (Blending)

| Teknik Blending | Blend Width | Seam Visibility | Ghosting | Rating (1-5) |
|-----------------|-------------|-----------------|----------|--------------|
| No Blending | - | ... | ... | ... |
| Alpha Blending | 50 | ... | ... | ... |
| Feather | 50 | ... | ... | ... |
| Feather | 100 | ... | ... | ... |

### 4.4 Tabel Pengamatan Percobaan 4 (Multi-Image)

| Jumlah Gambar | Total Features | Total Matches | Waktu Total | Dimensi Output |
|---------------|----------------|---------------|-------------|----------------|
| 3 | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... |

### 4.5 Tabel Perbandingan Proyeksi

| Proyeksi | FOV Maksimal | Distorsi | Cocok Untuk |
|----------|--------------|----------|-------------|
| Planar | ... | ... | ... |
| Cylindrical | ... | ... | ... |

---

## 5. ANALISIS

### 5.1 Panduan Analisis Percobaan 1-2

Jawab pertanyaan berikut:
1. **Pengaruh MIN_MATCH_COUNT:** Mengapa nilai terlalu rendah berbahaya?
2. **ORB vs SIFT:** Mana yang menghasilkan stitching lebih baik? Mengapa?
3. **Simple vs Stitcher Class:** Apa kelebihan masing-masing approach?
4. **Error handling:** Apa yang terjadi jika overlap kurang dari 10%?

### 5.2 Panduan Analisis Percobaan 3 (Blending)

Jawab pertanyaan berikut:
1. **Seam visibility:** Mengapa no blending menghasilkan seam yang jelas?
2. **Ghosting:** Kapan ghosting terjadi? Bagaimana mengatasinya?
3. **Blend width optimal:** Berapa nilai yang memberikan hasil terbaik?
4. **Trade-off:** Apa trade-off antara kecepatan dan kualitas blending?

### 5.3 Panduan Analisis Percobaan 4-5

Jawab pertanyaan berikut:
1. **Scalability:** Bagaimana waktu proses berubah dengan jumlah gambar?
2. **Error accumulation:** Apakah ada akumulasi error di panorama panjang?
3. **Cylindrical benefit:** Kapan proyeksi cylindrical lebih baik dari planar?
4. **Focal length:** Bagaimana focal length mempengaruhi hasil cylindrical?

### 5.4 Masalah Umum dan Solusi

| Masalah | Kemungkinan Penyebab | Solusi |
|---------|---------------------|--------|
| Stitching gagal | Overlap kurang | Ambil ulang foto dengan overlap 30-50% |
| Ghosting | Objek bergerak | Hindari objek bergerak di area overlap |
| Distorsi | Parallax | Rotasi di tempat, jangan bergeser |
| Seam visible | Exposure berbeda | Gunakan multi-band blending |

---

## 6. KESIMPULAN

### 6.1 Format Kesimpulan

Buat kesimpulan dengan menjawab pertanyaan berikut:

1. **Komponen Stitching:**
   - Apa saja langkah utama dalam image stitching?
   - Bagian mana yang paling kritis?

2. **Blending:**
   - Mengapa blending diperlukan?
   - Teknik mana yang paling cocok untuk berbagai situasi?

3. **Proyeksi:**
   - Kapan menggunakan planar vs cylindrical?
   - Apa batasan masing-masing?

4. **Praktis:**
   - Tips untuk mengambil foto panorama yang baik?
   - Error apa yang paling sering ditemui?

5. **Perbandingan dengan Smartphone:**
   - Bagaimana hasil dibanding fitur panorama bawaan HP?
   - Apa kelebihan dan kekurangan masing-masing?

### 6.2 Template Kesimpulan

```
KESIMPULAN PRAKTIKUM BAB 8

1. Image Stitching Pipeline:
   - Langkah utama: ...
   - Bagian paling kritis: ...

2. Blending:
   - No blending: cocok untuk...
   - Feather blending: cocok untuk...
   - Multi-band: cocok untuk...

3. Hasil Eksperimen:
   - Simple stitching berhasil dengan overlap minimal ...%
   - OpenCV Stitcher lebih robust karena...
   - Waktu proses rata-rata: ...

4. Tips Praktis:
   - Overlap optimal: ...%
   - Blend width optimal: ...
   - Detector terbaik untuk kasus ini: ...

5. Pembelajaran:
   - Kesulitan: ...
   - Solusi: ...
```

---

## 📎 LAMPIRAN

### Checklist Praktikum
- [ ] Semua percobaan selesai dijalankan
- [ ] Output tersimpan di folder yang benar
- [ ] Tabel pengamatan terisi lengkap
- [ ] Analisis setiap percobaan selesai
- [ ] Kesimpulan ditulis
- [ ] Mencoba dengan foto sendiri (bonus)

### Pengumpulan
1. Folder lengkap dengan output
2. Foto panorama hasil sendiri
3. Laporan dalam format PDF
4. Video penjelasan (sesuai tugas video)
