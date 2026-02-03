# PROJECT BAB 7: DETEKSI FITUR DAN PENCOCOKAN

## 🎯 SISTEM PENGENALAN KARTU IDENTITAS (ID Card Recognition System)

---

## 📖 LATAR BELAKANG

Sebuah perusahaan keamanan **"SecureGate Indonesia"** ingin mengembangkan sistem verifikasi kartu identitas otomatis untuk gedung perkantoran. Sistem ini akan digunakan di pintu masuk gedung untuk memverifikasi bahwa kartu yang ditunjukkan pengunjung adalah kartu asli yang terdaftar dalam database.

**Masalah yang dihadapi:**
- Verifikasi manual memakan waktu lama (rata-rata 30 detik per orang)
- Satpam kesulitan mendeteksi kartu palsu
- Antrian panjang saat jam sibuk
- Risiko human error tinggi

**Solusi yang diharapkan:**
Sistem berbasis computer vision yang dapat mengenali dan memverifikasi kartu identitas dalam waktu kurang dari 3 detik dengan akurasi minimal 95%.

---

## 🎯 TUJUAN PROJECT

### Tujuan Utama:
Mengembangkan sistem pengenalan kartu identitas menggunakan teknik feature detection dan matching.

### Tujuan Khusus:
1. Mendeteksi dan mengekstrak fitur dari kartu identitas template
2. Mencocokkan kartu yang di-scan dengan template di database
3. Menentukan apakah kartu valid atau tidak berdasarkan similarity score
4. Memberikan feedback visual hasil verifikasi

---

## 📋 DESKRIPSI TUGAS

### Skenario:
Anda adalah programmer di **SecureGate Indonesia**. Tim Anda ditugaskan untuk membuat **prototype** sistem verifikasi kartu. Prototype ini harus dapat:

1. **Registrasi Kartu Baru:**
   - Mengambil foto kartu identitas
   - Mengekstrak dan menyimpan fitur kartu ke database

2. **Verifikasi Kartu:**
   - Mengambil foto kartu yang akan diverifikasi
   - Mencocokkan dengan kartu di database
   - Menampilkan hasil: **VERIFIED** atau **REJECTED**

3. **Laporan:**
   - Menampilkan similarity score
   - Menunjukkan visualisasi matching points
   - Log waktu proses

---

## 📝 SPESIFIKASI TEKNIS

### Input:
- Gambar kartu identitas (dapat berupa KTP, kartu mahasiswa, atau kartu karyawan)
- Minimal 3 kartu berbeda untuk testing
- Gambar harus beresolusi minimal 640x480 pixel

### Output:
1. **Database kartu** (folder berisi gambar dan file fitur)
2. **Hasil verifikasi** dengan informasi:
   - Status: VERIFIED / REJECTED
   - Similarity Score (0-100%)
   - Jumlah matched features
   - Waktu proses (ms)
3. **Visualisasi** matched features

### Kriteria Keberhasilan:
| Kriteria | Target |
|----------|--------|
| Akurasi verifikasi kartu valid | ≥ 95% |
| Akurasi penolakan kartu invalid | ≥ 90% |
| Waktu proses per kartu | < 3 detik |
| False Positive Rate | < 5% |

---

## 🔧 FITUR YANG HARUS DIIMPLEMENTASIKAN

### Fitur Wajib (80 poin):

1. **Mode Registrasi** (20 poin)
   - Input dari webcam atau file gambar
   - Ekstraksi fitur menggunakan ORB atau SIFT
   - Penyimpanan fitur ke file/database

2. **Mode Verifikasi** (30 poin)
   - Input kartu untuk verifikasi
   - Matching dengan semua kartu di database
   - Penentuan threshold untuk VERIFIED/REJECTED
   - Tampilan hasil yang jelas

3. **Visualisasi Matching** (15 poin)
   - Menampilkan garis penghubung antar matched features
   - Menandai inliers dengan warna berbeda

4. **User Interface Sederhana** (15 poin)
   - Menu untuk memilih mode
   - Feedback yang jelas untuk user

### Fitur Tambahan (20 poin bonus):

1. **Multi-card Database** (5 poin)
   - Dapat menyimpan banyak kartu
   - Pencarian otomatis kartu yang cocok

2. **Real-time Webcam** (5 poin)
   - Verifikasi langsung dari webcam
   - Frame rate minimal 10 FPS

3. **Anti-spoofing Sederhana** (5 poin)
   - Deteksi jika kartu hanya foto dari layar HP
   - Hint: Gunakan deteksi moire pattern

4. **Report Generation** (5 poin)
   - Generate laporan PDF/HTML
   - Statistik penggunaan

---

## 📊 DATA YANG DIGUNAKAN

### Opsi 1: Kartu Buatan Sendiri
- Buat kartu identitas sederhana (desain bebas)
- Print atau gunakan secara digital
- Minimal 3 kartu berbeda

