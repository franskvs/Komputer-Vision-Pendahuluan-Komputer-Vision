# Referensi Bab 3: Pemrosesan Citra

## 📚 Buku Utama

### Wajib
1. **Computer Vision: Algorithms and Applications, 2nd Edition**
   - Penulis: Richard Szeliski
   - Bab 3: Image Processing
   - Link: [szeliski.org/Book](https://szeliski.org/Book/)

2. **Digital Image Processing, 4th Edition**
   - Penulis: Rafael C. Gonzalez, Richard E. Woods
   - Bab 3-6: Spatial & Frequency Domain Processing
   - *"Bible" untuk image processing*

### Pendukung
3. **Image Processing, Analysis, and Machine Vision**
   - Penulis: Milan Sonka, Vaclav Hlavac, Roger Boyle
   - Comprehensive coverage

4. **Fundamentals of Digital Image Processing**
   - Penulis: Anil K. Jain
   - Strong theoretical foundation

---

## 📄 Paper Penting

### Edge Detection
1. **A Computational Approach to Edge Detection** (1986)
   - Penulis: John Canny
   - DOI: 10.1109/TPAMI.1986.4767851
   - *Paper klasik Canny edge detector*

2. **Scale-Space Theory in Computer Vision** (1994)
   - Penulis: Tony Lindeberg
   - *Foundation untuk multi-scale analysis*

### Bilateral Filter
3. **Bilateral Filtering for Gray and Color Images** (1998)
   - Penulis: C. Tomasi, R. Manduchi
   - DOI: 10.1109/ICCV.1998.710815
   - *Original bilateral filter paper*

### Non-local Means
4. **A Non-Local Algorithm for Image Denoising** (2005)
   - Penulis: A. Buades, B. Coll, J.M. Morel
   - *State-of-the-art classical denoising*

### Morphological Operations
5. **Image Analysis and Mathematical Morphology** (1982)
   - Penulis: Jean Serra
   - *Foundational work on morphology*

---

## 🎥 Video Tutorial

### YouTube Channels
1. **First Principles of Computer Vision (Columbia)**
   - [Image Filtering](https://www.youtube.com/watch?v=1THuCOKNn6U)
   - [Edge Detection](https://www.youtube.com/watch?v=5_dBG2tJ2Os)
   - [Morphological Operations](https://www.youtube.com/watch?v=IcBzsP-fvPo)

2. **Computerphile**
   - [Canny Edge Detector](https://www.youtube.com/watch?v=sRFM5IEqR2w)
   - [Image Kernels](https://www.youtube.com/watch?v=C_zFhWdM4ic)

3. **3Blue1Brown**
   - [But what is the Fourier Transform?](https://www.youtube.com/watch?v=spUNpyF58BY)
   - *Visualisasi intuitif Fourier*

4. **The Coding Train**
   - [Image Processing with Pixels](https://www.youtube.com/watch?v=nMUMZ5YRxHI)
   - [Convolution](https://www.youtube.com/watch?v=8rrHTtUzyZA)

---

## 📖 Online Resources

### Tutorials & Documentation
1. **OpenCV Documentation**
   - [Image Filtering](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
   - [Morphological Operations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
   - [Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)

2. **scikit-image Documentation**
   - [Filtering Tutorial](https://scikit-image.org/docs/stable/auto_examples/filters/)
   - [Edge Detection](https://scikit-image.org/docs/stable/auto_examples/edges/)

3. **Image Processing Learning Resources**
   - [Image Processing in Python](https://datacarpentry.org/image-processing/)
   - Data Carpentry tutorial

### Interactive Demos
4. **Image Kernels Explained Visually**
   - [setosa.io - Image Kernels](https://setosa.io/ev/image-kernels/)
   - Interactive kernel visualization

5. **Fourier Transform Demo**
   - [Better Explained - Fourier](https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/)
   - Interactive Fourier guide

---

## 🛠️ Tools & Libraries

### Python Libraries
1. **OpenCV** - `pip install opencv-python`
   - De facto standard untuk CV
   - [Documentation](https://docs.opencv.org/)

2. **scikit-image** - `pip install scikit-image`
   - Scientific image processing
   - [Documentation](https://scikit-image.org/)

3. **Pillow (PIL)** - `pip install Pillow`
   - Basic image operations
   - [Documentation](https://pillow.readthedocs.io/)

4. **scipy.ndimage** - dalam scipy
   - N-dimensional image processing
   - [Documentation](https://docs.scipy.org/doc/scipy/reference/ndimage.html)

### Visualization
5. **Matplotlib** - `pip install matplotlib`
   - Plotting dan visualisasi
   - [Gallery](https://matplotlib.org/stable/gallery/)

6. **Plotly** - `pip install plotly`
   - Interactive plots
   - [Documentation](https://plotly.com/python/)

---

## 📋 Cheat Sheets

### Common Kernels
```
Mean 3x3:           Gaussian 3x3:        Sharpen:
| 1 1 1 |          | 1 2 1 |           | 0 -1  0 |
| 1 1 1 | /9       | 2 4 2 | /16      | -1  5 -1 |
| 1 1 1 |          | 1 2 1 |           | 0 -1  0 |

Laplacian:          Sobel X:             Sobel Y:
| 0  1  0 |        | -1 0 1 |          | -1 -2 -1 |
| 1 -4  1 |        | -2 0 2 |          |  0  0  0 |
| 0  1  0 |        | -1 0 1 |          |  1  2  1 |
```

### OpenCV Quick Reference
```python
# Blur
cv2.blur(img, (5,5))                    # Box filter
cv2.GaussianBlur(img, (5,5), sigma)     # Gaussian
cv2.medianBlur(img, 5)                  # Median
cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)

# Edge Detection
cv2.Sobel(img, cv2.CV_64F, 1, 0)       # Sobel X
cv2.Laplacian(img, cv2.CV_64F)         # Laplacian
cv2.Canny(img, low, high)               # Canny

# Morphology
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
cv2.erode(img, kernel)
cv2.dilate(img, kernel)
cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# Threshold
cv2.threshold(img, thresh, maxval, cv2.THRESH_BINARY)
cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                      cv2.THRESH_BINARY, blockSize, C)
```

---

## 🌐 Communities & Forums

### Stack Overflow Tags
- [image-processing](https://stackoverflow.com/questions/tagged/image-processing)
- [opencv](https://stackoverflow.com/questions/tagged/opencv)
- [python-imaging-library](https://stackoverflow.com/questions/tagged/python-imaging-library)

### Reddit Communities
- r/computervision
- r/imageprocessing
- r/learnpython

### Dedicated Forums
- [OpenCV Forum](https://forum.opencv.org/)
- [ImageMagick Forum](https://github.com/ImageMagick/ImageMagick/discussions)

---

## 💻 Code Examples

### GitHub Repositories
1. **OpenCV Examples**
   - [opencv/samples/python](https://github.com/opencv/opencv/tree/master/samples/python)

2. **scikit-image Examples**
   - [scikit-image/doc/examples](https://github.com/scikit-image/scikit-image/tree/main/doc/examples)

3. **Image Processing Course Materials**
   - [DIP Course](https://github.com/dipakkr/A-to-Z-Resources-for-Students)
   - Various university courses

### Jupyter Notebooks
4. **Kaggle Notebooks**
   - Search: "Image Processing Tutorial"
   - Banyak hands-on examples

5. **Google Colab Templates**
   - Search: "OpenCV tutorial"
   - Ready-to-run notebooks

---

## 📝 Exercise Resources

### Online Courses
1. **Coursera - Image Processing**
   - Duke University
   - [Link](https://www.coursera.org/specializations/image-and-video-processing)

2. **Udacity - Computer Vision**
   - Georgia Tech
   - [Link](https://www.udacity.com/course/introduction-to-computer-vision--ud810)

3. **MIT OpenCourseWare**
   - 6.869 Advances in Computer Vision
   - [Link](https://ocw.mit.edu/courses/6-869-advances-in-computer-vision-fall-2010/)

### Practice Problems
4. **HackerRank Image Processing**
   - [Challenges](https://www.hackerrank.com/domains/ai?filters%5Bsubdomains%5D%5B%5D=image-processing)

5. **LeetCode Related Problems**
   - Search: "image", "matrix convolution"

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| OpenCV Filtering | [Link](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) |
| scikit-image Filters | [Link](https://scikit-image.org/docs/stable/api/skimage.filters.html) |
| Canny Paper | [Link](https://ieeexplore.ieee.org/document/4767851) |
| Bilateral Filter Paper | [Link](https://ieeexplore.ieee.org/document/710815) |
| Image Kernels Demo | [Link](https://setosa.io/ev/image-kernels/) |

---

## 📌 Key Concepts Checklist

### Harus Dikuasai
- [ ] Point operators (brightness, contrast, gamma)
- [ ] Histogram equalization dan CLAHE
- [ ] Konvolusi dan berbagai kernel
- [ ] Gaussian blur dan separability
- [ ] Median dan bilateral filter
- [ ] Sobel, Laplacian edge detection
- [ ] Canny edge detection algorithm
- [ ] Morphological operations (erode, dilate, open, close)
- [ ] Fourier transform basics
- [ ] Image pyramids
- [ ] Thresholding (global, Otsu, adaptive)

### Formula Kunci
```python
# Point Operations
g = α*f + β          # Brightness/Contrast
g = c * f^γ          # Gamma correction

# Convolution
g[i,j] = Σ Σ f[i+m, j+n] * h[m,n]

# Gradient
Gx = ∂f/∂x, Gy = ∂f/∂y
Magnitude = √(Gx² + Gy²)
Direction = arctan(Gy/Gx)

# Gaussian
G(x,y) = (1/2πσ²) * exp(-(x²+y²)/2σ²)

# DFT
F(u,v) = Σ Σ f(x,y) * exp(-j2π(ux/M + vy/N))
```

---

**Selamat belajar!** 📖✨
