# RUBRIK PENILAIAN PROJECT BAB 13: 3D RECONSTRUCTION

## Informasi Project

| Item | Keterangan |
|------|------------|
| **Judul Project** | Digital Twin Factory: 3D Reconstruction untuk Industri 4.0 |
| **Mata Kuliah** | Praktikum Computer Vision |
| **Bab** | 13 - 3D Reconstruction |
| **Total Nilai** | 100 poin |

---

## A. Komponen Penilaian

### 1. Data Acquisition Module (20%)

| Kriteria | Excellent (90-100%) | Good (75-89%) | Satisfactory (60-74%) | Needs Improvement (<60%) |
|----------|---------------------|---------------|----------------------|-------------------------|
| **Format Support** | Mendukung 4+ format (PLY, PCD, XYZ, OBJ, LAS) dengan error handling lengkap | Mendukung 3 format dengan error handling | Mendukung 2 format dengan error handling minimal | Hanya 1 format atau tanpa error handling |
| **Depth Conversion** | Konversi depth ke point cloud akurat dengan kalibrasi intrinsik | Konversi berfungsi dengan parameter default | Konversi dengan error kecil | Konversi tidak akurat |
| **Multi-scan Merge** | Merge otomatis dengan alignment | Merge manual dengan alignment | Merge tanpa alignment | Tidak ada fitur merge |
| **Metadata** | Ekstraksi dan logging metadata lengkap | Metadata dasar tersedia | Metadata minimal | Tidak ada metadata |

**Poin Maksimal: 20**

| Sub-komponen | Bobot | Poin |
|--------------|-------|------|
| Format support | 5% | /5 |
| Depth conversion | 5% | /5 |
| Multi-scan merge | 5% | /5 |
| Metadata extraction | 5% | /5 |
| **Total** | **20%** | **/20** |

---

### 2. Point Cloud Processing Pipeline (30%)

| Kriteria | Excellent (90-100%) | Good (75-89%) | Satisfactory (60-74%) | Needs Improvement (<60%) |
|----------|---------------------|---------------|----------------------|-------------------------|
| **Downsampling** | Adaptive voxel size dengan preservasi fitur penting | Voxel downsampling dengan parameter manual | Downsampling basic | Tidak ada downsampling |
| **Outlier Removal** | Multiple method (Statistical + Radius) dengan parameter tuning | Satu metode dengan parameter tuning | Satu metode dengan default | Tidak ada outlier removal |
| **Normal Estimation** | Normal dengan consistent orientation dan validation | Normal estimation dengan orientation | Normal tanpa orientation | Normal tidak diestimasi |
| **Registration** | ICP dengan global registration dan error metrics | ICP dengan good convergence | ICP basic | Tidak ada registration |
| **Segmentation** | Ground plane + object segmentation | Ground plane segmentation | Basic segmentation | Tidak ada segmentation |

**Poin Maksimal: 30**

| Sub-komponen | Bobot | Poin |
|--------------|-------|------|
| Adaptive downsampling | 6% | /6 |
| Outlier removal | 6% | /6 |
| Normal estimation | 6% | /6 |
| Registration (ICP) | 8% | /8 |
| Segmentation | 4% | /4 |
| **Total** | **30%** | **/30** |

---

### 3. Surface Reconstruction Engine (30%)

| Kriteria | Excellent (90-100%) | Good (75-89%) | Satisfactory (60-74%) | Needs Improvement (<60%) |
|----------|---------------------|---------------|----------------------|-------------------------|
| **Poisson Reconstruction** | Parameter tuning otomatis dengan density filtering | Multiple depth levels dengan cropping | Single depth level | Tidak implementasi |
| **Ball Pivoting** | Multiple radii dengan adaptive selection | Single radius dengan tuning | BPA basic | Tidak implementasi |
| **Mesh Cleaning** | Hole filling + degenerate removal + smoothing | 2 operasi cleaning | 1 operasi cleaning | Tidak ada cleaning |
| **Auto Selection** | Algoritma memilih metode optimal berdasarkan input | Selection berdasarkan user hint | Manual selection only | Tidak ada selection |
| **Quality Metrics** | Watertight check + manifold + genus + area | 3 metrics | 2 metrics | 1 atau tidak ada |

**Poin Maksimal: 30**

