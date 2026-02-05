# Project Bab 14: Virtual Tour Creator - Sistem Image-Based Rendering untuk Tur Virtual Interaktif

## 1. Deskripsi Project

### 1.1 Latar Belakang
Di era digital, kebutuhan akan pengalaman virtual yang imersif semakin meningkat. Dari virtual tourism hingga real estate visualization, kemampuan untuk mengeksplorasi tempat secara virtual menjadi sangat berharga. Image-Based Rendering memungkinkan pembuatan pengalaman visual berkualitas tinggi dari kumpulan foto tanpa memerlukan 3D modeling yang kompleks.

### 1.2 Tujuan Project
Membangun sistem **Virtual Tour Creator** yang:
- Membuat panorama 360° dari sequential photos
- Mensintesis novel views untuk navigasi
- Menyediakan interface interaktif untuk eksplorasi
- Mengintegrasikan multiple locations dalam satu tour

### 1.3 Manfaat
- **Tourism**: Virtual tour destinasi wisata
- **Real Estate**: Property showcase
- **Education**: Virtual museum/lab
- **Documentation**: Cultural heritage preservation

---

## 2. Spesifikasi Teknis

### 2.1 Input
- Sequential images untuk panorama (minimum 5 per location)
- Image metadata (optional EXIF)
- Location markers/connections (graph)

### 2.2 Output
- 360° panoramic images per location
- Interactive viewer dengan navigation
- Transition animations antar lokasi
- Export untuk web/VR

### 2.3 Requirements
| Komponen | Minimum | Recommended |
|----------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| RAM | 8 GB | 16 GB |
| Storage | 10 GB | 50 GB |
| GPU | Optional | NVIDIA 6GB+ |

### 2.4 Dependencies
```
opencv-python>=4.5.0
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
pillow>=9.0.0
flask>=2.0.0 (untuk web viewer)
```

---

## 3. Arsitektur Sistem

### 3.1 System Overview
```
┌─────────────────────────────────────────────────────────┐
│                 Virtual Tour Creator                     │
├──────────┬──────────┬──────────┬──────────┬────────────┤
│ Module 1 │ Module 2 │ Module 3 │ Module 4 │ Module 5   │
│ Capture  │ Panorama │ View     │ Tour     │ Interactive│
│ & Import │ Stitching│ Synthesis│ Builder  │ Viewer     │
└──────────┴──────────┴──────────┴──────────┴────────────┘
```

### 3.2 Data Flow
```
Raw Images → Feature Detection → Homography → 
Cylindrical Warp → Blending → 360° Panorama →
View Synthesis → Navigation Graph → Interactive Tour
```

---

## 4. Modul Project

## Module 1: Image Capture & Import (15%)

### 1.1 Objectives
- Systematic image capture guidance
- Image quality assessment
- EXIF extraction dan organization

### 1.2 Features

#### A. Capture Guidelines
```python
class CaptureGuidance:
    """
    Panduan untuk capturing images optimal.
    """
    
    def calculate_overlap(self, fov, num_images):
        """Hitung overlap percentage."""
        coverage = num_images * fov
        if coverage > 360:
            overlap = (coverage - 360) / num_images
            return overlap / fov * 100
        return 0
    
    def recommend_settings(self, scene_type):
        """Recommend camera settings."""
        settings = {
            'indoor': {
                'overlap': 30,  # percent
                'num_images': 12,
                'tips': ['Use tripod', 'Consistent exposure', 'Avoid moving objects']
            },
            'outdoor': {
                'overlap': 25,
                'num_images': 16,
                'tips': ['Shoot quickly', 'Watch for clouds', 'Level horizon']
            }
        }
        return settings.get(scene_type, settings['indoor'])
```

#### B. Image Quality Assessment
```python
def assess_image_quality(image):
    """
    Evaluate image quality for stitching.
    
    Returns:
        dict: Quality metrics
    """
    metrics = {
        'sharpness': compute_laplacian_variance(image),
        'exposure': analyze_histogram(image),
        'blur_detected': detect_motion_blur(image),
        'resolution': image.shape[:2],
        'suitable': True
    }
    
    # Thresholds
    if metrics['sharpness'] < 100:
        metrics['suitable'] = False
        metrics['issues'] = ['Image too blurry']
    
    return metrics
```

