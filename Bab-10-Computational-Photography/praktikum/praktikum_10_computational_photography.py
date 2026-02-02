"""
Praktikum 10: Computational Photography
========================================
Implementasi berbagai teknik computational photography.

Topik:
1. HDR Imaging
2. Image Denoising
3. Image Deblurring
4. Super Resolution
5. Image Inpainting
6. Exposure Fusion

Requirements:
- opencv-contrib-python
- numpy
- matplotlib
- scikit-image
- torch (optional, untuk deep learning)
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from scipy import ndimage
from scipy.signal import convolve2d

# ============================================================================
# BAGIAN 1: HDR IMAGING
# ============================================================================

class HDRImaging:
    """
    High Dynamic Range imaging pipeline.
    """
    
    @staticmethod
    def create_exposure_stack(image: np.ndarray, exposures: List[float]
                              ) -> List[np.ndarray]:
        """
        Simulate exposure stack dari single image (untuk demo).
        
        Args:
            image: Input image
            exposures: List of exposure multipliers
            
        Returns:
            List of simulated exposures
        """
        stack = []
        for exp in exposures:
            adjusted = np.clip(image.astype(float) * exp, 0, 255).astype(np.uint8)
            stack.append(adjusted)
        return stack
    
    @staticmethod
    def compute_weights(image: np.ndarray) -> np.ndarray:
        """
        Compute weight map untuk exposure fusion (Mertens method).
        
        Berdasarkan:
        - Contrast
        - Saturation
        - Well-exposedness
        """
        # Convert to grayscale untuk contrast
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Contrast (Laplacian magnitude)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        contrast = np.abs(laplacian)
        
        # Saturation (untuk color images)
        if len(image.shape) == 3:
            saturation = image.std(axis=2)
        else:
            saturation = np.ones_like(gray, dtype=float)
        
        # Well-exposedness (prefer mid-tones)
        sigma = 0.2
        if len(image.shape) == 3:
            exposedness = np.exp(-0.5 * ((image.astype(float) / 255 - 0.5) ** 2) / sigma**2)
            exposedness = exposedness.prod(axis=2)
        else:
            exposedness = np.exp(-0.5 * ((gray.astype(float) / 255 - 0.5) ** 2) / sigma**2)
        
        # Combine weights
        weight = (contrast ** 1.0) * (saturation ** 1.0) * (exposedness ** 1.0)
        weight = weight + 1e-12  # Avoid division by zero
        
        return weight
    
    def exposure_fusion(self, images: List[np.ndarray]) -> np.ndarray:
        """
        Mertens exposure fusion - merge exposures without HDR creation.
        
        Args:
            images: List of differently exposed images
            
        Returns:
            Fused image
        """
        # Compute weights untuk setiap image
        weights = []
        for img in images:
            w = self.compute_weights(img)
            weights.append(w)
        
        # Normalize weights
        weight_sum = np.sum(weights, axis=0)
        weights = [w / weight_sum for w in weights]
        
        # Weighted sum
        result = np.zeros_like(images[0], dtype=float)
        for img, w in zip(images, weights):
            if len(img.shape) == 3:
                result += img.astype(float) * w[:, :, np.newaxis]
            else:
                result += img.astype(float) * w
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def pyramid_fusion(self, images: List[np.ndarray], levels: int = 5
                      ) -> np.ndarray:
        """
        Laplacian pyramid fusion untuk seamless blending.
        """
        # Compute weights
        weights = []
        for img in images:
            w = self.compute_weights(img)
            weights.append(w)
        
        # Normalize
        weight_sum = np.sum(weights, axis=0) + 1e-12
        weights = [w / weight_sum for w in weights]
        
        # Build Gaussian pyramids untuk weights
        weight_pyramids = []
        for w in weights:
            pyr = [w]
            for _ in range(levels - 1):
                pyr.append(cv2.pyrDown(pyr[-1]))
            weight_pyramids.append(pyr)
        
        # Build Laplacian pyramids untuk images
        img_pyramids = []
        for img in images:
            img_f = img.astype(float)
            gaussian_pyr = [img_f]
            for _ in range(levels - 1):
                gaussian_pyr.append(cv2.pyrDown(gaussian_pyr[-1]))
            
            laplacian_pyr = []
            for i in range(levels - 1):
                expanded = cv2.pyrUp(gaussian_pyr[i + 1],
                                    dstsize=(gaussian_pyr[i].shape[1], 
                                            gaussian_pyr[i].shape[0]))
                laplacian = gaussian_pyr[i] - expanded
                laplacian_pyr.append(laplacian)
            laplacian_pyr.append(gaussian_pyr[-1])
            
            img_pyramids.append(laplacian_pyr)
        
        # Blend at each level
        blended_pyr = []
        for level in range(levels):
            blended = np.zeros_like(img_pyramids[0][level])
            for i in range(len(images)):
                w = weight_pyramids[i][level]
                if len(blended.shape) == 3:
                    w = w[:, :, np.newaxis]
                blended += img_pyramids[i][level] * w
            blended_pyr.append(blended)
        
        # Reconstruct
        result = blended_pyr[-1]
        for i in range(levels - 2, -1, -1):
            expanded = cv2.pyrUp(result, dstsize=(blended_pyr[i].shape[1],
                                                  blended_pyr[i].shape[0]))
            result = expanded + blended_pyr[i]
        
        return np.clip(result, 0, 255).astype(np.uint8)


def demo_hdr_imaging():
    """Demo HDR imaging dan exposure fusion."""
    print("=" * 60)
    print("DEMO: HDR Imaging dan Exposure Fusion")
    print("=" * 60)
    
    # Buat scene dengan high dynamic range (simulasi)
    h, w = 300, 400
    
    # Simulated HDR scene
    scene = np.zeros((h, w, 3), dtype=float)
    
    # Dark region
    scene[:, :w//3] = [30, 40, 50]
    
    # Mid region
    scene[:, w//3:2*w//3] = [100, 120, 130]
    
    # Bright region (simulating window/light)
    scene[:, 2*w//3:] = [220, 230, 240]
    
    # Add details
    cv2.circle(scene, (50, 150), 30, (80, 90, 100), -1)
    cv2.rectangle(scene, (150, 100), (250, 200), (150, 160, 170), -1)
    cv2.circle(scene, (350, 150), 40, (255, 255, 200), -1)  # Bright light
    
    # Create exposure stack
    hdr = HDRImaging()
    
    # Simulate different exposures
    exposures = [0.3, 1.0, 3.0]
    exposure_stack = []
    
    for exp in exposures:
        img = np.clip(scene * exp, 0, 255).astype(np.uint8)
        exposure_stack.append(img)
    
    # Exposure fusion
    fused_simple = hdr.exposure_fusion(exposure_stack)
    fused_pyramid = hdr.pyramid_fusion(exposure_stack)
    
    # OpenCV HDR (if available)
    try:
        merge_debevec = cv2.createMergeDebevec()
        hdr_image = merge_debevec.process(exposure_stack, 
                                          times=np.array(exposures, dtype=np.float32))
        
        tonemap = cv2.createTonemap(gamma=2.2)
        ldr = tonemap.process(hdr_image)
        ldr = np.clip(ldr * 255, 0, 255).astype(np.uint8)
    except:
        ldr = fused_simple
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(exposure_stack[0], cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title(f'Under-exposed (x{exposures[0]})')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(exposure_stack[1], cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f'Normal (x{exposures[1]})')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(exposure_stack[2], cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title(f'Over-exposed (x{exposures[2]})')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(fused_simple, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Simple Fusion')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(fused_pyramid, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Pyramid Fusion')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(ldr, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('HDR + Tone Mapping')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_hdr_fusion.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_hdr_fusion.png")


# ============================================================================
# BAGIAN 2: IMAGE DENOISING
# ============================================================================

class ImageDenoising:
    """
    Berbagai metode image denoising.
    """
    
    @staticmethod
    def add_gaussian_noise(image: np.ndarray, sigma: float = 25) -> np.ndarray:
        """Add Gaussian noise ke image."""
        noise = np.random.normal(0, sigma, image.shape)
        noisy = image.astype(float) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)
    
    @staticmethod
    def add_salt_pepper_noise(image: np.ndarray, prob: float = 0.05) -> np.ndarray:
        """Add salt and pepper noise."""
        noisy = image.copy()
        
        # Salt
        salt_mask = np.random.random(image.shape[:2]) < prob / 2
        noisy[salt_mask] = 255
        
        # Pepper
        pepper_mask = np.random.random(image.shape[:2]) < prob / 2
        noisy[pepper_mask] = 0
        
        return noisy
    
    @staticmethod
    def gaussian_filter(image: np.ndarray, sigma: float = 1.5) -> np.ndarray:
        """Gaussian filtering."""
        return cv2.GaussianBlur(image, (0, 0), sigma)
    
    @staticmethod
    def median_filter(image: np.ndarray, ksize: int = 5) -> np.ndarray:
        """Median filtering."""
        return cv2.medianBlur(image, ksize)
    
    @staticmethod
    def bilateral_filter(image: np.ndarray, d: int = 9, 
                        sigma_color: float = 75, 
                        sigma_space: float = 75) -> np.ndarray:
        """Bilateral filtering - edge preserving."""
        return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    
    def non_local_means(self, image: np.ndarray, h: float = 10,
                       template_size: int = 7, search_size: int = 21
                       ) -> np.ndarray:
        """
        Non-Local Means denoising.
        """
        if len(image.shape) == 3:
            return cv2.fastNlMeansDenoisingColored(image, None, h, h,
                                                   template_size, search_size)
        else:
            return cv2.fastNlMeansDenoising(image, None, h,
                                           template_size, search_size)
    
    def simple_nlm(self, image: np.ndarray, h: float = 10, 
                   patch_size: int = 5, search_size: int = 11) -> np.ndarray:
        """
        Simplified Non-Local Means implementation.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        gray = gray.astype(float)
        height, width = gray.shape
        half_patch = patch_size // 2
        half_search = search_size // 2
        
        padded = np.pad(gray, half_search + half_patch, mode='reflect')
        result = np.zeros_like(gray)
        
        # Simplified version - process every Nth pixel
        step = 2
        
        for i in range(0, height, step):
            for j in range(0, width, step):
                # Reference patch
                pi = i + half_search + half_patch
                pj = j + half_search + half_patch
                ref_patch = padded[pi - half_patch:pi + half_patch + 1,
                                  pj - half_patch:pj + half_patch + 1]
                
                weighted_sum = 0
                weight_sum = 0
                
                # Search dalam window
                for di in range(-half_search, half_search + 1, 2):
                    for dj in range(-half_search, half_search + 1, 2):
                        ni = pi + di
                        nj = pj + dj
                        
                        neighbor_patch = padded[ni - half_patch:ni + half_patch + 1,
                                               nj - half_patch:nj + half_patch + 1]
                        
                        # Patch distance
                        dist = np.sum((ref_patch - neighbor_patch) ** 2)
                        
                        # Weight
                        weight = np.exp(-dist / (h ** 2))
                        
                        weighted_sum += weight * padded[ni, nj]
                        weight_sum += weight
                
                result[i, j] = weighted_sum / weight_sum
        
        # Fill gaps dengan interpolation
        if step > 1:
            result = cv2.resize(result, (width, height), interpolation=cv2.INTER_LINEAR)
        
        return result.astype(np.uint8)


