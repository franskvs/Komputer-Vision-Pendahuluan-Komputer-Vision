# Referensi Bab 11: Structure from Motion dan SLAM

## 1. Paper Fundamental

### Epipolar Geometry & Fundamental Matrix

1. **A Computer Algorithm for Reconstructing a Scene from Two Projections**
   - Longuet-Higgins, H. C. (1981)
   - Nature
   - Foundational paper untuk essential matrix

2. **In Defense of the Eight-Point Algorithm**
   - Hartley, R. I. (1997)
   - IEEE TPAMI
   - Normalized 8-point algorithm
   - Link: https://ieeexplore.ieee.org/document/601246

3. **Determining the Epipolar Geometry and its Uncertainty: A Review**
   - Zhang, Z. (1998)
   - IJCV
   - Comprehensive review

### Structure from Motion

4. **Building Rome in a Day**
   - Agarwal, S., Snavely, N., Simon, I., Seitz, S. M., & Szeliski, R. (2009)
   - ICCV 2009
   - Large-scale SfM
   - Link: https://grail.cs.washington.edu/projects/rome/

5. **Photo Tourism: Exploring Photo Collections in 3D**
   - Snavely, N., Seitz, S. M., & Szeliski, R. (2006)
   - SIGGRAPH 2006
   - Foundational SfM paper
   - Link: http://phototour.cs.washington.edu/

6. **Bundler: Structure from Motion (SfM) for Unordered Image Collections**
   - Snavely, N. (2006)
   - Link: https://www.cs.cornell.edu/~snavely/bundler/

### Bundle Adjustment

7. **Bundle Adjustment — A Modern Synthesis**
   - Triggs, B., McLauchlan, P. F., Hartley, R. I., & Fitzgibbon, A. W. (2000)
   - ICCV Vision Algorithms Workshop
   - Definitive BA reference
   - Link: https://link.springer.com/chapter/10.1007/3-540-44480-7_21

8. **SBA: A Software Package for Generic Sparse Bundle Adjustment**
   - Lourakis, M. I., & Argyros, A. A. (2009)
   - ACM TOMS
   - Link: http://users.ics.forth.gr/~lourakis/sba/

### Visual Odometry

9. **Visual Odometry Part I: The First 30 Years and Fundamentals**
   - Scaramuzza, D., & Fraundorfer, F. (2011)
   - IEEE Robotics & Automation Magazine
   - Excellent tutorial
   - Link: https://ieeexplore.ieee.org/document/6096039

10. **Visual Odometry Part II: Matching, Robustness, Optimization, and Applications**
    - Fraundorfer, F., & Scaramuzza, D. (2012)
    - IEEE Robotics & Automation Magazine

### SLAM - Classic

11. **MonoSLAM: Real-Time Single Camera SLAM**
    - Davison, A. J., Reid, I. D., Molton, N. D., & Stasse, O. (2007)
    - IEEE TPAMI
    - First real-time monocular SLAM
    - Link: https://www.doc.ic.ac.uk/~ajd/Publications/davison_etal_pami2007.pdf

12. **Parallel Tracking and Mapping for Small AR Workspaces (PTAM)**
    - Klein, G., & Murray, D. (2007)
    - ISMAR 2007
    - Influential parallel architecture
    - Link: https://www.robots.ox.ac.uk/~gk/PTAM/

13. **A Tutorial on Graph-Based SLAM**
    - Grisetti, G., Kümmerle, R., Stachniss, C., & Burgard, W. (2010)
    - IEEE Intelligent Transportation Systems Magazine
    - Excellent tutorial
    - Link: http://www2.informatik.uni-freiburg.de/~stachnis/pdf/grisetti10titsmag.pdf

### SLAM - Modern Feature-based

14. **ORB-SLAM: A Versatile and Accurate Monocular SLAM System**
    - Mur-Artal, R., Montiel, J. M. M., & Tardós, J. D. (2015)
    - IEEE Transactions on Robotics
    - Highly influential open-source SLAM
    - Link: https://arxiv.org/abs/1502.00956

