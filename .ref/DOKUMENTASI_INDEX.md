# INDEX DOKUMENTASI PRAKTIKUM COMPUTER VISION

## 📚 PANDUAN CEPAT MENGGUNAKAN DOKUMENTASI

### Jika Anda...

#### 1. **Ingin Belajar Function cv2.putText()**
**Lokasi:** `CV2_FUNCTIONS_REFERENCE.py` → Cari "cv2.putText"
- Dokumentasi lengkap 8 parameter (a sampai h)
- Contoh penggunaan berbeda-beda
- Penjelasan format BGR untuk warna

#### 2. **Ingin Lihat Contoh Lengkap Drawing Functions**
**Lokasi:** `06_menggambar_shapes_ENHANCED.py` (di Bab-01)
- Demo cv2.line() dengan 5 contoh berbeda
- Demo cv2.rectangle() dengan 5 contoh berbeda
- Demo cv2.circle() dengan 5 contoh berbeda
- Demo cv2.putText() dengan 6 contoh berbeda
- Setiap function dijelaskan parameter-nya secara detail

#### 3. **Ingin Referensi cv2.imread()**
**Lokasi:** `CV2_FUNCTIONS_REFERENCE.py` → Cari "cv2.imread"
- Penjelasan 2 parameter (filename, flags)
- Mode pembacaan: COLOR, GRAYSCALE, UNCHANGED
- Contoh penggunaan

#### 4. **Ingin Referensi cv2.cvtColor()**
**Lokasi:** `CV2_FUNCTIONS_REFERENCE.py` → Cari "cv2.cvtColor"
- Penjelasan 2 parameter (src, code)
- Berbagai mode konversi (BGR→RGB, BGR→GRAY, BGR→HSV, dll)
- Contoh: Gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)

#### 5. **Ingin Referensi cv2.resize()**
**Lokasi:** `CV2_FUNCTIONS_REFERENCE.py` → Cari "cv2.resize"
- Penjelasan 3 parameter (src, dsize, interpolation)
- Metode interpolasi terbaik untuk berbagai kasus
- Contoh penggunaan

#### 6. **Ingin Referensi cv2.findContours() atau cv2.drawContours()**
**Lokasi:** `CV2_FUNCTIONS_REFERENCE.py` → Bagian "CONTOUR FUNCTIONS"
- Penjelasan mode dan method
- Contoh penggunaan untuk deteksi objek
- Penjelasan binary image requirements

---

## 🎯 DAFTAR LENGKAP FUNCTIONS DI CV2_FUNCTIONS_REFERENCE.py

### Input/Output Functions
- `cv2.imread(filename, flags)` - Membaca gambar dari file
- `cv2.imwrite(filename, img)` - Menyimpan gambar ke file
- `cv2.imshow(winname, mat)` - Menampilkan gambar di window
- `cv2.waitKey(delay)` - Menunggu input keyboard
- `cv2.destroyAllWindows()` - Menutup semua window

### Drawing Functions ⭐ (Paling Sering Dipakai)
- `cv2.line(img, pt1, pt2, color, thickness, lineType)` ⭐⭐⭐
- `cv2.rectangle(img, pt1, pt2, color, thickness)` ⭐⭐⭐
- `cv2.circle(img, center, radius, color, thickness)` ⭐⭐⭐
- `cv2.ellipse(...)` - Menggambar elips
- `cv2.putText(...)` ⭐⭐⭐ **PALING DETAIL - 8 PARAMETER DIJELASKAN**
- `cv2.polylines(...)` - Menggambar polygon

### Color Conversion Functions
- `cv2.cvtColor(src, code)` - Konversi antar color space
- `cv2.inRange(src, lowerb, upperb)` - Membuat mask warna

### Geometric Transformation Functions
- `cv2.resize(src, dsize, interpolation)` - Mengubah ukuran gambar
- `cv2.warpAffine(src, M, dsize)` - Transformasi affine
- `cv2.warpPerspective(src, M, dsize)` - Transformasi perspektif

### Filtering Functions
- `cv2.blur(src, ksize)` - Blur sederhana
- `cv2.GaussianBlur(src, ksize, sigma)` - Gaussian blur
- `cv2.filter2D(src, ddepth, kernel)` - Custom kernel convolution

### Edge Detection Functions
- `cv2.Canny(image, threshold1, threshold2)` - Canny edge detector
- `cv2.Sobel(src, ddepth, dx, dy, ksize)` - Sobel edge detector

### Contour Functions
- `cv2.findContours(image, mode, method)` - Menemukan kontur
- `cv2.drawContours(image, contours, contourIdx, color, thickness)` - Menggambar kontur

---

## 📁 STRUKTUR DIREKTORI DOKUMENTASI

```
Praktikum Komputer Vision/
├── DOKUMENTASI_ENHANCEMENT_SUMMARY.md  ← File ini memberikan overview
│
└── Bab-01-Pendahuluan/praktikum/
    ├── CV2_FUNCTIONS_REFERENCE.py       ← REFERENSI LENGKAP (ada di semua bab)
    ├── 06_menggambar_shapes_ENHANCED.py ← TEMPLATE ENHANCED (contoh detail)
    ├── 01_loading_gambar.py
    ├── 02_menampilkan_gambar.py
    ├── ... (dan program lainnya)
    
├── Bab-02-Pembentukan-Citra/praktikum/
    ├── CV2_FUNCTIONS_REFERENCE.py       ← COPY dari Bab-01
    ├── (program-program)
    
├── Bab-03-Pemrosesan-Citra/praktikum/
    ├── CV2_FUNCTIONS_REFERENCE.py
    ├── (program-program)

... (Bab-04 hingga Bab-14 dengan struktur sama)
```

