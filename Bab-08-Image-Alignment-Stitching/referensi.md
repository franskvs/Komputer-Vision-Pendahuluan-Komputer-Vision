# Referensi Bab 8: Image Alignment dan Stitching

## 📚 Buku Referensi Utama

1. **Computer Vision: Algorithms and Applications, 2nd Ed** - Richard Szeliski (2022)
   - https://szeliski.org/Book/
   - Chapter 8: Image Alignment and Stitching

2. **Multiple View Geometry in Computer Vision** - Hartley & Zisserman
   - Chapter 4: Estimation - 2D Projective Transformations
   - Chapter 13: Scene planes and homographies

3. **Computer Vision: A Modern Approach** - Forsyth & Ponce
   - Chapter on image mosaics

---

## 📄 Paper Klasik dan Penting

### Image Alignment

1. **Lucas-Kanade Optical Flow**
   - Lucas & Kanade (1981)
   - "An Iterative Image Registration Technique with an Application to Stereo Vision"
   - https://www.ri.cmu.edu/pub_files/pub3/lucas_bruce_d_1981_2/lucas_bruce_d_1981_2.pdf

2. **Lucas-Kanade 20 Years On: A Unifying Framework**
   - Baker & Matthews (2004)
   - https://www.ri.cmu.edu/pub_files/pub4/baker_simon_2004_1/baker_simon_2004_1.pdf
   - **Must-read** untuk memahami variants LK

3. **Enhanced Correlation Coefficient (ECC)**
   - Evangelidis & Psarakis (2008)
   - "Parametric Image Alignment Using Enhanced Correlation Coefficient Maximization"
   - https://ieeexplore.ieee.org/document/4515873

### Panorama Stitching

4. **Automatic Panoramic Image Stitching using Invariant Features**
   - Brown & Lowe (2007)
   - https://www.cs.ubc.ca/~lowe/papers/07brown.pdf
   - Seminal paper for automatic panorama

5. **Recognising Panoramas**
   - Brown & Lowe (2003)
   - https://www.cs.ubc.ca/~lowe/papers/03iccv.pdf

6. **As-Projective-As-Possible Image Stitching with Moving DLT**
   - Zaragoza et al. (2013)
   - https://cs.adelaide.edu.au/~tjchin/apap/

### Blending

7. **A Multiresolution Spline with Application to Image Mosaics**
   - Burt & Adelson (1983)
   - http://persci.mit.edu/pub_pdfs/spline83.pdf
   - **Classic paper** untuk multi-band blending

8. **Optimal Seam Selection for Multi-Viewpoint Panoramas**
   - Agarwala et al. (2006)
   - Graph cut based seam finding

### Advanced Topics

9. **Bundle Adjustment - A Modern Synthesis**
   - Triggs et al. (2000)
   - https://hal.inria.fr/inria-00548290/document

10. **Globally Optimal Stitching of Tiled 3D Microscopic Image Acquisitions**
    - Preibisch et al. (2009)
    - Advanced stitching dengan global optimization

---

## 🎓 Kursus Online

1. **CS231A: Computer Vision, From 3D Reconstruction to Recognition**
   - Stanford University
   - https://web.stanford.edu/class/cs231a/
   - Lecture on Image Stitching

2. **Introduction to Computer Vision** - Georgia Tech (Udacity)
   - https://www.udacity.com/course/introduction-to-computer-vision--ud810
   - Module on panoramas

3. **First Principles of Computer Vision**
   - YouTube Channel
   - https://www.youtube.com/channel/UCf0WB91t8Ber7WNqr7JWLaU
   - Videos on alignment dan stitching

4. **Computational Photography** - CMU
   - http://graphics.cs.cmu.edu/courses/15-463/
   - Assignments on HDR dan panorama

---

## 🔧 Library dan Tools

### OpenCV
1. **OpenCV Stitching Module**
   - https://docs.opencv.org/master/d1/d46/group__stitching.html
   - Official documentation

2. **OpenCV Feature2D**
   - https://docs.opencv.org/master/db/d27/tutorial_py_table_of_contents_feature2d.html

### Specialized Libraries
3. **OpenPano**
   - https://github.com/ppwwyyxx/OpenPano
   - Feature-based stitching implementation

4. **Hugin**
   - http://hugin.sourceforge.net/
   - Open source panorama stitcher
   - GUI-based dengan advanced features

5. **libvips**
   - https://libvips.github.io/libvips/
   - Efficient image processing untuk large images

6. **OpenSfM**
   - https://github.com/mapillary/OpenSfM
   - Structure from Motion dengan panorama support

### Deep Learning
7. **Deep Homography Estimation**
   - https://github.com/mez/deep_homography_estimation

8. **Unsupervised Deep Homography**
   - https://github.com/tynguyen/unsupervisedDeepHomographyRAL2018

---

## 📊 Dataset dan Benchmarks

### Panorama Datasets
1. **PASSTA (Panoramic Stereo)**
   - http://www.wisdom.weizmann.ac.il/~bagon/matlab.html

2. **Adobe Panoramas**
   - Various test sequences

3. **Flickr Panorama Collection**
   - User-contributed panoramas

### Homography Datasets
4. **HPatches**
   - https://hpatches.github.io/
   - Homography patches benchmark

5. **COCO-Homography**
   - Derived from COCO untuk homography estimation

