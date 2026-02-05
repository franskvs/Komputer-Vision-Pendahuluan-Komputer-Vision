# JOBSHEET PRAKTIKUM
# MODUL 1: PENDAHULUAN COMPUTER VISION

---

## 🎯 TUJUAN PEMBELAJARAN

### Capaian Pembelajaran (Learning Outcomes):
Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. **Memahami** konsep dasar Computer Vision dan representasi citra digital
2. **Mengoperasikan** library OpenCV dan NumPy untuk pemrosesan gambar dasar
3. **Mengimplementasikan** operasi dasar: loading, display, konversi, dan manipulasi citra
4. **Menganalisis** properti gambar dan karakteristik color space yang berbeda
5. **Menerapkan** pemahaman untuk membangun aplikasi sederhana berbasis Computer Vision

### Tujuan Khusus per Percobaan:

| No | Percobaan | Tujuan Spesifik | Waktu |
|----|-----------|----------------|-------|
| 1 | Loading & Display Image | Memahami cara membaca dan menampilkan gambar dari berbagai format (jpg, png, bmp) menggunakan OpenCV dan Matplotlib | 20 menit |
| 2 | Image Properties | Mengakses dan memahami properti gambar (dimensi, channel, dtype, size) serta implikasinya | 20 menit |
| 3 | Color Space Conversion | Mengkonversi gambar antar color space (BGR, RGB, Grayscale, HSV) dan memahami aplikasinya | 25 menit |
| 4 | Pixel Access & Manipulation | Mengakses dan memodifikasi nilai piksel secara langsung untuk operasi tingkat rendah | 25 menit |
| 5 | Drawing & Annotation | Menggambar bentuk geometris dan menambahkan teks pada gambar untuk visualisasi | 20 menit |
| 6 | Arithmetic Operations | Melakukan operasi aritmatika pada gambar (blending, masking) | 20 menit |
| 7 | Save & Export | Menyimpan hasil pemrosesan dalam berbagai format dengan konfigurasi optimal | 20 menit |

---

## 🔧 2. ALAT & BAHAN

### A. Perangkat Keras (Hardware)
- [x] Laptop/PC dengan spesifikasi minimum:
  - Processor: Intel Core i3 atau setara
  - RAM: 4 GB (8 GB recommended)
  - Storage: 10 GB free space
- [x] Webcam (opsional, untuk beberapa percobaan)

### B. Perangkat Lunak (Software)
- [x] Sistem Operasi: Windows 10/11, Linux Ubuntu 20.04+, atau macOS 10.15+
- [x] Python 3.8 atau lebih baru
- [x] Code Editor: VS Code (recommended) atau PyCharm
- [x] Terminal/Command Prompt

### C. Library Python
```bash
pip install opencv-python numpy matplotlib pillow
```

### D. Bahan/Data
- [x] Sample gambar (sudah disediakan di folder `data/images/`)
- [x] Sample video (sudah disediakan di folder `data/videos/`)

---

## 📋 3. LANGKAH KERJA

### PERSIAPAN AWAL

#### Langkah 1: Setup Environment
```bash
# 1. Buka terminal/command prompt

# 2. Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv

# 3. Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

#### Langkah 2: Verifikasi Instalasi
```python
# Buat file test_install.py dan jalankan
import cv2
import numpy as np
import matplotlib.pyplot as plt

