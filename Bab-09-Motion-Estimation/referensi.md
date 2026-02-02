# Referensi Bab 9: Motion Estimation

## 📚 Buku Referensi Utama

1. **Computer Vision: Algorithms and Applications, 2nd Ed** - Richard Szeliski (2022)
   - https://szeliski.org/Book/
   - Chapter 9: Motion Estimation

2. **Computer Vision: A Modern Approach** - Forsyth & Ponce
   - Chapter on optical flow

3. **Video Processing and Communications** - Yao Wang et al.
   - Detailed coverage of motion estimation for video

---

## 📄 Paper Klasik dan Penting

### Foundational Papers

1. **Determining Optical Flow (Horn-Schunck)**
   - Horn & Schunck (1981)
   - https://dspace.mit.edu/handle/1721.1/6337
   - **Original** variational optical flow paper

2. **An Iterative Image Registration Technique with an Application to Stereo Vision (Lucas-Kanade)**
   - Lucas & Kanade (1981)
   - https://www.ri.cmu.edu/pub_files/pub3/lucas_bruce_d_1981_2/lucas_bruce_d_1981_2.pdf
   - **Classic** sparse optical flow

3. **Performance of Optical Flow Techniques**
   - Barron, Fleet, Beauchemin (1994)
   - https://www.cs.toronto.edu/~fleet/research/Papers/ijcv-94.pdf
   - Comprehensive comparison

### Robust Methods

4. **The Robust Estimation of Multiple Motions**
   - Black & Anandan (1996)
   - Robust optical flow dengan M-estimators

5. **High Accuracy Optical Flow Estimation Based on a Theory for Warping**
   - Brox et al. (2004)
   - https://lmb.informatik.uni-freiburg.de/Publications/2004/Bro04a/brox_eccv04_of.pdf
   - State-of-the-art variational method

6. **A Duality Based Approach for Realtime TV-L1 Optical Flow**
   - Zach, Pock, Bischof (2007)
   - Fast TV-L1 implementation

### Deep Learning Methods

7. **FlowNet: Learning Optical Flow with Convolutional Networks**
   - Dosovitskiy et al. (2015)
   - https://arxiv.org/abs/1504.06852
   - First end-to-end CNN for flow

8. **FlowNet 2.0: Evolution of Optical Flow Estimation with Deep Networks**
   - Ilg et al. (2017)
   - https://arxiv.org/abs/1612.01925
   - Improved FlowNet

9. **PWC-Net: CNNs for Optical Flow Using Pyramid, Warping, and Cost Volume**
   - Sun et al. (2018)
   - https://arxiv.org/abs/1709.02371
   - Efficient and accurate

10. **RAFT: Recurrent All-Pairs Field Transforms for Optical Flow**
    - Teed & Deng (2020)
    - https://arxiv.org/abs/2003.12039
    - **State-of-the-art** optical flow

11. **GMA: Learning to Estimate Hidden Motions with Global Motion Aggregation**
    - Jiang et al. (2021)
    - https://arxiv.org/abs/2104.02409
    - RAFT extension

### Frame Interpolation

12. **Video Frame Interpolation via Adaptive Convolution**
    - Niklaus et al. (2017)
    - https://arxiv.org/abs/1703.07514

13. **Super SloMo: High Quality Estimation of Multiple Intermediate Frames for Video Interpolation**
    - Jiang et al. (2018)
    - https://arxiv.org/abs/1712.00080
    - Flow-based interpolation

14. **FILM: Frame Interpolation for Large Motion**
    - Reda et al. (2022)
    - https://arxiv.org/abs/2202.04901

---

## 🎓 Kursus Online

1. **Introduction to Computer Vision** - Georgia Tech (Udacity)
   - https://www.udacity.com/course/introduction-to-computer-vision--ud810
   - Lectures on optical flow

2. **First Principles of Computer Vision**
   - https://www.youtube.com/channel/UCf0WB91t8Ber7WNqr7JWLaU
   - Optical flow series

3. **CS231n: Convolutional Neural Networks**
   - Stanford University
   - Video understanding lectures

---

## 🔧 Library dan Tools

### OpenCV
1. **OpenCV Optical Flow**
   - https://docs.opencv.org/master/d4/dee/tutorial_optical_flow.html
   - calcOpticalFlowPyrLK, calcOpticalFlowFarneback

2. **OpenCV contrib optflow**
   - DIS, TV-L1, DeepFlow
   - `pip install opencv-contrib-python`

### Deep Learning
3. **RAFT (Official)**
   - https://github.com/princeton-vl/RAFT
   - State-of-the-art deep flow

4. **PWC-Net**
   - https://github.com/NVlabs/PWC-Net
   - NVIDIA implementation

5. **FlowNet2**
   - https://github.com/NVIDIA/flownet2-pytorch
   - PyTorch implementation

6. **GMA**
   - https://github.com/zacjiang/GMA
   - RAFT with global motion

### Other Libraries
7. **kornia**
   - https://kornia.github.io/
   - Differentiable optical flow

8. **PyFlow**
   - https://github.com/pathak22/pyflow
   - Coarse-to-fine optical flow

9. **OpticalFlow (Matlab)**
   - http://cs.brown.edu/people/black/code.html
   - Classic implementations

