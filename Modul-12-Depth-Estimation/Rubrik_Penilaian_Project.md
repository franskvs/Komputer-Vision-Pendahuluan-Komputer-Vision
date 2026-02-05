# RUBRIK PENILAIAN PROJECT
## BAB 12: DEPTH ESTIMATION - AUTONOMOUS VEHICLE DEPTH PERCEPTION

---

## 📊 Ringkasan Bobot Penilaian

| Komponen | Bobot | Deskripsi |
|----------|-------|-----------|
| Stereo Pipeline | 35% | Kalibrasi, rectification, disparity |
| Depth Module | 25% | Depth conversion, post-processing |
| Obstacle Detection | 20% | Ground plane, clustering |
| Integration & Visualization | 20% | Real-time, dashboard |
| **Total** | **100%** | |

---

## 📋 Rubrik Detail per Komponen

### 1. Stereo Pipeline Implementation (35%)

#### 1.1 Stereo Calibration Module (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **Implementasi Kalibrasi** | Kalibrasi lengkap dengan corner detection akurat, multiple orientations, validasi otomatis | Kalibrasi berfungsi dengan baik, minimal 20 gambar | Kalibrasi berfungsi, hasil tidak optimal | Tidak berfungsi |
| **RMS Error** | < 0.3 pixel | 0.3-0.5 pixel | 0.5-1.0 pixel | > 1.0 pixel |
| **Parameter Export** | YAML/XML dengan semua parameter intrinsik dan extrinsik, format bersih | Export berfungsi, format cukup baik | Export partial | Tidak ada export |
| **Dokumentasi** | Komentar lengkap, cara penggunaan jelas | Dokumentasi cukup | Dokumentasi minimal | Tidak ada |

#### 1.2 Stereo Rectification Pipeline (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **Implementasi Rectification** | Rectification sempurna, epipolar lines horizontal, distortion removed | Rectification baik, sedikit residual error | Rectification partial | Tidak berfungsi |
| **Validasi** | Visualisasi epipolar lines, error metrics computed | Validasi visual ada | Validasi minimal | Tidak ada validasi |
| **Robustness** | Handle berbagai resolusi, edge cases | Handle resolusi standar | Hanya resolusi tertentu | Tidak robust |

#### 1.3 Disparity Computation (15%)

| Aspek | Excellent (13-15) | Good (10-12) | Fair (7-9) | Poor (0-6) |
|-------|------------------|--------------|------------|------------|
| **Multiple Methods** | BM dan SGM dengan parameter tuning optimal | Kedua metode berfungsi | Satu metode berfungsi | Tidak berfungsi |
| **Post-processing** | WLS filtering, speckle removal, hole filling | Post-processing dasar | Minimal post-processing | Tidak ada |
| **Kualitas Output** | Disparity smooth, edges preserved, minimal noise | Kualitas baik | Kualitas cukup | Banyak noise |
| **Perbandingan** | Analisis kuantitatif dan kualitatif lengkap | Perbandingan visual | Perbandingan minimal | Tidak ada |

---

### 2. Depth Estimation Module (25%)

#### 2.1 Disparity to Depth Conversion (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **Konversi Akurat** | Depth dalam meter, formula benar, validasi dengan ground truth | Konversi benar, unit tepat | Konversi berfungsi | Tidak akurat |
| **Invalid Handling** | Handle inf, NaN, negative disparity dengan baik | Handle kasus dasar | Partial handling | Tidak ada handling |
| **Akurasi** | Error < 5% pada range 1-15m | Error < 10% | Error < 20% | Error > 20% |

#### 2.2 Depth Map Post-Processing (15%)

| Aspek | Excellent (13-15) | Good (10-12) | Fair (7-9) | Poor (0-6) |
|-------|------------------|--------------|------------|------------|
| **Hole Filling** | Interpolasi cerdas, mempertahankan edge | Hole filling dasar | Partial filling | Tidak ada |
| **Temporal Filtering** | Stabilitas antar frame, minimal flickering | Filtering sederhana | Minimal filtering | Tidak stabil |
| **Edge Preservation** | Bilateral/guided filter, edges tajam | Edges cukup baik | Edges blurry | Tidak ada perhatian |
| **Noise Reduction** | Noise removed tanpa kehilangan detail | Noise reduction cukup | Masih banyak noise | Sangat noisy |

---

### 3. Obstacle Detection (20%)

#### 3.1 Ground Plane Estimation (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **RANSAC Implementation** | RANSAC robust, convergence cepat, handle outliers | RANSAC berfungsi | Implementasi dasar | Tidak berfungsi |
| **Plane Accuracy** | Ground plane akurat dalam berbagai kondisi | Akurat di kondisi standar | Kadang tidak akurat | Tidak reliable |
| **Segmentation** | Ground vs non-ground tersegmentasi dengan baik | Segmentasi cukup | Banyak misclassification | Tidak berfungsi |

#### 3.2 Obstacle Clustering (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **Clustering Method** | Euclidean clustering atau DBSCAN dengan parameter optimal | Clustering berfungsi | Clustering sederhana | Tidak ada |
| **Bounding Boxes** | 3D bounding boxes akurat, size estimation | 2D boxes atau 3D partial | Boxes tidak akurat | Tidak ada |
| **Distance Calculation** | Jarak ke obstacle akurat, minimum distance computed | Jarak cukup akurat | Jarak approximate | Tidak akurat |
| **False Positive Rate** | < 5% | 5-15% | 15-30% | > 30% |