15. **ORB-SLAM2: An Open-Source SLAM System for Monocular, Stereo, and RGB-D Cameras**
    - Mur-Artal, R., & Tardós, J. D. (2017)
    - IEEE Transactions on Robotics
    - Link: https://github.com/raulmur/ORB_SLAM2

16. **ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM**
    - Campos, C., et al. (2021)
    - IEEE Transactions on Robotics
    - Latest ORB-SLAM with IMU
    - Link: https://github.com/UZ-SLAMLab/ORB_SLAM3

### SLAM - Direct Methods

17. **LSD-SLAM: Large-Scale Direct Monocular SLAM**
    - Engel, J., Schöps, T., & Cremers, D. (2014)
    - ECCV 2014
    - Semi-dense direct SLAM
    - Link: https://vision.in.tum.de/research/vslam/lsdslam

18. **Direct Sparse Odometry**
    - Engel, J., Koltun, V., & Cremers, D. (2017)
    - IEEE TPAMI
    - Sparse direct method
    - Link: https://github.com/JakobEngel/dso

19. **SVO: Semi-Direct Visual Odometry for Monocular and Multicamera Systems**
    - Forster, C., Pizzoli, M., & Scaramuzza, D. (2014)
    - IEEE TRO
    - Link: https://github.com/uzh-rpg/rpg_svo

### Visual-Inertial SLAM

20. **VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator**
    - Qin, T., Li, P., & Shen, S. (2018)
    - IEEE Transactions on Robotics
    - State-of-the-art VIO
    - Link: https://github.com/HKUST-Aerial-Robotics/VINS-Mono

21. **OKVIS: Open Keyframe-based Visual-Inertial SLAM**
    - Leutenegger, S., Lynen, S., Bosse, M., Siegwart, R., & Furgale, P. (2015)
    - IJRR
    - Link: https://github.com/ethz-asl/okvis

22. **MSCKF: Multi-State Constraint Kalman Filter**
    - Mourikis, A. I., & Roumeliotis, S. I. (2007)
    - ICRA 2007
    - Efficient filter-based VIO

### Deep Learning for SLAM

23. **CNN-SLAM: Real-time dense monocular SLAM with learned depth prediction**
    - Tateno, K., Tombari, F., Laina, I., & Navab, N. (2017)
    - CVPR 2017

24. **DeepVO: Towards End-to-End Visual Odometry with Deep Recurrent Convolutional Neural Networks**
    - Wang, S., Clark, R., Wen, H., & Trigoni, N. (2017)
    - ICRA 2017

25. **DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D Cameras**
    - Teed, Z., & Deng, J. (2021)
    - NeurIPS 2021
    - State-of-the-art deep SLAM
    - Link: https://github.com/princeton-vl/DROID-SLAM

---

## 2. Buku Teks

1. **Multiple View Geometry in Computer Vision, 2nd Edition**
   - Hartley, R., & Zisserman, A. (2004)
   - Cambridge University Press
   - The definitive reference
   - Link: https://www.robots.ox.ac.uk/~vgg/hzbook/

2. **An Invitation to 3-D Vision**
   - Ma, Y., Soatto, S., Kosecka, J., & Sastry, S. S. (2003)
   - Springer
   - Mathematical foundations

3. **Computer Vision: Algorithms and Applications, 2nd Edition**
   - Szeliski, R. (2022)
   - Chapters 11-12
   - Free online: https://szeliski.org/Book/

4. **State Estimation for Robotics**
   - Barfoot, T. D. (2017)
   - Cambridge University Press
   - Excellent for SLAM math
   - Link: http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf

5. **Probabilistic Robotics**
   - Thrun, S., Burgard, W., & Fox, D. (2005)
   - MIT Press
   - SLAM fundamentals

---

## 3. Libraries dan Software

### SfM Systems

```bash
# COLMAP - State-of-the-art SfM
# https://colmap.github.io/
sudo apt install colmap

# OpenMVG - Open Multiple View Geometry
# https://github.com/openMVG/openMVG

# OpenMVS - Open Multi-View Stereo
# https://github.com/cdcseacave/openMVS

# Meshroom (GUI for photogrammetry)
# https://alicevision.org/
```

### SLAM Systems

