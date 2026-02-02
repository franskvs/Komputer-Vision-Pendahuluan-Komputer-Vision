# Referensi Bab 10: Computational Photography

## 1. Paper Fundamental

### HDR Imaging

1. **Recovering High Dynamic Range Radiance Maps from Photographs**
   - Debevec, P. E., & Malik, J. (1997)
   - SIGGRAPH '97
   - Foundational paper untuk HDR imaging
   - Link: http://www.pauldebevec.com/Research/HDR/

2. **Photographic Tone Reproduction for Digital Images**
   - Reinhard, E., Stark, M., Shirley, P., & Ferwerda, J. (2002)
   - SIGGRAPH '02
   - Global dan local tone mapping operators
   - Link: https://www.cs.utah.edu/~reinhard/cdrom/

3. **Exposure Fusion**
   - Mertens, T., Kautz, J., & Van Reeth, F. (2007)
   - Pacific Graphics
   - Fusion tanpa HDR radiance map
   - Link: https://mericam.github.io/exposure_fusion/

4. **Adaptive Logarithmic Mapping For Displaying High Contrast Scenes**
   - Drago, F., Myszkowski, K., Annen, T., & Chiba, N. (2003)
   - Eurographics
   - Drago tone mapping operator

### Image Denoising

5. **A Non-Local Algorithm for Image Denoising**
   - Buades, A., Coll, B., & Morel, J. M. (2005)
   - CVPR 2005
   - Non-Local Means denoising
   - Link: https://www.ipol.im/pub/art/2011/bcm_nlm/

6. **Image Denoising by Sparse 3D Transform-Domain Collaborative Filtering**
   - Dabov, K., Foi, A., Katkovnik, V., & Egiazarian, K. (2007)
   - IEEE TIP
   - BM3D algorithm
   - Link: http://www.cs.tut.fi/~foi/GCF-BM3D/

7. **Bilateral Filtering for Gray and Color Images**
   - Tomasi, C., & Manduchi, R. (1998)
   - ICCV 1998
   - Edge-preserving smoothing

8. **Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising**
   - Zhang, K., Zuo, W., Chen, Y., Meng, D., & Zhang, L. (2017)
   - IEEE TIP
   - DnCNN deep denoising
   - Link: https://github.com/cszn/DnCNN

### Image Deblurring

9. **Blind Deconvolution Using a Normalized Sparsity Measure**
   - Krishnan, D., Tay, T., & Fergus, R. (2011)
   - CVPR 2011
   - Blind motion deblurring

10. **Removing Camera Shake from a Single Photograph**
    - Fergus, R., Singh, B., Hertzmann, A., Roweis, S. T., & Freeman, W. T. (2006)
    - SIGGRAPH '06
    - Seminal blind deconvolution paper

11. **Deblurring by Solving a Total Variation Problem**
    - Rudin, L. I., Osher, S., & Fatemi, E. (1992)
    - Physica D
    - Total variation regularization

### Super Resolution

12. **Image Super-Resolution Using Deep Convolutional Networks**
    - Dong, C., Loy, C. C., He, K., & Tang, X. (2014)
    - ECCV 2014 / TPAMI 2016
    - SRCNN - first deep learning SR
    - Link: https://arxiv.org/abs/1501.00092

13. **Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network**
    - Shi, W., et al. (2016)
    - CVPR 2016
    - ESPCN dengan sub-pixel convolution
    - Link: https://arxiv.org/abs/1609.05158

14. **Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network**
    - Ledig, C., et al. (2017)
    - CVPR 2017
    - SRGAN untuk perceptual quality
    - Link: https://arxiv.org/abs/1609.04802

15. **ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks**
    - Wang, X., et al. (2018)
    - ECCVW 2018
    - State-of-the-art GAN-based SR
    - Link: https://github.com/xinntao/ESRGAN

### Image Inpainting

16. **Region Filling and Object Removal by Exemplar-Based Image Inpainting**
    - Criminisi, A., Pérez, P., & Toyama, K. (2004)
    - IEEE TIP
    - Patch-based inpainting

17. **PatchMatch: A Randomized Correspondence Algorithm for Structural Image Editing**
    - Barnes, C., Shechtman, E., Finkelstein, A., & Goldman, D. B. (2009)
    - SIGGRAPH '09
    - Fast patch matching untuk inpainting
    - Link: https://gfx.cs.princeton.edu/pubs/Barnes_2009_PAR/