---

## 💡 TIPS BELAJAR

### Tips 1: Pahami Format BGR, Bukan RGB
OpenCV menggunakan format BGR:
- `(255, 0, 0)` = BIRU (B=255, G=0, R=0)
- `(0, 255, 0)` = HIJAU
- `(0, 0, 255)` = MERAH
- `(255, 255, 255)` = PUTIH

Jangan lupa saat menampilkan di matplotlib, konversi terlebih dahulu!

### Tips 2: Parameter Koordinat (x, y)
- `x` = horizontal (dari kiri ke kanan)
- `y` = vertical (dari atas ke bawah)
- Origin `(0, 0)` ada di KIRI ATAS

Contoh:
```python
# Titik di (100, 50) = 100 pixel dari kiri, 50 pixel dari atas
cv2.circle(gambar, (100, 50), 10, (255, 0, 0), -1)
```

### Tips 3: Ketebalan -1 untuk Filled
Pada semua drawing functions (rectangle, circle, dll):
- `thickness=1` atau lebih: Hanya outline (garis tepi)
- `thickness=-1`: Diisi penuh dengan warna

Contoh:
```python
# Rectangle outline
cv2.rectangle(gambar, (50, 50), (200, 150), (0, 255, 0), 2)

# Rectangle filled
cv2.rectangle(gambar, (50, 50), (200, 150), (0, 255, 0), -1)
```

### Tips 4: cv2.putText() Menggunakan Posisi BAWAH KIRI
Koordinat pada cv2.putText() adalah posisi BAWAH KIRI dari teks:
```python
# Teks "Hello" akan ditampilkan dengan sudut bawah kiri di (50, 100)
cv2.putText(gambar, "Hello", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
```

### Tips 5: Eksperimen dengan Mengubah Parameter
Jangan hanya membaca - **coba ubah parameter** dan lihat hasilnya!

Contoh eksperimen untuk `cv2.line()`:
```python
# Eksperimen 1: Ubah warna
cv2.line(gambar, (0, 0), (100, 100), (255, 0, 0), 2)  # Biru
cv2.line(gambar, (0, 0), (100, 100), (0, 255, 0), 2)  # Hijau
cv2.line(gambar, (0, 0), (100, 100), (0, 0, 255), 2)  # Merah

# Eksperimen 2: Ubah ketebalan
cv2.line(gambar, (0, 0), (100, 100), (0, 0, 255), 1)  # Tipis
cv2.line(gambar, (0, 0), (100, 100), (0, 0, 255), 5)  # Tebal

# Eksperimen 3: Ubah jenis garis
cv2.line(gambar, (0, 0), (100, 100), (0, 0, 255), 2, cv2.LINE_AA)   # Smooth
cv2.line(gambar, (0, 0), (100, 100), (0, 0, 255), 2, cv2.LINE_8)    # Normal
```

---

## ❓ FAQ - PERTANYAAN UMUM

**Q: Saya tidak mengerti parameter cv2.putText, kemana saya harus lihat?**
A: Buka `CV2_FUNCTIONS_REFERENCE.py`, cari bagian "cv2.putText". Ada penjelasan lengkap untuk 8 parameter (a sampai h) dengan contoh.

**Q: Bagaimana saya tahu warna apa dalam format BGR?**
A: Lihat bagian "COLOR FORMAT" di `CV2_FUNCTIONS_REFERENCE.py`. Ada tabel lengkap warna BGR.

**Q: Saya ingin lihat contoh bagaimana menggunakan cv2.line(), cv2.rectangle(), dll?**
A: Buka `06_menggambar_shapes_ENHANCED.py` di Bab-01. File ini menunjukkan contoh lengkap untuk setiap function.

**Q: Apakah saya harus download data terlebih dahulu?**
A: Sebagian bab memiliki data sample. Jalankan `download_sample_data.py` di folder bab tersebut untuk download data.

**Q: Program saya error, bagaimana cara debug?**
A: 
1. Baca error message dengan seksama
2. Cek dokumentasi function yang error di `CV2_FUNCTIONS_REFERENCE.py`
3. Pastikan parameter-parameter sesuai dokumentasi
4. Coba lihat contoh di file ENHANCED

---

## 📞 KONTAK & DUKUNGAN

Jika ada pertanyaan tentang dokumentasi atau program praktikum, silakan:
1. Cek `CV2_FUNCTIONS_REFERENCE.py` terlebih dahulu
2. Lihat contoh di `06_menggambar_shapes_ENHANCED.py`
3. Baca `DOKUMENTASI_ENHANCEMENT_SUMMARY.md` untuk overview

---

**Selamat Belajar!** 🚀

Dokumentasi ini dibuat untuk memudahkan pembelajaran Computer Vision dengan OpenCV.
Jangan ragu untuk eksperimen dan coba mengubah parameter-parameter!

