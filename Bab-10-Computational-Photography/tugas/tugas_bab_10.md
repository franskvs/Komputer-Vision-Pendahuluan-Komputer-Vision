# Tugas Bab 10: Computational Photography

## Informasi Umum
- **Mata Kuliah**: Praktikum Komputer Vision
- **Topik**: Computational Photography
- **Tujuan**: Mengimplementasikan dan memahami teknik-teknik computational photography

---

## Tugas 1: HDR Pipeline Lengkap (25 poin)

### Deskripsi
Implementasikan pipeline HDR imaging lengkap dari exposure stack hingga tone mapped output.

### Spesifikasi

```python
class HDRPipeline:
    """
    Pipeline HDR imaging lengkap.
    """
    
    def __init__(self):
        """
        Inisialisasi HDR pipeline.
        """
        pass
    
    def load_exposure_stack(self, image_paths: List[str], 
                           exposure_times: List[float]) -> Tuple[List[np.ndarray], np.ndarray]:
        """
        Load dan validasi exposure stack.
        
        Args:
            image_paths: List path ke images
            exposure_times: Exposure time untuk setiap image (dalam detik)
            
        Returns:
            Tuple of (images, exposure_times as numpy array)
        """
        # TODO: Implement
        # - Load semua images
        # - Validate ukuran sama
        # - Convert exposure times ke numpy array
        pass
    
    def estimate_camera_response(self, images: List[np.ndarray],
                                  exposure_times: np.ndarray,
                                  num_samples: int = 100) -> np.ndarray:
        """
        Estimasi Camera Response Function (CRF) menggunakan metode Debevec-Malik.
        
        Args:
            images: Exposure stack
            exposure_times: Exposure times
            num_samples: Jumlah sample pixels
            
        Returns:
            CRF curve (256 values untuk 8-bit images)
            
        Hint:
            - Set up linear system Ax = b
            - g(Z) = ln(E) + ln(dt)
            - Gunakan weighting function w(z)
        """
        # TODO: Implement Debevec-Malik CRF estimation
        pass
    
    def merge_to_hdr(self, images: List[np.ndarray],
                     exposure_times: np.ndarray,
                     crf: np.ndarray = None) -> np.ndarray:
        """
        Merge exposure stack ke HDR radiance map.
        
        Args:
            images: Exposure stack
            exposure_times: Exposure times
            crf: Camera response function (optional, use if available)
            
        Returns:
            HDR radiance map (float32)
        """
        # TODO: Implement HDR merging
        # - Weighted average dengan CRF
        # - Handle saturated pixels
        pass
    
    def tone_map_reinhard(self, hdr: np.ndarray, 
                          key: float = 0.18,
                          white: float = 1.0) -> np.ndarray:
        """
        Reinhard global tone mapping.
        
        Args:
            hdr: HDR radiance map
            key: Key value (brightness)
            white: White point
            
        Returns:
            Tone mapped LDR image (uint8)
        """
        # TODO: Implement
        # L_d = L * (1 + L/white²) / (1 + L)
        pass
    
    def tone_map_drago(self, hdr: np.ndarray, 
                       bias: float = 0.85) -> np.ndarray:
        """
        Drago logarithmic tone mapping.
        
        Args:
            hdr: HDR radiance map
            bias: Bias parameter
            
        Returns:
            Tone mapped LDR image
        """
        # TODO: Implement Drago operator
        pass
    
    def tone_map_mantiuk(self, hdr: np.ndarray) -> np.ndarray:
        """
        Mantiuk contrast preserving tone mapping.
        
        Returns:
            Tone mapped LDR image
        """
        # TODO: Implement atau gunakan OpenCV
        pass
    
    def exposure_fusion(self, images: List[np.ndarray]) -> np.ndarray:
        """
        Mertens exposure fusion (tanpa HDR).
        
        Args:
            images: Exposure stack
            
        Returns:
            Fused image (uint8)
        """
        # TODO: Implement dengan weight maps:
        # - Contrast
        # - Saturation
        # - Well-exposedness
        pass
```

### Test Cases

