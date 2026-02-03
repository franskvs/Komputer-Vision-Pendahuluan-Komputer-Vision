# Referensi Bab 6: Recognition

## Buku Utama

### Computer Vision: Algorithms and Applications, 2nd Edition
- **Author**: Richard Szeliski
- **Chapter**: Chapter 6 - Recognition
- **URL**: https://szeliski.org/Book/
- **Topics Covered**:
  - Face detection and recognition
  - Object detection and classification
  - Scene recognition
  - Instance recognition

## Paper dan Artikel Ilmiah

### Face Detection

1. **Viola-Jones Face Detection**
   - Viola, P., & Jones, M. (2001). Rapid Object Detection using a Boosted Cascade of Simple Features
   - URL: https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf
   - Kontribusi: Haar cascade classifier, integral images

2. **MTCNN (Multi-task Cascaded CNNs)**
   - Zhang, K., et al. (2016). Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks
   - URL: https://arxiv.org/abs/1604.02878
   - Kontribusi: Multi-stage face detection

3. **RetinaFace**
   - Deng, J., et al. (2020). RetinaFace: Single-shot Multi-level Face Localisation in the Wild
   - URL: https://arxiv.org/abs/1905.00641
   - Kontribusi: State-of-the-art face detection

### Face Recognition

4. **FaceNet**
   - Schroff, F., et al. (2015). FaceNet: A Unified Embedding for Face Recognition and Clustering
   - URL: https://arxiv.org/abs/1503.03832
   - Kontribusi: Face embeddings, triplet loss

5. **DeepFace**
   - Taigman, Y., et al. (2014). DeepFace: Closing the Gap to Human-Level Performance in Face Verification
   - URL: https://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Taigman_DeepFace_Closing_the_2014_CVPR_paper.pdf

6. **ArcFace**
   - Deng, J., et al. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition
   - URL: https://arxiv.org/abs/1801.07698
   - Kontribusi: Angular margin loss

### Object Classification

7. **AlexNet**
   - Krizhevsky, A., et al. (2012). ImageNet Classification with Deep Convolutional Neural Networks
   - URL: https://papers.nips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf

8. **VGGNet**
   - Simonyan, K., & Zisserman, A. (2014). Very Deep Convolutional Networks for Large-Scale Image Recognition
   - URL: https://arxiv.org/abs/1409.1556

9. **ResNet**
   - He, K., et al. (2016). Deep Residual Learning for Image Recognition
   - URL: https://arxiv.org/abs/1512.03385

10. **EfficientNet**
    - Tan, M., & Le, Q. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
    - URL: https://arxiv.org/abs/1905.11946

### Scene Recognition

11. **Places Dataset**
    - Zhou, B., et al. (2017). Places: A 10 Million Image Database for Scene Recognition
    - URL: http://places2.csail.mit.edu/
    - Kontribusi: Large-scale scene recognition dataset

12. **Scene Recognition Survey**
    - Xie, G., et al. (2020). Scene Recognition: A Comprehensive Survey
    - URL: https://arxiv.org/abs/2001.00443

### OCR dan Text Recognition

13. **EAST Text Detector**
    - Zhou, X., et al. (2017). EAST: An Efficient and Accurate Scene Text Detector
    - URL: https://arxiv.org/abs/1704.03155

14. **CRAFT**
    - Baek, Y., et al. (2019). Character Region Awareness for Text Detection
    - URL: https://arxiv.org/abs/1904.01941

15. **Tesseract OCR**
    - Smith, R. (2007). An Overview of the Tesseract OCR Engine
    - URL: https://github.com/tesseract-ocr/tesseract

## Dokumentasi Library

### OpenCV Face Module
- OpenCV Face Recognition: https://docs.opencv.org/4.x/da/d60/tutorial_face_main.html
- LBPH Face Recognizer: https://docs.opencv.org/4.x/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html
- Haar Cascade Classifier: https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html

### face_recognition Library
- Documentation: https://face-recognition.readthedocs.io/
- GitHub: https://github.com/ageitgey/face_recognition
- Installation Guide: https://github.com/ageitgey/face_recognition#installation

### dlib
- Main Site: http://dlib.net/
- Face Recognition: http://dlib.net/face_recognition.py.html
- CNN Face Detector: http://dlib.net/cnn_face_detector.py.html

