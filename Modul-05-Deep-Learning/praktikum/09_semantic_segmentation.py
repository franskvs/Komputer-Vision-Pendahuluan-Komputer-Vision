"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 09 - SEMANTIC SEGMENTATION
# Assignment - set nilai ke variabel
=============================================================================
Program ini mendemonstrasikan konsep dan implementasi semantic segmentation
menggunakan berbagai model dan teknik.

Konsep yang dipelajari:
1. Dasar semantic segmentation
2. Arsitektur FCN (Fully Convolutional Networks)
3. DeepLabV3 dengan atrous convolution
4. U-Net architecture
5. Visualisasi dan evaluasi segmentation

Kebutuhan:
# Assignment - set nilai ke variabel
- torch >= 2.0.0
# Assignment - set nilai ke variabel
- torchvision >= 0.15.0
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy
- matplotlib

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
# Assignment - set nilai ke variabel
=============================================================================
"""

# Import library/module untuk digunakan
import cv2
# Import library/module untuk digunakan
import numpy as np
# Import library/module untuk digunakan
import matplotlib.pyplot as plt
# Import library/module untuk digunakan
import time

# Check apakah PyTorch tersedia
TORCH_AVAILABLE = False
# Blok try-except untuk error handling
try:
    # Import library/module untuk digunakan
    import torch
    # Import library/module untuk digunakan
    import torchvision
    # Import library/module untuk digunakan
    from torchvision import transforms
    # Import library/module untuk digunakan
    from torchvision.models.segmentation import (
        deeplabv3_resnet50, deeplabv3_resnet101,
        fcn_resnet50, fcn_resnet101
    )
    # Assignment - set nilai ke variabel
    TORCH_AVAILABLE = True
    print("[INFO] PyTorch dan Torchvision tersedia")
# Tangkap exception jika ada error di blok try
except ImportError:
    print("[WARNING] PyTorch tidak tersedia - menggunakan simulasi")


# ============================================================================
# DEFINISI CLASS DAN WARNA SEGMENTASI
# ============================================================================

# Pascal VOC classes (21 classes)
VOC_CLASSES = [
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 
    'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 
    'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 
    'train', 'tvmonitor'
]

# Color palette untuk visualisasi
VOC_COLORMAP = np.array([
    [0, 0, 0],       # background - black
    [128, 0, 0],     # aeroplane - maroon
    [0, 128, 0],     # bicycle - green
    [128, 128, 0],   # bird - olive
    [0, 0, 128],     # boat - navy
    [128, 0, 128],   # bottle - purple
    [0, 128, 128],   # bus - teal
    [128, 128, 128], # car - gray
    [64, 0, 0],      # cat - dark maroon
    [192, 0, 0],     # chair - red
    [64, 128, 0],    # cow - dark green
    [192, 128, 0],   # diningtable - gold
    [64, 0, 128],    # dog - dark purple
    [192, 0, 128],   # horse - pink
    [64, 128, 128],  # motorbike - dark teal
    [192, 128, 128], # person - light pink
    [0, 64, 0],      # pottedplant - very dark green
    [128, 64, 0],    # sheep - brown
    [0, 192, 0],     # sofa - lime
    [128, 192, 0],   # train - yellow-green
    [0, 64, 128]     # tvmonitor - dark blue
# Assignment - set nilai ke variabel
], dtype=np.uint8)


# Definisi function dengan nama dan parameter
def demo_segmentation_concept():
    """
    Demonstrasi konsep dasar semantic segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("KONSEP DASAR SEMANTIC SEGMENTATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [DEFINISI]
    ─────────────────────────────────────────────────────────────────────
    Semantic Segmentation adalah task untuk mengklasifikasikan SETIAP
    # Definisi class untuk membuat object
    PIXEL dalam gambar ke dalam class tertentu.
    
    Input:  Image (H × W × 3)
    # Definisi class untuk membuat object
    Output: Segmentation Map (H × W) dengan nilai class untuk tiap pixel
    
    
    [PERBEDAAN DENGAN TASK LAIN]
    ─────────────────────────────────────────────────────────────────────
    
    +------------------+------------------+-------------------------+
    | Task             | Output           | Granularity             |
    +------------------+------------------+-------------------------+
    | Classification   | Single label     | Per-image               |
    | Object Detection | Bounding boxes   | Per-object (rectangle)  |
    | Sem. Segmentation| Pixel-wise labels| Per-pixel               |
    | Inst. Segmentation| Pixel + instance| Per-pixel + per-object  |
    +------------------+------------------+-------------------------+
    
    
    [ARSITEKTUR UMUM]
    ─────────────────────────────────────────────────────────────────────
    
    Input Image      Encoder (Backbone)      Decoder          Output
    ┌─────────┐     ┌────────────────┐     ┌────────────┐    ┌──────┐
    │ H × W   │ --> │  Downsample    │ --> │  Upsample  │ -->│ H × W│
    │ × 3     │     │  + Features    │     │  + Refine  │    │ × C  │
    └─────────┘     └────────────────┘     └────────────┘    └──────┘
    
    - Encoder: Mengekstrak fitur (ResNet, VGG, dll)
    - Decoder: Mengembalikan resolusi ke ukuran asli
    
    
    [METRICS]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    1. Pixel Accuracy = (Correct Pixels) / (Total Pixels)
    
    2. Mean IoU (Intersection over Union):
       # Definisi class untuk membuat object
       IoU per class = TP / (TP + FP + FN)
       # Assignment - set nilai ke variabel
       mIoU = Average IoU across all classes
    
    3. Dice Coefficient:
       # Assignment - set nilai ke variabel
       Dice = 2 × |A ∩ B| / (|A| + |B|)
    """)
    
    # Visualisasi konsep
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    
    # Original image simulation
    img = np.ones((200, 300, 3), dtype=np.uint8) * 135  # Sky background
    # Ground
    img[150:, :] = [34, 139, 34]
    # Person
    cv2.rectangle(img, (100, 80), (150, 180), [192, 128, 128], -1)
    # Car
    cv2.rectangle(img, (180, 120), (280, 175), [128, 128, 128], -1)
    
    # Konversi format warna (BGR ke RGB, dll)
    axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    # Segmentation mask
    mask = np.zeros((200, 300), dtype=np.uint8)
    # Definisi class untuk membuat object
    mask[150:, :] = 1  # Ground as class 1
    # Definisi class untuk membuat object
    mask[80:180, 100:150] = 15  # Person as class 15
    # Definisi class untuk membuat object
    mask[120:175, 180:280] = 7  # Car as class 7
    
    # Color mask
    color_mask = VOC_COLORMAP[mask]
    axes[1].imshow(color_mask)
    axes[1].set_title('Segmentation Mask')
    axes[1].axis('off')
    
    # Overlay
    overlay = cv2.addWeighted(img, 0.5, color_mask.astype(np.uint8), 0.5, 0)
    # Konversi format warna (BGR ke RGB, dll)
    axes[2].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[2].set_title('Overlay')
    axes[2].axis('off')
    
    # Class distribution
    unique, counts = np.unique(mask, return_counts=True)
    # Assignment - set nilai ke variabel
    class_names = ['background', 'ground', 'person', 'car']
    axes[3].bar(class_names, counts)
    axes[3].set_title('Pixel Distribution')
    axes[3].set_ylabel('Pixel Count')
    
    # Atur spacing otomatis antar subplot
    plt.tight_layout()
    # Simpan figure ke file gambar
    plt.savefig('segmentation_concept.png', dpi=150, bbox_inches='tight')
    # Tampilkan semua figure yang telah dibuat
    plt.show()
    
    print("\n[INFO] Visualisasi disimpan: segmentation_concept.png")


# Definisi function dengan nama dan parameter
def demo_fcn_architecture():
    """
    Demonstrasi arsitektur FCN (Fully Convolutional Networks).
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("FCN (FULLY CONVOLUTIONAL NETWORKS)")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [FCN OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    FCN (Long et al., 2015) adalah arsitektur pertama yang menggantikan
    fully connected layers dengan convolutional layers untuk segmentation.
    
    
    [ARSITEKTUR FCN-32s, FCN-16s, FCN-8s]
    ─────────────────────────────────────────────────────────────────────
    
                        VGG-16 Backbone
    Input  →  Conv1  →  Conv2  →  Conv3  →  Conv4  →  Conv5  →  FC→Conv
    (224)     (224)     (112)     (56)      (28)      (14)       (7)
                ↓         ↓         ↓
    
    # Assignment - set nilai ke variabel
    FCN-32s: Output = 32× upsample from pool5
    # Assignment - set nilai ke variabel
    FCN-16s: Output = 16× upsample from pool4 + pool5
    # Assignment - set nilai ke variabel
    FCN-8s:  Output = 8× upsample from pool3 + pool4 + pool5
    
    
    [SKIP CONNECTIONS]
    ─────────────────────────────────────────────────────────────────────
    
    Pool3 (1/8)  ─────────────────────────────────┐
                                                  │
    Pool4 (1/16) ──────────────┐                  │
                               │                  │
    Pool5 (1/32) → Conv → 2× → + → 2× → + → 8× → Output
    
    Skip connections membantu menggabungkan informasi:
    - Low-level: detail spasial
    - High-level: semantic information
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if TORCH_AVAILABLE:
        print("\n[INFO] Loading FCN-ResNet50...")
        
        # Load pretrained model
        model = fcn_resnet50(pretrained=True)
        model.eval()
        
        # Model info
        total_params = sum(p.numel() for p in model.parameters())
        print(f"[INFO] Total parameters: {total_params:,}")
        
        # Generate sample input
        sample_input = torch.randn(1, 3, 520, 520)
        
        with torch.no_grad():
            # Assignment - set nilai ke variabel
            start = time.time()
            # Assignment - set nilai ke variabel
            output = model(sample_input)
            # Assignment - set nilai ke variabel
            inference_time = time.time() - start
        
        print(f"\n[INFO] Input shape: {sample_input.shape}")
        print(f"[INFO] Output shape: {output['out'].shape}")
        print(f"[INFO] Number of classes: {output['out'].shape[1]}")
        print(f"[INFO] Inference time: {inference_time*1000:.2f} ms")
        
        # Test with actual image
        print("\n[INFO] Creating test image...")
        
        # Create synthetic image
        test_img = np.zeros((520, 520, 3), dtype=np.uint8)
        # Assignment - set nilai ke variabel
        test_img[:, :] = [135, 206, 235]  # Sky blue
        # Assignment - set nilai ke variabel
        test_img[350:, :] = [34, 139, 34]  # Green ground
        # Gambar persegi panjang pada gambar
        cv2.rectangle(test_img, (100, 250), (180, 380), [192, 128, 128], -1)  # Person
        # Gambar persegi panjang pada gambar
        cv2.rectangle(test_img, (300, 280), (450, 370), [128, 128, 128], -1)  # Car
        
        # Preprocess
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            # Assignment - set nilai ke variabel
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                # Assignment - set nilai ke variabel
                                std=[0.229, 0.224, 0.225]),
        ])
        
        # Assignment - set nilai ke variabel
        input_tensor = preprocess(test_img).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            # Assignment - set nilai ke variabel
            output = model(input_tensor)['out']
        
        # Get predictions
        pred = output.argmax(1).squeeze().cpu().numpy()
        
        # Visualize
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        
        # Konversi format warna (BGR ke RGB, dll)
        axes[0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Input Image')
        axes[0].axis('off')
        
        # Assignment - set nilai ke variabel
        axes[1].imshow(pred, cmap='tab20')
        axes[1].set_title('FCN Prediction')
        axes[1].axis('off')
        
        # Color map
        color_pred = VOC_COLORMAP[pred % 21]
        axes[2].imshow(color_pred)
        axes[2].set_title('Colored Segmentation')
        axes[2].axis('off')
        
        # Atur spacing otomatis antar subplot
        plt.tight_layout()
        # Simpan figure ke file gambar
        plt.savefig('fcn_result.png', dpi=150, bbox_inches='tight')
        # Tampilkan semua figure yang telah dibuat
        plt.show()
        
    else:
        # Simulation
        print("\n[SIMULATION MODE]")
        print("FCN architecture components:")
        print("  - Backbone: ResNet-50 (pretrained on ImageNet)")
        print("  - Head: FCN head with skip connections")
        print("  - Output: 21 classes (Pascal VOC)")


# Definisi function dengan nama dan parameter
def demo_deeplabv3():
    """
    Demonstrasi arsitektur DeepLabV3.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DEEPLABV3 ARCHITECTURE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [DEEPLABV3 OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    DeepLabV3 (Chen et al., 2017) menggunakan Atrous Convolution dan
    Atrous Spatial Pyramid Pooling (ASPP) untuk multi-scale segmentation.
    
    
    [ATROUS (DILATED) CONVOLUTION]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    Standard Convolution (3×3):      Atrous Convolution (rate=2):
    
    ┌───┬───┬───┐                    ┌───┬───┬───┬───┬───┐
    │ × │ × │ × │                    │ × │   │ × │   │ × │
    ├───┼───┼───┤                    ├───┼───┼───┼───┼───┤
    │ × │ × │ × │                    │   │   │   │   │   │
    ├───┼───┼───┤                    ├───┼───┼───┼───┼───┤
    │ × │ × │ × │                    │ × │   │ × │   │ × │
    └───┴───┴───┘                    ├───┼───┼───┼───┼───┤
                                     │   │   │   │   │   │
    Receptive field: 3×3             ├───┼───┼───┼───┼───┤
                                     │ × │   │ × │   │ × │
                                     └───┴───┴───┴───┴───┘
                                     
                                     Receptive field: 5×5
    
    Benefits:
    - Larger receptive field without more parameters
    - No loss of resolution
    
    
    [ATROUS SPATIAL PYRAMID POOLING (ASPP)]
    ─────────────────────────────────────────────────────────────────────
    
    Input Feature Map
           │
    ┌──────┼──────┬──────────┬──────────┬──────────┐
    │      │      │          │          │          │
    ▼      ▼      ▼          ▼          ▼          ▼
    1×1   3×3    3×3        3×3       Global      
    # Assignment - set nilai ke variabel
    Conv  rate=6 rate=12    rate=18    Pooling
    │      │      │          │          │
    └──────┴──────┴──────────┴──────────┘
                   │
              Concatenate
                   │
              1×1 Conv
                   │
                Output
    
    Multi-scale feature extraction tanpa perlu image pyramid.
    
    
    [DEEPLABV3+ ENCODER-DECODER]
    ─────────────────────────────────────────────────────────────────────
    
    Encoder:                    Decoder:
    
    Input → Backbone → ASPP → Low-level features
                         │              │
                         └──────┬───────┘
                                │
                            Combine
                                │
                           3×3 Conv
                                │
                            4× Upsample
                                │
                             Output
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if TORCH_AVAILABLE:
        print("\n[INFO] Loading DeepLabV3-ResNet101...")
        
        # Load pretrained model
        model = deeplabv3_resnet101(pretrained=True)
        model.eval()
        
        # Model info
        total_params = sum(p.numel() for p in model.parameters())
        print(f"[INFO] Total parameters: {total_params:,}")
        
        # Generate sample image
        test_img = np.zeros((520, 520, 3), dtype=np.uint8)
        # Assignment - set nilai ke variabel
        test_img[:, :] = [135, 206, 235]  # Sky
        # Assignment - set nilai ke variabel
        test_img[350:, :] = [34, 139, 34]  # Ground
        
        # Add person and car
        cv2.rectangle(test_img, (100, 250), (180, 380), [192, 128, 128], -1)
        # Gambar persegi panjang pada gambar
        cv2.rectangle(test_img, (300, 280), (450, 370), [128, 128, 128], -1)
        
        # Preprocess
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            # Assignment - set nilai ke variabel
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                # Assignment - set nilai ke variabel
                                std=[0.229, 0.224, 0.225]),
        ])
        
        # Assignment - set nilai ke variabel
        input_tensor = preprocess(test_img).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            # Assignment - set nilai ke variabel
            start = time.time()
            # Assignment - set nilai ke variabel
            output = model(input_tensor)['out']
            # Assignment - set nilai ke variabel
            inference_time = time.time() - start
        
        print(f"[INFO] Inference time: {inference_time*1000:.2f} ms")
        
        # Get predictions
        pred = output.argmax(1).squeeze().cpu().numpy()
        
        # Confidence map
        probs = torch.softmax(output, dim=1)
        # Assignment - set nilai ke variabel
        confidence = probs.max(dim=1)[0].squeeze().cpu().numpy()
        
        # Visualize
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        
        # Konversi format warna (BGR ke RGB, dll)
        axes[0, 0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Input Image')
        axes[0, 0].axis('off')
        
        # Assignment - set nilai ke variabel
        color_pred = VOC_COLORMAP[pred % 21]
        axes[0, 1].imshow(color_pred)
        axes[0, 1].set_title('DeepLabV3 Segmentation')
        axes[0, 1].axis('off')
        
        # Assignment - set nilai ke variabel
        axes[1, 0].imshow(confidence, cmap='hot')
        axes[1, 0].set_title('Confidence Map')
        axes[1, 0].axis('off')
        
        # Overlay
        overlay = cv2.addWeighted(test_img, 0.5, color_pred.astype(np.uint8), 0.5, 0)
        # Konversi format warna (BGR ke RGB, dll)
        axes[1, 1].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Overlay')
        axes[1, 1].axis('off')
        
        # Atur spacing otomatis antar subplot
        plt.tight_layout()
        # Simpan figure ke file gambar
        plt.savefig('deeplabv3_result.png', dpi=150, bbox_inches='tight')
        # Tampilkan semua figure yang telah dibuat
        plt.show()
        
    else:
        print("\n[SIMULATION MODE] DeepLabV3 architecture demonstrated.")


# Definisi function dengan nama dan parameter
def demo_unet_architecture():
    """
    Demonstrasi arsitektur U-Net.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("U-NET ARCHITECTURE")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [U-NET OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    U-Net (Ronneberger et al., 2015) dirancang untuk biomedical image
    segmentation dengan encoder-decoder architecture dan skip connections.
    
    
    [ARSITEKTUR U-NET]
    ─────────────────────────────────────────────────────────────────────
    
    Contracting Path (Encoder)        Expanding Path (Decoder)
    
         ┌─────────────────────────────────────────────┐
    64 ch│  ■■■■ ────────────────────────────► ■■■■   │ 64 ch
         │  │                                    ↑     │
         │  ▼                                    │     │
    128ch│  ■■ ──────────────────────────────► ■■    │ 128ch
         │  │                                    ↑     │
         │  ▼                                    │     │
    256ch│  ■ ────────────────────────────────► ■     │ 256ch
         │  │                                    ↑     │
         │  ▼                                    │     │
    512ch│  ▪ ──────────────────────────────────▪     │ 512ch
         │  │                                    ↑     │
         │  ▼                                    │     │
    1024 │  ▪ ────────────────────────────────────►    │
         │                Bottleneck                   │
         └─────────────────────────────────────────────┘
    
    
    [KOMPONEN UTAMA]
    ─────────────────────────────────────────────────────────────────────
    
    1. CONTRACTING PATH (Encoder):
       - Repeated: Conv 3×3 → ReLU → Conv 3×3 → ReLU → MaxPool 2×2
       - Double channels at each step
       - Captures context
    
    2. EXPANDING PATH (Decoder):
       - Repeated: UpConv 2×2 → Concat skip → Conv 3×3 → ReLU → Conv 3×3 → ReLU
       - Halve channels at each step
       - Enables precise localization
    
    3. SKIP CONNECTIONS:
       - Copy and crop feature maps from encoder to decoder
       - Combine high-resolution features with upsampled output
       - Preserve spatial details
    
    4. FINAL LAYER:
       - 1×1 convolution to map features to desired number of classes
    """)
    
    # Simple U-Net implementation
    if TORCH_AVAILABLE:
        # Import library/module untuk digunakan
        import torch.nn as nn
        
        # Definisi class untuk membuat object
        class SimpleUNet(nn.Module):
            """
            # Iterasi/loop melalui elemen dalam koleksi
            Simplified U-Net implementation for demonstration.
            """
            # Definisi function dengan nama dan parameter
            def __init__(self, in_channels=3, out_channels=2, features=[64, 128, 256, 512]):
                super(SimpleUNet, self).__init__()
                
                # Assignment - set nilai ke variabel
                self.encoder = nn.ModuleList()
                # Assignment - set nilai ke variabel
                self.decoder = nn.ModuleList()
                # Assignment - set nilai ke variabel
                self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
                
                # Encoder
                for feature in features:
                    self.encoder.append(self._double_conv(in_channels, feature))
                    # Assignment - set nilai ke variabel
                    in_channels = feature
                
                # Bottleneck
                self.bottleneck = self._double_conv(features[-1], features[-1]*2)
                
                # Decoder
                for feature in reversed(features):
                    self.decoder.append(
                        # Assignment - set nilai ke variabel
                        nn.ConvTranspose2d(feature*2, feature, kernel_size=2, stride=2)
                    )
                    self.decoder.append(self._double_conv(feature*2, feature))
                
                # Final conv
                self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)
            
            # Definisi function dengan nama dan parameter
            def _double_conv(self, in_channels, out_channels):
                # Return value dari function
                return nn.Sequential(
                    # Assignment - set nilai ke variabel
                    nn.Conv2d(in_channels, out_channels, 3, padding=1),
                    nn.BatchNorm2d(out_channels),
                    # Assignment - set nilai ke variabel
                    nn.ReLU(inplace=True),
                    # Assignment - set nilai ke variabel
                    nn.Conv2d(out_channels, out_channels, 3, padding=1),
                    nn.BatchNorm2d(out_channels),
                    # Assignment - set nilai ke variabel
                    nn.ReLU(inplace=True),
                )
            
            # Definisi function dengan nama dan parameter
            def forward(self, x):
                # Assignment - set nilai ke variabel
                skip_connections = []
                
                # Encoder
                for encoder in self.encoder:
                    # Assignment - set nilai ke variabel
                    x = encoder(x)
                    skip_connections.append(x)
                    # Assignment - set nilai ke variabel
                    x = self.pool(x)
                
                # Assignment - set nilai ke variabel
                x = self.bottleneck(x)
                # Assignment - set nilai ke variabel
                skip_connections = skip_connections[::-1]
                
                # Decoder
                for idx in range(0, len(self.decoder), 2):
                    # Assignment - set nilai ke variabel
                    x = self.decoder[idx](x)
                    # Assignment - set nilai ke variabel
                    skip = skip_connections[idx//2]
                    
                    # Handle size mismatch
                    if x.shape != skip.shape:
                        # Assignment - set nilai ke variabel
                        x = torch.nn.functional.interpolate(x, size=skip.shape[2:])
                    
                    # Assignment - set nilai ke variabel
                    x = torch.cat((skip, x), dim=1)
                    # Assignment - set nilai ke variabel
                    x = self.decoder[idx+1](x)
                
                # Return value dari function
                return self.final_conv(x)
        
        print("\n[INFO] Creating U-Net model...")
        # Assignment - set nilai ke variabel
        model = SimpleUNet(in_channels=3, out_channels=2)
        
        # Count parameters
        total_params = sum(p.numel() for p in model.parameters())
        print(f"[INFO] Total parameters: {total_params:,}")
        
        # Test forward pass
        sample_input = torch.randn(1, 3, 256, 256)
        with torch.no_grad():
            # Assignment - set nilai ke variabel
            output = model(sample_input)
        
        print(f"[INFO] Input shape: {sample_input.shape}")
        print(f"[INFO] Output shape: {output.shape}")
        
        # Visualize U-Net output with synthetic data
        test_img = np.zeros((256, 256, 3), dtype=np.uint8)
        # Assignment - set nilai ke variabel
        test_img[:, :] = [200, 200, 200]  # Gray background
        
        # Draw a simple cell-like structure
        cv2.circle(test_img, (128, 128), 60, (100, 100, 150), -1)
        # Gambar lingkaran pada gambar
        cv2.circle(test_img, (128, 128), 30, (50, 50, 100), -1)
        
        # Preprocess
        input_tensor = torch.from_numpy(test_img).permute(2, 0, 1).float() / 255.0
        # Assignment - set nilai ke variabel
        input_tensor = input_tensor.unsqueeze(0)
        
        # Inference
        model.eval()
        with torch.no_grad():
            # Assignment - set nilai ke variabel
            output = model(input_tensor)
        
        # Assignment - set nilai ke variabel
        pred = output.argmax(1).squeeze().cpu().numpy()
        
        # Visualize
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        
        axes[0].imshow(test_img)
        axes[0].set_title('Input Image')
        axes[0].axis('off')
        
        # Assignment - set nilai ke variabel
        axes[1].imshow(pred, cmap='gray')
        axes[1].set_title('U-Net Prediction (untrained)')
        axes[1].axis('off')
        
        # Overlay
        overlay = test_img.copy()
        # Assignment - set nilai ke variabel
        overlay[pred == 1] = [255, 0, 0]
        axes[2].imshow(overlay)
        axes[2].set_title('Overlay')
        axes[2].axis('off')
        
        # Atur spacing otomatis antar subplot
        plt.tight_layout()
        # Simpan figure ke file gambar
        plt.savefig('unet_demo.png', dpi=150, bbox_inches='tight')
        # Tampilkan semua figure yang telah dibuat
        plt.show()
        
    else:
        print("\n[SIMULATION MODE] U-Net architecture explained.")


# Definisi function dengan nama dan parameter
def demo_segmentation_metrics():
    """
    Demonstrasi metrics untuk evaluasi semantic segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("SEGMENTATION METRICS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [EVALUATION METRICS]
    ─────────────────────────────────────────────────────────────────────
    
    1. PIXEL ACCURACY
       ────────────────
       # Assignment - set nilai ke variabel
       Pixel Accuracy = Σ(correct pixels) / Σ(total pixels)
       
       Pros: Simple, intuitive
       Cons: Biased towards dominant classes
    
    2. MEAN PIXEL ACCURACY
       ─────────────────────
       # Definisi class untuk membuat object
       Per-class accuracy, then average:
       # Assignment - set nilai ke variabel
       mPA = (1/K) × Σ(TP_k / (TP_k + FN_k))
    
    3. INTERSECTION OVER UNION (IoU / Jaccard Index)
       ──────────────────────────────────────────────
       # Assignment - set nilai ke variabel
       IoU = Area of Overlap / Area of Union
       # Assignment - set nilai ke variabel
       IoU = TP / (TP + FP + FN)
       
       Ranges from 0 to 1 (higher is better)
    
    4. MEAN IoU (mIoU)
       ─────────────────
       # Assignment - set nilai ke variabel
       mIoU = (1/K) × Σ(IoU_k)
       
       # Iterasi/loop melalui elemen dalam koleksi
       Standard metric for semantic segmentation benchmarks
    
    5. DICE COEFFICIENT (F1 Score)
       ────────────────────────────
       # Assignment - set nilai ke variabel
       Dice = 2 × |A ∩ B| / (|A| + |B|)
       # Assignment - set nilai ke variabel
       Dice = 2 × TP / (2×TP + FP + FN)
       
       Popular in medical image segmentation
    
    6. FREQUENCY WEIGHTED IoU
       ───────────────────────
       # Assignment - set nilai ke variabel
       FWIoU = Σ(freq_k × IoU_k) / Σ(freq_k)
       
       # Definisi class untuk membuat object
       Weights IoU by class frequency
    """)
    
    # Definisi function dengan nama dan parameter
    def compute_iou(pred, target, num_classes):
        """Compute IoU for each class."""
        # Assignment - set nilai ke variabel
        ious = []
        # Iterasi/loop melalui elemen dalam koleksi
        for cls in range(num_classes):
            # Assignment - set nilai ke variabel
            pred_mask = (pred == cls)
            # Assignment - set nilai ke variabel
            target_mask = (target == cls)
            
            # Assignment - set nilai ke variabel
            intersection = np.logical_and(pred_mask, target_mask).sum()
            # Assignment - set nilai ke variabel
            union = np.logical_or(pred_mask, target_mask).sum()
            
            # Conditional statement - eksekusi jika kondisi True
            if union == 0:
                # Assignment - set nilai ke variabel
                iou = float('nan')
            else:
                # Assignment - set nilai ke variabel
                iou = intersection / union
            
            ious.append(iou)
        
        # Return value dari function
        return ious
    
    # Definisi function dengan nama dan parameter
    def compute_dice(pred, target, num_classes):
        """Compute Dice coefficient for each class."""
        # Assignment - set nilai ke variabel
        dices = []
        # Iterasi/loop melalui elemen dalam koleksi
        for cls in range(num_classes):
            # Assignment - set nilai ke variabel
            pred_mask = (pred == cls)
            # Assignment - set nilai ke variabel
            target_mask = (target == cls)
            
            # Assignment - set nilai ke variabel
            intersection = np.logical_and(pred_mask, target_mask).sum()
            # Assignment - set nilai ke variabel
            total = pred_mask.sum() + target_mask.sum()
            
            # Conditional statement - eksekusi jika kondisi True
            if total == 0:
                # Assignment - set nilai ke variabel
                dice = float('nan')
            else:
                # Assignment - set nilai ke variabel
                dice = 2 * intersection / total
            
            dices.append(dice)
        
        # Return value dari function
        return dices
    
    # Create example prediction and ground truth
    np.random.seed(42)
    
    # Ground truth
    gt = np.zeros((100, 100), dtype=np.int32)
    # Assignment - set nilai ke variabel
    gt[20:80, 20:80] = 1  # Class 1: square
    # Assignment - set nilai ke variabel
    gt[40:60, 40:60] = 2  # Class 2: inner square
    
    # Prediction (with some errors)
    pred = gt.copy()
    # Add noise
    noise_mask = np.random.random((100, 100)) < 0.1
    # Generate random integer dalam range tertentu
    pred[noise_mask] = np.random.randint(0, 3, noise_mask.sum())
    # Shift prediction slightly
    pred = np.roll(pred, 2, axis=0)
    # Assignment - set nilai ke variabel
    pred = np.roll(pred, 2, axis=1)
    
    # Compute metrics
    num_classes = 3
    # Assignment - set nilai ke variabel
    ious = compute_iou(pred, gt, num_classes)
    # Assignment - set nilai ke variabel
    dices = compute_dice(pred, gt, num_classes)
    
    # Pixel accuracy
    pixel_acc = (pred == gt).sum() / pred.size
    
    print("\n[METRICS COMPUTATION EXAMPLE]")
    print(f"Image size: {gt.shape}")
    print(f"Number of classes: {num_classes}")
    print()
    
    # Definisi class untuk membuat object
    print("Per-class IoU:")
    # Iterasi/loop melalui elemen dalam koleksi
    for i, iou in enumerate(ious):
        print(f"  Class {i}: {iou:.4f}")
    print(f"  mIoU: {np.nanmean(ious):.4f}")
    print()
    
    # Definisi class untuk membuat object
    print("Per-class Dice:")
    # Iterasi/loop melalui elemen dalam koleksi
    for i, dice in enumerate(dices):
        print(f"  Class {i}: {dice:.4f}")
    print(f"  mDice: {np.nanmean(dices):.4f}")
    print()
    
    print(f"Pixel Accuracy: {pixel_acc:.4f}")
    
    # Visualize
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    
    # Assignment - set nilai ke variabel
    axes[0].imshow(gt, cmap='tab10', vmin=0, vmax=2)
    axes[0].set_title('Ground Truth')
    axes[0].axis('off')
    
    # Assignment - set nilai ke variabel
    axes[1].imshow(pred, cmap='tab10', vmin=0, vmax=2)
    axes[1].set_title('Prediction')
    axes[1].axis('off')
    
    # Difference
    diff = (pred != gt).astype(np.uint8)
    # Assignment - set nilai ke variabel
    axes[2].imshow(diff, cmap='Reds')
    # Assignment - set nilai ke variabel
    axes[2].set_title('Errors (white = error)')
    axes[2].axis('off')
    
    # Metrics bar chart
    classes = ['Background', 'Class 1', 'Class 2']
    # Assignment - set nilai ke variabel
    x = np.arange(len(classes))
    # Assignment - set nilai ke variabel
    width = 0.35
    
    # Assignment - set nilai ke variabel
    axes[3].bar(x - width/2, ious, width, label='IoU', color='blue', alpha=0.7)
    # Assignment - set nilai ke variabel
    axes[3].bar(x + width/2, dices, width, label='Dice', color='orange', alpha=0.7)
    axes[3].set_xticks(x)
    axes[3].set_xticklabels(classes)
    axes[3].set_ylabel('Score')
    axes[3].set_title('Metrics per Class')
    axes[3].legend()
    axes[3].set_ylim(0, 1)
    
    # Atur spacing otomatis antar subplot
    plt.tight_layout()
    # Simpan figure ke file gambar
    plt.savefig('segmentation_metrics.png', dpi=150, bbox_inches='tight')
    # Tampilkan semua figure yang telah dibuat
    plt.show()


# Definisi function dengan nama dan parameter
def demo_model_comparison():
    """
    Perbandingan berbagai model segmentation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("SEGMENTATION MODEL COMPARISON")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [MODEL COMPARISON]
    ─────────────────────────────────────────────────────────────────────
    
    ┌────────────────┬──────────┬─────────┬───────────┬─────────────────┐
    │ Model          │ Backbone │ Params  │ mIoU (VOC)│ Use Case        │
    ├────────────────┼──────────┼─────────┼───────────┼─────────────────┤
    │ FCN-8s         │ VGG-16   │ 134.5M  │ 62.2%     │ General purpose │
    │ FCN-ResNet50   │ ResNet50 │ 35.3M   │ 63.7%     │ Balanced        │
    │ DeepLabV3      │ ResNet101│ 58.6M   │ 77.2%     │ High accuracy   │
    │ DeepLabV3+     │ Xception │ 54.7M   │ 79.6%     │ SOTA accuracy   │
    │ U-Net          │ Custom   │ 31.0M   │ -         │ Medical imaging │
    │ PSPNet         │ ResNet101│ 65.7M   │ 82.6%     │ Scene parsing   │
    │ HRNet          │ Custom   │ 65.9M   │ 81.5%     │ High-res output │
    │ SegFormer      │ Transformer│48.0M  │ 82.2%     │ Modern approach │
    └────────────────┴──────────┴─────────┴───────────┴─────────────────┘
    
    * mIoU measured on Pascal VOC 2012 validation set
    
    
    [SELECTION GUIDELINES]
    ─────────────────────────────────────────────────────────────────────
    
    REAL-TIME / MOBILE:
    → BiSeNet, ENet, ICNet, ESPNet
    # Iterasi/loop melalui elemen dalam koleksi
    → Trade accuracy for speed
    
    HIGH ACCURACY:
    → DeepLabV3+, PSPNet, HRNet
    # Iterasi/loop melalui elemen dalam koleksi
    → Use for offline processing
    
    MEDICAL IMAGING:
    → U-Net, nnU-Net, V-Net
    # Iterasi/loop melalui elemen dalam koleksi
    → Designed for small datasets
    
    SCENE UNDERSTANDING:
    → PSPNet, DeepLabV3
    # Iterasi/loop melalui elemen dalam koleksi
    → Good for outdoor scenes
    
    EDGE DETECTION + SEGMENTATION:
    → HRNet
    → Maintains high resolution
    
    TRANSFORMER-BASED:
    → SegFormer, SETR, Mask2Former
    → Latest SOTA approaches
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if TORCH_AVAILABLE:
        print("\n[INFO] Benchmarking available models...")
        
        # Assignment - set nilai ke variabel
        models_info = []
        
        # FCN ResNet50
        print("  Loading FCN-ResNet50...")
        # Assignment - set nilai ke variabel
        model = fcn_resnet50(pretrained=True)
        # Iterasi/loop melalui elemen dalam koleksi
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('FCN-ResNet50', params))
        del model
        
        # FCN ResNet101
        print("  Loading FCN-ResNet101...")
        # Assignment - set nilai ke variabel
        model = fcn_resnet101(pretrained=True)
        # Iterasi/loop melalui elemen dalam koleksi
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('FCN-ResNet101', params))
        del model
        
        # DeepLabV3 ResNet50
        print("  Loading DeepLabV3-ResNet50...")
        # Assignment - set nilai ke variabel
        model = deeplabv3_resnet50(pretrained=True)
        # Iterasi/loop melalui elemen dalam koleksi
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('DeepLabV3-ResNet50', params))
        del model
        
        # DeepLabV3 ResNet101
        print("  Loading DeepLabV3-ResNet101...")
        # Assignment - set nilai ke variabel
        model = deeplabv3_resnet101(pretrained=True)
        # Iterasi/loop melalui elemen dalam koleksi
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('DeepLabV3-ResNet101', params))
        del model
        
        print("\n[INFO] Model Parameter Comparison:")
        # Iterasi/loop melalui elemen dalam koleksi
        for name, params in models_info:
            print(f"  {name}: {params/1e6:.2f}M parameters")
        
        # Visualize comparison
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Iterasi/loop melalui elemen dalam koleksi
        names = [m[0] for m in models_info]
        # Iterasi/loop melalui elemen dalam koleksi
        params = [m[1]/1e6 for m in models_info]
        
        # Assignment - set nilai ke variabel
        bars = ax.barh(names, params, color=['#3498db', '#2980b9', '#e74c3c', '#c0392b'])
        ax.set_xlabel('Parameters (Millions)')
        ax.set_title('Segmentation Model Parameters')
        
        # Iterasi/loop melalui elemen dalam koleksi
        for bar, p in zip(bars, params):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   # Assignment - set nilai ke variabel
                   f'{p:.1f}M', va='center')
        
        # Atur spacing otomatis antar subplot
        plt.tight_layout()
        # Simpan figure ke file gambar
        plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
        # Tampilkan semua figure yang telah dibuat
        plt.show()


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM SEMANTIC SEGMENTATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Konsep Dasar Semantic Segmentation")
        print("2. FCN (Fully Convolutional Networks)")
        print("3. DeepLabV3 Architecture")
        print("4. U-Net Architecture")
        print("5. Segmentation Metrics")
        print("6. Model Comparison")
        print("7. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-7): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_segmentation_concept()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_fcn_architecture()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_deeplabv3()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_unet_architecture()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_segmentation_metrics()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_model_comparison()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '7':
            demo_segmentation_concept()
            demo_fcn_architecture()
            demo_deeplabv3()
            demo_unet_architecture()
            demo_segmentation_metrics()
            demo_model_comparison()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
