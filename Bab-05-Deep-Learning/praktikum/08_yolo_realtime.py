"""
# Assignment - set nilai ke variabel
=============================================================================
# Load YOLOv8 model untuk object detection
PRAKTIKUM 08 - YOLO REAL-TIME DETECTION
# Assignment - set nilai ke variabel
=============================================================================
# Load YOLOv8 model untuk object detection
Program ini mendemonstrasikan penggunaan YOLO untuk real-time object
detection dengan berbagai fitur tambahan seperti object counting,
tracking, dan filtering.

Konsep yang dipelajari:
1. Real-time detection dari webcam
2. FPS optimization
3. Object counting
4. Class filtering
5. Detection zones

Kebutuhan:
- ultralytics (pip install ultralytics)
# Assignment - set nilai ke variabel
- opencv-python >= 4.8.0
- numpy

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
# Assignment - set nilai ke variabel
=============================================================================
"""

# Import library/module untuk digunakan
import cv2
# Import library/module untuk digunakan
import numpy as np
# Import library/module untuk digunakan
import time
# Import library/module untuk digunakan
from collections import deque

# Check apakah ultralytics tersedia
YOLO_AVAILABLE = False
# Blok try-except untuk error handling
try:
    # Load YOLOv8 model untuk object detection
    from ultralytics import YOLO
    # Load YOLOv8 model untuk object detection
    YOLO_AVAILABLE = True
    # Load YOLOv8 model untuk object detection
    print("[INFO] Ultralytics YOLO tersedia")
# Tangkap exception jika ada error di blok try
except ImportError:
    print("[WARNING] Ultralytics tidak tersedia - menggunakan simulasi")


# Definisi class untuk membuat object
class FPSCounter:
    """
    Class untuk menghitung dan menampilkan FPS.
    """
    # Definisi function dengan nama dan parameter
    def __init__(self, avg_frames=30):
        # Assignment - set nilai ke variabel
        self.fps_history = deque(maxlen=avg_frames)
        # Assignment - set nilai ke variabel
        self.last_time = time.time()
    
    # Definisi function dengan nama dan parameter
    def update(self):
        """Update FPS counter."""
        # Assignment - set nilai ke variabel
        current_time = time.time()
        # Assignment - set nilai ke variabel
        fps = 1.0 / (current_time - self.last_time)
        self.fps_history.append(fps)
        # Assignment - set nilai ke variabel
        self.last_time = current_time
        # Return value dari function
        return fps
    
    # Definisi function dengan nama dan parameter
    def get_avg_fps(self):
        """Get average FPS."""
        # Conditional statement - eksekusi jika kondisi True
        if len(self.fps_history) == 0:
            # Return value dari function
            return 0
        # Hitung rata-rata dari array
        return np.mean(self.fps_history)


