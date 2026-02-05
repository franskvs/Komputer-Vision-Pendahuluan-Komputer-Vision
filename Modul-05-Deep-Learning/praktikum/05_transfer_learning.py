"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 05 - TRANSFER LEARNING
# Assignment - set nilai ke variabel
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
# Assignment - set nilai ke variabel
- torch >= 2.0.0 atau tensorflow >= 2.10.0
- torchvision atau keras.applications
- numpy, matplotlib

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
# Assignment - set nilai ke variabel
=============================================================================
"""

# Import library/module untuk digunakan
import numpy as np
# Import library/module untuk digunakan
import os

# Check framework availability
PYTORCH_AVAILABLE = False
# Assignment - set nilai ke variabel
TENSORFLOW_AVAILABLE = False

# Blok try-except untuk error handling
try:
    # Import library/module untuk digunakan
    import torch
    # Import library/module untuk digunakan
    import torch.nn as nn
    # Import library/module untuk digunakan
    import torch.optim as optim
    # Import library/module untuk digunakan
    from torch.utils.data import DataLoader, Dataset
    # Import library/module untuk digunakan
    import torchvision
    # Import library/module untuk digunakan
    from torchvision import models, transforms
    # Assignment - set nilai ke variabel
    PYTORCH_AVAILABLE = True
    print("[INFO] PyTorch tersedia")
# Tangkap exception jika ada error di blok try
except ImportError:
    pass

# Blok try-except untuk error handling
try:
    # Import library/module untuk digunakan
    import tensorflow as tf
    # Import library/module untuk digunakan
    from tensorflow import keras
    # Import library/module untuk digunakan
    from tensorflow.keras import layers
    # Assignment - set nilai ke variabel
    TENSORFLOW_AVAILABLE = True
    print("[INFO] TensorFlow tersedia")
# Tangkap exception jika ada error di blok try
except ImportError:
    pass

# Conditional statement - eksekusi jika kondisi True
if not PYTORCH_AVAILABLE and not TENSORFLOW_AVAILABLE:
    print("[WARNING] Tidak ada framework DL yang tersedia - mode simulasi")


# =============================================================================
# PYTORCH IMPLEMENTATION
# =============================================================================

# Conditional statement - eksekusi jika kondisi True
if PYTORCH_AVAILABLE:
    # Definisi class untuk membuat object
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
        
        # Definisi function dengan nama dan parameter
        def __init__(self, images, labels, transform=None):
            """
            Args:
                images: List of images (numpy arrays)
                labels: List of labels (integers)
                transform: torchvision transforms
            """
            # Assignment - set nilai ke variabel
            self.images = images
            # Assignment - set nilai ke variabel
            self.labels = labels
            # Assignment - set nilai ke variabel
            self.transform = transform
        
        # Definisi function dengan nama dan parameter
        def __len__(self):
            # Return value dari function
            return len(self.images)
        
        # Definisi function dengan nama dan parameter
        def __getitem__(self, idx):
            # Assignment - set nilai ke variabel
            image = self.images[idx]
            # Assignment - set nilai ke variabel
            label = self.labels[idx]
            
            # Conditional statement - eksekusi jika kondisi True
            if self.transform:
                # Assignment - set nilai ke variabel
                image = self.transform(image)
            
            # Return value dari function
            return image, label


# Definisi function dengan nama dan parameter
def get_pretrained_model_pytorch(model_name='resnet18', num_classes=10, freeze=True):
    """
    Load pre-trained model dan modify untuk custom classes.
    
    Args:
        model_name: Nama model ('resnet18', 'resnet50', 'mobilenet_v2', etc.)
        # Definisi class untuk membuat object
        num_classes: Jumlah class output
        freeze: Apakah freeze base model weights
        
    Returns:
        model: Modified model untuk custom task
    """
    # Load pre-trained model
    if model_name == 'resnet18':
        # Assignment - set nilai ke variabel
        model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        # Assignment - set nilai ke variabel
        in_features = model.fc.in_features
        # Assignment - set nilai ke variabel
        model.fc = nn.Linear(in_features, num_classes)
        
    # Conditional statement - eksekusi jika kondisi True
    elif model_name == 'resnet50':
        # Assignment - set nilai ke variabel
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        # Assignment - set nilai ke variabel
        in_features = model.fc.in_features
        # Assignment - set nilai ke variabel
        model.fc = nn.Linear(in_features, num_classes)
        
    # Conditional statement - eksekusi jika kondisi True
    elif model_name == 'mobilenet_v2':
        # Assignment - set nilai ke variabel
        model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
        # Assignment - set nilai ke variabel
        in_features = model.classifier[1].in_features
        # Assignment - set nilai ke variabel
        model.classifier[1] = nn.Linear(in_features, num_classes)
        
    # Conditional statement - eksekusi jika kondisi True
    elif model_name == 'efficientnet_b0':
        # Assignment - set nilai ke variabel
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        # Assignment - set nilai ke variabel
        in_features = model.classifier[1].in_features
        # Assignment - set nilai ke variabel
        model.classifier[1] = nn.Linear(in_features, num_classes)
    
    else:
        raise ValueError(f"Model {model_name} tidak didukung")
    
    # Freeze base model jika diperlukan
    if freeze:
        # Iterasi/loop melalui elemen dalam koleksi
        for param in model.parameters():
            # Assignment - set nilai ke variabel
            param.requires_grad = False
        
        # Unfreeze classifier
        if model_name in ['resnet18', 'resnet50']:
            # Iterasi/loop melalui elemen dalam koleksi
            for param in model.fc.parameters():
                # Assignment - set nilai ke variabel
                param.requires_grad = True
        else:
            # Iterasi/loop melalui elemen dalam koleksi
            for param in model.classifier.parameters():
                # Assignment - set nilai ke variabel
                param.requires_grad = True
    
    # Return value dari function
    return model


# Definisi function dengan nama dan parameter
def demo_transfer_learning_pytorch():
    """
    Demonstrasi Transfer Learning dengan PyTorch.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("TRANSFER LEARNING DENGAN PYTORCH")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Conditional statement - eksekusi jika kondisi True
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n[INFO] Using device: {device}")
    
    # Hyperparameters
    num_classes = 5  # Contoh: 5 kategori produk
    # Assignment - set nilai ke variabel
    batch_size = 16
    # Assignment - set nilai ke variabel
    num_epochs = 5
    # Assignment - set nilai ke variabel
    learning_rate = 0.001
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        # Assignment - set nilai ke variabel
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        # Assignment - set nilai ke variabel
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           # Assignment - set nilai ke variabel
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Assignment - set nilai ke variabel
    val_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        # Assignment - set nilai ke variabel
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           # Assignment - set nilai ke variabel
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Generate dummy dataset
    print("\n[INFO] Generating synthetic dataset...")
    # Assignment - set nilai ke variabel
    num_samples = 100
    
    # Create random images (RGB, various sizes)
    train_images = [np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8) 
                   # Iterasi/loop melalui elemen dalam koleksi
                   for _ in range(num_samples)]
    # Iterasi/loop melalui elemen dalam koleksi
    train_labels = [i % num_classes for i in range(num_samples)]
    
    # Generate random integer dalam range tertentu
    val_images = [np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8) 
                 # Iterasi/loop melalui elemen dalam koleksi
                 for _ in range(20)]
    # Iterasi/loop melalui elemen dalam koleksi
    val_labels = [i % num_classes for i in range(20)]
    
    # Create datasets
    train_dataset = CustomDataset(train_images, train_labels, train_transform)
    # Assignment - set nilai ke variabel
    val_dataset = CustomDataset(val_images, val_labels, val_transform)
    
    # Assignment - set nilai ke variabel
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    # Assignment - set nilai ke variabel
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"[INFO] Training samples: {len(train_dataset)}")
    print(f"[INFO] Validation samples: {len(val_dataset)}")
    
    # Load pre-trained model
    print("\n[INFO] Loading pre-trained ResNet18...")
    # Assignment - set nilai ke variabel
    model = get_pretrained_model_pytorch('resnet18', num_classes, freeze=True)
    # Assignment - set nilai ke variabel
    model = model.to(device)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    # Iterasi/loop melalui elemen dalam koleksi
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"[INFO] Total parameters: {total_params:,}")
    print(f"[INFO] Trainable parameters: {trainable_params:,}")
    print(f"[INFO] Frozen parameters: {total_params - trainable_params:,}")
    
    # Loss dan optimizer
    criterion = nn.CrossEntropyLoss()
    # Assignment - set nilai ke variabel
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
                          # Assignment - set nilai ke variabel
                          lr=learning_rate)
    
    # Training loop
    print("\n[INFO] Starting training (Feature Extraction)...")
    print("-"*60)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for epoch in range(num_epochs):
        model.train()
        # Assignment - set nilai ke variabel
        running_loss = 0.0
        # Assignment - set nilai ke variabel
        correct = 0
        # Assignment - set nilai ke variabel
        total = 0
        
        # Iterasi/loop melalui elemen dalam koleksi
        for images, labels in train_loader:
            # Assignment - set nilai ke variabel
            images = images.to(device)
            # Assignment - set nilai ke variabel
            labels = labels.to(device)
            
            # Forward
            outputs = model(images)
            # Assignment - set nilai ke variabel
            loss = criterion(outputs, labels)
            
            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            # Assignment - set nilai ke variabel
            _, predicted = torch.max(outputs.data, 1)
            # Assignment - set nilai ke variabel
            total += labels.size(0)
            # Assignment - set nilai ke variabel
            correct += (predicted == labels).sum().item()
        
        # Assignment - set nilai ke variabel
        train_loss = running_loss / len(train_loader)
        # Assignment - set nilai ke variabel
        train_acc = 100 * correct / total
        
        # Validation
        model.eval()
        # Assignment - set nilai ke variabel
        val_correct = 0
        # Assignment - set nilai ke variabel
        val_total = 0
        
        with torch.no_grad():
            # Iterasi/loop melalui elemen dalam koleksi
            for images, labels in val_loader:
                # Assignment - set nilai ke variabel
                images = images.to(device)
                # Assignment - set nilai ke variabel
                labels = labels.to(device)
                # Assignment - set nilai ke variabel
                outputs = model(images)
                # Assignment - set nilai ke variabel
                _, predicted = torch.max(outputs.data, 1)
                # Assignment - set nilai ke variabel
                val_total += labels.size(0)
                # Assignment - set nilai ke variabel
                val_correct += (predicted == labels).sum().item()
        
        # Assignment - set nilai ke variabel
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
        # Conditional statement - eksekusi jika kondisi True
        if 'layer4' in name or 'fc' in name:
            # Assignment - set nilai ke variabel
            param.requires_grad = True
    
    # Iterasi/loop melalui elemen dalam koleksi
    trainable_params_ft = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[INFO] Trainable parameters after unfreezing: {trainable_params_ft:,}")
    
    # Lower learning rate untuk fine-tuning
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
                          # Assignment - set nilai ke variabel
                          lr=learning_rate * 0.1)
    
    # Train beberapa epoch lagi
    for epoch in range(2):
        model.train()
        # Assignment - set nilai ke variabel
        running_loss = 0.0
        
        # Iterasi/loop melalui elemen dalam koleksi
        for images, labels in train_loader:
            # Assignment - set nilai ke variabel
            images = images.to(device)
            # Assignment - set nilai ke variabel
            labels = labels.to(device)
            
            # Assignment - set nilai ke variabel
            outputs = model(images)
            # Assignment - set nilai ke variabel
            loss = criterion(outputs, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Assignment - set nilai ke variabel
            running_loss += loss.item()
        
        print(f"Fine-tune Epoch [{epoch+1}/2] Loss: {running_loss/len(train_loader):.4f}")
    
    print("\n[INFO] Fine-tuning complete!")
    
    # Save model
    torch.save(model.state_dict(), 'transfer_model_pytorch.pth')
    print("[INFO] Model saved to transfer_model_pytorch.pth")


# =============================================================================
# TENSORFLOW/KERAS IMPLEMENTATION
# =============================================================================

# Definisi function dengan nama dan parameter
def demo_transfer_learning_keras():
    """
    Demonstrasi Transfer Learning dengan Keras.
    """
    # Conditional statement - eksekusi jika kondisi True
    if not TENSORFLOW_AVAILABLE:
        print("[ERROR] TensorFlow tidak tersedia")
        return
    
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("TRANSFER LEARNING DENGAN KERAS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Parameters
    num_classes = 5
    # Assignment - set nilai ke variabel
    img_size = (224, 224)
    # Assignment - set nilai ke variabel
    batch_size = 16
    
    # Generate synthetic data
    print("\n[INFO] Generating synthetic dataset...")
    # Assignment - set nilai ke variabel
    num_train = 100
    # Assignment - set nilai ke variabel
    num_val = 20
    
    # Generate random integer dalam range tertentu
    x_train = np.random.randint(0, 255, (num_train, 224, 224, 3)).astype('float32') / 255.0
    # Generate random integer dalam range tertentu
    y_train = np.random.randint(0, num_classes, num_train)
    
    # Generate random integer dalam range tertentu
    x_val = np.random.randint(0, 255, (num_val, 224, 224, 3)).astype('float32') / 255.0
    # Generate random integer dalam range tertentu
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
    
    # Assignment - set nilai ke variabel
    base_model = keras.applications.MobileNetV2(
        # Assignment - set nilai ke variabel
        input_shape=(224, 224, 3),
        # Assignment - set nilai ke variabel
        include_top=False,
        # Assignment - set nilai ke variabel
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Build model
    inputs = keras.Input(shape=(224, 224, 3))
    # Assignment - set nilai ke variabel
    x = data_augmentation(inputs)
    
    # Preprocessing for MobileNetV2
    x = keras.applications.mobilenet_v2.preprocess_input(x)
    
    # Base model
    x = base_model(x, training=False)
    
    # Custom classifier
    x = layers.GlobalAveragePooling2D()(x)
    # Assignment - set nilai ke variabel
    x = layers.Dropout(0.2)(x)
    # Assignment - set nilai ke variabel
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    # Assignment - set nilai ke variabel
    model = keras.Model(inputs, outputs)
    
    # Print model info
    print(f"\n[INFO] Total layers: {len(model.layers)}")
    print(f"[INFO] Trainable variables: {len(model.trainable_variables)}")
    
    # Compile
    model.compile(
        # Assignment - set nilai ke variabel
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        # Assignment - set nilai ke variabel
        loss='sparse_categorical_crossentropy',
        # Assignment - set nilai ke variabel
        metrics=['accuracy']
    )
    
    # Feature Extraction training
    print("\n[INFO] Starting Feature Extraction training...")
    print("-"*60)
    
    # Train model dengan data training dan validation
    history = model.fit(
        x_train, y_train,
        # Assignment - set nilai ke variabel
        validation_data=(x_val, y_val),
        # Assignment - set nilai ke variabel
        epochs=5,
        # Assignment - set nilai ke variabel
        batch_size=batch_size,
        # Assignment - set nilai ke variabel
        verbose=1
    )
    
    # Fine-tuning
    print("\n[INFO] Starting Fine-tuning...")
    print("-"*60)
    
    # Unfreeze base model
    base_model.trainable = True
    
    # Freeze semua kecuali 20 layer terakhir
    for layer in base_model.layers[:-20]:
        # Assignment - set nilai ke variabel
        layer.trainable = False
    
    # Recompile dengan learning rate lebih kecil
    model.compile(
        # Assignment - set nilai ke variabel
        optimizer=keras.optimizers.Adam(learning_rate=1e-5),
        # Assignment - set nilai ke variabel
        loss='sparse_categorical_crossentropy',
        # Assignment - set nilai ke variabel
        metrics=['accuracy']
    )
    
    print(f"[INFO] Trainable variables after unfreezing: {len(model.trainable_variables)}")
    
    # Fine-tune
    history_ft = model.fit(
        x_train, y_train,
        # Assignment - set nilai ke variabel
        validation_data=(x_val, y_val),
        # Assignment - set nilai ke variabel
        epochs=3,
        # Assignment - set nilai ke variabel
        batch_size=batch_size,
        # Assignment - set nilai ke variabel
        verbose=1
    )
    
    # Save model
    model.save('transfer_model_keras.h5')
    print("\n[INFO] Model saved to transfer_model_keras.h5")


# Definisi function dengan nama dan parameter
def demo_transfer_learning_simulation():
    """
    Simulasi Transfer Learning tanpa framework.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("SIMULASI TRANSFER LEARNING")
    # Assignment - set nilai ke variabel
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
    # Assignment - set nilai ke variabel
    │  ∂L/∂w = 0 (no updates)           │  FC2: 256 → num_classes   │
    │                                    │  (Your classes)            │
    │                                    │                            │
    │  [FROZEN]                          │  [TRAINABLE]               │
    └─────────────────────────────────────────────────────────────────┘
    """)
    
    # Simulated training results
    print("\n[SIMULATED TRAINING - Feature Extraction]")
    print("-"*60)
    
    # Assignment - set nilai ke variabel
    feature_extraction_results = [
        {"epoch": 1, "train_loss": 1.234, "train_acc": 45.2, "val_acc": 52.3},
        {"epoch": 2, "train_loss": 0.856, "train_acc": 62.1, "val_acc": 65.4},
        {"epoch": 3, "train_loss": 0.623, "train_acc": 75.3, "val_acc": 72.1},
        {"epoch": 4, "train_loss": 0.478, "train_acc": 82.5, "val_acc": 78.6},
        {"epoch": 5, "train_loss": 0.356, "train_acc": 87.2, "val_acc": 82.3},
    ]
    
    print(f"{'Epoch':<8} {'Loss':<12} {'Train Acc':<12} {'Val Acc':<12}")
    print("-"*50)
    # Iterasi/loop melalui elemen dalam koleksi
    for r in feature_extraction_results:
        print(f"{r['epoch']:<8} {r['train_loss']:<12.4f} "
              f"{r['train_acc']:<12.1f}% {r['val_acc']:<12.1f}%")
    
    print("\n[SIMULATED TRAINING - Fine-tuning]")
    print("-"*60)
    
    # Assignment - set nilai ke variabel
    finetuning_results = [
        {"epoch": 1, "train_loss": 0.312, "train_acc": 89.1, "val_acc": 84.5},
        {"epoch": 2, "train_loss": 0.245, "train_acc": 91.5, "val_acc": 87.2},
        {"epoch": 3, "train_loss": 0.198, "train_acc": 93.2, "val_acc": 89.1},
    ]
    
    print(f"{'Epoch':<8} {'Loss':<12} {'Train Acc':<12} {'Val Acc':<12}")
    print("-"*50)
    # Iterasi/loop melalui elemen dalam koleksi
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


# Definisi function dengan nama dan parameter
def demo_pretrained_models_info():
    """
    Informasi tentang berbagai pre-trained models.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("PRE-TRAINED MODELS UNTUK TRANSFER LEARNING")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Assignment - set nilai ke variabel
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
    
    # Iterasi/loop melalui elemen dalam koleksi
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


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM TRANSFER LEARNING")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
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
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-5): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_pretrained_models_info()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            # Conditional statement - eksekusi jika kondisi True
            if PYTORCH_AVAILABLE:
                demo_transfer_learning_pytorch()
            else:
                print("[ERROR] PyTorch tidak tersedia")
                demo_transfer_learning_simulation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            # Conditional statement - eksekusi jika kondisi True
            if TENSORFLOW_AVAILABLE:
                demo_transfer_learning_keras()
            else:
                print("[ERROR] TensorFlow tidak tersedia")
                demo_transfer_learning_simulation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_transfer_learning_simulation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_pretrained_models_info()
            demo_transfer_learning_simulation()
            # Conditional statement - eksekusi jika kondisi True
            if PYTORCH_AVAILABLE:
                demo_transfer_learning_pytorch()
            # Conditional statement - eksekusi jika kondisi True
            if TENSORFLOW_AVAILABLE:
                demo_transfer_learning_keras()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
