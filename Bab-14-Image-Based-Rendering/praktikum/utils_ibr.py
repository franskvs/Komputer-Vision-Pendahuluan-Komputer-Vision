"""
Utilities untuk Image-Based Rendering Praktikum
===============================================

Modul ini menyediakan helper functions dan utilities yang
digunakan oleh semua program praktikum IBR.

Features:
- Image display dengan auto-close
- Logging dan progress tracking
- Sample data generation
- Common image operations
"""

import numpy as np
import cv2
from pathlib import Path
import sys

# ============================================================
# DISPLAY UTILITIES
# ============================================================

def show_image(title, image, wait_ms=2000):
    """
    Display image dengan auto-close setelah delay.
    
    Args:
        title: Judul window
        image: Image untuk ditampilkan
        wait_ms: Delay dalam milliseconds (default 2000ms = 2 detik)
    
    Returns:
        key yang dipressed (atau 'timeout' jika auto-close)
    
    Deskripsi:
    - Buat window display dengan cv2.imshow()
    - Tunggu user input atau timeout
    - Jika user press 'q' atau ESC, close window
    - Jika timeout, auto-close window
    - Return info tentang apa yang terjadi
    
    Contoh real-world:
    >>> img = cv2.imread('foto.jpg')
    >>> show_image('Preview', img, wait_ms=3000)
    # Window akan close otomatis setelah 3 detik
    """
    try:
        # Create window dan display image
        cv2.imshow(title, image)
        
        # Wait dengan timeout
        # waitKey(0) = tunggu key press (infinite)
        # waitKey(ms) = tunggu ms atau sampai key press
        key = cv2.waitKey(wait_ms)
        
        # Check if user pressed 'q' (113) atau ESC (27)
        if key == ord('q') or key == 27:  # 27 = ESC
            print(f"[Display] User pressed 'q' or ESC, closing window...")
            cv2.destroyWindow(title)
            return 'user_close'
        else:
            # Auto-close after timeout
            print(f"[Display] Auto-closing window '{title}' after {wait_ms}ms...")
            cv2.destroyWindow(title)
            return 'timeout'
    
    except Exception as e:
        print(f"[Error] Failed to display image: {e}")
        return 'error'

