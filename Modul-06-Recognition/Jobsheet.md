# Jobsheet Bab 06: Recognition

## Informasi Umum

| Komponen | Keterangan |
|----------|------------|
| **Mata Kuliah** | Praktikum Computer Vision |
| **Bab** | 06 - Recognition |
| **Durasi** | 6 Pertemuan (@ 2-3 jam) |
| **Prasyarat** | Bab 01-05, Pemahaman Deep Learning |

---

## Pertemuan 1: Face Detection Methods

### Tujuan
- Memahami berbagai metode face detection
- Mengimplementasikan Haar Cascades dan HOG
- Menggunakan deep learning face detector

### Teori Singkat

Face detection adalah langkah pertama dalam pipeline face recognition. Metode utama:

1. **Haar Cascades** (Viola-Jones)
   - Cepat dan ringan
   - Kurang akurat untuk pose miring
   - Tersedia di OpenCV

2. **HOG + SVM**
   - Lebih robust terhadap pencahayaan
   - Digunakan oleh dlib
   - Medium speed

3. **Deep Learning**
   - MTCNN, RetinaFace, BlazeFace
   - Paling akurat
   - Memerlukan GPU untuk real-time

### Praktik

#### Latihan 1.1: Haar Cascade Detection
```python
# Jalankan: python 01_face_detection_opencv.py
# Pilih menu 1: Haar Cascade Detection
```

Eksperimen:
- [ ] Deteksi wajah pada gambar
- [ ] Ubah parameter scaleFactor (1.1, 1.2, 1.3)
- [ ] Ubah parameter minNeighbors (3, 4, 5, 6)
- [ ] Bandingkan hasil dengan frontal vs profile cascade

#### Latihan 1.2: HOG Face Detection
```python
# Jalankan: python 01_face_detection_opencv.py
# Pilih menu 2: HOG Detection
```

Eksperimen:
- [ ] Bandingkan kecepatan dengan Haar
- [ ] Test dengan berbagai orientasi wajah
- [ ] Catat jumlah deteksi benar dan salah

#### Latihan 1.3: Deep Learning Detection
```python
# Jalankan: python 02_face_detection_deep.py
```

Eksperimen:
- [ ] Test MTCNN detector
- [ ] Bandingkan akurasi dengan metode tradisional
- [ ] Ukur inference time

### Tugas Pertemuan 1

1. Buat tabel perbandingan metode deteksi:
   
| Metode | Accuracy | Speed | Robustness |
|--------|----------|-------|------------|
| Haar Cascade | | | |
| HOG + SVM | | | |
| MTCNN | | | |

2. Capture screenshot hasil deteksi untuk 3 gambar berbeda

---

## Pertemuan 2: Face Landmarks & Alignment

### Tujuan
- Memahami face landmarks dan kegunaannya
- Mengimplementasikan landmark detection
- Melakukan face alignment

### Teori Singkat

Face landmarks adalah titik-titik kunci pada wajah:
- 5 points: mata (2), hidung (1), mulut (2)
- 68 points: detail lengkap wajah (dlib standard)
- 478 points: MediaPipe Face Mesh

Kegunaan landmarks:
1. **Face Alignment**: Normalisasi pose sebelum recognition
2. **Expression Analysis**: Deteksi emosi
3. **Eye Tracking**: Gaze estimation
4. **Face Morphing**: Visual effects

### Praktik

#### Latihan 2.1: Landmark Detection
```python
# Jalankan: python 03_face_landmarks.py
# Pilih menu 1: Landmark Detection
```

Eksperimen:
- [ ] Visualisasi 5-point landmarks
- [ ] Visualisasi 68-point landmarks
- [ ] Identifikasi bagian wajah (mata, hidung, mulut, rahang)

#### Latihan 2.2: Face Alignment
```python
# Jalankan: python 03_face_landmarks.py
# Pilih menu 2: Face Alignment
```

Eksperimen:
- [ ] Align wajah yang miring ke kiri
- [ ] Align wajah yang miring ke kanan
- [ ] Bandingkan sebelum dan sesudah alignment

#### Latihan 2.3: Eye Detection
```python
# Jalankan: python 03_face_landmarks.py
# Pilih menu 3: Eye Detection
```

Eksperimen:
- [ ] Hitung Eye Aspect Ratio (EAR)
- [ ] Deteksi kedipan mata
- [ ] Implementasi drowsiness detection sederhana

### Tugas Pertemuan 2

1. Implementasikan face alignment untuk 5 gambar wajah yang berbeda orientasinya
2. Hitung dan visualisasikan EAR untuk sequence video pendek (5-10 detik)

