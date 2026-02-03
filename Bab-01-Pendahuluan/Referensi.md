# Referensi dan Sumber Belajar Tambahan
# Praktikum Computer Vision - Bab 1: Pendahuluan

## 📚 Buku Utama

### Computer Vision: Algorithms and Applications, 2nd Edition
- **Penulis**: Richard Szeliski
- **Tahun**: 2022
- **Penerbit**: Springer
- **URL**: https://szeliski.org/Book/
- **Chapter yang relevan**: Chapter 1 - Introduction

---

## 📖 Buku Pendukung

### 1. Learning OpenCV 4 Computer Vision with Python 3
- **Penulis**: Joseph Howse, Joe Minichino
- **Tahun**: 2020
- **Penerbit**: Packt Publishing
- **Deskripsi**: Panduan praktis OpenCV dengan Python

### 2. Programming Computer Vision with Python
- **Penulis**: Jan Erik Solem
- **Tahun**: 2012
- **Penerbit**: O'Reilly Media
- **URL**: http://programmingcomputervision.com/
- **Deskripsi**: Implementasi algoritma CV dengan Python

### 3. Digital Image Processing
- **Penulis**: Rafael C. Gonzalez, Richard E. Woods
- **Edisi**: 4th Edition
- **Penerbit**: Pearson
- **Deskripsi**: Teori fundamental pemrosesan citra digital

---

## 🌐 Dokumentasi Resmi

### OpenCV
- **Dokumentasi**: https://docs.opencv.org/4.x/
- **Tutorial Python**: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- **GitHub**: https://github.com/opencv/opencv

### NumPy
- **Dokumentasi**: https://numpy.org/doc/
- **User Guide**: https://numpy.org/doc/stable/user/index.html

### Matplotlib
- **Dokumentasi**: https://matplotlib.org/stable/contents.html
- **Gallery**: https://matplotlib.org/stable/gallery/index.html

---

## 🎓 Kursus Online

### Coursera
1. **Computer Vision Basics** - University at Buffalo
   - URL: https://www.coursera.org/learn/computer-vision-basics
   
2. **Deep Learning Specialization** - Andrew Ng
   - URL: https://www.coursera.org/specializations/deep-learning
   - Course 4: Convolutional Neural Networks

### Udacity
1. **Introduction to Computer Vision** - Georgia Tech
   - URL: https://www.udacity.com/course/introduction-to-computer-vision--ud810

### YouTube
1. **OpenCV Course - Full Tutorial with Python** - freeCodeCamp
   - URL: https://www.youtube.com/watch?v=oXlwWbU8l2o
   
2. **Computer Vision with Python** - Sentdex
   - Playlist lengkap tentang OpenCV dan computer vision

---

## 📝 Tutorial dan Blog

### PyImageSearch
- **URL**: https://pyimagesearch.com/
- **Deskripsi**: Blog terlengkap tentang computer vision dengan Python
- **Artikel Relevan**:
  - OpenCV Tutorial: A Guide to Learn OpenCV
  - Getting Started with OpenCV
  - Basic Image Manipulations in Python

### LearnOpenCV
- **URL**: https://learnopencv.com/
- **Deskripsi**: Tutorial praktis OpenCV dengan contoh kode
- **Artikel Relevan**:
  - Read, Display and Write an Image using OpenCV
  - Color spaces in OpenCV (C++ / Python)

### Real Python
- **URL**: https://realpython.com/
- **Artikel**: Python Image Processing with OpenCV

### Towards Data Science
- **URL**: https://towardsdatascience.com/
- **Banyak artikel tentang computer vision dan deep learning**

---

## 🔬 Paper dan Jurnal

### Untuk referensi akademis:
1. **IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)**
2. **International Journal of Computer Vision (IJCV)**
3. **Computer Vision and Image Understanding (CVIU)**

### Paper Klasik:
1. Canny, J. (1986). "A Computational Approach to Edge Detection"
2. Lowe, D. G. (2004). "Distinctive Image Features from Scale-Invariant Keypoints"
3. Viola, P., & Jones, M. (2001). "Rapid Object Detection using a Boosted Cascade of Simple Features"

---

## 🛠️ Tools dan Software

### IDE dan Editor
- **VS Code**: https://code.visualstudio.com/
- **PyCharm**: https://www.jetbrains.com/pycharm/
- **Jupyter Notebook**: https://jupyter.org/

### Visualisasi
- **ImageJ/Fiji**: https://imagej.net/
- **GIMP**: https://www.gimp.org/

### Dataset
- **ImageNet**: https://www.image-net.org/
- **COCO Dataset**: https://cocodataset.org/
- **Pascal VOC**: http://host.robots.ox.ac.uk/pascal/VOC/

---

## 🔗 Resource Tambahan

### GitHub Repository
1. **Awesome Computer Vision**: https://github.com/jbhuang0604/awesome-computer-vision
2. **Awesome OpenCV**: https://github.com/gary-robotics/awesome-opencv

### Komunitas
- **Stack Overflow**: Tag [opencv], [computer-vision], [image-processing]
- **Reddit**: r/computervision, r/learnmachinelearning
- **OpenCV Forum**: https://forum.opencv.org/

### Cheat Sheets
- **OpenCV Cheat Sheet**: https://learnopencv.com/opencv-cheat-sheet/
- **NumPy Cheat Sheet**: https://www.dataquest.io/blog/numpy-cheat-sheet/

---

## 📋 Daftar Fungsi OpenCV yang Dipelajari

### Bab 1 - Pendahuluan

| Fungsi | Kegunaan |
|--------|----------|
| `cv2.imread()` | Membaca gambar dari file |
| `cv2.imshow()` | Menampilkan gambar di window |
| `cv2.imwrite()` | Menyimpan gambar ke file |
| `cv2.cvtColor()` | Konversi color space |
| `cv2.resize()` | Mengubah ukuran gambar |
| `cv2.line()` | Menggambar garis |
| `cv2.rectangle()` | Menggambar persegi |
| `cv2.circle()` | Menggambar lingkaran |
| `cv2.ellipse()` | Menggambar elips |
| `cv2.polylines()` | Menggambar polygon |
| `cv2.putText()` | Menulis teks |
| `cv2.add()` | Penambahan dengan saturasi |
| `cv2.subtract()` | Pengurangan dengan saturasi |
| `cv2.addWeighted()` | Blending dua gambar |
| `cv2.bitwise_not()` | Operasi NOT bitwise |
| `cv2.inRange()` | Thresholding berdasarkan range |
| `cv2.split()` | Memisahkan channel |
| `cv2.merge()` | Menggabungkan channel |

---

## 📅 Timeline Pembelajaran yang Disarankan

| Minggu | Topik | Fokus |
|--------|-------|-------|
| 1 | Instalasi & Setup | Environment, library |
| 1-2 | Loading & Menampilkan | cv2.imread, cv2.imshow, plt.imshow |
| 2 | Properti Gambar | Shape, dtype, channels |
| 2-3 | Color Space | BGR, RGB, HSV, Grayscale |
| 3 | Manipulasi Piksel | Akses, ROI, operasi aritmatika |
| 3-4 | Drawing | Shapes, text, anotasi |
| 4 | Saving Output | Format, kompresi, video |

---

*Terakhir diperbarui: 2024*
