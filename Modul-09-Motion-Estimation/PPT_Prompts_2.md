# PPT Prompt 2 — Modul 09: Motion Estimation (Panduan Desain & Narasi)

## Panduan Desain Visual Lengkap

### 1. Tema dan Warna

#### Color Palette Primary
```
Background:  #1a1a2e (Navy Dark)
Accent 1:    #00ff88 (Neon Green) - untuk highlight motion/flow
Accent 2:    #00d4ff (Cyan) - untuk technical elements
Text:        #f5f5f5 (Off-white)
Code BG:     #2d2d44 (Dark Purple)
```

#### Color Palette Secondary
```
Warning:     #ffd93d (Yellow) - untuk catatan penting
Error:       #ff6b6b (Soft Red) - untuk limitation/pitfalls
Success:     #6bcf7f (Mint Green) - untuk best practices
Neutral:     #95a5a6 (Gray) - untuk secondary info
```

#### Penggunaan Warna untuk Optical Flow Visualization
- **Motion ke kanan:** Red (#ff0000)
- **Motion ke kiri:** Cyan (#00ffff)
- **Motion ke atas:** Blue (#0000ff)
- **Motion ke bawah:** Yellow (#ffff00)
- **No motion:** Black/Dark gray
- **Magnitude:** Brightness/Saturation

### 2. Typography System

```
H1 (Slide Title):     Montserrat Bold, 44pt, #00ff88
H2 (Section):         Montserrat Semibold, 36pt, #00d4ff
H3 (Subsection):      Roboto Bold, 28pt, #f5f5f5
Body Text:            Open Sans Regular, 20pt, #e0e0e0
Code:                 Fira Code, 16pt, #a8dadc
Caption:              Open Sans Light, 14pt, #95a5a6
Bullet Points:        18-20pt, sufficient line spacing (1.5)
```

### 3. Layout Templates

#### Template A - Theory Slide
```
┌──────────────────────────────────────────┐
│ Title (H1)                          Icon │
├──────────────────────────────────────────┤
│                                          │
│  [Visual/Diagram]     • Point 1          │
│   50% width           • Point 2          │
│                       • Point 3          │
│                       • Point 4          │
│                                          │
├──────────────────────────────────────────┤
│ Footer: Module 09 | Slide #              │
└──────────────────────────────────────────┘
```

#### Template B - Code Example
```
┌──────────────────────────────────────────┐
│ Title + Brief Explanation                │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ # Code dengan syntax highlighting  │  │
│  │ import cv2                         │  │
│  │ flow = cv2.calcOpticalFlowPyrLK()  │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Output Preview        Parameters Info   │
│  [Image/Result]        • param1: value   │
│                       • param2: value   │
│                                          │
└──────────────────────────────────────────┘
```

#### Template C - Comparison
```
┌──────────────────────────────────────────┐
│ Title: Comparison                        │
├──────────────────────────────────────────┤
│                                          │
│  Method A          vs          Method B  │
│  ┌──────────┐              ┌──────────┐  │
│  │ Visual   │              │ Visual   │  │
│  └──────────┘              └──────────┘  │
│  • Pro 1                   • Pro 1       │
│  • Pro 2                   • Pro 2       │
│  • Con 1                   • Con 1       │
│                                          │
│  [Comparison Table]                      │
│                                          │
└──────────────────────────────────────────┘
```

### 4. Visual Assets Required

#### Diagrams yang Harus Dibuat
1. **Optical Flow Concept**
   - Two frames side by side
   - Arrows showing motion vectors
   - Color-coded by direction

2. **Brightness Constancy**
   - Pixel intensity graph
   - Before/after movement
   - Equation overlay

3. **Lucas-Kanade Window**
   - Feature point dengan window
   - Neighborhood pixels highlighted
   - Flow vector calculated

4. **Image Pyramid**
   - 3-level pyramid visual
   - Annotations: coarse → fine
   - Flow propagation arrows

5. **HSV Color Wheel**
   - 360° wheel dengan labels
   - Direction to color mapping
   - Magnitude gradient

6. **Dense vs Sparse Comparison**
   - Split screen
   - Sparse: feature points only
   - Dense: full flow field

7. **Video Stabilization Pipeline**
   - Flowchart: Input → Estimation → Smoothing → Warping → Output
   - Visual examples at each stage

8. **Background Subtraction**
   - Original → Mask → Foreground
   - MOG2 visualization

#### Icons Needed
- 🎥 Camera/Video
- 🎯 Target/Tracking
- ⚡ Speed/Fast
- 🎨 Color/Visualization
- 🔍 Detection
- 📊 Analysis/Graph
- ⚙️ Settings/Parameters
- ✅ Success/Correct
- ⚠️ Warning/Limitation

### 5. Animation Guidelines

#### Subtle Animations (Recommended)
```
Entry Animations:
- Fade in (0.3s): untuk text dan images
- Wipe from left (0.5s): untuk comparisons
- Zoom in (0.4s): untuk key concepts

Emphasis:
- Pulse: untuk important numbers/terms
- Highlight: untuk code lines
- Arrow motion: untuk flow direction

Exit:
- Fade out (0.2s): standard transition
```

#### Avoid
- Spinning, bouncing, atau overly flashy effects
- Automatic advance (biarkan presenter control)
- Sound effects (kecuali untuk demo videos)

### 6. Demo Video Production

#### Spesifikasi Video
```
Resolution:   1920x1080 (Full HD)
Frame Rate:   30 fps
Duration:     10-20 seconds per demo
Format:       MP4 (H.264)
Audio:        Optional, soft background music
Captions:     Ya, untuk key information
```

#### Video Content Guidelines
1. **Lucas-Kanade Demo:**
   - Start: Clear frame dengan objects
   - Middle: Tracking trails appear
   - End: Full trajectory visualization
   - Text overlay: "Sparse Optical Flow - Lucas-Kanade"

2. **Dense Flow Demo:**
   - Start: Normal video
   - Transition: Fade to HSV visualization
   - Highlight: Color meaning explanation
   - Text overlay: "Dense Optical Flow - Farneback"

3. **Motion Detection Demo:**
   - Start: Static scene
   - Event: Person enters frame
   - Result: Bounding box appears
   - Text overlay: "Real-time Motion Detection"

#### Video Editing Tips
- Add slow-motion (0.5x) untuk complex motions
- Split screen untuk before/after
- Circle/arrow annotations untuk focus areas
- Consistent branding (logo corner)

## Panduan Narasi Presentasi

### 1. Opening Strategy (Slide 1-3)

#### Hook - First 30 Seconds
```
"Pernahkah Anda bertanya bagaimana smartphone Anda bisa 
menstabilkan video yang goyang? Atau bagaimana mobil 
self-driving bisa memahami pergerakan di sekitarnya?"

[Tampilkan contoh visual yang relatable]

"Semua ini dimungkinkan oleh teknologi MOTION ESTIMATION 
dan OPTICAL FLOW yang akan kita pelajari hari ini."
```

#### Build Credibility
- Mention aplikasi industri yang familiar
- Reference teknologi yang mereka gunakan daily
- Connect dengan materi sebelumnya (feature detection)

### 2. Explaining Complex Concepts

#### Brightness Constancy (Abstract → Concrete)
```
JANGAN:
"Brightness constancy assumption states that I(x,y,t) = I(x+dx,y+dy,t+dt)"

LAKUKAN:
"Bayangkan Anda menutup mata sebentar. Saat membuka mata,
Anda masih bisa mengenali objek yang sama meski sudah 
bergerak. Kenapa? Karena BRIGHTNESS objek tersebut tidak 
berubah, hanya POSISInya saja.

Ini adalah BRIGHTNESS CONSTANCY - asumsi fundamental dalam
optical flow. [Tunjukkan diagram visual]"
```

#### Aperture Problem
```
"Coba lihat slide ini melalui lubang kecil [simulasi].
Anda hanya melihat garis. Ke arah mana garis ini bergerak?
Atas? Diagonal? Susah kan?

Ini adalah APERTURE PROBLEM - kenapa kita perlu melihat 
NEIGHBORHOOD, bukan hanya satu pixel."
```

### 3. Differentiating Sparse vs Dense

#### Use Analogy
```
"Sparse Optical Flow seperti GPS tracking:
- Kita track beberapa titik penting (landmark)
- Cepat dan efisien
- Cukup untuk navigasi

Dense Optical Flow seperti weather radar:
- Kita monitoring setiap titik di area
- Lebih lambat tapi lebih detail
- Perlu untuk analisis mendalam

Pilih sesuai kebutuhan Anda!"
```

### 4. Transition Phrases

#### Moving Between Topics
```
Theory → Implementation:
"Sekarang teori sudah clear, mari kita lihat bagaimana 
mengimplementasikannya dengan OpenCV..."

Concept → Application:
"Konsep ini mungkin terdengar abstrak. Tapi lihat aplikasi
nyatanya di..."

Problem → Solution:
"Lucas-Kanade punya keterbatasan untuk large motion. 
Solusinya? Image pyramid..."
```

### 5. Demo Narration

#### During Live Demo
```
"Perhatikan video ini. [Pause 2 detik]

Saat pemain berlari, Anda lihat tracking trails berwarna?
[Point ke screen] 
- Warna merah: gerakan ke kanan
- Warna biru: gerakan ke atas
- Intensity: seberapa cepat

Ini adalah real-time tracking dengan Lucas-Kanade.
Cepat kan? Hanya 30ms per frame!"
```

### 6. Addressing Limitations

#### Be Honest About Trade-offs
```
"Lucas-Kanade memang cepat, TAPI...
[Pause untuk emphasis]

Gagal pada kondisi:
1. Large motion - solusi: pyramid
2. Illumination change - solusi: normalization  
3. Occlusion - solusi: re-detection

Tidak ada algoritma yang perfect. Pilih sesuai context."
```

### 7. Connecting to Real World

#### Case Study Examples

**Example 1: Tesla Autopilot**
```
"Tesla menggunakan optical flow untuk mengestimasi:
- Ego-motion (pergerakan mobil sendiri)
- Object motion (mobil lain, pejalan kaki)
- Time-to-collision

Dense optical flow di 8 kamera, real-time!
Ini bukan sci-fi, ini production system hari ini."
```

**Example 2: Smartphone Camera**
```
"Google Pixel 'Night Sight':
1. Ambil 15 burst photos
2. Estimasi motion dengan optical flow
3. Align semua frames
4. Merge → foto low-light tanpa blur

Semua ini dalam <1 detik. Magic? No, optical flow!"
```

**Example 3: Sports Analytics**
```
"Premier League tracking:
- 25 pemain + bola + referee
- 60 minutes match
- Heatmap, speed, distance traveled

Lucas-Kanade untuk initial tracking,
Kalman filter untuk smoothing."
```

### 8. Interactive Elements

#### Polling Questions
```
Slide 10 - After explaining LK:
"Quick poll: Menurut Anda, Lucas-Kanade lebih cocok untuk:
A) Security camera (slow motion)
B) Sports analysis (fast motion)  
C) Medical imaging (high precision)
Jawab di chat!"

Slide 20 - Dense vs Sparse:
"Jika Anda develop aplikasi video compression,
pilih sparse atau dense flow? Why?"
```

### 9. Handling Questions

#### Prepared Responses

**Q: "Kenapa tidak pakai deep learning saja?"**
```
A: "Great question! Deep learning (RAFT, PWC-Net) memang
lebih akurat, TAPI:
- Perlu GPU (Lucas-Kanade: CPU cukup)
- Model size 50MB+ (LK: built-in OpenCV)
- Inference 20ms (LK: 2ms)

Untuk edge devices atau real-time system, classical methods
masih very relevant!"
```

**Q: "Bagaimana handle occlusion?"**
```
A: "Occlusion is challenging. Strategi:
1. Track confidence score
2. Re-detection jika confidence drop
3. Kalman filter untuk prediction
4. Multiple hypothesis tracking

Ini topik lanjut, nanti di project Anda bisa explore!"
```

### 10. Closing Strong

#### Summary dengan Actionable Takeaways
```
"Hari ini kita belajar Motion Estimation. Key takeaways:

1. Optical flow = motion field visualization
2. Sparse (LK) = fast, dense (Farneback) = detailed
3. Pilih method berdasarkan: speed, accuracy, resources

Next steps untuk Anda:
- Run 8 praktikum programs
- Experiment dengan parameters
- Apply di project: MotionGuard system

Questions? Let's discuss!"
```

## Technical Presentation Tips

### 1. Screen Setup
- **Dual Monitor:** PPT di presenter view, audience view di proyektor
- **Backup:** PDF version siap jika PPTX error
- **Videos:** Local files, bukan streaming (avoid network issues)

### 2. Timing Management
```
Introduction:     5-7 minutes
Theory:          15-20 minutes
Methods:         15-20 minutes  
Applications:    10-12 minutes
Demo:             8-10 minutes
Praktikum:        5-7 minutes
Q&A:              5-10 minutes
Total:           63-86 minutes (target: 70 minutes)
```

### 3. Engagement Strategies
- Ask rhetorical questions
- "Raise hand if you've used..."
- Live demo jika memungkinkan
- Call-back ke contoh sebelumnya
- Use humor (appropriately)

### 4. Accessibility
- High contrast colors
- Large fonts (min 18pt)
- Describe images verbally
- Provide slide deck before/after
- Caption untuk videos

## Quality Assurance Checklist

### Content
- [ ] All technical terms defined
- [ ] Math equations explained intuitively
- [ ] Code examples tested
- [ ] Citations for external content
- [ ] Consistent terminology throughout

### Design
- [ ] Color contrast ratio > 4.5:1
- [ ] Font size readable from back row
- [ ] No orphaned headers
- [ ] Consistent layout across slides
- [ ] Visual hierarchy clear

### Media
- [ ] All images high-resolution
- [ ] Videos play smoothly
- [ ] Animations not distracting
- [ ] Loading time < 3s per slide

### Delivery
- [ ] Speaker notes prepared
- [ ] Timing rehearsed
- [ ] Backup plan ready
- [ ] Interactive elements tested

---

**Final Note:** Presentasi yang baik adalah yang membuat audience paham DAN excited tentang topik. Balance antara rigor akademis dan praktikalitas real-world. Good luck! 🎯
