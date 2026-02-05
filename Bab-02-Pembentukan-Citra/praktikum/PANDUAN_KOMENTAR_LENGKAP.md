# PANDUAN PENULISAN KOMENTAR LENGKAP UNTUK SEMUA PROGRAM

## Filosofi Komentar yang Baik
Setiap baris kode harus bisa dipahami oleh pemula yang belajar computer vision untuk pertama kali. Komentar harus menjelaskan:
1. **APA** yang dilakukan (fungsi/operasi)
2. **MENGAPA** dilakukan (tujuan/alasan)
3. **BAGAIMANA** cara kerjanya (mekanisme)
4. **PARAMETER** setiap fungsi dengan detail

---

## Format Standar Komentar

### 1. Header Program
```python
# ============================================================
# PROGRAM: [Nama Program]
# PRAKTIKUM COMPUTER VISION - BAB 2: PEMBENTUKAN CITRA
# ============================================================
# Deskripsi: [Penjelasan singkat apa yang dilakukan program]
# 
# Tujuan Pembelajaran:
#   1. [Tujuan 1]
#   2. [Tujuan 2]
#   3. [Tujuan 3]
# ============================================================
```

### 2. Import Library
```python
# ====================
# IMPORT LIBRARY
# ====================
# cv2: OpenCV untuk computer vision dan image processing
import cv2
# numpy: untuk operasi array, matrix, dan matematika
import numpy as np
# matplotlib: untuk plotting dan visualisasi
import matplotlib
matplotlib.use('Agg')  # Gunakan backend Agg (non-GUI) untuk automated testing
import matplotlib.pyplot as plt
```

### 3. Dokumentasi Fungsi OpenCV (WAJIB)
Setiap fungsi OpenCV yang digunakan HARUS dijelaskan parameter-parameternya:

```python
# ============================================================
# PANDUAN FUNGSI OPENCV - PENJELASAN DETAIL
# ============================================================
# cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType)
#   img: gambar yang akan ditambahkan teks (numpy array BGR)
#   text: string teks yang akan ditampilkan
#   org: (x, y) koordinat bottom-left dari teks
#   fontFace: jenis font, misal cv2.FONT_HERSHEY_SIMPLEX
#   fontScale: ukuran font (float), misal 0.5, 1.0, 2.0
#   color: warna dalam format BGR, misal (255, 0, 0) = biru
#   thickness: ketebalan huruf (int), misal 1, 2, 3
#   lineType: tipe garis (opsional), cv2.LINE_AA = anti-aliased
#   Return: None (modifikasi langsung pada img)
#
# cv2.rectangle(img, pt1, pt2, color, thickness)
#   img: gambar yang akan digambar persegi
#   pt1: (x, y) titik sudut kiri-atas
#   pt2: (x, y) titik sudut kanan-bawah
#   color: warna BGR, misal (0, 255, 0) = hijau
#   thickness: ketebalan garis, -1 untuk isi penuh (filled)
#   Return: None (modifikasi langsung)
#
# cv2.circle(img, center, radius, color, thickness)
#   img: gambar yang akan digambar lingkaran
#   center: (x, y) koordinat pusat lingkaran
#   radius: jari-jari dalam piksel (int)
#   color: warna BGR
#   thickness: ketebalan garis, -1 untuk isi penuh
#   Return: None (modifikasi langsung)
#
# cv2.warpAffine(src, M, dsize, flags, borderMode, borderValue)
#   src: gambar sumber (input) yang akan ditransformasi
#   M: matriks transformasi affine 2x3
#   dsize: (width, height) ukuran gambar output
#   flags: metode interpolasi, cv2.INTER_LINEAR = bilinear
#   borderMode: mode pengisian area kosong di tepi
#   borderValue: warna untuk area kosong (jika BORDER_CONSTANT)
#   Return: gambar hasil transformasi
#
# cv2.warpPerspective(src, M, dsize, flags, borderMode, borderValue)
#   src: gambar sumber (input)
#   M: matriks transformasi perspektif 3x3
#   dsize: (width, height) ukuran output
#   flags: metode interpolasi
#   borderMode: mode border
#   borderValue: warna border
#   Return: gambar hasil transformasi perspektif
#
# cv2.getPerspectiveTransform(src, dst)
#   src: 4 titik sumber (numpy array 4x2)
#   dst: 4 titik tujuan (numpy array 4x2)
#   Return: matriks transformasi perspektif 3x3
#
# cv2.resize(img, dsize, fx, fy, interpolation)
#   img: gambar input
#   dsize: (width, height) ukuran baru, atau None jika pakai fx/fy
#   fx: faktor skala horizontal (misal 0.5 = 50%, 2.0 = 200%)
#   fy: faktor skala vertikal
#   interpolation: cv2.INTER_LINEAR, INTER_CUBIC, INTER_NEAREST
#   Return: gambar yang sudah di-resize
#
# cv2.cvtColor(img, code)
#   img: gambar input
#   code: kode konversi warna, misal cv2.COLOR_BGR2RGB, COLOR_BGR2GRAY
#   Return: gambar dengan color space baru
#
# cv2.imread(path, flags)
#   path: string path lokasi file gambar
#   flags: cv2.IMREAD_COLOR (default, BGR), IMREAD_GRAYSCALE, dll
#   Return: numpy array gambar atau None jika gagal
#
# cv2.imwrite(filename, img, params)
#   filename: nama file output
#   img: gambar yang akan disimpan (numpy array)
#   params: parameter tambahan (opsional), misal kualitas JPEG
#   Return: True jika berhasil, False jika gagal
```

