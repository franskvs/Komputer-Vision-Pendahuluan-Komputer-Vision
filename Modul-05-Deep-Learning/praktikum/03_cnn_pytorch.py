"""
# Assignment - set nilai ke variabel
=============================================================================
PRAKTIKUM 03 - CONVOLUTIONAL NEURAL NETWORK DENGAN PYTORCH
# Assignment - set nilai ke variabel
=============================================================================
Program ini membangun dan melatih CNN dari awal menggunakan PyTorch.
Kita akan menggunakan dataset MNIST untuk klasifikasi digit handwritten.

Konsep yang dipelajari:
1. Definisi arsitektur CNN dengan nn.Module
2. Forward pass dan backward pass
3. Training loop dengan optimizer
4. Evaluasi model dengan accuracy
5. Visualisasi training progress

Arsitektur yang dibangun:
- 2 Convolutional layers
- 2 MaxPooling layers
- 2 Fully Connected layers
- ReLU activation

Kebutuhan:
# Assignment - set nilai ke variabel
- torch >= 2.0.0
- torchvision
- numpy
- matplotlib

Note: Jika PyTorch tidak tersedia, program akan menjalankan simulasi.

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

# Check apakah PyTorch tersedia
PYTORCH_AVAILABLE = False
# Blok try-except untuk error handling
try:
    # Import library/module untuk digunakan
    import torch
    # Import library/module untuk digunakan
    import torch.nn as nn
    # Import library/module untuk digunakan
    import torch.optim as optim
    # Import library/module untuk digunakan
    import torch.nn.functional as F
    # Import library/module untuk digunakan
    from torch.utils.data import DataLoader
    # Import library/module untuk digunakan
    import torchvision
    # Import library/module untuk digunakan
    import torchvision.transforms as transforms
    # Assignment - set nilai ke variabel
    PYTORCH_AVAILABLE = True
    print("[INFO] PyTorch tersedia - menggunakan real implementation")
# Tangkap exception jika ada error di blok try
except ImportError:
    print("[WARNING] PyTorch tidak tersedia - menggunakan simulasi")


# =============================================================================
# DEFINISI ARSITEKTUR CNN
# =============================================================================

# Conditional statement - eksekusi jika kondisi True
if PYTORCH_AVAILABLE:
    # Definisi class untuk membuat object
    class SimpleCNN(nn.Module):
        """
        CNN sederhana untuk klasifikasi MNIST.
        
        Arsitektur:
        - Conv1: 1 → 32 channels, 3×3 kernel
        - MaxPool: 2×2
        - Conv2: 32 → 64 channels, 3×3 kernel  
        - MaxPool: 2×2
        - FC1: 1600 → 128
        - FC2: 128 → 10 (output classes)
        
        Input: 28×28×1 grayscale image
        # Definisi class untuk membuat object
        Output: 10 class probabilities
        """
        
        # Definisi function dengan nama dan parameter
        def __init__(self, num_classes=10):
            """
            Inisialisasi layers CNN.
            
            Args:
                # Definisi class untuk membuat object
                num_classes: Jumlah class output (default: 10 untuk MNIST)
            """
            super(SimpleCNN, self).__init__()
            
            # =============================================================
            # CONVOLUTIONAL LAYERS
            # =============================================================
            
            # Layer 1: Convolutional
            # Input: 1×28×28 (grayscale)
            # Output: 32×26×26 (setelah conv 3×3 tanpa padding)
            self.conv1 = nn.Conv2d(
                # Assignment - set nilai ke variabel
                in_channels=1,       # Input channels (grayscale = 1)
                # Assignment - set nilai ke variabel
                out_channels=32,     # Number of filters
                # Assignment - set nilai ke variabel
                kernel_size=3,       # 3×3 filter
                # Assignment - set nilai ke variabel
                padding=1            # Same padding
            )
            # Output setelah conv1: 32×28×28
            
            # Layer 2: Convolutional
            # Input: 32×14×14 (setelah pooling)
            # Output: 64×14×14
            self.conv2 = nn.Conv2d(
                # Assignment - set nilai ke variabel
                in_channels=32,
                # Assignment - set nilai ke variabel
                out_channels=64,
                # Assignment - set nilai ke variabel
                kernel_size=3,
                # Assignment - set nilai ke variabel
                padding=1
            )
            # Output setelah conv2: 64×14×14
            
            # =============================================================
            # POOLING LAYERS
            # =============================================================
            
            # Max Pooling: reduce spatial dimensions by 2
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
            
            # =============================================================
            # FULLY CONNECTED LAYERS
            # =============================================================
            
            # Setelah 2 pooling layers: 28 → 14 → 7
            # Feature map size: 64 × 7 × 7 = 3136
            self.fc1 = nn.Linear(64 * 7 * 7, 128)
            # Assignment - set nilai ke variabel
            self.fc2 = nn.Linear(128, num_classes)
            
            # Dropout untuk regularization
            self.dropout = nn.Dropout(0.25)
        
        # Definisi function dengan nama dan parameter
        def forward(self, x):
            """
            Forward pass melalui network.
            
            Args:
                x: Input tensor shape (batch, 1, 28, 28)
                
            Returns:
                Output logits shape (batch, 10)
            """
            # Layer 1: Conv → ReLU → Pool
            # x: (batch, 1, 28, 28) → (batch, 32, 28, 28) → (batch, 32, 14, 14)
            x = self.pool(F.relu(self.conv1(x)))
            
            # Layer 2: Conv → ReLU → Pool
            # x: (batch, 32, 14, 14) → (batch, 64, 14, 14) → (batch, 64, 7, 7)
            x = self.pool(F.relu(self.conv2(x)))
            
            # Flatten: (batch, 64, 7, 7) → (batch, 3136)
            x = x.view(-1, 64 * 7 * 7)
            
            # Fully connected layers
            x = self.dropout(x)
            # Assignment - set nilai ke variabel
            x = F.relu(self.fc1(x))
            # Assignment - set nilai ke variabel
            x = self.dropout(x)
            # Assignment - set nilai ke variabel
            x = self.fc2(x)  # No activation (raw logits)
            
            # Return value dari function
            return x


# Definisi function dengan nama dan parameter
def print_architecture():
    """
    Menampilkan arsitektur CNN dalam format visual.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("ARSITEKTUR CNN")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    ┌─────────────────────────────────────────────────────────────────┐
    │                    SimpleCNN Architecture                        │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  Input Layer                                                     │
    │  └─ Shape: (batch, 1, 28, 28) ─ Grayscale MNIST images          │
    │                        │                                         │
    │                        ▼                                         │
    │  ┌───────────────────────────────────────┐                      │
    # Assignment - set nilai ke variabel
    │  │ Conv2D(1→32, kernel=3×3, padding=1)   │                      │
    │  │ Output: (batch, 32, 28, 28)           │                      │
    # Assignment - set nilai ke variabel
    │  │ Parameters: 1×3×3×32 + 32 = 320       │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ ReLU Activation                       │                      │
    │  │ Output: (batch, 32, 28, 28)           │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    # Assignment - set nilai ke variabel
    │  │ MaxPool2D(kernel=2×2, stride=2)       │                      │
    │  │ Output: (batch, 32, 14, 14)           │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    # Assignment - set nilai ke variabel
    │  │ Conv2D(32→64, kernel=3×3, padding=1)  │                      │
    │  │ Output: (batch, 64, 14, 14)           │                      │
    # Assignment - set nilai ke variabel
    │  │ Parameters: 32×3×3×64 + 64 = 18,496   │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ ReLU Activation                       │                      │
    │  │ Output: (batch, 64, 14, 14)           │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    # Assignment - set nilai ke variabel
    │  │ MaxPool2D(kernel=2×2, stride=2)       │                      │
    │  │ Output: (batch, 64, 7, 7)             │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ Flatten                               │                      │
    │  │ Output: (batch, 3136)                 │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ Dropout(0.25)                         │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ Linear(3136 → 128)                    │                      │
    # Assignment - set nilai ke variabel
    │  │ Parameters: 3136×128 + 128 = 401,536  │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ ReLU Activation                       │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ Dropout(0.25)                         │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    │  ┌───────────────────────────────────────┐                      │
    │  │ Linear(128 → 10)                      │                      │
    # Assignment - set nilai ke variabel
    │  │ Parameters: 128×10 + 10 = 1,290       │                      │
    │  └───────────────────┬───────────────────┘                      │
    │                      ▼                                           │
    # Iterasi/loop melalui elemen dalam koleksi
    │  Output: (batch, 10) ─ Logits for 10 digit classes              │
    │                                                                  │
    │  Total Parameters: ~421,642                                      │
    └─────────────────────────────────────────────────────────────────┘
    """)


# Definisi function dengan nama dan parameter
def demo_training_pytorch():
    """
    Demonstrasi training CNN dengan PyTorch pada dataset MNIST.
    """
    # Conditional statement - eksekusi jika kondisi True
    if not PYTORCH_AVAILABLE:
        print("[ERROR] PyTorch tidak tersedia. Gunakan demo_training_simulation()")
        return
    
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("TRAINING CNN DENGAN PYTORCH")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # ==========================================================================
    # SETUP
    # ==========================================================================
    
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n[INFO] Using device: {device}")
    
    # Hyperparameters
    num_epochs = 5
    # Assignment - set nilai ke variabel
    batch_size = 64
    # Assignment - set nilai ke variabel
    learning_rate = 0.001
    
    print(f"[INFO] Hyperparameters:")
    print(f"       - Epochs: {num_epochs}")
    print(f"       - Batch size: {batch_size}")
    print(f"       - Learning rate: {learning_rate}")
    
    # ==========================================================================
    # DATA LOADING
    # ==========================================================================
    
    print("\n[INFO] Loading MNIST dataset...")
    
    # Transforms untuk preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(),  # Convert to tensor [0, 1]
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST mean & std
    ])
    
    # Download dan load dataset
    try:
        # Assignment - set nilai ke variabel
        train_dataset = torchvision.datasets.MNIST(
            # Assignment - set nilai ke variabel
            root='./data',
            # Assignment - set nilai ke variabel
            train=True,
            # Assignment - set nilai ke variabel
            transform=transform,
            # Assignment - set nilai ke variabel
            download=True
        )
        
        # Assignment - set nilai ke variabel
        test_dataset = torchvision.datasets.MNIST(
            # Assignment - set nilai ke variabel
            root='./data',
            # Assignment - set nilai ke variabel
            train=False,
            # Assignment - set nilai ke variabel
            transform=transform
        )
        
        # DataLoaders
        train_loader = DataLoader(
            # Assignment - set nilai ke variabel
            dataset=train_dataset,
            # Assignment - set nilai ke variabel
            batch_size=batch_size,
            # Assignment - set nilai ke variabel
            shuffle=True
        )
        
        # Assignment - set nilai ke variabel
        test_loader = DataLoader(
            # Assignment - set nilai ke variabel
            dataset=test_dataset,
            # Assignment - set nilai ke variabel
            batch_size=batch_size,
            # Assignment - set nilai ke variabel
            shuffle=False
        )
        
        print(f"[INFO] Training samples: {len(train_dataset)}")
        print(f"[INFO] Test samples: {len(test_dataset)}")
        print(f"[INFO] Training batches: {len(train_loader)}")
        
    # Tangkap exception jika ada error di blok try
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        print("[INFO] Running simulation instead...")
        demo_training_simulation()
        return
    
    # ==========================================================================
    # MODEL INITIALIZATION
    # ==========================================================================
    
    print("\n[INFO] Initializing model...")
    # Assignment - set nilai ke variabel
    model = SimpleCNN(num_classes=10).to(device)
    
    # Print model summary
    total_params = sum(p.numel() for p in model.parameters())
    # Iterasi/loop melalui elemen dalam koleksi
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[INFO] Total parameters: {total_params:,}")
    print(f"[INFO] Trainable parameters: {trainable_params:,}")
    
    # Loss function dan optimizer
    criterion = nn.CrossEntropyLoss()
    # Assignment - set nilai ke variabel
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # ==========================================================================
    # TRAINING LOOP
    # ==========================================================================
    
    print("\n[INFO] Starting training...")
    print("-"*60)
    
    # Assignment - set nilai ke variabel
    train_losses = []
    # Assignment - set nilai ke variabel
    train_accuracies = []
    
    # Iterasi/loop melalui elemen dalam koleksi
    for epoch in range(num_epochs):
        model.train()  # Set ke training mode
        # Assignment - set nilai ke variabel
        running_loss = 0.0
        # Assignment - set nilai ke variabel
        correct = 0
        # Assignment - set nilai ke variabel
        total = 0
        
        # Iterasi/loop melalui elemen dalam koleksi
        for i, (images, labels) in enumerate(train_loader):
            # Move data ke device
            images = images.to(device)
            # Assignment - set nilai ke variabel
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(images)
            # Assignment - set nilai ke variabel
            loss = criterion(outputs, labels)
            
            # Backward pass dan optimization
            optimizer.zero_grad()  # Clear gradients
            loss.backward()        # Compute gradients
            optimizer.step()       # Update weights
            
            # Statistics
            running_loss += loss.item()
            # Assignment - set nilai ke variabel
            _, predicted = torch.max(outputs.data, 1)
            # Assignment - set nilai ke variabel
            total += labels.size(0)
            # Assignment - set nilai ke variabel
            correct += (predicted == labels).sum().item()
            
            # Print progress setiap 100 batch
            if (i + 1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], '
                      f'Step [{i+1}/{len(train_loader)}], '
                      f'Loss: {loss.item():.4f}')
        
        # Epoch statistics
        epoch_loss = running_loss / len(train_loader)
        # Assignment - set nilai ke variabel
        epoch_acc = 100 * correct / total
        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_acc)
        
        print(f'\nEpoch [{epoch+1}/{num_epochs}] Summary:')
        print(f'  Training Loss: {epoch_loss:.4f}')
        print(f'  Training Accuracy: {epoch_acc:.2f}%')
        print("-"*60)
    
    # ==========================================================================
    # EVALUATION
    # ==========================================================================
    
    print("\n[INFO] Evaluating on test set...")
    
    model.eval()  # Set ke evaluation mode
    # Assignment - set nilai ke variabel
    correct = 0
    # Assignment - set nilai ke variabel
    total = 0
    
    with torch.no_grad():  # Disable gradient computation
        # Iterasi/loop melalui elemen dalam koleksi
        for images, labels in test_loader:
            # Assignment - set nilai ke variabel
            images = images.to(device)
            # Assignment - set nilai ke variabel
            labels = labels.to(device)
            
            # Assignment - set nilai ke variabel
            outputs = model(images)
            # Assignment - set nilai ke variabel
            _, predicted = torch.max(outputs.data, 1)
            
            # Assignment - set nilai ke variabel
            total += labels.size(0)
            # Assignment - set nilai ke variabel
            correct += (predicted == labels).sum().item()
    
    # Assignment - set nilai ke variabel
    test_accuracy = 100 * correct / total
    print(f'\n[RESULT] Test Accuracy: {test_accuracy:.2f}%')
    
    # ==========================================================================
    # SAVE MODEL
    # ==========================================================================
    
    # Assignment - set nilai ke variabel
    save_path = 'mnist_cnn.pth'
    torch.save(model.state_dict(), save_path)
    print(f"\n[INFO] Model saved to {save_path}")
    
    # Print training history
    print("\n[INFO] Training History:")
    print("-"*40)
    # Iterasi/loop melalui elemen dalam koleksi
    for i, (loss, acc) in enumerate(zip(train_losses, train_accuracies)):
        # Assignment - set nilai ke variabel
        bar = "█" * int(acc / 5)
        # Assignment - set nilai ke variabel
        print(f"Epoch {i+1}: Loss={loss:.4f}, Acc={acc:.2f}% {bar}")


# Definisi function dengan nama dan parameter
def demo_training_simulation():
    """
    Simulasi training CNN tanpa PyTorch.
    Berguna untuk memahami konsep tanpa dependency.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("SIMULASI TRAINING CNN")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("\n[INFO] Mode simulasi - tanpa PyTorch")
    print("[INFO] Nilai-nilai berikut adalah simulasi untuk demonstrasi")
    
    # Simulated training progress
    epochs = 5
    # Assignment - set nilai ke variabel
    simulated_results = [
        {"loss": 0.4523, "train_acc": 85.2, "val_acc": 87.1},
        {"loss": 0.2134, "train_acc": 92.3, "val_acc": 93.5},
        {"loss": 0.1256, "train_acc": 95.8, "val_acc": 96.2},
        {"loss": 0.0892, "train_acc": 97.1, "val_acc": 97.4},
        {"loss": 0.0654, "train_acc": 98.0, "val_acc": 97.8},
    ]
    
    print("\n[TRAINING PROGRESS]")
    print("-"*60)
    print(f"{'Epoch':<8} {'Loss':<12} {'Train Acc':<12} {'Val Acc':<12}")
    print("-"*60)
    
    # Iterasi/loop melalui elemen dalam koleksi
    for i, result in enumerate(simulated_results, 1):
        print(f"{i:<8} {result['loss']:<12.4f} {result['train_acc']:<12.1f}% "
              f"{result['val_acc']:<12.1f}%")
    
    print("-"*60)
    
    # Visualisasi ASCII
    print("\n[TRAINING CURVE - ASCII]")
    print("Loss over epochs:")
    # Iterasi/loop melalui elemen dalam koleksi
    for i, result in enumerate(simulated_results, 1):
        # Assignment - set nilai ke variabel
        bar_length = int((1 - result['loss']) * 40)
        # Assignment - set nilai ke variabel
        bar = "█" * bar_length
        print(f"Epoch {i}: {bar} {result['loss']:.4f}")
    
    print("\nAccuracy over epochs:")
    # Iterasi/loop melalui elemen dalam koleksi
    for i, result in enumerate(simulated_results, 1):
        # Assignment - set nilai ke variabel
        bar_length = int(result['train_acc'] / 2.5)
        # Assignment - set nilai ke variabel
        bar = "█" * bar_length
        print(f"Epoch {i}: {bar} {result['train_acc']:.1f}%")
    
    # Confusion matrix simulasi
    print("\n[SIMULATED CONFUSION MATRIX] (Test Set)")
    print("-"*50)
    
    # Generate random-ish confusion matrix dengan diagonal dominant
    np.random.seed(42)
    # Generate random integer dalam range tertentu
    cm = np.random.randint(0, 20, (10, 10))
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(10):
        # Generate random integer dalam range tertentu
        cm[i, i] = np.random.randint(80, 100)  # High diagonal
    
    # Iterasi/loop melalui elemen dalam koleksi
    print("    " + "".join([f"{i:>5}" for i in range(10)]))
    print("    " + "-"*50)
    # Iterasi/loop melalui elemen dalam koleksi
    for i in range(10):
        # Assignment - set nilai ke variabel
        row_str = f"{i:>2} |"
        # Iterasi/loop melalui elemen dalam koleksi
        for j in range(10):
            # Assignment - set nilai ke variabel
            row_str += f"{cm[i,j]:>5}"
        print(row_str)
    
    print("\n[RESULT] Simulated Test Accuracy: 97.8%")


