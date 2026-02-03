"""
=============================================================================
PRAKTIKUM 09 - SEMANTIC SEGMENTATION
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
- torch >= 2.0.0
- torchvision >= 0.15.0
- opencv-python >= 4.8.0
- numpy
- matplotlib

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

# Check apakah PyTorch tersedia
TORCH_AVAILABLE = False
try:
    import torch
    import torchvision
    from torchvision import transforms
    from torchvision.models.segmentation import (
        deeplabv3_resnet50, deeplabv3_resnet101,
        fcn_resnet50, fcn_resnet101
    )
    TORCH_AVAILABLE = True
    print("[INFO] PyTorch dan Torchvision tersedia")
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
], dtype=np.uint8)


def demo_segmentation_concept():
    """
    Demonstrasi konsep dasar semantic segmentation.
    """
    print("\n" + "="*70)
    print("KONSEP DASAR SEMANTIC SEGMENTATION")
    print("="*70)
    
    print("""
    [DEFINISI]
    ─────────────────────────────────────────────────────────────────────
    Semantic Segmentation adalah task untuk mengklasifikasikan SETIAP
    PIXEL dalam gambar ke dalam class tertentu.
    
    Input:  Image (H × W × 3)
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
    
    1. Pixel Accuracy = (Correct Pixels) / (Total Pixels)
    
    2. Mean IoU (Intersection over Union):
       IoU per class = TP / (TP + FP + FN)
       mIoU = Average IoU across all classes
    
    3. Dice Coefficient:
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
    
    axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    # Segmentation mask
    mask = np.zeros((200, 300), dtype=np.uint8)
    mask[150:, :] = 1  # Ground as class 1
    mask[80:180, 100:150] = 15  # Person as class 15
    mask[120:175, 180:280] = 7  # Car as class 7
    
    # Color mask
    color_mask = VOC_COLORMAP[mask]
    axes[1].imshow(color_mask)
    axes[1].set_title('Segmentation Mask')
    axes[1].axis('off')
    
    # Overlay
    overlay = cv2.addWeighted(img, 0.5, color_mask.astype(np.uint8), 0.5, 0)
    axes[2].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[2].set_title('Overlay')
    axes[2].axis('off')
    
    # Class distribution
    unique, counts = np.unique(mask, return_counts=True)
    class_names = ['background', 'ground', 'person', 'car']
    axes[3].bar(class_names, counts)
    axes[3].set_title('Pixel Distribution')
    axes[3].set_ylabel('Pixel Count')
    
    plt.tight_layout()
    plt.savefig('segmentation_concept.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\n[INFO] Visualisasi disimpan: segmentation_concept.png")


def demo_fcn_architecture():
    """
    Demonstrasi arsitektur FCN (Fully Convolutional Networks).
    """
    print("\n" + "="*70)
    print("FCN (FULLY CONVOLUTIONAL NETWORKS)")
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
    
    FCN-32s: Output = 32× upsample from pool5
    FCN-16s: Output = 16× upsample from pool4 + pool5
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
            start = time.time()
            output = model(sample_input)
            inference_time = time.time() - start
        
        print(f"\n[INFO] Input shape: {sample_input.shape}")
        print(f"[INFO] Output shape: {output['out'].shape}")
        print(f"[INFO] Number of classes: {output['out'].shape[1]}")
        print(f"[INFO] Inference time: {inference_time*1000:.2f} ms")
        
        # Test with actual image
        print("\n[INFO] Creating test image...")
        
        # Create synthetic image
        test_img = np.zeros((520, 520, 3), dtype=np.uint8)
        test_img[:, :] = [135, 206, 235]  # Sky blue
        test_img[350:, :] = [34, 139, 34]  # Green ground
        cv2.rectangle(test_img, (100, 250), (180, 380), [192, 128, 128], -1)  # Person
        cv2.rectangle(test_img, (300, 280), (450, 370), [128, 128, 128], -1)  # Car
        
        # Preprocess
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225]),
        ])
        
        input_tensor = preprocess(test_img).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            output = model(input_tensor)['out']
        
        # Get predictions
        pred = output.argmax(1).squeeze().cpu().numpy()
        
        # Visualize
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        
        axes[0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Input Image')
        axes[0].axis('off')
        
        axes[1].imshow(pred, cmap='tab20')
        axes[1].set_title('FCN Prediction')
        axes[1].axis('off')
        
        # Color map
        color_pred = VOC_COLORMAP[pred % 21]
        axes[2].imshow(color_pred)
        axes[2].set_title('Colored Segmentation')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.savefig('fcn_result.png', dpi=150, bbox_inches='tight')
        plt.show()
        
    else:
        # Simulation
        print("\n[SIMULATION MODE]")
        print("FCN architecture components:")
        print("  - Backbone: ResNet-50 (pretrained on ImageNet)")
        print("  - Head: FCN head with skip connections")
        print("  - Output: 21 classes (Pascal VOC)")


def demo_deeplabv3():
    """
    Demonstrasi arsitektur DeepLabV3.
    """
    print("\n" + "="*70)
    print("DEEPLABV3 ARCHITECTURE")
    print("="*70)
    
    print("""
    [DEEPLABV3 OVERVIEW]
    ─────────────────────────────────────────────────────────────────────
    DeepLabV3 (Chen et al., 2017) menggunakan Atrous Convolution dan
    Atrous Spatial Pyramid Pooling (ASPP) untuk multi-scale segmentation.
    
    
    [ATROUS (DILATED) CONVOLUTION]
    ─────────────────────────────────────────────────────────────────────
    
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
        test_img[:, :] = [135, 206, 235]  # Sky
        test_img[350:, :] = [34, 139, 34]  # Ground
        
        # Add person and car
        cv2.rectangle(test_img, (100, 250), (180, 380), [192, 128, 128], -1)
        cv2.rectangle(test_img, (300, 280), (450, 370), [128, 128, 128], -1)
        
        # Preprocess
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225]),
        ])
        
        input_tensor = preprocess(test_img).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            start = time.time()
            output = model(input_tensor)['out']
            inference_time = time.time() - start
        
        print(f"[INFO] Inference time: {inference_time*1000:.2f} ms")
        
        # Get predictions
        pred = output.argmax(1).squeeze().cpu().numpy()
        
        # Confidence map
        probs = torch.softmax(output, dim=1)
        confidence = probs.max(dim=1)[0].squeeze().cpu().numpy()
        
        # Visualize
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        
        axes[0, 0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Input Image')
        axes[0, 0].axis('off')
        
        color_pred = VOC_COLORMAP[pred % 21]
        axes[0, 1].imshow(color_pred)
        axes[0, 1].set_title('DeepLabV3 Segmentation')
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(confidence, cmap='hot')
        axes[1, 0].set_title('Confidence Map')
        axes[1, 0].axis('off')
        
        # Overlay
        overlay = cv2.addWeighted(test_img, 0.5, color_pred.astype(np.uint8), 0.5, 0)
        axes[1, 1].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Overlay')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig('deeplabv3_result.png', dpi=150, bbox_inches='tight')
        plt.show()
        
    else:
        print("\n[SIMULATION MODE] DeepLabV3 architecture demonstrated.")


def demo_unet_architecture():
    """
    Demonstrasi arsitektur U-Net.
    """
    print("\n" + "="*70)
    print("U-NET ARCHITECTURE")
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
        import torch.nn as nn
        
        class SimpleUNet(nn.Module):
            """
            Simplified U-Net implementation for demonstration.
            """
            def __init__(self, in_channels=3, out_channels=2, features=[64, 128, 256, 512]):
                super(SimpleUNet, self).__init__()
                
                self.encoder = nn.ModuleList()
                self.decoder = nn.ModuleList()
                self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
                
                # Encoder
                for feature in features:
                    self.encoder.append(self._double_conv(in_channels, feature))
                    in_channels = feature
                
                # Bottleneck
                self.bottleneck = self._double_conv(features[-1], features[-1]*2)
                
                # Decoder
                for feature in reversed(features):
                    self.decoder.append(
                        nn.ConvTranspose2d(feature*2, feature, kernel_size=2, stride=2)
                    )
                    self.decoder.append(self._double_conv(feature*2, feature))
                
                # Final conv
                self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)
            
            def _double_conv(self, in_channels, out_channels):
                return nn.Sequential(
                    nn.Conv2d(in_channels, out_channels, 3, padding=1),
                    nn.BatchNorm2d(out_channels),
                    nn.ReLU(inplace=True),
                    nn.Conv2d(out_channels, out_channels, 3, padding=1),
                    nn.BatchNorm2d(out_channels),
                    nn.ReLU(inplace=True),
                )
            
            def forward(self, x):
                skip_connections = []
                
                # Encoder
                for encoder in self.encoder:
                    x = encoder(x)
                    skip_connections.append(x)
                    x = self.pool(x)
                
                x = self.bottleneck(x)
                skip_connections = skip_connections[::-1]
                
                # Decoder
                for idx in range(0, len(self.decoder), 2):
                    x = self.decoder[idx](x)
                    skip = skip_connections[idx//2]
                    
                    # Handle size mismatch
                    if x.shape != skip.shape:
                        x = torch.nn.functional.interpolate(x, size=skip.shape[2:])
                    
                    x = torch.cat((skip, x), dim=1)
                    x = self.decoder[idx+1](x)
                
                return self.final_conv(x)
        
        print("\n[INFO] Creating U-Net model...")
        model = SimpleUNet(in_channels=3, out_channels=2)
        
        # Count parameters
        total_params = sum(p.numel() for p in model.parameters())
        print(f"[INFO] Total parameters: {total_params:,}")
        
        # Test forward pass
        sample_input = torch.randn(1, 3, 256, 256)
        with torch.no_grad():
            output = model(sample_input)
        
        print(f"[INFO] Input shape: {sample_input.shape}")
        print(f"[INFO] Output shape: {output.shape}")
        
        # Visualize U-Net output with synthetic data
        test_img = np.zeros((256, 256, 3), dtype=np.uint8)
        test_img[:, :] = [200, 200, 200]  # Gray background
        
        # Draw a simple cell-like structure
        cv2.circle(test_img, (128, 128), 60, (100, 100, 150), -1)
        cv2.circle(test_img, (128, 128), 30, (50, 50, 100), -1)
        
        # Preprocess
        input_tensor = torch.from_numpy(test_img).permute(2, 0, 1).float() / 255.0
        input_tensor = input_tensor.unsqueeze(0)
        
        # Inference
        model.eval()
        with torch.no_grad():
            output = model(input_tensor)
        
        pred = output.argmax(1).squeeze().cpu().numpy()
        
        # Visualize
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        
        axes[0].imshow(test_img)
        axes[0].set_title('Input Image')
        axes[0].axis('off')
        
        axes[1].imshow(pred, cmap='gray')
        axes[1].set_title('U-Net Prediction (untrained)')
        axes[1].axis('off')
        
        # Overlay
        overlay = test_img.copy()
        overlay[pred == 1] = [255, 0, 0]
        axes[2].imshow(overlay)
        axes[2].set_title('Overlay')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.savefig('unet_demo.png', dpi=150, bbox_inches='tight')
        plt.show()
        
    else:
        print("\n[SIMULATION MODE] U-Net architecture explained.")


def demo_segmentation_metrics():
    """
    Demonstrasi metrics untuk evaluasi semantic segmentation.
    """
    print("\n" + "="*70)
    print("SEGMENTATION METRICS")
    print("="*70)
    
    print("""
    [EVALUATION METRICS]
    ─────────────────────────────────────────────────────────────────────
    
    1. PIXEL ACCURACY
       ────────────────
       Pixel Accuracy = Σ(correct pixels) / Σ(total pixels)
       
       Pros: Simple, intuitive
       Cons: Biased towards dominant classes
    
    2. MEAN PIXEL ACCURACY
       ─────────────────────
       Per-class accuracy, then average:
       mPA = (1/K) × Σ(TP_k / (TP_k + FN_k))
    
    3. INTERSECTION OVER UNION (IoU / Jaccard Index)
       ──────────────────────────────────────────────
       IoU = Area of Overlap / Area of Union
       IoU = TP / (TP + FP + FN)
       
       Ranges from 0 to 1 (higher is better)
    
    4. MEAN IoU (mIoU)
       ─────────────────
       mIoU = (1/K) × Σ(IoU_k)
       
       Standard metric for semantic segmentation benchmarks
    
    5. DICE COEFFICIENT (F1 Score)
       ────────────────────────────
       Dice = 2 × |A ∩ B| / (|A| + |B|)
       Dice = 2 × TP / (2×TP + FP + FN)
       
       Popular in medical image segmentation
    
    6. FREQUENCY WEIGHTED IoU
       ───────────────────────
       FWIoU = Σ(freq_k × IoU_k) / Σ(freq_k)
       
       Weights IoU by class frequency
    """)
    
    def compute_iou(pred, target, num_classes):
        """Compute IoU for each class."""
        ious = []
        for cls in range(num_classes):
            pred_mask = (pred == cls)
            target_mask = (target == cls)
            
            intersection = np.logical_and(pred_mask, target_mask).sum()
            union = np.logical_or(pred_mask, target_mask).sum()
            
            if union == 0:
                iou = float('nan')
            else:
                iou = intersection / union
            
            ious.append(iou)
        
        return ious
    
    def compute_dice(pred, target, num_classes):
        """Compute Dice coefficient for each class."""
        dices = []
        for cls in range(num_classes):
            pred_mask = (pred == cls)
            target_mask = (target == cls)
            
            intersection = np.logical_and(pred_mask, target_mask).sum()
            total = pred_mask.sum() + target_mask.sum()
            
            if total == 0:
                dice = float('nan')
            else:
                dice = 2 * intersection / total
            
            dices.append(dice)
        
        return dices
    
    # Create example prediction and ground truth
    np.random.seed(42)
    
    # Ground truth
    gt = np.zeros((100, 100), dtype=np.int32)
    gt[20:80, 20:80] = 1  # Class 1: square
    gt[40:60, 40:60] = 2  # Class 2: inner square
    
    # Prediction (with some errors)
    pred = gt.copy()
    # Add noise
    noise_mask = np.random.random((100, 100)) < 0.1
    pred[noise_mask] = np.random.randint(0, 3, noise_mask.sum())
    # Shift prediction slightly
    pred = np.roll(pred, 2, axis=0)
    pred = np.roll(pred, 2, axis=1)
    
    # Compute metrics
    num_classes = 3
    ious = compute_iou(pred, gt, num_classes)
    dices = compute_dice(pred, gt, num_classes)
    
    # Pixel accuracy
    pixel_acc = (pred == gt).sum() / pred.size
    
    print("\n[METRICS COMPUTATION EXAMPLE]")
    print(f"Image size: {gt.shape}")
    print(f"Number of classes: {num_classes}")
    print()
    
    print("Per-class IoU:")
    for i, iou in enumerate(ious):
        print(f"  Class {i}: {iou:.4f}")
    print(f"  mIoU: {np.nanmean(ious):.4f}")
    print()
    
    print("Per-class Dice:")
    for i, dice in enumerate(dices):
        print(f"  Class {i}: {dice:.4f}")
    print(f"  mDice: {np.nanmean(dices):.4f}")
    print()
    
    print(f"Pixel Accuracy: {pixel_acc:.4f}")
    
    # Visualize
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    
    axes[0].imshow(gt, cmap='tab10', vmin=0, vmax=2)
    axes[0].set_title('Ground Truth')
    axes[0].axis('off')
    
    axes[1].imshow(pred, cmap='tab10', vmin=0, vmax=2)
    axes[1].set_title('Prediction')
    axes[1].axis('off')
    
    # Difference
    diff = (pred != gt).astype(np.uint8)
    axes[2].imshow(diff, cmap='Reds')
    axes[2].set_title('Errors (white = error)')
    axes[2].axis('off')
    
    # Metrics bar chart
    classes = ['Background', 'Class 1', 'Class 2']
    x = np.arange(len(classes))
    width = 0.35
    
    axes[3].bar(x - width/2, ious, width, label='IoU', color='blue', alpha=0.7)
    axes[3].bar(x + width/2, dices, width, label='Dice', color='orange', alpha=0.7)
    axes[3].set_xticks(x)
    axes[3].set_xticklabels(classes)
    axes[3].set_ylabel('Score')
    axes[3].set_title('Metrics per Class')
    axes[3].legend()
    axes[3].set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('segmentation_metrics.png', dpi=150, bbox_inches='tight')
    plt.show()


def demo_model_comparison():
    """
    Perbandingan berbagai model segmentation.
    """
    print("\n" + "="*70)
    print("SEGMENTATION MODEL COMPARISON")
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
    → Trade accuracy for speed
    
    HIGH ACCURACY:
    → DeepLabV3+, PSPNet, HRNet
    → Use for offline processing
    
    MEDICAL IMAGING:
    → U-Net, nnU-Net, V-Net
    → Designed for small datasets
    
    SCENE UNDERSTANDING:
    → PSPNet, DeepLabV3
    → Good for outdoor scenes
    
    EDGE DETECTION + SEGMENTATION:
    → HRNet
    → Maintains high resolution
    
    TRANSFORMER-BASED:
    → SegFormer, SETR, Mask2Former
    → Latest SOTA approaches
    """)
    
    if TORCH_AVAILABLE:
        print("\n[INFO] Benchmarking available models...")
        
        models_info = []
        
        # FCN ResNet50
        print("  Loading FCN-ResNet50...")
        model = fcn_resnet50(pretrained=True)
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('FCN-ResNet50', params))
        del model
        
        # FCN ResNet101
        print("  Loading FCN-ResNet101...")
        model = fcn_resnet101(pretrained=True)
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('FCN-ResNet101', params))
        del model
        
        # DeepLabV3 ResNet50
        print("  Loading DeepLabV3-ResNet50...")
        model = deeplabv3_resnet50(pretrained=True)
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('DeepLabV3-ResNet50', params))
        del model
        
        # DeepLabV3 ResNet101
        print("  Loading DeepLabV3-ResNet101...")
        model = deeplabv3_resnet101(pretrained=True)
        params = sum(p.numel() for p in model.parameters())
        models_info.append(('DeepLabV3-ResNet101', params))
        del model
        
        print("\n[INFO] Model Parameter Comparison:")
        for name, params in models_info:
            print(f"  {name}: {params/1e6:.2f}M parameters")
        
        # Visualize comparison
        fig, ax = plt.subplots(figsize=(10, 5))
        
        names = [m[0] for m in models_info]
        params = [m[1]/1e6 for m in models_info]
        
        bars = ax.barh(names, params, color=['#3498db', '#2980b9', '#e74c3c', '#c0392b'])
        ax.set_xlabel('Parameters (Millions)')
        ax.set_title('Segmentation Model Parameters')
        
        for bar, p in zip(bars, params):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{p:.1f}M', va='center')
        
        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
        plt.show()


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM SEMANTIC SEGMENTATION")
    print("="*70)
    
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
        
        choice = input("\nPilih menu (0-7): ").strip()
        
        if choice == '1':
            demo_segmentation_concept()
        elif choice == '2':
            demo_fcn_architecture()
        elif choice == '3':
            demo_deeplabv3()
        elif choice == '4':
            demo_unet_architecture()
        elif choice == '5':
            demo_segmentation_metrics()
        elif choice == '6':
            demo_model_comparison()
        elif choice == '7':
            demo_segmentation_concept()
            demo_fcn_architecture()
            demo_deeplabv3()
            demo_unet_architecture()
            demo_segmentation_metrics()
            demo_model_comparison()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
