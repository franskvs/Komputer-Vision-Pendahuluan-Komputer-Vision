# PROJECT BAB 1: PENDAHULUAN COMPUTER VISION

---

## 🎯 JUDUL PROJECT
# "Sistem Pencatat Kehadiran Digital Berbasis Kartu Identitas"

---

## 📖 DESKRIPSI SOAL CERITA

### Latar Belakang:
Anda adalah seorang developer di sebuah perusahaan startup bernama "SmartAttend". Perusahaan ini sedang mengembangkan sistem pencatatan kehadiran untuk sekolah-sekolah di Indonesia. 

Saat ini, banyak sekolah masih menggunakan sistem absensi manual dengan tanda tangan di kertas, yang memakan waktu dan rawan kesalahan. SmartAttend ingin membuat solusi sederhana: **siswa cukup menunjukkan kartu identitas mereka ke kamera, dan sistem akan otomatis mengambil foto kartu tersebut, memproses informasi dasar, dan menyimpannya dengan format yang terstandar.**

### Skenario:
Sebagai tahap awal pengembangan, Anda diminta untuk membuat **prototype sistem capture kartu identitas** yang dapat:
1. Mengambil foto dari webcam atau file gambar
2. Melakukan crop/resize ke ukuran standar
3. Menambahkan timestamp dan watermark
4. Menyimpan dalam folder terorganisir
5. Membuat preview collage dari beberapa kartu

### Tantangan Real:
- Gambar dari kamera bisa dalam berbagai orientasi
- Pencahayaan mungkin tidak ideal
- Perlu standardisasi ukuran output
- Harus bisa running di berbagai OS (Windows/Linux/Mac)

---

## 🎯 TUJUAN PROJECT

1. **Mengaplikasikan** semua konsep dasar yang dipelajari di praktikum
2. **Mengintegrasikan** berbagai operasi gambar dalam satu sistem
3. **Memahami** workflow pemrosesan gambar dari input hingga output
4. **Membangun** fondasi untuk sistem computer vision yang lebih kompleks

---

## 📋 REQUIREMENTS & SPESIFIKASI

### Fitur Wajib (Minimum):
1. **[ ] Capture/Load Image**
   - Mampu load gambar dari file (jpg/png)
   - BONUS: Mampu capture dari webcam

2. **[ ] Image Processing Pipeline**
   - Resize gambar ke ukuran standar (400x250 piksel untuk kartu ID)
   - Konversi ke grayscale (untuk preview)
   - Adjust brightness/contrast dasar

3. **[ ] Annotation**
   - Tambahkan timestamp di pojok gambar
   - Tambahkan border/frame
   - BONUS: Tambahkan watermark "SmartAttend"

4. **[ ] Save Output**
   - Simpan dengan format: `YYYYMMDD_HHMMSS_kartu.jpg`
   - Organisasi folder berdasarkan tanggal

5. **[ ] Collage Generator**
   - Gabungkan 4 gambar kartu dalam 1 gambar (2x2 grid)
   - Tampilkan sebagai "Daily Summary"

### Fitur Bonus (Opsional):
- [ ] GUI sederhana menggunakan Tkinter
- [ ] Real-time preview dari webcam
- [ ] Deteksi orientasi kartu (portrait/landscape)
- [ ] Histogram equalization untuk gambar gelap

---

## 📁 STRUKTUR PROJECT

```
Project_Sistem_Kartu/
├── main.py                 # Program utama
├── capture_module.py       # Modul untuk capture gambar
├── process_module.py       # Modul untuk pemrosesan
├── utils.py               # Fungsi utilitas
├── config.py              # Konfigurasi (ukuran, path, dll)
│
├── input/                 # Folder untuk gambar input
│   └── sample_kartu.jpg
│
├── output/                # Folder untuk output
│   ├── 2024-01-15/       # Organisasi per tanggal
│   │   ├── 20240115_083045_kartu.jpg
│   │   └── ...
│   └── collages/         # Folder untuk collage
│       └── summary_2024-01-15.jpg
│
└── README.md             # Dokumentasi project
```

---

## 📝 INSTRUKSI PENGERJAAN

### Langkah 1: Setup Project (30 menit)
1. Buat folder project sesuai struktur di atas
2. Siapkan minimal 5 gambar kartu identitas (bisa KTP, kartu mahasiswa, kartu perpustakaan - SENSOR informasi sensitif!)
3. Buat file `config.py` dengan parameter dasar