# Definisi class untuk membuat object
class ObjectCounter:
    """
    Class untuk menghitung objek yang melewati garis/zona tertentu.
    """
    # Definisi function dengan nama dan parameter
    def __init__(self, line_position, direction='horizontal'):
        """
        Args:
            line_position: Posisi garis (y untuk horizontal, x untuk vertical)
            direction: 'horizontal' atau 'vertical'
        """
        # Assignment - set nilai ke variabel
        self.line_position = line_position
        # Assignment - set nilai ke variabel
        self.direction = direction
        # Assignment - set nilai ke variabel
        self.count_up = 0
        # Assignment - set nilai ke variabel
        self.count_down = 0
        # Assignment - set nilai ke variabel
        self.tracked_objects = {}  # {object_id: last_position}
    
    # Definisi function dengan nama dan parameter
    def update(self, detections, frame_shape):
        """
        Update counter berdasarkan deteksi baru.
        
        Args:
            detections: List of (box, class_id, confidence)
            frame_shape: Shape of frame (h, w)
        """
        # Simplified tracking berdasarkan center point
        h, w = frame_shape[:2]
        
        # Iterasi/loop melalui elemen dalam koleksi
        for i, (box, class_id, conf) in enumerate(detections):
            # Assignment - set nilai ke variabel
            x1, y1, x2, y2 = box
            # Assignment - set nilai ke variabel
            center_x = (x1 + x2) / 2
            # Assignment - set nilai ke variabel
            center_y = (y1 + y2) / 2
            
            # Check crossing
            if self.direction == 'horizontal':
                # Conditional statement - eksekusi jika kondisi True
                if i in self.tracked_objects:
                    # Assignment - set nilai ke variabel
                    last_y = self.tracked_objects[i]
                    # Conditional statement - eksekusi jika kondisi True
                    if last_y < self.line_position <= center_y:
                        # Assignment - set nilai ke variabel
                        self.count_down += 1
                    # Conditional statement - eksekusi jika kondisi True
                    elif last_y > self.line_position >= center_y:
                        # Assignment - set nilai ke variabel
                        self.count_up += 1
                # Assignment - set nilai ke variabel
                self.tracked_objects[i] = center_y
            else:
                # Conditional statement - eksekusi jika kondisi True
                if i in self.tracked_objects:
                    # Assignment - set nilai ke variabel
                    last_x = self.tracked_objects[i]
                    # Conditional statement - eksekusi jika kondisi True
                    if last_x < self.line_position <= center_x:
                        # Assignment - set nilai ke variabel
                        self.count_up += 1
                    # Conditional statement - eksekusi jika kondisi True
                    elif last_x > self.line_position >= center_x:
                        # Assignment - set nilai ke variabel
                        self.count_down += 1
                # Assignment - set nilai ke variabel
                self.tracked_objects[i] = center_x
    
    # Definisi function dengan nama dan parameter
    def draw_line(self, frame):
        """Draw counting line on frame."""
        # Assignment - set nilai ke variabel
        h, w = frame.shape[:2]
        
        # Conditional statement - eksekusi jika kondisi True
        if self.direction == 'horizontal':
            # Gambar garis pada gambar
            cv2.line(frame, (0, self.line_position), (w, self.line_position),
                    (0, 255, 255), 2)
        else:
            # Gambar garis pada gambar
            cv2.line(frame, (self.line_position, 0), (self.line_position, h),
                    (0, 255, 255), 2)


