# PPT Prompt 1 — Modul 05: Deep Learning untuk Computer Vision

Buat presentasi PowerPoint profesional untuk **Modul 05: Deep Learning untuk Computer Vision**. 

## Sumber Referensi
Gunakan konten lengkap dari:
- `Materi.md` - Teori dan konsep fundamental
- `Jobsheet.md` - Praktikum dan hands-on exercises
- `Project.md` - DeepVision project specifications
- `Referensi.md` - Papers dan resources
- `praktikum/*.py` - Code examples untuk demonstrasi

## Spesifikasi Presentasi
- **Jumlah Slide**: 35–45 slide (termasuk cover dan referensi)
- **Bahasa**: Bahasa Indonesia dengan istilah teknis dalam English
- **Durasi**: Disesuaikan untuk 2-3 sesi perkuliahan (@ 90-120 menit)
- **Audience**: Mahasiswa tingkat menengah dengan background Python dan CV dasar

## Struktur Slide Detail

### 1. Opening (3 slides)
- **Slide 1**: Cover slide
  - Judul: "Deep Learning untuk Computer Vision"
  - Subtitle: "Modul 05 - Praktikum Computer Vision"
  - Logo institusi dan informasi dosen/asisten
- **Slide 2**: Agenda & Timeline
  - Overview 6 pertemuan
  - Topik per pertemuan
  - Deliverables (project, video, quiz)
- **Slide 3**: Learning Outcomes
  - 6-8 poin learning objectives yang spesifik dan measurable
  - Link ke real-world applications

### 2. Motivasi dan Konteks (4-5 slides)
- **Slide 4**: Evolution of Computer Vision
  - Timeline: Traditional CV → Deep Learning revolution
  - ImageNet moment (AlexNet 2012)
  - Performance comparison graph
- **Slide 5**: Traditional CV vs Deep Learning
  - Side-by-side comparison table
  - Hand-crafted features vs learned features
  - Visual diagram pipeline comparison
- **Slide 6**: Why Deep Learning Dominates CV?
  - Automatic feature learning
  - State-of-the-art performance
  - End-to-end training
  - Transfer learning capabilities
- **Slide 7**: Real-World Applications Today
  - Face recognition (smartphone unlock)
  - Autonomous vehicles
  - Medical imaging diagnosis
  - Quality control in manufacturing
  - Augmented reality
  - (Include images/icons untuk setiap application)

### 3. CNN Fundamentals (8-10 slides)
- **Slide 8**: What is a Neural Network?
  - Biological neuron vs artificial neuron
  - Forward propagation basics
  - Activation functions visualization
- **Slide 9**: From NN to CNN
  - Why fully connected doesn't work for images
  - Parameter explosion problem
  - Local connectivity concept
- **Slide 10**: Convolutional Layer Explained
  - Filter/kernel concept dengan animasi atau diagram
  - Convolution operation step-by-step
  - Feature maps visualization
  - Formula: Output size = (Input - Kernel + 2×Padding) / Stride + 1
- **Slide 11**: Convolutional Layer Parameters
  - Kernel size (3×3, 5×5, 7×7)
  - Stride effects
  - Padding types (same, valid)
  - Number of filters
  - Visual examples untuk setiap parameter
- **Slide 12**: What Do CNN Filters Learn?
  - Layer 1: edges, colors
  - Layer 2: textures, patterns
  - Layer 3+: parts, objects
  - Visualization examples dari real networks
- **Slide 13**: Pooling Layers
  - Max pooling vs average pooling
  - Visual example dengan numbers
  - Purpose: dimensionality reduction, translation invariance
  - Typical: 2×2 with stride 2
- **Slide 14**: Activation Functions
  - ReLU, Leaky ReLU, Sigmoid, Tanh
  - Graphs untuk setiap function
  - When to use which?
  - Dying ReLU problem
- **Slide 15**: Fully Connected Layers
  - Role dalam CNN architecture
  - Flattening operation
  - Classification head
- **Slide 16**: Complete CNN Architecture Example
  - End-to-end flow diagram
  - Example: LeNet atau simple custom architecture
  - Show dimensions di setiap layer
  - Total parameters calculation
- **Slide 17**: Modern CNN Design Principles
  - Deeper is better (with skip connections)
  - 3×3 convolutions (VGG insight)
  - Batch normalization
  - Bottleneck designs

### 4. Training Deep Networks (6-7 slides)
- **Slide 18**: Training Pipeline Overview
  - Data → Model → Loss → Optimizer → Update → Repeat
  - Flowchart visualization
- **Slide 19**: Loss Functions
  - Cross-entropy untuk classification
  - MSE untuk regression
  - Custom losses untuk specific tasks
  - Formula dan intuition
- **Slide 20**: Optimization Algorithms
  - SGD vs Adam vs RMSprop
  - Learning rate importance
  - Learning rate scheduling
  - Comparison table