def demo_denoising():
    """Demo berbagai metode denoising."""
    print("\n" + "=" * 60)
    print("DEMO: Image Denoising")
    print("=" * 60)
    
    # Buat test image
    h, w = 256, 256
    image = np.zeros((h, w), dtype=np.uint8)
    
    # Add patterns
    cv2.rectangle(image, (50, 50), (150, 150), 200, -1)
    cv2.circle(image, (190, 190), 40, 180, -1)
    cv2.line(image, (20, 220), (230, 220), 150, 3)
    
    # Add texture
    for i in range(0, w, 20):
        for j in range(0, h, 20):
            cv2.circle(image, (i + 10, j + 10), 3, 100, -1)
    
    denoiser = ImageDenoising()
    
    # Add noise
    sigma = 25
    noisy_gaussian = denoiser.add_gaussian_noise(image, sigma)
    noisy_sp = denoiser.add_salt_pepper_noise(image, 0.05)
    
    # Denoise
    denoised_gaussian = denoiser.gaussian_filter(noisy_gaussian, sigma=1.5)
    denoised_median = denoiser.median_filter(noisy_sp, ksize=5)
    denoised_bilateral = denoiser.bilateral_filter(noisy_gaussian, d=9)
    denoised_nlm = denoiser.non_local_means(noisy_gaussian, h=10)
    
    # Visualize
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    axes[0, 0].imshow(image, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(noisy_gaussian, cmap='gray')
    axes[0, 1].set_title(f'Gaussian Noise (σ={sigma})')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(denoised_gaussian, cmap='gray')
    axes[0, 2].set_title('Gaussian Filter')
    axes[0, 2].axis('off')
    
    axes[0, 3].imshow(denoised_bilateral, cmap='gray')
    axes[0, 3].set_title('Bilateral Filter')
    axes[0, 3].axis('off')
    
    axes[1, 0].imshow(noisy_sp, cmap='gray')
    axes[1, 0].set_title('Salt & Pepper Noise')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(denoised_median, cmap='gray')
    axes[1, 1].set_title('Median Filter')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(denoised_nlm, cmap='gray')
    axes[1, 2].set_title('Non-Local Means')
    axes[1, 2].axis('off')
    
    # PSNR comparison
    def psnr(original, compressed):
        mse = np.mean((original.astype(float) - compressed.astype(float)) ** 2)
        if mse == 0:
            return float('inf')
        return 20 * np.log10(255.0 / np.sqrt(mse))
    
    psnr_noisy = psnr(image, noisy_gaussian)
    psnr_gaussian = psnr(image, denoised_gaussian)
    psnr_bilateral = psnr(image, denoised_bilateral)
    psnr_nlm = psnr(image, denoised_nlm)
    
    axes[1, 3].bar(['Noisy', 'Gaussian', 'Bilateral', 'NLM'],
                   [psnr_noisy, psnr_gaussian, psnr_bilateral, psnr_nlm])
    axes[1, 3].set_ylabel('PSNR (dB)')
    axes[1, 3].set_title('Quality Comparison')
    
    plt.tight_layout()
    plt.savefig('output_denoising.png', dpi=150)
    plt.show()
    
    print(f"PSNR - Noisy: {psnr_noisy:.2f} dB")
    print(f"PSNR - Gaussian Filter: {psnr_gaussian:.2f} dB")
    print(f"PSNR - Bilateral Filter: {psnr_bilateral:.2f} dB")
    print(f"PSNR - NLM: {psnr_nlm:.2f} dB")
    print("Hasil disimpan: output_denoising.png")


# ============================================================================
# BAGIAN 3: IMAGE DEBLURRING
# ============================================================================

class ImageDeblurring:
    """
    Image deblurring / deconvolution.
    """
    
    @staticmethod
    def create_motion_blur_kernel(length: int, angle: float) -> np.ndarray:
        """Create motion blur kernel."""
        kernel = np.zeros((length, length), dtype=np.float32)
        center = length // 2
        
        # Create line
        for i in range(length):
            x = int(center + (i - center) * np.cos(np.radians(angle)))
            y = int(center + (i - center) * np.sin(np.radians(angle)))
            if 0 <= x < length and 0 <= y < length:
                kernel[y, x] = 1
        
        return kernel / kernel.sum()
    
    @staticmethod
    def create_gaussian_blur_kernel(size: int, sigma: float) -> np.ndarray:
        """Create Gaussian blur kernel."""
        kernel = cv2.getGaussianKernel(size, sigma)
        return kernel @ kernel.T
    
    @staticmethod
    def apply_blur(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """Apply blur ke image."""
        return cv2.filter2D(image, -1, kernel)
    
    def wiener_filter(self, blurred: np.ndarray, kernel: np.ndarray,
                     noise_var: float = 0.01) -> np.ndarray:
        """
        Wiener filter deconvolution.
        
        Args:
            blurred: Blurred image
            kernel: Blur kernel (PSF)
            noise_var: Noise variance estimate (NSR)
            
        Returns:
            Deblurred image
        """
        # Pad kernel ke ukuran image
        h, w = blurred.shape[:2]
        kernel_padded = np.zeros((h, w), dtype=np.float32)
        kh, kw = kernel.shape
        kernel_padded[:kh, :kw] = kernel
        
        # FFT
        if len(blurred.shape) == 3:
            result = np.zeros_like(blurred, dtype=np.float32)
            for c in range(3):
                result[:, :, c] = self._wiener_channel(blurred[:, :, c], 
                                                       kernel_padded, noise_var)
            return np.clip(result, 0, 255).astype(np.uint8)
        else:
            result = self._wiener_channel(blurred, kernel_padded, noise_var)
            return np.clip(result, 0, 255).astype(np.uint8)
    
    def _wiener_channel(self, channel: np.ndarray, kernel: np.ndarray,
                        noise_var: float) -> np.ndarray:
        """Wiener filter untuk single channel."""
        # FFT
        F_img = np.fft.fft2(channel.astype(np.float32))
        F_kernel = np.fft.fft2(kernel)
        
        # Wiener filter
        F_kernel_conj = np.conj(F_kernel)
        F_kernel_abs2 = np.abs(F_kernel) ** 2
        
        F_result = (F_kernel_conj * F_img) / (F_kernel_abs2 + noise_var)
        
        result = np.real(np.fft.ifft2(F_result))
        return np.fft.fftshift(result)
    
    def richardson_lucy(self, blurred: np.ndarray, kernel: np.ndarray,
                       num_iterations: int = 30) -> np.ndarray:
        """
        Richardson-Lucy deconvolution.
        """
        kernel_flip = np.flip(kernel)
        
        if len(blurred.shape) == 3:
            result = np.zeros_like(blurred, dtype=np.float32)
            for c in range(3):
                result[:, :, c] = self._rl_channel(blurred[:, :, c].astype(np.float32),
                                                   kernel, kernel_flip, num_iterations)
            return np.clip(result, 0, 255).astype(np.uint8)
        else:
            result = self._rl_channel(blurred.astype(np.float32), 
                                     kernel, kernel_flip, num_iterations)
            return np.clip(result, 0, 255).astype(np.uint8)
    
    def _rl_channel(self, channel: np.ndarray, kernel: np.ndarray,
                    kernel_flip: np.ndarray, num_iterations: int) -> np.ndarray:
        """RL deconvolution untuk single channel."""
        estimate = channel.copy()
        
        for _ in range(num_iterations):
            convolved = cv2.filter2D(estimate, -1, kernel)
            convolved = np.maximum(convolved, 1e-10)
            
            ratio = channel / convolved
            correction = cv2.filter2D(ratio, -1, kernel_flip)
            
            estimate = estimate * correction
        
        return estimate


def demo_deblurring():
    """Demo image deblurring."""
    print("\n" + "=" * 60)
    print("DEMO: Image Deblurring")
    print("=" * 60)
    
    # Create test image
    h, w = 256, 256
    image = np.zeros((h, w), dtype=np.uint8)
    
    # Sharp edges dan patterns
    cv2.rectangle(image, (60, 60), (130, 130), 220, -1)
    cv2.circle(image, (180, 100), 35, 200, -1)
    cv2.putText(image, "TEXT", (80, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                1, 180, 2)
    
    # Add fine details
    for i in range(0, w, 15):
        cv2.line(image, (i, 220), (i, 250), 150, 1)
    
    deblur = ImageDeblurring()
    
    # Motion blur
    motion_kernel = deblur.create_motion_blur_kernel(15, 0)
    blurred_motion = deblur.apply_blur(image, motion_kernel)
    
    # Gaussian blur
    gaussian_kernel = deblur.create_gaussian_blur_kernel(15, 3)
    blurred_gaussian = deblur.apply_blur(image, gaussian_kernel)
    
    # Deblur
    deblurred_wiener_motion = deblur.wiener_filter(blurred_motion, motion_kernel, 0.01)
    deblurred_rl_motion = deblur.richardson_lucy(blurred_motion, motion_kernel, 30)
    
    deblurred_wiener_gaussian = deblur.wiener_filter(blurred_gaussian, gaussian_kernel, 0.01)
    deblurred_rl_gaussian = deblur.richardson_lucy(blurred_gaussian, gaussian_kernel, 30)
    
    # Visualize
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    
    # Row 1: Original dan kernels
    axes[0, 0].imshow(image, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(motion_kernel, cmap='gray')
    axes[0, 1].set_title('Motion Blur Kernel')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(gaussian_kernel, cmap='gray')
    axes[0, 2].set_title('Gaussian Blur Kernel')
    axes[0, 2].axis('off')
    
    # Row 2: Motion blur
    axes[1, 0].imshow(blurred_motion, cmap='gray')
    axes[1, 0].set_title('Motion Blurred')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(deblurred_wiener_motion, cmap='gray')
    axes[1, 1].set_title('Wiener Deblurred')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(deblurred_rl_motion, cmap='gray')
    axes[1, 2].set_title('Richardson-Lucy')
    axes[1, 2].axis('off')
    
    # Row 3: Gaussian blur
    axes[2, 0].imshow(blurred_gaussian, cmap='gray')
    axes[2, 0].set_title('Gaussian Blurred')
    axes[2, 0].axis('off')
    
    axes[2, 1].imshow(deblurred_wiener_gaussian, cmap='gray')
    axes[2, 1].set_title('Wiener Deblurred')
    axes[2, 1].axis('off')
    
    axes[2, 2].imshow(deblurred_rl_gaussian, cmap='gray')
    axes[2, 2].set_title('Richardson-Lucy')
    axes[2, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_deblurring.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_deblurring.png")


# ============================================================================
# BAGIAN 4: SUPER RESOLUTION
# ============================================================================

class SuperResolution:
    """
    Image super resolution methods.
    """
    
    @staticmethod
    def bicubic_upscale(image: np.ndarray, scale: int = 2) -> np.ndarray:
        """Bicubic interpolation upscaling."""
        h, w = image.shape[:2]
        return cv2.resize(image, (w * scale, h * scale), 
                         interpolation=cv2.INTER_CUBIC)
    
    @staticmethod
    def lanczos_upscale(image: np.ndarray, scale: int = 2) -> np.ndarray:
        """Lanczos interpolation upscaling."""
        h, w = image.shape[:2]
        return cv2.resize(image, (w * scale, h * scale), 
                         interpolation=cv2.INTER_LANCZOS4)
    
    def edge_directed_upscale(self, image: np.ndarray, scale: int = 2
                              ) -> np.ndarray:
        """
        Simple edge-directed interpolation.
        """
        # First bicubic upscale
        upscaled = self.bicubic_upscale(image, scale)
        
        if len(upscaled.shape) == 3:
            gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
        else:
            gray = upscaled
        
        # Compute gradients
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Edge magnitude
        edge_mag = np.sqrt(gx**2 + gy**2)
        
        # Sharpen edges
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]], dtype=np.float32)
        
        sharpened = cv2.filter2D(upscaled, -1, kernel)
        
        # Blend based on edge strength
        if len(upscaled.shape) == 3:
            edge_mag = edge_mag[:, :, np.newaxis]
        
        edge_mag = edge_mag / (edge_mag.max() + 1e-10)
        
        result = upscaled.astype(float) * (1 - edge_mag * 0.3) + \
                 sharpened.astype(float) * (edge_mag * 0.3)
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def iterative_back_projection(self, lr_image: np.ndarray, scale: int = 2,
                                   iterations: int = 10) -> np.ndarray:
        """
        Iterative Back Projection super resolution.
        """
        # Initial estimate
        hr_estimate = self.bicubic_upscale(lr_image, scale)
        
        h, w = lr_image.shape[:2]
        
        for _ in range(iterations):
            # Downscale estimate
            lr_estimate = cv2.resize(hr_estimate, (w, h), 
                                    interpolation=cv2.INTER_CUBIC)
            
            # Compute error
            error = lr_image.astype(float) - lr_estimate.astype(float)
            
            # Upscale error
            error_upscaled = cv2.resize(error, (w * scale, h * scale),
                                       interpolation=cv2.INTER_CUBIC)
            
            # Back project
            hr_estimate = hr_estimate.astype(float) + 0.5 * error_upscaled
            hr_estimate = np.clip(hr_estimate, 0, 255).astype(np.uint8)
        
        return hr_estimate


def demo_super_resolution():
    """Demo super resolution methods."""
    print("\n" + "=" * 60)
    print("DEMO: Super Resolution")
    print("=" * 60)
    
    # Create high-res test image
    h, w = 256, 256
    hr_image = np.zeros((h, w), dtype=np.uint8)
    
    # Fine details
    cv2.rectangle(hr_image, (40, 40), (100, 100), 220, -1)
    cv2.circle(hr_image, (170, 70), 25, 200, -1)
    cv2.putText(hr_image, "SR", (80, 180), cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, 180, 2)
    
    # Fine lines
    for i in range(0, w, 8):
        cv2.line(hr_image, (i, 200), (i, 250), 150, 1)
    
    # Create low-res by downsampling
    scale = 4
    lr_image = cv2.resize(hr_image, (w // scale, h // scale),
                         interpolation=cv2.INTER_CUBIC)
    
    sr = SuperResolution()
    
    # Upscale dengan berbagai metode
    bicubic_up = sr.bicubic_upscale(lr_image, scale)
    lanczos_up = sr.lanczos_upscale(lr_image, scale)
    edge_up = sr.edge_directed_upscale(lr_image, scale)
    ibp_up = sr.iterative_back_projection(lr_image, scale, iterations=10)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(hr_image, cmap='gray')
    axes[0, 0].set_title('Original HR')
    axes[0, 0].axis('off')
    
    # LR dengan nearest neighbor untuk visualization
    lr_display = cv2.resize(lr_image, (w, h), interpolation=cv2.INTER_NEAREST)
    axes[0, 1].imshow(lr_display, cmap='gray')
    axes[0, 1].set_title(f'Low Resolution ({w//scale}x{h//scale})')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(bicubic_up, cmap='gray')
    axes[0, 2].set_title('Bicubic Upscale')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(lanczos_up, cmap='gray')
    axes[1, 0].set_title('Lanczos Upscale')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(edge_up, cmap='gray')
    axes[1, 1].set_title('Edge-Directed')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(ibp_up, cmap='gray')
    axes[1, 2].set_title('Iterative Back Projection')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_super_resolution.png', dpi=150)
    plt.show()
    
    # PSNR
    def psnr(a, b):
        mse = np.mean((a.astype(float) - b.astype(float)) ** 2)
        if mse == 0:
            return float('inf')
        return 20 * np.log10(255.0 / np.sqrt(mse))
    
    print(f"PSNR - Bicubic: {psnr(hr_image, bicubic_up):.2f} dB")
    print(f"PSNR - Lanczos: {psnr(hr_image, lanczos_up):.2f} dB")
    print(f"PSNR - Edge-Directed: {psnr(hr_image, edge_up):.2f} dB")
    print(f"PSNR - IBP: {psnr(hr_image, ibp_up):.2f} dB")
    print("Hasil disimpan: output_super_resolution.png")


# ============================================================================
# BAGIAN 5: IMAGE INPAINTING
# ============================================================================

class ImageInpainting:
    """
    Image inpainting methods.
    """
    
    @staticmethod
    def telea_inpaint(image: np.ndarray, mask: np.ndarray, 
                     radius: int = 3) -> np.ndarray:
        """
        Telea's fast marching method inpainting.
        """
        return cv2.inpaint(image, mask, radius, cv2.INPAINT_TELEA)
    
    @staticmethod
    def navier_stokes_inpaint(image: np.ndarray, mask: np.ndarray,
                             radius: int = 3) -> np.ndarray:
        """
        Navier-Stokes based inpainting.
        """
        return cv2.inpaint(image, mask, radius, cv2.INPAINT_NS)
    
    def diffusion_inpaint(self, image: np.ndarray, mask: np.ndarray,
                          iterations: int = 100) -> np.ndarray:
        """
        Simple diffusion-based inpainting.
        """
        result = image.copy().astype(float)
        mask_bool = mask > 0
        
        kernel = np.array([[0, 1, 0],
                          [1, 0, 1],
                          [0, 1, 0]], dtype=float) / 4
        
        for _ in range(iterations):
            if len(result.shape) == 3:
                for c in range(3):
                    avg = cv2.filter2D(result[:, :, c], -1, kernel)
                    result[:, :, c][mask_bool] = avg[mask_bool]
            else:
                avg = cv2.filter2D(result, -1, kernel)
                result[mask_bool] = avg[mask_bool]
        
        return np.clip(result, 0, 255).astype(np.uint8)


def demo_inpainting():
    """Demo image inpainting."""
    print("\n" + "=" * 60)
    print("DEMO: Image Inpainting")
    print("=" * 60)
    
    # Create test image
    h, w = 256, 256
    image = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Background gradient
    for x in range(w):
        image[:, x] = [int(100 + 100 * x / w), 
                       int(150 - 50 * x / w), 
                       int(50 + 150 * x / w)]
    
    # Add objects
    cv2.circle(image, (80, 80), 40, (200, 100, 50), -1)
    cv2.rectangle(image, (150, 60), (220, 130), (50, 150, 200), -1)
    cv2.circle(image, (128, 180), 35, (100, 200, 100), -1)
    
    # Create mask (region to inpaint)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (128, 128), 40, 255, -1)  # Center region
    cv2.rectangle(mask, (180, 160), (230, 210), 255, -1)  # Corner
    
    # Damaged image
    damaged = image.copy()
    damaged[mask > 0] = [0, 0, 0]
    
    inpainter = ImageInpainting()
    
    # Inpaint
    result_telea = inpainter.telea_inpaint(damaged, mask, radius=5)
    result_ns = inpainter.navier_stokes_inpaint(damaged, mask, radius=5)
    result_diffusion = inpainter.diffusion_inpaint(damaged, mask, iterations=200)
    
    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(mask, cmap='gray')
    axes[0, 1].set_title('Mask')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(cv2.cvtColor(damaged, cv2.COLOR_BGR2RGB))
    axes[0, 2].set_title('Damaged')
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(result_telea, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title('Telea Inpainting')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(result_ns, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Navier-Stokes Inpainting')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(cv2.cvtColor(result_diffusion, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('Diffusion Inpainting')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('output_inpainting.png', dpi=150)
    plt.show()
    
    print("Hasil disimpan: output_inpainting.png")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function untuk menjalankan semua demo."""
    print("=" * 70)
    print("PRAKTIKUM 10: COMPUTATIONAL PHOTOGRAPHY")
    print("=" * 70)
    
    demos = [
        ("1. HDR Imaging & Exposure Fusion", demo_hdr_imaging),
        ("2. Image Denoising", demo_denoising),
        ("3. Image Deblurring", demo_deblurring),
        ("4. Super Resolution", demo_super_resolution),
        ("5. Image Inpainting", demo_inpainting),
    ]
    
    print("\nPilih demo yang ingin dijalankan:")
    for i, (name, _) in enumerate(demos):
        print(f"  {name}")
    print("  6. Jalankan Semua")
    print("  0. Keluar")
    
    while True:
        try:
            choice = input("\nMasukkan pilihan (0-6): ").strip()
            
            if choice == '0':
                print("Terima kasih!")
                break
            elif choice == '6':
                for name, func in demos:
                    print(f"\n>>> Menjalankan {name}...")
                    func()
                break
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(demos):
                    demos[idx][1]()
                else:
                    print("Pilihan tidak valid!")
        except ValueError:
            print("Input tidak valid!")
        except KeyboardInterrupt:
            print("\nDibatalkan.")
            break


if __name__ == "__main__":
    main()
