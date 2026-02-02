# Referensi Bab 6: Recognition (Pengenalan)

## 📚 Buku Referensi

### Core Textbooks
1. **Computer Vision: Algorithms and Applications, 2nd Ed** - Richard Szeliski (2022)
   - https://szeliski.org/Book/
   - Chapter 6: Recognition

2. **Deep Learning** - Goodfellow, Bengio, Courville
   - https://www.deeplearningbook.org/
   - Chapter 9: Convolutional Networks

3. **Pattern Recognition and Machine Learning** - Christopher Bishop
   - Klasik untuk machine learning fundamentals

### Specialized Books
4. **Object Detection in 20 Years: A Survey** - Zou et al.
   - Comprehensive survey object detection

5. **Image Classification using Deep Neural Networks** - Multiple Authors
   - Focus pada CNN classification

---

## 📄 Paper Penting

### Image Classification

1. **ImageNet Classification with Deep CNNs (AlexNet)**
   - Krizhevsky, Sutskever, Hinton (2012)
   - https://papers.nips.cc/paper/4824
   - Breakthrough deep learning untuk CV

2. **Very Deep Convolutional Networks (VGG)**
   - Simonyan & Zisserman (2014)
   - https://arxiv.org/abs/1409.1556
   - Depth matters

3. **Deep Residual Learning for Image Recognition (ResNet)**
   - He et al. (2015)
   - https://arxiv.org/abs/1512.03385
   - Skip connections

4. **Densely Connected Convolutional Networks (DenseNet)**
   - Huang et al. (2016)
   - https://arxiv.org/abs/1608.06993

5. **EfficientNet: Rethinking Model Scaling**
   - Tan & Le (2019)
   - https://arxiv.org/abs/1905.11946
   - Compound scaling

6. **An Image is Worth 16x16 Words: ViT**
   - Dosovitskiy et al. (2020)
   - https://arxiv.org/abs/2010.11929
   - Vision Transformer

### Object Detection

7. **Rich Feature Hierarchies (R-CNN)**
   - Girshick et al. (2014)
   - https://arxiv.org/abs/1311.2524
   - Region-based CNN

8. **Fast R-CNN**
   - Girshick (2015)
   - https://arxiv.org/abs/1504.08083
   - RoI pooling

9. **Faster R-CNN: Towards Real-Time Object Detection**
   - Ren et al. (2015)
   - https://arxiv.org/abs/1506.01497
   - Region Proposal Network

10. **You Only Look Once: Unified, Real-Time Object Detection (YOLO)**
    - Redmon et al. (2015)
    - https://arxiv.org/abs/1506.02640
    - One-stage detector

11. **SSD: Single Shot MultiBox Detector**
    - Liu et al. (2016)
    - https://arxiv.org/abs/1512.02325
    - Multi-scale detection

12. **Feature Pyramid Networks for Object Detection (FPN)**
    - Lin et al. (2016)
    - https://arxiv.org/abs/1612.03144
    - Multi-scale feature pyramids

13. **Focal Loss for Dense Object Detection (RetinaNet)**
    - Lin et al. (2017)
    - https://arxiv.org/abs/1708.02002
    - Class imbalance

14. **DETR: End-to-End Object Detection with Transformers**
    - Carion et al. (2020)
    - https://arxiv.org/abs/2005.12872
    - Transformer-based detection

### Semantic Segmentation

15. **Fully Convolutional Networks (FCN)**
    - Long, Shelhamer, Darrell (2014)
    - https://arxiv.org/abs/1411.4038
    - Foundational work

16. **Semantic Image Segmentation with Deep CNNs and Fully Connected CRFs (DeepLab)**
    - Chen et al. (2014)
    - https://arxiv.org/abs/1412.7062

17. **U-Net: Convolutional Networks for Biomedical Image Segmentation**
    - Ronneberger et al. (2015)
    - https://arxiv.org/abs/1505.04597
    - Encoder-decoder with skip connections

18. **DeepLab v3+: Encoder-Decoder with Atrous Separable Convolution**
    - Chen et al. (2018)
    - https://arxiv.org/abs/1802.02611

19. **Pyramid Scene Parsing Network (PSPNet)**
    - Zhao et al. (2016)
    - https://arxiv.org/abs/1612.01105
    - Pyramid pooling module

### Instance Segmentation

20. **Mask R-CNN**
    - He et al. (2017)
    - https://arxiv.org/abs/1703.06870
    - Instance segmentation benchmark

21. **YOLACT: Real-time Instance Segmentation**
    - Bolya et al. (2019)
    - https://arxiv.org/abs/1904.02689
    - Fast instance segmentation

### Bag of Visual Words

22. **Video Google: A Text Retrieval Approach to Object Matching**
    - Sivic & Zisserman (2003)
    - Original BoVW paper

23. **Beyond Bags of Features: Spatial Pyramid Matching**
    - Lazebnik, Schmid, Ponce (2006)
    - https://hal.inria.fr/inria-00548585
    - Spatial pyramid

---

## 🎓 Kursus Online

### Deep Learning untuk Recognition
1. **CS231n: CNNs for Visual Recognition** - Stanford
   - https://cs231n.stanford.edu/
   - Comprehensive course

2. **Deep Learning Specialization** - Andrew Ng (Coursera)
   - https://www.coursera.org/specializations/deep-learning
   - Course 4: CNNs

3. **Fast.ai Practical Deep Learning**
   - https://course.fast.ai/
   - Hands-on approach

### Object Detection Specific
4. **Object Detection Course** - Stanford CS231A
   - Detection fundamentals