### Langkah 2: Implementasi Core Features (2-3 jam)
1. Buat fungsi `load_image()` di `capture_module.py`
2. Buat fungsi `resize_standard()` di `process_module.py`
3. Buat fungsi `add_timestamp()` di `process_module.py`
4. Buat fungsi `save_with_organization()` di `utils.py`

### Langkah 3: Implementasi Collage (1 jam)
1. Buat fungsi `create_collage()` yang menggabungkan 4 gambar
2. Tambahkan judul dan tanggal di collage

### Langkah 4: Integrasi di main.py (30 menit)
1. Buat flow: Load → Process → Annotate → Save
2. Tambahkan menu sederhana di terminal

### Langkah 5: Testing & Dokumentasi (1 jam)
1. Test dengan berbagai gambar input
2. Dokumentasikan di README.md

---

## 🖼️ CONTOH OUTPUT YANG DIHARAPKAN

### Output Individual Card:
```
┌─────────────────────────────────┐
│  [Gambar Kartu yang di-resize]  │
│                                 │
│                                 │
│                                 │
├─────────────────────────────────┤
│ 📅 2024-01-15 08:30:45          │
│ SmartAttend System v1.0         │
└─────────────────────────────────┘
```

### Output Collage (2x2):
```
┌─────────────────────────────────────┐
│     DAILY SUMMARY: 2024-01-15       │
├────────────────┬────────────────────┤
│   Card #1      │      Card #2       │
│   08:30:45     │      09:15:22      │
├────────────────┼────────────────────┤
│   Card #3      │      Card #4       │
│   10:00:15     │      11:45:33      │
└────────────────┴────────────────────┘
```

---

## 🔍 KRITERIA PENILAIAN

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| **Fungsionalitas** | 40% | Semua fitur wajib berfungsi dengan baik |
| **Code Quality** | 20% | Kode terstruktur, ada komentar, mengikuti PEP8 |
| **Dokumentasi** | 15% | README lengkap, ada screenshot hasil |
| **Kreativitas** | 15% | Implementasi fitur bonus, ide tambahan |
| **Presentasi** | 10% | Mampu menjelaskan kode dan demo dengan baik |

### Breakdown Fungsionalitas (40%):
- Load/Capture Image: 8%
- Resize & Processing: 10%
- Annotation (timestamp, border): 8%
- Save dengan organisasi: 7%
- Collage Generator: 7%

---

## ⏰ DEADLINE & PENGUMPULAN

- **Waktu Pengerjaan**: 1 minggu
- **Format Pengumpulan**: ZIP file dengan format `NIM_Nama_Project1.zip`
- **Isi ZIP**:
  - Source code lengkap
  - README.md
  - Screenshot hasil (minimal 5)
  - Video demo singkat (2-3 menit)

---

## 💡 HINTS & TIPS

### Hint 1: Struktur config.py
```python
# config.py
CARD_WIDTH = 400
CARD_HEIGHT = 250
OUTPUT_QUALITY = 95
WATERMARK_TEXT = "SmartAttend v1.0"
```

### Hint 2: Membuat Timestamp
```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

### Hint 3: Membuat Grid Collage
```python
# Gunakan numpy untuk menggabungkan gambar
row1 = np.hstack([img1, img2])
row2 = np.hstack([img3, img4])
collage = np.vstack([row1, row2])
```

### Hint 4: Membuat Folder Otomatis
```python
import os
from datetime import datetime

folder = datetime.now().strftime("%Y-%m-%d")
os.makedirs(f"output/{folder}", exist_ok=True)
```

---

## ❓ FAQ

**Q: Boleh pakai gambar KTP asli?**
A: Boleh, tapi WAJIB sensor/blur semua informasi sensitif (NIK, alamat, dll)

**Q: Bagaimana jika tidak punya webcam?**
A: Gunakan mode load dari file saja, webcam adalah fitur bonus

**Q: Boleh menggunakan library tambahan?**
A: Boleh, selama library utama tetap OpenCV. Dokumentasikan di requirements.txt

**Q: Bagaimana menghitung aspect ratio?**
A: `aspect_ratio = width / height`. Kartu ID standar biasanya 85.6mm x 53.98mm (rasio ~1.586)

---

## 📚 REFERENSI TAMBAHAN

1. OpenCV Documentation: https://docs.opencv.org/
2. NumPy Array Operations: https://numpy.org/doc/
3. Python datetime: https://docs.python.org/3/library/datetime.html

---

**Selamat Mengerjakan! 🚀**

*"Perjalanan seribu mil dimulai dari satu langkah - dan langkah pertama Anda dalam Computer Vision dimulai dari sini!"*
