# Referensi Bab 7: Feature Detection dan Matching

## 📚 Buku Referensi Utama

1. **Computer Vision: Algorithms and Applications, 2nd Ed** - Richard Szeliski (2022)
   - https://szeliski.org/Book/
   - Chapter 7: Feature Detection and Matching

2. **Multiple View Geometry in Computer Vision** - Hartley & Zisserman
   - Referensi standar untuk geometric vision
   - Essential/Fundamental matrix, homography

3. **Computer Vision: Models, Learning, and Inference** - Simon Prince
   - http://www.computervisionmodels.com/

---

## 📄 Paper Klasik dan Penting

### Corner Detection

1. **A Combined Corner and Edge Detector (Harris)**
   - Harris & Stephens (1988)
   - http://www.bmva.org/bmvc/1988/avc-88-023.pdf
   - Original Harris corner paper

2. **Good Features to Track (Shi-Tomasi)**
   - Shi & Tomasi (1994)
   - https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf

3. **FAST: Machine Learning for High-Speed Corner Detection**
   - Rosten & Drummond (2006)
   - https://www.edwardrosten.com/work/rosten_2006_machine.pdf

### Scale-Invariant Features

4. **Distinctive Image Features from Scale-Invariant Keypoints (SIFT)**
   - David Lowe (2004)
   - https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
   - **Must-read** paper untuk feature detection

5. **SURF: Speeded Up Robust Features**
   - Bay et al. (2008)
   - https://www.vision.ee.ethz.ch/~surf/eccv06.pdf
   - Faster alternative to SIFT

6. **ORB: An Efficient Alternative to SIFT or SURF**
   - Rublee et al. (2011)
   - http://www.willowgarage.com/sites/default/files/orb_final.pdf
   - Free alternative, real-time performance

7. **BRIEF: Binary Robust Independent Elementary Features**
   - Calonder et al. (2010)
   - https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf

8. **BRISK: Binary Robust Invariant Scalable Keypoints**
   - Leutenegger et al. (2011)
   - https://www.research-collection.ethz.ch/handle/20.500.11850/43288

### Model Fitting

9. **Random Sample Consensus (RANSAC)**
   - Fischler & Bolles (1981)
   - https://www.sri.com/wp-content/uploads/pdf/ransac-publication.pdf
   - Fundamental paper untuk outlier rejection

10. **Optimizing and Learning for MAGSAC++**
    - Barath et al. (2020)
    - Modern RANSAC variant

### Learned Features

11. **SuperPoint: Self-Supervised Interest Point Detection and Description**
    - DeTone et al. (2018)
    - https://arxiv.org/abs/1712.07629
    - Learned detector + descriptor

12. **SuperGlue: Learning Feature Matching with Graph Neural Networks**
    - Sarlin et al. (2019)
    - https://arxiv.org/abs/1911.11763
    - Learned matcher

13. **LoFTR: Detector-Free Local Feature Matching with Transformers**
    - Sun et al. (2021)
    - https://arxiv.org/abs/2104.00680
    - Transformer-based matching

14. **LightGlue: Local Feature Matching at Light Speed**
    - Lindenberger et al. (2023)
    - https://arxiv.org/abs/2306.13643
    - Efficient learned matching

---

## 🎓 Kursus Online

1. **CS231A: Computer Vision, From 3D Reconstruction to Recognition**
   - Stanford University
   - https://web.stanford.edu/class/cs231a/
   - Feature detection dan matching

2. **Introduction to Computer Vision** - Georgia Tech (Udacity)
   - https://www.udacity.com/course/introduction-to-computer-vision--ud810
   - Free course dengan hands-on assignments

3. **First Principles of Computer Vision** - YouTube
   - https://www.youtube.com/channel/UCf0WB91t8Ber7WNqr7JWLaU
   - Detailed explanations

---

## 🔧 Library dan Tools

### OpenCV
1. **OpenCV Feature Detection**
   - https://docs.opencv.org/master/db/d27/tutorial_py_table_of_contents_feature2d.html
   - Official tutorials

2. **opencv-contrib** untuk SIFT/SURF
   - `pip install opencv-contrib-python`

### Feature Detection Libraries
3. **kornia**
   - https://kornia.github.io/
   - Differentiable CV untuk PyTorch
   - SIFT, ORB, LoFTR implementations

4. **hloc (Hierarchical Localization)**
   - https://github.com/cvg/Hierarchical-Localization
   - SuperPoint + SuperGlue pipeline

5. **pydegensac**
   - https://github.com/ducha-aiki/pydegensac
   - Degeneracy-aware RANSAC