```python
def test_hdr_pipeline():
    pipeline = HDRPipeline()
    
    # Test dengan simulated exposures
    base_scene = create_hdr_scene()  # Your function
    exposures = [0.25, 0.5, 1.0, 2.0, 4.0]
    
    # Generate exposure stack
    stack = [simulate_exposure(base_scene, e) for e in exposures]
    times = np.array(exposures)
    
    # Estimate CRF
    crf = pipeline.estimate_camera_response(stack, times)
    assert crf.shape == (256,), "CRF should have 256 values"
    
    # Merge ke HDR
    hdr = pipeline.merge_to_hdr(stack, times, crf)
    assert hdr.dtype == np.float32, "HDR should be float32"
    
    # Tone mapping
    ldr_reinhard = pipeline.tone_map_reinhard(hdr)
    ldr_drago = pipeline.tone_map_drago(hdr)
    
    assert ldr_reinhard.dtype == np.uint8
    assert ldr_drago.dtype == np.uint8
    
    # Exposure fusion
    fused = pipeline.exposure_fusion(stack)
    assert fused.dtype == np.uint8
    
    print("All HDR tests passed!")
```

### Deliverables
1. Source code lengkap dengan dokumentasi
2. Hasil visualisasi exposure stack, HDR radiance map, dan berbagai tone mappings
3. Perbandingan kualitas (contrast, detail preservation) berbagai tone mappers
4. Analisis CRF yang diestimasi (plot curve)

---

## Tugas 2: Perbandingan Metode Denoising (25 poin)

### Deskripsi
Implementasikan dan bandingkan berbagai metode denoising dengan analisis mendalam.

### Spesifikasi

```python
class DenoisingComparison:
    """
    Framework untuk perbandingan metode denoising.
    """
    
    def add_noise(self, image: np.ndarray, noise_type: str, 
                  **params) -> np.ndarray:
        """
        Add noise ke image.
        
        Args:
            image: Clean image
            noise_type: 'gaussian', 'poisson', 'salt_pepper', 'speckle'
            params: Noise parameters (sigma, prob, etc.)
            
        Returns:
            Noisy image
        """
        # TODO: Implement berbagai jenis noise
        pass
    
    def denoise_gaussian(self, image: np.ndarray, 
                         sigma: float = 1.0) -> np.ndarray:
        """Gaussian filtering."""
        pass
    
    def denoise_bilateral(self, image: np.ndarray,
                          sigma_spatial: float = 75,
                          sigma_range: float = 75) -> np.ndarray:
        """Bilateral filtering."""
        pass
    
    def denoise_nlm(self, image: np.ndarray, h: float = 10) -> np.ndarray:
        """Non-Local Means."""
        pass
    
    def denoise_bm3d(self, image: np.ndarray, 
                     sigma: float = 25) -> np.ndarray:
        """
        BM3D denoising (simplified or using library).
        
        BM3D steps:
        1. Block matching - find similar blocks
        2. 3D transform (stack + DCT/wavelet)
        3. Collaborative filtering
        4. Aggregate results
        """
        # TODO: Implement simplified version atau gunakan library
        pass
    
    def denoise_total_variation(self, image: np.ndarray,
                                weight: float = 0.1,
                                iterations: int = 100) -> np.ndarray:
        """
        Total Variation denoising.
        
        Minimize: ||I - I_noisy||² + λ * TV(I)
        TV(I) = Σ |∇I|
        """
        # TODO: Implement TV denoising
        pass
    
    def compute_metrics(self, original: np.ndarray, 
                        denoised: np.ndarray) -> dict:
        """
        Compute quality metrics.
        
        Returns:
            Dict dengan PSNR, SSIM, MSE
        """
        # TODO: Implement
        pass
    
    def run_comparison(self, test_image: np.ndarray,
                       noise_sigmas: List[float] = [15, 25, 50]
                       ) -> pd.DataFrame:
        """
        Run comprehensive comparison.
        
        Returns:
            DataFrame dengan results untuk setiap method dan noise level
        """
        # TODO: Run all methods, compute metrics
        pass
```

### Test Cases

```python
def test_denoising():
    comparator = DenoisingComparison()
    
    # Load test image
    image = cv2.imread('test_image.png', 0)  # Grayscale
    
    # Test noise addition
    noisy_gauss = comparator.add_noise(image, 'gaussian', sigma=25)
    noisy_sp = comparator.add_noise(image, 'salt_pepper', prob=0.05)
    
    # Test denoising methods
    methods = ['gaussian', 'bilateral', 'nlm', 'tv']
    
    for method in methods:
        denoised = getattr(comparator, f'denoise_{method}')(noisy_gauss)
        metrics = comparator.compute_metrics(image, denoised)
        print(f"{method}: PSNR={metrics['psnr']:.2f}, SSIM={metrics['ssim']:.4f}")
    
    # Run full comparison
    results = comparator.run_comparison(image)
    print(results)
```

