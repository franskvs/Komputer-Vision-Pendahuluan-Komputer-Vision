# JOBSHEET BAB 13: 3D RECONSTRUCTION

## Informasi Umum

| Item | Keterangan |
|------|------------|
| **Mata Kuliah** | Praktikum Computer Vision |
| **Bab** | 13 - 3D Reconstruction |
| **Topik** | Point Cloud Processing, Surface Reconstruction, Mesh Generation |
| **Durasi** | 4 x 50 menit |
| **Referensi Utama** | Szeliski, R. (2022). Computer Vision: Algorithms and Applications (2nd ed.) |

---

## Praktikum 1: Point Cloud Basics

### Tujuan
1. Memahami struktur data point cloud
2. Mampu load, visualize, dan save point cloud
3. Memahami berbagai format file point cloud

### Alat dan Bahan

**Hardware:**
- Komputer dengan GPU (opsional, untuk rendering cepat)
- RAM minimal 8GB
- Depth camera (opsional: Intel RealSense, Kinect)

**Software:**
- Python 3.8+
- Open3D 0.17+
- NumPy, Matplotlib

### Langkah Kerja

1. **Persiapan Environment:**
   ```bash
   pip install open3d numpy matplotlib
   ```

2. **Jalankan Program:**
   ```bash
   cd praktikum/
   python 01_point_cloud_basics.py
   ```

3. **Eksperimen:**
   - Load berbagai format point cloud (PLY, PCD, XYZ)
   - Generate point cloud sintetis (sphere, cube, bunny)
   - Eksplorasi atribut: coordinates, colors, normals
   - Visualisasi dengan berbagai rendering mode

4. **Modifikasi Kode:**
   - Ubah jumlah points yang di-generate
   - Tambahkan noise ke point cloud
   - Simpan ke format berbeda

### Data Pengamatan

| No | Format File | Ukuran (KB) | Jumlah Points | Waktu Load (ms) | Atribut |
|----|-------------|-------------|---------------|-----------------|---------|
| 1 | PLY | | | | |
| 2 | PCD | | | | |
| 3 | XYZ | | | | |
| 4 | OBJ | | | | |

### Analisis
1. Format mana yang paling efisien untuk penyimpanan?
2. Format mana yang mendukung warna dan normal?
3. Bagaimana hubungan jumlah points dengan ukuran file?

### Kesimpulan
(Tulis kesimpulan berdasarkan hasil pengamatan)

---

## Praktikum 2: Point Cloud Filtering

### Tujuan
1. Menerapkan teknik filtering untuk membersihkan point cloud
2. Memahami voxel grid downsampling
3. Menggunakan statistical dan radius outlier removal

### Alat dan Bahan

**Software:**
- Python 3.8+
- Open3D 0.17+
- NumPy

### Langkah Kerja

1. **Jalankan Program:**
   ```bash
   python 02_point_cloud_filtering.py
   ```

2. **Eksperimen:**
   - Terapkan voxel downsampling dengan berbagai ukuran
   - Gunakan statistical outlier removal
   - Gunakan radius outlier removal
   - Bandingkan hasil sebelum dan sesudah filtering

3. **Parameter yang Diubah:**
   - `voxel_size`: [0.01, 0.02, 0.05, 0.1]
   - `nb_neighbors`: [10, 20, 50]
   - `std_ratio`: [1.0, 2.0, 3.0]
   - `nb_points`: [5, 10, 20]
   - `radius`: [0.01, 0.05, 0.1]

### Data Pengamatan

**Voxel Downsampling:**

| Voxel Size | Points Sebelum | Points Sesudah | Reduksi (%) | Waktu (ms) |
|------------|----------------|----------------|-------------|------------|
| 0.01 | | | | |
| 0.02 | | | | |
| 0.05 | | | | |
| 0.1 | | | | |

**Statistical Outlier Removal:**

| nb_neighbors | std_ratio | Points Dihapus | Waktu (ms) |
|--------------|-----------|----------------|------------|
| 10 | 1.0 | | |
| 20 | 2.0 | | |
| 50 | 3.0 | | |

**Radius Outlier Removal:**

| radius | nb_points | Points Dihapus | Waktu (ms) |
|--------|-----------|----------------|------------|
| 0.01 | 5 | | |
| 0.05 | 10 | | |
| 0.1 | 20 | | |

### Analisis
1. Bagaimana voxel size mempengaruhi detail point cloud?
2. Kapan statistical outlier removal lebih baik dari radius outlier removal?
3. Bagaimana kombinasi filtering yang optimal?

---

## Praktikum 3: Normal Estimation

