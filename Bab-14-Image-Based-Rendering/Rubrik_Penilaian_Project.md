# Rubrik Penilaian Project
## Virtual Tour Creator - Image-Based Rendering untuk Tur Virtual Interaktif

### Informasi Umum
- **Mata Kuliah**: Praktikum Computer Vision
- **Bab**: 14 - Image-Based Rendering
- **Total Nilai**: 100 poin
- **Bonus Maksimal**: 20 poin

---

## Komponen Penilaian

### 1. Module 1: Image Capture & Import (15%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Capture Guidance** (5%) | Panduan lengkap dengan rekomendasi per scene type, overlap calculation, camera settings | Panduan dasar dengan tips capture | Panduan minimal | Tidak ada panduan |
| **Quality Assessment** (5%) | Metrics komprehensif (sharpness, exposure, blur, resolution), automatic rejection | Metrics dasar dengan threshold | Hanya cek resolusi | Tidak ada assessment |
| **Organization** (5%) | Fully automated dengan metadata extraction, directory structure, naming convention | Semi-automated organization | Manual organization dengan struktur | Tidak terorganisir |

**Skor Module 1**: _____ / 15

---

### 2. Module 2: Panorama Stitching Engine (30%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Feature Detection** (5%) | Multiple detector support, adaptive parameters, robust matching dengan ratio test | SIFT/ORB working reliably | Basic feature detection | Tidak berfungsi |
| **Homography Estimation** (5%) | RANSAC dengan adaptive threshold, outlier visualization, error metrics | RANSAC working | Basic homography | Estimasi error |
| **Cylindrical Projection** (5%) | Accurate projection, auto focal length estimation, distortion handling | Working cylindrical projection | Basic projection | Tidak ada projection |
| **Multi-band Blending** (5%) | Seamless blending, exposure compensation, ghost removal | Good multi-band blending | Alpha blending | Visible seams |
| **360° Support** (5%) | Full 360° dengan wraparound, drift correction, bundle adjustment | 300°+ coverage | 180°+ coverage | < 180° coverage |
| **Quality Hasil** (5%) | Professional quality, no visible artifacts | Good quality, minor issues | Acceptable quality | Poor quality |

**Skor Module 2**: _____ / 30

---

### 3. Module 3: View Synthesis (25%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Equirectangular Sampling** (5%) | Accurate sampling, multiple FOV support, anti-aliasing | Working sampling | Basic sampling | Artifacts |
| **View Rendering** (5%) | Smooth, real-time capable, artifact-free | Good rendering, minor issues | Working but slow | Not working |
| **Transition Effects** (5%) | 3+ effect types, smooth animations, configurable | 2 working effects | Basic fade | Abrupt transition |
| **Depth Estimation** (5%) | Learning-based atau geometric dengan quality | Geometric estimation | Constant depth | No depth |
| **Parallax Handling** (5%) | Depth-based parallax, occlusion handling | Basic parallax | No parallax | N/A |

**Skor Module 3**: _____ / 25

---

### 4. Module 4: Tour Builder (15%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Graph Management** (5%) | Full CRUD operations, validation, persistence | Add/remove locations | Basic graph | Hardcoded |
| **Hotspot System** (5%) | Multiple types (nav, info, media), customizable appearance | Navigation hotspots only | Basic hotspots | No hotspots |
| **Export** (5%) | Multiple formats (web, standalone), complete configuration | Single format export | Manual export | No export |

**Skor Module 4**: _____ / 15

---

### 5. Module 5: Interactive Viewer (15%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Viewer Implementation** (5%) | Smooth rendering, responsive, cross-browser | Working viewer | Basic display | Not working |
| **Interaction** (5%) | Full mouse/touch/keyboard, zoom, auto-rotate | Mouse control only | Limited interaction | No interaction |
| **Navigation** (5%) | Seamless location transitions, minimap, progress indicator | Working navigation | Basic navigation | Manual only |

**Skor Module 5**: _____ / 15

---

## Bonus Points (Maksimal +20%)

| Bonus | Poin | Kriteria |
|-------|------|----------|
| VR Support | +10% | Functional WebVR/WebXR mode dengan head tracking |
| Mobile App | +10% | Native atau PWA dengan gesture support |
| Learning-based Depth | +5% | Integrasi dengan neural depth estimation |
| Multi-resolution | +5% | Progressive loading, LOD system |
| Real-time Processing | +5% | Live stitching dari camera feed |

**Total Bonus**: _____ / 20

---

## Dokumentasi dan Presentasi (Wajib)