def show_images_comparison(title1, img1, title2, img2, wait_ms=3000):
    """
    Display dua images side-by-side untuk comparison.
    
    Args:
        title1, title2: Judul masing-masing image
        img1, img2: Images untuk dibandingkan
        wait_ms: Delay
    
    Deskripsi:
    - Buat horizontal stack dari dua images
    - Resize jika sizes berbeda
    - Display side-by-side
    - Auto-close setelah delay
    
    Real-world: Compare before/after hasil processing
    """
    try:
        # Ensure same height untuk proper stacking
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        target_h = min(h1, h2)
        
        # Resize if needed
        if h1 != target_h or w1 != w1:
            img1_resized = cv2.resize(img1, (int(w1 * target_h / h1), target_h))
        else:
            img1_resized = img1
        
        if h2 != target_h or w2 != w2:
            img2_resized = cv2.resize(img2, (int(w2 * target_h / h2), target_h))
        else:
            img2_resized = img2
        
        # Stack horizontally
        combined = np.hstack([img1_resized, img2_resized])
        
        # Add text labels
        cv2.putText(combined, title1, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(combined, title2, (img1_resized.shape[1] + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Display
        show_image(f"Comparison: {title1} vs {title2}", combined, wait_ms)
        
    except Exception as e:
        print(f"[Error] Failed to display comparison: {e}")

def show_grid_images(images, titles=None, grid_shape=None, wait_ms=3000):
    """
    Display multiple images dalam grid.
    
    Args:
        images: List of images
        titles: List of titles (optional)
        grid_shape: (rows, cols) atau None untuk auto
        wait_ms: Delay
    
    Real-world: Display intermediate results dari processing pipeline
    """
    try:
        n = len(images)
        
        if grid_shape is None:
            # Auto compute grid
            cols = int(np.ceil(np.sqrt(n)))
            rows = int(np.ceil(n / cols))
        else:
            rows, cols = grid_shape
        
        # Standardize image size
        h, w = images[0].shape[:2]
        
        # Create grid
        grid = np.zeros((rows * h, cols * w, 3), dtype=np.uint8)
        
        for idx, img in enumerate(images):
            row = idx // cols
            col = idx % cols
            
            # Ensure 3 channels
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            
            # Resize if needed
            img_resized = cv2.resize(img, (w, h))
            
            # Place in grid
            grid[row*h:(row+1)*h, col*w:(col+1)*w] = img_resized
            
            # Add title if provided
            if titles and idx < len(titles):
                cv2.putText(grid, titles[idx],
                           (col*w + 10, row*h + 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                           (255, 255, 255), 1)
        
        show_image("Image Grid", grid, wait_ms)
        
    except Exception as e:
        print(f"[Error] Failed to display grid: {e}")

# ============================================================
# FILE UTILITIES
# ============================================================

def ensure_dir(path):
    """
    Ensure directory exists, create if not.
    
    Args:
        path: Directory path
    
    Returns:
        Path object
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_image(filename, image, subdir='output'):
    """
    Save image dengan organized directory structure.
    
    Args:
        filename: Nama file (misalnya 'result.jpg')
        image: Image array
        subdir: Subdirectory dalam output (default 'output')
    
    Real-world: Auto-organize hasil ke folder dengan timestamp
    """
    try:
        output_dir = ensure_dir(Path(__file__).parent / subdir)
        filepath = output_dir / filename
        
        cv2.imwrite(str(filepath), image)
        print(f"[Save] Saved: {filepath}")
        
        return filepath
    
    except Exception as e:
        print(f"[Error] Failed to save image: {e}")
        return None

# ============================================================
# IMAGE PROCESSING UTILITIES
# ============================================================

def create_sample_image(width=640, height=480, pattern='checkerboard'):
    """
    Create sample image dengan berbagai patterns untuk testing.
    
    Args:
        width, height: Image dimensions
        pattern: 'checkerboard', 'gradient', 'circles', 'mixed'
    
    Real-world: Generate synthetic data untuk testing tanpa hardware
    """
    if pattern == 'checkerboard':
        # Checkerboard pattern
        img = np.zeros((height, width, 3), dtype=np.uint8)
        square_size = 50
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                if ((x // square_size) + (y // square_size)) % 2 == 0:
                    img[y:y+square_size, x:x+square_size] = [255, 255, 255]
                else:
                    img[y:y+square_size, x:x+square_size] = [0, 0, 0]
        
        # Add some colored features
        cv2.circle(img, (width//4, height//4), 30, (255, 0, 0), -1)
        cv2.circle(img, (3*width//4, height//4), 30, (0, 255, 0), -1)
        cv2.circle(img, (width//2, 3*height//4), 30, (0, 0, 255), -1)
        
        return img
    
    elif pattern == 'gradient':
        # Color gradient
        img = np.zeros((height, width, 3), dtype=np.uint8)
        for x in range(width):
            for y in range(height):
                img[y, x] = [
                    int(255 * x / width),
                    int(255 * y / height),
                    int(255 * (1 - x / width))
                ]
        return img
    
    elif pattern == 'circles':
        # Random circles
        img = np.zeros((height, width, 3), dtype=np.uint8)
        np.random.seed(42)
        
        for _ in range(20):
            center = (np.random.randint(0, width),
                     np.random.randint(0, height))
            radius = np.random.randint(10, 50)
            color = tuple(np.random.randint(0, 255, 3).tolist())
            cv2.circle(img, center, radius, color, -1)
        
        return img
    
    elif pattern == 'mixed':
        # Combination
        img = create_sample_image(width, height, 'gradient')
        
        # Add some shapes
        cv2.rectangle(img, (50, 50), (200, 200), (255, 255, 0), -1)
        cv2.circle(img, (width//2, height//2), 80, (255, 0, 255), 2)
        cv2.putText(img, 'Sample Image', (150, 450),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return img
    
    return create_sample_image(width, height, 'checkerboard')

def resize_image(image, max_width=800, max_height=600):
    """
    Resize image untuk fit dalam display window.
    
    Args:
        image: Input image
        max_width, max_height: Maximum dimensions
    
    Real-world: Resize large images untuk preview
    """
    h, w = image.shape[:2]
    
    if w <= max_width and h <= max_height:
        return image
    
    # Calculate scaling factor
    scale = min(max_width / w, max_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    return cv2.resize(image, (new_w, new_h))

# ============================================================
# LOGGING UTILITIES
# ============================================================

class Logger:
    """
    Simple logger untuk track progress dan results.
    
    Real-world: Maintain log file untuk debugging dan documentation
    """
    
    def __init__(self, name='ibr_praktikum'):
        """Initialize logger."""
        self.name = name
        self.messages = []
    
    def info(self, message):
        """Log info message."""
        msg = f"[INFO] {message}"
        print(msg)
        self.messages.append(msg)
    
    def success(self, message):
        """Log success message."""
        msg = f"[✓] {message}"
        print(msg)
        self.messages.append(msg)
    
    def warning(self, message):
        """Log warning message."""
        msg = f"[!] {message}"
        print(msg)
        self.messages.append(msg)
    
    def error(self, message):
        """Log error message."""
        msg = f"[✗] {message}"
        print(msg, file=sys.stderr)
        self.messages.append(msg)
    
    def save_log(self, filepath=None):
        """Save log ke file."""
        if filepath is None:
            filepath = ensure_dir('output') / 'execution.log'
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(self.messages))
        
        print(f"[Log] Saved to {filepath}")

# ============================================================
# TIMING UTILITIES
# ============================================================

class Timer:
    """
    Simple timer untuk measure execution time.
    
    Real-world: Benchmark untuk performance analysis
    """
    
    def __init__(self, name="Operation"):
        """Initialize timer."""
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        """Enter context manager."""
        self.start_time = cv2.getTickCount()
        return self
    
    def __exit__(self, *args):
        """Exit context manager dan print elapsed time."""
        end_time = cv2.getTickCount()
        elapsed_ms = (end_time - self.start_time) / cv2.getTickFrequency() * 1000
        print(f"[Time] {self.name}: {elapsed_ms:.2f} ms")

# ============================================================
# EXPORT
# ============================================================

__all__ = [
    'show_image',
    'show_images_comparison',
    'show_grid_images',
    'ensure_dir',
    'save_image',
    'create_sample_image',
    'resize_image',
    'Logger',
    'Timer'
]