### Deep Learning Features
6. **SuperPoint/SuperGlue PyTorch**
   - https://github.com/magicleap/SuperPointPretrainedNetwork
   - https://github.com/magicleap/SuperGluePretrainedNetwork

7. **LoFTR**
   - https://github.com/zju3dv/LoFTR

8. **LightGlue**
   - https://github.com/cvg/LightGlue

---

## 📊 Dataset dan Benchmarks

### Feature Matching Benchmarks
1. **HPatches**
   - https://hpatches.github.io/
   - Homography patches for matching evaluation

2. **IMC (Image Matching Challenge)**
   - https://www.kaggle.com/c/image-matching-challenge-2022
   - Large-scale matching benchmark

3. **ScanNet**
   - https://www.scan-net.org/
   - Indoor scene matching

4. **MegaDepth**
   - https://www.cs.cornell.edu/projects/megadepth/
   - Internet photos with depth

### Visual Odometry
5. **KITTI Visual Odometry**
   - https://www.cvlibs.net/datasets/kitti/eval_odometry.php
   - Automotive benchmark

6. **TUM RGB-D**
   - https://vision.in.tum.de/data/datasets/rgbd-dataset
   - Indoor RGB-D benchmark

---

## 📝 Tutorial dan Blog

1. **AI Shack - SIFT Tutorial**
   - https://aishack.in/tutorials/sift-scale-invariant-feature-transform-introduction/
   - Step-by-step SIFT explanation

2. **Learn OpenCV**
   - https://learnopencv.com/
   - Feature detection tutorials

3. **Feature Matching + Homography to Find Objects**
   - OpenCV official tutorial
   - https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html

4. **Demystifying SIFT**
   - Multiple blog series

---

## 🎥 Video Resources

1. **First Principles of Computer Vision - Feature Detection**
   - https://www.youtube.com/playlist?list=PL2zRqk16wsdqXEMpHrc4Qnb5rA1Cylrhx

2. **Computerphile - SIFT Explained**
   - Clear visual explanations

3. **Cyrill Stachniss - Photogrammetry**
   - https://www.youtube.com/c/CyrillStachniss
   - Feature matching untuk mapping

---

## 🔬 Implementasi Reference

### OpenCV Python
```python
import cv2

# SIFT
sift = cv2.SIFT_create()
kps, desc = sift.detectAndCompute(gray, None)

# ORB
orb = cv2.ORB_create(nfeatures=1000)
kps, desc = orb.detectAndCompute(gray, None)

# Matching
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
matches = bf.knnMatch(desc1, desc2, k=2)

# Ratio test
good = [m for m,n in matches if m.distance < 0.75*n.distance]

# RANSAC homography
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
```

### SuperPoint + SuperGlue
```python
from hloc import extractors, matchers

# Extract features
extractor = extractors.SuperPoint({'nms_radius': 4, 'keypoint_threshold': 0.005})
features = extractor.extract(image)

# Match
matcher = matchers.SuperGlue({'weights': 'outdoor'})
matches = matcher.match(features0, features1)
```

---

## 📌 Formula Penting

### Harris Response
$$R = \det(M) - k \cdot \text{trace}(M)^2$$

$$M = \sum_{x,y} w(x,y) \begin{bmatrix} I_x^2 & I_xI_y \\ I_xI_y & I_y^2 \end{bmatrix}$$

### Scale-Normalized LoG
$$\nabla^2_{norm} L = \sigma^2 (L_{xx} + L_{yy})$$

### Homography Estimation (DLT)
Untuk setiap correspondence:
$$\begin{bmatrix} -u_1 & -v_1 & -1 & 0 & 0 & 0 & u_2 u_1 & u_2 v_1 & u_2 \\ 0 & 0 & 0 & -u_1 & -v_1 & -1 & v_2 u_1 & v_2 v_1 & v_2 \end{bmatrix} \mathbf{h} = 0$$

### RANSAC Iterations
$$N = \frac{\log(1-p)}{\log(1-(1-\epsilon)^s)}$$

Di mana:
- $p$: probability of success (e.g., 0.99)
- $\epsilon$: outlier ratio
- $s$: minimum sample size

---

## 🔗 Links Penting

- **OpenCV Feature2D**: https://docs.opencv.org/master/d5/d51/group__features2d__main.html
- **Papers with Code - Feature Matching**: https://paperswithcode.com/task/feature-matching
- **Visual Localization Benchmark**: https://www.visuallocalization.net/

---

*Terakhir diperbarui: 2024*
