# Referensi Bab 12: Depth Estimation

## Buku Referensi Utama

### Computer Vision: Algorithms and Applications (2nd Edition)
- **Penulis**: Richard Szeliski
- **Bab**: 11 - Stereo Correspondence, 12 - 3D Reconstruction
- **Link**: https://szeliski.org/Book/
- **Topik**: Stereo matching, multi-view stereo, depth estimation

### Multiple View Geometry in Computer Vision (2nd Edition)
- **Penulis**: Richard Hartley, Andrew Zisserman
- **Bab**: 11 - Stereo Systems, 12 - Structure Computation
- **Relevansi**: Teori geometri stereo, triangulasi, rekonstruksi

---

## Paper Fundamental

### Stereo Matching - Classical Methods

1. **A Taxonomy and Evaluation of Dense Two-Frame Stereo Correspondence Algorithms**
   - Penulis: D. Scharstein, R. Szeliski
   - Tahun: 2002 (IJCV)
   - Link: https://vision.middlebury.edu/stereo/taxonomy-IJCV.pdf
   - Signifikansi: Survey komprehensif stereo matching

2. **Accurate, Dense, and Robust Multi-View Stereopsis (PMVS)**
   - Penulis: Y. Furukawa, J. Ponce
   - Tahun: 2010 (TPAMI)
   - Link: https://www.di.ens.fr/pmvs/
   - Signifikansi: Dense MVS algorithm

3. **Stereo Matching by Training a Convolutional Neural Network to Compare Image Patches**
   - Penulis: J. Zbontar, Y. LeCun
   - Tahun: 2015 (CVPR)
   - Link: https://arxiv.org/abs/1510.05970
   - Signifikansi: Deep learning untuk stereo matching

### Semi-Global Matching

4. **Stereo Processing by Semi-Global Matching and Mutual Information**
   - Penulis: H. Hirschmuller
   - Tahun: 2008 (TPAMI)
   - Link: https://ieeexplore.ieee.org/document/4359315
   - Signifikansi: SGM algorithm, widely used

5. **SGM-Nets: Semi-Global Matching with Neural Networks**
   - Penulis: A. Seki, M. Pollefeys
   - Tahun: 2017 (CVPR)
   - Link: https://openaccess.thecvf.com/content_cvpr_2017/papers/Seki_SGM-Nets_Semi-Global_Matching_CVPR_2017_paper.pdf
   - Signifikansi: SGM dengan learned penalties

### Deep Stereo Matching

6. **End-to-End Learning of Geometry and Context for Deep Stereo Regression (GC-Net)**
   - Penulis: A. Kendall et al.
   - Tahun: 2017 (ICCV)
   - Link: https://arxiv.org/abs/1703.04309
   - Signifikansi: 3D cost volume dengan 3D convolutions

7. **Pyramid Stereo Matching Network (PSMNet)**
   - Penulis: J. Chang, Y. Chen
   - Tahun: 2018 (CVPR)
   - Link: https://arxiv.org/abs/1803.08669
   - Signifikansi: Spatial pyramid pooling untuk stereo

8. **AANet: Adaptive Aggregation Network for Efficient Stereo Matching**
   - Penulis: H. Xu, J. Zhang
   - Tahun: 2020 (CVPR)
   - Link: https://arxiv.org/abs/2004.09548
   - Signifikansi: Efficient adaptive cost aggregation

9. **RAFT-Stereo: Multilevel Recurrent Field Transforms for Stereo Matching**
   - Penulis: L. Lipson et al.
   - Tahun: 2021 (3DV)
   - Link: https://arxiv.org/abs/2109.07547
   - Signifikansi: Iterative refinement untuk stereo

10. **Practical Stereo Matching via Cascaded Recurrent Network (CREStereo)**
    - Penulis: J. Li et al.
    - Tahun: 2022 (CVPR)
    - Link: https://arxiv.org/abs/2203.11483
    - Signifikansi: State-of-the-art practical stereo

---

## Monocular Depth Estimation

### Supervised Methods

11. **Depth Map Prediction from a Single Image using a Multi-Scale Deep Network**
    - Penulis: D. Eigen et al.
    - Tahun: 2014 (NIPS)
    - Link: https://arxiv.org/abs/1406.2283
    - Signifikansi: Pioneering deep monocular depth

12. **Predicting Depth, Surface Normals and Semantic Labels with a Common Multi-Scale Convolutional Architecture**
    - Penulis: D. Eigen, R. Fergus
    - Tahun: 2015 (ICCV)
    - Link: https://arxiv.org/abs/1411.4734
    - Signifikansi: Multi-task depth prediction

