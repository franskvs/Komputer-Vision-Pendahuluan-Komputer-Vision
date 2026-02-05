# BAB 1: PENDAHULUAN - PRAKTIKUM
## Computer Vision - Introduction to OpenCV

### 📋 RINGKASAN

Praktikum ini mencakup **7 program** yang mendemonstrasikan konsep-konsep dasar dalam Computer Vision menggunakan OpenCV, mulai dari loading gambar hingga menyimpan output.

**Status:** ✅ **PROGRAM TERVERIFIKASI**
- **7 programs** untuk pembelajaran dasar OpenCV
- Output tersimpan di folder `output/`

---

### 🎯 STRUKTUR PRAKTIKUM

#### 1. **Input/Output Gambar** (Programs 01-02)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 01 | Loading Gambar | cv2.imread() | Membaca file gambar |
| 02 | Menampilkan Gambar | cv2.imshow(), matplotlib | Visualisasi gambar |

#### 2. **Properti dan Konversi** (Programs 03-04)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 03 | Properti Gambar | Shape, dtype, channels | Analisis gambar |
| 04 | Konversi Warna | cvtColor() | Preprocessing gambar |

#### 3. **Manipulasi dan Drawing** (Programs 05-06)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 05 | Manipulasi Piksel | Indexing, slicing | Editing gambar |
| 06 | Menggambar Shapes | line, rectangle, circle | Anotasi gambar |

#### 4. **Output** (Program 07)
| No | Program | Konsep | Penerapan Nyata |
|----|---------|--------|-----------------|
| 07 | Menyimpan Output | cv2.imwrite() | Export hasil |

---

### 🚀 CARA MENJALANKAN

#### Setup Awal (Hanya Sekali)
```bash
# 1. Generate/download semua gambar untuk praktikum
python3 setup_images.py

# Output: Gambar di folder data/images/
```

#### Menjalankan Program Individual
```bash
# Contoh: Jalankan program loading gambar
python3 01_loading_gambar.py

# Output akan tersimpan di: output/output1/
```

#### Automated Testing (Semua Program Sekaligus)
```bash
# Test semua program secara otomatis
python3 run_all_tests.py

# Output: 
# - Verification report
# - Execution statistics
```

---

### 📁 STRUKTUR DIREKTORI

```
Bab-01-Pendahuluan/praktikum/
│
├── data/
│   └── images/               # Gambar praktikum
│       ├── portrait.jpg      # Gambar wajah
│       ├── landscape.jpg     # Pemandangan
│       ├── building.jpg      # Bangunan
│       └── ...
│
├── output/
│   ├── output1/             # Hasil program 01
│   ├── output2/             # Hasil program 02
│   └── ...
│
├── 01_loading_gambar.py     # Program 1
├── 02_menampilkan_gambar.py # Program 2
├── 03_properti_gambar.py    # Program 3
├── 04_konversi_warna.py     # Program 4
├── 05_manipulasi_piksel.py  # Program 5
├── 06_menggambar_shapes.py  # Program 6
├── 07_menyimpan_output.py   # Program 7
│
├── CV2_FUNCTIONS_REFERENCE.py  # Referensi fungsi OpenCV
├── setup_images.py             # Setup gambar
├── run_all_tests.py            # Test runner
├── README.md                   # Dokumentasi ini
└── QUICKSTART.md               # Panduan cepat
```

---

### 📚 KONSEP YANG DIPELAJARI

1. **cv2.imread()** - Membaca gambar dari file
2. **cv2.imshow()** - Menampilkan gambar di window
3. **cv2.imwrite()** - Menyimpan gambar ke file
4. **cv2.cvtColor()** - Konversi color space
5. **cv2.line(), cv2.rectangle(), cv2.circle()** - Drawing shapes
6. **cv2.putText()** - Menambahkan teks
7. **numpy array indexing** - Manipulasi piksel

---

### 🔧 TROUBLESHOOTING

**Q: Gambar tidak ditemukan?**
```bash
# Jalankan setup terlebih dahulu
python3 setup_images.py
```

**Q: Error "No module named cv2"?**
```bash
pip install opencv-python numpy matplotlib
```

**Q: Window tidak muncul (headless server)?**
- Program menggunakan matplotlib dengan backend 'Agg'
- Output tersimpan otomatis ke folder output/

---

### 📖 REFERENSI

- [OpenCV Documentation](https://docs.opencv.org/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- File: `CV2_FUNCTIONS_REFERENCE.py` - Dokumentasi fungsi lengkap