### Tesseract OCR
- Documentation: https://tesseract-ocr.github.io/
- pytesseract: https://pypi.org/project/pytesseract/

## Dataset

### Face Detection/Recognition
1. **LFW (Labeled Faces in the Wild)**
   - URL: http://vis-www.cs.umass.edu/lfw/
   - 13,000+ images, 5,749 people

2. **WIDER FACE**
   - URL: http://shuoyang1213.me/WIDERFACE/
   - 32,203 images, 393,703 faces

3. **CelebA**
   - URL: https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
   - 200,000+ celebrity images

4. **VGGFace2**
   - URL: https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/
   - 3.31 million images, 9,131 subjects

### Object Classification
5. **ImageNet**
   - URL: https://www.image-net.org/
   - 14+ million images, 1000 classes

6. **CIFAR-10/100**
   - URL: https://www.cs.toronto.edu/~kriz/cifar.html
   - CIFAR-10: 60,000 images, 10 classes
   - CIFAR-100: 60,000 images, 100 classes

### Scene Recognition
7. **Places365**
   - URL: http://places2.csail.mit.edu/
   - 1.8 million images, 365 scene categories

8. **SUN Database**
   - URL: https://vision.princeton.edu/projects/2010/SUN/
   - 130,519 images, 908 scene categories

### OCR
9. **ICDAR Datasets**
   - URL: https://rrc.cvc.uab.es/
   - Scene text detection and recognition

10. **SVT (Street View Text)**
    - URL: http://www.iapr-tc11.org/mediawiki/index.php/The_Street_View_Text_Dataset
    - Street view images with text

## Tutorial dan Course

### Face Recognition
- Face Recognition with Python - Real Python
  https://realpython.com/face-recognition-with-python/

- Face Detection with OpenCV and Deep Learning
  https://pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/

### Scene Recognition
- Places365 CNN Model
  https://github.com/CSAILVision/places365

### OCR
- Tesseract OCR Tutorial
  https://nanonets.com/blog/ocr-with-tesseract/

- PaddleOCR Tutorial
  https://github.com/PaddlePaddle/PaddleOCR

## Pre-trained Models

### Face Detection
- OpenCV DNN face detector (Caffe model)
  https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector

- MTCNN
  https://github.com/ipazc/mtcnn

### Face Recognition
- dlib face recognition model
  http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2

- OpenCV face recognition models
  https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface

### Scene Classification
- Places365 models (ResNet, VGG)
  https://github.com/CSAILVision/places365

### OCR
- Tesseract language data
  https://github.com/tesseract-ocr/tessdata

- EAST text detector
  https://github.com/argman/EAST

## Video Tutorial

### YouTube Resources
1. Face Recognition Full Course - freeCodeCamp
   https://www.youtube.com/watch?v=t-DPPqmN-3M

2. OpenCV Face Detection Tutorial
   https://www.youtube.com/watch?v=WQeoO7MI0Bs

3. OCR with Python and Tesseract
   https://www.youtube.com/watch?v=ADV-AjAXHdc

## Aplikasi dan Demo

### Face Recognition
- face_recognition library examples
  https://github.com/ageitgey/face_recognition/tree/master/examples

### OCR
- PaddleOCR Demo
  https://huggingface.co/spaces/PaddlePaddle/PaddleOCR

- Tesseract Online Demo
  https://tesseract.projectnaptha.com/

## Referensi Tambahan Indonesia

### Jurnal
- Jurnal Informatika (JI) - ITB
- Jurnal Teknologi Informasi dan Ilmu Komputer (JTIIK) - UB

### Repository Kode
- GitHub Indonesia OpenCV Community
  https://github.com/nicholausdy/face-recognition-indonesia

---

## Catatan Penggunaan

1. **Prioritas Baca**: Mulai dari buku Szeliski Chapter 6, kemudian paper klasik (Viola-Jones, FaceNet), lalu implementasi praktis

2. **Untuk Tugas**: Gunakan OpenCV face module atau face_recognition library untuk implementasi face recognition

3. **Untuk Research**: Pelajari paper terbaru (ArcFace, RetinaFace) dan benchmark di dataset standar

4. **Untuk Aplikasi**: Gunakan library siap pakai seperti face_recognition atau InsightFace untuk production

5. **OCR**: Mulai dengan Tesseract untuk dokumen sederhana, gunakan PaddleOCR atau EasyOCR untuk scene text
