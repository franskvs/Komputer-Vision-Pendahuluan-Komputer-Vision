"""
PRAKTIKUM BAB 5: DEEP LEARNING UNTUK COMPUTER VISION
====================================================

Tujuan:
1. Memahami dasar neural networks dan backpropagation
2. Mengimplementasikan CNN dari scratch dan dengan framework
3. Training model untuk image classification
4. Transfer learning dengan pretrained models

Kebutuhan:
- Python 3.8+
- PyTorch atau TensorFlow
- torchvision
- NumPy
- Matplotlib

Instalasi:
pip install torch torchvision numpy matplotlib tqdm
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Check if PyTorch is available
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, Dataset
    import torchvision
    import torchvision.transforms as transforms
    from torchvision import models
    TORCH_AVAILABLE = True
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not installed. Install with: pip install torch torchvision")

# ============================================================
# BAGIAN 1: NEURAL NETWORK FROM SCRATCH (NumPy)
# ============================================================

print("=" * 60)
print("BAGIAN 1: NEURAL NETWORK FROM SCRATCH")
print("=" * 60)

class NeuralNetworkNumPy:
    """
    Simple 2-layer neural network implemented with NumPy
    For understanding backpropagation
    """
    
    def __init__(self, input_size, hidden_size, output_size):
        """Initialize weights with Xavier initialization"""
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))
    
    def relu(self, x):
        """ReLU activation"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Derivative of ReLU"""
        return (x > 0).astype(float)
    
    def softmax(self, x):
        """Softmax for output layer"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        """Forward pass"""
        # Layer 1
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)
        
        # Layer 2 (output)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.softmax(self.z2)
        
        return self.a2
    
    def cross_entropy_loss(self, y_pred, y_true):
        """Cross-entropy loss"""
        n_samples = y_true.shape[0]
        # Clip untuk numerical stability
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
        loss = -np.sum(y_true * np.log(y_pred)) / n_samples
        return loss
    
    def backward(self, X, y_true, learning_rate=0.01):
        """Backward pass (backpropagation)"""
        n_samples = X.shape[0]
        
        # Output layer gradient
        dz2 = self.a2 - y_true  # Derivative of softmax + cross-entropy
        dW2 = (self.a1.T @ dz2) / n_samples
        db2 = np.sum(dz2, axis=0, keepdims=True) / n_samples
        
        # Hidden layer gradient
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.relu_derivative(self.z1)
        dW1 = (X.T @ dz1) / n_samples
        db1 = np.sum(dz1, axis=0, keepdims=True) / n_samples
        
        # Update weights
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
    
    def train(self, X, y, epochs=1000, learning_rate=0.1, verbose=True):
        """Training loop"""
        losses = []
        
        for epoch in range(epochs):
            # Forward
            y_pred = self.forward(X)
            
            # Loss
            loss = self.cross_entropy_loss(y_pred, y)
            losses.append(loss)
            
            # Backward
            self.backward(X, y, learning_rate)
            
            if verbose and (epoch + 1) % 100 == 0:
                acc = self.accuracy(X, np.argmax(y, axis=1))
                print(f"Epoch {epoch+1}/{epochs}, Loss: {loss:.4f}, Acc: {acc:.2%}")
        
        return losses
    
    def predict(self, X):
        """Predict class labels"""
        probs = self.forward(X)
        return np.argmax(probs, axis=1)
    
    def accuracy(self, X, y_true):
        """Calculate accuracy"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y_true)