### 4. Variabel yang Bisa Diubah (Eksperimen)
```python
# ============================================================
# VARIABEL YANG BISA DIUBAH-UBAH (EKSPERIMEN)
# ============================================================

# 1. File gambar yang akan diproses
NAMA_FILE_GAMBAR = "portrait.jpg"  # Coba ubah: "cameraman.jpg", "building.jpg"

# 2. Parameter transformasi
TX = 100  # Translasi horizontal: positif=kanan, negatif=kiri
TY = 50   # Translasi vertikal: positif=bawah, negatif=atas

# 3. Mode border
#    cv2.BORDER_CONSTANT: Warna solid
#    cv2.BORDER_REPLICATE: Duplikasi piksel tepi
#    cv2.BORDER_REFLECT: Pantulan cermin
MODE_BORDER = cv2.BORDER_CONSTANT

# 4. Warna border (BGR format)
WARNA_BORDER = (50, 50, 50)  # Abu-abu gelap
```

### 5. Komentar untuk Operasi Array
```python
# Buat matriks translasi 2x3
# Format: [[1, 0, tx], [0, 1, ty]]
# Persamaan: x' = x + tx, y' = y + ty
M = np.float32([
    [1, 0, tx],  # Baris 1: transformasi x (x' = 1*x + 0*y + tx)
    [0, 1, ty]   # Baris 2: transformasi y (y' = 0*x + 1*y + ty)
])

# Buat array kosong dengan ukuran 400x600, 3 channels, tipe uint8 (0-255)
# dtype=uint8: unsigned integer 8-bit untuk menyimpan nilai warna
img = np.zeros((400, 600, 3), dtype=np.uint8)

# Ambil dimensi gambar
# shape mengembalikan tuple (height, width, channels)
h, w = img.shape[:2]  # [:2] ambil hanya height dan width, abaikan channels
```

### 6. Komentar untuk Loop
```python
# Loop untuk setiap baris gambar (dari atas ke bawah)
for i in range(tinggi):
    # Loop untuk setiap kolom (dari kiri ke kanan)
    for j in range(lebar):
        # Hitung nilai piksel berdasarkan posisi
        # Koordinat (j, i) dalam format (x, y)
        nilai = fungsi_hitung(i, j)
        
        # Set nilai piksel pada posisi [i, j]
        # Format: img[row, col, channel]
        gambar[i, j] = nilai
```