18. **Generative Image Inpainting with Contextual Attention**
    - Yu, J., Lin, Z., Yang, J., Shen, X., Lu, X., & Huang, T. S. (2018)
    - CVPR 2018
    - Deep learning inpainting
    - Link: https://github.com/JiahuiYu/generative_inpainting

19. **Free-Form Image Inpainting with Gated Convolution**
    - Yu, J., et al. (2019)
    - ICCV 2019
    - Improved deep inpainting

---

## 2. Buku Teks

1. **Computer Vision: Algorithms and Applications, 2nd Edition**
   - Szeliski, R. (2022)
   - Chapter 10: Computational Photography
   - Free online: https://szeliski.org/Book/

2. **Computational Photography: Methods and Applications**
   - Lukac, R. (Ed.) (2010)
   - CRC Press
   - Comprehensive coverage

3. **High Dynamic Range Imaging: Acquisition, Display, and Image-Based Lighting**
   - Reinhard, E., Heidrich, W., Debevec, P., Pattanaik, S., Ward, G., & Myszkowski, K. (2010)
   - Morgan Kaufmann
   - Definitive HDR reference

4. **Digital Image Processing**
   - Gonzalez, R. C., & Woods, R. E. (2018)
   - 4th Edition, Pearson
   - Image enhancement dan restoration fundamentals

---

## 3. Libraries dan Tools

### Python Libraries

```python
# Core
pip install opencv-contrib-python  # OpenCV with extra modules
pip install numpy scipy matplotlib

# Image processing
pip install scikit-image
pip install Pillow

# Denoising
pip install bm3d  # BM3D implementation
pip install scikit-learn  # Dictionary learning

# Deep learning
pip install torch torchvision  # PyTorch
pip install tensorflow keras  # TensorFlow

# HDR
pip install openexr  # EXR file support
pip install imageio  # Various HDR formats

# Quality metrics
pip install piq  # Perceptual Image Quality
pip install lpips  # Learned Perceptual Image Patch Similarity
```

### Specialized Tools

1. **Luminance HDR** - Open source HDR tonemapping
   - https://luminancehdr.software/

2. **OpenCV HDR Module**
   - cv2.createMergeDebevec()
   - cv2.createMergeMertens()
   - cv2.createTonemap*()

3. **GIMP G'MIC** - Image processing filters
   - https://gmic.eu/

4. **ImageMagick** - Command line processing
   - https://imagemagick.org/

### Pre-trained Models

1. **Real-ESRGAN** - Practical super resolution
   - https://github.com/xinntao/Real-ESRGAN

2. **DnCNN** - Deep denoising
   - https://github.com/cszn/DnCNN

3. **DeepFill** - Image inpainting
   - https://github.com/JiahuiYu/generative_inpainting

4. **LaMa** - Large mask inpainting
   - https://github.com/advimman/lama

---

## 4. Datasets

### HDR Datasets

1. **Fairchild HDR Survey**
   - http://rit-mcsl.org/fairchild/HDR.html
   - HDR images untuk testing

2. **HDR+ Burst Photography Dataset**
   - https://hdrplusdata.org/
   - Mobile HDR imaging

3. **HDRI Haven**
   - https://polyhaven.com/hdris
   - Free HDR environment maps

### Denoising Datasets

4. **BSD68** - Berkeley Segmentation Dataset
   - 68 images untuk denoising testing
   - https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/

5. **Set12** - Classic test images
   - Standard denoising benchmark

6. **Smartphone Image Denoising Dataset (SIDD)**
   - https://www.eecs.yorku.ca/~ka101/sidd/
   - Real smartphone noise

7. **DND (Darmstadt Noise Dataset)**
   - https://noise.visinf.tu-darmstadt.de/
   - Benchmark untuk real noise

### Super Resolution Datasets

8. **Set5, Set14, BSD100**
   - Classic SR test sets
   - https://cvnote.ddlee.cc/2019/09/22/image-super-resolution-datasets

9. **DIV2K** - DIVerse 2K resolution images
   - https://data.vision.ee.ethz.ch/cvl/DIV2K/
   - High quality training data

10. **Urban100**
    - Urban scenes dengan fine details
    - Challenging for SR

### Inpainting Datasets

11. **Places2**
    - https://places2.csail.mit.edu/
    - Scene images

12. **CelebA-HQ**
    - High quality face images
    - For face inpainting

---

## 5. Tutorial dan Course

### Online Courses

1. **Computational Photography - Georgia Tech (Udacity)**
   - https://www.udacity.com/course/computational-photography--ud955
   - Comprehensive free course

