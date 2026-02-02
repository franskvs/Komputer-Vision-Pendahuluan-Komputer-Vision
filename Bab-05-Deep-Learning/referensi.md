# Referensi Bab 5: Deep Learning untuk Computer Vision

## 📚 Buku Utama

### Deep Learning Fundamentals
1. **Deep Learning** - Goodfellow, Bengio, Courville (2016)
   - https://www.deeplearningbook.org/
   - Buku referensi standar untuk deep learning
   - Teori matematika yang mendalam

2. **Neural Networks and Deep Learning** - Michael Nielsen
   - http://neuralnetworksanddeeplearning.com/
   - Online book, gratis
   - Penjelasan intuitif dengan visualisasi

3. **Dive into Deep Learning** - Zhang et al.
   - https://d2l.ai/
   - Interactive book dengan kode
   - Tersedia dalam PyTorch dan TensorFlow

### Computer Vision Specific
4. **Deep Learning for Computer Vision** - Rajalingappaa Shanmugamani
   - Fokus pada aplikasi CV dengan deep learning

5. **Programming Computer Vision with Python** - Jan Erik Solem
   - http://programmingcomputervision.com/

---

## 🎓 Kursus Online

### Fundamental Courses
1. **CS231n: Convolutional Neural Networks for Visual Recognition**
   - Stanford University
   - https://cs231n.stanford.edu/
   - Video: https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv
   - Course notes sangat komprehensif

2. **Deep Learning Specialization** - Andrew Ng (Coursera)
   - https://www.coursera.org/specializations/deep-learning
   - 5 courses covering fundamentals to applications

3. **Fast.ai Practical Deep Learning for Coders**
   - https://course.fast.ai/
   - Top-down approach, sangat praktis
   - Gratis dan highly recommended

4. **MIT 6.S191: Introduction to Deep Learning**
   - http://introtodeeplearning.com/
   - Video dan slides tersedia gratis

### Advanced Courses
5. **CS229: Machine Learning** - Stanford
   - https://cs229.stanford.edu/
   - Mathematical foundations

6. **NYU Deep Learning** - Yann LeCun & Alfredo Canziani
   - https://atcold.github.io/pytorch-Deep-Learning/

---

## 📄 Paper Penting (Must Read)

### Foundational Papers

1. **ImageNet Classification with Deep CNNs (AlexNet)**
   - Krizhevsky, Sutskever, Hinton (2012)
   - https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks
   - Breakthrough yang memulai era deep learning di CV

2. **Very Deep Convolutional Networks (VGGNet)**
   - Simonyan & Zisserman (2014)
   - https://arxiv.org/abs/1409.1556
   - Menunjukkan pentingnya depth

3. **Deep Residual Learning (ResNet)**
   - He et al. (2015)
   - https://arxiv.org/abs/1512.03385
   - Skip connections untuk very deep networks

4. **Going Deeper with Convolutions (GoogLeNet/Inception)**
   - Szegedy et al. (2014)
   - https://arxiv.org/abs/1409.4842
   - Inception modules untuk efficiency

5. **Batch Normalization**
   - Ioffe & Szegedy (2015)
   - https://arxiv.org/abs/1502.03167
   - Teknik yang memungkinkan training lebih cepat

6. **Dropout: A Simple Way to Prevent Overfitting**
   - Srivastava et al. (2014)
   - https://jmlr.org/papers/v15/srivastava14a.html

### Modern Architectures

7. **EfficientNet: Rethinking Model Scaling**
   - Tan & Le (2019)
   - https://arxiv.org/abs/1905.11946
   - Compound scaling method

8. **An Image is Worth 16x16 Words: ViT**
   - Dosovitskiy et al. (2020)
   - https://arxiv.org/abs/2010.11929
   - Transformers untuk image recognition

9. **MobileNets: Efficient CNNs for Mobile Vision**
   - Howard et al. (2017)
   - https://arxiv.org/abs/1704.04861
   - Depthwise separable convolutions

### Object Detection

10. **Rich Feature Hierarchies (R-CNN)**
    - Girshick et al. (2014)
    - https://arxiv.org/abs/1311.2524

11. **You Only Look Once (YOLO)**
    - Redmon et al. (2015)
    - https://arxiv.org/abs/1506.02640

12. **Faster R-CNN**
    - Ren et al. (2015)
    - https://arxiv.org/abs/1506.01497

### Semantic Segmentation

13. **Fully Convolutional Networks (FCN)**
    - Long, Shelhamer, Darrell (2015)
    - https://arxiv.org/abs/1411.4038

14. **U-Net: Convolutional Networks for Biomedical Image Segmentation**
    - Ronneberger et al. (2015)
    - https://arxiv.org/abs/1505.04597

15. **DeepLab: Semantic Image Segmentation**
    - Chen et al. (2016)
    - https://arxiv.org/abs/1606.00915

---

## 🔧 Framework dan Library

### Deep Learning Frameworks

1. **PyTorch**
   - https://pytorch.org/
   - Documentation: https://pytorch.org/docs/stable/index.html
   - Tutorials: https://pytorch.org/tutorials/
   - Dominan di research

2. **TensorFlow / Keras**
   - https://www.tensorflow.org/
   - Keras: https://keras.io/
   - Dominan di production

3. **JAX**
   - https://github.com/google/jax
   - High-performance ML research

### Model Zoo dan Pretrained Models

4. **torchvision.models**
   - https://pytorch.org/vision/stable/models.html
   - ResNet, VGG, Inception, EfficientNet, etc.