| Sub-komponen | Bobot | Poin |
|--------------|-------|------|
| Poisson reconstruction | 8% | /8 |
| Ball pivoting | 6% | /6 |
| Mesh cleaning | 6% | /6 |
| Auto algorithm selection | 5% | /5 |
| Quality metrics | 5% | /5 |
| **Total** | **30%** | **/30** |

---

### 4. Quality Inspection & Export (20%)

| Kriteria | Excellent (90-100%) | Good (75-89%) | Satisfactory (60-74%) | Needs Improvement (<60%) |
|----------|---------------------|---------------|----------------------|-------------------------|
| **CAD Comparison** | Distance computation + deviation map + statistics | Deviation map + basic stats | Distance only | Tidak ada comparison |
| **Report Generation** | PDF report + visualizations + metrics table | HTML/text report + metrics | Basic text report | Tidak ada report |
| **Export Formats** | 4+ formats (OBJ, STL, PLY, GLTF) dengan options | 3 formats | 2 formats | 1 format |
| **Visualization** | Interactive 3D viewer (web atau desktop) | Static visualization | Screenshot only | Tidak ada visualization |

**Poin Maksimal: 20**

| Sub-komponen | Bobot | Poin |
|--------------|-------|------|
| CAD comparison | 6% | /6 |
| Report generation | 6% | /6 |
| Export formats | 4% | /4 |
| Visualization | 4% | /4 |
| **Total** | **20%** | **/20** |

---

## B. Penilaian Code Quality (Bonus/Penalty)

### Bonus Points (+15% maksimal)

| Kriteria | Bonus |
|----------|-------|
| PEP8 compliance dengan linting | +3% |
| Comprehensive docstrings | +3% |
| Type hints | +2% |
| Unit tests (>70% coverage) | +4% |
| CI/CD integration | +3% |

### Penalty Points (-15% maksimal)

| Kriteria | Penalty |
|----------|---------|
| No error handling | -5% |
| Hardcoded paths | -3% |
| No comments | -3% |
| Memory leaks | -4% |

---

## C. Penilaian Dokumentasi

### README.md (5%)

| Kriteria | Poin |
|----------|------|
| Project overview | 1 |
| Installation instructions | 1 |
| Usage examples | 1 |
| Sample output/screenshots | 1 |
| Contributing guidelines | 1 |
| **Total** | **/5** |

### API Documentation (5%)

| Kriteria | Poin |
|----------|------|
| Function signatures | 1 |
| Parameter descriptions | 1 |
| Return value documentation | 1 |
| Usage examples | 1 |
| Generated docs (Sphinx/MkDocs) | 1 |
| **Total** | **/5** |

### Technical Report (5%)

| Kriteria | Poin |
|----------|------|
| Problem statement | 1 |
| Methodology | 1 |
| Results & analysis | 1 |
| Conclusions | 1 |
| References | 1 |
| **Total** | **/5** |

---

## D. Bonus Challenges

| Challenge | Bonus Points | Kriteria Penilaian |
|-----------|--------------|-------------------|
| Real-time Processing | +10% | Processing depth stream >10 FPS |
| Deep Learning | +10% | Neural network untuk reconstruction (PointNet, etc.) |
| AR/VR Integration | +10% | Demo di AR (mobile) atau VR (desktop) |
| Web Viewer | +5% | Three.js viewer dengan interaksi |

---

## E. Rekap Penilaian

### Nilai Komponen Utama

| Komponen | Bobot | Nilai | Poin |
|----------|-------|-------|------|
| Data Acquisition | 20% | | /20 |
| Point Cloud Processing | 30% | | /30 |
| Surface Reconstruction | 30% | | /30 |
| Quality Inspection | 20% | | /20 |
| **Subtotal** | **100%** | | **/100** |

### Bonus & Penalty

| Item | Adjustment |
|------|------------|
| Code Quality Bonus | + |
| Code Quality Penalty | - |
| Documentation Bonus | + |
| Challenge Bonus | + |
| **Total Adjustment** | |

### Nilai Akhir

| | |
|---|---|
| **Nilai Komponen** | /100 |
| **Adjustment** | ± |
| **NILAI AKHIR** | **/100** |

---

## F. Catatan Penilai

### Kelebihan Project:
```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

### Area yang Perlu Diperbaiki:
```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

### Rekomendasi:
```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

## G. Tanda Tangan

| | Mahasiswa | Penilai |
|---|---|---|
| Nama | | |
| NIM/NIP | | |
| Tanggal | | |
| Tanda Tangan | | |
