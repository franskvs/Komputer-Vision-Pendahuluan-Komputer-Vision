"""
PRAKTIKUM BAB 6: RECOGNITION (PENGENALAN)
==========================================

Tujuan:
1. Memahami dan mengimplementasikan Bag of Visual Words
2. Image Classification dengan CNN
3. Object Detection dengan pretrained models
4. Semantic Segmentation

Kebutuhan:
- Python 3.8+
- OpenCV
- PyTorch + torchvision
- scikit-learn
- NumPy, Matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Check dependencies
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torchvision
    from torchvision import transforms, models
    TORCH_AVAILABLE = True
    print(f"PyTorch version: {torch.__version__}")
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available")

try:
    from sklearn.cluster import KMeans
    from sklearn.svm import SVC
    from sklearn.metrics import classification_report, confusion_matrix
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("scikit-learn not available")

# ============================================================
# BAGIAN 1: BAG OF VISUAL WORDS (BoVW)
# ============================================================

print("=" * 60)
print("BAGIAN 1: BAG OF VISUAL WORDS")
print("=" * 60)

class BagOfVisualWords:
    """
    Implementasi Bag of Visual Words untuk Image Retrieval dan Classification
    """
    
    def __init__(self, n_clusters=100):
        """
        Args:
            n_clusters: Jumlah visual words (vocabulary size)
        """
        self.n_clusters = n_clusters
        self.kmeans = None
        self.vocabulary = None
        self.sift = cv2.SIFT_create()
    
    def extract_features(self, image):
        """Extract SIFT features dari image"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        keypoints, descriptors = self.sift.detectAndCompute(gray, None)
        return keypoints, descriptors
    
    def build_vocabulary(self, images, max_features_per_image=500):
        """
        Build visual vocabulary dari training images
        
        Args:
            images: List of images
            max_features_per_image: Max features to sample per image
        """
        print("Extracting features from images...")
        all_descriptors = []
        
        for i, img in enumerate(images):
            _, descriptors = self.extract_features(img)
            if descriptors is not None:
                # Sample jika terlalu banyak
                if len(descriptors) > max_features_per_image:
                    indices = np.random.choice(len(descriptors), 
                                               max_features_per_image, 
                                               replace=False)
                    descriptors = descriptors[indices]
                all_descriptors.append(descriptors)
        
        all_descriptors = np.vstack(all_descriptors)
        print(f"Total descriptors: {len(all_descriptors)}")
        
        # K-Means clustering
        print(f"Building vocabulary with {self.n_clusters} visual words...")
        self.kmeans = KMeans(n_clusters=self.n_clusters, 
                            random_state=42, 
                            n_init=10,
                            max_iter=100)
        self.kmeans.fit(all_descriptors)
        self.vocabulary = self.kmeans.cluster_centers_
        print("Vocabulary built!")
        
        return self.vocabulary
    
    def compute_histogram(self, image, normalize=True):
        """
        Compute BoVW histogram untuk single image
        
        Args:
            image: Input image
            normalize: Whether to L2 normalize histogram
            
        Returns:
            histogram: BoVW histogram
        """
        _, descriptors = self.extract_features(image)
        
        if descriptors is None:
            return np.zeros(self.n_clusters)
        
        # Assign descriptors ke visual words
        words = self.kmeans.predict(descriptors)
        
        # Build histogram
        histogram, _ = np.histogram(words, bins=range(self.n_clusters + 1))
        histogram = histogram.astype(np.float32)
        
        if normalize:
            norm = np.linalg.norm(histogram)
            if norm > 0:
                histogram /= norm
        
        return histogram
    
    def compute_histograms(self, images):
        """Compute histograms for multiple images"""
        histograms = []
        for img in images:
            hist = self.compute_histogram(img)
            histograms.append(hist)
        return np.array(histograms)
    
    def compute_similarity(self, hist1, hist2):
        """
        Compute similarity between two histograms
        Using cosine similarity
        """
        dot_product = np.dot(hist1, hist2)
        norm1 = np.linalg.norm(hist1)
        norm2 = np.linalg.norm(hist2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def retrieve(self, query_image, database_images, top_k=5):
        """
        Image retrieval: find most similar images to query
        
        Args:
            query_image: Query image
            database_images: List of database images
            top_k: Number of results to return
            
        Returns:
            indices: Indices of top-k similar images
            similarities: Similarity scores
        """
        query_hist = self.compute_histogram(query_image)
        
        similarities = []
        for img in database_images:
            db_hist = self.compute_histogram(img)
            sim = self.compute_similarity(query_hist, db_hist)
            similarities.append(sim)
        
        # Sort by similarity (descending)
        indices = np.argsort(similarities)[::-1][:top_k]
        top_similarities = [similarities[i] for i in indices]
        
        return indices, top_similarities


class SpatialPyramidMatching:
    """
    Spatial Pyramid Matching untuk memasukkan informasi spatial ke BoVW
    """
    
    def __init__(self, bovw, levels=3):
        """
        Args:
            bovw: Trained BagOfVisualWords instance
            levels: Number of pyramid levels (0, 1, 2, ...)
        """
        self.bovw = bovw
        self.levels = levels
    
    def compute_histogram(self, image):
        """
        Compute spatial pyramid histogram
        """
        h, w = image.shape[:2]
        n_words = self.bovw.n_clusters
        
        all_histograms = []
        
        for level in range(self.levels):
            n_cells = 2 ** level  # 1, 2, 4, ...
            cell_h = h // n_cells
            cell_w = w // n_cells
            
            # Weight untuk level ini
            if level == 0:
                weight = 1.0 / (2 ** (self.levels - 1))
            else:
                weight = 1.0 / (2 ** (self.levels - level))
            
            for i in range(n_cells):
                for j in range(n_cells):
                    # Extract cell
                    y1, y2 = i * cell_h, (i + 1) * cell_h
                    x1, x2 = j * cell_w, (j + 1) * cell_w
                    cell = image[y1:y2, x1:x2]
                    
                    # Compute histogram untuk cell
                    hist = self.bovw.compute_histogram(cell, normalize=False)
                    all_histograms.append(weight * hist)
        
        # Concatenate semua histograms
        final_histogram = np.concatenate(all_histograms)
        
        # Normalize
        norm = np.linalg.norm(final_histogram)
        if norm > 0:
            final_histogram /= norm
        
        return final_histogram


def demo_bovw():
    """Demo Bag of Visual Words"""
    print("\n📊 Demo: Bag of Visual Words\n")
    
    if not SKLEARN_AVAILABLE:
        print("❌ scikit-learn required for this demo")
        return
    
    # Generate synthetic dataset (simple shapes)
    def create_shape_image(shape, size=128):
        """Create image with a specific shape"""
        img = np.zeros((size, size), dtype=np.uint8)
        center = size // 2
        
        if shape == 'circle':
            cv2.circle(img, (center, center), size//3, 255, -1)
        elif shape == 'square':
            s = size // 3
            cv2.rectangle(img, (center-s, center-s), (center+s, center+s), 255, -1)
        elif shape == 'triangle':
            pts = np.array([
                [center, center - size//3],
                [center - size//3, center + size//3],
                [center + size//3, center + size//3]
            ])
            cv2.fillPoly(img, [pts], 255)
        
        # Add noise
        noise = np.random.randint(0, 30, img.shape, dtype=np.uint8)
        img = cv2.add(img, noise)
        
        return img
    
    # Create dataset
    shapes = ['circle', 'square', 'triangle']
    n_per_class = 10
    
    images = []
    labels = []
    
    for i, shape in enumerate(shapes):
        for _ in range(n_per_class):
            img = create_shape_image(shape)
            images.append(img)
            labels.append(i)
    
    # Shuffle
    indices = np.random.permutation(len(images))
    images = [images[i] for i in indices]
    labels = [labels[i] for i in indices]
    
    # Split train/test
    n_train = 20
    train_images = images[:n_train]
    train_labels = labels[:n_train]
    test_images = images[n_train:]
    test_labels = labels[n_train:]
    
    # Build BoVW
    bovw = BagOfVisualWords(n_clusters=50)
    bovw.build_vocabulary(train_images)
    
    # Compute histograms
    train_histograms = bovw.compute_histograms(train_images)
    test_histograms = bovw.compute_histograms(test_images)
    
    # Train SVM classifier
    svm = SVC(kernel='rbf', C=10)
    svm.fit(train_histograms, train_labels)
    
    # Predict
    predictions = svm.predict(test_histograms)
    
    # Evaluate
    accuracy = np.mean(predictions == test_labels)
    print(f"Classification Accuracy: {accuracy:.2%}")
    
    # Visualize
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    
    for idx, ax in enumerate(axes.flat):
        if idx < len(test_images):
            ax.imshow(test_images[idx], cmap='gray')
            pred = shapes[predictions[idx]]
            true = shapes[test_labels[idx]]
            color = 'green' if pred == true else 'red'
            ax.set_title(f'Pred: {pred}\nTrue: {true}', color=color)
        ax.axis('off')
    
    plt.suptitle('Bag of Visual Words Classification Results')
    plt.tight_layout()
    plt.savefig('output_bovw_classification.png', dpi=150)
    plt.show()
    
    print("✅ BoVW demo selesai!")


# ============================================================
# BAGIAN 2: CNN IMAGE CLASSIFICATION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 2: CNN IMAGE CLASSIFICATION")
print("=" * 60)

if TORCH_AVAILABLE:
    
    class ImageClassifier:
        """
        Image Classifier menggunakan pretrained CNN
        """
        
        def __init__(self, model_name='resnet18', num_classes=10, pretrained=True):
            """
            Args:
                model_name: Nama model ('resnet18', 'resnet50', 'vgg16', etc.)
                num_classes: Jumlah kelas
                pretrained: Gunakan pretrained weights
            """
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model_name = model_name
            self.num_classes = num_classes
            
            # Load model
            if model_name == 'resnet18':
                self.model = models.resnet18(weights='DEFAULT' if pretrained else None)
                self.model.fc = nn.Linear(512, num_classes)
            elif model_name == 'resnet50':
                self.model = models.resnet50(weights='DEFAULT' if pretrained else None)
                self.model.fc = nn.Linear(2048, num_classes)
            elif model_name == 'vgg16':
                self.model = models.vgg16(weights='DEFAULT' if pretrained else None)
                self.model.classifier[-1] = nn.Linear(4096, num_classes)
            
            self.model = self.model.to(self.device)
            
            # Transforms
            self.train_transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize(256),
                transforms.RandomCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], 
                                   [0.229, 0.224, 0.225])
            ])
            
            self.test_transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], 
                                   [0.229, 0.224, 0.225])
            ])
        
        def predict(self, image, return_probs=False):
            """
            Predict class untuk single image
            
            Args:
                image: Input image (numpy array atau PIL Image)
                return_probs: Return probability distribution
            """
            self.model.eval()
            
            # Preprocess
            if isinstance(image, np.ndarray):
                x = self.test_transform(image)
            else:
                x = self.test_transform(np.array(image))
            
            x = x.unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(x)
                probs = F.softmax(outputs, dim=1)
                pred = outputs.argmax(dim=1).item()
            
            if return_probs:
                return pred, probs[0].cpu().numpy()
            return pred
        
        def predict_batch(self, images):
            """Batch prediction"""
            self.model.eval()
            
            batch = torch.stack([self.test_transform(img) for img in images])
            batch = batch.to(self.device)
            
            with torch.no_grad():
                outputs = self.model(batch)
                preds = outputs.argmax(dim=1).cpu().numpy()
            
            return preds
        
        def get_features(self, image):
            """
            Extract feature vector dari image (before final FC layer)
            """
            self.model.eval()
            
            # Hook untuk capture features
            features = {}
            def hook(module, input, output):
                features['feat'] = output.detach()
            
            # Register hook
            if 'resnet' in self.model_name:
                handle = self.model.avgpool.register_forward_hook(hook)
            elif 'vgg' in self.model_name:
                handle = self.model.avgpool.register_forward_hook(hook)
            
            # Forward
            x = self.test_transform(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                _ = self.model(x)
            
            handle.remove()
            
            return features['feat'].flatten().cpu().numpy()
    
    
    def demo_imagenet_classification():
        """Demo ImageNet classification dengan pretrained model"""
        print("\n📊 Demo: ImageNet Classification\n")
        
        # Load pretrained ResNet
        model = models.resnet18(weights='DEFAULT')
        model.eval()
        
        # ImageNet class names (subset)
        # Full list: https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a
        imagenet_classes = {
            281: 'tabby cat',
            282: 'tiger cat',
            285: 'Egyptian cat',
            243: 'bulldog',
            244: 'bull mastiff'
        }
        
        # Create sample image (cat-like pattern)
        img = np.random.randint(100, 200, (224, 224, 3), dtype=np.uint8)
        
        # Preprocess
        transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], 
                               [0.229, 0.224, 0.225])
        ])
        
        x = transform(img).unsqueeze(0)
        
        # Predict
        with torch.no_grad():
            outputs = model(x)
            probs = F.softmax(outputs, dim=1)
            
            # Top-5 predictions
            top5_prob, top5_idx = probs.topk(5)
        
        print("Top-5 Predictions:")
        for prob, idx in zip(top5_prob[0], top5_idx[0]):
            print(f"  Class {idx.item()}: {prob.item():.2%}")
        
        print("\n✅ ImageNet classification demo selesai!")


