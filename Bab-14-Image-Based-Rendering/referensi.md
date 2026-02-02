# Referensi Bab 14: Image-Based Rendering

## Buku Referensi Utama

### Computer Vision: Algorithms and Applications (2nd Edition)
- **Penulis**: Richard Szeliski
- **Bab**: 13 - Image-Based Rendering, 14 - Recognition
- **Link**: https://szeliski.org/Book/
- **Topik**: View interpolation, light fields, panoramas, IBR

### Image-Based Rendering
- **Penulis**: Heung-Yeung Shum, Shing-Chow Chan, Sing Bing Kang
- **Penerbit**: Springer
- **Topik**: Comprehensive coverage of IBR techniques

---

## Paper Fundamental

### Light Fields

1. **Light Field Rendering**
   - Penulis: M. Levoy, P. Hanrahan
   - Tahun: 1996 (SIGGRAPH)
   - Link: https://graphics.stanford.edu/papers/light/
   - Signifikansi: Foundational light field paper

2. **The Lumigraph**
   - Penulis: S. Gortler et al.
   - Tahun: 1996 (SIGGRAPH)
   - Link: https://dl.acm.org/doi/10.1145/237170.237200
   - Signifikansi: Similar approach, different focus

3. **Plenoptic Modeling: An Image-Based Rendering System**
   - Penulis: L. McMillan, G. Bishop
   - Tahun: 1995 (SIGGRAPH)
   - Link: https://www.cs.unc.edu/~mcmillan/pubs/sig95.pdf
   - Signifikansi: Early plenoptic function work

4. **Unstructured Light Fields**
   - Penulis: M. Davis et al.
   - Tahun: 2012 (CGF)
   - Link: https://graphics.stanford.edu/papers/ulr/
   - Signifikansi: Rendering dari unstructured captures

### View Morphing dan Interpolation

5. **View Morphing**
   - Penulis: S. Seitz, C. Dyer
   - Tahun: 1996 (SIGGRAPH)
   - Link: https://www.cs.washington.edu/research/graphics/vm/
   - Signifikansi: Classic view interpolation

6. **View Synthesis using Stereo Vision**
   - Penulis: S. Laveau, O. Faugeras
   - Tahun: 1994 (Springer)
   - Signifikansi: Stereo-based view synthesis

7. **Image Morphing: A Survey**
   - Penulis: G. Wolberg
   - Tahun: 1998 (TVCG)
   - Link: https://www.cs.cmu.edu/~ph/morph.htm
   - Signifikansi: Comprehensive morphing survey

### View-Dependent Texture Mapping

8. **View-Dependent Texture Mapping on Surfaces**
   - Penulis: P. Debevec et al.
   - Tahun: 1996 (SIGGRAPH)
   - Link: https://www.pauldebevec.com/Research/VDT/
   - Signifikansi: Textured IBR with geometry

9. **Unstructured Lumigraph Rendering**
   - Penulis: C. Buehler et al.
   - Tahun: 2001 (SIGGRAPH)
   - Link: https://grail.cs.washington.edu/projects/ulr/
   - Signifikansi: Blend multiple views

---

## Depth Image-Based Rendering

10. **DIBR: A New Image-Based Rendering Approach**
    - Penulis: C. Fehn
    - Tahun: 2004 (SPIE)
    - Signifikansi: DIBR fundamentals

11. **Depth-Image-Based Rendering (DIBR), Compression, and Transmission for a New Approach on 3D-TV**
    - Penulis: C. Fehn
    - Tahun: 2004
    - Signifikansi: DIBR untuk 3D TV

12. **A Layered Approach to Stereo Reconstruction**
    - Penulis: S. Baker et al.
    - Tahun: 1998 (CVPR)
    - Signifikansi: Layer-based rendering

---

## Panoramas dan 360° Rendering

13. **QuickTime VR - An Image-Based Approach to Virtual Environment Navigation**
    - Penulis: S. Chen
    - Tahun: 1995 (SIGGRAPH)
    - Signifikansi: Commercial panorama system