#### C. Image Organization
```
project/
├── location_001/
│   ├── raw/
│   │   ├── IMG_001.jpg
│   │   ├── IMG_002.jpg
│   │   └── ...
│   ├── metadata.json
│   └── panorama.jpg
├── location_002/
│   └── ...
└── tour_config.json
```

### 1.3 Deliverables
- [ ] Capture guidance module
- [ ] Quality assessment tool
- [ ] Automatic organization
- [ ] EXIF extraction

### 1.4 Rubrik Penilaian Module 1
| Kriteria | Excellent (90-100) | Good (70-89) | Fair (50-69) |
|----------|-------------------|--------------|--------------|
| Quality Assessment | Comprehensive metrics | Basic metrics | Minimal checking |
| Organization | Fully automated | Semi-automated | Manual |
| Documentation | Complete guide | Basic guide | Minimal |

---

## Module 2: Panorama Stitching Engine (30%)

### 2.1 Objectives
- Robust feature matching
- Cylindrical/spherical projection
- Multi-band blending
- 360° panorama generation

### 2.2 Features

#### A. Feature Detection & Matching
```python
class FeatureMatcher:
    """
    Robust feature detection dan matching.
    """
    
    def __init__(self, method='SIFT'):
        if method == 'SIFT':
            self.detector = cv2.SIFT_create(nfeatures=2000)
        elif method == 'ORB':
            self.detector = cv2.ORB_create(nfeatures=3000)
        
        self.matcher = cv2.BFMatcher()
    
    def match_images(self, img1, img2, ratio_thresh=0.7):
        """Match features dengan ratio test."""
        kp1, des1 = self.detector.detectAndCompute(img1, None)
        kp2, des2 = self.detector.detectAndCompute(img2, None)
        
        matches = self.matcher.knnMatch(des1, des2, k=2)
        
        # Ratio test
        good = []
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good.append(m)
        
        return kp1, kp2, good
```

#### B. Cylindrical Projection
```python
def cylindrical_warp(image, focal_length):
    """
    Warp image ke cylindrical projection.
    
    Args:
        image: Input image
        focal_length: Focal length dalam pixels
    
    Returns:
        Warped image
    """
    h, w = image.shape[:2]
    cx, cy = w / 2, h / 2
    
    # Create meshgrid
    x = np.arange(w)
    y = np.arange(h)
    X, Y = np.meshgrid(x, y)
    
    # Cylindrical projection
    theta = (X - cx) / focal_length
    h_cyl = (Y - cy) / np.sqrt((X - cx)**2 + focal_length**2)
    
    # Map back
    x_orig = focal_length * np.tan(theta) + cx
    y_orig = h_cyl * np.sqrt((x_orig - cx)**2 + focal_length**2) + cy
    
    # Warp
    warped = cv2.remap(image, 
                       x_orig.astype(np.float32), 
                       y_orig.astype(np.float32),
                       cv2.INTER_LINEAR)
    
    return warped
```

#### C. Multi-band Blending
```python
class MultiBandBlender:
    """
    Multi-band blending untuk seamless stitching.
    """
    
    def __init__(self, levels=5):
        self.levels = levels
    
    def blend(self, img1, img2, mask):
        """
        Blend dua gambar dengan multi-band.
        """
        # Build Gaussian pyramids
        G1 = self.gaussian_pyramid(img1)
        G2 = self.gaussian_pyramid(img2)
        GM = self.gaussian_pyramid(mask)
        
        # Build Laplacian pyramids
        L1 = self.laplacian_pyramid(G1)
        L2 = self.laplacian_pyramid(G2)
        
        # Blend pyramids
        blended = []
        for l1, l2, gm in zip(L1, L2, GM):
            blend_level = l1 * gm + l2 * (1 - gm)
            blended.append(blend_level)
        
        # Reconstruct
        return self.reconstruct(blended)
```