| Kriteria | Excellent | Good | Fair | Poor |
|----------|-----------|------|------|------|
| **Dokumentasi Kode** | Lengkap dengan docstrings, type hints, examples | Cukup lengkap | Minimal | Tidak ada |
| **README** | Komprehensif dengan installation, usage, examples, screenshots | Lengkap | Minimal | Tidak ada |
| **Demo Video** | 5+ menit, narasi jelas, semua fitur | 3+ menit, fitur utama | < 3 menit | Tidak ada |
| **Presentasi** | Profesional, live demo berhasil | Good presentasi | Presentasi dasar | Tidak presentasi |

*Dokumentasi yang tidak memadai akan mengurangi nilai hingga 20%*

---

## Perhitungan Nilai Akhir

```
Nilai Dasar = Module 1 + Module 2 + Module 3 + Module 4 + Module 5
            = _____ + _____ + _____ + _____ + _____
            = _____ / 100

Bonus Points = _____

Nilai Sebelum Adjustment = min(Nilai Dasar + Bonus, 100)
                        = _____

Pengurangan:
- Keterlambatan: _____ × (-10%) = _____
- Dokumentasi kurang: _____
- Lainnya: _____

Total Pengurangan = _____

NILAI AKHIR = _____ / 100
```

---

## Kriteria Khusus

### Kualitas Panorama
| Grade | Kriteria |
|-------|----------|
| A | No visible seams, consistent exposure, sharp throughout |
| B | Minor seams, slight exposure variation, mostly sharp |
| C | Some visible seams, exposure differences, acceptable |
| D | Obvious seams, poor blending, noticeable blur |
| F | Unusable panorama |

### View Synthesis Quality
| Grade | Kriteria |
|-------|----------|
| A | Smooth transitions, no artifacts, realistic parallax |
| B | Good transitions, minor artifacts at extremes |
| C | Working transitions, noticeable artifacts |
| D | Jerky transitions, significant artifacts |
| F | Non-functional |

### User Experience
| Grade | Kriteria |
|-------|----------|
| A | Intuitive, responsive, professional feel |
| B | Easy to use, minor UX issues |
| C | Functional, some confusion points |
| D | Difficult to use |
| F | Unusable |

---

## Catatan Penilai

### Komentar Module 1:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Module 2:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Module 3:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Module 4:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Module 5:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Umum:
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Tanda Tangan

| | Nama | Tanda Tangan | Tanggal |
|---|------|--------------|---------|
| Mahasiswa | | | |
| Penilai 1 | | | |
| Penilai 2 | | | |

---

## Rubrik Detail per Komponen

### A. Panorama Stitching Quality Rubric

**Level 5 (Excellent - 90-100%)**
- Seamless blending tanpa visible seams
- Consistent exposure dan color
- Sharp focus throughout
- No ghosting atau misalignment
- Full 360° coverage

**Level 4 (Good - 70-89%)**
- Minor seams yang hanya terlihat saat zoom
- Slight exposure variation yang tidak mengganggu
- Mostly sharp dengan minor softness
- No significant ghosting
- 300°+ coverage

**Level 3 (Satisfactory - 50-69%)**
- Visible seams tapi tidak severe
- Noticeable exposure differences
- Some softness atau blur
- Minor ghosting di beberapa area
- 180°+ coverage

**Level 2 (Below Expectations - 30-49%)**
- Obvious seams
- Significant exposure problems
- Noticeable blur
- Visible ghosting
- < 180° coverage

**Level 1 (Unsatisfactory - <30%)**
- Severe stitching errors
- Unusable result

### B. View Synthesis Quality Rubric

**Level 5 (Excellent)**
- Real-time rendering
- Artifact-free views
- Realistic depth parallax
- Smooth transitions
- High resolution output

**Level 4 (Good)**
- Near real-time (>15 fps)
- Minor artifacts at view boundaries
- Basic parallax effect
- Smooth transitions
- Good resolution

**Level 3 (Satisfactory)**
- Interactive speed (>5 fps)
- Some artifacts visible
- Simple view changes
- Working transitions

**Level 2 (Below Expectations)**
- Slow rendering
- Obvious artifacts
- Limited view range

**Level 1 (Unsatisfactory)**
- Non-functional

### C. Code Quality Rubric

**Level 5 (Excellent)**
- Clean, well-organized code
- Comprehensive documentation
- Error handling
- Unit tests
- Efficient algorithms

**Level 4 (Good)**
- Organized code
- Good documentation
- Basic error handling
- Some tests

**Level 3 (Satisfactory)**
- Readable code
- Some documentation
- Minimal error handling

**Level 2 (Below Expectations)**
- Messy code
- Poor documentation

**Level 1 (Unsatisfactory)**
- Unreadable code