### Tujuan
1. Memahami pentingnya normal dalam rekonstruksi 3D
2. Mengimplementasikan estimasi normal
3. Menerapkan konsisten orientasi normal

### Alat dan Bahan

**Software:**
- Python 3.8+
- Open3D 0.17+

### Langkah Kerja

1. **Jalankan Program:**
   ```bash
   python 03_normal_estimation.py
   ```

2. **Eksperimen:**
   - Estimate normal dengan berbagai parameter
   - Visualisasi normal vectors
   - Orient normals consistently
   - Bandingkan metode KNN vs Radius search

3. **Parameter yang Diubah:**
   - `search_param_knn`: [10, 20, 30, 50]
   - `search_param_radius`: [0.01, 0.05, 0.1]
   - Orientasi: toward camera vs outward

### Data Pengamatan

| Parameter | Metode | Waktu Estimasi (ms) | Kualitas Visual | Konsistensi |
|-----------|--------|---------------------|-----------------|-------------|
| KNN=10 | KNN | | | |
| KNN=30 | KNN | | | |
| r=0.01 | Radius | | | |
| r=0.1 | Radius | | | |

### Analisis
1. Mengapa normal penting untuk surface reconstruction?
2. Bagaimana parameter search mempengaruhi kualitas normal?
3. Apa perbedaan hasil antara metode KNN dan Radius?

---

## Praktikum 4: Point Cloud Registration (ICP)

### Tujuan
1. Memahami konsep point cloud registration
2. Mengimplementasikan Iterative Closest Point (ICP)
3. Melakukan global registration dengan RANSAC

### Alat dan Bahan

**Software:**
- Python 3.8+
- Open3D 0.17+

### Langkah Kerja

1. **Jalankan Program:**
   ```bash
   python 04_point_cloud_registration.py
   ```

2. **Eksperimen:**
   - Apply transformasi ke point cloud
   - Gunakan Point-to-Point ICP
   - Gunakan Point-to-Plane ICP
   - Bandingkan dengan global registration

3. **Skenario Testing:**
   - Rotasi kecil (< 30°)
   - Rotasi besar (> 45°)
   - Dengan noise
   - Partial overlap

### Data Pengamatan

| Metode | Initial Error | Final Error | Iterasi | Waktu (ms) | Fitness |
|--------|---------------|-------------|---------|------------|---------|
| Point-to-Point ICP | | | | | |
| Point-to-Plane ICP | | | | | |
| RANSAC + ICP | | | | | |
| Colored ICP | | | | | |

### Analisis
1. Kapan Point-to-Plane ICP lebih baik dari Point-to-Point?
2. Mengapa global registration diperlukan untuk transformasi besar?
3. Bagaimana noise mempengaruhi akurasi registration?

---

## Praktikum 5: Surface Reconstruction - Poisson

### Tujuan
1. Memahami algoritma Poisson surface reconstruction
2. Mengimplementasikan rekonstruksi dengan berbagai depth
3. Melakukan post-processing pada mesh hasil

### Alat dan Bahan

**Software:**
- Python 3.8+
- Open3D 0.17+

### Langkah Kerja

1. **Jalankan Program:**
   ```bash
   python 05_poisson_reconstruction.py
   ```

2. **Eksperimen:**
   - Preprocessing: downsample dan estimate normals
   - Rekonstruksi dengan berbagai depth levels
   - Crop mesh berdasarkan density
   - Bandingkan quality metrics

3. **Parameter yang Diubah:**
   - `depth`: [6, 8, 10, 12]
   - `width`: [0.0, 0.5, 1.0]
   - `scale`: [1.0, 1.1, 1.2]

### Data Pengamatan

| Depth | Vertices | Faces | Waktu (s) | Watertight | Visual Quality |
|-------|----------|-------|-----------|------------|----------------|
| 6 | | | | ☐ Yes ☐ No | |
| 8 | | | | ☐ Yes ☐ No | |
| 10 | | | | ☐ Yes ☐ No | |
| 12 | | | | ☐ Yes ☐ No | |

### Analisis
1. Bagaimana depth mempengaruhi detail mesh?
2. Kapan perlu melakukan density-based cropping?
3. Apa trade-off antara kualitas dan waktu komputasi?

---

## Praktikum 6: Surface Reconstruction - Ball Pivoting

### Tujuan
1. Memahami algoritma Ball Pivoting Algorithm (BPA)
2. Membandingkan BPA dengan Poisson reconstruction
3. Memilih algoritma yang tepat untuk berbagai kasus

### Alat dan Bahan