- **Slide 21**: Regularization Techniques
  - Dropout visualization
  - Weight decay (L2 regularization)
  - Data augmentation examples
  - Early stopping
- **Slide 22**: Data Augmentation
  - Horizontal flip, rotation, crop
  - Color jitter, brightness
  - Before/after examples
  - Code snippet
- **Slide 23**: Training Best Practices
  - Batch size selection
  - Train/val/test split (80/10/10 atau 70/15/15)
  - Monitoring training curves
  - Overfitting vs underfitting diagnosis
- **Slide 24**: Common Training Problems
  - Vanishing/exploding gradients
  - Overfitting
  - Slow convergence
  - Solutions untuk setiap problem

### 5. Popular CNN Architectures (5-6 slides)
- **Slide 25**: LeNet-5 (1998)
  - Historical significance
  - Architecture diagram
  - MNIST results
- **Slide 26**: AlexNet (2012) - The Game Changer
  - ImageNet breakthrough
  - Key innovations (ReLU, Dropout, GPU training)
  - Architecture overview
- **Slide 27**: VGGNet (2014)
  - Deep with 3×3 convolutions
  - Architecture variants (VGG-16, VGG-19)
  - Parameter count
- **Slide 28**: ResNet (2015) - Skip Connections
  - Residual learning concept
  - Skip connection diagram
  - Why it enables very deep networks (152 layers)
- **Slide 29**: Modern Architectures Landscape
  - Inception/GoogLeNet
  - MobileNet (efficiency)
  - EfficientNet (compound scaling)
  - Comparison table (size, accuracy, speed)
- **Slide 30**: Architecture Selection Guide
  - Decision tree atau flowchart
  - For mobile: MobileNet, EfficientNet-B0
  - For accuracy: ResNet-50, EfficientNet-B3
  - For research: ResNet-101, ViT

### 6. Transfer Learning (4-5 slides)
- **Slide 31**: What is Transfer Learning?
  - Motivation: limited data problem
  - Pre-trained on ImageNet
  - Fine-tune for custom task
  - Analogy: learning bicycle → learning motorcycle
- **Slide 32**: Transfer Learning Strategies
  - Feature extraction (freeze all, train classifier)
  - Fine-tuning (freeze early, train late layers)
  - Full training (use as initialization)
  - Decision flowchart based on dataset size
- **Slide 33**: How to Fine-Tune
  - Step-by-step process
  - Learning rate selection (10-100x smaller)
  - Gradual unfreezing
  - Code snippet example
- **Slide 34**: Transfer Learning Results
  - Before/after accuracy comparison
  - Training curves with vs without transfer learning
  - Data efficiency (10x less data needed)
- **Slide 35**: Best Practices
  - Always start with pre-trained weights
  - Use similar domain data (ImageNet for general vision)
  - Adjust batch size dan learning rate
  - Monitor validation loss

### 7. Object Detection with YOLO (5-6 slides)
- **Slide 36**: From Classification to Detection
  - Classification: "what"
  - Detection: "what" + "where"
  - Bounding box representation (x, y, w, h)
- **Slide 37**: Two-Stage vs One-Stage Detectors
  - R-CNN family (two-stage)
  - YOLO, SSD (one-stage)
  - Speed vs accuracy trade-off
  - Comparison table
- **Slide 38**: YOLO Architecture Overview
  - "You Only Look Once" concept
  - Grid-based detection
  - High-level architecture diagram
  - Real-time capability
- **Slide 39**: YOLO Evolution
  - YOLOv1 → YOLOv3 → YOLOv5 → YOLOv8
  - Performance improvements
  - mAP comparison chart
- **Slide 40**: Using YOLOv8
  - Ultralytics library
  - Model variants (n, s, m, l, x)
  - Quick start code
  - Demo results
- **Slide 41**: Detection Metrics
  - IoU (Intersection over Union)
  - Precision, Recall, F1
  - mAP (mean Average Precision)
  - Confusion matrix untuk detection

### 8. Image Segmentation (3-4 slides)
- **Slide 42**: Types of Segmentation
  - Semantic: classify each pixel
  - Instance: separate instances
  - Panoptic: combine both
  - Visual examples
- **Slide 43**: Segmentation Architectures
  - FCN (Fully Convolutional Networks)
  - U-Net (encoder-decoder with skip)
  - Mask R-CNN (instance segmentation)
  - Architecture diagrams
- **Slide 44**: Segmentation Metrics
  - IoU per class
  - Dice coefficient
  - Pixel accuracy
  - Visual examples
- **Slide 45**: Applications
  - Medical imaging
  - Autonomous driving
  - Background removal
  - Scene understanding

### 9. Praktikum dan Demo (4-5 slides)
- **Slide 46**: Praktikum Overview
  - 6 pertemuan roadmap
  - Topik per pertemuan
  - Hands-on activities
