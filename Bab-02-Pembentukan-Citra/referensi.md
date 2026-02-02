# Referensi Bab 2: Pembentukan Citra

## 📚 Buku Utama

### Wajib
1. **Computer Vision: Algorithms and Applications, 2nd Edition**
   - Penulis: Richard Szeliski
   - Bab 2: Image Formation
   - Link: [szeliski.org/Book](https://szeliski.org/Book/)

2. **Multiple View Geometry in Computer Vision, 2nd Edition**
   - Penulis: Richard Hartley, Andrew Zisserman
   - Bab 2-6: Projective Geometry and Transformations
   - *Buku standar untuk geometri multi-view*

### Pendukung
3. **An Invitation to 3-D Vision**
   - Penulis: Yi Ma, Stefano Soatto, Jana Košecká, S. Shankar Sastry
   - Geometri proyektif dan rekonstruksi 3D

4. **Computer Vision: A Modern Approach, 2nd Edition**
   - Penulis: David Forsyth, Jean Ponce
   - Part I: Image Formation

---

## 📄 Paper Penting

### Camera Calibration
1. **A Flexible New Technique for Camera Calibration** (2000)
   - Penulis: Zhengyou Zhang
   - DOI: 10.1109/34.888718
   - *Metode kalibrasi Zhang - standar industri*

2. **Camera Calibration with Distortion Models and Accuracy Evaluation** (1994)
   - Penulis: Janne Heikkilä, Olli Silvén
   - *Model distorsi lensa komprehensif*

### Projective Geometry
3. **Direct Linear Transformation from Comparator Coordinates** (1971)
   - Penulis: Abdel-Aziz, Karara
   - *Paper klasik DLT untuk homography*

4. **In Defense of the Eight-Point Algorithm** (1997)
   - Penulis: Richard Hartley
   - *Normalisasi untuk stabilitas numerik*

### Image Formation
5. **A Computational Model of Lightness Perception** (1999)
   - Penulis: A. Gilchrist et al.
   - *Model pembentukan persepsi cahaya*

---

## 🎥 Video Tutorial

### YouTube
1. **First Principles of Computer Vision (Columbia)**
   - [Camera Model](https://www.youtube.com/watch?v=qByYk6JggQU)
   - [Camera Calibration](https://www.youtube.com/watch?v=j1M-b2hBXr0)
   - Channel: First Principles of Computer Vision

2. **Camera Calibration - OpenCV Tutorial**
   - [Camera Calibration using Python](https://www.youtube.com/watch?v=3h7wgR5fYik)
   - Channel: Programming Knowledge

3. **3Blue1Brown - Linear Algebra**
   - [Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
   - *Fundamental untuk memahami transformasi*

4. **Computerphile**
   - [How Digital Images Work](https://www.youtube.com/watch?v=06OzprhYO5E)
   - [Pinhole Cameras](https://www.youtube.com/watch?v=L1sd_fzTq3g)

---

## 📖 Online Resources

### Tutorials
1. **OpenCV Documentation - Camera Calibration**
   - [Camera Calibration Tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
   - Tutorial lengkap dengan kode

2. **Learn OpenCV - Camera Calibration**
   - [Camera Calibration using OpenCV](https://learnopencv.com/camera-calibration-using-opencv/)
   - Step-by-step guide

3. **CMU 16-385 Computer Vision**
   - [Lecture Notes on Projective Geometry](http://www.cs.cmu.edu/~16385/)
   - Materi kuliah CMU

### Interactive Demos
4. **Camera Matrix Calculator**
   - [Online K Matrix Calculator](https://ksimek.github.io/2012/08/13/introduction/)
   - Penjelasan visual matriks intrinsik

5. **Homography Playground**
   - [Interactive Homography Demo](https://codepen.io/collection/homography-demos)
   - Eksperimen transformasi perspektif

---

## 🛠️ Tools & Software

### Kalibrasi Kamera
1. **MATLAB Camera Calibrator App**
   - [Camera Calibrator](https://www.mathworks.com/help/vision/ug/using-the-single-camera-calibrator-app.html)
   - GUI untuk kalibrasi

2. **Kalibr (ROS)**
   - [Kalibr GitHub](https://github.com/ethz-asl/kalibr)
   - Kalibrasi multi-kamera dan IMU

3. **GML Camera Calibration Toolbox**
   - [GML C++ Toolbox](http://graphics.cs.msu.ru/en/node/909)
   - Library C++ untuk kalibrasi

### Visualisasi 3D
4. **PyVista**
   - [PyVista Documentation](https://docs.pyvista.org/)
   - 3D plotting untuk Python

5. **Plotly**
   - [Plotly 3D Scatter](https://plotly.com/python/3d-scatter-plots/)
   - Interactive 3D visualization

---

## 📋 Cheat Sheets

### Transformasi 2D
| Transformasi | DoF | Matriks | Invariant |
|--------------|-----|---------|-----------|
| Translation | 2 | [I \| t] | Jarak, sudut |
| Rotation | 1 | [R \| 0] | Jarak, sudut |
| Euclidean | 3 | [R \| t] | Jarak, sudut |
| Similarity | 4 | [sR \| t] | Sudut, ratio |
| Affine | 6 | [A \| t] | Garis paralel |
| Projective | 8 | [H] | Garis lurus |

### Model Distorsi
```
Radial: r' = r(1 + k1*r² + k2*r⁴ + k3*r⁶)
Tangensial: 
    x' = x + [2*p1*xy + p2*(r² + 2x²)]
    y' = y + [p1*(r² + 2y²) + 2*p2*xy]
```

### Proyeksi Perspektif
```
            | f   0   cx |   | r11 r12 r13 tx |
P = K[R|t] =| 0   f   cy | * | r21 r22 r23 ty |
            | 0   0   1  |   | r31 r32 r33 tz |
```

---

## 🌐 Communities & Forums

### Stack Overflow
- Tag: [camera-calibration](https://stackoverflow.com/questions/tagged/camera-calibration)
- Tag: [homography](https://stackoverflow.com/questions/tagged/homography)
- Tag: [opencv-python](https://stackoverflow.com/questions/tagged/opencv-python)

### Reddit
- r/computervision - General CV discussions
- r/opencv - OpenCV specific

### Discord
- [OpenCV Discord](https://discord.gg/opencv)
- [Computer Vision Discord](https://discord.gg/computervision)

---

## 💻 Kode Referensi

### Repository GitHub
1. **OpenCV Samples**
   - [Camera Calibration Samples](https://github.com/opencv/opencv/tree/master/samples/python/calibration)
   - Official examples

2. **Camera Calibration Examples**
   - [kornia](https://github.com/kornia/kornia)
   - Differentiable computer vision library

3. **PyTorch3D**
   - [PyTorch3D Camera](https://github.com/facebookresearch/pytorch3d)
   - Camera models in PyTorch

---

## 📝 Latihan Tambahan

### Online Judges / Platforms
1. **Kaggle Notebooks**
   - Search: "Camera Calibration"
   - Many worked examples

2. **Google Colab Templates**
   - [Camera Projection Demo](https://colab.research.google.com/)
   - Search for camera transformation notebooks

### Problem Sets
3. **Stanford CS231A**
   - [Problem Sets](https://web.stanford.edu/class/cs231a/)
   - Camera models assignments

4. **MIT 6.801/6.866**
   - [Machine Vision Course](https://ocw.mit.edu/courses/6-801-machine-vision-fall-2004/)
   - Problem sets dengan solusi

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| OpenCV Camera Calibration | [Link](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) |
| Hartley & Zisserman Book | [Link](https://www.robots.ox.ac.uk/~vgg/hzbook/) |
| Zhang's Calibration Paper | [Link](https://www.microsoft.com/en-us/research/publication/a-flexible-new-technique-for-camera-calibration/) |
| Camera Matrix Tutorial | [Link](https://ksimek.github.io/2013/08/13/intrinsic/) |
| Homography Tutorial | [Link](https://www.learnopencv.com/homography-examples-using-opencv-python-c/) |

---

## 📌 Key Concepts Summary

### Yang Harus Dikuasai
1. ✅ Koordinat homogen dan konversi
2. ✅ Hierarki transformasi 2D
3. ✅ Model kamera pinhole
4. ✅ Matriks intrinsik K
5. ✅ Matriks ekstrinsik [R|t]
6. ✅ Distorsi lensa (radial & tangensial)
7. ✅ Proses kalibrasi kamera
8. ✅ Estimasi homography dengan DLT

### Formula Penting
```python
# Proyeksi 3D ke 2D
p = K @ (R @ P + t)
u, v = p[0]/p[2], p[1]/p[2]

# Homography
p' = H @ p  # dalam koordinat homogen

# Undistort
r² = x² + y²
x_distorted = x(1 + k1*r² + k2*r⁴) + 2*p1*xy + p2*(r² + 2x²)
```

---

**Selamat belajar!** 📖✨