---

### 4. Integration & Visualization (20%)

#### 4.1 Real-time Pipeline (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **Frame Rate** | > 20 fps pada GPU, > 10 fps CPU | > 15 fps | > 10 fps | < 10 fps |
| **Memory Management** | Tidak ada memory leak, efisien | Cukup efisien | Ada minor issues | Memory leak |
| **Integration Quality** | Pipeline seamless, error handling robust | Integration baik | Ada masalah minor | Banyak bug |
| **Code Quality** | Clean, modular, well-documented | Cukup clean | Code messy | Tidak readable |

#### 4.2 Visualization Dashboard (10%)

| Aspek | Excellent (9-10) | Good (7-8) | Fair (5-6) | Poor (0-4) |
|-------|-----------------|------------|------------|------------|
| **RGB + Depth Overlay** | Depth colormap pada RGB, transparency adjustable | Overlay berfungsi | Overlay basic | Tidak ada |
| **Bird's Eye View** | BEV dengan obstacle positions, grid overlay | BEV sederhana | BEV minimal | Tidak ada |
| **Warning System** | Audio/visual warning untuk obstacle dekat | Warning visual | Warning basic | Tidak ada |
| **UI Quality** | Professional, responsive, keyboard shortcuts | UI baik | UI functional | UI jelek |

---

## 📝 Rubrik Deliverables

### Source Code (40% dari total nilai)

| Kriteria | Excellent (36-40) | Good (28-35) | Fair (20-27) | Poor (0-19) |
|----------|------------------|--------------|--------------|-------------|
| **Functionality** | Semua fitur berfungsi sempurna | Sebagian besar berfungsi | Fitur utama berfungsi | Banyak error |
| **Code Quality** | Clean code, DRY principle, SOLID | Cukup bersih | Ada redundancy | Sangat messy |
| **Documentation** | Docstrings lengkap, README comprehensive | Dokumentasi cukup | Dokumentasi minimal | Tidak ada |
| **Error Handling** | Try-except lengkap, graceful degradation | Error handling cukup | Handling minimal | Tidak ada |
| **Testing** | Unit tests, integration tests | Beberapa tests | Testing minimal | Tidak ada |

### Demo Video (20% dari total nilai)

| Kriteria | Excellent (18-20) | Good (14-17) | Fair (10-13) | Poor (0-9) |
|----------|------------------|--------------|--------------|------------|
| **Durasi** | 5-7 menit, pace tepat | Sedikit over/under | Durasi tidak sesuai | Jauh dari target |
| **Konten** | Semua fitur ditunjukkan | Sebagian besar fitur | Fitur utama saja | Tidak lengkap |
| **Kualitas Video** | HD, audio jelas, editing baik | Kualitas baik | Kualitas cukup | Kualitas buruk |
| **Narasi** | Bahasa Indonesia baik, jelas, informatif | Narasi cukup | Narasi minimal | Tidak jelas |

### Technical Report (25% dari total nilai)

| Kriteria | Excellent (22-25) | Good (18-21) | Fair (13-17) | Poor (0-12) |
|----------|------------------|--------------|--------------|-------------|
| **Format** | IEEE format sempurna, max 10 halaman | Format cukup baik | Format tidak konsisten | Tidak mengikuti format |
| **Methodology** | Metodologi jelas, reproducible | Cukup jelas | Kurang detail | Tidak jelas |
| **Results** | Hasil lengkap, tabel/grafik informatif | Hasil cukup | Hasil minimal | Tidak ada hasil |
| **Analysis** | Analisis mendalam, insight valuable | Analisis cukup | Analisis surface level | Tidak ada analisis |

### Presentation (15% dari total nilai)

| Kriteria | Excellent (13-15) | Good (10-12) | Fair (7-9) | Poor (0-6) |
|----------|------------------|--------------|------------|------------|
| **Slide Quality** | Professional, visual menarik | Slides baik | Slides basic | Slides jelek |
| **Delivery** | Percaya diri, pace tepat, engaging | Delivery baik | Cukup nervous | Tidak prepare |
| **Live Demo** | Demo sukses tanpa masalah | Demo dengan minor issue | Demo dengan masalah | Demo gagal |
| **Q&A** | Menjawab dengan baik dan mendalam | Jawaban cukup | Jawaban minimal | Tidak bisa jawab |

---

## 📊 Konversi Nilai

| Skor Total | Nilai Huruf | Keterangan |
|------------|-------------|------------|
| 90-100 | A | Exceptional |
| 85-89 | A- | Excellent |
| 80-84 | B+ | Very Good |
| 75-79 | B | Good |
| 70-74 | B- | Above Average |
| 65-69 | C+ | Average |
| 60-64 | C | Below Average |
| 55-59 | D | Poor |
| < 55 | E | Fail |

---

## ⚠️ Ketentuan Khusus

1. **Plagiarisme**: Penggunaan kode tanpa atribusi = nilai 0
2. **Keterlambatan**: -10% per hari keterlambatan (max 3 hari)
3. **Kelengkapan**: Submission tidak lengkap = nilai maksimal B-
4. **Live Demo Gagal**: Maksimal nilai C+ untuk komponen Integration