14. **Creating Full View Panoramic Image Mosaics and Environment Maps**
    - Penulis: R. Szeliski, H. Shum
    - Tahun: 1997 (SIGGRAPH)
    - Link: https://www.microsoft.com/en-us/research/publication/creating-full-view-panoramic-image-mosaics-and-environment-maps/
    - Signifikansi: Panorama stitching

15. **A Flexible New Technique for Camera Calibration**
    - Penulis: Z. Zhang
    - Tahun: 2000 (TPAMI)
    - Link: https://www.microsoft.com/en-us/research/publication/a-flexible-new-technique-for-camera-calibration/
    - Signifikansi: Checkerboard calibration

---

## Neural Image-Based Rendering

### Neural Radiance Fields (NeRF)

16. **NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis**
    - Penulis: B. Mildenhall et al.
    - Tahun: 2020 (ECCV)
    - Link: https://arxiv.org/abs/2003.08934
    - Project: https://www.matthewtancik.com/nerf
    - Signifikansi: Revolutionary neural view synthesis

17. **NeRF++: Analyzing and Improving Neural Radiance Fields**
    - Penulis: K. Zhang et al.
    - Tahun: 2020
    - Link: https://arxiv.org/abs/2010.07492
    - Signifikansi: NeRF for unbounded scenes

18. **Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields**
    - Penulis: J. Barron et al.
    - Tahun: 2021 (ICCV)
    - Link: https://arxiv.org/abs/2103.13415
    - Signifikansi: Anti-aliasing untuk NeRF

19. **Instant Neural Graphics Primitives**
    - Penulis: T. Müller et al.
    - Tahun: 2022 (ToG)
    - Link: https://arxiv.org/abs/2201.05989
    - Code: https://github.com/NVlabs/instant-ngp
    - Signifikansi: Fast NeRF training

20. **3D Gaussian Splatting for Real-Time Radiance Field Rendering**
    - Penulis: B. Kerbl et al.
    - Tahun: 2023 (SIGGRAPH)
    - Link: https://arxiv.org/abs/2308.04079
    - Project: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/
    - Signifikansi: Real-time neural rendering

### Multi-Plane Images

21. **Stereo Magnification: Learning View Synthesis using Multiplane Images**
    - Penulis: T. Zhou et al.
    - Tahun: 2018 (SIGGRAPH)
    - Link: https://arxiv.org/abs/1805.09817
    - Signifikansi: MPI representation

22. **DeepView: View Synthesis with Learned Gradient Descent**
    - Penulis: J. Flynn et al.
    - Tahun: 2019 (CVPR)
    - Link: https://arxiv.org/abs/1906.07316
    - Signifikansi: Iterative view synthesis

23. **Single-View View Synthesis with Multiplane Images**
    - Penulis: R. Tucker, N. Snavely
    - Tahun: 2020 (CVPR)
    - Link: https://single-view-mpi.github.io/
    - Signifikansi: MPI dari single image

---

## Image Blending

24. **A Multiresolution Spline With Application to Image Mosaics**
    - Penulis: P. Burt, E. Adelson
    - Tahun: 1983 (ToG)
    - Link: https://dl.acm.org/doi/10.1145/245.247
    - Signifikansi: Laplacian pyramid blending

25. **Poisson Image Editing**
    - Penulis: P. Pérez et al.
    - Tahun: 2003 (SIGGRAPH)
    - Link: https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf
    - Signifikansi: Seamless cloning

---

## Dataset dan Benchmark

### Light Field Datasets

26. **Stanford Light Field Archive**
    - Link: http://lightfield.stanford.edu/
    - Konten: Various light field captures
    - Format: Sub-aperture images

27. **Lytro Light Field Dataset**
    - Link: https://www.irisa.fr/temics/demos/lightField/index.html
    - Konten: Consumer light field camera data

### IBR Datasets

28. **Tanks and Temples**
    - Link: https://www.tanksandtemples.org/
    - Konten: Multi-view scenes
    - Usage: IBR evaluation

