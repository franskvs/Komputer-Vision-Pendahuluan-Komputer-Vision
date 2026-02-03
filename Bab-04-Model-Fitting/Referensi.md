# Referensi Bab 4: Model Fitting dan Feature Matching

## Referensi Utama

### Buku Teks
1. **Szeliski, R. (2022)**. *Computer Vision: Algorithms and Applications, 2nd Edition*. Springer.
   - Chapter 7: Feature Detection and Matching
   - Chapter 8: Image Alignment and Stitching
   - Website: https://szeliski.org/Book/

2. **Hartley, R., & Zisserman, A. (2004)**. *Multiple View Geometry in Computer Vision, 2nd Edition*. Cambridge University Press.
   - Comprehensive treatment of projective geometry and RANSAC

3. **Prince, S.J.D. (2012)**. *Computer Vision: Models, Learning, and Inference*. Cambridge University Press.
   - Chapter 13: Image transformations

## Dokumentasi Library

### OpenCV Documentation
- **Feature Detection**: https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html
- **RANSAC Homography**: https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html
- **Hough Transform**: https://docs.opencv.org/4.x/d6/d10/tutorial_py_houghlines.html
- **Optical Flow**: https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html

## Paper Klasik

### Feature Detection
1. **Harris, C., & Stephens, M. (1988)**. A Combined Corner and Edge Detector. *Alvey Vision Conference*.
   - Harris Corner Detector original paper

2. **Rosten, E., & Drummond, T. (2006)**. Machine Learning for High-Speed Corner Detection. *ECCV*.
   - FAST feature detector

3. **Rublee, E., et al. (2011)**. ORB: An Efficient Alternative to SIFT or SURF. *ICCV*.
   - ORB descriptor paper

4. **Lowe, D.G. (2004)**. Distinctive Image Features from Scale-Invariant Keypoints. *IJCV*.
   - SIFT original paper
   - DOI: 10.1023/B:VISI.0000029664.99615.94

5. **Alcantarilla, P.F., et al. (2012)**. KAZE Features. *ECCV*.
   - KAZE/AKAZE paper

### RANSAC
6. **Fischler, M.A., & Bolles, R.C. (1981)**. Random Sample Consensus: A Paradigm for Model Fitting with Applications to Image Analysis and Automated Cartography. *Communications of the ACM*.
   - RANSAC original paper
   - DOI: 10.1145/358669.358692

### Hough Transform
7. **Duda, R.O., & Hart, P.E. (1972)**. Use of the Hough Transformation to Detect Lines and Curves in Pictures. *Communications of the ACM*.
   - Hough Transform original paper

8. **Illingworth, J., & Kittler, J. (1988)**. A Survey of the Hough Transform. *Computer Vision, Graphics, and Image Processing*.
   - Comprehensive survey

### Optical Flow
9. **Lucas, B.D., & Kanade, T. (1981)**. An Iterative Image Registration Technique with an Application to Stereo Vision. *IJCAI*.
   - Lucas-Kanade method

10. **Farneback, G. (2003)**. Two-Frame Motion Estimation Based on Polynomial Expansion. *SCIA*.
    - Farneback dense optical flow

11. **Horn, B.K.P., & Schunck, B.G. (1981)**. Determining Optical Flow. *Artificial Intelligence*.
    - Horn-Schunck method (classical)

### Deep Learning Methods
12. **Dosovitskiy, A., et al. (2015)**. FlowNet: Learning Optical Flow with Convolutional Networks. *ICCV*.
    - First CNN-based optical flow

13. **Teed, Z., & Deng, J. (2020)**. RAFT: Recurrent All-Pairs Field Transforms for Optical Flow. *ECCV*.
    - State-of-the-art optical flow

## Tutorial dan Artikel Online

### Feature Matching
- **OpenCV Feature Matching Tutorial**: https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
- **Learn OpenCV - Feature Matching**: https://learnopencv.com/image-alignment-feature-based-using-opencv-c-python/

### RANSAC
- **RANSAC Explained**: https://www.mathworks.com/discovery/ransac.html
- **PyImageSearch - RANSAC**: https://pyimagesearch.com/2021/01/04/opencv-panorama-stitching/

### Homography
- **OpenCV Homography Tutorial**: https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html
- **Learn OpenCV - Homography**: https://learnopencv.com/homography-examples-using-opencv-python-c/

### Document Scanner
- **PyImageSearch - Document Scanner**: https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
- **4-Point Transform**: https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

### Optical Flow
- **OpenCV Optical Flow Tutorial**: https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html
- **Learn OpenCV - Optical Flow**: https://learnopencv.com/optical-flow-in-opencv/

## Video Tutorial

### YouTube Channels
1. **Computerphile**: Feature detection explanations
2. **First Principles of Computer Vision**: RANSAC, Homography
3. **Sentdex**: Python OpenCV tutorials

### Specific Videos
- RANSAC Explained: https://www.youtube.com/watch?v=9D5rrtCC_E0
- Optical Flow Visualization: https://www.youtube.com/watch?v=lnXFcmLB7sM

## Dataset untuk Latihan

### Feature Matching & Homography
1. **Oxford Affine Covariant Regions Dataset**: 
   https://www.robots.ox.ac.uk/~vgg/research/affine/
   - Standard benchmark untuk feature matching

2. **HPatches**: 
   https://github.com/hpatches/hpatches-dataset
   - Homography patches dataset

### Optical Flow
3. **MPI Sintel**: 
   http://sintel.is.tue.mpg.de/
   - Optical flow benchmark

4. **KITTI Flow**: 
   http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=flow
   - Real-world optical flow

5. **Flying Chairs**: 
   https://lmb.informatik.uni-freiburg.de/resources/datasets/FlyingChairs.en.html
   - Synthetic dataset untuk training

### Document Scanning
6. **SmartDoc-QA**: 
   https://github.com/jlerouge/ICDAR-2015-SmartDoc
   - Document capture dataset

## Tools dan Library Tambahan

### Python
- **scikit-image**: `from skimage import feature, transform`
- **Kornia**: https://kornia.github.io/ (differentiable CV)
- **OpenCV-contrib**: Extended modules

### Deep Learning
- **PyTorch**: Flow networks implementation
- **RAFT Repository**: https://github.com/princeton-vl/RAFT
- **SuperGlue**: https://github.com/magicleap/SuperGluePretrainedNetwork

## Aplikasi Praktis

### Commercial Applications
1. **Google Photos**: Image stitching untuk panorama
2. **Adobe Photoshop**: Content-aware fill, panorama
3. **Smartphone Cameras**: Night mode, HDR alignment
4. **Tesla Autopilot**: Optical flow untuk motion estimation
5. **CamScanner**: Document perspective correction

### Open Source Projects
1. **OpenCV Stitching**: https://github.com/opencv/opencv/tree/4.x/samples/cpp/stitching
2. **Hugin**: Panorama stitcher (http://hugin.sourceforge.net/)
3. **OpenSfM**: Structure from Motion (https://github.com/mapillary/OpenSfM)

## Catatan Penting

### Patent Status
- **SIFT**: Patent expired 2020, now freely usable
- **SURF**: Still patented, use SIFT atau ORB sebagai alternatif
- **ORB**: Free to use (developed as SIFT alternative)

### Best Practices
1. Gunakan ORB untuk real-time applications
2. SIFT lebih akurat untuk offline processing
3. RANSAC essential untuk robust estimation
4. Dense optical flow mahal computationally
5. Consider GPU acceleration untuk production
