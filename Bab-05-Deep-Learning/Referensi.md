# Referensi Bab 05 - Deep Learning untuk Computer Vision

## 1. Referensi Utama

### Buku Teks
1. **Szeliski, R. (2022).** *Computer Vision: Algorithms and Applications, 2nd Edition.* Springer.
   - Chapter 5: Deep Learning
   - Online: https://szeliski.org/Book/

2. **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep Learning.* MIT Press.
   - Free online: https://www.deeplearningbook.org/
   - Chapter 6: Deep Feedforward Networks
   - Chapter 9: Convolutional Networks

3. **Chollet, F. (2021).** *Deep Learning with Python, 2nd Edition.* Manning Publications.
   - Practical Keras/TensorFlow guide

4. **Stevens, E., Antiga, L., & Viehmann, T. (2020).** *Deep Learning with PyTorch.* Manning Publications.
   - PyTorch fundamentals and applications

## 2. Paper Klasik CNN

### Arsitektur Dasar
1. **LeCun, Y., et al. (1998).** "Gradient-Based Learning Applied to Document Recognition."
   - Paper LeNet original
   - http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf

2. **Krizhevsky, A., Sutskever, I., & Hinton, G. (2012).** "ImageNet Classification with Deep Convolutional Neural Networks."
   - Paper AlexNet
   - Breakthrough paper untuk deep learning
   - https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks

3. **Simonyan, K. & Zisserman, A. (2015).** "Very Deep Convolutional Networks for Large-Scale Image Recognition."
   - Paper VGGNet
   - https://arxiv.org/abs/1409.1556

4. **He, K., et al. (2016).** "Deep Residual Learning for Image Recognition."
   - Paper ResNet (skip connections)
   - https://arxiv.org/abs/1512.03385

5. **Tan, M. & Le, Q.V. (2019).** "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks."
   - Paper EfficientNet
   - https://arxiv.org/abs/1905.11946

## 3. Object Detection Papers

### YOLO Family
1. **Redmon, J., et al. (2016).** "You Only Look Once: Unified, Real-Time Object Detection."
   - Paper YOLO v1
   - https://arxiv.org/abs/1506.02640

2. **Redmon, J. & Farhadi, A. (2017).** "YOLO9000: Better, Faster, Stronger."
   - Paper YOLO v2
   - https://arxiv.org/abs/1612.08242

3. **Redmon, J. & Farhadi, A. (2018).** "YOLOv3: An Incremental Improvement."
   - Paper YOLO v3
   - https://arxiv.org/abs/1804.02767

4. **Bochkovskiy, A., Wang, C.-Y., & Liao, H.-Y. M. (2020).** "YOLOv4: Optimal Speed and Accuracy of Object Detection."
   - Paper YOLO v4
   - https://arxiv.org/abs/2004.10934

5. **Ultralytics (2023).** "YOLOv8 Documentation"
   - Official documentation
   - https://docs.ultralytics.com/

### R-CNN Family
1. **Girshick, R., et al. (2014).** "Rich feature hierarchies for accurate object detection and semantic segmentation."
   - Paper R-CNN
   - https://arxiv.org/abs/1311.2524

2. **Girshick, R. (2015).** "Fast R-CNN."
   - https://arxiv.org/abs/1504.08083

3. **Ren, S., et al. (2015).** "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks."
   - https://arxiv.org/abs/1506.01497

## 4. Semantic Segmentation Papers

1. **Long, J., Shelhamer, E., & Darrell, T. (2015).** "Fully Convolutional Networks for Semantic Segmentation."
   - Paper FCN
   - https://arxiv.org/abs/1411.4038

2. **Ronneberger, O., Fischer, P., & Brox, T. (2015).** "U-Net: Convolutional Networks for Biomedical Image Segmentation."
   - Paper U-Net
   - https://arxiv.org/abs/1505.04597

3. **Chen, L.-C., et al. (2017).** "Rethinking Atrous Convolution for Semantic Image Segmentation."
   - Paper DeepLabV3
   - https://arxiv.org/abs/1706.05587

4. **Chen, L.-C., et al. (2018).** "Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation."
   - Paper DeepLabV3+
   - https://arxiv.org/abs/1802.02611

## 5. Instance Segmentation Papers

1. **He, K., et al. (2017).** "Mask R-CNN."
   - Foundational instance segmentation
   - https://arxiv.org/abs/1703.06870

2. **Kirillov, A., et al. (2019).** "Panoptic Segmentation."
   - Combines semantic and instance segmentation
   - https://arxiv.org/abs/1801.00868

## 6. Transfer Learning Papers

1. **Yosinski, J., et al. (2014).** "How transferable are features in deep neural networks?"
   - Fundamental transfer learning study
   - https://arxiv.org/abs/1411.1792

2. **Howard, A.G., et al. (2017).** "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications."
   - Paper MobileNet
   - https://arxiv.org/abs/1704.04861

## 7. Data Augmentation Papers