### Deliverables
1. Implementasi lengkap semua metode denoising
2. Tabel perbandingan PSNR/SSIM untuk berbagai noise levels
3. Visualisasi hasil denoising (zoomed in untuk detail)
4. Analisis:
   - Kelebihan/kekurangan masing-masing metode
   - Waktu komputasi
   - Preservasi edge vs smoothing

---

## Tugas 3: Super Resolution System (25 poin)

### Deskripsi
Bangun sistem super resolution dengan multiple methods dan evaluation framework.

### Spesifikasi

```python
class SuperResolutionSystem:
    """
    Comprehensive super resolution system.
    """
    
    def create_lr_image(self, hr_image: np.ndarray, 
                        scale: int = 4,
                        blur_sigma: float = 1.0,
                        noise_sigma: float = 5.0) -> np.ndarray:
        """
        Create realistic low-resolution image.
        
        Pipeline: HR -> Blur -> Downsample -> Add noise
        """
        pass
    
    def upscale_interpolation(self, lr: np.ndarray, scale: int,
                              method: str = 'bicubic') -> np.ndarray:
        """
        Interpolation-based upscaling.
        
        Methods: 'nearest', 'bilinear', 'bicubic', 'lanczos'
        """
        pass
    
    def upscale_ibp(self, lr: np.ndarray, scale: int,
                    iterations: int = 20) -> np.ndarray:
        """
        Iterative Back Projection.
        
        Iterate:
            1. Downscale HR estimate
            2. Compute error dengan LR
            3. Upscale error dan add ke HR estimate
        """
        pass
    
    def upscale_sparse_coding(self, lr: np.ndarray, scale: int,
                              dictionary_size: int = 512) -> np.ndarray:
        """
        Sparse coding super resolution.
        
        Steps:
            1. Extract patches dari LR
            2. Sparse coding dengan learned dictionary
            3. Reconstruct HR patches
            4. Aggregate
        """
        # TODO: Implement simplified version
        pass
    
    def upscale_edge_enhanced(self, lr: np.ndarray, 
                              scale: int) -> np.ndarray:
        """
        Edge-guided super resolution.
        
        1. Upscale dengan bicubic
        2. Detect edges
        3. Enhance edges directionally
        """
        pass
    
    def train_srcnn(self, train_data: List[Tuple[np.ndarray, np.ndarray]],
                    epochs: int = 100) -> 'SimpleSRCNN':
        """
        Train simple SRCNN model (jika menggunakan deep learning).
        
        Architecture:
            - Patch extraction: Conv 9x9, 64 filters
            - Non-linear mapping: Conv 1x1, 32 filters
            - Reconstruction: Conv 5x5, 1 filter
        """
        # TODO: Implement dengan PyTorch/TensorFlow (optional)
        pass
    
    def evaluate(self, hr: np.ndarray, sr: np.ndarray) -> dict:
        """
        Evaluate super resolution quality.
        
        Metrics:
            - PSNR
            - SSIM
            - LPIPS (jika available)
        """
        pass
```

### Deep Learning Model (Bonus)

```python
import torch
import torch.nn as nn

class SRCNN(nn.Module):
    """
    Super Resolution CNN (Dong et al., 2014)
    """
    
    def __init__(self):
        super().__init__()
        
        # TODO: Implement SRCNN architecture
        # Patch extraction dan representation
        self.conv1 = nn.Conv2d(1, 64, kernel_size=9, padding=4)
        
        # Non-linear mapping
        self.conv2 = nn.Conv2d(64, 32, kernel_size=1)
        
        # Reconstruction
        self.conv3 = nn.Conv2d(32, 1, kernel_size=5, padding=2)
        
        self.relu = nn.ReLU()
    
    def forward(self, x):
        """Forward pass."""
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.conv3(x)
        return x


class ESPCN(nn.Module):
    """
    Efficient Sub-Pixel CNN (Shi et al., 2016)
    """
    
    def __init__(self, scale_factor: int = 4):
        super().__init__()
        
        # TODO: Implement dengan sub-pixel convolution
        # (PixelShuffle layer)
        pass
```

### Test Cases

```python
def test_super_resolution():
    sr_system = SuperResolutionSystem()
    
    # Load HR image
    hr = cv2.imread('hr_image.png', 0)
    scale = 4
    
    # Create LR
    lr = sr_system.create_lr_image(hr, scale)
    
    # Test methods
    sr_bicubic = sr_system.upscale_interpolation(lr, scale, 'bicubic')
    sr_ibp = sr_system.upscale_ibp(lr, scale)
    sr_edge = sr_system.upscale_edge_enhanced(lr, scale)
    
    # Evaluate
    for name, sr in [('Bicubic', sr_bicubic), ('IBP', sr_ibp), ('Edge', sr_edge)]:
        metrics = sr_system.evaluate(hr, sr)
        print(f"{name}: PSNR={metrics['psnr']:.2f} dB")
```

