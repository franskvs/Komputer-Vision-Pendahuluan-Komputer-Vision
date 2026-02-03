# Jobsheet: Bab 14 - Image-Based Rendering

## Informasi Umum
- **Mata Kuliah**: Praktikum Computer Vision
- **Topik**: Image-Based Rendering
- **Waktu**: 3 x 170 menit (3 pertemuan)
- **Referensi Utama**: Szeliski, R. "Computer Vision: Algorithms and Applications" 2nd Edition, Chapter 14

---

## Tujuan Pembelajaran

Setelah menyelesaikan praktikum ini, mahasiswa mampu:
1. Memahami konsep dan spektrum Image-Based Rendering
2. Mengimplementasikan panorama stitching dan cylindrical projection
3. Menerapkan view morphing dan image interpolation
4. Memahami konsep Multi-Plane Images (MPI)
5. Mengimplementasikan basic view synthesis
6. Memahami konsep Neural Radiance Fields (NeRF)
7. Mengevaluasi kualitas hasil rendering dengan metrik standar

---

## Alat dan Bahan

### Software
- Python 3.8+
- OpenCV 4.5+
- NumPy
- Matplotlib
- SciPy
- Pillow (PIL)
- scikit-image
- PyTorch (opsional, untuk NeRF)

### Hardware
- Komputer dengan RAM minimal 8 GB
- GPU (opsional, untuk neural methods)
- Webcam atau kamera digital

### Data
- Sequential images untuk panorama
- Stereo image pairs
- Multi-view images dataset
- Sample videos

---

## Percobaan 1: Image Warping dan Homography

### Tujuan
Memahami dasar image warping menggunakan transformasi homography.

### Dasar Teori
Homography mentransformasi titik dari satu plane ke plane lain:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} \sim H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

### Prosedur
1. Load dua gambar dengan overlap
2. Deteksi keypoints (SIFT/ORB)
3. Match features antar gambar
4. Estimasi homography dengan RANSAC
5. Warp gambar menggunakan homography
6. Blend hasil warping

### Tabel Pengamatan 1.1: Feature Matching
| Parameter | Nilai | Matches | Inliers | Accuracy |
|-----------|-------|---------|---------|----------|
| ORB, 500 features |  |  |  |  |
| ORB, 1000 features |  |  |  |  |
| SIFT, 500 features |  |  |  |  |
| SIFT, 1000 features |  |  |  |  |

### Tabel Pengamatan 1.2: RANSAC Threshold
| Threshold | Inliers | Reprojection Error | Visual Quality |
|-----------|---------|-------------------|----------------|
| 3.0 |  |  |  |
| 5.0 |  |  |  |
| 10.0 |  |  |  |
| 15.0 |  |  |  |

### Pertanyaan Analisis
1. Bagaimana jumlah features mempengaruhi kualitas matching?
2. Mengapa RANSAC diperlukan untuk estimasi homography?
3. Apa efek threshold RANSAC terhadap hasil?

---

## Percobaan 2: Panorama Stitching

### Tujuan
Mengimplementasikan panorama stitching dari multiple images.

### Dasar Teori
Panorama stitching menggabungkan gambar dengan overlap:
1. Feature detection dan matching
2. Homography estimation
3. Image warping
4. Blending (alpha, multi-band)

### Prosedur
1. Capture/load sequence gambar panorama
2. Detect dan match features
3. Estimasi homographies ke reference frame
4. Warp semua images
5. Blend dengan berbagai metode
6. Evaluasi hasil

### Tabel Pengamatan 2.1: Blending Methods
| Metode Blending | Seam Visibility | Processing Time | Exposure Consistency |
|-----------------|-----------------|-----------------|---------------------|
| Simple Overlay |  |  |  |
| Alpha Blending |  |  |  |
| Feather Blending |  |  |  |
| Multi-band |  |  |  |

### Tabel Pengamatan 2.2: Number of Images
| Jumlah Images | Field of View | Distortion | Quality |
|---------------|---------------|------------|---------|
| 3 |  |  |  |
| 5 |  |  |  |
| 7 |  |  |  |
| 10+ |  |  |  |

### Pertanyaan Analisis
1. Mengapa multi-band blending memberikan hasil lebih baik?
2. Apa penyebab ghosting pada panorama?
3. Bagaimana menangani exposure difference?

---

## Percobaan 3: Cylindrical dan Spherical Projection

### Tujuan
Mengimplementasikan cylindrical dan spherical image projection untuk 360° panorama.

### Dasar Teori
**Cylindrical Projection**:
$$x' = f \cdot \arctan\left(\frac{x - c_x}{f}\right)$$
$$y' = f \cdot \frac{y - c_y}{\sqrt{(x - c_x)^2 + f^2}}$$

