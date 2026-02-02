# Referensi Bab 13: 3D Reconstruction

## Buku Referensi Utama

### Computer Vision: Algorithms and Applications (2nd Edition)
- **Penulis**: Richard Szeliski
- **Bab**: 12 - 3D Reconstruction, 13 - Image-Based Rendering
- **Link**: https://szeliski.org/Book/
- **Topik**: Multi-view stereo, surface reconstruction, volumetric methods

### Multiple View Geometry in Computer Vision (2nd Edition)
- **Penulis**: Richard Hartley, Andrew Zisserman
- **Bab**: 10-17 - Reconstruction
- **Relevansi**: Theoretical foundation untuk 3D reconstruction

### 3D Computer Vision: Efficient Methods and Applications
- **Penulis**: Christian Wöhler
- **Topik**: Comprehensive coverage dari 3D vision methods

---

## Paper Fundamental

### Multi-View Stereo

1. **A Comparison and Evaluation of Multi-View Stereo Reconstruction Algorithms**
   - Penulis: S. Seitz et al.
   - Tahun: 2006 (CVPR)
   - Link: https://vision.middlebury.edu/mview/seitz_mview_cvpr06.pdf
   - Signifikansi: Benchmark MVS algorithms

2. **Accurate, Dense, and Robust Multi-View Stereopsis (PMVS)**
   - Penulis: Y. Furukawa, J. Ponce
   - Tahun: 2010 (TPAMI)
   - Link: https://www.di.ens.fr/pmvs/
   - Signifikansi: Patch-based dense MVS

3. **Multi-View Stereo: A Tutorial**
   - Penulis: Y. Furukawa, C. Hernandez
   - Tahun: 2015 (FnTCG)
   - Link: http://www.nowpublishers.com/article/Details/CGV-052
   - Signifikansi: Comprehensive MVS tutorial

### Surface Reconstruction

4. **Poisson Surface Reconstruction**
   - Penulis: M. Kazhdan, M. Bolitho, H. Hoppe
   - Tahun: 2006 (SGP)
   - Link: https://hhoppe.com/poissonrecon.pdf
   - Signifikansi: Standard untuk watertight reconstruction

5. **Screened Poisson Surface Reconstruction**
   - Penulis: M. Kazhdan, H. Hoppe
   - Tahun: 2013 (ToG)
   - Link: https://hhoppe.com/screenedpoisson.pdf
   - Signifikansi: Improved Poisson dengan data fidelity

6. **Marching Cubes: A High Resolution 3D Surface Construction Algorithm**
   - Penulis: W. Lorensen, H. Cline
   - Tahun: 1987 (SIGGRAPH)
   - Link: https://dl.acm.org/doi/10.1145/37401.37422
   - Signifikansi: Classic isosurface extraction

7. **The Ball-Pivoting Algorithm for Surface Reconstruction**
   - Penulis: F. Bernardini et al.
   - Tahun: 1999 (TVCG)
   - Link: https://vgc.poly.edu/~csilva/papers/tvcg99.pdf
   - Signifikansi: Incremental surface reconstruction

### TSDF dan Volumetric Methods

8. **KinectFusion: Real-time Dense Surface Mapping and Tracking**
   - Penulis: R. Newcombe et al.
   - Tahun: 2011 (ISMAR)
   - Link: https://www.microsoft.com/en-us/research/publication/kinectfusion-real-time-dense-surface-mapping-and-tracking/
   - Signifikansi: Real-time TSDF fusion

9. **A Volumetric Method for Building Complex Models from Range Images**
   - Penulis: B. Curless, M. Levoy
   - Tahun: 1996 (SIGGRAPH)
   - Link: https://graphics.stanford.edu/papers/volrange/volrange.pdf
   - Signifikansi: Original TSDF fusion

---

## Deep Learning 3D Reconstruction

### Implicit Representations

10. **Occupancy Networks: Learning 3D Reconstruction in Function Space**
    - Penulis: L. Mescheder et al.
    - Tahun: 2019 (CVPR)
    - Link: https://arxiv.org/abs/1812.03828
    - Code: https://github.com/autonomousvision/occupancy_networks
    - Signifikansi: Continuous implicit representation