print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")
print("Instalasi berhasil!")
```

#### Langkah 3: Siapkan Struktur Folder
```
Bab-01-Pendahuluan/
├── praktikum/
│   ├── 01_loading_gambar.py
│   ├── 02_menampilkan_gambar.py
│   ├── ...
│   └── output/
├── data/
│   ├── images/
│   └── videos/
```

---

### PERCOBAAN 1: LOADING GAMBAR

**File:** `01_loading_gambar.py`

**Langkah-langkah:**
1. Buka file `01_loading_gambar.py`
2. Pelajari variabel yang dapat diubah di bagian atas
3. Jalankan program: `python 01_loading_gambar.py`
4. Amati output di terminal dan gambar yang ditampilkan
5. Coba ubah variabel `NAMA_FILE_GAMBAR` dengan gambar lain

**Variabel yang bisa dieksperimen:**
- `NAMA_FILE_GAMBAR`: Coba berbagai format (.jpg, .png, .bmp)
- Mode loading: `cv2.IMREAD_COLOR`, `cv2.IMREAD_GRAYSCALE`

---

### PERCOBAAN 2: MENAMPILKAN GAMBAR

**File:** `02_menampilkan_gambar.py`

**Langkah-langkah:**
1. Jalankan program
2. Amati perbedaan tampilan OpenCV vs Matplotlib
3. Perhatikan perbedaan urutan warna BGR vs RGB
4. Tutup window dengan menekan tombol keyboard

---

### PERCOBAAN 3: MEMBACA PROPERTI GAMBAR

**File:** `03_properti_gambar.py`

**Langkah-langkah:**
1. Jalankan program
2. Catat semua properti yang ditampilkan
3. Coba dengan gambar yang berbeda ukuran dan format

---

### PERCOBAAN 4: KONVERSI COLOR SPACE

**File:** `04_konversi_warna.py`

**Langkah-langkah:**
1. Jalankan program
2. Amati perbedaan visual setiap color space
3. Coba ubah threshold untuk HSV

---

### PERCOBAAN 5: MANIPULASI PIKSEL

**File:** `05_manipulasi_piksel.py`

**Langkah-langkah:**
1. Jalankan program
2. Pelajari cara akses piksel individual
3. Eksperimen dengan mengubah region piksel

---

### PERCOBAAN 6: MENGGAMBAR SHAPES

**File:** `06_menggambar_shapes.py`

**Langkah-langkah:**
1. Jalankan program
2. Pelajari parameter setiap fungsi drawing
3. Eksperimen dengan warna dan ketebalan berbeda

---

### PERCOBAAN 7: MENYIMPAN OUTPUT

**File:** `07_menyimpan_output.py`

**Langkah-langkah:**
1. Jalankan program
2. Cek folder output untuk hasil
3. Bandingkan ukuran file berbagai format

---

## 📊 4. DATA PENGAMATAN

### Tabel 1: Properti Gambar
| Parameter | Gambar 1 | Gambar 2 | Gambar 3 |
|-----------|----------|----------|----------|
| Nama File |          |          |          |
| Dimensi (W x H) |    |          |          |
| Jumlah Channel |     |          |          |
| Tipe Data |          |          |          |
| Ukuran File (KB) |   |          |          |
| Total Piksel |       |          |          |

### Tabel 2: Perbandingan Color Space
| Color Space | Jumlah Channel | Range Nilai | Karakteristik Visual |
|-------------|----------------|-------------|---------------------|
| BGR         |                |             |                     |
| RGB         |                |             |                     |
| Grayscale   |                |             |                     |
| HSV         |                |             |                     |

### Tabel 3: Hasil Drawing Operations
| Shape | Parameter | Hasil (screenshot) |
|-------|-----------|-------------------|
| Line  | pt1, pt2, color, thickness |     |
| Rectangle | pt1, pt2, color, thickness | |
| Circle | center, radius, color, thickness | |
| Text | text, position, font, scale |     |

### Tabel 4: Perbandingan Format Output
| Format | Ukuran File | Kualitas | Waktu Simpan |
|--------|-------------|----------|--------------|
| .jpg (Q=95) |         |          |              |
| .jpg (Q=50) |         |          |              |
| .png   |             |          |              |
| .bmp   |             |          |              |

---

## 🔬 5. ANALISIS

### Panduan Analisis Data:

#### A. Analisis Properti Gambar
1. **Bandingkan** dimensi gambar RGB vs Grayscale
   - Mengapa jumlah channel berbeda?
   - Bagaimana pengaruhnya terhadap ukuran memori?

2. **Hitung** total piksel dan bandingkan dengan ukuran file
   - Apakah ada kompresi?
   - Berapa rasio kompresi?

#### B. Analisis Color Space
1. **Jelaskan** mengapa OpenCV menggunakan BGR bukan RGB
2. **Analisis** kapan sebaiknya menggunakan HSV dibanding RGB
3. **Identifikasi** keuntungan konversi ke Grayscale

#### C. Analisis Manipulasi Piksel
1. **Bandingkan** kecepatan akses piksel individual vs slicing
2. **Analisis** efek perubahan piksel terhadap gambar keseluruhan

#### D. Analisis Format Output
1. **Bandingkan** trade-off antara ukuran file dan kualitas
2. **Identifikasi** format terbaik untuk setiap use case:
   - Web publishing
   - Archiving
   - Pemrosesan lebih lanjut

### Pertanyaan Analisis:
1. Mengapa gambar Grayscale memiliki 1 channel sedangkan RGB memiliki 3?
2. Apa perbedaan mendasar antara format lossy (JPG) dan lossless (PNG)?
3. Bagaimana koordinat piksel direpresentasikan dalam OpenCV?
4. Apa yang terjadi jika kita mengassign nilai > 255 ke piksel?

---

## 📝 6. KESIMPULAN

### Panduan Membuat Kesimpulan:

#### Format Kesimpulan yang Baik:
```
Dari praktikum ini dapat disimpulkan bahwa:

1. [Sebutkan konsep utama yang dipelajari]
   Contoh: "Gambar digital direpresentasikan sebagai array NumPy 
   dengan dimensi (height, width, channels)"

2. [Sebutkan teknik/metode yang dikuasai]
   Contoh: "Konversi color space dapat dilakukan menggunakan 
   cv2.cvtColor() dengan berbagai kode konversi"

3. [Sebutkan insight dari hasil eksperimen]
   Contoh: "Format PNG menghasilkan file lebih besar namun tanpa 
   kehilangan kualitas dibanding JPG"

4. [Hubungkan dengan aplikasi dunia nyata]
   Contoh: "Pemahaman tentang color space sangat penting untuk 
   aplikasi seperti deteksi warna objek"
```

#### Checklist Kesimpulan:
- [ ] Menjawab tujuan praktikum
- [ ] Berdasarkan data hasil percobaan
- [ ] Menggunakan bahasa ilmiah
- [ ] Ada insight/pembelajaran baru
- [ ] Tidak copy-paste dari materi

---

## ✅ CHECKLIST PENYELESAIAN

- [ ] Semua percobaan telah dijalankan
- [ ] Semua tabel data pengamatan terisi
- [ ] Analisis setiap percobaan selesai
- [ ] Kesimpulan ditulis dengan baik
- [ ] Output tersimpan di folder yang benar
- [ ] Screenshot hasil dilampirkan

---

**Catatan:**
- Simpan semua hasil percobaan
- Jika ada error, screenshot dan dokumentasikan solusinya
- Diskusikan dengan teman/asisten jika menemui kesulitan
