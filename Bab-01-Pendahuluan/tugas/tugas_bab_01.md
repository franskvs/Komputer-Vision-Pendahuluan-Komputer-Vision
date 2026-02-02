# TUGAS BAB 1: PENDAHULUAN COMPUTER VISION

## 📋 Informasi Tugas

| Aspek | Detail |
|-------|--------|
| **Deadline** | 1 minggu setelah praktikum |
| **Format** | Jupyter Notebook (.ipynb) atau Python (.py) + Laporan PDF |
| **Pengumpulan** | Melalui platform e-learning |

---

## Tugas 1: Essay - Pemahaman Computer Vision (20 poin)

### Instruksi
Tulis essay singkat (500-700 kata) yang menjawab pertanyaan berikut:

1. **Jelaskan mengapa computer vision disebut sebagai "inverse problem"?** 
   - Berikan contoh konkret
   - Apa kesulitan yang muncul dari sifat ini?

2. **Bandingkan pendekatan tradisional (feature-based) dengan pendekatan deep learning dalam computer vision**
   - Sebutkan minimal 3 perbedaan utama
   - Kapan sebaiknya menggunakan masing-masing pendekatan?

3. **Pilih satu aplikasi computer vision yang menurut Anda paling berdampak**
   - Jelaskan bagaimana aplikasi tersebut bekerja secara umum
   - Apa tantangan teknis yang dihadapi?

### Kriteria Penilaian
- Kedalaman pemahaman konsep (40%)
- Kemampuan mengaitkan teori dengan praktik (30%)
- Kejelasan penulisan (20%)
- Referensi yang digunakan (10%)

---

## Tugas 2: Coding - Operasi Dasar Citra (40 poin)

### Instruksi
Buat program Python yang melakukan hal-hal berikut:

### 2.1 Fungsi Image Info (10 poin)
```python
def image_info(image_path):
    """
    Fungsi untuk menampilkan informasi lengkap tentang citra
    
    Parameter:
        image_path: string, path ke file citra
    
    Output yang harus ditampilkan:
        - Nama file
        - Dimensi (width x height)
        - Jumlah channel
        - Tipe data
        - Ukuran file (KB)
        - Nilai minimum, maksimum, dan rata-rata pixel
        - Mode warna (grayscale/RGB/RGBA)
    """
    # Implementasi Anda di sini
    pass
```

### 2.2 Fungsi Image Transformation (15 poin)
```python
def transform_image(image, operation, **params):
    """
    Fungsi untuk melakukan transformasi pada citra
    
    Parameter:
        image: numpy array, citra input
        operation: string, jenis operasi ('brightness', 'contrast', 
                   'negative', 'grayscale', 'threshold')
        params: parameter tambahan sesuai operasi
    
    Return:
        numpy array: citra hasil transformasi
    
    Contoh penggunaan:
        result = transform_image(img, 'brightness', value=50)
        result = transform_image(img, 'contrast', factor=1.5)
        result = transform_image(img, 'threshold', thresh=127)
    """
    # Implementasi Anda di sini
    pass
```

### 2.3 Fungsi Histogram Analysis (15 poin)
```python
def analyze_histogram(image):
    """
    Fungsi untuk menganalisis histogram citra
    
    Parameter:
        image: numpy array, citra input
    
    Output:
        - Plot citra dan histogramnya
        - Statistik: mean, std, median, mode
        - Klasifikasi otomatis: 'dark', 'bright', 'normal', 'low_contrast', 'high_contrast'
        - Rekomendasi enhancement yang diperlukan
    
    Return:
        dict: berisi statistik dan analisis
    """
    # Implementasi Anda di sini
    pass
```

---

## Tugas 3: Mini Project - Image Enhancement Tool (40 poin)

### Deskripsi
Buat aplikasi sederhana untuk melakukan image enhancement dengan fitur-fitur berikut:

### Requirements

1. **Input/Output** (10 poin)
   - Bisa membaca citra dari file
   - Bisa menyimpan citra hasil
   - Mendukung format umum (JPG, PNG, BMP)

2. **Operasi Enhancement** (20 poin)
   - Brightness adjustment
   - Contrast adjustment
   - Histogram equalization
   - Auto-enhancement (berdasarkan analisis histogram)
   - Negative image
   - Konversi grayscale