# ============================================================
# BAGIAN 3: OBJECT DETECTION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 3: OBJECT DETECTION")
print("=" * 60)

if TORCH_AVAILABLE:
    
    class ObjectDetector:
        """
        Object Detection menggunakan pretrained models (Faster R-CNN, YOLO, etc.)
        """
        
        def __init__(self, model_name='fasterrcnn'):
            """
            Args:
                model_name: 'fasterrcnn' atau 'retinanet'
            """
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            if model_name == 'fasterrcnn':
                self.model = models.detection.fasterrcnn_resnet50_fpn(weights='DEFAULT')
            elif model_name == 'retinanet':
                self.model = models.detection.retinanet_resnet50_fpn(weights='DEFAULT')
            
            self.model = self.model.to(self.device)
            self.model.eval()
            
            # COCO class names
            self.class_names = [
                '__background__', 'person', 'bicycle', 'car', 'motorcycle',
                'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench',
                'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
                'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella',
                'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
                'snowboard', 'sports ball', 'kite', 'baseball bat',
                'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
                'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
                'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
                'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A',
                'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                'refrigerator', 'N/A', 'book', 'clock', 'vase', 'scissors',
                'teddy bear', 'hair drier', 'toothbrush'
            ]
        
        def detect(self, image, threshold=0.5):
            """
            Detect objects in image
            
            Args:
                image: Input image (numpy array, BGR or RGB)
                threshold: Confidence threshold
                
            Returns:
                boxes: List of bounding boxes [x1, y1, x2, y2]
                labels: List of class labels
                scores: List of confidence scores
            """
            # Preprocess
            if isinstance(image, np.ndarray):
                if len(image.shape) == 2:
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                elif image.shape[2] == 4:
                    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
                elif image.shape[2] == 3:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Convert to tensor
            transform = transforms.ToTensor()
            x = transform(image).to(self.device)
            
            # Detect
            with torch.no_grad():
                predictions = self.model([x])[0]
            
            # Filter by threshold
            boxes = predictions['boxes'].cpu().numpy()
            labels = predictions['labels'].cpu().numpy()
            scores = predictions['scores'].cpu().numpy()
            
            mask = scores >= threshold
            boxes = boxes[mask]
            labels = labels[mask]
            scores = scores[mask]
            
            return boxes, labels, scores
        
        def visualize(self, image, boxes, labels, scores, save_path=None):
            """Visualize detections"""
            img = image.copy()
            
            for box, label, score in zip(boxes, labels, scores):
                x1, y1, x2, y2 = box.astype(int)
                
                # Draw box
                color = (0, 255, 0)  # Green
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                class_name = self.class_names[label]
                text = f'{class_name}: {score:.2f}'
                cv2.putText(img, text, (x1, y1-5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            plt.figure(figsize=(12, 8))
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.title(f'Detected {len(boxes)} objects')
            
            if save_path:
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.show()
            
            return img
    
    
    def compute_iou(box1, box2):
        """
        Compute IoU between two boxes
        
        Args:
            box1, box2: [x1, y1, x2, y2]
        """
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0
    
    
    def non_max_suppression(boxes, scores, iou_threshold=0.5):
        """
        Non-Maximum Suppression
        
        Args:
            boxes: Array of boxes [N, 4]
            scores: Confidence scores [N]
            iou_threshold: IoU threshold for suppression
            
        Returns:
            keep: Indices of boxes to keep
        """
        if len(boxes) == 0:
            return []
        
        # Sort by score
        indices = np.argsort(scores)[::-1]
        
        keep = []
        while len(indices) > 0:
            current = indices[0]
            keep.append(current)
            
            if len(indices) == 1:
                break
            
            indices = indices[1:]
            
            # Compute IoU dengan box yang sudah dipilih
            ious = np.array([compute_iou(boxes[current], boxes[i]) for i in indices])
            
            # Keep boxes dengan IoU < threshold
            indices = indices[ious < iou_threshold]
        
        return keep


# ============================================================
# BAGIAN 4: SEMANTIC SEGMENTATION
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 4: SEMANTIC SEGMENTATION")
print("=" * 60)

if TORCH_AVAILABLE:
    
    class SemanticSegmenter:
        """
        Semantic Segmentation menggunakan pretrained models (DeepLabV3, FCN)
        """
        
        def __init__(self, model_name='deeplabv3'):
            """
            Args:
                model_name: 'deeplabv3' atau 'fcn'
            """
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            if model_name == 'deeplabv3':
                self.model = models.segmentation.deeplabv3_resnet101(weights='DEFAULT')
            elif model_name == 'fcn':
                self.model = models.segmentation.fcn_resnet101(weights='DEFAULT')
            
            self.model = self.model.to(self.device)
            self.model.eval()
            
            # Pascal VOC class names
            self.class_names = [
                'background', 'aeroplane', 'bicycle', 'bird', 'boat',
                'bottle', 'bus', 'car', 'cat', 'chair', 'cow',
                'diningtable', 'dog', 'horse', 'motorbike', 'person',
                'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
            ]
            
            # Color palette
            self.colors = np.random.randint(0, 255, (len(self.class_names), 3))
            self.colors[0] = [0, 0, 0]  # Background hitam
        
        def segment(self, image):
            """
            Segment image
            
            Args:
                image: Input image (numpy array)
                
            Returns:
                segmentation: Segmentation mask [H, W]
            """
            # Preprocess
            transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], 
                                   [0.229, 0.224, 0.225])
            ])
            
            x = transform(image).unsqueeze(0).to(self.device)
            
            # Segment
            with torch.no_grad():
                output = self.model(x)['out']
                segmentation = output.argmax(1).squeeze().cpu().numpy()
            
            return segmentation
        
        def visualize(self, image, segmentation, alpha=0.5, save_path=None):
            """Visualize segmentation overlay"""
            # Create colored mask
            colored_mask = self.colors[segmentation].astype(np.uint8)
            
            # Resize mask ke ukuran image jika berbeda
            if colored_mask.shape[:2] != image.shape[:2]:
                colored_mask = cv2.resize(colored_mask, 
                                         (image.shape[1], image.shape[0]),
                                         interpolation=cv2.INTER_NEAREST)
            
            # Convert image ke RGB jika perlu
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            
            # Overlay
            overlay = cv2.addWeighted(image, 1-alpha, colored_mask, alpha, 0)
            
            # Plot
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            axes[0].set_title('Original Image')
            axes[0].axis('off')
            
            axes[1].imshow(colored_mask)
            axes[1].set_title('Segmentation Mask')
            axes[1].axis('off')
            
            axes[2].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
            axes[2].set_title('Overlay')
            axes[2].axis('off')
            
            # Legend
            unique_classes = np.unique(segmentation)
            legend_patches = []
            for cls_id in unique_classes:
                if cls_id < len(self.class_names):
                    color = self.colors[cls_id] / 255.0
                    from matplotlib.patches import Patch
                    patch = Patch(color=color, label=self.class_names[cls_id])
                    legend_patches.append(patch)
            
            fig.legend(handles=legend_patches, loc='lower center', 
                      ncol=min(5, len(legend_patches)))
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.show()
            
            return overlay


