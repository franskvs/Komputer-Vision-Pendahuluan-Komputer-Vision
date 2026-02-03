"""
=============================================================================
PRAKTIKUM 08 - YOLO REAL-TIME DETECTION
=============================================================================
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
- opencv-python >= 4.8.0
- numpy

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import time
from collections import deque

# Check apakah ultralytics tersedia
YOLO_AVAILABLE = False
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
    print("[INFO] Ultralytics YOLO tersedia")
except ImportError:
    print("[WARNING] Ultralytics tidak tersedia - menggunakan simulasi")


class FPSCounter:
    """
    Class untuk menghitung dan menampilkan FPS.
    """
    def __init__(self, avg_frames=30):
        self.fps_history = deque(maxlen=avg_frames)
        self.last_time = time.time()
    
    def update(self):
        """Update FPS counter."""
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_time)
        self.fps_history.append(fps)
        self.last_time = current_time
        return fps
    
    def get_avg_fps(self):
        """Get average FPS."""
        if len(self.fps_history) == 0:
            return 0
        return np.mean(self.fps_history)


class ObjectCounter:
    """
    Class untuk menghitung objek yang melewati garis/zona tertentu.
    """
    def __init__(self, line_position, direction='horizontal'):
        """
        Args:
            line_position: Posisi garis (y untuk horizontal, x untuk vertical)
            direction: 'horizontal' atau 'vertical'
        """
        self.line_position = line_position
        self.direction = direction
        self.count_up = 0
        self.count_down = 0
        self.tracked_objects = {}  # {object_id: last_position}
    
    def update(self, detections, frame_shape):
        """
        Update counter berdasarkan deteksi baru.
        
        Args:
            detections: List of (box, class_id, confidence)
            frame_shape: Shape of frame (h, w)
        """
        # Simplified tracking berdasarkan center point
        h, w = frame_shape[:2]
        
        for i, (box, class_id, conf) in enumerate(detections):
            x1, y1, x2, y2 = box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            # Check crossing
            if self.direction == 'horizontal':
                if i in self.tracked_objects:
                    last_y = self.tracked_objects[i]
                    if last_y < self.line_position <= center_y:
                        self.count_down += 1
                    elif last_y > self.line_position >= center_y:
                        self.count_up += 1
                self.tracked_objects[i] = center_y
            else:
                if i in self.tracked_objects:
                    last_x = self.tracked_objects[i]
                    if last_x < self.line_position <= center_x:
                        self.count_up += 1
                    elif last_x > self.line_position >= center_x:
                        self.count_down += 1
                self.tracked_objects[i] = center_x
    
    def draw_line(self, frame):
        """Draw counting line on frame."""
        h, w = frame.shape[:2]
        
        if self.direction == 'horizontal':
            cv2.line(frame, (0, self.line_position), (w, self.line_position),
                    (0, 255, 255), 2)
        else:
            cv2.line(frame, (self.line_position, 0), (self.line_position, h),
                    (0, 255, 255), 2)


def draw_detection(frame, box, class_name, confidence, color=(0, 255, 0)):
    """
    Menggambar detection box dan label.
    """
    x1, y1, x2, y2 = map(int, box)
    
    # Box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    
    # Label
    label = f"{class_name}: {confidence:.2f}"
    (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame, (x1, y1-label_h-10), (x1+label_w+10, y1), color, -1)
    cv2.putText(frame, label, (x1+5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    # Center point
    center = ((x1+x2)//2, (y1+y2)//2)
    cv2.circle(frame, center, 4, color, -1)


def demo_realtime_detection():
    """
    Demonstrasi real-time YOLO detection dengan webcam.
    """
    print("\n" + "="*70)
    print("YOLO REAL-TIME DETECTION")
    print("="*70)
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    use_webcam = cap.isOpened()
    if not use_webcam:
        print("[WARNING] Webcam tidak tersedia, menggunakan synthetic video")
    
    fps_counter = FPSCounter()
    
    if YOLO_AVAILABLE and use_webcam:
        print("\n[INFO] Loading YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        
        print("[INFO] Starting real-time detection. Press 'q' to quit.")
        print("[INFO] Press 'p' to pause/resume.")
        
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Run YOLO inference
                results = model(frame, verbose=False, conf=0.5)
                
                # Draw detections
                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        xyxy = box.xyxy[0].cpu().numpy()
                        class_name = model.names[cls]
                        
                        draw_detection(frame, xyxy, class_name, conf)
                
                # Update and display FPS
                fps_counter.update()
                avg_fps = fps_counter.get_avg_fps()
                
                cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Press 'q' to quit, 'p' to pause", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow("YOLO Real-time Detection", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                paused = not paused
        
        cap.release()
        cv2.destroyAllWindows()
        
    else:
        # Synthetic video simulation
        print("\n[SIMULATION MODE] Running synthetic video detection...")
        
        frame_count = 0
        max_frames = 200
        
        while frame_count < max_frames:
            # Generate synthetic frame
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
            
            # Add moving objects
            t = frame_count / 30  # time in seconds
            
            # Person walking
            person_x = int(100 + 200 * np.sin(t))
            cv2.rectangle(frame, (person_x, 150), (person_x+80, 400), (50, 100, 150), -1)
            draw_detection(frame, [person_x, 150, person_x+80, 400], 'person', 0.92)
            
            # Car moving
            car_x = int(frame_count * 2) % 640
            cv2.rectangle(frame, (car_x, 280), (car_x+150, 360), (100, 100, 200), -1)
            draw_detection(frame, [car_x, 280, car_x+150, 360], 'car', 0.87)
            
            # Update FPS
            fps_counter.update()
            avg_fps = fps_counter.get_avg_fps()
            
            cv2.putText(frame, f"FPS: {avg_fps:.1f} (simulated)", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Frame: {frame_count}/{max_frames}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, "Press 'q' to quit", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow("YOLO Real-time Detection (Simulated)", frame)
            
            if cv2.waitKey(33) & 0xFF == ord('q'):
                break
            
            frame_count += 1
        
        cv2.destroyAllWindows()


def demo_object_counting():
    """
    Demonstrasi object counting dengan line crossing.
    """
    print("\n" + "="*70)
    print("OBJECT COUNTING (LINE CROSSING)")
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
    counter = ObjectCounter(line_y, direction='horizontal')
    
    frame_count = 0
    max_frames = 150
    
    while frame_count < max_frames:
        # Generate synthetic frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 220
        
        # Draw counting line
        counter.draw_line(frame)
        
        # Generate moving objects
        t = frame_count / 30
        
        # Object 1: Moving down
        obj1_y = int(100 + frame_count * 2) % 400
        obj1_box = [100, obj1_y, 160, obj1_y + 80]
        draw_detection(frame, obj1_box, 'person', 0.9, (0, 255, 0))
        
        # Object 2: Moving up
        obj2_y = int(350 - frame_count * 1.5) % 400
        obj2_box = [400, obj2_y, 500, obj2_y + 60]
        draw_detection(frame, obj2_box, 'car', 0.85, (255, 0, 0))
        
        # Update counter
        detections = [
            (obj1_box, 0, 0.9),
            (obj2_box, 2, 0.85)
        ]
        counter.update(detections, frame.shape)
        
        # Display counts
        cv2.putText(frame, f"Crossing Down: {counter.count_down}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Crossing Up: {counter.count_up}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Total: {counter.count_down + counter.count_up}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        cv2.imshow("Object Counting", frame)
        
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cv2.destroyAllWindows()
    
    print(f"\n[RESULT] Final counts:")
    print(f"  - Crossing Down: {counter.count_down}")
    print(f"  - Crossing Up: {counter.count_up}")
    print(f"  - Total: {counter.count_down + counter.count_up}")


def demo_class_filtering():
    """
    Demonstrasi filtering deteksi berdasarkan class tertentu.
    """
    print("\n" + "="*70)
    print("CLASS FILTERING")
    print("="*70)
    
    # Classes to filter
    target_classes = ['person', 'car', 'truck', 'bus']
    
    print(f"\n[INFO] Filtering for classes: {target_classes}")
    
    if YOLO_AVAILABLE:
        print("[INFO] Loading model...")
        model = YOLO('yolov8n.pt')
        
        # Get class indices for target classes
        target_indices = []
        for name, idx in model.names.items():
            if model.names[idx] in target_classes:
                target_indices.append(idx)
        
        print(f"[INFO] Target class indices: {target_indices}")
        
        # Demo with webcam or synthetic
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("[INFO] Press 'q' to quit")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Run inference with class filter
                results = model(frame, verbose=False, classes=target_indices)
                
                # Draw only filtered detections
                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        xyxy = box.xyxy[0].cpu().numpy()
                        class_name = model.names[cls]
                        
                        draw_detection(frame, xyxy, class_name, conf)
                
                cv2.putText(frame, f"Filtering: {', '.join(target_classes)}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.imshow("Class Filtering", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
        else:
            print("[WARNING] Webcam not available")
    
    else:
        # Simulation
        print("\n[SIMULATION MODE]")
        
        all_detections = [
            {'class': 'person', 'box': [100, 100, 180, 350], 'conf': 0.92},
            {'class': 'car', 'box': [300, 200, 500, 350], 'conf': 0.88},
            {'class': 'dog', 'box': [200, 300, 280, 380], 'conf': 0.75},
            {'class': 'bicycle', 'box': [450, 150, 550, 300], 'conf': 0.65},
            {'class': 'truck', 'box': [50, 200, 150, 300], 'conf': 0.82},
        ]
        
        # Create frames
        for show_filtered in [False, True]:
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
            
            if show_filtered:
                detections = [d for d in all_detections if d['class'] in target_classes]
                title = "After Filtering"
            else:
                detections = all_detections
                title = "Before Filtering"
            
            for det in detections:
                color = (0, 255, 0) if det['class'] in target_classes else (128, 128, 128)
                draw_detection(frame, det['box'], det['class'], det['conf'], color)
            
            cv2.putText(frame, f"{title}: {len(detections)} detections", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            if show_filtered:
                cv2.putText(frame, f"Filtering: {', '.join(target_classes)}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            
            cv2.imshow("Class Filtering", frame)
            cv2.waitKey(2000)
        
        cv2.destroyAllWindows()


def demo_detection_zones():
    """
    Demonstrasi detection zones - hanya deteksi di area tertentu.
    """
    print("\n" + "="*70)
    print("DETECTION ZONES")
    print("="*70)
    
    # Define zones
    zones = {
        'Zone A': {'points': [(50, 100), (250, 100), (250, 350), (50, 350)], 
                   'color': (0, 255, 0)},
        'Zone B': {'points': [(300, 100), (600, 100), (600, 350), (300, 350)], 
                   'color': (255, 0, 0)},
    }
    
    print("\n[INFO] Defined zones:")
    for name, zone in zones.items():
        print(f"  - {name}: {zone['points']}")
    
    def point_in_polygon(point, polygon):
        """Check if point is inside polygon."""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    # Simulation
    frame_count = 0
    max_frames = 100
    
    zone_counts = {name: 0 for name in zones.keys()}
    
    while frame_count < max_frames:
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 220
        
        # Draw zones
        for name, zone in zones.items():
            pts = np.array(zone['points'], np.int32)
            cv2.polylines(frame, [pts], True, zone['color'], 2)
            cv2.putText(frame, name, (zone['points'][0][0]+5, zone['points'][0][1]+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, zone['color'], 2)
        
        # Generate moving objects
        t = frame_count / 20
        
        objects = [
            {'center': (int(150 + 50*np.sin(t*2)), int(200 + 100*np.sin(t))), 
             'box': None, 'class': 'person'},
            {'center': (int(400 + 100*np.cos(t)), int(250 + 50*np.sin(t*1.5))), 
             'box': None, 'class': 'car'},
        ]
        
        # Update boxes based on centers
        for obj in objects:
            cx, cy = obj['center']
            obj['box'] = [cx-40, cy-50, cx+40, cy+50]
        
        # Reset zone counts for this frame
        zone_counts = {name: 0 for name in zones.keys()}
        
        # Draw objects and check zones
        for obj in objects:
            # Check which zone the center is in
            cx, cy = obj['center']
            obj_zone = None
            
            for name, zone in zones.items():
                if point_in_polygon((cx, cy), zone['points']):
                    obj_zone = name
                    zone_counts[name] += 1
                    break
            
            # Draw with zone color
            if obj_zone:
                color = zones[obj_zone]['color']
            else:
                color = (128, 128, 128)
            
            draw_detection(frame, obj['box'], obj['class'], 0.9, color)
        
        # Display zone counts
        y_pos = 400
        for name, count in zone_counts.items():
            cv2.putText(frame, f"{name}: {count} objects", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, zones[name]['color'], 2)
            y_pos += 25
        
        cv2.imshow("Detection Zones", frame)
        
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cv2.destroyAllWindows()


def demo_performance_optimization():
    """
    Tips untuk mengoptimasi performa YOLO.
    """
    print("\n" + "="*70)
    print("PERFORMANCE OPTIMIZATION TIPS")
    print("="*70)
    
    print("""
    [INFERENCE SPEED OPTIMIZATION]
    ─────────────────────────────────────────────────────────────────────
    
    1. MODEL SELECTION
       - YOLOv8n: Fastest (nano) - untuk real-time
       - YOLOv8s: Balanced - untuk akurasi lebih baik
       - YOLOv8m/l/x: Slower - untuk akurasi maksimal
    
    2. INPUT RESOLUTION
       - Default: 640×640
       - Lower: 320×320 (faster, less accurate)
       - Higher: 1280×1280 (slower, more accurate)
       
       model(image, imgsz=320)  # Faster inference
    
    3. BATCH SIZE
       - Untuk video: process multiple frames at once
       
       results = model([frame1, frame2, frame3, frame4])
    
    4. HALF PRECISION (FP16)
       - Reduces memory and speeds up GPU inference
       
       model.half()  # Convert to FP16
    
    5. EXPORT TO OPTIMIZED FORMAT
       - ONNX: Cross-platform
       - TensorRT: NVIDIA GPU optimization
       - OpenVINO: Intel CPU optimization
       
       model.export(format='onnx')
       model.export(format='engine')  # TensorRT
    
    6. SKIP FRAMES
       - Process every Nth frame
       
       if frame_count % 2 == 0:  # Process every 2nd frame
           results = model(frame)
    
    7. ASYNC PROCESSING
       - Run detection in separate thread
       
       from threading import Thread
       Thread(target=detect_async, args=(frame,)).start()
    
    
    [MEMORY OPTIMIZATION]
    ─────────────────────────────────────────────────────────────────────
    
    1. Release frames after processing
       
       del frame
       cv2.destroyAllWindows()
    
    2. Use streaming mode for videos
       
       results = model.predict(source='video.mp4', stream=True)
       for result in results:
           process(result)
    
    3. Limit detection classes
       
       model(image, classes=[0, 2, 5])  # Only person, car, bus
    
    
    [BENCHMARK RESULTS (Example)]
    ─────────────────────────────────────────────────────────────────────
    
    Model      | GPU (ms) | CPU (ms) | mAP    | Use Case
    -----------|----------|----------|--------|------------------
    YOLOv8n    |   1.0    |   25     | 37.3%  | Real-time
    YOLOv8s    |   1.2    |   45     | 44.9%  | Balanced
    YOLOv8m    |   1.8    |   95     | 50.2%  | Accuracy
    YOLOv8n+TRT|   0.5    |   -      | 37.3%  | Optimized RT
    
    * Tested on NVIDIA RTX 3080 / Intel i7-12700K
    """)
    
    if YOLO_AVAILABLE:
        print("\n[INFO] Running quick benchmark...")
        
        model = YOLO('yolov8n.pt')
        
        # Generate test image
        test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        
        # Warmup
        for _ in range(3):
            model(test_image, verbose=False)
        
        # Benchmark
        times = []
        for _ in range(10):
            start = time.time()
            model(test_image, verbose=False)
            times.append(time.time() - start)
        
        avg_time = np.mean(times) * 1000
        std_time = np.std(times) * 1000
        
        print(f"\n[BENCHMARK] YOLOv8n on current device:")
        print(f"  - Average: {avg_time:.2f} ms")
        print(f"  - Std Dev: {std_time:.2f} ms")
        print(f"  - FPS: {1000/avg_time:.1f}")


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM YOLO REAL-TIME DETECTION")
    print("="*70)
    
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
        
        choice = input("\nPilih menu (0-6): ").strip()
        
        if choice == '1':
            demo_realtime_detection()
        elif choice == '2':
            demo_object_counting()
        elif choice == '3':
            demo_class_filtering()
        elif choice == '4':
            demo_detection_zones()
        elif choice == '5':
            demo_performance_optimization()
        elif choice == '6':
            demo_realtime_detection()
            demo_object_counting()
            demo_class_filtering()
            demo_detection_zones()
            demo_performance_optimization()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