3. **Visualisasi** (10 poin)
   - Tampilan before-after
   - Histogram sebelum dan sesudah
   - Statistik perubahan

### Template Kode

```python
"""
Mini Project: Image Enhancement Tool
Nama: [Nama Anda]
NIM: [NIM Anda]
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

class ImageEnhancer:
    def __init__(self, image_path=None):
        """Initialize dengan path citra atau None"""
        self.original = None
        self.current = None
        self.history = []  # Untuk undo
        
        if image_path:
            self.load(image_path)
    
    def load(self, image_path):
        """Load citra dari file"""
        # Implementasi Anda
        pass
    
    def save(self, output_path):
        """Simpan citra hasil ke file"""
        # Implementasi Anda
        pass
    
    def adjust_brightness(self, value):
        """Adjust brightness dengan value tertentu"""
        # Implementasi Anda
        pass
    
    def adjust_contrast(self, factor):
        """Adjust contrast dengan factor tertentu"""
        # Implementasi Anda
        pass
    
    def histogram_equalization(self):
        """Lakukan histogram equalization"""
        # Implementasi Anda
        pass
    
    def auto_enhance(self):
        """
        Auto enhancement berdasarkan analisis histogram
        - Jika terlalu gelap: brighten
        - Jika kontras rendah: increase contrast
        - dll
        """
        # Implementasi Anda
        pass
    
    def to_negative(self):
        """Konversi ke citra negatif"""
        # Implementasi Anda
        pass
    
    def to_grayscale(self):
        """Konversi ke grayscale"""
        # Implementasi Anda
        pass
    
    def reset(self):
        """Reset ke citra original"""
        # Implementasi Anda
        pass
    
    def show_comparison(self):
        """Tampilkan perbandingan original vs current"""
        # Implementasi Anda
        pass
    
    def show_histogram(self):
        """Tampilkan histogram original dan current"""
        # Implementasi Anda
        pass


# Main program
if __name__ == "__main__":
    # Demonstrasi penggunaan
    enhancer = ImageEnhancer("sample_image.jpg")
    
    # Tampilkan info awal
    print("=== Image Info ===")
    # ...
    
    # Lakukan enhancement
    enhancer.adjust_brightness(30)
    enhancer.adjust_contrast(1.2)
    
    # Tampilkan perbandingan
    enhancer.show_comparison()
    
    # Simpan hasil
    enhancer.save("enhanced_image.jpg")
```

### Kriteria Penilaian Mini Project

| Kriteria | Poin |
|----------|------|
| Kode berjalan tanpa error | 10 |
| Semua fungsi diimplementasi | 10 |
| Hasil enhancement terlihat baik | 10 |
| Kode rapi dan terdokumentasi | 5 |
| Fitur tambahan (bonus) | +5 |

---

## Bonus Challenge (Opsional, +10 poin)

Implementasikan salah satu dari berikut:

1. **Interactive Mode**: Buat interface command-line yang interaktif
2. **Batch Processing**: Proses banyak citra sekaligus
3. **GUI sederhana**: Menggunakan tkinter atau PyQt
4. **Filter artistik**: Sepia, vignette, dll

---

## Rubrik Penilaian Total

| Komponen | Poin |
|----------|------|
| Tugas 1: Essay | 20 |
| Tugas 2: Coding Dasar | 40 |
| Tugas 3: Mini Project | 40 |
| **Total** | **100** |
| Bonus | +10 |

---

## Ketentuan Pengumpulan

1. **Nama file**: `Tugas1_NIM_Nama.zip`
2. **Isi ZIP**:
   - `essay.pdf` - Jawaban Tugas 1
   - `tugas2.py` atau `tugas2.ipynb` - Jawaban Tugas 2
   - `mini_project/` - Folder berisi Tugas 3
   - `README.md` - Penjelasan cara menjalankan kode

3. **Keterlambatan**: -10 poin per hari

---

## Tips Pengerjaan

1. Mulai dengan memahami materi dan praktikum terlebih dahulu
2. Gunakan sample images dari `skimage.data` jika tidak punya citra sendiri
3. Test kode Anda dengan berbagai jenis citra
4. Dokumentasikan kode dengan baik (comments, docstrings)
5. Simpan progress secara berkala (gunakan git jika bisa)

---

**Selamat mengerjakan!** 🎉