# ============================================================
# BAGIAN 5: INSTANCE SEGMENTATION (Mask R-CNN)
# ============================================================

print("\n" + "=" * 60)
print("BAGIAN 5: INSTANCE SEGMENTATION")
print("=" * 60)

if TORCH_AVAILABLE:
    
    class InstanceSegmenter:
        """
        Instance Segmentation menggunakan Mask R-CNN
        """
        
        def __init__(self):
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model = models.detection.maskrcnn_resnet50_fpn(weights='DEFAULT')
            self.model = self.model.to(self.device)
            self.model.eval()
            
            # COCO class names
            self.class_names = [
                '__background__', 'person', 'bicycle', 'car', 'motorcycle',
                'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench',
                'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
                'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella',
                'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
                'snowboard', 'sports ball', 'kite', 'baseball bat',
                'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
                'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
                'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
                'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A',
                'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                'refrigerator', 'N/A', 'book', 'clock', 'vase', 'scissors',
                'teddy bear', 'hair drier', 'toothbrush'
            ]
        
        def segment(self, image, threshold=0.5):
            """
            Instance segmentation
            
            Returns:
                boxes: Bounding boxes
                labels: Class labels
                scores: Confidence scores
                masks: Instance masks [N, H, W]
            """
            # Preprocess
            if isinstance(image, np.ndarray):
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            transform = transforms.ToTensor()
            x = transform(image).to(self.device)
            
            # Detect
            with torch.no_grad():
                predictions = self.model([x])[0]
            
            # Filter by threshold
            mask = predictions['scores'] >= threshold
            
            boxes = predictions['boxes'][mask].cpu().numpy()
            labels = predictions['labels'][mask].cpu().numpy()
            scores = predictions['scores'][mask].cpu().numpy()
            masks = predictions['masks'][mask].squeeze(1).cpu().numpy()
            
            return boxes, labels, scores, masks
        
        def visualize(self, image, boxes, labels, scores, masks, save_path=None):
            """Visualize instance segmentation"""
            img = image.copy()
            
            # Random colors for each instance
            colors = np.random.randint(0, 255, (len(boxes), 3))
            
            # Create combined mask
            combined_mask = np.zeros_like(img)
            
            for i, (box, label, score, mask) in enumerate(zip(boxes, labels, scores, masks)):
                color = colors[i].tolist()
                
                # Threshold mask
                binary_mask = (mask > 0.5).astype(np.uint8)
                
                # Resize mask jika perlu
                if binary_mask.shape != img.shape[:2]:
                    binary_mask = cv2.resize(binary_mask, 
                                            (img.shape[1], img.shape[0]),
                                            interpolation=cv2.INTER_NEAREST)
                
                # Color mask
                colored_mask = np.zeros_like(img)
                for c in range(3):
                    colored_mask[:, :, c] = binary_mask * color[c]
                
                combined_mask = cv2.add(combined_mask, colored_mask)
                
                # Draw box
                x1, y1, x2, y2 = box.astype(int)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                class_name = self.class_names[label]
                text = f'{class_name}: {score:.2f}'
                cv2.putText(img, text, (x1, y1-5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Overlay
            overlay = cv2.addWeighted(img, 0.7, combined_mask, 0.3, 0)
            
            plt.figure(figsize=(12, 8))
            plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.title(f'Instance Segmentation: {len(boxes)} instances')
            
            if save_path:
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.show()
            
            return overlay


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PRAKTIKUM BAB 6: RECOGNITION")
    print("=" * 60)
    
    # Demo 1: Bag of Visual Words
    demo_bovw()
    
    if TORCH_AVAILABLE:
        # Demo 2: ImageNet Classification
        demo_imagenet_classification()
        
        # Demo 3: Object Detection (show architecture)
        print("\n📊 Object Detection dengan Faster R-CNN")
        print("   Untuk testing dengan gambar nyata, gunakan:")
        print("   detector = ObjectDetector('fasterrcnn')")
        print("   boxes, labels, scores = detector.detect(image)")
        print("   detector.visualize(image, boxes, labels, scores)")
        
        # Demo 4: Semantic Segmentation
        print("\n📊 Semantic Segmentation dengan DeepLabV3")
        print("   Untuk testing dengan gambar nyata, gunakan:")
        print("   segmenter = SemanticSegmenter('deeplabv3')")
        print("   mask = segmenter.segment(image)")
        print("   segmenter.visualize(image, mask)")
    
    print("\n" + "=" * 60)
    print("PRAKTIKUM SELESAI!")
    print("=" * 60)
    print("\nFile output yang dihasilkan:")
    print("  - output_bovw_classification.png")
    print("\n📝 Tugas: Lihat file tugas/tugas_bab_06.md")