### 7. Komentar untuk Matplotlib
```python
# Buat figure dengan 2 baris x 3 kolom = 6 subplots
# figsize=(15, 10): lebar 15 inch, tinggi 10 inch
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Flatten axes dari 2D menjadi 1D untuk kemudahan akses
# Sebelum: axes[row][col], Sesudah: axes[i]
axes = axes.flatten()

# Tampilkan gambar pada subplot pertama
# imshow: menampilkan array numpy sebagai gambar
# cmap='gray': gunakan colormap grayscale (untuk gambar hitam-putih)
axes[0].imshow(gambar_rgb)

# Set judul subplot
axes[0].set_title("Judul Gambar", fontsize=12)

# Nonaktifkan sumbu untuk tampilan lebih bersih
axes[0].axis('off')

# Simpan figure ke file
# dpi=150: resolusi 150 dots per inch
# bbox_inches='tight': otomatis crop whitespace di pinggir
plt.savefig("output.png", dpi=150, bbox_inches='tight')

# Tutup figure untuk menghemat memori
plt.close()
```

---

## Fungsi OpenCV yang Sering Dipakai

### Geometric Transformations
```python
# cv2.warpAffine(src, M, dsize, ...)
#   Transformasi affine (preserves parallelism)
#   M: matriks 2x3
#   Use case: translasi, rotasi, scaling, shearing

# cv2.warpPerspective(src, M, dsize, ...)
#   Transformasi perspektif (projects 3D to 2D)
#   M: matriks 3x3
#   Use case: perspective correction, bird's eye view

# cv2.getRotationMatrix2D(center, angle, scale)
#   Buat matriks rotasi 2D
#   center: (x, y) titik pusat rotasi
#   angle: sudut rotasi dalam derajat (positif=CCW)
#   scale: faktor scaling (1.0 = ukuran asli)
#   Return: matriks affine 2x3

# cv2.getPerspectiveTransform(src, dst)
#   Buat matriks perspektif dari 4 pasangan titik
#   src/dst: numpy array 4x2 (4 titik, 2 koordinat)
```

### Drawing Functions
```python
# cv2.line(img, pt1, pt2, color, thickness, lineType)
# cv2.rectangle(img, pt1, pt2, color, thickness)
# cv2.circle(img, center, radius, color, thickness)
# cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)
# cv2.polylines(img, pts, isClosed, color, thickness)
# cv2.putText(img, text, org, fontFace, fontScale, color, thickness)
```

### Color Space Conversions
```python
# cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    # OpenCV BGR → Matplotlib RGB
# cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # BGR → Grayscale
# cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # BGR → HSV
# cv2.cvtColor(img, cv2.COLOR_BGR2LAB)    # BGR → LAB
# cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)  # BGR → YCrCb
```

### Image Processing
```python
# cv2.GaussianBlur(img, ksize, sigmaX)
#   ksize: (width, height) kernel size (harus ganjil)
#   sigmaX: standard deviation di arah X

# cv2.Canny(img, threshold1, threshold2)
#   Edge detection
#   threshold1/2: hysteresis thresholds

# cv2.dilate(img, kernel, iterations)
#   Morphological dilation
#   kernel: structuring element

# cv2.erode(img, kernel, iterations)
#   Morphological erosion
```

---

## Checklist Komentar yang Baik

Untuk setiap program, pastikan sudah ada:

- [ ] Header program dengan deskripsi dan tujuan pembelajaran
- [ ] Komentar import library
- [ ] Dokumentasi lengkap fungsi OpenCV yang dipakai
- [ ] Variabel yang bisa diubah dengan penjelasan range/opsi
- [ ] Komentar untuk setiap fungsi (docstring)
- [ ] Komentar inline untuk operasi penting (matrix, loop, dll)
- [ ] Penjelasan parameter untuk SETIAP fungsi call
- [ ] Penjelasan return value dan tipe data
- [ ] Contoh nilai untuk parameter yang tidak jelas
- [ ] Ringkasan output di bagian akhir

