# QUICK START GUIDE
## Bab 10: Computational Photography

---

## 🚀 MEMULAI PRAKTIKUM

### Step 1: Setup Data (HANYA SEKALI)
```bash
cd Bab-10-Computational-Photography/praktikum
python3 download_sample_data.py
```

Output:
```
✅ Semua data berhasil disiapkan!
```

### Step 2: Jalankan Program
```bash
# Program 1: HDR Imaging
python3 01_hdr_imaging.py

# Program 2: Exposure Fusion
python3 02_exposure_fusion.py

# Program 3: Image Denoising
python3 03_denoising.py

# Program 4: Synthetic Bokeh
python3 04_synthetic_bokeh.py

# Program 5: Image Enhancement
python3 05_image_enhancement.py

# Program 6: Multi-Frame Enhancement
python3 06_multi_frame_enhancement.py
```

**Note**: Semua window akan otomatis tertutup setelah 2 detik

---

## 📚 ALUR PEMBELAJARAN

### Minggu 1: Foundation
1. **Baca**: Materi.md Bab 1-2 (Intro & HDR)
2. **Praktikum**: Program 1 (HDR Imaging)
3. **Eksperimen**: Modify GAMMA, SATURATION
4. **Tugas**: Ambil 3 foto bracket sendiri, buat HDR

### Minggu 2: Advanced Techniques
1. **Baca**: Materi.md Bab 3-4 (Denoising & Focus)
2. **Praktikum**: Program 2-4 (Fusion, Denoising, Bokeh)
3. **Eksperimen**: Compare denoising methods
4. **Tugas**: Algorithm comparison report

### Minggu 3: Enhancement & Integration
1. **Baca**: Materi.md Bab 5-9 (SR, Workflows)
2. **Praktikum**: Program 5-6 (Enhancement, Multi-frame)
3. **Eksperimen**: Create enhancement pipeline
4. **Tugas**: Final project

---

## 🔧 MODIFIKASI PARAMETER

### Program 1: HDR Imaging
```python
# Line ~50-55
GAMMA = 2.2          # Try: 1.0-3.0 (brightness)
SATURATION = 1.2     # Try: 0.5-2.0 (color intensity)
CONTRAST = 0.5       # Try: 0.0-2.0 (dynamic range)
```

### Program 2: Exposure Fusion
```python
# Line ~45-50
CONTRAST_WEIGHT = 1.0      # Try: 0.0-2.0
SATURATION_WEIGHT = 1.0    # Try: 0.0-2.0
EXPOSURE_WEIGHT = 1.0      # Try: 0.0-2.0
```

### Program 3: Denoising
```python
# Line ~50-55
GAUSSIAN_KERNEL = 5        # Try: 3, 5, 7, 9
BILATERAL_D = 9            # Try: 5, 9, 15
NLM_H = 10                 # Try: 5, 10, 15, 20
```

### Program 4: Synthetic Bokeh
```python
# Line ~50-55
FOCAL_DISTANCE = 0.4       # Try: 0.0-1.0
APERTURE = 2.8             # Try: 1.4, 2.8, 5.6
BLUR_SIZE = 15             # Try: 5, 10, 15, 20
```

### Program 5: Image Enhancement
```python
# Line ~50-55
CLAHE_CLIP = 2.0           # Try: 1.0-5.0
SATURATION_SCALE = 1.3     # Try: 0.5-2.0
SHARPNESS_AMOUNT = 1.5     # Try: 0.5-3.0
```

### Program 6: Multi-Frame Enhancement
```python
# Line ~50-55
NUM_FRAMES = 8             # Try: 2, 4, 8, 16
NOISE_SIGMA = 25           # Try: 10, 25, 50
```

---

## 📂 STRUKTUR OUTPUT

Semua output disimpan di folder `output/`:

```
output/
├── 01_hdr_image.hdr                    # HDR radiance map
├── 01_tonemap_drago.jpg                # Tone mapped hasil
├── 01_tonemap_reinhard.jpg
├── 01_tonemap_mantiuk.jpg
├── 01_hdr_comparison.png               # Side-by-side comparison
├── 02_fusion_mertens.jpg               # Exposure fusion hasil
├── 03_denoised_nlm.jpg                 # Denoised image
├── 03_denoising_comparison.png         # Method comparison
├── 04_bokeh_comparison.png             # Bokeh effects
├── 05_enhancement_comparison.png       # Enhancement results
└── 06_multiframe_comparison.png        # Multi-frame averaging
```

