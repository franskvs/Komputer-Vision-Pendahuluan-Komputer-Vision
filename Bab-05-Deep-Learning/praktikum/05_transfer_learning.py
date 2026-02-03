"""
=============================================================================
PRAKTIKUM 05 - TRANSFER LEARNING
=============================================================================
Program ini mendemonstrasikan Transfer Learning menggunakan pre-trained
models untuk image classification pada custom dataset.

Transfer Learning memungkinkan kita memanfaatkan knowledge dari model
yang sudah dilatih pada dataset besar (ImageNet) untuk task baru dengan
dataset yang lebih kecil.

Konsep yang dipelajari:
1. Loading pre-trained models
2. Feature extraction (freeze base model)
3. Fine-tuning (unfreeze beberapa layers)
4. Custom dataset preparation
5. Training strategies

Kebutuhan:
- torch >= 2.0.0 atau tensorflow >= 2.10.0
- torchvision atau keras.applications
- numpy, matplotlib

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import numpy as np
import os

# Check framework availability
PYTORCH_AVAILABLE = False
TENSORFLOW_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, Dataset
    import torchvision
    from torchvision import models, transforms
    PYTORCH_AVAILABLE = True
    print("[INFO] PyTorch tersedia")
except ImportError:
    pass

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
    print("[INFO] TensorFlow tersedia")
except ImportError:
    pass

if not PYTORCH_AVAILABLE and not TENSORFLOW_AVAILABLE:
    print("[WARNING] Tidak ada framework DL yang tersedia - mode simulasi")


# =============================================================================
# PYTORCH IMPLEMENTATION
# =============================================================================

if PYTORCH_AVAILABLE:
    class CustomDataset(Dataset):
        """
        Custom Dataset untuk loading gambar.
        
        Struktur folder expected:
        data/
        ├── train/
        │   ├── class1/
        │   │   ├── img1.jpg
        │   │   └── ...
        │   └── class2/
        │       └── ...
        └── val/
            └── ...
        """
        
        def __init__(self, images, labels, transform=None):
            """
            Args:
                images: List of images (numpy arrays)
                labels: List of labels (integers)
                transform: torchvision transforms
            """
            self.images = images
            self.labels = labels
            self.transform = transform
        
        def __len__(self):
            return len(self.images)
        
        def __getitem__(self, idx):
            image = self.images[idx]
            label = self.labels[idx]
            
            if self.transform:
                image = self.transform(image)
            
            return image, label


def get_pretrained_model_pytorch(model_name='resnet18', num_classes=10, freeze=True):
    """
    Load pre-trained model dan modify untuk custom classes.
    
    Args:
        model_name: Nama model ('resnet18', 'resnet50', 'mobilenet_v2', etc.)
        num_classes: Jumlah class output
        freeze: Apakah freeze base model weights
        
    Returns:
        model: Modified model untuk custom task
    """
    # Load pre-trained model
    if model_name == 'resnet18':
        model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)
        
    elif model_name == 'resnet50':
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)
        
    elif model_name == 'mobilenet_v2':
        model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
        
    elif model_name == 'efficientnet_b0':
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
    
    else:
        raise ValueError(f"Model {model_name} tidak didukung")
    
    # Freeze base model jika diperlukan
    if freeze:
        for param in model.parameters():
            param.requires_grad = False
        
        # Unfreeze classifier
        if model_name in ['resnet18', 'resnet50']:
            for param in model.fc.parameters():
                param.requires_grad = True
        else:
            for param in model.classifier.parameters():
                param.requires_grad = True
    
    return model


def demo_transfer_learning_pytorch():
    """
    Demonstrasi Transfer Learning dengan PyTorch.
    """
    print("\n" + "="*70)
    print("TRANSFER LEARNING DENGAN PYTORCH")
    print("="*70)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n[INFO] Using device: {device}")
    
    # Hyperparameters
    num_classes = 5  # Contoh: 5 kategori produk
    batch_size = 16
    num_epochs = 5
    learning_rate = 0.001
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Generate dummy dataset
    print("\n[INFO] Generating synthetic dataset...")
    num_samples = 100
    
    # Create random images (RGB, various sizes)
    train_images = [np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8) 
                   for _ in range(num_samples)]
    train_labels = [i % num_classes for i in range(num_samples)]
    
    val_images = [np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8) 
                 for _ in range(20)]
    val_labels = [i % num_classes for i in range(20)]
    
    # Create datasets
    train_dataset = CustomDataset(train_images, train_labels, train_transform)
    val_dataset = CustomDataset(val_images, val_labels, val_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"[INFO] Training samples: {len(train_dataset)}")
    print(f"[INFO] Validation samples: {len(val_dataset)}")
    
    # Load pre-trained model
    print("\n[INFO] Loading pre-trained ResNet18...")
    model = get_pretrained_model_pytorch('resnet18', num_classes, freeze=True)
    model = model.to(device)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"[INFO] Total parameters: {total_params:,}")
    print(f"[INFO] Trainable parameters: {trainable_params:,}")
    print(f"[INFO] Frozen parameters: {total_params - trainable_params:,}")
    
    # Loss dan optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
                          lr=learning_rate)
    
    # Training loop
    print("\n[INFO] Starting training (Feature Extraction)...")
    print("-"*60)
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            # Forward
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        train_loss = running_loss / len(train_loader)
        train_acc = 100 * correct / total
        
        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_acc = 100 * val_correct / val_total
        
        print(f"Epoch [{epoch+1}/{num_epochs}] "
              f"Loss: {train_loss:.4f}, "
              f"Train Acc: {train_acc:.2f}%, "
              f"Val Acc: {val_acc:.2f}%")
    
    print("\n[INFO] Feature Extraction complete!")
    
    # Fine-tuning demonstration
    print("\n[INFO] Starting Fine-tuning (unfreeze last layers)...")
    print("-"*60)
    
    # Unfreeze last few layers
    for name, param in model.named_parameters():
        if 'layer4' in name or 'fc' in name:
            param.requires_grad = True
    
    trainable_params_ft = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[INFO] Trainable parameters after unfreezing: {trainable_params_ft:,}")
    
    # Lower learning rate untuk fine-tuning
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
                          lr=learning_rate * 0.1)
    
    # Train beberapa epoch lagi
    for epoch in range(2):
        model.train()
        running_loss = 0.0
        
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f"Fine-tune Epoch [{epoch+1}/2] Loss: {running_loss/len(train_loader):.4f}")
    
    print("\n[INFO] Fine-tuning complete!")
    
    # Save model
    torch.save(model.state_dict(), 'transfer_model_pytorch.pth')
    print("[INFO] Model saved to transfer_model_pytorch.pth")


# =============================================================================
# TENSORFLOW/KERAS IMPLEMENTATION
# =============================================================================

def demo_transfer_learning_keras():
    """
    Demonstrasi Transfer Learning dengan Keras.
    """
    if not TENSORFLOW_AVAILABLE:
        print("[ERROR] TensorFlow tidak tersedia")
        return
    
    print("\n" + "="*70)
    print("TRANSFER LEARNING DENGAN KERAS")
    print("="*70)
    
    # Parameters
    num_classes = 5
    img_size = (224, 224)
    batch_size = 16
    
    # Generate synthetic data
    print("\n[INFO] Generating synthetic dataset...")
    num_train = 100
    num_val = 20
    
    x_train = np.random.randint(0, 255, (num_train, 224, 224, 3)).astype('float32') / 255.0
    y_train = np.random.randint(0, num_classes, num_train)
    
    x_val = np.random.randint(0, 255, (num_val, 224, 224, 3)).astype('float32') / 255.0
    y_val = np.random.randint(0, num_classes, num_val)
    
    print(f"[INFO] Training samples: {len(x_train)}")
    print(f"[INFO] Validation samples: {len(x_val)}")
    
    # Data augmentation
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ])
    
    # Load pre-trained MobileNetV2
    print("\n[INFO] Loading pre-trained MobileNetV2...")
    
    base_model = keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Build model
    inputs = keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    
    # Preprocessing for MobileNetV2
    x = keras.applications.mobilenet_v2.preprocess_input(x)
    
    # Base model
    x = base_model(x, training=False)
    
    # Custom classifier
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    
    # Print model info
    print(f"\n[INFO] Total layers: {len(model.layers)}")
    print(f"[INFO] Trainable variables: {len(model.trainable_variables)}")
    
    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Feature Extraction training
    print("\n[INFO] Starting Feature Extraction training...")
    print("-"*60)
    
    history = model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=5,
        batch_size=batch_size,
        verbose=1
    )
    
    # Fine-tuning
    print("\n[INFO] Starting Fine-tuning...")
    print("-"*60)
    
    # Unfreeze base model
    base_model.trainable = True
    
    # Freeze semua kecuali 20 layer terakhir
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    # Recompile dengan learning rate lebih kecil
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"[INFO] Trainable variables after unfreezing: {len(model.trainable_variables)}")
    
    # Fine-tune
    history_ft = model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=3,
        batch_size=batch_size,
        verbose=1
    )
    
    # Save model
    model.save('transfer_model_keras.h5')
    print("\n[INFO] Model saved to transfer_model_keras.h5")


def demo_transfer_learning_simulation():
    """
    Simulasi Transfer Learning tanpa framework.
    """
    print("\n" + "="*70)
    print("SIMULASI TRANSFER LEARNING")
    print("="*70)
    
    print("""
    [KONSEP TRANSFER LEARNING]
    ─────────────────────────────────────────────────────────────────────
    
    Pre-trained Model (ImageNet):
    ┌─────────────────────────────────────────────────────────────────┐
    │ Conv Layers (Feature Extractor)    │  FC Layers (Classifier)    │
    │                                    │                            │
    │  Layer 1: Edge detection           │  FC1: 2048 → 1000 classes │
    │  Layer 2: Textures                 │  (ImageNet classes)        │
    │  Layer 3: Patterns                 │                            │
    │  Layer 4: Object parts             │                            │
    │  Layer 5: High-level features      │                            │
    │                                    │                            │
    │  [FREEZE THESE LAYERS]             │  [REPLACE THIS]            │
    └─────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
    Custom Model:
    ┌─────────────────────────────────────────────────────────────────┐
    │ Conv Layers (Pre-trained, Frozen)  │  New Classifier           │
    │                                    │                            │
    │  Same as above                     │  FC1: 2048 → 256          │
    │  ∂L/∂w = 0 (no updates)           │  FC2: 256 → num_classes   │
    │                                    │  (Your classes)            │
    │                                    │                            │
    │  [FROZEN]                          │  [TRAINABLE]               │
    └─────────────────────────────────────────────────────────────────┘
    """)
    
    # Simulated training results
    print("\n[SIMULATED TRAINING - Feature Extraction]")
    print("-"*60)
    
    feature_extraction_results = [
        {"epoch": 1, "train_loss": 1.234, "train_acc": 45.2, "val_acc": 52.3},
        {"epoch": 2, "train_loss": 0.856, "train_acc": 62.1, "val_acc": 65.4},
        {"epoch": 3, "train_loss": 0.623, "train_acc": 75.3, "val_acc": 72.1},
        {"epoch": 4, "train_loss": 0.478, "train_acc": 82.5, "val_acc": 78.6},
        {"epoch": 5, "train_loss": 0.356, "train_acc": 87.2, "val_acc": 82.3},
    ]
    
    print(f"{'Epoch':<8} {'Loss':<12} {'Train Acc':<12} {'Val Acc':<12}")
    print("-"*50)
    for r in feature_extraction_results:
        print(f"{r['epoch']:<8} {r['train_loss']:<12.4f} "
              f"{r['train_acc']:<12.1f}% {r['val_acc']:<12.1f}%")
    
    print("\n[SIMULATED TRAINING - Fine-tuning]")
    print("-"*60)
    
    finetuning_results = [
        {"epoch": 1, "train_loss": 0.312, "train_acc": 89.1, "val_acc": 84.5},
        {"epoch": 2, "train_loss": 0.245, "train_acc": 91.5, "val_acc": 87.2},
        {"epoch": 3, "train_loss": 0.198, "train_acc": 93.2, "val_acc": 89.1},
    ]
    
    print(f"{'Epoch':<8} {'Loss':<12} {'Train Acc':<12} {'Val Acc':<12}")
    print("-"*50)
    for r in finetuning_results:
        print(f"{r['epoch']:<8} {r['train_loss']:<12.4f} "
              f"{r['train_acc']:<12.1f}% {r['val_acc']:<12.1f}%")
    
    print("\n[RESULT] Final Validation Accuracy: 89.1%")
    
    # Comparison
    print("\n[COMPARISON: Transfer Learning vs Training from Scratch]")
    print("-"*60)
    print("""
    Metric                  Transfer Learning    From Scratch
    ──────────────────────────────────────────────────────────
    Training Time           ~15 minutes          ~2 hours
    Data Required           100-1000 images      10,000+ images
    Final Accuracy          89.1%                75.3%
    Convergence             Fast (5-10 epochs)   Slow (50+ epochs)
    GPU Memory              Lower                Higher
    """)


def demo_pretrained_models_info():
    """
    Informasi tentang berbagai pre-trained models.
    """
    print("\n" + "="*70)
    print("PRE-TRAINED MODELS UNTUK TRANSFER LEARNING")
    print("="*70)
    
    models_info = {
        "MobileNetV2": {
            "params": "3.5M",
            "input_size": "224×224",
            "top1_acc": "72.0%",
            "best_for": "Mobile, edge devices",
            "feature_dim": 1280
        },
        "ResNet50": {
            "params": "25.6M",
            "input_size": "224×224",
            "top1_acc": "76.1%",
            "best_for": "General purpose, medium datasets",
            "feature_dim": 2048
        },
        "EfficientNetB0": {
            "params": "5.3M",
            "input_size": "224×224",
            "top1_acc": "77.1%",
            "best_for": "Best efficiency/accuracy",
            "feature_dim": 1280
        },
        "EfficientNetB4": {
            "params": "19M",
            "input_size": "380×380",
            "top1_acc": "82.9%",
            "best_for": "High accuracy needs",
            "feature_dim": 1792
        },
        "VGG16": {
            "params": "138M",
            "input_size": "224×224",
            "top1_acc": "71.5%",
            "best_for": "Feature extraction, style transfer",
            "feature_dim": 4096
        },
        "InceptionV3": {
            "params": "23.8M",
            "input_size": "299×299",
            "top1_acc": "77.9%",
            "best_for": "Multi-scale features",
            "feature_dim": 2048
        }
    }
    
    print(f"\n{'Model':<16} {'Params':<10} {'Input':<12} {'Top-1':<10} {'Features':<10}")
    print("-"*70)
    
    for name, info in models_info.items():
        print(f"{name:<16} {info['params']:<10} {info['input_size']:<12} "
              f"{info['top1_acc']:<10} {info['feature_dim']:<10}")
    
    print("\n[RECOMMENDATIONS BY DATASET SIZE]")
    print("-"*60)
    print("""
    Dataset Size          Recommended Strategy
    ──────────────────────────────────────────────────────────────
    < 1000 images         Feature extraction only (freeze all)
    1000-10000 images     Fine-tune top layers
    > 10000 images        Fine-tune more layers atau train from scratch
    
    [RECOMMENDATIONS BY COMPUTE]
    ──────────────────────────────────────────────────────────────
    CPU only              MobileNetV2, EfficientNetB0
    Low-end GPU           ResNet50, EfficientNetB2
    High-end GPU          EfficientNetB4-B7, ResNet152
    """)


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM TRANSFER LEARNING")
    print("="*70)
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Info Pre-trained Models")
        print("2. Transfer Learning dengan PyTorch")
        print("3. Transfer Learning dengan Keras")
        print("4. Simulasi Transfer Learning")
        print("5. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-5): ").strip()
        
        if choice == '1':
            demo_pretrained_models_info()
        elif choice == '2':
            if PYTORCH_AVAILABLE:
                demo_transfer_learning_pytorch()
            else:
                print("[ERROR] PyTorch tidak tersedia")
                demo_transfer_learning_simulation()
        elif choice == '3':
            if TENSORFLOW_AVAILABLE:
                demo_transfer_learning_keras()
            else:
                print("[ERROR] TensorFlow tidak tersedia")
                demo_transfer_learning_simulation()
        elif choice == '4':
            demo_transfer_learning_simulation()
        elif choice == '5':
            demo_pretrained_models_info()
            demo_transfer_learning_simulation()
            if PYTORCH_AVAILABLE:
                demo_transfer_learning_pytorch()
            if TENSORFLOW_AVAILABLE:
                demo_transfer_learning_keras()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