### Deliverables
1. Implementasi semua metode super resolution
2. Perbandingan visual (side-by-side zoomed regions)
3. Tabel metrics untuk berbagai scale factors (2x, 3x, 4x)
4. Analisis trade-off speed vs quality
5. (Bonus) Deep learning model dengan training code

---

## Tugas 4: Proyek Akhir - Smart Photo Editor (25 poin)

### Deskripsi
Bangun aplikasi photo editor yang mengintegrasikan semua teknik computational photography.

### Spesifikasi

```python
class SmartPhotoEditor:
    """
    Comprehensive photo editor dengan computational photography techniques.
    """
    
    def __init__(self):
        self.image = None
        self.history = []  # Untuk undo
        self.max_history = 10
    
    def load_image(self, path: str) -> None:
        """Load image dan initialize."""
        pass
    
    def save_image(self, path: str) -> None:
        """Save current image."""
        pass
    
    def push_history(self) -> None:
        """Save state untuk undo."""
        pass
    
    def undo(self) -> bool:
        """Undo last operation."""
        pass
    
    # === HDR Features ===
    
    def auto_tone(self) -> None:
        """
        Auto tone adjustment (simplified local tone mapping).
        """
        pass
    
    def hdr_effect(self, strength: float = 0.5) -> None:
        """
        Simulate HDR effect dari single image.
        
        - Local contrast enhancement
        - Shadow/highlight recovery
        """
        pass
    
    def exposure_correction(self, ev: float) -> None:
        """
        Adjust exposure (EV stops).
        """
        pass
    
    # === Enhancement Features ===
    
    def denoise(self, strength: float = 1.0, 
                preserve_detail: bool = True) -> None:
        """
        Smart denoising dengan adaptive parameters.
        """
        pass
    
    def sharpen(self, amount: float = 1.0, 
                radius: float = 1.0,
                threshold: int = 0) -> None:
        """
        Unsharp masking dengan edge-aware processing.
        """
        pass
    
    def enhance_resolution(self, scale: float = 2.0) -> None:
        """
        AI-style upscaling dengan edge enhancement.
        """
        pass
    
    # === Restoration Features ===
    
    def remove_object(self, mask: np.ndarray) -> None:
        """
        Remove object menggunakan inpainting.
        """
        pass
    
    def deblur(self, blur_type: str = 'auto') -> None:
        """
        Deblur image (motion atau gaussian).
        """
        pass
    
    def restore_old_photo(self) -> None:
        """
        Restore old/damaged photo:
        - Remove scratches
        - Fix color fading
        - Reduce noise
        """
        pass
    
    # === Creative Effects ===
    
    def bokeh_effect(self, focus_mask: np.ndarray, 
                     blur_amount: float = 5.0) -> None:
        """
        Simulate depth of field / bokeh effect.
        """
        pass
    
    def night_mode(self) -> None:
        """
        Enhance night photos:
        - Noise reduction
        - Brightness boost
        - Color correction
        """
        pass
    
    def portrait_enhance(self, face_mask: np.ndarray = None) -> None:
        """
        Enhance portrait:
        - Skin smoothing
        - Eye enhancement
        - Lighting correction
        """
        pass
    
    # === Batch Processing ===
    
    def process_batch(self, image_paths: List[str],
                      operations: List[Tuple[str, dict]],
                      output_dir: str) -> None:
        """
        Batch process multiple images.
        
        Args:
            image_paths: List of input paths
            operations: List of (operation_name, params) tuples
            output_dir: Output directory
        """
        pass


class PhotoEditorGUI:
    """
    Simple GUI untuk photo editor (dengan OpenCV atau Tkinter).
    """
    
    def __init__(self):
        self.editor = SmartPhotoEditor()
        self.window_name = "Smart Photo Editor"
    
    def create_gui(self) -> None:
        """Create GUI dengan controls."""
        pass
    
    def run(self) -> None:
        """Run GUI main loop."""
        pass
```

### Fitur Wajib
1. **Basic Operations**: Load, save, undo
2. **HDR Enhancement**: Auto tone, HDR effect
3. **Denoising**: Dengan adjustable strength
4. **Sharpening**: Unsharp mask
5. **Inpainting**: Object removal
6. **Super Resolution**: Basic upscaling