def demo_numpy_nn():
    """Demo neural network from scratch"""
    print("\n📊 Demo: Neural Network from Scratch (NumPy)\n")
    
    # Generate synthetic data (XOR problem - not linearly separable)
    np.random.seed(42)
    n_samples = 200
    
    # Create 4 clusters
    X = np.vstack([
        np.random.randn(n_samples//4, 2) + [0, 0],
        np.random.randn(n_samples//4, 2) + [2, 2],
        np.random.randn(n_samples//4, 2) + [0, 2],
        np.random.randn(n_samples//4, 2) + [2, 0]
    ])
    
    # XOR labels
    y_labels = np.array([0]*(n_samples//4) + [0]*(n_samples//4) + 
                        [1]*(n_samples//4) + [1]*(n_samples//4))
    
    # One-hot encoding
    y_onehot = np.zeros((n_samples, 2))
    y_onehot[np.arange(n_samples), y_labels] = 1
    
    # Create and train network
    nn = NeuralNetworkNumPy(input_size=2, hidden_size=8, output_size=2)
    losses = nn.train(X, y_onehot, epochs=1000, learning_rate=0.5)
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Loss curve
    axes[0].plot(losses)
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training Loss')
    axes[0].grid(True, alpha=0.3)
    
    # Decision boundary
    xx, yy = np.meshgrid(np.linspace(-2, 4, 100), np.linspace(-2, 4, 100))
    Z = nn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    axes[1].contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    axes[1].scatter(X[y_labels==0, 0], X[y_labels==0, 1], c='blue', label='Class 0')
    axes[1].scatter(X[y_labels==1, 0], X[y_labels==1, 1], c='red', label='Class 1')
    axes[1].set_xlabel('X1')
    axes[1].set_ylabel('X2')
    axes[1].set_title(f'Decision Boundary (Acc: {nn.accuracy(X, y_labels):.2%})')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('output_numpy_nn.png', dpi=150)
    plt.show()
    
    print("✅ NumPy Neural Network demo selesai!")


# ============================================================
# BAGIAN 2: CNN DENGAN PYTORCH
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 2: CNN DENGAN PYTORCH")
print("=" * 60)

if TORCH_AVAILABLE:
    
    class SimpleCNN(nn.Module):
        """Simple CNN for CIFAR-10 classification"""
        
        def __init__(self, num_classes=10):
            super(SimpleCNN, self).__init__()
            
            # Convolutional layers
            self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
            self.bn1 = nn.BatchNorm2d(32)
            
            self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
            self.bn2 = nn.BatchNorm2d(64)
            
            self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
            self.bn3 = nn.BatchNorm2d(128)
            
            # Pooling
            self.pool = nn.MaxPool2d(2, 2)
            
            # Fully connected layers
            self.fc1 = nn.Linear(128 * 4 * 4, 256)
            self.fc2 = nn.Linear(256, num_classes)
            
            # Dropout
            self.dropout = nn.Dropout(0.5)
        
        def forward(self, x):
            # Conv block 1
            x = self.pool(F.relu(self.bn1(self.conv1(x))))  # 32x32 -> 16x16
            
            # Conv block 2
            x = self.pool(F.relu(self.bn2(self.conv2(x))))  # 16x16 -> 8x8
            
            # Conv block 3
            x = self.pool(F.relu(self.bn3(self.conv3(x))))  # 8x8 -> 4x4
            
            # Flatten
            x = x.view(x.size(0), -1)
            
            # FC layers
            x = self.dropout(F.relu(self.fc1(x)))
            x = self.fc2(x)
            
            return x
    
    
    class ResidualBlock(nn.Module):
        """Basic Residual Block"""
        
        def __init__(self, in_channels, out_channels, stride=1):
            super(ResidualBlock, self).__init__()
            
            self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
            self.bn1 = nn.BatchNorm2d(out_channels)
            self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
            self.bn2 = nn.BatchNorm2d(out_channels)
            
            # Shortcut connection
            self.shortcut = nn.Sequential()
            if stride != 1 or in_channels != out_channels:
                self.shortcut = nn.Sequential(
                    nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
                    nn.BatchNorm2d(out_channels)
                )
        
        def forward(self, x):
            out = F.relu(self.bn1(self.conv1(x)))
            out = self.bn2(self.conv2(out))
            out += self.shortcut(x)  # Skip connection
            out = F.relu(out)
            return out
    
    
    class SimpleResNet(nn.Module):
        """Simple ResNet-like architecture"""
        
        def __init__(self, num_classes=10):
            super(SimpleResNet, self).__init__()
            
            self.conv1 = nn.Conv2d(3, 32, 3, 1, 1, bias=False)
            self.bn1 = nn.BatchNorm2d(32)
            
            self.layer1 = self._make_layer(32, 64, 2, stride=1)
            self.layer2 = self._make_layer(64, 128, 2, stride=2)
            self.layer3 = self._make_layer(128, 256, 2, stride=2)
            
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
            self.fc = nn.Linear(256, num_classes)
        
        def _make_layer(self, in_channels, out_channels, num_blocks, stride):
            layers = []
            layers.append(ResidualBlock(in_channels, out_channels, stride))
            for _ in range(1, num_blocks):
                layers.append(ResidualBlock(out_channels, out_channels))
            return nn.Sequential(*layers)
        
        def forward(self, x):
            x = F.relu(self.bn1(self.conv1(x)))
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            x = self.avgpool(x)
            x = x.view(x.size(0), -1)
            x = self.fc(x)
            return x
    
    
    def train_epoch(model, train_loader, criterion, optimizer, device):
        """Train for one epoch"""
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
        
        return running_loss / len(train_loader), correct / total
    
    
    def evaluate(model, test_loader, criterion, device):
        """Evaluate model"""
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        
        return running_loss / len(test_loader), correct / total
    
    
    def demo_pytorch_cnn():
        """Demo CNN dengan PyTorch pada CIFAR-10"""
        print("\n📊 Demo: CNN dengan PyTorch (CIFAR-10)\n")
        
        # Device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # Data augmentation
        transform_train = transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        ])
        
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        ])
        
        # Load CIFAR-10
        print("Loading CIFAR-10 dataset...")
        trainset = torchvision.datasets.CIFAR10(
            root='./data', train=True, download=True, transform=transform_train)
        testset = torchvision.datasets.CIFAR10(
            root='./data', train=False, download=True, transform=transform_test)
        
        # Use smaller subset for demo
        train_subset = torch.utils.data.Subset(trainset, range(5000))
        test_subset = torch.utils.data.Subset(testset, range(1000))
        
        train_loader = DataLoader(train_subset, batch_size=64, shuffle=True, num_workers=0)
        test_loader = DataLoader(test_subset, batch_size=64, shuffle=False, num_workers=0)
        
        classes = ('plane', 'car', 'bird', 'cat', 'deer', 
                   'dog', 'frog', 'horse', 'ship', 'truck')
        
        # Create model
        model = SimpleCNN(num_classes=10).to(device)
        print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
        
        # Training
        n_epochs = 15
        train_losses, train_accs = [], []
        test_losses, test_accs = [], []
        
        print("\nTraining...")
        for epoch in range(n_epochs):
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            test_loss, test_acc = evaluate(model, test_loader, criterion, device)
            scheduler.step()
            
            train_losses.append(train_loss)
            train_accs.append(train_acc)
            test_losses.append(test_loss)
            test_accs.append(test_acc)
            
            print(f"Epoch {epoch+1}/{n_epochs}: "
                  f"Train Loss={train_loss:.4f}, Train Acc={train_acc:.2%}, "
                  f"Test Loss={test_loss:.4f}, Test Acc={test_acc:.2%}")
        
        # Visualize training
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        axes[0].plot(train_losses, label='Train')
        axes[0].plot(test_losses, label='Test')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].set_title('Training and Test Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(train_accs, label='Train')
        axes[1].plot(test_accs, label='Test')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Accuracy')
        axes[1].set_title('Training and Test Accuracy')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('output_pytorch_cnn_training.png', dpi=150)
        plt.show()
        
        # Visualize predictions
        visualize_predictions(model, test_loader, classes, device)
        
        print("✅ PyTorch CNN demo selesai!")
        return model
    
    
    def visualize_predictions(model, test_loader, classes, device, n_samples=16):
        """Visualize model predictions"""
        model.eval()
        
        # Get a batch
        dataiter = iter(test_loader)
        images, labels = next(dataiter)
        images, labels = images[:n_samples], labels[:n_samples]
        
        # Predict
        with torch.no_grad():
            outputs = model(images.to(device))
            _, predicted = torch.max(outputs, 1)
        
        # Denormalize
        mean = torch.tensor([0.4914, 0.4822, 0.4465]).view(3, 1, 1)
        std = torch.tensor([0.2023, 0.1994, 0.2010]).view(3, 1, 1)
        images = images * std + mean
        images = images.clamp(0, 1)
        
        # Plot
        fig, axes = plt.subplots(4, 4, figsize=(12, 12))
        
        for idx, ax in enumerate(axes.flat):
            img = images[idx].permute(1, 2, 0).numpy()
            ax.imshow(img)
            
            pred_label = classes[predicted[idx]]
            true_label = classes[labels[idx]]
            color = 'green' if pred_label == true_label else 'red'
            
            ax.set_title(f'Pred: {pred_label}\nTrue: {true_label}', color=color)
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig('output_cnn_predictions.png', dpi=150)
        plt.show()


# ============================================================
# BAGIAN 3: TRANSFER LEARNING
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 3: TRANSFER LEARNING")
print("=" * 60)

if TORCH_AVAILABLE:
    
    def demo_transfer_learning():
        """Demo transfer learning dengan pretrained model"""
        print("\n📊 Demo: Transfer Learning dengan ResNet18\n")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load pretrained ResNet18
        print("Loading pretrained ResNet18...")
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        
        # Freeze all layers
        for param in model.parameters():
            param.requires_grad = False
        
        # Replace final layer
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, 10)  # 10 classes untuk CIFAR-10
        
        model = model.to(device)
        
        print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
        
        # Data
        transform = transforms.Compose([
            transforms.Resize(224),  # ResNet expects 224x224
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])
        
        trainset = torchvision.datasets.CIFAR10(
            root='./data', train=True, download=True, transform=transform)
        testset = torchvision.datasets.CIFAR10(
            root='./data', train=False, download=True, transform=transform)
        
        # Smaller subset
        train_subset = torch.utils.data.Subset(trainset, range(2000))
        test_subset = torch.utils.data.Subset(testset, range(500))
        
        train_loader = DataLoader(train_subset, batch_size=32, shuffle=True, num_workers=0)
        test_loader = DataLoader(test_subset, batch_size=32, shuffle=False, num_workers=0)
        
        # Train only the new FC layer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
        
        n_epochs = 5
        print("\nTraining (only FC layer)...")
        
        for epoch in range(n_epochs):
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            test_loss, test_acc = evaluate(model, test_loader, criterion, device)
            
            print(f"Epoch {epoch+1}/{n_epochs}: "
                  f"Train Acc={train_acc:.2%}, Test Acc={test_acc:.2%}")
        
        print("\n✅ Transfer Learning demo selesai!")
        print(f"   Final Test Accuracy: {test_acc:.2%}")
        print("   (Dengan fine-tuning lebih banyak epoch, akurasi bisa lebih tinggi)")


# ============================================================
# BAGIAN 4: VISUALISASI FILTERS DAN FEATURE MAPS
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 4: VISUALISASI FILTERS DAN FEATURE MAPS")
print("=" * 60)

if TORCH_AVAILABLE:
    
    def visualize_filters(model):
        """Visualize convolutional filters"""
        # Get first conv layer filters
        if hasattr(model, 'conv1'):
            filters = model.conv1.weight.data.cpu()
        else:
            # For ResNet
            filters = model.conv1.weight.data.cpu()
        
        n_filters = min(32, filters.shape[0])
        
        fig, axes = plt.subplots(4, 8, figsize=(16, 8))
        
        for idx, ax in enumerate(axes.flat):
            if idx < n_filters:
                # Get filter (normalize for visualization)
                filt = filters[idx]
                if filt.shape[0] == 3:  # RGB filter
                    filt = filt.permute(1, 2, 0)
                    filt = (filt - filt.min()) / (filt.max() - filt.min() + 1e-8)
                    ax.imshow(filt)
                else:  # Single channel
                    filt = filt[0]
                    ax.imshow(filt, cmap='gray')
                
                ax.set_title(f'Filter {idx}')
            ax.axis('off')
        
        plt.suptitle('First Layer Convolutional Filters')
        plt.tight_layout()
        plt.savefig('output_conv_filters.png', dpi=150)
        plt.show()
    
    
    def visualize_feature_maps(model, image_tensor, device):
        """Visualize feature maps from different layers"""
        model.eval()
        
        # Hook to capture intermediate outputs
        activations = {}
        
        def get_activation(name):
            def hook(model, input, output):
                activations[name] = output.detach()
            return hook
        
        # Register hooks
        if hasattr(model, 'conv1'):
            model.conv1.register_forward_hook(get_activation('conv1'))
        if hasattr(model, 'conv2'):
            model.conv2.register_forward_hook(get_activation('conv2'))
        if hasattr(model, 'layer1'):
            model.layer1.register_forward_hook(get_activation('layer1'))
        
        # Forward pass
        with torch.no_grad():
            _ = model(image_tensor.unsqueeze(0).to(device))
        
        # Visualize
        fig, axes = plt.subplots(len(activations), 8, figsize=(16, 3*len(activations)))
        
        for row, (name, act) in enumerate(activations.items()):
            act = act[0].cpu()  # First image in batch
            n_channels = min(8, act.shape[0])
            
            for col in range(8):
                if col < n_channels:
                    if len(activations) > 1:
                        ax = axes[row, col]
                    else:
                        ax = axes[col]
                    ax.imshow(act[col], cmap='viridis')
                    if col == 0:
                        ax.set_ylabel(name)
                ax.axis('off')
        
        plt.suptitle('Feature Maps at Different Layers')
        plt.tight_layout()
        plt.savefig('output_feature_maps.png', dpi=150)
        plt.show()


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PRAKTIKUM BAB 5: DEEP LEARNING UNTUK COMPUTER VISION")
    print("=" * 60)
    
    print("\n🚀 Menjalankan demos...\n")
    
    # Demo 1: NumPy Neural Network
    demo_numpy_nn()
    
    if TORCH_AVAILABLE:
        # Demo 2: PyTorch CNN
        model = demo_pytorch_cnn()
        
        # Demo 3: Transfer Learning
        demo_transfer_learning()
        
        # Demo 4: Visualize filters
        print("\n📊 Visualizing convolutional filters...")
        visualize_filters(model)
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM SELESAI!")
    print("=" * 60)
    print("\nFile output yang dihasilkan:")
    print("  - output_numpy_nn.png")
    if TORCH_AVAILABLE:
        print("  - output_pytorch_cnn_training.png")
        print("  - output_cnn_predictions.png")
        print("  - output_conv_filters.png")
    print("\n📝 Tugas: Lihat file tugas/tugas_bab_05.md")