#### D. 360° Stitching
```python
def create_360_panorama(images, focal_length=None):
    """
    Create 360° panorama from sequential images.
    
    Args:
        images: List of images (captured in sequence)
        focal_length: Optional, estimated if None
    
    Returns:
        360° panoramic image
    """
    # 1. Estimate focal length if needed
    if focal_length is None:
        focal_length = estimate_focal_length(images)
    
    # 2. Warp to cylindrical
    warped = [cylindrical_warp(img, focal_length) for img in images]
    
    # 3. Match and compute translations
    translations = []
    for i in range(len(warped) - 1):
        H = compute_homography(warped[i], warped[i+1])
        translations.append(H[0, 2])  # x translation
    
    # 4. Bundle adjustment
    translations = bundle_adjust(translations, images[0].shape[1])
    
    # 5. Stitch with multi-band blending
    panorama = stitch_images(warped, translations)
    
    return panorama
```

### 2.3 Deliverables
- [ ] Feature matching module
- [ ] Cylindrical projection
- [ ] Spherical projection (bonus)
- [ ] Multi-band blending
- [ ] 360° panorama generation
- [ ] Exposure compensation

### 2.4 Rubrik Penilaian Module 2
| Kriteria | Excellent (90-100) | Good (70-89) | Fair (50-69) |
|----------|-------------------|--------------|--------------|
| Feature Matching | Robust, handles difficult cases | Works on standard cases | Basic matching |
| Blending | Seamless multi-band | Good alpha blending | Visible seams |
| 360° Support | Full 360° with wraparound | 270°+ coverage | < 270° |
| Quality | Professional quality | Good quality | Acceptable |

---

## Module 3: View Synthesis (25%)

### 3.1 Objectives
- Novel view generation untuk navigasi
- Smooth transitions antar panorama
- Depth-aware interpolation

### 3.2 Features

#### A. View Interpolation
```python
class ViewInterpolator:
    """
    Interpolasi view untuk smooth navigation.
    """
    
    def __init__(self, panorama, depth_map=None):
        self.panorama = panorama
        self.depth = depth_map
    
    def render_view(self, rotation, translation):
        """
        Render view dari virtual camera position.
        
        Args:
            rotation: (pitch, yaw, roll) dalam radians
            translation: (x, y, z) displacement
        
        Returns:
            Rendered view
        """
        # Create view transformation
        R = create_rotation_matrix(*rotation)
        
        # Sample from panorama
        view = sample_equirectangular(self.panorama, R, 
                                       fov=90, output_size=(800, 600))
        
        if self.depth is not None and np.any(translation):
            # Depth-based parallax
            view = apply_parallax(view, self.depth, translation)
        
        return view
```

#### B. Transition Effects
```python
class TransitionRenderer:
    """
    Render transisi antar lokasi panorama.
    """
    
    def dolly_zoom(self, pano1, pano2, t, speed_curve='ease'):
        """
        Dolly zoom transition effect.
        """
        # Apply speed curve
        t = self.apply_curve(t, speed_curve)
        
        # Zoom out from pano1
        fov1 = 90 + t * 30  # Expand FOV
        view1 = render_perspective(pano1, fov1)
        
        # Zoom in to pano2  
        fov2 = 120 - t * 30  # Contract FOV
        view2 = render_perspective(pano2, fov2)
        
        # Blend
        alpha = self.smooth_alpha(t)
        return view1 * (1 - alpha) + view2 * alpha
    
    def fade_transition(self, pano1, pano2, t):
        """Simple fade transition."""
        return pano1 * (1 - t) + pano2 * t
    
    def wipe_transition(self, pano1, pano2, t, direction='left'):
        """Wipe transition."""
        h, w = pano1.shape[:2]
        
        if direction == 'left':
            split = int(w * t)
            result = np.concatenate([pano2[:, :split], pano1[:, split:]], axis=1)
        
        return result
```

#### C. Depth from Panorama
```python
def estimate_panorama_depth(panorama, method='learning'):
    """
    Estimasi depth dari single panorama.
    
    Args:
        panorama: Equirectangular panorama
        method: 'learning' atau 'geometric'
    
    Returns:
        Depth map
    """
    if method == 'geometric':
        # Simple geometric assumption
        # Floor plane, vertical surfaces
        depth = geometric_depth_estimation(panorama)
    
    elif method == 'learning':
        # Use pre-trained model if available
        # e.g., OmniDepth, 360MonoDepth
        depth = neural_depth_estimation(panorama)
    
    return depth
```