# Definisi function dengan nama dan parameter
def draw_detection(frame, box, class_name, confidence, color=(0, 255, 0)):
    """
    Menggambar detection box dan label.
    """
    # Assignment - set nilai ke variabel
    x1, y1, x2, y2 = map(int, box)
    
    # Box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    
    # Label
    label = f"{class_name}: {confidence:.2f}"
    # Assignment - set nilai ke variabel
    (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    # Gambar persegi panjang pada gambar
    cv2.rectangle(frame, (x1, y1-label_h-10), (x1+label_w+10, y1), color, -1)
    # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
    # d=font, e=skala, f=warna(B,G,R), g=ketebalan
    cv2.putText(frame, label, (x1+5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    # Center point
    center = ((x1+x2)//2, (y1+y2)//2)
    # Gambar lingkaran pada gambar
    cv2.circle(frame, center, 4, color, -1)


# Definisi function dengan nama dan parameter
def demo_realtime_detection():
    """
    # Load YOLOv8 model untuk object detection
    Demonstrasi real-time YOLO detection dengan webcam.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    # Load YOLOv8 model untuk object detection
    print("YOLO REAL-TIME DETECTION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    # Assignment - set nilai ke variabel
    use_webcam = cap.isOpened()
    # Conditional statement - eksekusi jika kondisi True
    if not use_webcam:
        print("[WARNING] Webcam tidak tersedia, menggunakan synthetic video")
    
    # Assignment - set nilai ke variabel
    fps_counter = FPSCounter()
    
    # Load YOLOv8 model untuk object detection
    if YOLO_AVAILABLE and use_webcam:
        # Load YOLOv8 model untuk object detection
        print("\n[INFO] Loading YOLOv8n model...")
        # Load YOLOv8 model untuk object detection
        model = YOLO('yolov8n.pt')
        
        print("[INFO] Starting real-time detection. Press 'q' to quit.")
        print("[INFO] Press 'p' to pause/resume.")
        
        # Assignment - set nilai ke variabel
        paused = False
        
        # Loop berulang selama kondisi bernilai True
        while True:
            # Conditional statement - eksekusi jika kondisi True
            if not paused:
                # Assignment - set nilai ke variabel
                ret, frame = cap.read()
                # Conditional statement - eksekusi jika kondisi True
                if not ret:
                    break
                
                # Run YOLO inference
                results = model(frame, verbose=False, conf=0.5)
                
                # Draw detections
                for result in results:
                    # Iterasi/loop melalui elemen dalam koleksi
                    for box in result.boxes:
                        # Assignment - set nilai ke variabel
                        cls = int(box.cls[0])
                        # Assignment - set nilai ke variabel
                        conf = float(box.conf[0])
                        # Assignment - set nilai ke variabel
                        xyxy = box.xyxy[0].cpu().numpy()
                        # Assignment - set nilai ke variabel
                        class_name = model.names[cls]
                        
                        draw_detection(frame, xyxy, class_name, conf)
                
                # Update and display FPS
                fps_counter.update()
                # Assignment - set nilai ke variabel
                avg_fps = fps_counter.get_avg_fps()
                
                # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
                # d=font, e=skala, f=warna(B,G,R), g=ketebalan
                cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
                # d=font, e=skala, f=warna(B,G,R), g=ketebalan
                cv2.putText(frame, "Press 'q' to quit, 'p' to pause", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Tampilkan gambar di window
            cv2.imshow("YOLO Real-time Detection", frame)
            
            # Tunggu input keyboard (1ms per iterasi)
            key = cv2.waitKey(1) & 0xFF
            # Conditional statement - eksekusi jika kondisi True
            if key == ord('q') or key == 27:
                break
            # Conditional statement - eksekusi jika kondisi True
            elif key == ord('p'):
                # Assignment - set nilai ke variabel
                paused = not paused
        
        cap.release()
        # Tutup semua window
        cv2.destroyAllWindows()
        
    else:
        # Synthetic video simulation
        print("\n[SIMULATION MODE] Running synthetic video detection...")
        
        # Assignment - set nilai ke variabel
        frame_count = 0
        # Assignment - set nilai ke variabel
        max_frames = 200
        
        # Loop berulang selama kondisi bernilai True
        while frame_count < max_frames:
            # Generate synthetic frame
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
            
            # Add moving objects
            t = frame_count / 30  # time in seconds
            
            # Person walking
            person_x = int(100 + 200 * np.sin(t))
            # Gambar persegi panjang pada gambar
            cv2.rectangle(frame, (person_x, 150), (person_x+80, 400), (50, 100, 150), -1)
            draw_detection(frame, [person_x, 150, person_x+80, 400], 'person', 0.92)
            
            # Car moving
            car_x = int(frame_count * 2) % 640
            # Gambar persegi panjang pada gambar
            cv2.rectangle(frame, (car_x, 280), (car_x+150, 360), (100, 100, 200), -1)
            draw_detection(frame, [car_x, 280, car_x+150, 360], 'car', 0.87)
            
            # Update FPS
            fps_counter.update()
            # Assignment - set nilai ke variabel
            avg_fps = fps_counter.get_avg_fps()
            
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"FPS: {avg_fps:.1f} (simulated)", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"Frame: {frame_count}/{max_frames}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, "Press 'q' to quit", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Tampilkan gambar di window
            cv2.imshow("YOLO Real-time Detection (Simulated)", frame)
            
            # Tunggu input keyboard (1ms per iterasi)
            key = cv2.waitKey(33) & 0xFF
            # Conditional statement - eksekusi jika kondisi True
            if key == ord('q') or key == 27:
                break
            
            # Assignment - set nilai ke variabel
            frame_count += 1
        
        # Tutup semua window
        cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_object_counting():
    """
    Demonstrasi object counting dengan line crossing.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("OBJECT COUNTING (LINE CROSSING)")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFO] Object Counting Algorithm:
    
    1. Deteksi objek di setiap frame
    2. Track center point setiap objek
    3. Detect crossing ketika center melewati garis
    4. Increment counter based on direction
    """)
    
    # Create counter
    line_y = 240  # Horizontal line di tengah
    # Assignment - set nilai ke variabel
    counter = ObjectCounter(line_y, direction='horizontal')
    
    # Assignment - set nilai ke variabel
    frame_count = 0
    # Assignment - set nilai ke variabel
    max_frames = 150
    
    # Loop berulang selama kondisi bernilai True
    while frame_count < max_frames:
        # Generate synthetic frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 220
        
        # Draw counting line
        counter.draw_line(frame)
        
        # Generate moving objects
        t = frame_count / 30
        
        # Object 1: Moving down
        obj1_y = int(100 + frame_count * 2) % 400
        # Assignment - set nilai ke variabel
        obj1_box = [100, obj1_y, 160, obj1_y + 80]
        draw_detection(frame, obj1_box, 'person', 0.9, (0, 255, 0))
        
        # Object 2: Moving up
        obj2_y = int(350 - frame_count * 1.5) % 400
        # Assignment - set nilai ke variabel
        obj2_box = [400, obj2_y, 500, obj2_y + 60]
        draw_detection(frame, obj2_box, 'car', 0.85, (255, 0, 0))
        
        # Update counter
        detections = [
            (obj1_box, 0, 0.9),
            (obj2_box, 2, 0.85)
        ]
        counter.update(detections, frame.shape)
        
        # Display counts
        # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(frame, f"Crossing Down: {counter.count_down}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(frame, f"Crossing Up: {counter.count_up}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
        # d=font, e=skala, f=warna(B,G,R), g=ketebalan
        cv2.putText(frame, f"Total: {counter.count_down + counter.count_up}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Tampilkan gambar di window
        cv2.imshow("Object Counting", frame)
        
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(50) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:
            break
        
        # Assignment - set nilai ke variabel
        frame_count += 1
    
    # Tutup semua window
    cv2.destroyAllWindows()
    
    print(f"\n[RESULT] Final counts:")
    print(f"  - Crossing Down: {counter.count_down}")
    print(f"  - Crossing Up: {counter.count_up}")
    print(f"  - Total: {counter.count_down + counter.count_up}")


# Definisi function dengan nama dan parameter
def demo_class_filtering():
    """
    # Definisi class untuk membuat object
    Demonstrasi filtering deteksi berdasarkan class tertentu.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("CLASS FILTERING")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Classes to filter
    target_classes = ['person', 'car', 'truck', 'bus']
    
    # Iterasi/loop melalui elemen dalam koleksi
    print(f"\n[INFO] Filtering for classes: {target_classes}")
    
    # Load YOLOv8 model untuk object detection
    if YOLO_AVAILABLE:
        print("[INFO] Loading model...")
        # Load YOLOv8 model untuk object detection
        model = YOLO('yolov8n.pt')
        
        # Get class indices for target classes
        target_indices = []
        # Iterasi/loop melalui elemen dalam koleksi
        for name, idx in model.names.items():
            # Conditional statement - eksekusi jika kondisi True
            if model.names[idx] in target_classes:
                target_indices.append(idx)
        
        # Definisi class untuk membuat object
        print(f"[INFO] Target class indices: {target_indices}")
        
        # Demo with webcam or synthetic
        cap = cv2.VideoCapture(0)
        
        # Conditional statement - eksekusi jika kondisi True
        if cap.isOpened():
            print("[INFO] Press 'q' to quit")
            
            # Loop berulang selama kondisi bernilai True
            while True:
                # Assignment - set nilai ke variabel
                ret, frame = cap.read()
                # Conditional statement - eksekusi jika kondisi True
                if not ret:
                    break
                
                # Run inference with class filter
                results = model(frame, verbose=False, classes=target_indices)
                
                # Draw only filtered detections
                for result in results:
                    # Iterasi/loop melalui elemen dalam koleksi
                    for box in result.boxes:
                        # Assignment - set nilai ke variabel
                        cls = int(box.cls[0])
                        # Assignment - set nilai ke variabel
                        conf = float(box.conf[0])
                        # Assignment - set nilai ke variabel
                        xyxy = box.xyxy[0].cpu().numpy()
                        # Assignment - set nilai ke variabel
                        class_name = model.names[cls]
                        
                        draw_detection(frame, xyxy, class_name, conf)
                
                # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
                # d=font, e=skala, f=warna(B,G,R), g=ketebalan
                cv2.putText(frame, f"Filtering: {', '.join(target_classes)}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Tampilkan gambar di window
                cv2.imshow("Class Filtering", frame)
                
                # Tunggu input keyboard (1ms per iterasi)
                key = cv2.waitKey(1) & 0xFF
                # Conditional statement - eksekusi jika kondisi True
                if key == ord('q') or key == 27:
                    break
            
            cap.release()
            # Tutup semua window
            cv2.destroyAllWindows()
        else:
            print("[WARNING] Webcam not available")
    
    else:
        # Simulation
        print("\n[SIMULATION MODE]")
        
        # Assignment - set nilai ke variabel
        all_detections = [
            {'class': 'person', 'box': [100, 100, 180, 350], 'conf': 0.92},
            {'class': 'car', 'box': [300, 200, 500, 350], 'conf': 0.88},
            {'class': 'dog', 'box': [200, 300, 280, 380], 'conf': 0.75},
            {'class': 'bicycle', 'box': [450, 150, 550, 300], 'conf': 0.65},
            {'class': 'truck', 'box': [50, 200, 150, 300], 'conf': 0.82},
        ]
        
        # Create frames
        for show_filtered in [False, True]:
            # Buat array numpy penuh dengan nilai 1
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
            
            # Conditional statement - eksekusi jika kondisi True
            if show_filtered:
                # Iterasi/loop melalui elemen dalam koleksi
                detections = [d for d in all_detections if d['class'] in target_classes]
                # Assignment - set nilai ke variabel
                title = "After Filtering"
            else:
                # Assignment - set nilai ke variabel
                detections = all_detections
                # Assignment - set nilai ke variabel
                title = "Before Filtering"
            
            # Iterasi/loop melalui elemen dalam koleksi
            for det in detections:
                # Conditional statement - eksekusi jika kondisi True
                color = (0, 255, 0) if det['class'] in target_classes else (128, 128, 128)
                draw_detection(frame, det['box'], det['class'], det['conf'], color)
            
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"{title}: {len(detections)} detections", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Conditional statement - eksekusi jika kondisi True
            if show_filtered:
                # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
                # d=font, e=skala, f=warna(B,G,R), g=ketebalan
                cv2.putText(frame, f"Filtering: {', '.join(target_classes)}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            
            # Tampilkan gambar di window
            cv2.imshow("Class Filtering", frame)
            # Tunggu input keyboard (1ms per iterasi)
            cv2.waitKey(2000)
        
        # Tutup semua window
        cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_detection_zones():
    """
    Demonstrasi detection zones - hanya deteksi di area tertentu.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("DETECTION ZONES")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Define zones
    zones = {
        'Zone A': {'points': [(50, 100), (250, 100), (250, 350), (50, 350)], 
                   'color': (0, 255, 0)},
        'Zone B': {'points': [(300, 100), (600, 100), (600, 350), (300, 350)], 
                   'color': (255, 0, 0)},
    }
    
    print("\n[INFO] Defined zones:")
    # Iterasi/loop melalui elemen dalam koleksi
    for name, zone in zones.items():
        print(f"  - {name}: {zone['points']}")
    
    # Definisi function dengan nama dan parameter
    def point_in_polygon(point, polygon):
        """Check if point is inside polygon."""
        # Assignment - set nilai ke variabel
        x, y = point
        # Assignment - set nilai ke variabel
        n = len(polygon)
        # Assignment - set nilai ke variabel
        inside = False
        
        # Assignment - set nilai ke variabel
        p1x, p1y = polygon[0]
        # Iterasi/loop melalui elemen dalam koleksi
        for i in range(1, n + 1):
            # Assignment - set nilai ke variabel
            p2x, p2y = polygon[i % n]
            # Conditional statement - eksekusi jika kondisi True
            if y > min(p1y, p2y):
                # Conditional statement - eksekusi jika kondisi True
                if y <= max(p1y, p2y):
                    # Conditional statement - eksekusi jika kondisi True
                    if x <= max(p1x, p2x):
                        # Conditional statement - eksekusi jika kondisi True
                        if p1y != p2y:
                            # Assignment - set nilai ke variabel
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # Conditional statement - eksekusi jika kondisi True
                        if p1x == p2x or x <= xinters:
                            # Assignment - set nilai ke variabel
                            inside = not inside
            # Assignment - set nilai ke variabel
            p1x, p1y = p2x, p2y
        
        # Return value dari function
        return inside
    
    # Simulation
    frame_count = 0
    # Assignment - set nilai ke variabel
    max_frames = 100
    
    # Iterasi/loop melalui elemen dalam koleksi
    zone_counts = {name: 0 for name in zones.keys()}
    
    # Loop berulang selama kondisi bernilai True
    while frame_count < max_frames:
        # Buat array numpy penuh dengan nilai 1
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 220
        
        # Draw zones
        for name, zone in zones.items():
            # Buat array numpy dari list/data
            pts = np.array(zone['points'], np.int32)
            cv2.polylines(frame, [pts], True, zone['color'], 2)
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, name, (zone['points'][0][0]+5, zone['points'][0][1]+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, zone['color'], 2)
        
        # Generate moving objects
        t = frame_count / 20
        
        # Assignment - set nilai ke variabel
        objects = [
            {'center': (int(150 + 50*np.sin(t*2)), int(200 + 100*np.sin(t))), 
             'box': None, 'class': 'person'},
            {'center': (int(400 + 100*np.cos(t)), int(250 + 50*np.sin(t*1.5))), 
             'box': None, 'class': 'car'},
        ]
        
        # Update boxes based on centers
        for obj in objects:
            # Assignment - set nilai ke variabel
            cx, cy = obj['center']
            # Assignment - set nilai ke variabel
            obj['box'] = [cx-40, cy-50, cx+40, cy+50]
        
        # Reset zone counts for this frame
        zone_counts = {name: 0 for name in zones.keys()}
        
        # Draw objects and check zones
        for obj in objects:
            # Check which zone the center is in
            cx, cy = obj['center']
            # Assignment - set nilai ke variabel
            obj_zone = None
            
            # Iterasi/loop melalui elemen dalam koleksi
            for name, zone in zones.items():
                # Conditional statement - eksekusi jika kondisi True
                if point_in_polygon((cx, cy), zone['points']):
                    # Assignment - set nilai ke variabel
                    obj_zone = name
                    # Assignment - set nilai ke variabel
                    zone_counts[name] += 1
                    break
            
            # Draw with zone color
            if obj_zone:
                # Assignment - set nilai ke variabel
                color = zones[obj_zone]['color']
            else:
                # Assignment - set nilai ke variabel
                color = (128, 128, 128)
            
            draw_detection(frame, obj['box'], obj['class'], 0.9, color)
        
        # Display zone counts
        y_pos = 400
        # Iterasi/loop melalui elemen dalam koleksi
        for name, count in zone_counts.items():
            # cv2.putText(a, b, c, d, e, f, g): a=frame, b=teks, c=posisi(x,y),
            # d=font, e=skala, f=warna(B,G,R), g=ketebalan
            cv2.putText(frame, f"{name}: {count} objects", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, zones[name]['color'], 2)
            # Assignment - set nilai ke variabel
            y_pos += 25
        
        # Tampilkan gambar di window
        cv2.imshow("Detection Zones", frame)
        
        # Tunggu input keyboard (1ms per iterasi)
        key = cv2.waitKey(50) & 0xFF
        # Conditional statement - eksekusi jika kondisi True
        if key == ord('q') or key == 27:
            break
        
        # Assignment - set nilai ke variabel
        frame_count += 1
    
    # Tutup semua window
    cv2.destroyAllWindows()


# Definisi function dengan nama dan parameter
def demo_performance_optimization():
    """
    # Load YOLOv8 model untuk object detection
    Tips untuk mengoptimasi performa YOLO.
    """
    # Assignment - set nilai ke variabel
    print("\n" + "="*70)
    print("PERFORMANCE OPTIMIZATION TIPS")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    print("""
    [INFERENCE SPEED OPTIMIZATION]
    ─────────────────────────────────────────────────────────────────────
    
    1. MODEL SELECTION
       # Load YOLOv8 model untuk object detection
       - YOLOv8n: Fastest (nano) - untuk real-time
       # Load YOLOv8 model untuk object detection
       - YOLOv8s: Balanced - untuk akurasi lebih baik
       # Load YOLOv8 model untuk object detection
       - YOLOv8m/l/x: Slower - untuk akurasi maksimal
    
    2. INPUT RESOLUTION
       - Default: 640×640
       - Lower: 320×320 (faster, less accurate)
       - Higher: 1280×1280 (slower, more accurate)
       
       # Assignment - set nilai ke variabel
       model(image, imgsz=320)  # Faster inference
    
    3. BATCH SIZE
       - Untuk video: process multiple frames at once
       
       # Assignment - set nilai ke variabel
       results = model([frame1, frame2, frame3, frame4])
    
    4. HALF PRECISION (FP16)
       - Reduces memory and speeds up GPU inference
       
       model.half()  # Convert to FP16
    
    5. EXPORT TO OPTIMIZED FORMAT
       - ONNX: Cross-platform
       - TensorRT: NVIDIA GPU optimization
       - OpenVINO: Intel CPU optimization
       
       # Assignment - set nilai ke variabel
       model.export(format='onnx')
       # Assignment - set nilai ke variabel
       model.export(format='engine')  # TensorRT
    
    6. SKIP FRAMES
       - Process every Nth frame
       
       # Conditional statement - eksekusi jika kondisi True
       if frame_count % 2 == 0:  # Process every 2nd frame
           # Assignment - set nilai ke variabel
           results = model(frame)
    
    7. ASYNC PROCESSING
       - Run detection in separate thread
       
       # Import library/module untuk digunakan
       from threading import Thread
       # Assignment - set nilai ke variabel
       Thread(target=detect_async, args=(frame,)).start()
    
    
    [MEMORY OPTIMIZATION]
    ─────────────────────────────────────────────────────────────────────
    
    1. Release frames after processing
       
       del frame
       # Tutup semua window
       cv2.destroyAllWindows()
    
    # Iterasi/loop melalui elemen dalam koleksi
    2. Use streaming mode for videos
       
       # Jalankan inference YOLOv8 pada gambar
       results = model.predict(source='video.mp4', stream=True)
       # Iterasi/loop melalui elemen dalam koleksi
       for result in results:
           process(result)
    
    3. Limit detection classes
       
       # Assignment - set nilai ke variabel
       model(image, classes=[0, 2, 5])  # Only person, car, bus
    
    
    [BENCHMARK RESULTS (Example)]
    ─────────────────────────────────────────────────────────────────────
    
    Model      | GPU (ms) | CPU (ms) | mAP    | Use Case
    -----------|----------|----------|--------|------------------
    # Load YOLOv8 model untuk object detection
    YOLOv8n    |   1.0    |   25     | 37.3%  | Real-time
    # Load YOLOv8 model untuk object detection
    YOLOv8s    |   1.2    |   45     | 44.9%  | Balanced
    # Load YOLOv8 model untuk object detection
    YOLOv8m    |   1.8    |   95     | 50.2%  | Accuracy
    # Load YOLOv8 model untuk object detection
    YOLOv8n+TRT|   0.5    |   -      | 37.3%  | Optimized RT
    
    * Tested on NVIDIA RTX 3080 / Intel i7-12700K
    """)
    
    # Load YOLOv8 model untuk object detection
    if YOLO_AVAILABLE:
        print("\n[INFO] Running quick benchmark...")
        
        # Load YOLOv8 model untuk object detection
        model = YOLO('yolov8n.pt')
        
        # Generate test image
        test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        
        # Warmup
        for _ in range(3):
            # Assignment - set nilai ke variabel
            model(test_image, verbose=False)
        
        # Benchmark
        times = []
        # Iterasi/loop melalui elemen dalam koleksi
        for _ in range(10):
            # Assignment - set nilai ke variabel
            start = time.time()
            # Assignment - set nilai ke variabel
            model(test_image, verbose=False)
            times.append(time.time() - start)
        
        # Hitung rata-rata dari array
        avg_time = np.mean(times) * 1000
        # Hitung standard deviation dari array
        std_time = np.std(times) * 1000
        
        # Load YOLOv8 model untuk object detection
        print(f"\n[BENCHMARK] YOLOv8n on current device:")
        print(f"  - Average: {avg_time:.2f} ms")
        print(f"  - Std Dev: {std_time:.2f} ms")
        print(f"  - FPS: {1000/avg_time:.1f}")


# Definisi function dengan nama dan parameter
def main():
    """
    Fungsi utama program.
    """
    # Assignment - set nilai ke variabel
    print("="*70)
    # Load YOLOv8 model untuk object detection
    print("PRAKTIKUM YOLO REAL-TIME DETECTION")
    # Assignment - set nilai ke variabel
    print("="*70)
    
    # Loop berulang selama kondisi bernilai True
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Real-time Detection (Webcam/Synthetic)")
        print("2. Object Counting (Line Crossing)")
        print("3. Class Filtering")
        print("4. Detection Zones")
        print("5. Performance Optimization Tips")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        # Assignment - set nilai ke variabel
        choice = input("\nPilih menu (0-6): ").strip()
        
        # Conditional statement - eksekusi jika kondisi True
        if choice == '1':
            demo_realtime_detection()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '2':
            demo_object_counting()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '3':
            demo_class_filtering()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '4':
            demo_detection_zones()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '5':
            demo_performance_optimization()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '6':
            demo_realtime_detection()
            demo_object_counting()
            demo_class_filtering()
            demo_detection_zones()
            demo_performance_optimization()
        # Conditional statement - eksekusi jika kondisi True
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


# Conditional statement - eksekusi jika kondisi True
if __name__ == "__main__":
    main()