13. **High Quality Monocular Depth Estimation via Transfer Learning (DenseDepth)**
    - Penulis: I. Alhashim, P. Wonka
    - Tahun: 2018
    - Link: https://arxiv.org/abs/1812.11941
    - Signifikansi: Transfer learning for depth

14. **Towards Robust Monocular Depth Estimation (MiDaS)**
    - Penulis: R. Ranftl et al.
    - Tahun: 2020 (TPAMI)
    - Link: https://arxiv.org/abs/1907.01341
    - Code: https://github.com/isl-org/MiDaS
    - Signifikansi: Robust cross-dataset depth

15. **Vision Transformers for Dense Prediction (DPT)**
    - Penulis: R. Ranftl et al.
    - Tahun: 2021 (ICCV)
    - Link: https://arxiv.org/abs/2103.13413
    - Signifikansi: ViT untuk depth estimation

### Self-Supervised Methods

16. **Unsupervised Monocular Depth Estimation with Left-Right Consistency**
    - Penulis: C. Godard et al.
    - Tahun: 2017 (CVPR)
    - Link: https://arxiv.org/abs/1609.03677
    - Signifikansi: Self-supervised dari stereo pairs

17. **Digging into Self-Supervised Monocular Depth Prediction (Monodepth2)**
    - Penulis: C. Godard et al.
    - Tahun: 2019 (ICCV)
    - Link: https://arxiv.org/abs/1806.01260
    - Code: https://github.com/nianticlabs/monodepth2
    - Signifikansi: Improved self-supervised depth

18. **Depth from Videos in the Wild: Unsupervised Monocular Depth Learning from Unknown Cameras**
    - Penulis: A. Gordon et al.
    - Tahun: 2019 (ICCV)
    - Link: https://arxiv.org/abs/1904.04998
    - Signifikansi: Learn dari video tanpa known intrinsics

19. **Feature-metric Loss for Self-supervised Learning of Depth and Egomotion**
    - Penulis: C. Shu et al.
    - Tahun: 2020 (ECCV)
    - Link: https://arxiv.org/abs/2007.10603
    - Signifikansi: Feature-based photometric loss

---

## Multi-View Stereo (MVS)

20. **Multi-View Stereo: A Tutorial**
    - Penulis: Y. Furukawa, C. Hernandez
    - Tahun: 2015 (FnTCG)
    - Link: http://www.nowpublishers.com/article/Details/CGV-052
    - Signifikansi: Comprehensive MVS tutorial

21. **MVSNet: Depth Inference for Unstructured Multi-view Stereo**
    - Penulis: Y. Yao et al.
    - Tahun: 2018 (ECCV)
    - Link: https://arxiv.org/abs/1804.02505
    - Signifikansi: Deep learning MVS

22. **Recurrent MVSNet for High-resolution Multi-view Stereo Depth Inference**
    - Penulis: Y. Yao et al.
    - Tahun: 2019 (CVPR)
    - Link: https://arxiv.org/abs/1902.10556
    - Signifikansi: Memory-efficient MVS

23. **Cascade Cost Volume for High-Resolution Multi-View Stereo**
    - Penulis: X. Gu et al.
    - Tahun: 2020 (CVPR)
    - Link: https://arxiv.org/abs/1912.06378
    - Signifikansi: Coarse-to-fine MVS

---

## Dataset dan Benchmark

### Stereo Datasets

24. **Middlebury Stereo Evaluation**
    - Link: https://vision.middlebury.edu/stereo/
    - Konten: Indoor stereo pairs dengan ground truth
    - Paper: Scharstein et al. (2014)

25. **KITTI Stereo Benchmark**
    - Link: https://www.cvlibs.net/datasets/kitti/eval_stereo.php
    - Konten: Outdoor driving scenes
    - Paper: Geiger et al. (2012)

26. **ETH3D Benchmark**
    - Link: https://www.eth3d.net/
    - Konten: High-quality indoor/outdoor
    - Paper: Schops et al. (2017)

27. **Scene Flow Dataset**
    - Link: https://lmb.informatik.uni-freiburg.de/resources/datasets/SceneFlowDatasets.en.html
    - Konten: Synthetic stereo dengan ground truth
    - Paper: Mayer et al. (2016)

### Monocular Depth Datasets

28. **NYU Depth V2**
    - Link: https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html
    - Konten: Indoor scenes dengan Kinect depth
    - Paper: Silberman et al. (2012)

29. **KITTI Depth**
    - Link: https://www.cvlibs.net/datasets/kitti/eval_depth.php
    - Konten: Outdoor depth dari LiDAR
    - Paper: Uhrig et al. (2017)

30. **Diode Dataset**
    - Link: https://diode-dataset.org/
    - Konten: Indoor/outdoor dengan high-quality depth
    - Paper: Vasiljevic et al. (2019)