### 3.3 Deliverables
- [ ] Equirectangular sampling
- [ ] Perspective view rendering
- [ ] Transition effects (3+ types)
- [ ] Basic depth estimation
- [ ] Parallax handling

### 3.4 Rubrik Penilaian Module 3
| Kriteria | Excellent (90-100) | Good (70-89) | Fair (50-69) |
|----------|-------------------|--------------|--------------|
| View Rendering | Smooth, artifact-free | Minor artifacts | Noticeable issues |
| Transitions | Multiple smooth effects | Basic fade | Abrupt |
| Depth | Learning-based | Geometric | No depth |

---

## Module 4: Tour Builder (15%)

### 4.1 Objectives
- Define navigation graph
- Configure hotspots dan interactions
- Export tour configuration

### 4.2 Features

#### A. Tour Graph
```python
class TourGraph:
    """
    Graph structure untuk virtual tour.
    """
    
    def __init__(self):
        self.nodes = {}  # location_id -> PanoramaNode
        self.edges = {}  # (from_id, to_id) -> TransitionConfig
    
    def add_location(self, location_id, panorama_path, metadata=None):
        """Add panorama location."""
        self.nodes[location_id] = PanoramaNode(
            id=location_id,
            panorama=panorama_path,
            metadata=metadata or {},
            hotspots=[]
        )
    
    def add_connection(self, from_id, to_id, transition_type='fade'):
        """Connect two locations."""
        self.edges[(from_id, to_id)] = TransitionConfig(
            from_node=from_id,
            to_node=to_id,
            transition=transition_type,
            direction=self.calculate_direction(from_id, to_id)
        )
    
    def add_hotspot(self, location_id, hotspot):
        """Add interactive hotspot."""
        self.nodes[location_id].hotspots.append(hotspot)
```

#### B. Hotspot Types
```python
@dataclass
class Hotspot:
    """Interactive hotspot dalam panorama."""
    position: Tuple[float, float]  # (theta, phi) dalam panorama
    type: str  # 'navigation', 'info', 'media'
    target: str  # target location atau content
    icon: str = 'default'
    label: str = ''

class NavigationHotspot(Hotspot):
    """Hotspot untuk navigasi ke lokasi lain."""
    type: str = 'navigation'
    direction: float = 0.0  # Facing direction at destination

class InfoHotspot(Hotspot):
    """Hotspot untuk informasi popup."""
    type: str = 'info'
    content: str = ''  # HTML content

class MediaHotspot(Hotspot):
    """Hotspot untuk media (video, audio, image)."""
    type: str = 'media'
    media_url: str = ''
    media_type: str = 'image'  # 'image', 'video', 'audio'
```

#### C. Tour Export
```python
def export_tour(tour_graph, output_dir, format='web'):
    """
    Export tour untuk deployment.
    
    Args:
        tour_graph: TourGraph object
        output_dir: Output directory
        format: 'web', 'standalone', 'vr'
    """
    # Create directory structure
    create_directory_structure(output_dir, format)
    
    # Copy panoramas
    for node in tour_graph.nodes.values():
        copy_panorama(node.panorama, output_dir)
    
    # Generate configuration
    config = generate_tour_config(tour_graph)
    save_json(config, output_dir / 'tour.json')
    
    # Generate viewer
    if format == 'web':
        generate_web_viewer(output_dir)
    elif format == 'standalone':
        generate_standalone(output_dir)
```

### 4.3 Deliverables
- [ ] Tour graph management
- [ ] Hotspot system
- [ ] Configuration interface
- [ ] Export functionality

### 4.4 Rubrik Penilaian Module 4
| Kriteria | Excellent (90-100) | Good (70-89) | Fair (50-69) |
|----------|-------------------|--------------|--------------|
| Graph Management | Full CRUD, validation | Basic management | Minimal |
| Hotspot System | Multiple types, customizable | Navigation only | Basic |
| Export | Multiple formats | Single format | Manual |

---

## Module 5: Interactive Viewer (15%)

### 5.1 Objectives
- Web-based panorama viewer
- Touch/mouse interaction
- VR support (bonus)

### 5.2 Features

