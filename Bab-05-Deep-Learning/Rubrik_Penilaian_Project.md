# Rubrik Penilaian Project "DeepVision" - Bab 05 Deep Learning

## Informasi Umum

| Komponen | Deskripsi |
|----------|-----------|
| **Nama Project** | DeepVision - Sistem Klasifikasi Produk Otomatis |
| **Mata Kuliah** | Praktikum Computer Vision |
| **Bobot** | 40% dari nilai Bab 05 |
| **Waktu** | 5 Minggu |

---

## A. Modul 1: Product Classifier (30%)

### A.1. Implementasi Transfer Learning (15%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Pemilihan Model** | Memilih model pre-trained yang tepat (EfficientNet/MobileNet) dengan justifikasi yang kuat berdasarkan kebutuhan | Memilih model yang tepat dengan justifikasi cukup | Memilih model tanpa justifikasi yang jelas | Model tidak sesuai kebutuhan |
| **Fine-tuning Strategy** | Implementasi gradual unfreezing yang optimal, learning rate scheduling yang tepat | Fine-tuning dengan strategi standar, hasil cukup baik | Fine-tuning basic tanpa optimasi | Tidak melakukan fine-tuning dengan benar |
| **Data Preprocessing** | Pipeline preprocessing lengkap, normalization sesuai model, handling edge cases | Preprocessing standar dengan normalization | Preprocessing basic | Preprocessing tidak lengkap |
| **Code Quality** | Code clean, modular, dokumentasi lengkap, mengikuti best practices | Code terstruktur dengan dokumentasi memadai | Code berfungsi tapi kurang terstruktur | Code sulit dibaca dan tidak terstruktur |

**Skor A.1:** ____/16 × 15% = ____%

### A.2. Data Augmentation (8%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Variasi Augmentation** | Implementasi ≥5 teknik augmentation yang relevan (flip, rotate, color jitter, mixup, cutout) | 3-4 teknik augmentation yang relevan | 2 teknik augmentation | Hanya 1 atau tanpa augmentation |
| **Relevansi** | Semua augmentation relevan dengan domain produk retail | Sebagian besar relevan | Beberapa kurang relevan | Augmentation tidak relevan |

**Skor A.2:** ____/8 × 8% = ____%

### A.3. Evaluasi Model (7%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Akurasi** | Akurasi ≥95% pada test set | 90-94% | 80-89% | <80% |
| **Confusion Matrix** | Analisis confusion matrix lengkap dengan insight per class | Confusion matrix dengan analisis basic | Confusion matrix tanpa analisis | Tidak ada confusion matrix |
| **Inference Speed** | <50ms per image dengan dokumentasi benchmark | <100ms dengan benchmark | <200ms | >200ms atau tanpa benchmark |

**Skor A.3:** ____/12 × 7% = ____%

---

## B. Modul 2: Shelf Detector dengan YOLO (35%)

### B.1. Implementasi YOLO (15%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Model Selection** | Memilih variant YOLO yang optimal untuk use case dengan benchmark | Memilih variant yang sesuai dengan justifikasi | Menggunakan default tanpa pertimbangan | Variant tidak sesuai |
| **Configuration** | Konfigurasi confidence threshold, NMS threshold, dan input size yang optimal | Konfigurasi standar dengan hasil baik | Konfigurasi default | Konfigurasi menyebabkan masalah |
| **Integration** | Integrasi smooth dengan pipeline product classifier | Integrasi berfungsi dengan minor issues | Integrasi dengan beberapa masalah | Integrasi gagal |
| **Real-time Performance** | ≥30 FPS dengan deteksi stabil | 20-29 FPS | 10-19 FPS | <10 FPS |

**Skor B.1:** ____/16 × 15% = ____%

### B.2. Custom Training (Opsional, Bonus +10%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Dataset Preparation** | Dataset minimal 500 images dengan label berkualitas | 300-499 images, label cukup baik | 100-299 images | <100 images |
| **Training Process** | Training dengan hyperparameter tuning, early stopping, augmentation | Training standar dengan hasil baik | Training basic | Training gagal/overfit |
| **mAP Score** | mAP@50 ≥ 80% | 70-79% | 60-69% | <60% |

**Skor B.2 (Bonus):** ____/12 × 10% = ____%

### B.3. Post-processing (10%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **NMS Implementation** | Custom NMS dengan threshold tuning untuk menghindari duplicate | NMS standar dengan hasil baik | NMS basic | Tanpa NMS atau tidak berfungsi |
| **Filtering Logic** | Filter berdasarkan confidence, class, dan area yang relevan | Filter confidence dan class | Filter confidence saja | Tanpa filtering |
| **Visualization** | Visualisasi bbox, label, confidence dengan design yang informatif | Visualisasi standar lengkap | Visualisasi basic | Visualisasi tidak lengkap |

**Skor B.3:** ____/12 × 10% = ____%

### B.4. Shelf Analysis (10%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Product Counting** | Counting akurat dengan tracking untuk menghindari double count | Counting dengan akurasi tinggi | Counting dengan beberapa error | Counting tidak akurat |
| **Position Analysis** | Analisis posisi produk di rak (kiri/tengah/kanan, atas/bawah) | Analisis posisi basic | Analisis minimal | Tidak ada analisis posisi |
| **Alert System** | Sistem alert untuk stok rendah, produk salah posisi | Alert untuk stok rendah | Alert basic | Tanpa sistem alert |