**Software:**
- Python 3.8+
- Open3D 0.17+

### Langkah Kerja

1. **Jalankan Program:**
   ```bash
   python 06_ball_pivoting.py
   ```

2. **Eksperimen:**
   - Tentukan optimal ball radius
   - Gunakan multiple radii
   - Bandingkan dengan Poisson
   - Handle sparse regions

3. **Parameter yang Diubah:**
   - `radii`: single vs multiple
   - Ball radius relative to point spacing

### Data Pengamatan

**Perbandingan Metode:**

| Aspek | Ball Pivoting | Poisson |
|-------|---------------|---------|
| Vertices | | |
| Faces | | |
| Waktu (s) | | |
| Holes | | |
| Detail preservation | | |
| Noise sensitivity | | |

### Analisis
1. Kapan BPA lebih cocok daripada Poisson?
2. Bagaimana menentukan optimal ball radius?
3. Apa kelebihan dan kekurangan masing-masing metode?

---

## Praktikum 7: Mesh Processing dan Aplikasi

### Tujuan
1. Melakukan operasi post-processing pada mesh
2. Mengimplementasikan mesh simplification
3. Menerapkan texture mapping pada mesh

### Alat dan Bahan

**Software:**
- Python 3.8+
- Open3D 0.17+
- Trimesh (opsional)

### Langkah Kerja

1. **Jalankan Program:**
   ```bash
   python 07_mesh_processing.py
   ```

2. **Eksperimen:**
   - Mesh smoothing (Laplacian, Taubin)
   - Mesh simplification (decimation)
   - Hole filling
   - Texture mapping dari gambar

3. **Operasi yang Dilakukan:**
   - Smoothing dengan berbagai iterasi
   - Decimation ke berbagai target face count
   - UV mapping dan texturing

### Data Pengamatan

**Smoothing:**

| Metode | Iterasi | Smoothness | Detail Loss | Waktu (ms) |
|--------|---------|------------|-------------|------------|
| Laplacian | 1 | | | |
| Laplacian | 5 | | | |
| Laplacian | 10 | | | |
| Taubin | 10 | | | |

**Decimation:**

| Target Faces | Actual Faces | Error (mm) | Waktu (ms) |
|--------------|--------------|------------|------------|
| 50% | | | |
| 25% | | | |
| 10% | | | |

### Analisis
1. Berapa iterasi smoothing yang optimal?
2. Seberapa besar decimation yang dapat ditoleransi?
3. Bagaimana texture mapping mempengaruhi kualitas visual?

---

## Tugas Mandiri

### Tugas 1: Pipeline Rekonstruksi Lengkap

Implementasikan pipeline rekonstruksi 3D lengkap:
1. Load depth images atau point cloud
2. Preprocessing (filtering, downsampling)
3. Normal estimation
4. Surface reconstruction
5. Mesh processing
6. Export hasil final

**Deliverables:**
- Source code Python
- Dokumentasi pipeline
- Sample output mesh

### Tugas 2: Perbandingan Algoritma

Bandingkan minimal 3 metode rekonstruksi:
1. Poisson reconstruction
2. Ball Pivoting Algorithm
3. Alpha shapes (atau metode lain)

**Evaluasi:**
- Kualitas visual
- Waktu komputasi
- Memory usage
- Robustness terhadap noise

### Tugas 3: Aplikasi Real-World

Pilih salah satu aplikasi dan implementasikan:
1. 3D scanning dengan depth camera
2. Photogrammetry dari foto smartphone
3. Medical image 3D reconstruction
4. Reverse engineering komponen mesin

---

## Checklist Praktikum

| No | Item | Status |
|----|------|--------|
| 1 | Point cloud basics | ☐ |
| 2 | Point cloud filtering | ☐ |
| 3 | Normal estimation | ☐ |
| 4 | Point cloud registration | ☐ |
| 5 | Poisson reconstruction | ☐ |
| 6 | Ball pivoting reconstruction | ☐ |
| 7 | Mesh processing | ☐ |
| 8 | Tugas mandiri 1 | ☐ |
| 9 | Tugas mandiri 2 | ☐ |
| 10 | Tugas mandiri 3 | ☐ |

---

## Catatan Penting

1. **Backup Data:** Selalu backup point cloud dan mesh sebelum processing
2. **Memory Management:** Point cloud besar membutuhkan RAM yang cukup
3. **Visualization:** Gunakan Open3D visualizer untuk inspeksi detail
4. **File Formats:** PLY mendukung color dan normal, OBJ untuk mesh standar
5. **Normal Orientation:** Pastikan normal konsisten sebelum reconstruction