#### A. Panorama Viewer (Python/Flask Backend)
```python
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('viewer.html')

@app.route('/api/tour')
def get_tour():
    """Return tour configuration."""
    return jsonify(load_tour_config())

@app.route('/api/panorama/<location_id>')
def get_panorama(location_id):
    """Serve panorama image."""
    return send_file(get_panorama_path(location_id))
```

#### B. Frontend Viewer (HTML/JS Template)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Virtual Tour</title>
    <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
</head>
<body>
    <a-scene>
        <a-sky id="panorama" src="" rotation="0 0 0"></a-sky>
        
        <!-- Hotspots dynamically added -->
        <a-entity id="hotspots"></a-entity>
        
        <a-camera>
            <a-cursor></a-cursor>
        </a-camera>
    </a-scene>
    
    <script src="tour-viewer.js"></script>
</body>
</html>
```

#### C. Controls
```python
class ViewerControls:
    """
    Controls untuk panorama viewer.
    """
    
    def handle_mouse_drag(self, dx, dy):
        """Handle mouse drag untuk rotation."""
        self.yaw += dx * self.sensitivity
        self.pitch = np.clip(self.pitch + dy * self.sensitivity, -90, 90)
    
    def handle_scroll(self, delta):
        """Handle scroll untuk zoom."""
        self.fov = np.clip(self.fov - delta * 5, 30, 120)
    
    def handle_touch(self, touches):
        """Handle touch gestures."""
        if len(touches) == 1:
            # Single touch - rotate
            self.handle_mouse_drag(touches[0].dx, touches[0].dy)
        elif len(touches) == 2:
            # Pinch - zoom
            dist = touch_distance(touches)
            self.handle_scroll(dist - self.last_pinch_dist)
```

### 5.3 Deliverables
- [ ] Basic web viewer
- [ ] Mouse/touch controls
- [ ] Hotspot interaction
- [ ] Navigation between locations
- [ ] Minimap/overview (bonus)
- [ ] VR mode (bonus)

### 5.4 Rubrik Penilaian Module 5
| Kriteria | Excellent (90-100) | Good (70-89) | Fair (50-69) |
|----------|-------------------|--------------|--------------|
| Viewer | Smooth, responsive | Functional | Basic |
| Interaction | Full gesture support | Mouse only | Limited |
| Navigation | Seamless transitions | Working | Abrupt |

---

## 5. Timeline

| Minggu | Aktivitas | Deliverables |
|--------|-----------|--------------|
| 1 | Setup & Module 1 | Capture tool, quality assessment |
| 2-3 | Module 2 (Stitching) | Feature matching, blending |
| 4 | Module 2 (360°) | Full panorama pipeline |
| 5-6 | Module 3 (View Synthesis) | View rendering, transitions |
| 7 | Module 4 (Tour Builder) | Graph, hotspots, export |
| 8 | Module 5 (Viewer) | Web viewer, interactions |
| 9 | Integration | Full system testing |
| 10 | Documentation & Demo | Final delivery |

---

## 6. Penilaian

### Komponen Nilai
| Komponen | Bobot |
|----------|-------|
| Module 1: Capture & Import | 15% |
| Module 2: Panorama Stitching | 30% |
| Module 3: View Synthesis | 25% |
| Module 4: Tour Builder | 15% |
| Module 5: Interactive Viewer | 15% |

### Bonus Points (+20% max)
- VR support: +10%
- Mobile app: +10%
- Learning-based depth: +5%
- Multi-resolution support: +5%

### Penalty
- Keterlambatan: -10% per minggu
- Plagiarisme: -100%

---

## 7. Referensi

1. Szeliski, R. (2022). "Computer Vision: Algorithms and Applications", Chapter 14
2. Brown, M. & Lowe, D. (2007). "Automatic Panoramic Image Stitching using Invariant Features"
3. Shum, H. Y. & Kang, S. B. (2000). "A Review of Image-Based Rendering Techniques"
4. A-Frame Documentation (https://aframe.io/docs/)
5. Pannellum Documentation (https://pannellum.org/)

---

## 8. Resources

### Sample Datasets
- Indoor panorama sequences
- Outdoor multi-view
- Museum/gallery images

### Code Templates
- Panorama stitching baseline
- Flask viewer template
- Tour configuration examples

### Tools
- Hugin (reference panorama software)
- Pannellum (web panorama viewer)
- A-Frame (VR framework)