---

## Pertemuan 3: Face Recognition Basics

### Tujuan
- Memahami konsep face embedding
- Mengimplementasikan feature extraction
- Melakukan face matching sederhana

### Teori Singkat

Face Recognition menggunakan embedding - vektor yang merepresentasikan wajah:

```
Face Image → CNN → Embedding (128-D atau 512-D)
```

Properti embedding yang baik:
- Wajah orang sama → vektor berdekatan (distance kecil)
- Wajah orang beda → vektor berjauhan (distance besar)

Model populer:
- FaceNet: 128-D embedding, triplet loss
- ArcFace: 512-D embedding, angular margin loss
- VGGFace: 2048-D features

### Praktik

#### Latihan 3.1: Feature Extraction
```python
# Jalankan: python 04_face_recognition.py
# Pilih menu 1: Feature Extraction
```

Eksperimen:
- [ ] Extract embedding dari gambar wajah
- [ ] Lihat dimensi dan statistik embedding
- [ ] Bandingkan embedding beberapa gambar

#### Latihan 3.2: Simple Matching
```python
# Jalankan: python 04_face_recognition.py
# Pilih menu 2: Face Matching
```

Eksperimen:
- [ ] Hitung jarak antara dua wajah orang sama
- [ ] Hitung jarak antara dua wajah orang berbeda
- [ ] Tentukan threshold yang optimal

#### Latihan 3.3: Distance Metrics
```python
# Jalankan: python 04_face_recognition.py
# Pilih menu 3: Distance Metrics
```

Eksperimen:
- [ ] Bandingkan Euclidean vs Cosine distance
- [ ] Plot distribusi jarak untuk same/different pairs
- [ ] Analisis mana metric yang lebih baik

### Tugas Pertemuan 3

1. Kumpulkan 5 gambar dari 3 orang berbeda (15 gambar total)
2. Extract embedding untuk semua gambar
3. Buat distance matrix dan analisis hasilnya

---

## Pertemuan 4: Face Database & Matching

### Tujuan
- Membangun database wajah
- Mengimplementasikan face verification (1:1)
- Mengimplementasikan face identification (1:N)

### Teori Singkat

**Verification (1:1)**:
```
Input: Probe image + Claimed ID
Output: Match / No Match
Process: Compare probe embedding dengan stored embedding untuk claimed ID
```

**Identification (1:N)**:
```
Input: Probe image + Database of N identities
Output: Best match identity (atau unknown)
Process: Compare probe dengan semua embeddings, return closest
```

### Praktik

#### Latihan 4.1: Face Verification
```python
# Jalankan: python 05_face_verification.py
```

Eksperimen:
- [ ] Setup verification system
- [ ] Test dengan same person (should match)
- [ ] Test dengan different person (should not match)
- [ ] Tune threshold

#### Latihan 4.2: Face Database
```python
# Jalankan: python 06_face_database.py
# Pilih menu 1: Enroll Faces
```

Eksperimen:
- [ ] Enroll minimal 5 identitas
- [ ] Simpan database ke file
- [ ] Load database dari file

#### Latihan 4.3: Face Identification
```python
# Jalankan: python 06_face_database.py
# Pilih menu 2: Identify Face
```

Eksperimen:
- [ ] Identifikasi wajah yang terdaftar
- [ ] Test dengan wajah yang tidak terdaftar
- [ ] Analisis confidence score

### Tugas Pertemuan 4

1. Bangun database dengan minimal 10 identitas
2. Implementasikan sistem attendance sederhana:
   - Enroll karyawan
   - Check-in dengan face verification
   - Log waktu attendance

---

## Pertemuan 5: OCR Implementation

### Tujuan
- Memahami OCR pipeline
- Mengimplementasikan text detection
- Melakukan text recognition

### Teori Singkat

OCR (Optical Character Recognition) pipeline:
```
Image → Text Detection → Text Recognition → Post-processing
```

Tools populer:
1. **Tesseract**: Open source, mendukung banyak bahasa
2. **EasyOCR**: Deep learning based, mudah digunakan
3. **PaddleOCR**: Akurat, multilingual

### Praktik

#### Latihan 5.1: Basic OCR
```python
# Jalankan: python 08_ocr_basic.py
```

Eksperimen:
- [ ] OCR pada dokumen cetak
- [ ] OCR pada teks tulisan tangan
- [ ] Bandingkan akurasi

#### Latihan 5.2: Scene Text Recognition
```python
# Jalankan: python 09_ocr_advanced.py
# Pilih menu 1: Scene Text
```

