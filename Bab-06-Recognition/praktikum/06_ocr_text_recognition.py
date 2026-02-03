"""
=============================================================================
PRAKTIKUM 06 - OCR DAN TEXT RECOGNITION
=============================================================================
Program ini mendemonstrasikan Optical Character Recognition (OCR) dan
Text Detection/Recognition dalam gambar.

Konsep yang dipelajari:
1. Text Detection - menemukan lokasi teks dalam gambar
2. Text Recognition - membaca/mengenali karakter
3. Pre-processing untuk OCR
4. Scene text recognition vs document OCR

Kebutuhan:
- opencv-python >= 4.8.0
- numpy
- pytesseract (optional, untuk actual OCR)
- tesseract-ocr (system package)

Instalasi tesseract:
- Ubuntu/Debian: sudo apt install tesseract-ocr
- Windows: Download dari GitHub
- macOS: brew install tesseract

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import os

# Check for pytesseract
TESSERACT_AVAILABLE = False
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    print("[INFO] pytesseract tersedia - OCR aktif")
except ImportError:
    print("[INFO] pytesseract tidak tersedia - menggunakan mode simulasi")


def print_ocr_concepts():
    """
    Menampilkan konsep OCR dan text recognition.
    """
    print("\n" + "="*70)
    print("KONSEP OCR DAN TEXT RECOGNITION")
    print("="*70)
    
    print("""
    [DEFINISI]
    ─────────────────────────────────────────────────────────────────────
    
    OCR (Optical Character Recognition):
    Teknologi untuk mengkonversi berbagai jenis dokumen
    (scanned paper, PDF, foto) menjadi editable text.
    
    Text Detection:
    Menemukan LOKASI teks dalam gambar (bounding boxes)
    
    Text Recognition:
    MEMBACA karakter/kata dari region yang terdeteksi
    
    
    [PIPELINE OCR]
    ─────────────────────────────────────────────────────────────────────
    
    Input Image
         │
         ▼
    ┌─────────────────┐
    │  Pre-processing │ ── Binarization, denoising, deskewing
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  Text Detection │ ── Find text regions (EAST, CRAFT, etc.)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Text Recognition│ ── Character/word recognition (Tesseract, CRNN)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Post-processing │ ── Spell check, language model
    └────────┬────────┘
             │
             ▼
       Output Text
    
    
    [JENIS TEXT RECOGNITION]
    ─────────────────────────────────────────────────────────────────────
    
    1. Document OCR (Traditional)
       - Scanned documents
       - High resolution, clean background
       - Structured layout
       - Example: PDF, scanned forms
    
    2. Scene Text Recognition
       - Text in natural images
       - Various fonts, colors, orientations
       - Complex backgrounds
       - Example: Street signs, product labels
    
    3. Handwriting Recognition
       - Handwritten text
       - Highly variable styles
       - Example: Notes, signatures
    
    
    [PRE-PROCESSING TECHNIQUES]
    ─────────────────────────────────────────────────────────────────────
    
    1. Grayscale Conversion
       - Simplify processing
    
    2. Binarization (Thresholding)
       - Otsu's method
       - Adaptive thresholding
    
    3. Noise Removal
       - Gaussian blur
       - Morphological operations
    
    4. Deskewing
       - Rotate to horizontal orientation
    
    5. Scaling
       - Resize for optimal recognition
    
    
    [POPULAR OCR ENGINES]
    ─────────────────────────────────────────────────────────────────────
    
    Traditional:
    - Tesseract OCR (Open source, by Google)
    - ABBYY FineReader (Commercial)
    
    Deep Learning Based:
    - EAST (Efficient Accurate Scene Text Detector)
    - CRAFT (Character Region Awareness For Text)
    - CRNN (Convolutional Recurrent Neural Network)
    - PaddleOCR (By Baidu)
    - EasyOCR
    """)


def create_text_image(text="Hello", font_scale=2, add_noise=False, rotate_angle=0):
    """
    Membuat gambar dengan teks untuk demonstrasi OCR.
    """
    # Create white background
    width = max(300, len(text) * 30)
    height = 100
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Calculate text position
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, 3)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    
    # Draw text
    cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), 3)
    
    # Add noise if requested
    if add_noise:
        noise = np.random.normal(0, 25, image.shape).astype(np.int16)
        image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Rotate if requested
    if rotate_angle != 0:
        center = (width // 2, height // 2)
        matrix = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
        image = cv2.warpAffine(image, matrix, (width, height), 
                               borderValue=(255, 255, 255))
    
    return image


def create_document_image():
    """
    Membuat simulasi document image.
    """
    image = np.ones((500, 400, 3), dtype=np.uint8) * 255
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Title
    cv2.putText(image, "INVOICE", (140, 50), font, 1.2, (0, 0, 0), 2)
    cv2.line(image, (50, 65), (350, 65), (0, 0, 0), 2)
    
    # Company info
    cv2.putText(image, "Company: ABC Corp", (50, 100), font, 0.5, (0, 0, 0), 1)
    cv2.putText(image, "Date: 2024-01-15", (50, 125), font, 0.5, (0, 0, 0), 1)
    cv2.putText(image, "Invoice #: INV-001", (50, 150), font, 0.5, (0, 0, 0), 1)
    
    # Table header
    cv2.rectangle(image, (50, 180), (350, 210), (200, 200, 200), -1)
    cv2.putText(image, "Item", (60, 200), font, 0.4, (0, 0, 0), 1)
    cv2.putText(image, "Qty", (170, 200), font, 0.4, (0, 0, 0), 1)
    cv2.putText(image, "Price", (230, 200), font, 0.4, (0, 0, 0), 1)
    cv2.putText(image, "Total", (300, 200), font, 0.4, (0, 0, 0), 1)
    
    # Table rows
    rows = [
        ("Product A", "2", "$50", "$100"),
        ("Product B", "3", "$30", "$90"),
        ("Service C", "1", "$200", "$200"),
    ]
    
    for i, (item, qty, price, total) in enumerate(rows):
        y = 240 + i * 30
        cv2.putText(image, item, (60, y), font, 0.4, (0, 0, 0), 1)
        cv2.putText(image, qty, (175, y), font, 0.4, (0, 0, 0), 1)
        cv2.putText(image, price, (230, y), font, 0.4, (0, 0, 0), 1)
        cv2.putText(image, total, (300, y), font, 0.4, (0, 0, 0), 1)
    
    # Total line
    cv2.line(image, (50, 340), (350, 340), (0, 0, 0), 1)
    cv2.putText(image, "TOTAL:", (230, 370), font, 0.6, (0, 0, 0), 2)
    cv2.putText(image, "$390", (300, 370), font, 0.6, (0, 0, 0), 2)
    
    return image


def create_scene_text_image():
    """
    Membuat simulasi scene text (teks dalam scene natural).
    """
    # Create background with gradient
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    for y in range(400):
        for x in range(600):
            image[y, x] = [180 - y//4, 200 - y//5, 220 - y//6]
    
    # Road sign
    sign_pts = np.array([[200, 50], [400, 50], [420, 130], [180, 130]])
    cv2.fillPoly(image, [sign_pts], (0, 150, 0))
    cv2.putText(image, "EXIT 25", (220, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    
    # Store sign
    cv2.rectangle(image, (50, 200), (250, 280), (0, 0, 180), -1)
    cv2.putText(image, "OPEN", (90, 250), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    
    # Street name
    cv2.rectangle(image, (350, 200), (550, 250), (0, 100, 0), -1)
    cv2.putText(image, "MAIN ST", (365, 235), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # License plate (on a car shape)
    cv2.rectangle(image, (200, 320), (400, 390), (100, 100, 100), -1)  # Car
    cv2.rectangle(image, (250, 350), (350, 380), (255, 255, 255), -1)  # Plate
    cv2.putText(image, "AB 1234", (255, 372), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    return image


def demo_preprocessing():
    """
    Demonstrasi pre-processing untuk OCR.
    """
    print("\n" + "="*70)
    print("PRE-PROCESSING UNTUK OCR")
    print("="*70)
    
    # Create noisy text image
    text = "Hello World"
    original = create_text_image(text, font_scale=2, add_noise=True, rotate_angle=5)
    
    print("\n[STEP 1] Original Image (with noise and rotation)")
    
    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    print("[STEP 2] Converted to grayscale")
    
    # Step 2: Denoise
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    print("[STEP 3] Applied Gaussian blur for denoising")
    
    # Step 3: Binarization (Otsu)
    _, binary_otsu = cv2.threshold(denoised, 0, 255, 
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("[STEP 4] Applied Otsu thresholding")
    
    # Step 4: Adaptive thresholding
    binary_adaptive = cv2.adaptiveThreshold(denoised, 255, 
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    print("[STEP 5] Applied adaptive thresholding")
    
    # Step 5: Deskewing
    coords = np.column_stack(np.where(binary_otsu < 128))
    if len(coords) > 0:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = 90 + angle
        print(f"[STEP 6] Detected rotation angle: {angle:.2f} degrees")
    
    # Visualize
    row1 = np.hstack([
        cv2.cvtColor(original, cv2.COLOR_BGR2GRAY),
        gray,
        denoised
    ])
    row2 = np.hstack([
        binary_otsu,
        binary_adaptive,
        binary_otsu  # Placeholder for deskewed
    ])
    
    combined = np.vstack([row1, row2])
    
    # Add labels
    cv2.putText(combined, "Original", (10, 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(combined, "Grayscale", (original.shape[1]+10, 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(combined, "Denoised", (2*original.shape[1]+10, 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(combined, "Otsu", (10, original.shape[0]+20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
    cv2.putText(combined, "Adaptive", (original.shape[1]+10, original.shape[0]+20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
    
    cv2.imshow("OCR Pre-processing Steps", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_text_detection():
    """
    Demonstrasi text detection.
    """
    print("\n" + "="*70)
    print("TEXT DETECTION DEMO")
    print("="*70)
    
    # Create scene with text
    scene = create_scene_text_image()
    
    print("""
    [TEXT DETECTION METHODS]
    ─────────────────────────────────────────────────────────────────────
    
    Traditional Methods:
    1. MSER (Maximally Stable Extremal Regions)
    2. SWT (Stroke Width Transform)
    3. Edge-based detection
    
    Deep Learning Methods:
    1. EAST (Efficient Accurate Scene Text)
    2. CRAFT (Character Region Awareness)
    3. TextBoxes / TextBoxes++
    4. FOTS (Fast Oriented Text Spotting)
    
    [DEMO] Using simulated bounding boxes for text regions
    """)
    
    # Simulated text regions (in real scenario, use EAST/CRAFT)
    text_regions = [
        {"box": (200, 50, 200, 80), "text": "EXIT 25", "confidence": 0.95},
        {"box": (50, 200, 200, 80), "text": "OPEN", "confidence": 0.98},
        {"box": (350, 200, 200, 50), "text": "MAIN ST", "confidence": 0.92},
        {"box": (250, 350, 100, 30), "text": "AB 1234", "confidence": 0.88}
    ]
    
    result = scene.copy()
    
    print("\n[DETECTED TEXT REGIONS]")
    print("-"*50)
    
    for i, region in enumerate(text_regions, 1):
        x, y, w, h = region["box"]
        text = region["text"]
        conf = region["confidence"]
        
        # Draw bounding box
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Draw label
        label = f"{i}: {text} ({conf:.0%})"
        cv2.putText(result, label, (x, y-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        print(f"Region {i}: '{text}' - Confidence: {conf:.2%}")
        print(f"  Location: ({x}, {y}), Size: {w}x{h}")
    
    cv2.imshow("Text Detection Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_ocr_tesseract():
    """
    Demonstrasi OCR menggunakan Tesseract.
    """
    print("\n" + "="*70)
    print("OCR dengan TESSERACT")
    print("="*70)
    
    # Create test images
    test_cases = [
        ("Simple text", create_text_image("Hello World", font_scale=2)),
        ("Numbers", create_text_image("12345 67890", font_scale=2)),
        ("Mixed", create_text_image("Price: $99.99", font_scale=1.5)),
    ]
    
    print("\n[OCR RESULTS]")
    print("-"*50)
    
    for name, image in test_cases:
        # Pre-process
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, 
                                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        if TESSERACT_AVAILABLE:
            # Actual OCR
            text = pytesseract.image_to_string(binary, config='--psm 7')
            text = text.strip()
        else:
            # Simulated result
            if "Hello" in name:
                text = "Hello World"
            elif "Numbers" in name:
                text = "12345 67890"
            else:
                text = "Price: $99.99"
        
        print(f"\n{name}:")
        print(f"  Recognized: '{text}'")
        
        # Show image with result
        display = np.vstack([image, np.ones_like(image) * 240])
        cv2.putText(display, f"Result: {text}", (10, image.shape[0] + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        cv2.imshow(f"OCR - {name}", display)
        cv2.waitKey(0)
    
    cv2.destroyAllWindows()


def demo_document_ocr():
    """
    Demonstrasi document OCR.
    """
    print("\n" + "="*70)
    print("DOCUMENT OCR DEMO")
    print("="*70)
    
    # Create document image
    document = create_document_image()
    
    print("""
    [DOCUMENT OCR PIPELINE]
    ─────────────────────────────────────────────────────────────────────
    
    1. Layout Analysis
       - Detect text blocks, tables, images
       - Determine reading order
    
    2. Line Detection
       - Segment text into lines
    
    3. Word Segmentation
       - Split lines into words
    
    4. Character Recognition
       - Recognize individual characters
    
    5. Post-processing
       - Dictionary lookup
       - Spell correction
    """)
    
    # Simulated OCR results
    ocr_results = [
        {"line": 1, "text": "INVOICE", "confidence": 0.99},
        {"line": 2, "text": "Company: ABC Corp", "confidence": 0.95},
        {"line": 3, "text": "Date: 2024-01-15", "confidence": 0.97},
        {"line": 4, "text": "Invoice #: INV-001", "confidence": 0.96},
        {"line": 5, "text": "Item    Qty    Price    Total", "confidence": 0.92},
        {"line": 6, "text": "Product A    2    $50    $100", "confidence": 0.94},
        {"line": 7, "text": "Product B    3    $30    $90", "confidence": 0.93},
        {"line": 8, "text": "Service C    1    $200    $200", "confidence": 0.95},
        {"line": 9, "text": "TOTAL: $390", "confidence": 0.98},
    ]
    
    print("\n[OCR RESULTS]")
    print("-"*50)
    
    for result in ocr_results:
        conf_bar = "█" * int(result['confidence'] * 10)
        print(f"Line {result['line']:2d}: {result['text']:<30s} [{result['confidence']:.0%}] {conf_bar}")
    
    # Calculate average confidence
    avg_conf = np.mean([r['confidence'] for r in ocr_results])
    print(f"\nAverage confidence: {avg_conf:.2%}")
    
    # Display document
    cv2.imshow("Document OCR", document)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_scene_text_recognition():
    """
    Demonstrasi scene text recognition.
    """
    print("\n" + "="*70)
    print("SCENE TEXT RECOGNITION")
    print("="*70)
    
    # Create scene
    scene = create_scene_text_image()
    
    print("""
    [CHALLENGES IN SCENE TEXT]
    ─────────────────────────────────────────────────────────────────────
    
    1. Variable fonts and styles
    2. Non-uniform lighting
    3. Complex backgrounds
    4. Perspective distortion
    5. Partial occlusion
    6. Motion blur
    7. Different orientations
    
    [SOLUTIONS]
    ─────────────────────────────────────────────────────────────────────
    
    1. Deep learning-based detection (EAST, CRAFT)
    2. Attention-based recognition (transformers)
    3. Multi-scale processing
    4. Data augmentation during training
    """)
    
    # Simulated detection and recognition results
    detections = [
        {"region": "Road Sign", "text": "EXIT 25", "type": "Highway sign"},
        {"region": "Store", "text": "OPEN", "type": "Business sign"},
        {"region": "Street", "text": "MAIN ST", "type": "Street name"},
        {"region": "Vehicle", "text": "AB 1234", "type": "License plate"},
    ]
    
    print("\n[DETECTED TEXT IN SCENE]")
    print("-"*50)
    
    for det in detections:
        print(f"\n{det['region']}:")
        print(f"  Text: '{det['text']}'")
        print(f"  Type: {det['type']}")
    
    cv2.imshow("Scene Text Recognition", scene)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_ocr_applications():
    """
    Demonstrasi aplikasi OCR.
    """
    print("\n" + "="*70)
    print("APLIKASI OCR")
    print("="*70)
    
    print("""
    [APLIKASI OCR DI DUNIA NYATA]
    ─────────────────────────────────────────────────────────────────────
    
    1. DOCUMENT DIGITIZATION
       - Scanning old documents
       - Creating searchable PDFs
       - Digital archiving
    
    2. AUTOMATIC DATA ENTRY
       - Invoice processing
       - Receipt scanning
       - Form digitization
    
    3. IDENTITY VERIFICATION
       - ID card reading
       - Passport scanning
       - License plate recognition (ALPR/ANPR)
    
    4. ACCESSIBILITY
       - Text-to-speech for visually impaired
       - Real-time translation
       - Screen readers
    
    5. BANKING & FINANCE
       - Check processing
       - Credit card scanning
       - Statement digitization
    
    6. RETAIL
       - Price tag reading
       - Inventory management
       - Receipt parsing
    
    7. HEALTHCARE
       - Medical record digitization
       - Prescription reading
       - Lab report processing
    
    8. TRANSLATION
       - Real-time text translation
       - Menu translation
       - Sign translation for travelers
    
    
    [LICENSE PLATE RECOGNITION EXAMPLE]
    ─────────────────────────────────────────────────────────────────────
    """)
    
    # Create license plate demo
    plate_img = np.ones((120, 300, 3), dtype=np.uint8) * 255
    cv2.rectangle(plate_img, (20, 20), (280, 100), (0, 0, 0), 2)
    cv2.rectangle(plate_img, (25, 25), (275, 95), (240, 240, 240), -1)
    cv2.putText(plate_img, "B 1234 ABC", (40, 75), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
    
    # Simulated processing steps
    print("\n[LICENSE PLATE RECOGNITION PIPELINE]")
    print("-"*50)
    print("Step 1: Detect vehicle -> Found 1 vehicle")
    print("Step 2: Locate plate region -> Region at (x=40, y=350)")
    print("Step 3: Pre-process plate image -> Enhanced contrast")
    print("Step 4: Segment characters -> Found 9 characters")
    print("Step 5: Recognize characters -> B 1 2 3 4 A B C")
    print("Step 6: Validate format -> Valid Indonesian plate format")
    print("\nResult: B 1234 ABC")
    print("  Region: Jakarta (B)")
    print("  Type: Private vehicle")
    
    cv2.imshow("License Plate Recognition", plate_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM OCR DAN TEXT RECOGNITION")
    print("="*70)
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Konsep OCR dan Text Recognition")
        print("2. Pre-processing untuk OCR")
        print("3. Text Detection Demo")
        print("4. OCR dengan Tesseract")
        print("5. Document OCR Demo")
        print("6. Scene Text Recognition")
        print("7. Aplikasi OCR")
        print("8. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-8): ").strip()
        
        if choice == '1':
            print_ocr_concepts()
        elif choice == '2':
            demo_preprocessing()
        elif choice == '3':
            demo_text_detection()
        elif choice == '4':
            demo_ocr_tesseract()
        elif choice == '5':
            demo_document_ocr()
        elif choice == '6':
            demo_scene_text_recognition()
        elif choice == '7':
            demo_ocr_applications()
        elif choice == '8':
            print_ocr_concepts()
            demo_preprocessing()
            demo_text_detection()
            demo_ocr_tesseract()
            demo_document_ocr()
            demo_scene_text_recognition()
            demo_ocr_applications()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