# Definisi function dengan nama dan parameter
def demo_forward_pass():
    """
    Demonstrasi forward pass step by step.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DEMONSTRASI FORWARD PASS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Conditional statement - eksekusi jika kondisi True
    if PYTORCH_AVAILABLE:
        # Create model dan dummy input
        model = SimpleCNN()
        model.eval()
        
        # Dummy input: batch of 1, grayscale, 28x28
        x = torch.randn(1, 1, 28, 28)
        
        print("\n[INFO] Tracing forward pass dengan hooks...")
        
        # Hook untuk capture intermediate outputs
        activations = {}
        
        # Definisi function dengan nama dan parameter
        def get_activation(name):
            # Definisi function dengan nama dan parameter
            def hook(model, input, output):
                # Assignment - set nilai ke variabel
                activations[name] = output.detach()
            # Return value dari function
            return hook
        
        # Register hooks
        model.conv1.register_forward_hook(get_activation('conv1'))
        model.conv2.register_forward_hook(get_activation('conv2'))
        model.fc1.register_forward_hook(get_activation('fc1'))
        model.fc2.register_forward_hook(get_activation('fc2'))
        
        # Forward pass
        with torch.no_grad():
            # Assignment - set nilai ke variabel
            output = model(x)
        
        # Print shapes
        print(f"\nInput shape: {x.shape}")
        print(f"After conv1: {activations['conv1'].shape}")
        print(f"After pool1: {model.pool(F.relu(activations['conv1'])).shape}")
        print(f"After conv2: {activations['conv2'].shape}")
        print(f"After pool2: {model.pool(F.relu(activations['conv2'])).shape}")
        print(f"After fc1: {activations['fc1'].shape}")
        print(f"Output (fc2): {activations['fc2'].shape}")
        
        # Output probabilities
        probabilities = F.softmax(output, dim=1)
        print(f"\nOutput logits: {output[0].numpy()}")
        print(f"Probabilities: {probabilities[0].numpy()}")
        print(f"Predicted class: {torch.argmax(probabilities).item()}")
        
    else:
        # Simulasi forward pass
        print("\n[SIMULASI] Forward pass tanpa PyTorch")
        print("""
        Input: (1, 1, 28, 28)
                │
                ▼
        Conv1 + ReLU: (1, 32, 28, 28)
                │
                ▼
        MaxPool: (1, 32, 14, 14)
                │
                ▼
        Conv2 + ReLU: (1, 64, 14, 14)
                │
                ▼
        MaxPool: (1, 64, 7, 7)
                │
                ▼
        Flatten: (1, 3136)
                │
                ▼
        FC1 + ReLU: (1, 128)
                │
                ▼
        FC2: (1, 10)
                │
                ▼
        Output logits: [0.23, -1.45, 2.31, ...]
        Softmax: [0.05, 0.01, 0.42, ...]
        Predicted: Class 2
        """)


# Definisi function dengan nama dan parameter
def demo_backpropagation():
    """
    Demonstrasi konsep backpropagation.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("KONSEP BACKPROPAGATION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [FORWARD PASS]
    ─────────────────────────────────────────────────────────────────────
    
    Input x → Layer 1 → Layer 2 → ... → Output ŷ → Loss L
         ↓         ↓         ↓                ↓
        h₁        h₂        ...           Prediction
    
    # Assignment - set nilai ke variabel
    L = CrossEntropy(ŷ, y) = -Σ yᵢ log(ŷᵢ)
    
    
    [BACKWARD PASS - Chain Rule]
    ─────────────────────────────────────────────────────────────────────
    
    Gradient flows backward:
    
    # Assignment - set nilai ke variabel
    ∂L/∂w₁ = ∂L/∂ŷ × ∂ŷ/∂hₙ × ... × ∂h₂/∂h₁ × ∂h₁/∂w₁
    
                    ∂L/∂ŷ ← Loss derivative
                       ↓
    Output ← ... ← Layer 2 ← Layer 1 ← Input
                       ↓
                  Gradients
                   ∂L/∂w
    
    
    [WEIGHT UPDATE - Gradient Descent]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    w_new = w_old - η × ∂L/∂w
    
    Dimana η adalah learning rate
    
    
    [OPTIMIZER VARIANTS]
    ─────────────────────────────────────────────────────────────────────
    
    # Assignment - set nilai ke variabel
    SGD:    w = w - η × ∇L
    
    Momentum:
            # Assignment - set nilai ke variabel
            v = β × v + ∇L
            # Assignment - set nilai ke variabel
            w = w - η × v
    
    Adam (Adaptive Moment):
            # Assignment - set nilai ke variabel
            m = β₁ × m + (1-β₁) × ∇L           # First moment
            # Assignment - set nilai ke variabel
            v = β₂ × v + (1-β₂) × (∇L)²        # Second moment
            # Assignment - set nilai ke variabel
            w = w - η × m / (√v + ε)
    """)
    
    # Conditional statement - eksekusi jika kondisi True
    if PYTORCH_AVAILABLE:
        print("\n[DEMO] PyTorch Autograd")
        print("-"*50)
        
        # Simple example
        x = torch.tensor([2.0], requires_grad=True)
        # Buat tensor PyTorch dari data
        w = torch.tensor([3.0], requires_grad=True)
        
        # Forward
        y = w * x  # y = 3 * 2 = 6
        # Assignment - set nilai ke variabel
        loss = (y - 10) ** 2  # (6 - 10)^2 = 16
        
        # Assignment - set nilai ke variabel
        print(f"x = {x.item()}, w = {w.item()}")
        # Assignment - set nilai ke variabel
        print(f"y = w * x = {y.item()}")
        # Assignment - set nilai ke variabel
        print(f"Loss = (y - 10)² = {loss.item()}")
        
        # Backward
        loss.backward()
        
        # Assignment - set nilai ke variabel
        print(f"\n∂Loss/∂w = {w.grad.item()}")
        # Assignment - set nilai ke variabel
        print(f"∂Loss/∂x = {x.grad.item()}")
        
        # Manual verification
        # loss = (wx - 10)^2
        # ∂loss/∂w = 2(wx - 10) * x = 2(6-10)*2 = -16
        print(f"\nVerification: 2*(6-10)*2 = {2*(6-10)*2}")


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    print("PRAKTIKUM CNN DENGAN PYTORCH")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Conditional statement - eksekusi jika kondisi True
    if PYTORCH_AVAILABLE:
        print(f"\n[INFO] PyTorch version: {torch.__version__}")
        print(f"[INFO] CUDA available: {torch.cuda.is_available()}")
        # Conditional statement - eksekusi jika kondisi True
        if torch.cuda.is_available():
            print(f"[INFO] CUDA device: {torch.cuda.get_device_name(0)}")
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Tampilkan Arsitektur CNN")
        print("2. Training CNN (PyTorch/Simulasi)")
        print("3. Demo Forward Pass")
        print("4. Konsep Backpropagation")
        print("5. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-5): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            print_architecture()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            # Conditional statement - eksekusi jika kondisi True
            if PYTORCH_AVAILABLE:
                demo_training_pytorch()
            else:
                demo_training_simulation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_forward_pass()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_backpropagation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            print_architecture()
            # Conditional statement - eksekusi jika kondisi True
            if PYTORCH_AVAILABLE:
                demo_training_pytorch()
            else:
                demo_training_simulation()
            demo_forward_pass()
            demo_backpropagation()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