---

## 🎯 TIPS PRAKTIKUM

### Untuk Hasil Terbaik:

1. **HDR Photography**:
   - Gunakan tripod jika ada
   - Ambil 3-7 bracket exposures (EV -2, -1, 0, +1, +2)
   - Scene dengan high contrast (window, sunset)

2. **Denoising**:
   - Test pada foto ISO tinggi (3200+)
   - Compare PSNR/SSIM values
   - Observe texture preservation

3. **Bokeh**:
   - Portrait dengan background jauh
   - Clear subject separation
   - Experiment dengan focal distance

4. **Enhancement**:
   - Start dengan underexposed foto
   - Try different combinations
   - Avoid over-processing

5. **Multi-Frame**:
   - Handheld burst ok (program handle alignment)
   - More frames = less noise (√N improvement)
   - Trade-off: motion blur vs noise reduction

---

## 🐛 TROUBLESHOOTING

### "No module named 'cv2'"
```bash
pip install opencv-python opencv-contrib-python
```

### "No module named 'skimage'"
```bash
pip install scikit-image
```

### "No bracket images found"
```bash
python3 download_sample_data.py
```

### Window tidak muncul
- Normal! Auto-close setelah 2 detik
- Check folder `output/` untuk hasil

### Ingin interactive mode
Modify program:
```python
# Change line:
cv2.waitKey(2000)   # 2 second auto-close

# To:
cv2.waitKey(0)      # Wait for keypress
```

---

## 📊 METRICS EXPLAINED

### PSNR (Peak Signal-to-Noise Ratio)
- Higher = Better
- > 40 dB: Excellent
- 30-40 dB: Good
- < 30 dB: Poor

### SSIM (Structural Similarity Index)
- Range: 0.0 - 1.0
- 1.0 = Identical
- > 0.9: Excellent
- 0.8-0.9: Good
- < 0.8: Poor

---

## 🔗 RESOURCES

### Documentation
- [Materi.md](Materi.md) - Complete theory dengan real-world examples
- [Jobsheet.md](Jobsheet.md) - Detailed experiments
- [Project.md](Project.md) - Project guidelines
- [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) - Complete verification

### Sample Workflows
See Materi.md Section 9.2:
- Real estate photography
- Smartphone night photography
- Portrait enhancement

### References
See [Referensi.md](Referensi.md):
- 10 textbooks
- 50 academic papers
- Online resources

---

## ✅ CHECKLIST PRAKTIKUM

Sebelum submit laporan, pastikan:

- [ ] Semua 6 program berhasil dijalankan
- [ ] Screenshot/foto hasil dari output folder
- [ ] Parameter experiments documented
- [ ] PSNR/SSIM values recorded (Program 3)
- [ ] Before/after comparisons analyzed
- [ ] Real-world application discussed
- [ ] Trade-offs understood
- [ ] Code modifications tested
- [ ] Laporan format sesuai rubrik
- [ ] References cited properly

---

## 🎓 LEARNING OBJECTIVES

Setelah praktikum, Anda harus bisa:

✅ Explain computational photography concepts  
✅ Implement HDR imaging pipeline  
✅ Apply appropriate denoising methods  
✅ Create synthetic bokeh effects  
✅ Enhance images systematically  
✅ Understand multi-frame techniques  
✅ Analyze quality metrics  
✅ Design enhancement workflows  

---

## 💡 NEXT STEPS

### Untuk Project:
1. Choose real-world application
2. Design enhancement pipeline
3. Implement dengan program basis
4. Test dengan real photos
5. Document results
6. Present findings

### Untuk Self-Learning:
1. Try programs dengan your own photos
2. Experiment dengan extreme parameters
3. Combine techniques (HDR + denoising)
4. Research deep learning methods
5. Build real-time applications

---

**Quick Help**: Jika ada error atau pertanyaan, check:
1. VERIFICATION_REPORT.md untuk troubleshooting
2. Program docstrings untuk detailed explanation
3. Materi.md untuk theory background

**Happy Learning! 🚀📷**