---

## Depth Sensors

### Sensor Technologies

31. **A Survey on 3D Cameras: Metrological Comparison of Time-of-Flight, Structured-Light and Active Stereoscopy Technologies**
    - Penulis: B. Giancola et al.
    - Tahun: 2018
    - Link: https://www.mdpi.com/1424-8220/18/11/3962
    - Signifikansi: Comparison of depth sensors

32. **KinectFusion: Real-time Dense Surface Mapping and Tracking**
    - Penulis: R. Newcombe et al.
    - Tahun: 2011 (ISMAR)
    - Link: https://www.microsoft.com/en-us/research/publication/kinectfusion-real-time-dense-surface-mapping-and-tracking/
    - Signifikansi: Real-time depth fusion

---

## Tools dan Library

### OpenCV Stereo
```python
# StereoBM dan StereoSGBM
import cv2
stereo_bm = cv2.StereoBM_create()
stereo_sgbm = cv2.StereoSGBM_create()
```
- Dokumentasi: https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html

### Open3D
- Link: http://www.open3d.org/
- Fitur: Point cloud processing, RGBD integration, TSDF fusion
```python
import open3d as o3d
# RGBD image dan point cloud
```

### PyTorch3D
- Link: https://pytorch3d.org/
- Fitur: Differentiable rendering, 3D data structures

### MiDaS / DPT
- Link: https://github.com/isl-org/MiDaS
- Fitur: State-of-the-art monocular depth
```python
import torch
model = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
```

### Monodepth2
- Link: https://github.com/nianticlabs/monodepth2
- Fitur: Self-supervised monocular depth

### COLMAP
- Link: https://colmap.github.io/
- Fitur: SfM + MVS pipeline

---

## Tutorial dan Course

### Video Lectures

1. **First Principles of Computer Vision - Stereo**
   - Instructor: Shree Nayar (Columbia)
   - Link: https://fpcv.cs.columbia.edu/
   - Topik: Stereo geometry, matching, depth

2. **CS231A: Computer Vision - Stereo and 3D**
   - Stanford University
   - Link: https://web.stanford.edu/class/cs231a/

3. **Multiple View Geometry - Stereo**
   - TU Munich
   - Link: https://vision.in.tum.de/teaching/online/mvg

### Online Resources

4. **LearnOpenCV Tutorials**
   - Stereo matching: https://learnopencv.com/depth-estimation-using-stereo-matching-in-opencv/
   - Depth prediction: https://learnopencv.com/depth-prediction-with-midas/

5. **PyImageSearch**
   - Depth estimation tutorials
   - Link: https://www.pyimagesearch.com/

---

## Code Repositories

| Repository | Deskripsi | Link |
|-----------|-----------|------|
| MiDaS | Monocular depth | https://github.com/isl-org/MiDaS |
| Monodepth2 | Self-supervised depth | https://github.com/nianticlabs/monodepth2 |
| PSMNet | Deep stereo matching | https://github.com/JiaRenChang/PSMNet |
| AANet | Efficient stereo | https://github.com/haofeixu/aanet |
| RAFT-Stereo | Iterative stereo | https://github.com/princeton-vl/RAFT-Stereo |
| MVSNet | Multi-view stereo | https://github.com/YoYo000/MVSNet |
| CasMVSNet | Cascade MVS | https://github.com/alibaba/cascade-stereo |

---

## Metrics dan Evaluation

### Stereo Metrics
- **Bad pixel rate**: % pixels dengan error > threshold
- **End-point error (EPE)**: Average disparity error
- **D1-all**: % pixels dengan error > 3px dan > 5%

### Monocular Depth Metrics
- **AbsRel**: $\frac{1}{N}\sum|d - d^*|/d^*$
- **SqRel**: $\frac{1}{N}\sum||d - d^*||^2/d^*$
- **RMSE**: $\sqrt{\frac{1}{N}\sum||d - d^*||^2}$
- **δ < 1.25**: % pixels dengan $max(\frac{d}{d^*}, \frac{d^*}{d}) < 1.25$

---

## Konferensi dan Journal

### Top Venues
- **CVPR** - IEEE Conference on Computer Vision and Pattern Recognition
- **ICCV** - International Conference on Computer Vision
- **ECCV** - European Conference on Computer Vision
- **TPAMI** - IEEE Transactions on Pattern Analysis and Machine Intelligence
- **IJCV** - International Journal of Computer Vision
- **3DV** - International Conference on 3D Vision

### Workshops
- Stereo Vision Workshop (CVPR)
- 3D Reconstruction Workshop (ICCV)
- Autonomous Driving Workshop