11. **DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation**
    - Penulis: J. Park et al.
    - Tahun: 2019 (CVPR)
    - Link: https://arxiv.org/abs/1901.05103
    - Code: https://github.com/facebookresearch/DeepSDF
    - Signifikansi: Neural SDF representation

12. **IM-NET: Learning Implicit Fields for Generative Shape Modeling**
    - Penulis: Z. Chen, H. Zhang
    - Tahun: 2019 (CVPR)
    - Link: https://arxiv.org/abs/1812.02822
    - Signifikansi: Implicit decoder untuk 3D generation

### Neural Radiance Fields (NeRF)

13. **NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis**
    - Penulis: B. Mildenhall et al.
    - Tahun: 2020 (ECCV)
    - Link: https://arxiv.org/abs/2003.08934
    - Project: https://www.matthewtancik.com/nerf
    - Signifikansi: Revolutionary view synthesis

14. **Instant Neural Graphics Primitives with a Multiresolution Hash Encoding**
    - Penulis: T. Müller et al.
    - Tahun: 2022 (ToG)
    - Link: https://arxiv.org/abs/2201.05989
    - Code: https://github.com/NVlabs/instant-ngp
    - Signifikansi: Fast NeRF training

15. **Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields**
    - Penulis: J. Barron et al.
    - Tahun: 2021 (ICCV)
    - Link: https://arxiv.org/abs/2103.13415
    - Signifikansi: Anti-aliased NeRF

16. **NeuS: Learning Neural Implicit Surfaces by Volume Rendering for Multi-view Reconstruction**
    - Penulis: P. Wang et al.
    - Tahun: 2021 (NeurIPS)
    - Link: https://arxiv.org/abs/2106.10689
    - Signifikansi: NeRF for surface reconstruction

### Deep MVS

17. **MVSNet: Depth Inference for Unstructured Multi-view Stereo**
    - Penulis: Y. Yao et al.
    - Tahun: 2018 (ECCV)
    - Link: https://arxiv.org/abs/1804.02505
    - Code: https://github.com/YoYo000/MVSNet
    - Signifikansi: Deep learning MVS

18. **Cascade Cost Volume for High-Resolution Multi-View Stereo**
    - Penulis: X. Gu et al.
    - Tahun: 2020 (CVPR)
    - Link: https://arxiv.org/abs/1912.06378
    - Signifikansi: Coarse-to-fine MVS

19. **PatchmatchNet: Learned Multi-View Patchmatch Stereo**
    - Penulis: F. Wang et al.
    - Tahun: 2021 (CVPR)
    - Link: https://arxiv.org/abs/2012.01411
    - Signifikansi: Efficient learned MVS

---

## Dataset dan Benchmark

### Multi-View Stereo Datasets

20. **DTU Dataset**
    - Link: https://roboimagedata.compute.dtu.dk/?page_id=36
    - Konten: 124 scenes dengan ground truth
    - Paper: Jensen et al. (2014)

21. **Tanks and Temples**
    - Link: https://www.tanksandtemples.org/
    - Konten: Indoor/outdoor scenes
    - Paper: Knapitsch et al. (2017)

22. **ETH3D Benchmark**
    - Link: https://www.eth3d.net/
    - Konten: High-resolution multi-view
    - Paper: Schops et al. (2017)

23. **BlendedMVS**
    - Link: https://github.com/YoYo000/BlendedMVS
    - Konten: Large-scale dataset
    - Paper: Yao et al. (2020)

### Shape Datasets

24. **ShapeNet**
    - Link: https://shapenet.org/
    - Konten: 3D model database
    - Paper: Chang et al. (2015)

25. **ModelNet**
    - Link: https://modelnet.cs.princeton.edu/
    - Konten: Clean 3D CAD models
    - Paper: Wu et al. (2015)

26. **Stanford 3D Scanning Repository**
    - Link: http://graphics.stanford.edu/data/3Dscanrep/
    - Konten: Classic 3D scans (bunny, dragon, etc.)

---

## Tools dan Software

### Open Source

| Tool | Deskripsi | Link |
|------|-----------|------|
| COLMAP | SfM + MVS | https://colmap.github.io/ |
| OpenMVS | Dense reconstruction | https://github.com/cdcseacave/openMVS |
| Open3D | Point cloud & mesh processing | http://www.open3d.org/ |
| MeshLab | Mesh editing & processing | https://www.meshlab.net/ |
| CloudCompare | Point cloud processing | https://www.cloudcompare.org/ |
| PCL | Point Cloud Library | https://pointclouds.org/ |