1. **Shorten, C. & Khoshgoftaar, T.M. (2019).** "A survey on Image Data Augmentation for Deep Learning."
   - Comprehensive augmentation survey
   - https://journalofbigdata.springeropen.com/articles/10.1186/s40537-019-0197-0

2. **Zhang, H., et al. (2018).** "mixup: Beyond Empirical Risk Minimization."
   - Paper Mixup
   - https://arxiv.org/abs/1710.09412

3. **Yun, S., et al. (2019).** "CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features."
   - Paper CutMix
   - https://arxiv.org/abs/1905.04899

## 8. Model Deployment & Optimization

### ONNX
1. **ONNX Official Documentation**
   - https://onnx.ai/
   - https://github.com/onnx/onnx

2. **ONNX Runtime**
   - https://onnxruntime.ai/
   - https://github.com/microsoft/onnxruntime

### TensorRT
1. **NVIDIA TensorRT Documentation**
   - https://developer.nvidia.com/tensorrt

### OpenVINO
1. **Intel OpenVINO Documentation**
   - https://docs.openvino.ai/

## 9. Framework Documentation

### PyTorch
- Official Documentation: https://pytorch.org/docs/stable/index.html
- Tutorials: https://pytorch.org/tutorials/
- PyTorch Vision: https://pytorch.org/vision/stable/index.html

### TensorFlow/Keras
- Official Documentation: https://www.tensorflow.org/api_docs
- Keras Guide: https://keras.io/guides/
- TensorFlow Hub: https://tfhub.dev/

### OpenCV DNN
- Official Tutorial: https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html
- DNN Module: https://docs.opencv.org/4.x/d6/d0f/group__dnn.html

## 10. Dataset dan Model Zoo

### Datasets
1. **ImageNet**: https://www.image-net.org/
2. **COCO**: https://cocodataset.org/
3. **Pascal VOC**: http://host.robots.ox.ac.uk/pascal/VOC/
4. **CIFAR-10/100**: https://www.cs.toronto.edu/~kriz/cifar.html
5. **Open Images**: https://storage.googleapis.com/openimages/web/index.html

### Pre-trained Models
1. **PyTorch Model Zoo**: https://pytorch.org/vision/stable/models.html
2. **TensorFlow Model Garden**: https://github.com/tensorflow/models
3. **Hugging Face**: https://huggingface.co/models
4. **Ultralytics Model Zoo**: https://docs.ultralytics.com/models/

## 11. Tutorial Online

### Kursus Online
1. **CS231n: Convolutional Neural Networks for Visual Recognition** (Stanford)
   - https://cs231n.stanford.edu/
   - Video: https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv

2. **Deep Learning Specialization** (Coursera - Andrew Ng)
   - https://www.coursera.org/specializations/deep-learning

3. **Fast.ai Practical Deep Learning**
   - https://course.fast.ai/

### YouTube Channels
1. **3Blue1Brown** - Neural networks visualization
   - https://www.youtube.com/c/3blue1brown

2. **Sentdex** - Python and ML tutorials
   - https://www.youtube.com/c/sentdex

3. **StatQuest** - Statistical concepts explained
   - https://www.youtube.com/c/joshstarmer

## 12. Tools dan Libraries

### Visualization
1. **Netron** - Model visualizer
   - https://netron.app/
   
2. **TensorBoard**
   - https://www.tensorflow.org/tensorboard

3. **Weights & Biases**
   - https://wandb.ai/

### Labeling Tools
1. **LabelImg** - Image annotation
   - https://github.com/heartexlabs/labelImg

2. **CVAT** - Computer Vision Annotation Tool
   - https://cvat.ai/

3. **Labelme** - Polygon annotation
   - https://github.com/wkentaro/labelme

## 13. Komunitas dan Forum

1. **PyTorch Forums**: https://discuss.pytorch.org/
2. **TensorFlow Forums**: https://www.tensorflow.org/community/forums
3. **Stack Overflow**: https://stackoverflow.com/questions/tagged/deep-learning
4. **Reddit r/MachineLearning**: https://www.reddit.com/r/MachineLearning/
5. **Papers With Code**: https://paperswithcode.com/

## 14. Best Practices

### Coding Style
1. **PEP 8 Style Guide**: https://peps.python.org/pep-0008/
2. **PyTorch Best Practices**: https://pytorch.org/docs/stable/notes/best_practices.html

### Model Training
1. **A Recipe for Training Neural Networks** (Andrej Karpathy)
   - http://karpathy.github.io/2019/04/25/recipe/

2. **Deep Learning Tuning Playbook** (Google)
   - https://github.com/google-research/tuning_playbook

---

## Catatan Penting

1. **Selalu cite sumber** saat menggunakan pretrained models atau code dari paper
2. **Check lisensi** sebelum menggunakan model untuk aplikasi komersial
3. **Update dependencies** secara berkala untuk keamanan
4. **Benchmark** dengan dataset yang relevan dengan use case Anda
5. **Document** preprocessing dan postprocessing steps

---

*Referensi terakhir diperbarui: 2024*
