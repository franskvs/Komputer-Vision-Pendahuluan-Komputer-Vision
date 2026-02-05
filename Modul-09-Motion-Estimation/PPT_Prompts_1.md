# PPT Prompt 1 — Modul 09: Motion Estimation dan Optical Flow

## Instruksi Pembuatan Presentasi

Buat presentasi PowerPoint profesional untuk **Modul 09: Motion Estimation dan Optical Flow**. 

### Sumber Materi
Gunakan sebagai referensi:
- Materi.md (teori dan konsep)
- Jobsheet.md (praktikum dan implementasi)
- Project.md (aplikasi real-world)
- Referensi.md (paper dan buku)
- praktikum/*.py (contoh kode)

### Target
- **Jumlah Slide:** 28-35 slide
- **Durasi Presentasi:** 60-75 menit
- **Audience:** Mahasiswa tingkat menengah dengan dasar computer vision

## Struktur Slide Detail

### 1. Opening (3 slide)
- **Slide 1:** Cover Page
  - Judul: "Motion Estimation dan Optical Flow"
  - Subtitle: "Menganalisis Pergerakan dalam Video"
  - Nama dosen, kode mata kuliah, semester
  - Visual: Contoh optical flow visualization yang menarik

- **Slide 2:** Agenda
  - Overview materi hari ini
  - Timeline presentasi
  - Ekspektasi pembelajaran

- **Slide 3:** Learning Outcomes
  - 6-8 poin learning objectives yang spesifik
  - Menggunakan Bloom's taxonomy
  - Terkait dengan kompetensi industri

### 2. Introduction (4-5 slide)
- **Slide 4:** Motivasi - Mengapa Motion Estimation Penting?
  - 3-4 aplikasi real-world dengan visual
  - Video surveillance, autonomous vehicles, video compression
  - Smartphone camera stabilization
  - Sports analytics

- **Slide 5:** Definisi Motion Estimation
  - Definisi formal dengan bahasa sederhana
  - Diagram: Frame t → Frame t+1 dengan motion vectors
  - Perbedaan dengan static image processing

- **Slide 6:** Optical Flow - Konsep Dasar
  - Definisi optical flow
  - Visual representation dengan arrows
  - Brightness constancy assumption

- **Slide 7:** Brightness Constancy Equation
  - Persamaan matematis: I(x,y,t) = I(x+dx, y+dy, t+dt)
  - Taylor expansion
  - Optical flow equation: Ix*u + Iy*v + It = 0
  - Penjelasan setiap komponen

- **Slide 8:** Aperture Problem
  - Ilustrasi visual aperture problem
  - Mengapa single pixel tidak cukup
  - Solusi: gunakan neighborhood

### 3. Sparse Optical Flow (5-6 slide)
- **Slide 9:** Lucas-Kanade Method - Overview
  - Karakteristik: sparse, efficient, feature-based
  - 3 Asumsi utama dengan visual
  - Use cases: tracking, video stabilization

- **Slide 10:** Lucas-Kanade - Matematis
  - Window/neighborhood concept
  - Over-determined system
  - Least squares solution
  - Diagram matrix equation

- **Slide 11:** Pyramid/Multi-scale Approach
  - Diagram image pyramid (3 levels)
  - Coarse-to-fine estimation
  - Handling large motions
  - Trade-off: accuracy vs speed

- **Slide 12:** Lucas-Kanade - Implementation
  - OpenCV function: cv2.calcOpticalFlowPyrLK()
  - Key parameters explained:
    - winSize, maxLevel, criteria
  - Code snippet sederhana
  - Visual result: tracking trails

- **Slide 13:** Demo Video - Sparse Flow
  - Embedded short video (10-15 detik)
  - Feature tracking pada objek bergerak
  - Highlight: colored tracking trails

- **Slide 14:** Kelebihan & Keterbatasan Lucas-Kanade
  - Tabel perbandingan pros/cons
  - Kondisi gagal: occlusion, illumination change
  - Best practices

### 4. Dense Optical Flow (5-6 slide)
- **Slide 15:** Dense Optical Flow - Overview
  - Definisi: flow untuk setiap pixel
  - Perbedaan dengan sparse flow (tabel)
  - Visual: sparse points vs dense field

- **Slide 16:** Farneback Method
  - Polynomial expansion approach
  - Multi-scale pyramid
  - Smoother, more complete flow field

- **Slide 17:** Flow Visualization - HSV Color Coding
  - Diagram color wheel
  - Hue = direction (angle)
  - Saturation = magnitude (speed)
  - Contoh visual dengan arah panah

- **Slide 18:** Dense Flow - Implementation
  - OpenCV: cv2.calcOpticalFlowFarneback()
  - Parameters: pyr_scale, levels, winsize
  - Code snippet
  - Visual result: colorful flow field

- **Slide 19:** Horn-Schunck Method (Brief)
  - Global smoothness constraint
  - Energy minimization
  - Comparison dengan Farneback

- **Slide 20:** Demo Video - Dense Flow
  - Video 15 detik dengan HSV visualization
  - Interpretasi warna pada berbagai gerakan

### 5. Advanced Topics (3-4 slide)
- **Slide 21:** Translational Alignment
  - SSD (Sum of Squared Differences)
  - Phase Correlation (Fourier-based)
  - Application: image registration, stabilization

- **Slide 22:** Frame Interpolation
  - Creating intermediate frames
  - Bi-directional flow
  - Slow-motion effects
  - Visual: Frame 1 → Interpolated → Frame 2

- **Slide 23:** Deep Learning Methods (Overview)
  - FlowNet, PWC-Net, RAFT
  - CNN-based optical flow
  - Accuracy vs speed comparison chart
  - Industry adoption

### 6. Applications (4-5 slide)
- **Slide 24:** Application 1 - Object Tracking
  - Kalman filter + optical flow
  - Multi-object tracking
  - Real-world case: traffic monitoring

- **Slide 25:** Application 2 - Video Stabilization
  - Pipeline diagram: motion estimation → smoothing → warping
  - Before/after comparison
  - GoPro, smartphone examples

- **Slide 26:** Application 3 - Motion Detection
  - Background subtraction
  - Surveillance systems
  - Security applications

- **Slide 27:** Application 4 - Video Compression
  - MPEG motion compensation
  - P-frames and B-frames
  - Block matching algorithms

- **Slide 28:** More Applications
  - Sports analytics: player tracking
  - Medical imaging: ultrasound tracking
  - Autonomous vehicles: scene flow
  - Augmented reality: camera pose

### 7. Praktikum Overview (3 slide)
- **Slide 29:** Praktikum - 8 Percobaan
  - List semua percobaan dengan icon
  - 01: Lucas-Kanade ✓
  - 02: Dense Flow ✓
  - 03: Motion Detection ✓
  - 04: Object Tracking ✓
  - 05: Motion History ✓
  - 06: Video Stabilization ✓
  - 07: Translational Alignment ✓
  - 08: Frame Interpolation ✓

- **Slide 30:** Setup dan Requirements
  - Python 3.8+, OpenCV 4.8+
  - Sample data dan video
  - Expected outputs per percobaan
  - Tips untuk sukses

- **Slide 31:** Project - MotionGuard System
  - Smart home security dengan motion detection
  - Fitur-fitur utama
  - Deliverables dan rubrik penilaian

### 8. Comparison & Analysis (2 slide)
- **Slide 32:** Trade-offs: Akurasi vs Kecepatan
  - Tabel comparison:
    - Method | Accuracy | Speed | Memory | Use Case
  - Lucas-Kanade vs Farneback vs Deep Learning
  - Decision tree: kapan pakai yang mana

- **Slide 33:** Best Practices
  - Pre-processing: denoise, resize
  - Parameter tuning guidelines
  - Common pitfalls dan solusinya
  - Debugging tips

### 9. Closing (2-3 slide)
- **Slide 34:** Summary - Key Takeaways
  - 6-8 poin penting yang harus diingat
  - Visual mindmap/flowchart

- **Slide 35:** Resources & Further Learning
  - Buku referensi (3-4 recommended)
  - Online courses dan tutorials
  - Datasets untuk practice: Middlebury, KITTI
  - OpenCV documentation links

- **Slide 36:** Q&A
  - Contact information
  - Office hours
  - Forum diskusi

## Ketentuan Design & Visual

### Gaya Visual
- **Color Scheme:** Profesional, gelap dengan aksen terang
  - Background: Dark gray/navy (#1a1a2e atau #16213e)
  - Accent: Cyan/teal (#00d4ff atau #0dcaf0) untuk highlights
  - Text: White/light gray untuk readability

### Typography
- **Heading:** Sans-serif bold (Montserrat, Roboto)
- **Body:** Sans-serif regular (Open Sans, Lato)
- **Code:** Monospace (Fira Code, Consolas)

### Layout Guidelines
- Jangan overcrowd - max 6-7 poin per slide
- Gunakan white space effectively
- Consistent margins dan spacing
- Icon untuk visual interest

### Visual Requirements
- **Minimum 15 diagram/illustration** original
- **3-4 short video demos** (10-20 detik each)
- **Flow field visualization** dengan color coding
- **Before/after comparison** untuk aplikasi
- **Code snippets** dengan syntax highlighting
- **Animated transitions** untuk flow concepts (subtle)

### Specific Visual Elements Wajib
1. Optical flow arrows overlay pada video frame
2. HSV color wheel dengan direction labels
3. Image pyramid diagram (3 levels minimum)
4. Comparison table: sparse vs dense
5. Pipeline diagram untuk video stabilization
6. Real-world application screenshots

## Narasi dan Delivery

### Tone
- Profesional namun approachable
- Explain complex concepts dengan analogies
- Real-world examples untuk setiap konsep

### Storytelling
- Mulai dengan problem statement
- Build dari simple ke complex
- Connect setiap concept dengan aplikasi

### Technical Depth
- Balance teori dan praktik
- Matematis explain secara intuitive
- Code examples harus runnable

## Quality Checklist

Sebelum finalisasi, pastikan:
- [ ] Semua slide memiliki header/footer konsisten
- [ ] Semua diagram memiliki caption
- [ ] Code snippets tested dan correct
- [ ] Videos embedded dengan baik
- [ ] No typos atau grammar errors
- [ ] Citation untuk gambar/video dari sumber lain
- [ ] Konsisten dalam terminology
- [ ] Navigation clear (slide numbers)
- [ ] Accessible (contrast ratio, font size min 18pt)
- [ ] Export ke PDF backup

## Deliverables

1. **PowerPoint file (.pptx)** dengan embedded media
2. **PDF version** untuk distribution
3. **Video files** terpisah (jika ukuran terlalu besar)
4. **Speaker notes** untuk setiap slide teknis
5. **Quiz/polling questions** (5-7 questions) untuk engagement