### Fitur Bonus
- Deep learning based super resolution
- Face detection untuk portrait mode
- AI-based object removal (jika menggunakan pre-trained model)
- Real-time preview
- Histogram display
- Before/after comparison slider

### Test Scenarios

```python
def test_photo_editor():
    editor = SmartPhotoEditor()
    
    # Test workflow
    editor.load_image('test_photo.jpg')
    
    # Enhance underexposed photo
    editor.exposure_correction(1.5)
    editor.auto_tone()
    editor.denoise(strength=0.5)
    editor.sharpen(amount=0.8)
    
    editor.save_image('enhanced.jpg')
    
    # Test restoration
    editor.load_image('old_damaged_photo.jpg')
    editor.restore_old_photo()
    editor.save_image('restored.jpg')
    
    # Test object removal
    editor.load_image('photo_with_object.jpg')
    mask = create_object_mask()  # Manual atau automatic
    editor.remove_object(mask)
    editor.save_image('object_removed.jpg')
```

### Deliverables
1. **Source Code**:
   - Core editor class dengan semua fungsi
   - (Optional) GUI implementation

2. **Demo Video/Screenshots**:
   - Workflow demonstration
   - Before/after comparisons

3. **Documentation**:
   - User guide
   - API documentation
   - Limitations dan known issues

4. **Test Results**:
   - Test pada berbagai jenis foto
   - Performance metrics (processing time)
   - Quality assessment

---

## Kriteria Penilaian

### Tugas 1: HDR Pipeline (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| CRF Estimation | 6 | Implementasi Debevec-Malik |
| HDR Merging | 6 | Weighted averaging, handling saturated pixels |
| Tone Mapping | 8 | 2+ operators, quality output |
| Documentation | 5 | Visualisasi, analisis |

### Tugas 2: Denoising Comparison (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| Methods | 10 | 4+ methods implemented |
| Metrics | 5 | PSNR, SSIM correctly computed |
| Analysis | 7 | Comprehensive comparison |
| Code Quality | 3 | Clean, documented |

### Tugas 3: Super Resolution (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| Methods | 10 | 3+ methods implemented |
| Evaluation | 5 | Proper metrics, visual comparison |
| Analysis | 5 | Scale factors, trade-offs |
| Deep Learning | 5 | Bonus: working SRCNN/ESPCN |

### Tugas 4: Photo Editor (25 poin)
| Aspek | Bobot | Kriteria |
|-------|-------|----------|
| Features | 10 | All required features working |
| Integration | 5 | Smooth workflow |
| Usability | 5 | Easy to use, undo works |
| Documentation | 5 | User guide, API docs |

---

## Tips dan Panduan

### Untuk HDR
1. Mulai dengan exposure fusion (lebih mudah dari full HDR)
2. Gunakan OpenCV HDR functions untuk validasi
3. Perhatikan handling pixel saturated (0 dan 255)

### Untuk Denoising
1. Test pada synthetic noise dulu (ground truth tersedia)
2. BM3D bisa gunakan library seperti `bm3d` package
3. Perhatikan trade-off noise reduction vs detail preservation

### Untuk Super Resolution
1. Gunakan standard test images (Set5, Set14, BSD100)
2. Bicubic sebagai baseline
3. Deep learning methods butuh GPU untuk training reasonable

### Untuk Photo Editor
1. Implement core functions dulu, GUI terakhir
2. History/undo penting untuk usability
3. Parameter defaults yang reasonable

---

## Referensi Tambahan

1. **HDR**: [Debevec & Malik, SIGGRAPH 1997](http://www.pauldebevec.com/Research/HDR/)
2. **Tone Mapping**: [Reinhard et al., SIGGRAPH 2002](https://www.cs.utah.edu/~reinhard/cdrom/)
3. **Denoising**: [BM3D](http://www.cs.tut.fi/~foi/GCF-BM3D/)
4. **Super Resolution**: [SRCNN](https://arxiv.org/abs/1501.00092), [ESPCN](https://arxiv.org/abs/1609.05158)
5. **Inpainting**: [PatchMatch](https://gfx.cs.princeton.edu/gfx/pubs/Barnes_2009_PAR/index.php)

---

## Deadline dan Pengumpulan

- **Format**: ZIP file berisi source code, hasil, dan dokumentasi
- **Naming**: `Tugas10_NIM_Nama.zip`
- **Platform**: Upload ke sistem e-learning

**Selamat mengerjakan!**