### Commercial

| Software | Deskripsi |
|----------|-----------|
| Agisoft Metashape | Photogrammetry |
| RealityCapture | Fast photogrammetry |
| Pix4D | Drone mapping |
| 3DF Zephyr | Photogrammetry |

### Python Libraries

```python
# Point cloud processing
import open3d as o3d
import trimesh
import pyvista as pv

# Mesh processing
import pymeshlab
from scipy.spatial import Delaunay

# Deep learning
import torch
import pytorch3d
```

---

## Code Repositories

### Classical Methods
| Repository | Deskripsi | Link |
|-----------|-----------|------|
| COLMAP | SfM + MVS | https://github.com/colmap/colmap |
| OpenMVS | Dense MVS | https://github.com/cdcseacave/openMVS |
| MVE | Multi-View Environment | https://github.com/simonfuhrmann/mve |

### Deep Learning
| Repository | Deskripsi | Link |
|-----------|-----------|------|
| Occupancy Networks | Implicit 3D | https://github.com/autonomousvision/occupancy_networks |
| DeepSDF | Neural SDF | https://github.com/facebookresearch/DeepSDF |
| NeRF-PyTorch | NeRF implementation | https://github.com/yenchenlin/nerf-pytorch |
| Instant-NGP | Fast NeRF | https://github.com/NVlabs/instant-ngp |
| MVSNet | Deep MVS | https://github.com/YoYo000/MVSNet |
| NerfStudio | NeRF framework | https://github.com/nerfstudio-project/nerfstudio |

---

## Tutorial dan Course

### Video Lectures

1. **First Principles of Computer Vision - 3D Reconstruction**
   - Instructor: Shree Nayar (Columbia)
   - Link: https://fpcv.cs.columbia.edu/
   - Topik: Stereo, multi-view, surface reconstruction

2. **3D Machine Learning**
   - Instructor: Stanford CS231A
   - Link: https://web.stanford.edu/class/cs231a/

3. **Neural Radiance Fields Tutorial**
   - CVPR 2022 Tutorial
   - Link: https://www.neuralradiancefields.com/

### Online Resources

4. **Open3D Tutorial**
   - Link: http://www.open3d.org/docs/release/tutorial/
   - Topik: Point cloud, mesh, RGBD

5. **PyTorch3D Tutorial**
   - Link: https://pytorch3d.org/tutorials/
   - Topik: Differentiable rendering, mesh operations

6. **COLMAP Tutorial**
   - Link: https://colmap.github.io/tutorial.html
   - Topik: SfM workflow

---

## Evaluation Metrics

### Point Cloud Metrics
- **Chamfer Distance**: Bidirectional average distance
- **Earth Mover Distance**: Optimal transport distance
- **F-Score**: Precision/recall at distance threshold

### Surface Metrics
- **Hausdorff Distance**: Maximum minimum distance
- **Mean Surface Distance**: Average point-to-surface
- **Normal Consistency**: Angle between normals

### Rendering Metrics (NeRF)
- **PSNR**: Peak signal-to-noise ratio
- **SSIM**: Structural similarity
- **LPIPS**: Learned perceptual similarity

---

## Konferensi dan Journal

### Top Venues
- **SIGGRAPH/ToG** - Computer graphics
- **CVPR/ICCV/ECCV** - Computer vision
- **3DV** - 3D vision
- **TPAMI/IJCV** - Journals
- **NeurIPS/ICML** - Machine learning

### Workshops
- 3D Vision Workshop (CVPR/ICCV)
- 3D Reconstruction Meets Semantics (ECCV)
- Neural Rendering Workshop

---

## Trending Topics (2023-2024)

1. **3D Gaussian Splatting** - Real-time neural rendering
2. **Large Reconstruction Models** - Foundation models untuk 3D
3. **Text-to-3D** - Generate 3D dari text prompt
4. **NeRF variants** - Dynamic, relightable, editable
5. **Implicit-Explicit Hybrid** - Combining representations
6. **Single-Image 3D** - Reconstruction dari satu gambar
