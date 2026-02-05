# Rubrik Penilaian Tugas Video
## Bab 14: Image-Based Rendering

### Informasi Umum
- **Durasi Video**: 7-10 menit
- **Format**: MP4 (H.264), resolusi minimal 720p
- **Deadline**: Sesuai jadwal praktikum
- **Pengumpulan**: Platform e-learning

---

## Komponen Penilaian

### 1. Konten Materi (40%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Konsep IBR** (8%) | Penjelasan spektrum IBR lengkap, motivasi jelas, perbandingan dengan geometry-based | Penjelasan cukup lengkap | Penjelasan dasar | Tidak akurat/tidak ada |
| **Light Fields** (8%) | Plenoptic function, parameterisasi 4D, capture dan rendering | Konsep dasar light fields | Menyebut light fields | Tidak dibahas |
| **Panorama Stitching** (8%) | Homography, blending methods, cylindrical/spherical projection | Feature matching dan stitching | Stitching dasar | Tidak dibahas |
| **Neural Methods** (8%) | NeRF architecture, volume rendering, 3D Gaussian Splatting | Salah satu neural method | Menyebut NeRF/3DGS | Tidak dibahas |
| **View Synthesis** (8%) | Forward/backward warping, MPI, depth handling | View interpolation dasar | Konsep dasar | Tidak dibahas |

**Skor Konten**: _____ / 40

### 2. Kejelasan Penyampaian (25%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Struktur Presentasi** (7%) | Alur logis, transisi smooth, opening & closing kuat | Struktur jelas | Cukup terstruktur | Tidak terstruktur |
| **Bahasa & Artikulasi** (6%) | Jelas, pace tepat, terminologi benar | Cukup jelas | Beberapa bagian sulit dipahami | Tidak jelas |
| **Visualisasi Konsep** (6%) | Diagram informatif, animasi, ilustrasi original | Visualisasi mendukung | Visualisasi minimal | Tanpa visualisasi |
| **Engagement** (6%) | Menarik, interaktif, contoh relatable | Cukup engaging | Monoton tapi informatif | Membosankan |

**Skor Kejelasan**: _____ / 25

### 3. Kualitas Produksi (20%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Video Quality** (5%) | 1080p+, stable, well-lit | 720p, stable | 720p, minor issues | Low quality |
| **Audio Quality** (5%) | Clear, no noise, good levels | Clear, minimal noise | Some audio issues | Poor audio |
| **Editing** (5%) | Professional cuts, graphics, lower thirds | Good editing | Basic editing | No editing |
| **Graphics/Slides** (5%) | High quality, consistent branding | Good graphics | Basic slides | No graphics |

**Skor Produksi**: _____ / 20

### 4. Demonstrasi Teknis (15%)

| Kriteria | Excellent (90-100%) | Good (70-89%) | Fair (50-69%) | Poor (<50%) |
|----------|---------------------|---------------|---------------|-------------|
| **Demo Panorama** (5%) | Live capture to result, explain steps | Show stitching process | Show result only | No demo |
| **Demo View Synthesis** (5%) | Interactive novel view generation | Show view interpolation | Static comparison | No demo |
| **Code Walkthrough** (5%) | Explain key algorithms with code | Show some code | Mention code exists | No code shown |

**Skor Demo**: _____ / 15

---

## Detail Penilaian per Topik

### Topik 1: Konsep Image-Based Rendering (1-1.5 menit)

**Harus mencakup:**
- [ ] Definisi IBR dan motivasi
- [ ] Spektrum IBR (image-only vs geometry-based)
- [ ] Perbandingan dengan traditional 3D rendering
- [ ] Aplikasi real-world (VR, tourism, real estate)

**Nilai**: _____ / 10

### Topik 2: Light Fields dan Panorama (2 menit)

**Harus mencakup:**
- [ ] Plenoptic function (apa yang direpresentasikan)
- [ ] 4D light field parameterisasi
- [ ] Panorama stitching pipeline
- [ ] Cylindrical/spherical projection
- [ ] Multi-band blending

**Nilai**: _____ / 15

### Topik 3: Neural Rendering Methods (2 menit)

**Harus mencakup:**
- [ ] NeRF: representasi MLP, input/output
- [ ] Volume rendering equation
- [ ] Positional encoding
- [ ] 3D Gaussian Splatting overview
- [ ] Perbandingan speed vs quality

**Nilai**: _____ / 15

### Topik 4: View Synthesis Techniques (1.5 menit)