**Skor B.4:** ____/12 × 10% = ____%

---

## C. Modul 3: Deployment Pipeline (35%)

### C.1. ONNX Export (12%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Export Process** | Export kedua model (classifier + detector) dengan opset optimal | Export berhasil dengan opset standar | Export satu model saja | Export gagal |
| **Validation** | Validasi output ONNX vs original model dengan tolerance check | Validasi basic | Tanpa validasi formal | Output berbeda signifikan |
| **Optimization** | Model dioptimasi (graph optimization, quantization) | Optimasi standar | Tanpa optimasi | - |

**Skor C.1:** ____/12 × 12% = ____%

### C.2. OpenCV DNN Integration (13%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **Loading & Inference** | Model berhasil di-load dan inference dengan OpenCV DNN | Inference berfungsi dengan minor issues | Inference dengan beberapa error | Inference gagal |
| **Performance** | Speed comparable dengan ONNX Runtime (<20% slower) | <50% slower | <100% slower | Terlalu lambat untuk praktis |
| **Cross-platform** | Tested di Windows, Linux, atau Mac | Tested di 1 platform selain development | Development platform saja | Tidak tested |

**Skor C.2:** ____/12 × 13% = ____%

### C.3. Complete Pipeline (10%)

| Kriteria | Sangat Baik (4) | Baik (3) | Cukup (2) | Kurang (1) |
|----------|-----------------|----------|-----------|------------|
| **End-to-End Flow** | Pipeline lengkap dari input → detection → classification → output | Pipeline berfungsi dengan manual steps | Pipeline partial | Pipeline tidak berfungsi |
| **Error Handling** | Error handling comprehensive dengan logging | Error handling untuk common cases | Error handling basic | Tanpa error handling |
| **Documentation** | API documentation, usage examples, troubleshooting guide | Documentation cukup lengkap | README basic | Dokumentasi minimal |

**Skor C.3:** ____/12 × 10% = ____%

---

## D. Deliverables Quality (Bonus/Penalty)

### D.1. Code Quality

| Aspek | Bonus | Penalty |
|-------|-------|---------|
| **Clean Code** | +5% untuk code yang sangat clean dan modular | -5% untuk code yang sulit dibaca |
| **Testing** | +3% untuk unit tests | -3% untuk tanpa testing sama sekali |
| **Version Control** | +2% untuk git history yang clean | -2% untuk single commit |

### D.2. Documentation

| Aspek | Bonus | Penalty |
|-------|-------|---------|
| **Technical Report** | +5% untuk report yang sangat detailed | -5% untuk report yang tidak lengkap |
| **Demo Video** | +3% untuk video demo yang profesional | -3% untuk tanpa video demo |

### D.3. Presentation

| Aspek | Bonus | Penalty |
|-------|-------|---------|
| **Live Demo** | +5% untuk live demo yang sukses | -5% untuk demo yang gagal |
| **Q&A** | +3% untuk menjawab pertanyaan dengan baik | -3% untuk tidak bisa menjawab pertanyaan |

---

## Perhitungan Nilai Akhir

### Formula

```
Nilai Akhir = (A + B + C) + Bonus - Penalty

Dimana:
A = Skor Modul 1 (max 30%)
B = Skor Modul 2 (max 35% + 10% bonus custom training)
C = Skor Modul 3 (max 35%)
Bonus = Max 26%
Penalty = Varies
```

### Konversi ke Huruf

| Range | Grade |
|-------|-------|
| ≥ 85% | A |
| 80-84% | A- |
| 75-79% | B+ |
| 70-74% | B |
| 65-69% | B- |
| 60-64% | C+ |
| 55-59% | C |
| 50-54% | C- |
| 40-49% | D |
| < 40% | E |

---

## Lembar Penilaian

### Identitas Mahasiswa

| Field | Value |
|-------|-------|
| Nama | |
| NIM | |
| Kelompok | |
| Tanggal Pengumpulan | |
| Tanggal Penilaian | |

### Rekap Nilai

| Komponen | Skor | Bobot | Nilai |
|----------|------|-------|-------|
| A.1 Transfer Learning | /16 | 15% | |
| A.2 Data Augmentation | /8 | 8% | |
| A.3 Evaluasi Model | /12 | 7% | |
| **Total Modul 1** | | **30%** | |
| B.1 Implementasi YOLO | /16 | 15% | |
| B.2 Custom Training (Bonus) | /12 | 10% | |
| B.3 Post-processing | /12 | 10% | |
| B.4 Shelf Analysis | /12 | 10% | |
| **Total Modul 2** | | **35%+** | |
| C.1 ONNX Export | /12 | 12% | |
| C.2 OpenCV DNN | /12 | 13% | |
| C.3 Complete Pipeline | /12 | 10% | |
| **Total Modul 3** | | **35%** | |
| **Subtotal** | | | |
| Bonus | | | + |
| Penalty | | | - |
| **NILAI AKHIR** | | | |
| **GRADE** | | | |

### Catatan Penilai

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

### Tanda Tangan

| | |
|---|---|
| Penilai | Mahasiswa |
| | |
| Nama: _________________ | Nama: _________________ |
| Tanggal: _______________ | Tanggal: _______________ |

---

*Rubrik ini digunakan untuk menilai Project DeepVision pada Bab 05 Deep Learning untuk Computer Vision*
