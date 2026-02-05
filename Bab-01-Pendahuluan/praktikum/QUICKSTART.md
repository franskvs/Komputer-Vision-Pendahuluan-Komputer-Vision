# QUICK START GUIDE - BAB 1 PENDAHULUAN

## ⚡ LANGKAH CEPAT (5 MENIT)

### 1️⃣ Setup Images (Pertama Kali Saja)
```bash
cd "Bab-01-Pendahuluan/praktikum"
python3 setup_images.py
```
✅ Output: Gambar di `data/images/`

---

### 2️⃣ Test Semua Program (Opsional - Verifikasi)
```bash
python3 run_all_tests.py
```
✅ Output: Verification report + output files

---

### 3️⃣ Jalankan Program Individual
```bash
# Program dasar:

# Loading gambar
python3 01_loading_gambar.py

# Menampilkan gambar
python3 02_menampilkan_gambar.py

# Properti gambar
python3 03_properti_gambar.py

# Konversi warna
python3 04_konversi_warna.py

# Manipulasi piksel
python3 05_manipulasi_piksel.py

# Menggambar shapes
python3 06_menggambar_shapes.py

# Menyimpan output
python3 07_menyimpan_output.py
```

---

## 📂 LIHAT HASIL

Semua output tersimpan di:
```
output/
├── output1/  ← Loading gambar
├── output2/  ← Display gambar
├── output3/  ← Properti gambar
├── output4/  ← Konversi warna
├── output5/  ← Manipulasi piksel
├── output6/  ← Drawing shapes
└── output7/  ← Menyimpan output
```

---

## 🎯 PROGRAM FAVORIT (MUST TRY)

| Program | File | Wow Factor | Deskripsi |
|---------|------|------------|-----------|
| **Drawing Shapes** | `06_menggambar_shapes.py` | ⭐⭐⭐⭐⭐ | Visualisasi |
| **Konversi Warna** | `04_konversi_warna.py` | ⭐⭐⭐⭐ | Color spaces |
| **Manipulasi Piksel** | `05_manipulasi_piksel.py` | ⭐⭐⭐⭐ | Array operations |
| **Properti Gambar** | `03_properti_gambar.py` | ⭐⭐⭐ | Analisis dasar |

---

## 🔥 DEMO UNTUK PRESENTASI

### Demo 1: Drawing dan Anotasi
```bash
python3 06_menggambar_shapes.py
```
**Output:** Gambar dengan berbagai shapes dan teks

### Demo 2: Color Space Conversion
```bash
python3 04_konversi_warna.py
```
**Output:** Perbandingan RGB, Grayscale, HSV, LAB

### Demo 3: Pixel Manipulation
```bash
python3 05_manipulasi_piksel.py
```
**Output:** ROI extraction, color manipulation

---

## 🎨 GAMBAR YANG TERSEDIA

| Image | Ukuran | Best For | Deskripsi |
|-------|--------|----------|-----------|
| `portrait.jpg` | 640px | Programs 1-5 | Gambar wajah |
| `landscape.jpg` | 640px | Programs 3-4 | Pemandangan |
| `building.jpg` | 640px | Program 6 | Bangunan |
| `colorful.jpg` | 640px | Program 4 | Warna-warni |
| `checkerboard.png` | 400px | All programs | Pattern test |

---

## ⚠️ TROUBLESHOOTING

### Error "No module named cv2"
```bash
pip install opencv-python numpy matplotlib
```

### Gambar tidak ditemukan
```bash
python3 setup_images.py
```

### Window tidak muncul
Program menyimpan output ke folder, buka file hasil di folder output/
