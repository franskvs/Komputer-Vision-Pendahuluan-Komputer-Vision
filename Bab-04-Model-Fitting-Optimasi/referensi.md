# Referensi Bab 4: Model Fitting dan Optimisasi

## 📚 Buku Utama

### Wajib
1. **Computer Vision: Algorithms and Applications, 2nd Edition**
   - Penulis: Richard Szeliski
   - Bab 4: Model Fitting and Optimization
   - Link: [szeliski.org/Book](https://szeliski.org/Book/)

2. **Multiple View Geometry in Computer Vision, 2nd Edition**
   - Penulis: Richard Hartley, Andrew Zisserman
   - Bab 4: Estimation – 2D Projective Transformations
   - *Gold standard untuk estimasi geometri*

### Pendukung
3. **Numerical Optimization, 2nd Edition**
   - Penulis: Jorge Nocedal, Stephen J. Wright
   - *Comprehensive optimization textbook*

4. **Pattern Recognition and Machine Learning**
   - Penulis: Christopher Bishop
   - Bab 3-4: Linear Models and Optimization

---

## 📄 Paper Klasik

### RANSAC
1. **Random Sample Consensus: A Paradigm for Model Fitting** (1981)
   - Penulis: Martin A. Fischler, Robert C. Bolles
   - DOI: 10.1145/358669.358692
   - *Original RANSAC paper - must read*

2. **MLESAC: A New Robust Estimator** (2000)
   - Penulis: Philip H.S. Torr, Andrew Zisserman
   - *Maximum Likelihood RANSAC variant*

3. **LO-RANSAC: Local Optimization** (2003)
   - Penulis: Ondřej Chum, Jiří Matas, Josef Kittler
   - *Local optimization setelah RANSAC*

4. **PROSAC: Progressive Sampling** (2005)
   - Penulis: Ondřej Chum, Jiří Matas
   - *Sampling berdasarkan quality score*

### Hough Transform
5. **Use of the Hough Transformation to Detect Lines and Curves** (1972)
   - Penulis: Richard O. Duda, Peter E. Hart
   - *Generalized Hough Transform*

6. **Generalizing the Hough Transform** (1981)
   - Penulis: Dana H. Ballard
   - *Generalized Hough untuk arbitrary shapes*

### Robust Estimation
7. **M-Estimators for Robust Estimation** (1964)
   - Penulis: Peter J. Huber
   - *Foundation of robust statistics*

---

## 🎥 Video Tutorial

### YouTube
1. **First Principles of Computer Vision (Columbia)**
   - [RANSAC](https://www.youtube.com/watch?v=1YNjMxxXO-E)
   - [Hough Transform](https://www.youtube.com/watch?v=ebfi7qOFLuo)

2. **Computerphile**
   - [RANSAC Explained](https://www.youtube.com/watch?v=9D5rrtCC_E0)
   - [Hough Lines](https://www.youtube.com/watch?v=4zHbI-fFIlI)

3. **Gradient Descent Visualization**
   - [3Blue1Brown - Gradient Descent](https://www.youtube.com/watch?v=IHZwWFHWa-w)
   - *Visual intuition for optimization*

4. **Stanford CS231n**
   - [Optimization Algorithms](https://www.youtube.com/watch?v=_JB0AO7QxSA)
   - Gradient descent variants

---

## 📖 Online Resources

### Tutorials
1. **OpenCV Documentation**
   - [Feature Matching + Homography](https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html)
   - [Hough Lines](https://docs.opencv.org/4.x/d6/d10/tutorial_py_houghlines.html)
   - [Hough Circles](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html)

2. **scikit-learn**
   - [RANSAC Regression](https://scikit-learn.org/stable/modules/linear_model.html#ransac-regression)
   - Documentation & examples

3. **SciPy Optimization**
   - [scipy.optimize Tutorial](https://docs.scipy.org/doc/scipy/tutorial/optimize.html)
   - Various optimization methods

### Interactive Demos
4. **RANSAC Visualization**
   - [Interactive RANSAC Demo](https://www.cse.usf.edu/~r1k/MachineVisionBook/MachineVision.files/MachineVision_Chapter5.pdf)
   
5. **Gradient Descent Visualization**
   - [Distill.pub - Momentum](https://distill.pub/2017/momentum/)
   - Interactive optimization visualization

---

## 🛠️ Tools & Libraries

### Python Libraries
1. **scikit-learn** - `pip install scikit-learn`
   - RANSACRegressor, other regressors
   - [Documentation](https://scikit-learn.org/)

2. **OpenCV** - `pip install opencv-python`
   - cv2.findHomography (RANSAC built-in)
   - cv2.HoughLines, cv2.HoughCircles
   - [Documentation](https://docs.opencv.org/)

3. **SciPy** - `pip install scipy`
   - scipy.optimize (gradient methods, L-BFGS, etc.)
   - [Documentation](https://docs.scipy.org/)

4. **skimage** - `pip install scikit-image`
   - skimage.transform.ransac
   - skimage.transform.hough_line
   - [Documentation](https://scikit-image.org/)

### Specialized Libraries
5. **pyransac3d** - `pip install pyransac3d`
   - RANSAC untuk primitive 3D
   - [GitHub](https://github.com/leomariga/pyRANSAC-3D)

6. **opencv-contrib-python** - `pip install opencv-contrib-python`
   - Additional features like SIFT
   - RANSAC-based estimators

---

## 📋 Cheat Sheets

### RANSAC Formula
```
Required Iterations:
N = log(1 - p) / log(1 - w^n)

where:
  p = desired success probability (e.g., 0.99)
  w = inlier ratio
  n = minimum samples needed

Examples:
  Line (n=2), w=0.5: N ≈ 17
  Homography (n=4), w=0.5: N ≈ 72
  Fundamental (n=8), w=0.5: N ≈ 1177
```

### Least Squares
```python
# Normal Equation
x = (A.T @ A)^(-1) @ A.T @ b
x = np.linalg.lstsq(A, b)[0]

# Weighted Least Squares
x = (A.T @ W @ A)^(-1) @ A.T @ W @ b

# Total Least Squares (SVD)
U, S, Vt = np.linalg.svd(augmented_A)
x = Vt[-1]  # last row
```

### Robust Loss Functions
```
Squared (L2):  ρ(e) = e²
Absolute (L1): ρ(e) = |e|
Huber:         ρ(e) = e²/2 if |e| ≤ δ, else δ(|e| - δ/2)
Tukey:         ρ(e) = (c²/6)(1 - (1 - (e/c)²)³) if |e| ≤ c, else c²/6
```

### Gradient Descent Variants
```python
# Vanilla GD
θ = θ - α * ∇L

# Momentum
v = γ*v + α*∇L
θ = θ - v

# Adam
m = β1*m + (1-β1)*∇L
v = β2*v + (1-β2)*(∇L)²
θ = θ - α * m / (√v + ε)
```

---

## 🌐 Communities & Forums

### Stack Overflow
- Tag: [ransac](https://stackoverflow.com/questions/tagged/ransac)
- Tag: [hough-transform](https://stackoverflow.com/questions/tagged/hough-transform)
- Tag: [least-squares](https://stackoverflow.com/questions/tagged/least-squares)

### Research Communities
- CVPR, ICCV, ECCV conferences
- [Papers With Code - RANSAC](https://paperswithcode.com/method/ransac)

### Discussion Forums
- [OpenCV Forum](https://forum.opencv.org/)
- r/computervision
- r/MachineLearning

---

## 💻 Code References

### GitHub Repositories
1. **OpenCV Samples**
   - [samples/python](https://github.com/opencv/opencv/tree/master/samples/python)
   - find_obj.py (homography estimation)

2. **scikit-image Examples**
   - [transform module](https://github.com/scikit-image/scikit-image/tree/main/skimage/transform)
   - RANSAC implementation

3. **RANSAC Implementations**
   - [pyransac3d](https://github.com/leomariga/pyRANSAC-3D)
   - Various primitive fitting

---

## 📝 Additional Reading

### Survey Papers
1. **A Survey of Model Fitting Methods** (2018)
   - Overview of fitting techniques

2. **Robust Estimation in Computer Vision** (2020)
   - Modern robust methods

### Optimization in Deep Learning
3. **An Overview of Gradient Descent Optimization Algorithms** (2016)
   - Penulis: Sebastian Ruder
   - [arXiv:1609.04747](https://arxiv.org/abs/1609.04747)
   - *Excellent overview of optimizers*

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| OpenCV RANSAC | [Link](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) |
| scikit-learn RANSAC | [Link](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html) |
| Hough Transform | [Link](https://docs.opencv.org/4.x/d6/d10/tutorial_py_houghlines.html) |
| SciPy Optimize | [Link](https://docs.scipy.org/doc/scipy/reference/optimize.html) |
| RANSAC Paper | [Link](https://dl.acm.org/doi/10.1145/358669.358692) |

---

## 📌 Key Concepts Checklist

### Yang Harus Dikuasai
- [ ] Least Squares (ordinary, weighted, total)
- [ ] RANSAC algorithm dan variasi
- [ ] Perhitungan jumlah iterasi RANSAC
- [ ] Hough Transform (garis dan lingkaran)
- [ ] Homography estimation dengan DLT
- [ ] Gradient descent dan variasinya
- [ ] M-estimators (Huber, Tukey)
- [ ] Regularization (L1, L2)

### Formula Kunci
```python
# RANSAC iterations
N = log(1-p) / log(1-w^n)

# Linear least squares
x = (A.T @ A)^(-1) @ A.T @ b

# Hough line transform
ρ = x*cos(θ) + y*sin(θ)

# Gradient descent
θ_new = θ - α * ∇L(θ)
```

---

**Selamat belajar!** 📖✨
