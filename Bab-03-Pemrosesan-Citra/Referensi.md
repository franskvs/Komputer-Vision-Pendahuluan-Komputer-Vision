# Referensi - Bab 3: Pemrosesan Citra (Image Processing)

## Referensi Utama

### Buku Teks
1. **Szeliski, R. (2022). Computer Vision: Algorithms and Applications, 2nd Edition.**
   - Chapter 3: Image Processing
   - Website: https://szeliski.org/Book/
   - Materi: Point operations, histogram, filtering, edge detection

2. **Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing, 4th Edition.**
   - Chapter 3: Intensity Transformations and Spatial Filtering
   - Chapter 9: Morphological Image Processing
   - Chapter 10: Image Segmentation

3. **Burger, W., & Burge, M. J. (2016). Digital Image Processing: An Algorithmic Introduction Using Java, 2nd Edition.**
   - Part II: Filters
   - Springer

## Dokumentasi Resmi

### OpenCV Documentation
- **Image Processing Functions**
  - https://docs.opencv.org/4.x/d7/da8/tutorial_table_of_content_imgproc.html

- **Point Operations**
  - cv2.convertScaleAbs(): https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga3460e9c9f37b563ab9dd550c4d8c4e7d
  - cv2.LUT(): https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gab55b8d062b7f5587720ede032d34156f

- **Histogram Functions**
  - cv2.calcHist(): https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html#ga4b2b5fd75503ff9e6844cc4dcdaed35d
  - cv2.equalizeHist(): https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html#ga7e54091f0c937d49bf84152a16f76c6d
  - cv2.createCLAHE(): https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html#gad689d2607b7b3889c4a1ee3cd4f401e8