```bash
# ORB-SLAM3
git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git

# OpenVSLAM (discontinued but useful)
git clone https://github.com/xdspacelab/openvslam.git

# RTAB-Map (RGB-D SLAM)
sudo apt install ros-noetic-rtabmap-ros

# Kimera (VIO + semantic)
git clone https://github.com/MIT-SPARK/Kimera-VIO.git
```

### Optimization Libraries

```bash
# g2o - General Graph Optimization
git clone https://github.com/RainerKuemmerle/g2o.git

# GTSAM - Georgia Tech Smoothing and Mapping
pip install gtsam
# atau dari source: https://github.com/borglab/gtsam

# Ceres Solver
# https://github.com/ceres-solver/ceres-solver

# scipy (untuk simple optimization)
pip install scipy
```

### Python Libraries

```python
# Core
pip install opencv-contrib-python numpy scipy

# 3D visualization
pip install open3d
pip install plotly
pip install pyvista

# Evaluation
pip install evo  # Trajectory evaluation

# Deep learning
pip install torch torchvision
```

### Feature Matchers

```python
# SuperGlue / LightGlue
# https://github.com/cvg/LightGlue

# LoFTR
# https://github.com/zju3dv/LoFTR

# DKM
# https://github.com/Parskatt/DKM
```

---

## 4. Datasets

### Odometry & SLAM

1. **KITTI Odometry Benchmark**
   - https://www.cvlibs.net/datasets/kitti/eval_odometry.php
   - Outdoor driving sequences
   - Stereo + LIDAR + GPS

2. **TUM RGB-D Dataset**
   - https://vision.in.tum.de/data/datasets/rgbd-dataset
   - Indoor RGB-D sequences
   - Ground truth from motion capture

3. **EuRoC MAV Dataset**
   - https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets
   - MAV visual-inertial data
   - Accurate ground truth

4. **ICL-NUIM**
   - https://www.doc.ic.ac.uk/~ahanda/VaFRIC/iclnuim.html
   - Synthetic RGB-D for evaluation

5. **ScanNet**
   - http://www.scan-net.org/
   - Large-scale indoor reconstruction

6. **ETH3D**
   - https://www.eth3d.net/
   - High-quality ground truth

### SfM Datasets

7. **Photo Tourism Datasets**
   - http://phototour.cs.washington.edu/datasets/
   - Landmark image collections

8. **1DSfM Dataset**
   - https://www.cs.cornell.edu/projects/1dsfm/
   - Large-scale SfM evaluation

9. **Tanks and Temples**
   - https://www.tanksandtemples.org/
   - MVS benchmark

---

## 5. Tutorial dan Courses

### Online Courses

1. **Multiple View Geometry - TU Munich**
   - https://vision.in.tum.de/teaching/online/mvg
   - Comprehensive course by Daniel Cremers

2. **Visual SLAM - ETH Zurich**
   - https://www.youtube.com/playlist?list=PLTBdjV_4f-EJn6udZ34tht9EVIW7lbeo4

3. **Robot Mapping - Uni Freiburg**
   - http://ais.informatik.uni-freiburg.de/teaching/ws13/mapping/
   - SLAM fundamentals

4. **Computer Vision II: Multiple View Geometry**
   - https://www.youtube.com/playlist?list=PLTBdjV_4f-EJn6udZ34tht9EVIW7lbeo4

### Tutorial Articles

5. **OpenCV SfM Tutorial**
   - https://docs.opencv.org/master/de/d7c/tutorial_table_of_content_sfm.html

6. **SLAM Tutorial (Cyrill Stachniss)**
   - https://www.youtube.com/playlist?list=PLgnQpQtFTOGQrZ4O5QzbIHgl3b1JHimN_

7. **Visual Odometry Tutorial (Scaramuzza)**
   - https://rpg.ifi.uzh.ch/visual_odometry_tutorial.html

### Blog Posts

8. **SLAM Overview (Tombone)**
   - https://www.tombone.de/slam-overview

9. **Visual SLAM Summary**
   - https://github.com/OpenSLAM-org/openslam_org

---

## 6. Research Groups