### Opsi 2: Kartu Asli (Disensor)
- Gunakan kartu mahasiswa/karyawan sendiri
- **WAJIB** sensor informasi pribadi (NIK, alamat, dll)
- Hanya gunakan untuk testing, tidak disebarkan

### Opsi 3: Kartu Template
- Download template kartu dari internet
- Modifikasi dengan informasi dummy

---

## 📁 STRUKTUR PROJECT

```
project_id_card_recognition/
├── main.py                 # Program utama
├── card_register.py        # Modul registrasi kartu
├── card_verify.py          # Modul verifikasi
├── feature_extractor.py    # Ekstraksi fitur
├── database/
│   ├── cards/              # Gambar kartu terdaftar
│   └── features/           # File fitur tersimpan
├── test_images/
│   ├── valid_cards/        # Kartu untuk testing valid
│   └── invalid_cards/      # Kartu untuk testing invalid
├── output/
│   ├── results/            # Hasil verifikasi
│   └── visualizations/     # Visualisasi matching
└── README.md               # Dokumentasi
```

---

## 📝 LANGKAH PENGERJAAN

### Tahap 1: Persiapan (Hari 1)
1. Buat struktur folder project
2. Siapkan minimal 5 kartu untuk testing:
   - 3 kartu untuk registrasi
   - 2 kartu untuk testing (1 valid, 1 invalid)
3. Install dependencies yang diperlukan

### Tahap 2: Implementasi Core (Hari 2-3)
1. Implementasi ekstraksi fitur
2. Implementasi penyimpanan ke database
3. Implementasi matching algorithm
4. Testing dengan gambar statis

### Tahap 3: Implementasi UI (Hari 4)
1. Buat menu interaktif
2. Implementasi mode registrasi
3. Implementasi mode verifikasi
4. Tambahkan visualisasi

### Tahap 4: Testing & Dokumentasi (Hari 5)
1. Testing dengan berbagai kondisi
2. Tuning threshold optimal
3. Buat dokumentasi/README
4. Record demo video

---

## 🎥 DEMO YANG HARUS DITUNJUKKAN

Buat video demo (3-5 menit) yang menunjukkan:

1. **Registrasi kartu baru**
   - Tunjukkan proses registrasi 2 kartu berbeda
   - Tampilkan fitur yang terdeteksi

2. **Verifikasi kartu valid**
   - Gunakan kartu yang sudah terdaftar
   - Tunjukkan status VERIFIED dan score

3. **Verifikasi kartu invalid**
   - Gunakan kartu yang tidak terdaftar
   - Tunjukkan status REJECTED dan alasannya

4. **Visualisasi matching**
   - Tampilkan matched features
   - Jelaskan mengapa match/tidak match

---

## 📊 RUBRIK PENILAIAN

| Komponen | Bobot | Kriteria |
|----------|-------|----------|
| **Fungsionalitas** | 40% | Program berjalan sesuai spesifikasi |
| **Akurasi** | 20% | Memenuhi target akurasi |
| **Kode** | 20% | Clean code, well-documented |
| **Dokumentasi** | 10% | README lengkap, mudah diikuti |
| **Demo Video** | 10% | Jelas, lengkap, profesional |

### Detail Penilaian Fungsionalitas:
| Fitur | Poin |
|-------|------|
| Registrasi kartu berhasil | 10 |
| Ekstraksi fitur benar | 10 |
| Matching berjalan | 10 |
| Verifikasi akurat | 10 |
| Visualisasi bagus | 5 |
| UI berfungsi | 5 |
| Fitur bonus | +20 |

---

## ⚠️ CATATAN PENTING

1. **Privasi:** Jangan gunakan kartu identitas asli tanpa sensor
2. **Original Work:** Plagiarisme akan mendapat nilai 0
3. **Deadline:** Kumpulkan sesuai jadwal yang ditentukan
4. **Format:** ZIP folder lengkap dengan semua file

---

## 💡 HINTS DAN TIPS

### Tip 1: Threshold Optimal
```python
# Mulai dengan threshold ini, lalu tune
MATCH_THRESHOLD = 0.75  # Untuk ratio test
MIN_MATCH_COUNT = 10    # Minimal matched features
SIMILARITY_THRESHOLD = 60  # Persentase untuk VERIFIED
```

### Tip 2: Preprocessing
```python
# Preprocessing dapat meningkatkan akurasi
img = cv2.resize(img, (640, 480))
img = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

### Tip 3: Database Structure
```python
# Simpan fitur sebagai pickle file
import pickle
data = {'keypoints': kp, 'descriptors': desc}
with open('card_001.pkl', 'wb') as f:
    pickle.dump(data, f)
```

### Tip 4: Evaluation
```python
# Hitung similarity score
similarity = (num_good_matches / total_features) * 100
```

---

## 📚 REFERENSI YANG BERGUNA

1. OpenCV Feature Matching Tutorial
2. ORB Documentation
3. RANSAC Homography Tutorial
4. Materi Praktikum Bab 7

---

**Selamat mengerjakan! 💪**

*"The best way to learn is by doing."*