**Spherical Projection**:
$$\theta = \arctan\left(\frac{x - c_x}{f}\right)$$
$$\phi = \arctan\left(\frac{y - c_y}{\sqrt{(x - c_x)^2 + f^2}}\right)$$

### Prosedur
1. Kalibrasi atau estimasi focal length
2. Project images ke cylindrical/spherical
3. Stitch projected images
4. Handle wraparound untuk 360°
5. Render view dari arbitrary direction

### Tabel Pengamatan 3.1: Focal Length Effect
| Focal Length (px) | Vertical Distortion | Horizontal Coverage | Alignment |
|-------------------|--------------------|--------------------|-----------|
| 500 |  |  |  |
| 800 |  |  |  |
| 1200 |  |  |  |
| Auto-estimated |  |  |  |

### Tabel Pengamatan 3.2: Projection Comparison
| Aspek | Cylindrical | Spherical | Planar |
|-------|-------------|-----------|--------|
| Vertical distortion |  |  |  |
| Horizontal distortion |  |  |  |
| Full 360° support |  |  |  |
| Computation time |  |  |  |

### Pertanyaan Analisis
1. Kapan menggunakan cylindrical vs spherical projection?
2. Bagaimana focal length mempengaruhi distortion?
3. Apa tantangan membuat 360° spherical panorama?

---

## Percobaan 4: View Interpolation

### Tujuan
Mengimplementasikan view interpolation menggunakan stereo dan depth.

### Dasar Teori
View interpolation mensintesis view antara dua posisi kamera:
$$I_t = (1-t) \cdot W_1(I_1) + t \cdot W_2(I_2)$$

Membutuhkan depth atau disparity untuk warping.

### Prosedur
1. Load stereo image pair
2. Compute disparity map
3. Forward warp dari kedua views
4. Handle occlusions
5. Blend warped images
6. Generate in-between views

### Tabel Pengamatan 4.1: Interpolation Position
| t Value | Artifact Level | Consistency | Temporal Smoothness |
|---------|----------------|-------------|-------------------|
| 0.0 (source) |  |  |  |
| 0.25 |  |  |  |
| 0.5 |  |  |  |
| 0.75 |  |  |  |
| 1.0 (target) |  |  |  |

### Tabel Pengamatan 4.2: Occlusion Handling
| Metode | Hole Coverage | Artifact | Computation |
|--------|---------------|----------|-------------|
| No handling |  |  |  |
| Nearest pixel |  |  |  |
| Inpainting |  |  |  |
| Multi-view |  |  |  |

### Pertanyaan Analisis
1. Mengapa terjadi artifacts pada interpolated views?
2. Bagaimana menangani disoccluded regions?
3. Apa hubungan baseline dan quality?

---

## Percobaan 5: Multi-Plane Images (MPI)

### Tujuan
Memahami dan mengimplementasikan Multi-Plane Image representation.

### Dasar Teori
MPI merepresentasikan scene sebagai set of RGBA planes:
$$C(x,y) = \sum_{d=1}^{D} \alpha_d(x,y) \cdot c_d(x,y) \cdot \prod_{d'<d}(1 - \alpha_{d'}(x,y))$$

### Prosedur
1. Create MPI representation dari stereo
2. Assign pixels ke depth planes
3. Compute alpha values
4. Render novel views dengan plane homographies
5. Alpha compositing
6. Evaluate quality

### Tabel Pengamatan 5.1: Number of Planes
| Jumlah Planes | Depth Resolution | Memory | Quality | Speed |
|---------------|------------------|--------|---------|-------|
| 8 |  |  |  |  |
| 16 |  |  |  |  |
| 32 |  |  |  |  |
| 64 |  |  |  |  |

### Tabel Pengamatan 5.2: View Range
| Baseline Ratio | Valid Range | Artifacts | Parallax Accuracy |
|----------------|-------------|-----------|------------------|
| 0.1x |  |  |  |
| 0.5x |  |  |  |
| 1.0x |  |  |  |
| 2.0x |  |  |  |

### Pertanyaan Analisis
1. Mengapa MPI cocok untuk real-time rendering?
2. Apa trade-off antara jumlah planes dan quality?
3. Bagaimana MPI menangani semi-transparency?

---

## Percobaan 6: Image Quality Metrics

### Tujuan
Mengimplementasikan dan membandingkan metrik evaluasi kualitas rendering.

### Dasar Teori
**PSNR**:
$$PSNR = 10 \log_{10}\left(\frac{MAX^2}{MSE}\right)$$