5. **timm (PyTorch Image Models)**
   - https://github.com/rwightman/pytorch-image-models
   - 700+ pretrained models
   - State-of-the-art implementations

6. **Hugging Face Transformers**
   - https://huggingface.co/models
   - Vision Transformers dan multimodal models

### Visualization Tools

7. **TensorBoard**
   - https://www.tensorflow.org/tensorboard
   - Training visualization

8. **Weights & Biases (wandb)**
   - https://wandb.ai/
   - Experiment tracking

9. **Netron**
   - https://netron.app/
   - Model architecture visualization

---

## 📊 Dataset Penting

### Image Classification
1. **ImageNet (ILSVRC)**
   - https://image-net.org/
   - 14M images, 1000 classes
   - Benchmark standar

2. **CIFAR-10/100**
   - https://www.cs.toronto.edu/~kriz/cifar.html
   - Small images untuk quick experiments

3. **Fashion-MNIST**
   - https://github.com/zalandoresearch/fashion-mnist
   - Alternative to MNIST

4. **MNIST**
   - http://yann.lecun.com/exdb/mnist/
   - Classic handwritten digits

### Object Detection
5. **COCO (Common Objects in Context)**
   - https://cocodataset.org/
   - Detection, segmentation, keypoints

6. **Pascal VOC**
   - http://host.robots.ox.ac.uk/pascal/VOC/
   - Classic detection benchmark

### Semantic Segmentation
7. **ADE20K**
   - https://groups.csail.mit.edu/vision/datasets/ADE20K/
   - Scene parsing

8. **Cityscapes**
   - https://www.cityscapes-dataset.com/
   - Urban scene understanding

---

## 🛠️ Tools Praktis

### Training & Optimization
1. **PyTorch Lightning**
   - https://www.pytorchlightning.ai/
   - Simplified training loops

2. **Albumentations**
   - https://albumentations.ai/
   - Fast image augmentation

3. **NVIDIA DALI**
   - https://developer.nvidia.com/dali
   - GPU-accelerated data loading

### Model Interpretation
4. **Captum** (PyTorch)
   - https://captum.ai/
   - Model interpretability

5. **tf-explain** (TensorFlow)
   - https://github.com/sicara/tf-explain
   - Grad-CAM dan lainnya

6. **SHAP**
   - https://github.com/slundberg/shap
   - Explainable AI

### Deployment
7. **ONNX**
   - https://onnx.ai/
   - Model interoperability

8. **TensorRT**
   - https://developer.nvidia.com/tensorrt
   - NVIDIA inference optimization

9. **OpenVINO**
   - https://docs.openvino.ai/
   - Intel inference optimization

---

## 📝 Blog dan Tutorial

1. **Distill.pub**
   - https://distill.pub/
   - High-quality ML explanations dengan visualisasi interaktif

2. **Towards Data Science**
   - https://towardsdatascience.com/
   - Medium publication untuk DS/ML

3. **Papers with Code**
   - https://paperswithcode.com/
   - Papers dengan implementasi kode
   - State-of-the-art benchmarks

4. **PyTorch Blog**
   - https://pytorch.org/blog/
   - Updates dan tutorials

5. **The Gradient**
   - https://thegradient.pub/
   - In-depth ML articles

---

## 🎥 Video Resources

### YouTube Channels
1. **3Blue1Brown** - Neural Networks series
   - https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi
   - Visual explanations yang excellent

2. **Two Minute Papers**
   - https://www.youtube.com/c/K%C3%A1rolyZsolnai
   - Summaries of latest research

3. **Yannic Kilcher**
   - https://www.youtube.com/c/YannicKilcher
   - Paper explanations

4. **Computerphile**
   - Neural network dan CV explanations

### Conference Talks
5. **NeurIPS, ICML, CVPR** conference videos
   - Cutting-edge research presentations

---

## 🔬 Research Repositories

1. **Papers with Code**
   - https://paperswithcode.com/area/computer-vision
   - State-of-the-art methods dengan kode

2. **GitHub Topics**
   - https://github.com/topics/deep-learning
   - https://github.com/topics/computer-vision

3. **Awesome Deep Learning**
   - https://github.com/ChristosChristofidis/awesome-deep-learning

4. **Awesome Computer Vision**
   - https://github.com/jbhuang0604/awesome-computer-vision

---

## 💡 Tips Belajar Deep Learning

### Untuk Pemula
1. Mulai dengan course praktis (Fast.ai)
2. Implementasi dari scratch untuk memahami backprop
3. Gunakan pretrained models sebelum training from scratch
4. Eksperimen dengan dataset kecil dulu

### Untuk Intermediate
1. Baca paper foundational (ResNet, VGG, etc.)
2. Implementasi arsitektur dari paper
3. Pahami berbagai teknik regularisasi
4. Coba berbagai augmentation strategies

### Untuk Advanced
1. Follow latest research di ArXiv
2. Reproduksi paper results
3. Contribute ke open source projects
4. Publish findings atau blog posts

---

## 📌 Quick Reference

### Formula Penting

**Output Size Konvolusi:**
$$O = \frac{W - K + 2P}{S} + 1$$

**Cross-Entropy Loss:**
$$L = -\sum_{i} y_i \log(\hat{y}_i)$$

**Backpropagation (Chain Rule):**
$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} \cdot \frac{\partial z}{\partial w}$$

**Batch Normalization:**
$$\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}$$

---

*Terakhir diperbarui: 2024*