Eksperimen:
- [ ] Deteksi teks pada foto jalanan
- [ ] Deteksi teks pada produk
- [ ] Handle rotated text

#### Latihan 5.3: Document OCR
```python
# Jalankan: python 09_ocr_advanced.py
# Pilih menu 2: Document OCR
```

Eksperimen:
- [ ] OCR pada KTP/ID card (sample)
- [ ] OCR pada invoice/receipt
- [ ] Extract structured information

### Tugas Pertemuan 5

1. Implementasikan OCR untuk membaca plat nomor kendaraan
2. Buat system yang dapat:
   - Detect region plat nomor
   - Extract teks plat
   - Format output sesuai standar Indonesia

---

## Pertemuan 6: Real-time Recognition System

### Tujuan
- Mengintegrasikan semua komponen
- Membangun sistem real-time
- Optimasi performa

### Teori Singkat

Real-time recognition requirements:
- Processing speed: ≥15 FPS untuk smooth experience
- Latency: <200ms untuk responsif
- Accuracy: Balance dengan speed

Optimization techniques:
1. **Face Detection**: Use smaller model (BlazeFace)
2. **Skip Frames**: Process every N frames
3. **Tracking**: Use tracking between detections
4. **Batching**: Process multiple faces together

### Praktik

#### Latihan 6.1: Real-time Face Recognition
```python
# Jalankan: python 10_realtime_recognition.py
# Pilih menu 1: Real-time Recognition
```

Eksperimen:
- [ ] Setup webcam recognition
- [ ] Enroll faces secara real-time
- [ ] Test recognition accuracy
- [ ] Ukur FPS

#### Latihan 6.2: Performance Optimization
```python
# Jalankan: python 10_realtime_recognition.py
# Pilih menu 2: Optimization
```

Eksperimen:
- [ ] Test dengan skip frames (setiap 2, 3, 5 frame)
- [ ] Implement face tracking
- [ ] Bandingkan FPS sebelum dan sesudah optimasi

#### Latihan 6.3: Complete System
```python
# Jalankan: python 10_realtime_recognition.py
# Pilih menu 3: Complete System
```

Features:
- [ ] Face detection + recognition
- [ ] Unknown face handling
- [ ] Logging dan reporting
- [ ] Simple UI

### Tugas Pertemuan 6

1. Demo sistem recognition lengkap dengan:
   - Enrollment minimal 3 orang
   - Real-time recognition via webcam
   - Display nama dan confidence
   - Log ke file

2. Dokumentasikan:
   - Arsitektur sistem
   - Performance metrics
   - Limitations dan future improvements

---

## Penilaian Praktikum

### Komponen Penilaian

| Komponen | Bobot |
|----------|-------|
| Kehadiran & Partisipasi | 10% |
| Tugas Mingguan | 20% |
| Tugas Video | 30% |
| Project | 40% |

### Tugas Video

Buat video demonstrasi (10-15 menit) yang mencakup:

1. **Face Detection** (3 menit)
   - Demo berbagai metode
   - Perbandingan hasil

2. **Face Recognition** (4 menit)
   - Penjelasan embedding
   - Demo verification dan identification

3. **OCR** (3 menit)
   - Demo text detection dan recognition
   - Aplikasi praktis

4. **Real-time System** (3 menit)
   - Demo sistem lengkap
   - Performance analysis

### Project: FaceGuard

Bangun sistem absensi berbasis face recognition (detail di Project.md)

---

## Resources

### Library Documentation
- face_recognition: https://face-recognition.readthedocs.io/
- dlib: http://dlib.net/
- EasyOCR: https://github.com/JaidedAI/EasyOCR
- Tesseract: https://tesseract-ocr.github.io/

### Datasets untuk Testing
- LFW (Labeled Faces in the Wild)
- CelebA
- WiderFace

### Pre-trained Models
- dlib face recognition model
- FaceNet (facenet-pytorch)
- ArcFace (insightface)

---

## Troubleshooting

### Common Issues

1. **dlib installation gagal**
   ```bash
   # Install cmake first
   pip install cmake
   pip install dlib
   ```

2. **face_recognition tidak detect wajah**
   - Pastikan gambar cukup terang
   - Gunakan model='cnn' untuk akurasi lebih baik

3. **OCR hasil tidak akurat**
   - Preprocessing: grayscale, threshold
   - Atur DPI gambar (minimal 300 untuk dokumen)
   - Specify language dengan benar

4. **Real-time terlalu lambat**
   - Reduce input resolution
   - Skip frames
   - Use GPU jika tersedia

---

*Jobsheet ini adalah panduan praktikum untuk Bab 06 Recognition*