**SSIM**:
$$SSIM(x,y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$$

### Prosedur
1. Generate rendered views
2. Compare dengan ground truth
3. Compute PSNR
4. Compute SSIM
5. Compute perceptual metrics (optional: LPIPS)
6. Analyze correlation

### Tabel Pengamatan 6.1: Metric Comparison
| Method | PSNR (dB) | SSIM | MSE | Visual Quality |
|--------|-----------|------|-----|----------------|
| Simple warp |  |  |  |  |
| View interpolation |  |  |  |  |
| MPI |  |  |  |  |
| Neural (if available) |  |  |  |  |

### Tabel Pengamatan 6.2: Metric vs Perceptual
| Image Pair | PSNR | SSIM | Human Rating (1-5) |
|------------|------|------|-------------------|
| A |  |  |  |
| B |  |  |  |
| C |  |  |  |
| D |  |  |  |

### Pertanyaan Analisis
1. Mengapa SSIM lebih sesuai dengan persepsi manusia?
2. Kapan PSNR tidak reliable?
3. Apa kelebihan learned metrics seperti LPIPS?

---

## Percobaan 7: NeRF Concepts dan Visualization

### Tujuan
Memahami konsep Neural Radiance Fields dan volume rendering.

### Dasar Teori
NeRF mempelajari fungsi kontinu:
$$F_\Theta: (\mathbf{x}, \mathbf{d}) \rightarrow (\mathbf{c}, \sigma)$$

Volume rendering:
$$C(\mathbf{r}) = \sum_{i=1}^{N} T_i(1 - \exp(-\sigma_i \delta_i))\mathbf{c}_i$$

### Prosedur
1. Understand ray marching concept
2. Implement basic volume rendering
3. Visualize rays melalui volume
4. Experiment dengan sampling strategies
5. Understand positional encoding
6. Analyze NeRF architecture

### Tabel Pengamatan 7.1: Ray Sampling
| Samples per Ray | Quality | Computation Time | Memory |
|-----------------|---------|-----------------|--------|
| 32 |  |  |  |
| 64 |  |  |  |
| 128 |  |  |  |
| 256 |  |  |  |

### Tabel Pengamatan 7.2: Positional Encoding
| Encoding Levels (L) | High-freq Detail | Noise | Training Stability |
|--------------------|------------------|-------|-------------------|
| 0 (none) |  |  |  |
| 4 |  |  |  |
| 8 |  |  |  |
| 10 (default) |  |  |  |

### Pertanyaan Analisis
1. Mengapa positional encoding diperlukan?
2. Apa trade-off coarse vs fine sampling?
3. Bagaimana NeRF berbeda dari explicit 3D representation?

---

## Tugas Praktikum

### Tugas 1: Panorama Stitching System
Buat sistem panorama stitching yang:
- Deteksi otomatis overlap
- Robust feature matching
- Multi-band blending
- Support cylindrical projection

### Tugas 2: View Synthesis Application
Implementasikan aplikasi view synthesis:
- Input: stereo images
- Depth estimation
- Novel view generation
- Interactive view control

### Tugas 3: Quality Comparison Study
Lakukan comparative study:
- Implement 3 metode view synthesis
- Evaluate dengan multiple metrics
- User study sederhana
- Report dan rekomendasi

---

## Format Laporan

### Struktur Laporan
1. **Pendahuluan** (10%)
   - Latar belakang IBR
   - Tujuan percobaan

2. **Dasar Teori** (15%)
   - Homography dan warping
   - Blending techniques
   - View synthesis concepts

3. **Metodologi** (20%)
   - Setup eksperimen
   - Dataset yang digunakan
   - Parameter konfigurasi

4. **Hasil dan Pembahasan** (40%)
   - Tabel pengamatan lengkap
   - Screenshot hasil
   - Analisis perbandingan

5. **Kesimpulan** (10%)
   - Ringkasan temuan
   - Best practices

6. **Lampiran** (5%)
   - Source code
   - Data tambahan

### Kriteria Penilaian
| Komponen | Bobot |
|----------|-------|
| Kelengkapan percobaan | 25% |
| Analisis hasil | 30% |
| Implementasi kode | 25% |
| Laporan | 20% |

---

## Tips Praktikum

### Best Practices
1. **Feature Matching**
   - Gunakan ratio test untuk filtering
   - RANSAC untuk outlier rejection

2. **Blending**
   - Multi-band untuk seams
   - Exposure compensation untuk color consistency

3. **View Synthesis**
   - Handle occlusions explicitly
   - Use depth-aware blending

### Common Issues
- Ghosting: object bergerak saat capture
- Drift: cumulative error pada banyak images
- Holes: missing data di disoccluded regions

### Troubleshooting
```
Problem: Poor panorama alignment
Solution: Check focal length, increase features

Problem: Visible seams
Solution: Use multi-band blending, exposure compensation

Problem: Holes in synthesized views
Solution: Better inpainting, use more source views
```

---

## Referensi Praktikum

1. Szeliski, R. (2022). "Computer Vision: Algorithms and Applications", Chapter 14
2. OpenCV Documentation - Image Stitching Module
3. NeRF: Neural Radiance Fields (Mildenhall et al., 2020)
4. Multi-Plane Images (Zhou et al., 2018)