- **Filtering Functions**
  - cv2.GaussianBlur(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
  - cv2.medianBlur(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga564869aa33e58769b4469101aac458f9
  - cv2.bilateralFilter(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed
  - cv2.filter2D(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga27c049795ce870216ddfb366086b5a04

- **Edge Detection**
  - cv2.Sobel(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gacea54f142e81b6758cb6f375ce782c8d
  - cv2.Laplacian(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gad78703e4c8fe703d479c1860d76f7e48
  - cv2.Canny(): https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de

- **Morphological Operations**
  - cv2.erode(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaeb1e0c1033e3f6b891a25d0511362aeb
  - cv2.dilate(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga4ff0f3318642c4f469d0e11f242f3b6c
  - cv2.morphologyEx(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga67493776e3ad1a3df63883829375201f
  - cv2.getStructuringElement(): https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gac342a1bb6eabf6f55c803b09268e36dc

## Tutorial dan Artikel

### Point Operations
1. **Brightness and Contrast Control**
   - OpenCV Tutorial: https://docs.opencv.org/4.x/d3/dc1/tutorial_basic_linear_transform.html
   
2. **Gamma Correction**
   - PyImageSearch: https://pyimagesearch.com/2015/10/05/opencv-gamma-correction/
   - Adrian Rosebrock's detailed explanation

3. **Image Thresholding**
   - OpenCV Tutorial: https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
   - Adaptive thresholding explanation

### Histogram Operations
1. **Histogram Equalization**
   - OpenCV Tutorial: https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html
   
2. **CLAHE (Contrast Limited Adaptive Histogram Equalization)**
   - Detailed explanation: https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html
   - Medical imaging applications

### Spatial Filtering
1. **Smoothing Images**
   - OpenCV Tutorial: https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html
   - Comparison of different filters

2. **Bilateral Filter**
   - Tomasi, C., & Manduchi, R. (1998). "Bilateral Filtering for Gray and Color Images"
   - ICCV 1998 paper

3. **Unsharp Masking**
   - Understanding unsharp masking for image sharpening
   - https://homepages.inf.ed.ac.uk/rbf/HIPR2/unsharp.htm

### Edge Detection
1. **Canny Edge Detection**
   - Original paper: Canny, J. (1986). "A Computational Approach to Edge Detection"
   - OpenCV Tutorial: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html

2. **Sobel and Scharr Derivatives**
   - OpenCV Tutorial: https://docs.opencv.org/4.x/d2/d2c/tutorial_sobel_derivatives.html

### Morphological Operations
1. **Morphological Transformations**
   - OpenCV Tutorial: https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html

2. **Serra, J. (1982). Image Analysis and Mathematical Morphology**
   - Foundational text on mathematical morphology

## Video Tutorial

### YouTube Channels
1. **Computerphile**
   - "How Blurs & Filters Work"
   - "Edge Detection - Computerphile"

2. **First Principles of Computer Vision (Columbia University)**
   - Image Processing playlist
   - Edge Detection lectures
   - Channel: https://www.youtube.com/@firstprinciplesofcomputerv3258

3. **Sentdex - Python Programming tutorials**
   - OpenCV with Python series
   - https://www.youtube.com/user/sentdex

4. **PyImageSearch**
   - Practical OpenCV tutorials
   - https://www.youtube.com/c/PyImageSearch

## Papers Penting

### Foundational Papers
1. **Otsu, N. (1979). "A Threshold Selection Method from Gray-Level Histograms"**
   - IEEE Transactions on Systems, Man, and Cybernetics
   - Metode Otsu untuk automatic thresholding

2. **Canny, J. (1986). "A Computational Approach to Edge Detection"**
   - IEEE PAMI
   - Foundational edge detection algorithm

3. **Pizer, S. M., et al. (1987). "Adaptive Histogram Equalization and Its Variations"**
   - Computer Vision, Graphics, and Image Processing
   - CLAHE algorithm

4. **Marr, D., & Hildreth, E. (1980). "Theory of Edge Detection"**
   - Proceedings of the Royal Society of London
   - Laplacian of Gaussian (LoG)

### Modern Papers
1. **Perona, P., & Malik, J. (1990). "Scale-Space and Edge Detection Using Anisotropic Diffusion"**
   - IEEE PAMI
   - Anisotropic diffusion for edge-preserving smoothing

2. **Dabov, K., et al. (2007). "Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering"**
   - IEEE TIP
   - BM3D algorithm

## Tools dan Resources

### Online Tools
1. **Image Processing Online Demo**
   - https://eeweb.engineering.nyu.edu/~yao/EL5123/image_enhancement.html

2. **Setosa Visual Explanations**
   - Image Kernels: https://setosa.io/ev/image-kernels/

### Software
1. **GIMP** - Open source image editor
   - Filter menu demonstrates various image processing

2. **ImageJ/Fiji** - Scientific image analysis
   - https://imagej.net/software/fiji/

3. **scikit-image** - Python image processing
   - https://scikit-image.org/

## Aplikasi Industri

### Medical Imaging
- X-ray enhancement dengan CLAHE
- MRI/CT noise reduction
- Histopathology image processing

### Photography & Creative
- Instagram filters
- Adobe Lightroom algorithms
- Auto-enhance features

### Industrial Vision
- Automated Optical Inspection (AOI)
- Quality control dengan edge detection
- Surface defect detection

### Satellite/Remote Sensing
- Atmospheric correction
- Pan-sharpening
- Change detection

## Latihan dan Dataset

### Datasets untuk Praktik
1. **Standard Test Images**
   - Lena, Barbara, Cameraman, Peppers
   - USC-SIPI Image Database: http://sipi.usc.edu/database/

2. **BSD (Berkeley Segmentation Dataset)**
   - https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/

3. **Kodak Lossless True Color Image Suite**
   - http://r0k.us/graphics/kodak/

### Online Courses
1. **Coursera - Image and Video Processing**
   - Duke University
   - Covers fundamentals thoroughly

2. **edX - Introduction to Computer Vision**
   - Georgia Tech

3. **OpenCV Bootcamp**
   - https://opencv.org/courses/

## Glossary (Istilah Penting)

| Istilah | Definisi |
|---------|----------|
| **Point Operation** | Operasi yang memodifikasi piksel individual tanpa mempertimbangkan tetangga |
| **Neighborhood Operation** | Operasi yang mempertimbangkan piksel tetangga (spatial filtering) |
| **Convolution** | Operasi matematika sliding kernel over image |
| **Histogram** | Distribusi frekuensi nilai intensitas dalam gambar |
| **Equalization** | Redistribusi intensitas untuk meningkatkan kontras |
| **CLAHE** | Contrast Limited Adaptive Histogram Equalization |
| **Gradient** | Rate of change intensitas (first derivative) |
| **Laplacian** | Second derivative, deteksi zero crossing |
| **Structuring Element** | Kernel untuk operasi morfologi |
| **Erosion** | Mengecilkan objek foreground |
| **Dilation** | Memperbesar objek foreground |
| **Opening** | Erosi followed by dilation |
| **Closing** | Dilation followed by erosion |

---

*Referensi ini dikompilasi untuk mendukung pembelajaran Bab 3: Pemrosesan Citra*
*Terakhir diperbarui: 2024*