2. **Marc Levoy's Lectures on Digital Photography**
   - https://sites.google.com/site/maraborosf2/home
   - Fundamentals dari Google Pixel camera creator

3. **Image and Video Processing - Duke (Coursera)**
   - HDR dan image enhancement topics

### Tutorial Articles

4. **HDR Imaging using OpenCV (LearnOpenCV)**
   - https://learnopencv.com/high-dynamic-range-hdr-imaging-using-opencv-cpp-python/

5. **Image Denoising (Papers with Code)**
   - https://paperswithcode.com/task/image-denoising

6. **Super Resolution (Papers with Code)**
   - https://paperswithcode.com/task/image-super-resolution

### Video Tutorials

7. **Two Minute Papers** - Research summaries
   - https://www.youtube.com/c/K%C3%A1rolyZsolnai

8. **First Principles of Computer Vision**
   - https://www.youtube.com/c/FirstPrinciplesofComputerVision

---

## 6. Research Groups

1. **MIT CSAIL - Graphics**
   - https://graphics.csail.mit.edu/
   - Computational photography research

2. **Adobe Research**
   - https://research.adobe.com/
   - Practical CP applications

3. **Google Research - Computational Photography**
   - https://research.google/teams/perception/
   - Mobile CP (HDR+, Night Sight)

4. **KAIST Visual Computing Lab**
   - https://vclab.kaist.ac.kr/
   - HDR dan display research

5. **Stanford Computational Imaging**
   - https://www.computationalimaging.org/
   - Novel imaging techniques

---

## 7. Konferensi dan Jurnal

### Konferensi

1. **CVPR** - IEEE Conference on Computer Vision and Pattern Recognition
2. **ICCV** - International Conference on Computer Vision
3. **ECCV** - European Conference on Computer Vision
4. **SIGGRAPH** - ACM Special Interest Group on Computer Graphics
5. **ICCP** - IEEE International Conference on Computational Photography

### Jurnal

1. **IEEE Transactions on Image Processing (TIP)**
2. **IEEE Transactions on PAMI**
3. **ACM Transactions on Graphics (TOG)**
4. **International Journal of Computer Vision (IJCV)**

---

## 8. Code Repositories

### GitHub Collections

1. **Awesome Computational Photography**
   - https://github.com/rossant/awesome-computational-photography

2. **Image Quality Assessment**
   - https://github.com/chaofengc/IQA-PyTorch

3. **Super Resolution Collection**
   - https://github.com/ChaofWang/Awesome-Super-Resolution

4. **Image Denoising Collection**
   - https://github.com/wenbihan/reproducible-image-denoising-state-of-the-art

5. **HDR Imaging**
   - https://github.com/banterle/HDR_Toolbox

---

## 9. Aplikasi Praktis

### Mobile Photography

1. **Google Camera (Gcam)** - HDR+, Night Sight
   - https://ai.googleblog.com/2014/10/hdr-low-light-and-high-dynamic-range.html

2. **Apple Computational Photography**
   - Deep Fusion, Night mode
   - https://developer.apple.com/documentation/avfoundation/photo_capture

3. **Huawei AI Photography**
   - Master AI, AI stabilization

### Software Applications

4. **Adobe Lightroom** - HDR merge, denoise
5. **Capture One** - Professional editing
6. **Topaz Labs** - AI photo enhancement
   - DeNoise AI, Gigapixel AI, Sharpen AI
7. **DxO PhotoLab** - Deep PRIME denoising

---

## 10. Tips Pembelajaran

### Progression Path

```
1. Dasar Image Processing
   ↓
2. Filtering (Gaussian, Bilateral)
   ↓
3. HDR Basics (Exposure Fusion)
   ↓
4. Advanced Denoising (NLM, BM3D)
   ↓
5. Deblurring (Wiener, RL)
   ↓
6. Super Resolution (Interpolation → Deep Learning)
   ↓
7. Inpainting (Patch-based → Deep Learning)
   ↓
8. Integration (Photo Editor)
```

### Hands-on Projects

1. **Week 1-2**: HDR pipeline dari exposure stack
2. **Week 3-4**: Denoising comparison study
3. **Week 5-6**: Super resolution implementation
4. **Week 7-8**: Photo editor integration

### Evaluation Practice

- Selalu bandingkan dengan ground truth
- Use PSNR, SSIM untuk quantitative
- Visual inspection untuk perceptual quality
- Processing time untuk practical applications

---

*Referensi ini dikompilasi untuk mendukung pembelajaran Bab 10: Computational Photography*