29. **NeRF Synthetic Dataset**
    - Link: https://drive.google.com/drive/folders/128yBriW1IG_3NJ5Rp7APSTZsJqdJdfc1
    - Konten: Synthetic scenes untuk NeRF

30. **LLFF (Local Light Field Fusion)**
    - Link: https://github.com/Fyusion/LLFF
    - Konten: Forward-facing scenes

---

## Tools dan Software

### Panorama Tools

| Tool | Deskripsi | Link |
|------|-----------|------|
| Hugin | Open source panorama stitcher | http://hugin.sourceforge.net/ |
| PTGui | Commercial stitching | https://www.ptgui.com/ |
| AutoStitch | Academic tool | http://matthewalunbrown.com/autostitch/autostitch.html |

### Light Field Tools

| Tool | Deskripsi |
|------|-----------|
| MATLAB Light Field Toolbox | Processing utilities |
| Lytro Desktop | Consumer LF software |

### Neural IBR

| Repository | Deskripsi | Link |
|-----------|-----------|------|
| NeRF-PyTorch | NeRF implementation | https://github.com/yenchenlin/nerf-pytorch |
| Instant-NGP | Fast NeRF | https://github.com/NVlabs/instant-ngp |
| NerfStudio | NeRF framework | https://github.com/nerfstudio-project/nerfstudio |
| Gaussian Splatting | Real-time rendering | https://github.com/graphdeco-inria/gaussian-splatting |
| LLFF | Local light field fusion | https://github.com/Fyusion/LLFF |

### OpenCV Functions
```python
# Stitching
cv2.Stitcher_create()
cv2.createStitcher()

# Warping
cv2.warpPerspective()
cv2.warpAffine()
cv2.remap()

# Blending
cv2.seamlessClone()
cv2.createMergeMertens()  # Exposure fusion
```

---

## Tutorial dan Course

### Video Lectures

1. **SIGGRAPH Course: Image-Based Rendering**
   - Various years
   - Comprehensive IBR overview

2. **First Principles of Computer Vision - Panoramas**
   - Instructor: Shree Nayar
   - Link: https://fpcv.cs.columbia.edu/

3. **NeRF Explained**
   - Various YouTube tutorials
   - Covers NeRF architecture dan training

### Online Resources

4. **LearnOpenCV - Panorama Stitching**
   - Link: https://learnopencv.com/image-stitching-with-opencv-python/

5. **PyImageSearch - Image Stitching**
   - Link: https://www.pyimagesearch.com/

6. **Matthew Tancik's NeRF Tutorial**
   - Link: https://www.matthewtancik.com/nerf

---

## Evaluation Metrics

### Image Quality
- **PSNR**: Peak Signal-to-Noise Ratio
- **SSIM**: Structural Similarity Index
- **LPIPS**: Learned Perceptual Image Patch Similarity
- **FID**: Fréchet Inception Distance

### IBR-Specific
- **Reprojection error**: Geometric accuracy
- **Temporal consistency**: Frame-to-frame smoothness
- **Stitching seams**: Boundary visibility
- **Ghosting artifacts**: Double images

---

## Konferensi dan Journal

### Top Venues
- **SIGGRAPH/ToG** - Computer graphics
- **CVPR/ICCV/ECCV** - Computer vision
- **TVCG** - Visualization
- **CGF** - Computer Graphics Forum
- **3DV** - 3D Vision

### Specialized
- **Eurographics Symposium on Rendering**
- **High Performance Graphics**
- **VMV** - Vision, Modeling and Visualization

---

## Trending Topics (2023-2024)

1. **3D Gaussian Splatting**
   - Real-time rendering
   - Fast training
   - High quality

2. **Diffusion Models untuk View Synthesis**
   - Zero-shot novel view
   - Generative capabilities

3. **Large Reconstruction Models**
   - Foundation models untuk 3D
   - Few-shot reconstruction

4. **Neural Light Fields**
   - Combining light fields dengan neural networks

5. **Mobile Neural Rendering**
   - Real-time pada smartphones
   - Edge deployment

6. **Dynamic Scene Rendering**
   - NeRF untuk video
   - Deformable scenes