5. **YOLO Tutorial Series** - YouTube
   - Practical implementation guides

---

## 🔧 Framework dan Library

### Deep Learning
1. **PyTorch**
   - https://pytorch.org/
   - torchvision untuk vision tasks

2. **TensorFlow / Keras**
   - https://www.tensorflow.org/
   - tf.keras.applications

3. **MMDetection** (OpenMMLab)
   - https://github.com/open-mmlab/mmdetection
   - Comprehensive detection toolbox

4. **Detectron2** (Facebook AI)
   - https://github.com/facebookresearch/detectron2
   - State-of-the-art detection/segmentation

### Model Zoo
5. **torchvision.models**
   - Classification: ResNet, VGG, etc.
   - Detection: Faster R-CNN, RetinaNet
   - Segmentation: DeepLabV3, FCN

6. **timm (PyTorch Image Models)**
   - https://github.com/rwightman/pytorch-image-models
   - 700+ pretrained models

7. **Hugging Face Transformers**
   - https://huggingface.co/
   - Vision Transformers

### YOLO Implementations
8. **Ultralytics YOLOv8**
   - https://github.com/ultralytics/ultralytics
   - Latest YOLO version

9. **YOLOv5**
   - https://github.com/ultralytics/yolov5
   - Popular implementation

### Segmentation
10. **Segmentation Models PyTorch**
    - https://github.com/qubvel/segmentation_models.pytorch
    - Various architectures

---

## 📊 Dataset Benchmark

### Image Classification
1. **ImageNet (ILSVRC)**
   - https://image-net.org/
   - 14M images, 1000 classes

2. **CIFAR-10/100**
   - https://www.cs.toronto.edu/~kriz/cifar.html
   - Small images, quick experiments

3. **Caltech-101/256**
   - Object recognition benchmark

4. **Places365**
   - Scene recognition

### Object Detection
5. **MS COCO**
   - https://cocodataset.org/
   - 80 object categories
   - Detection, segmentation, keypoints

6. **Pascal VOC**
   - http://host.robots.ox.ac.uk/pascal/VOC/
   - Classic benchmark

7. **Open Images**
   - https://storage.googleapis.com/openimages/web/index.html
   - 9M images, 600 classes

### Semantic Segmentation
8. **ADE20K**
   - Scene parsing (150 classes)

9. **Cityscapes**
   - Urban scene understanding

10. **Pascal VOC Segmentation**
    - 21 classes

### Instance Segmentation
11. **COCO Instance**
    - Standard benchmark

12. **LVIS**
    - Long-tail instance segmentation

---

## 🛠️ Tools Praktis

### Annotation Tools
1. **LabelImg**
   - https://github.com/tzutalin/labelImg
   - Bounding box annotation

2. **LabelMe**
   - http://labelme.csail.mit.edu/
   - Polygon annotation

3. **CVAT**
   - https://github.com/openvinotoolkit/cvat
   - Comprehensive annotation

4. **Roboflow**
   - https://roboflow.com/
   - Dataset management + augmentation

### Evaluation
5. **pycocotools**
   - COCO evaluation metrics
   - mAP calculation

6. **scikit-learn metrics**
   - Classification metrics

### Visualization
7. **Grad-CAM**
   - Model interpretability

8. **FiftyOne**
   - https://voxel51.com/fiftyone/
   - Dataset visualization

---

## 📝 Blog dan Tutorial

1. **Papers with Code - Object Detection**
   - https://paperswithcode.com/task/object-detection
   - State-of-the-art benchmarks

2. **Towards Data Science**
   - Detection and segmentation tutorials

3. **Medium - Analytics Vidhya**
   - Practical implementations

4. **PyTorch Official Tutorials**
   - https://pytorch.org/tutorials/
   - Detection and segmentation examples

5. **Learn OpenCV**
   - https://learnopencv.com/
   - Practical CV tutorials

---

## 🎥 Video Resources

1. **Two Minute Papers**
   - Latest research summaries

2. **Yannic Kilcher**
   - Paper explanations

3. **AI Coffee Break with Letitia**
   - Detection/segmentation papers

4. **Weights & Biases**
   - MLOps tutorials

---

## 📌 Quick Reference

### IoU Calculation
```python
def iou(box1, box2):
    # box format: [x1, y1, x2, y2]
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    intersection = max(0, x2-x1) * max(0, y2-y1)
    area1 = (box1[2]-box1[0]) * (box1[3]-box1[1])
    area2 = (box2[2]-box2[0]) * (box2[3]-box2[1])
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0
```

### mAP Formula
$$mAP = \frac{1}{|Classes|} \sum_{c \in Classes} AP_c$$

$$AP = \int_0^1 p(r) dr \approx \sum_k (r_{k+1} - r_k) \cdot p_{interp}(r_{k+1})$$

### Segmentation Metrics

**Pixel Accuracy:**
$$PA = \frac{\sum_i n_{ii}}{\sum_i t_i}$$

**Mean IoU:**
$$mIoU = \frac{1}{k} \sum_i \frac{n_{ii}}{t_i + \sum_j n_{ji} - n_{ii}}$$

**Dice Score:**
$$Dice = \frac{2|A \cap B|}{|A| + |B|}$$

---

## 🔗 Links Penting

- **Papers with Code**: https://paperswithcode.com/
- **COCO Evaluation**: https://cocodataset.org/#detection-eval
- **Pascal VOC Devkit**: http://host.robots.ox.ac.uk/pascal/VOC/
- **ImageNet Challenge**: https://image-net.org/challenges/LSVRC/

---

*Terakhir diperbarui: 2024*