### Video Stabilization
6. **NUS Video Stabilization Dataset**
   - https://www.comp.nus.edu.sg/~brown/vio/

7. **DeepStab Dataset**
   - Video stabilization benchmark

---

## 📝 Tutorial dan Blog

1. **Learn OpenCV - Image Alignment**
   - https://learnopencv.com/image-alignment-ecc-in-opencv-c-python/
   - ECC alignment tutorial

2. **Learn OpenCV - Homography**
   - https://learnopencv.com/homography-examples-using-opencv-python-c/

3. **OpenCV Panorama Stitching Tutorial**
   - https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/

4. **CMU Panorama Assignment**
   - http://graphics.cs.cmu.edu/courses/15-463/2011_fall/hw/proj5/

5. **Brown Panorama Tutorial**
   - https://www.cs.ubc.ca/~lowe/papers/brown07.html

---

## 🎥 Video Resources

1. **First Principles - Image Registration**
   - Detailed explanation of alignment

2. **Computerphile - Panoramas**
   - How panoramas work

3. **Two Minute Papers - Deep Image Stitching**
   - Recent advances

4. **Cyrill Stachniss - Photogrammetry Lectures**
   - Bundle adjustment dan registration

---

## 🔬 Implementasi Reference

### OpenCV Python - Stitching
```python
import cv2

# Simple stitching
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
status, panorama = stitcher.stitch(images)

# Custom pipeline
detector = cv2.SIFT_create()
matcher = cv2.BFMatcher(cv2.NORM_L2)

# Detect and match
kp1, desc1 = detector.detectAndCompute(img1, None)
kp2, desc2 = detector.detectAndCompute(img2, None)
matches = matcher.knnMatch(desc1, desc2, k=2)

# Ratio test
good = [m for m,n in matches if m.distance < 0.75*n.distance]

# Homography with RANSAC
src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
```

### ECC Alignment
```python
# Direct alignment with ECC
warp_mode = cv2.MOTION_EUCLIDEAN
warp_matrix = np.eye(2, 3, dtype=np.float32)

criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-6)
cc, warp_matrix = cv2.findTransformECC(template, image, warp_matrix, 
                                        warp_mode, criteria)

# Warp image
aligned = cv2.warpAffine(image, warp_matrix, (w, h),
                         flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
```

### Multi-Band Blending
```python
def multiband_blend(img1, img2, mask, levels=5):
    # Build Laplacian pyramids
    lap1 = build_laplacian_pyramid(img1, levels)
    lap2 = build_laplacian_pyramid(img2, levels)
    
    # Build Gaussian pyramid for mask
    mask_pyr = build_gaussian_pyramid(mask, levels)
    
    # Blend at each level
    blended_pyr = []
    for l1, l2, m in zip(lap1, lap2, mask_pyr):
        blended = m * l1 + (1 - m) * l2
        blended_pyr.append(blended)
    
    # Reconstruct
    return reconstruct_from_laplacian(blended_pyr)
```

---

## 📌 Formula Penting

### Homography DLT
Untuk setiap korespondensi $(x, y) \leftrightarrow (x', y')$:

$$\begin{bmatrix} -x & -y & -1 & 0 & 0 & 0 & x'x & x'y & x' \\ 0 & 0 & 0 & -x & -y & -1 & y'x & y'y & y' \end{bmatrix} \mathbf{h} = 0$$

### Lucas-Kanade Update
$$\Delta\mathbf{p} = H^{-1} \sum_{\mathbf{x}} \left[ \nabla I \frac{\partial \mathbf{W}}{\partial \mathbf{p}} \right]^T [T(\mathbf{x}) - I(\mathbf{W}(\mathbf{x}; \mathbf{p}))]$$

### ECC Objective
$$\text{ECC}(\mathbf{p}) = \frac{\mathbf{\hat{t}}^T \mathbf{\hat{i}}(\mathbf{p})}{\|\mathbf{\hat{t}}\| \|\mathbf{\hat{i}}(\mathbf{p})\|}$$

### Bundle Adjustment
$$\min_{\{R_i, t_i, f_i\}} \sum_{i,j} \sum_k \|x_{ij}^k - \pi(R_i, t_i, f_i, X^k)\|^2$$

### Exposure Compensation
$$\min_{\{g_n\}} \sum_{(i,j)} \sum_{\text{overlap}} (g_i I_i - g_j I_j)^2$$

---

## 🔗 Links Penting

- **OpenCV Stitching**: https://docs.opencv.org/master/d1/d46/group__stitching.html
- **Hugin**: http://hugin.sourceforge.net/
- **Papers with Code - Image Stitching**: https://paperswithcode.com/task/image-stitching
- **AutoStitch**: http://matthewalunbrown.com/autostitch/autostitch.html

---

## 🛠️ Software Tools

| Tool | Deskripsi | Link |
|------|-----------|------|
| **Hugin** | Open-source panorama creator | http://hugin.sourceforge.net/ |
| **Microsoft ICE** | Image Composite Editor | Microsoft Store |
| **PTGui** | Commercial stitcher | https://www.ptgui.com/ |
| **AutoStitch** | Auto panorama | http://matthewalunbrown.com/autostitch/ |
| **Photoshop** | Photomerge feature | Adobe |

---

*Terakhir diperbarui: 2024*