---

## 📊 Dataset dan Benchmarks

### Optical Flow Benchmarks
1. **Middlebury Optical Flow**
   - http://vision.middlebury.edu/flow/
   - Classic benchmark with ground truth

2. **KITTI Flow**
   - http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php
   - Automotive benchmark

3. **MPI Sintel**
   - http://sintel.is.tue.mpg.de/
   - Synthetic with challenging effects

4. **Flying Chairs / Flying Things**
   - https://lmb.informatik.uni-freiburg.de/resources/datasets/
   - Training data for deep flow

### Video Datasets
5. **UCF101**
   - https://www.crcv.ucf.edu/data/UCF101.php
   - Action recognition

6. **DAVIS**
   - https://davischallenge.org/
   - Video object segmentation

7. **Vimeo-90K**
   - https://github.com/anchen1011/toflow
   - Frame interpolation

---

## 📝 Tutorial dan Blog

1. **OpenCV Optical Flow Tutorial**
   - https://docs.opencv.org/master/d4/dee/tutorial_optical_flow.html

2. **PyImageSearch - Optical Flow**
   - https://www.pyimagesearch.com/2019/09/30/opencv-optical-flow/

3. **Learn OpenCV - Optical Flow**
   - https://learnopencv.com/optical-flow-in-opencv/

4. **RAFT Explained**
   - Various blog posts explaining RAFT architecture

---

## 🎥 Video Resources

1. **First Principles of Computer Vision - Optical Flow**
   - https://www.youtube.com/playlist?list=PL2zRqk16wsdoYzrWStffqBAoUY8XdvatV

2. **Computerphile - Optical Flow**
   - Visual explanation

3. **Two Minute Papers - RAFT**
   - Quick overview of SOTA

---

## 🔬 Implementasi Reference

### Lucas-Kanade (OpenCV)
```python
import cv2
import numpy as np

# Sparse Lucas-Kanade
prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=100, 
                                   qualityLevel=0.3, minDistance=7)

lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, 
                                                  prev_pts, None, **lk_params)
```

### Dense Flow (Farneback)
```python
# Farneback dense flow
flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None,
                                     pyr_scale=0.5, levels=3, winsize=15,
                                     iterations=3, poly_n=5, poly_sigma=1.2,
                                     flags=0)

# DIS flow (faster)
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
flow = dis.calc(prev_gray, curr_gray, None)
```

### TV-L1 Flow
```python
# TV-L1 (robust)
tvl1 = cv2.optflow.DualTVL1OpticalFlow_create()
flow = tvl1.calc(prev_gray, curr_gray, None)
```

### RAFT (PyTorch)
```python
from raft import RAFT
import torch

model = RAFT(args)
model.load_state_dict(torch.load('raft-things.pth'))
model.eval()

with torch.no_grad():
    flow_low, flow_up = model(image1, image2, iters=20)
```

### Flow Visualization
```python
def flow_to_color(flow):
    """Convert flow to RGB image."""
    h, w = flow.shape[:2]
    hsv = np.zeros((h, w, 3), dtype=np.uint8)
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 1] = 255
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
```

---

## 📌 Formula Penting

### Optical Flow Constraint
$$I_x u + I_y v + I_t = 0$$

### Lucas-Kanade Solution
$$\begin{bmatrix} u \\ v \end{bmatrix} = (A^T A)^{-1} A^T b$$

Di mana:
$$A = \begin{bmatrix} I_x(p_1) & I_y(p_1) \\ \vdots & \vdots \\ I_x(p_n) & I_y(p_n) \end{bmatrix}, \quad b = -\begin{bmatrix} I_t(p_1) \\ \vdots \\ I_t(p_n) \end{bmatrix}$$

### Horn-Schunck Energy
$$E = \iint \left[ (I_x u + I_y v + I_t)^2 + \alpha^2 (|\nabla u|^2 + |\nabla v|^2) \right] dx dy$$

### Horn-Schunck Update (Gauss-Seidel)
$$u^{n+1} = \bar{u}^n - \frac{I_x(I_x \bar{u}^n + I_y \bar{v}^n + I_t)}{\alpha^2 + I_x^2 + I_y^2}$$

### Robust Penalty (Charbonnier)
$$\rho(x) = \sqrt{x^2 + \epsilon^2}$$

### End-Point Error
$$\text{EPE} = \sqrt{(u - u_{gt})^2 + (v - v_{gt})^2}$$

---

## 🔗 Links Penting

- **Middlebury Flow**: http://vision.middlebury.edu/flow/
- **KITTI Flow**: http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php
- **Sintel**: http://sintel.is.tue.mpg.de/
- **Papers with Code - Optical Flow**: https://paperswithcode.com/task/optical-flow-estimation

---

## 🏆 Leaderboards

### Sintel Benchmark (EPE)
| Method | Clean | Final |
|--------|-------|-------|
| RAFT | 1.43 | 2.71 |
| GMA | 1.30 | 2.74 |
| FlowFormer | 1.16 | 2.09 |

### KITTI 2015 (Fl-all)
| Method | All |
|--------|-----|
| RAFT | 5.10% |
| GMA | 5.15% |

---

*Terakhir diperbarui: 2024*