- **Slide 47**: Demo 1 - Image Classification
  - OpenCV DNN dengan pre-trained model
  - Screenshot hasil
  - Key code snippets
- **Slide 48**: Demo 2 - Training Custom CNN
  - PyTorch/Keras implementation
  - Training curves
  - Results comparison
- **Slide 49**: Demo 3 - YOLO Detection
  - Real-time detection demo
  - Multiple objects
  - Performance metrics
- **Slide 50**: Demo 4 - Model Deployment
  - ONNX export
  - OpenCV inference
  - Speed comparison

### 10. Project: DeepVision (3-4 slides)
- **Slide 51**: Project Overview
  - Smart retail product classification system
  - 3 modules: Classifier, Detector, Deployment
  - Timeline: 5 weeks
- **Slide 52**: Module 1 - Product Classifier
  - Transfer learning requirements
  - Dataset specifications
  - Expected outputs
- **Slide 53**: Module 2 - Shelf Detector
  - YOLO fine-tuning
  - Object counting
  - Real-time performance
- **Slide 54**: Module 3 - Deployment
  - ONNX export
  - OpenCV DNN integration
  - Performance benchmarking
- **Slide 55**: Grading Rubric
  - Functionality (30%)
  - Technical implementation (30%)
  - Deployment (20%)
  - Documentation (20%)

### 11. Resources dan Next Steps (3-4 slides)
- **Slide 56**: Learning Resources
  - CS231n course (Stanford)
  - Fast.ai practical deep learning
  - Papers with Code
  - PyTorch/TensorFlow tutorials
- **Slide 57**: Tools dan Libraries
  - PyTorch, TensorFlow/Keras
  - Ultralytics, MMDetection
  - Weights & Biases, TensorBoard
  - Roboflow untuk dataset management
- **Slide 58**: Industry Trends 2024-2026
  - Vision Transformers (ViT)
  - Foundation models (SAM, CLIP)
  - Efficient models (MobileViT)
  - Multimodal learning
- **Slide 59**: Q&A dan Diskusi
  - Key takeaways summary
  - Contact information
  - Office hours
- **Slide 60**: Referensi
  - Key papers cited
  - Books dan online resources
  - GitHub repositories

## Ketentuan Visual dan Desain

### Gaya Visual
- **Color Scheme**: Professional blue/grey palette
  - Primary: Dark blue (#1e3a8a)
  - Secondary: Light blue (#3b82f6)
  - Accent: Orange (#f97316) untuk highlights
- **Fonts**: 
  - Headings: Montserrat Bold
  - Body: Open Sans Regular
  - Code: Fira Code atau Consolas
- **Consistency**: Gunakan template yang sama untuk semua slides

### Visual Elements
- **Diagrams**: Gunakan draw.io atau Lucidchart style
- **Icons**: Flaticon atau Font Awesome
- **Images**: High-quality, relevant, properly cited
- **Code**: Syntax highlighted, maksimal 10-15 lines per slide
- **Charts**: Clean, labeled, color-coded
- **Animations**: Subtle, purposeful (fade in, appear)

### Text Guidelines
- **Title**: 32-36pt, bold
- **Body**: 18-24pt, regular
- **Bullet points**: Maksimal 5-6 per slide
- **Line length**: Maksimal 70-80 characters
- **Avoid**: Text walls, too many animations, low-contrast colors

## Konten yang Wajib Ada

### Technical Details
- [ ] Formula matematika yang key (convolution, loss functions)
- [ ] Architecture diagrams dengan dimensi lengkap
- [ ] Code snippets yang runnable
- [ ] Performance metrics dan benchmarks
- [ ] Visualization dari intermediate layers

### Practical Elements
- [ ] Step-by-step instructions untuk praktikum
- [ ] Common errors dan troubleshooting
- [ ] Best practices dan tips
- [ ] Real-world examples
- [ ] Links ke resources tambahan

### Pedagogical Features
- [ ] Learning checks (quiz questions)
- [ ] Discussion prompts
- [ ] Hands-on exercises
- [ ] Critical thinking questions
- [ ] Connections to prior knowledge

## Validasi Kualitas

Sebelum finalize, pastikan:
- [ ] Tidak ada typos atau grammatical errors
- [ ] Semua images ter-cite dengan proper
- [ ] Code snippets sudah di-test
- [ ] Metrics dan numbers sudah di-verify
- [ ] Flow logis dari satu slide ke slide berikutnya
- [ ] Slide tidak terlalu ramai (clutter-free)
- [ ] Accessibility: contrast ratio cukup, font size readable
- [ ] File size reasonable (<50MB untuk compatibility)

## Output Format
- **File**: `Modul_05_Deep_Learning_[Nama].pptx`
- **Backup**: Export PDF untuk backup
- **Notes**: Tambahkan speaker notes untuk context tambahan
- **Handout**: Version printable (4-6 slides per page)