---

## Contoh Lengkap: cv2.putText()

### ❌ Komentar Buruk
```python
cv2.putText(img, "Hello", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
```

### ✅ Komentar Baik
```python
# Tambahkan teks "Hello" pada gambar
# Parameter:
#   img: gambar tujuan
#   "Hello": string yang ditampilkan
#   (50, 50): koordinat (x=50, y=50) bottom-left teks
#   FONT_HERSHEY_SIMPLEX: jenis font (clean, readable)
#   1: font scale (ukuran)
#   (255, 0, 0): warna BGR (biru penuh)
#   2: thickness (ketebalan) huruf
cv2.putText(img, "Hello", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
```

### 🌟 Komentar Sangat Baik (Recommended)
```python
# Tambahkan label teks pada gambar untuk identifikasi
# cv2.putText(img, text, org, fontFace, fontScale, color, thickness)
#   img: gambar yang akan ditambahkan teks (dimodifikasi langsung)
#   text: "Hello" = string yang ditampilkan
#   org: (50, 50) = koordinat bottom-left teks (x=50 dari kiri, y=50 dari atas)
#   fontFace: FONT_HERSHEY_SIMPLEX = font simple dan mudah dibaca
#   fontScale: 1 = ukuran normal (coba 0.5 lebih kecil, 2 lebih besar)
#   color: (255, 0, 0) = BGR format (B=255 biru penuh, G=0, R=0)
#   thickness: 2 = ketebalan huruf dalam piksel
cv2.putText(img, "Hello", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
```

---

## Tips Menulis Komentar Efektif

1. **Gunakan Bahasa Indonesia** untuk memudahkan pembelajaran
2. **Jelaskan MENGAPA**, bukan hanya APA
3. **Berikan contoh nilai** untuk parameter yang abstrak
4. **Hindari komentar redundan** seperti `x = x + 1  # tambah x dengan 1`
5. **Fokus pada parameter yang tidak obvious**
6. **Gunakan visualisasi ASCII** untuk konsep matematis
7. **Tambahkan referensi** ke dokumentasi atau paper jika perlu

---

## Template Fungsi dengan Komentar Lengkap

```python
def nama_fungsi(parameter1, parameter2, parameter3=default):
    """Penjelasan singkat fungsi dalam 1 kalimat.
    
    Penjelasan lebih detail tentang apa yang dilakukan fungsi ini,
    bagaimana cara kerjanya, dan use case yang cocok.
    
    Parameter:
    - parameter1 (tipe): penjelasan parameter 1
    - parameter2 (tipe): penjelasan parameter 2
    - parameter3 (tipe, optional): penjelasan parameter 3 (default: nilai_default)
    
    Return:
    - tipe: penjelasan return value
    
    Contoh penggunaan:
    >>> hasil = nama_fungsi(value1, value2)
    >>> print(hasil)
    """
    # Validasi input
    # Pastikan parameter1 tidak None
    if parameter1 is None:
        raise ValueError("parameter1 tidak boleh None")
    
    # Proses utama
    # Lakukan operasi A pada parameter1
    hasil_intermediate = operasi_a(parameter1)
    
    # Gabungkan dengan parameter2 menggunakan metode B
    hasil_final = operasi_b(hasil_intermediate, parameter2)
    
    # Terapkan parameter3 jika berbeda dari default
    if parameter3 != default:
        hasil_final = modifikasi(hasil_final, parameter3)
    
    # Kembalikan hasil
    return hasil_final
```

---

## Referensi Tambahan

- OpenCV Documentation: https://docs.opencv.org/
- NumPy Documentation: https://numpy.org/doc/
- Matplotlib Documentation: https://matplotlib.org/

---

**Catatan Penting:**
Program yang BAIK adalah program yang bisa dipahami oleh orang lain (atau diri sendiri 6 bulan kemudian) tanpa perlu bertanya. Komentar yang lengkap adalah investasi untuk pembelajaran yang lebih efektif!