1. **Computer Vision Group, TUM**
   - https://vision.in.tum.de/
   - LSD-SLAM, DSO

2. **Robotics & Perception Group, UZH**
   - https://rpg.ifi.uzh.ch/
   - SVO, event cameras

3. **HKUST Aerial Robotics Group**
   - https://uav.hkust.edu.hk/
   - VINS-Mono

4. **Oxford VGG**
   - https://www.robots.ox.ac.uk/~vgg/
   - Multiple View Geometry

5. **University of Zaragoza SLAM Lab**
   - https://i3a.unizar.es/
   - ORB-SLAM

6. **MIT SPARK Lab**
   - https://web.mit.edu/sparklab/
   - Kimera

---

## 7. Evaluation Tools

### Trajectory Evaluation

```bash
# EVO - Evaluation of Odometry and SLAM
pip install evo

# Usage:
evo_ape kitti gt.txt estimated.txt
evo_rpe kitti gt.txt estimated.txt
evo_traj kitti gt.txt estimated.txt --plot
```

### Metrics

1. **Absolute Trajectory Error (ATE)**
   - Global consistency
   - RMSE of aligned trajectories

2. **Relative Pose Error (RPE)**
   - Local accuracy
   - Error over fixed distances/time

3. **Tracking Success Rate**
   - Percentage of successfully tracked frames

### Benchmark Websites

- KITTI: https://www.cvlibs.net/datasets/kitti/eval_odometry.php
- TUM RGB-D: https://vision.in.tum.de/data/datasets/rgbd-dataset/online_evaluation
- ETH3D: https://www.eth3d.net/slam_overview

---

## 8. Advanced Topics

### Semantic SLAM

1. **Kimera: an Open-Source Library for Real-Time Metric-Semantic SLAM**
   - Rosinol, A., et al. (2020)
   - https://github.com/MIT-SPARK/Kimera

2. **Fusion++: Volumetric Object-Level SLAM**
   - McCormac, J., et al. (2018)

### Dynamic SLAM

3. **DynaSLAM: Tracking, Mapping and Inpainting in Dynamic Scenes**
   - Bescos, B., et al. (2018)
   - https://github.com/BertaBesworking/DynaSLAM

### Multi-Robot SLAM

4. **Collaborative SLAM Overview**
   - Saeedi, S., et al. (2016)

### Event Camera SLAM

5. **Event-based Vision: A Survey**
   - Gallego, G., et al. (2020)

---

## 9. Tips Implementasi

### Numerical Stability

```python
# Selalu normalize coordinates
def normalize_points(pts):
    centroid = pts.mean(axis=0)
    pts_centered = pts - centroid
    avg_dist = np.mean(np.linalg.norm(pts_centered, axis=1))
    scale = np.sqrt(2) / avg_dist
    # ...
```

### RANSAC Best Practices

```python
# Adaptive iteration count
def compute_ransac_iterations(inlier_ratio, n_samples, confidence=0.999):
    if inlier_ratio == 0:
        return float('inf')
    return np.log(1 - confidence) / np.log(1 - inlier_ratio**n_samples)
```

### Bundle Adjustment Tips

```python
# Use sparse solvers for large problems
from scipy.sparse import lil_matrix
from scipy.optimize import least_squares

# Parameterize rotations properly (angle-axis, quaternions)
# Use robust loss functions (Huber, Cauchy)
```

---

## 10. Progression Path

```
1. Epipolar Geometry
   - 8-point algorithm
   - RANSAC
   ↓
2. Two-View Reconstruction
   - Triangulation
   - Essential matrix decomposition
   ↓
3. Visual Odometry
   - Feature tracking
   - Pose estimation
   ↓
4. Bundle Adjustment
   - Reprojection error
   - Sparse optimization
   ↓
5. Full SfM Pipeline
   - Incremental reconstruction
   ↓
6. Visual SLAM
   - Real-time tracking
   - Loop closure
   - Pose graph optimization
   ↓
7. Advanced SLAM
   - Visual-Inertial
   - Semantic
   - Multi-robot
```

---

*Referensi ini dikompilasi untuk mendukung pembelajaran Bab 11: Structure from Motion dan SLAM*