**Harus mencakup:**
- [ ] Forward vs backward warping
- [ ] Depth-based view interpolation
- [ ] Multi-Plane Images (MPI)
- [ ] Handling occlusions dan disocclusions

**Nilai**: _____ / 10

### Topik 5: Demonstrasi Praktis (1.5-2 menit)

**Harus mencakup:**
- [ ] Panorama stitching demo
- [ ] View synthesis demo (jika applicable)
- [ ] Hasil dan analisis quality

**Nilai**: _____ / 10

---

## Checklist Teknis

### Pre-Recording
- [ ] Script/outline prepared
- [ ] Demo environment tested
- [ ] Recording software configured
- [ ] Microphone tested
- [ ] Lighting adequate

### Content
- [ ] Duration 7-10 minutes
- [ ] All required topics covered
- [ ] Accurate information
- [ ] Proper citations for sources

### Post-Production
- [ ] Audio levels normalized
- [ ] Background noise removed
- [ ] Transitions added
- [ ] Graphics/text readable
- [ ] Final review completed

---

## Perhitungan Nilai Akhir

```
Konten Materi:        _____ × 0.40 = _____
Kejelasan:            _____ × 0.25 = _____
Kualitas Produksi:    _____ × 0.20 = _____
Demonstrasi:          _____ × 0.15 = _____
                                    -------
Subtotal:                           _____

Bonus (jika ada):                   _____
Penalti (jika ada):                 _____
                                    -------
NILAI AKHIR:                        _____ / 100
```

---

## Bonus dan Penalti

### Bonus (maksimal +15%)
| Item | Poin | Kriteria |
|------|------|----------|
| Deep Dive NeRF | +5% | Penjelasan detail architecture dan training |
| Multiple Demos | +5% | Demo berbagai teknik (panorama + view synthesis + NeRF) |
| Original Visuals | +3% | Diagram dan animasi buatan sendiri |
| Comparative Analysis | +2% | Perbandingan kuantitatif metode |

### Penalti
| Item | Poin | Kriteria |
|------|------|----------|
| Durasi < 7 menit | -10% | Konten tidak lengkap |
| Durasi > 12 menit | -5% | Terlalu panjang |
| Plagiarisme | -100% | Copy dari sumber lain |
| Terlambat | -10%/hari | Maksimal 3 hari |
| Kualitas video buruk | -10% | Tidak dapat ditonton dengan nyaman |

---

## Contoh Struktur Video yang Baik

### Opening (30 detik)
- Perkenalan
- Overview topik
- Agenda

### Section 1: Konsep IBR (1 menit)
- Definisi dan motivasi
- Spektrum IBR
- Real-world applications

### Section 2: Light Fields & Panorama (2 menit)
- Plenoptic function
- Panorama pipeline
- Demo stitching

### Section 3: Neural Methods (2 menit)
- NeRF explanation
- Volume rendering
- 3D Gaussian Splatting

### Section 4: View Synthesis (1.5 menit)
- Warping techniques
- MPI representation
- Quality considerations

### Section 5: Demo (1.5 menit)
- Live demonstration
- Results analysis

### Closing (30 detik)
- Summary
- Key takeaways
- References

---

## Rubrik Kualitas Video

### Video Excellence Indicators

**Visual Quality:**
- 1080p atau lebih tinggi
- Stable footage (tripod/stabilization)
- Good lighting
- Clear screen recordings
- Professional graphics

**Audio Quality:**
- Clear voice recording
- No background noise
- Consistent volume levels
- Good pacing

**Content Quality:**
- Accurate information
- Proper terminology
- Logical flow
- Appropriate depth

**Engagement:**
- Varied visuals
- Relevant examples
- Good energy
- Clear explanations

---

## Resources untuk Membuat Video

### Recording Tools
- OBS Studio (free)
- Camtasia
- ScreenFlow (Mac)

### Editing Tools
- DaVinci Resolve (free)
- Adobe Premiere Pro
- Final Cut Pro (Mac)

### Graphics
- Canva (slides, graphics)
- Figma (diagrams)
- Manim (math animations)

### Audio
- Audacity (editing)
- Krisp (noise removal)

---

## Catatan Penilai

### Komentar Konten:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Penyampaian:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Produksi:
```
_________________________________________________________________
_________________________________________________________________
```

### Komentar Demo:
```
_________________________________________________________________
_________________________________________________________________
```

### Rekomendasi Perbaikan:
```
_________________________________________________________________
_________________________________________________________________
```

---

**Tanggal Penilaian**: _____________

**Penilai**: _____________

**Tanda Tangan**: _____________
