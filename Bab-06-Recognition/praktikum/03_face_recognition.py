"""
=============================================================================
PRAKTIKUM 03 - FACE RECOGNITION
=============================================================================
Program ini mendemonstrasikan Face Recognition menggunakan berbagai metode.

Konsep yang dipelajari:
1. Face embedding dan face encoding
2. Perbandingan wajah dengan distance metrics
3. Face database management
4. One-shot learning untuk face recognition

Face Recognition vs Face Detection:
- Detection: Menemukan LOKASI wajah dalam gambar
- Recognition: MENGIDENTIFIKASI siapa wajah tersebut

Kebutuhan:
- opencv-python >= 4.8.0
- numpy
- face_recognition (optional, untuk embedding)
- dlib (optional, untuk landmark)

Author: [Nama Mahasiswa]
NIM: [NIM Mahasiswa]
Tanggal: [Tanggal Praktikum]
=============================================================================
"""

import cv2
import numpy as np
import os
from pathlib import Path

# Check optional libraries
FACE_RECOGNITION_AVAILABLE = False
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
    print("[INFO] face_recognition library tersedia")
except ImportError:
    print("[WARNING] face_recognition tidak tersedia - menggunakan OpenCV")


def print_face_recognition_concepts():
    """
    Menampilkan konsep Face Recognition.
    """
    print("\n" + "="*70)
    print("KONSEP FACE RECOGNITION")
    print("="*70)
    
    print("""
    [FACE RECOGNITION PIPELINE]
    ─────────────────────────────────────────────────────────────────────
    
    1. Face Detection
       Input Image → Detect Faces → Bounding Boxes
    
    2. Face Alignment (Optional)
       Cropped Face → Detect Landmarks → Align to Template
    
    3. Feature Extraction (Embedding)
       Aligned Face → Deep Network → 128/512-dim Vector
    
    4. Face Matching
       Query Embedding ←→ Database Embeddings → Similarity Score
    
    
    [FACE EMBEDDING]
    ─────────────────────────────────────────────────────────────────────
    
    Face Embedding adalah representasi numerik wajah dalam vector space.
    
    Karakteristik embedding yang baik:
    - Wajah orang SAMA → Vector DEKAT (low distance)
    - Wajah orang BEDA → Vector JAUH (high distance)
    
    ┌─────────────┐     Deep CNN      ┌─────────────┐
    │  Face Image │ ───────────────→  │ 128-d Vector│
    │  224×224×3  │    (FaceNet,      │ [0.1, 0.3,  │
    │             │     ArcFace)      │  ..., 0.5]  │
    └─────────────┘                   └─────────────┘
    
    
    [DISTANCE METRICS]
    ─────────────────────────────────────────────────────────────────────
    
    1. Euclidean Distance
       d = √(Σ(ai - bi)²)
       Threshold: ~0.6 untuk face_recognition library
    
    2. Cosine Similarity
       sim = (a·b) / (||a|| × ||b||)
       Range: [-1, 1], higher = more similar
    
    3. L2 Normalized Euclidean
       Normalize vectors ke unit length, lalu Euclidean
    
    
    [POPULAR FACE RECOGNITION MODELS]
    ─────────────────────────────────────────────────────────────────────
    
    ┌─────────────────┬─────────────────┬─────────────────────────────┐
    │ Model           │ Embedding Dim   │ Notes                        │
    ├─────────────────┼─────────────────┼─────────────────────────────┤
    │ FaceNet         │ 128             │ Google, triplet loss         │
    │ ArcFace         │ 512             │ State-of-the-art accuracy    │
    │ VGGFace         │ 2048/4096       │ VGG-based                    │
    │ DeepFace        │ 4096            │ Facebook                     │
    │ dlib (ResNet)   │ 128             │ Used by face_recognition lib │
    └─────────────────┴─────────────────┴─────────────────────────────┘
    """)


def create_sample_face_images():
    """
    Membuat sample face images untuk demonstrasi.
    """
    faces_dir = "sample_faces"
    os.makedirs(faces_dir, exist_ok=True)
    
    # Buat beberapa sample synthetic faces
    for i in range(3):
        # Generate synthetic face-like image
        img = np.ones((200, 200, 3), dtype=np.uint8) * 200
        
        # Add face-like features
        center = (100, 100)
        
        # Face oval
        cv2.ellipse(img, center, (60, 80), 0, 0, 360, (180, 160, 140), -1)
        
        # Eyes
        eye_y = 80
        cv2.ellipse(img, (70, eye_y), (15, 10), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(img, (130, eye_y), (15, 10), 0, 0, 360, (255, 255, 255), -1)
        cv2.circle(img, (70 + i*2, eye_y), 5, (50, 50, 50), -1)
        cv2.circle(img, (130 + i*2, eye_y), 5, (50, 50, 50), -1)
        
        # Nose
        pts = np.array([[100, 90], [90, 120], [110, 120]], np.int32)
        cv2.fillPoly(img, [pts], (160, 140, 120))
        
        # Mouth
        cv2.ellipse(img, (100, 145), (25, 10+i*3), 0, 0, 180, (150, 100, 100), -1)
        
        # Variation
        if i == 1:
            cv2.rectangle(img, (60, 50), (140, 65), (50, 30, 20), -1)  # Hair
        elif i == 2:
            cv2.rectangle(img, (55, 75), (80, 90), (100, 100, 100), 2)  # Glasses
            cv2.rectangle(img, (120, 75), (145, 90), (100, 100, 100), 2)
        
        cv2.imwrite(os.path.join(faces_dir, f"person_{i+1}.jpg"), img)
    
    return faces_dir


def demo_face_recognition_opencv():
    """
    Demonstrasi face recognition menggunakan OpenCV's LBPH recognizer.
    
    LBPH = Local Binary Pattern Histograms
    - Tidak memerlukan deep learning
    - Cepat tapi kurang akurat
    - Cocok untuk pembelajaran dasar
    """
    print("\n" + "="*70)
    print("FACE RECOGNITION DENGAN OPENCV LBPH")
    print("="*70)
    
    # Create sample faces
    faces_dir = create_sample_face_images()
    
    print("\n[INFO] OpenCV Face Recognizers:")
    print("  1. LBPH (Local Binary Pattern Histograms)")
    print("  2. EigenFaces")
    print("  3. FisherFaces")
    
    # Check if face module available
    try:
        # Create LBPH Face Recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1,           # Radius untuk LBP operator
            neighbors=8,        # Jumlah neighbors
            grid_x=8,           # Grid cells horizontal
            grid_y=8            # Grid cells vertical
        )
        print("\n[INFO] LBPH Recognizer created successfully")
        
    except AttributeError:
        print("\n[WARNING] cv2.face module tidak tersedia")
        print("[INFO] Install dengan: pip install opencv-contrib-python")
        demo_face_recognition_simulation()
        return
    
    # Prepare training data
    print("\n[STEP 1] Preparing training data...")
    
    faces = []
    labels = []
    label_names = {}
    
    for i in range(3):
        img_path = os.path.join(faces_dir, f"person_{i+1}.jpg")
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        
        if img is not None:
            # Resize to standard size
            img = cv2.resize(img, (100, 100))
            faces.append(img)
            labels.append(i)
            label_names[i] = f"Person {i+1}"
            print(f"  Loaded: {img_path}")
    
    faces = np.array(faces)
    labels = np.array(labels)
    
    print(f"\n[INFO] Training data: {len(faces)} faces, {len(set(labels))} persons")
    
    # Train recognizer
    print("\n[STEP 2] Training LBPH recognizer...")
    recognizer.train(faces, labels)
    print("[INFO] Training complete!")
    
    # Test recognition
    print("\n[STEP 3] Testing recognition...")
    
    # Test dengan salah satu training image (should match)
    test_image = faces[0].copy()
    
    # Add some noise untuk simulasi variasi
    noise = np.random.normal(0, 10, test_image.shape).astype(np.int16)
    test_image_noisy = np.clip(test_image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Predict
    label, confidence = recognizer.predict(test_image_noisy)
    
    print(f"\n[RESULT] Recognition result:")
    print(f"  Predicted: {label_names[label]}")
    print(f"  Confidence: {confidence:.2f}")
    print(f"  (Lower confidence = better match for LBPH)")
    
    # Threshold analysis
    print("\n[INFO] Confidence interpretation (LBPH):")
    print("  < 50: Very confident match")
    print("  50-80: Likely match")
    print("  80-100: Uncertain")
    print("  > 100: Probably not a match")
    
    # Visualisasi
    display = np.hstack([
        cv2.resize(cv2.cvtColor(faces[0], cv2.COLOR_GRAY2BGR), (200, 200)),
        cv2.resize(cv2.cvtColor(test_image_noisy, cv2.COLOR_GRAY2BGR), (200, 200))
    ])
    
    cv2.putText(display, "Training", (50, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(display, "Query", (250, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(display, f"Match: {label_names[label]}", (200, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imshow("Face Recognition (LBPH)", display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def demo_face_recognition_simulation():
    """
    Simulasi face recognition tanpa OpenCV face module.
    """
    print("\n[SIMULASI] Face Recognition workflow")
    print("""
    ─────────────────────────────────────────────────────────────────────
    
    [TRAINING PHASE]
    
    1. Collect face images per person
       person_1/: img1.jpg, img2.jpg, ...
       person_2/: img1.jpg, img2.jpg, ...
    
    2. Detect dan crop faces
       for each image:
           face = detect_and_crop(image)
           faces.append(face)
           labels.append(person_id)
    
    3. Train recognizer
       recognizer.train(faces, labels)
    
    
    [RECOGNITION PHASE]
    
    1. Detect face in query image
       query_face = detect_and_crop(query_image)
    
    2. Predict identity
       label, confidence = recognizer.predict(query_face)
    
    3. Apply threshold
       if confidence < threshold:
           return known_person[label]
       else:
           return "Unknown"
    
    
    [SIMULATED RESULTS]
    ─────────────────────────────────────────────────────────────────────
    
    Query Image → Predicted: Person 1, Confidence: 45.3
    
    Distance to each person in database:
    - Person 1: 45.3 (MATCH)
    - Person 2: 89.7
    - Person 3: 102.4
    """)


def demo_face_embedding():
    """
    Demonstrasi face embedding dan comparison.
    """
    print("\n" + "="*70)
    print("FACE EMBEDDING DAN COMPARISON")
    print("="*70)
    
    if FACE_RECOGNITION_AVAILABLE:
        demo_face_embedding_real()
    else:
        demo_face_embedding_simulation()


def demo_face_embedding_real():
    """
    Demo dengan face_recognition library.
    """
    print("\n[INFO] Using face_recognition library (dlib)")
    
    # Create sample faces
    faces_dir = create_sample_face_images()
    
    # Load images
    print("\n[STEP 1] Loading and encoding faces...")
    
    encodings = []
    names = []
    
    for i in range(3):
        img_path = os.path.join(faces_dir, f"person_{i+1}.jpg")
        img = face_recognition.load_image_file(img_path)
        
        # Get face encoding
        face_locations = face_recognition.face_locations(img)
        
        if len(face_locations) > 0:
            encoding = face_recognition.face_encodings(img, face_locations)[0]
            encodings.append(encoding)
            names.append(f"Person {i+1}")
            print(f"  {names[-1]}: encoding shape = {encoding.shape}")
    
    # Compare embeddings
    print("\n[STEP 2] Comparing face embeddings...")
    print("\nDistance matrix:")
    print("           ", end="")
    for name in names:
        print(f"{name:>12}", end="")
    print()
    
    for i, name_i in enumerate(names):
        print(f"{name_i:>10}", end=" ")
        for j, name_j in enumerate(names):
            dist = face_recognition.face_distance([encodings[j]], encodings[i])[0]
            print(f"{dist:>12.3f}", end="")
        print()
    
    # Recognition test
    print("\n[STEP 3] Recognition test...")
    
    test_img_path = os.path.join(faces_dir, "person_1.jpg")
    test_img = face_recognition.load_image_file(test_img_path)
    test_locations = face_recognition.face_locations(test_img)
    
    if len(test_locations) > 0:
        test_encoding = face_recognition.face_encodings(test_img, test_locations)[0]
        
        # Compare with all known faces
        distances = face_recognition.face_distance(encodings, test_encoding)
        matches = face_recognition.compare_faces(encodings, test_encoding, tolerance=0.6)
        
        print("\nQuery: Unknown face")
        print("Results:")
        for i, (match, dist) in enumerate(zip(matches, distances)):
            status = "MATCH" if match else "No match"
            print(f"  vs {names[i]}: {dist:.3f} ({status})")


def demo_face_embedding_simulation():
    """
    Simulasi face embedding tanpa library.
    """
    print("""
    ─────────────────────────────────────────────────────────────────────
    
    [FACE EMBEDDING SIMULATION]
    
    Face embeddings adalah 128-dimensional vectors:
    
    Person 1: [0.123, -0.456, 0.789, ..., 0.234]
    Person 2: [0.567, -0.123, 0.345, ..., -0.678]
    Person 3: [-0.234, 0.567, -0.890, ..., 0.123]
    
    
    [DISTANCE COMPARISON]
    ─────────────────────────────────────────────────────────────────────
    
    Distance Matrix (Euclidean):
    
               Person 1    Person 2    Person 3
    Person 1      0.000       0.892       0.945
    Person 2      0.892       0.000       0.867
    Person 3      0.945       0.867       0.000
    
    Same person (different photo): ~0.3-0.4
    Different person: ~0.8-1.2
    Threshold: 0.6
    
    
    [RECOGNITION TEST]
    ─────────────────────────────────────────────────────────────────────
    
    Query face → Compute embedding → Compare with database
    
    Query embedding: [0.125, -0.451, 0.792, ..., 0.231]
    
    Distance to Person 1: 0.089 → MATCH (< 0.6)
    Distance to Person 2: 0.901 → No match
    Distance to Person 3: 0.923 → No match
    
    Result: Identified as Person 1
    """)


def demo_face_database():
    """
    Demonstrasi face database management.
    """
    print("\n" + "="*70)
    print("FACE DATABASE MANAGEMENT")
    print("="*70)
    
    print("""
    [DATABASE STRUCTURE]
    ─────────────────────────────────────────────────────────────────────
    
    face_database/
    ├── embeddings.npy        # Numpy array of embeddings [N, 128]
    ├── names.json            # List of names/IDs
    ├── metadata.json         # Additional info per person
    └── images/               # Optional: original images
        ├── person_001/
        ├── person_002/
        └── ...
    
    
    [OPERATIONS]
    ─────────────────────────────────────────────────────────────────────
    
    1. ADD PERSON
       - Capture/load multiple face images
       - Compute average embedding (optional)
       - Add to database
    
    2. RECOGNIZE
       - Compute query embedding
       - Search nearest neighbors in database
       - Apply threshold
    
    3. UPDATE
       - Add more images untuk existing person
       - Recompute embedding
    
    4. DELETE
       - Remove person from database
    
    
    [SCALABILITY]
    ─────────────────────────────────────────────────────────────────────
    
    For large databases (>10,000 faces):
    
    1. Approximate Nearest Neighbors (ANN)
       - Faiss (Facebook)
       - Annoy (Spotify)
       - ScaNN (Google)
    
    2. Clustering
       - Group similar faces
       - Search within clusters
    
    3. Hashing
       - Locality Sensitive Hashing (LSH)
       - Fast approximate search
    """)
    
    # Demo simple database
    print("\n[DEMO] Simple Face Database")
    print("-"*50)
    
    # Simulated database
    np.random.seed(42)
    database = {
        'embeddings': np.random.randn(5, 128).astype(np.float32),
        'names': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    }
    
    # Normalize embeddings
    database['embeddings'] /= np.linalg.norm(
        database['embeddings'], axis=1, keepdims=True
    )
    
    print(f"Database size: {len(database['names'])} persons")
    print(f"Embedding dimension: {database['embeddings'].shape[1]}")
    
    # Simulate search
    print("\n[SEARCH] Query face...")
    
    # Create query (similar to first person)
    query = database['embeddings'][0] + np.random.randn(128) * 0.1
    query /= np.linalg.norm(query)
    
    # Compute distances
    distances = np.linalg.norm(database['embeddings'] - query, axis=1)
    
    # Sort by distance
    sorted_idx = np.argsort(distances)
    
    print("\nSearch results:")
    for i in sorted_idx:
        status = "MATCH" if distances[i] < 0.5 else ""
        print(f"  {database['names'][i]}: {distances[i]:.3f} {status}")


def demo_attendance_system():
    """
    Demonstrasi sistem absensi berbasis face recognition.
    """
    print("\n" + "="*70)
    print("APLIKASI: SISTEM ABSENSI WAJAH")
    print("="*70)
    
    print("""
    [SYSTEM ARCHITECTURE]
    ─────────────────────────────────────────────────────────────────────
    
    ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
    │   Camera    │────→│ Face Detect  │────→│ Face Recognize  │
    │   Input     │     │  & Crop      │     │  (Embedding)    │
    └─────────────┘     └──────────────┘     └────────┬────────┘
                                                      │
                                                      ▼
    ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
    │  Database   │←────│   Logging    │←────│    Matching     │
    │  (Records)  │     │  (Timestamp) │     │   & Decision    │
    └─────────────┘     └──────────────┘     └─────────────────┘
    
    
    [WORKFLOW]
    ─────────────────────────────────────────────────────────────────────
    
    1. ENROLLMENT
       ┌────────────────────────────────────────────────────────────┐
       │ Register new employee:                                     │
       │ - Input: Name, ID, multiple face photos                    │
       │ - Process: Compute face embedding(s)                       │
       │ - Store: embedding + metadata in database                  │
       └────────────────────────────────────────────────────────────┘
    
    2. ATTENDANCE CHECK
       ┌────────────────────────────────────────────────────────────┐
       │ When employee arrives:                                     │
       │ - Capture face from camera                                 │
       │ - Detect and crop face                                     │
       │ - Compute embedding                                        │
       │ - Match against database                                   │
       │ - If match found:                                          │
       │     Log: employee_id, timestamp, "CHECK_IN"                │
       │ - If no match:                                             │
       │     Alert: "Unknown person"                                │
       └────────────────────────────────────────────────────────────┘
    
    
    [CODE EXAMPLE]
    ─────────────────────────────────────────────────────────────────────
    
    class AttendanceSystem:
        def __init__(self):
            self.database = load_database()
            self.threshold = 0.6
            self.records = []
        
        def enroll(self, name, employee_id, images):
            embeddings = [get_embedding(img) for img in images]
            avg_embedding = np.mean(embeddings, axis=0)
            self.database.add(employee_id, name, avg_embedding)
        
        def check_attendance(self, frame):
            faces = detect_faces(frame)
            
            for face in faces:
                embedding = get_embedding(face)
                match, distance = self.database.search(embedding)
                
                if distance < self.threshold:
                    self.log_attendance(match.employee_id)
                    return match.name
                else:
                    return "Unknown"
        
        def log_attendance(self, employee_id):
            record = {
                'employee_id': employee_id,
                'timestamp': datetime.now(),
                'type': 'CHECK_IN'
            }
            self.records.append(record)
            save_to_database(record)
    """)


def main():
    """
    Fungsi utama program.
    """
    print("="*70)
    print("PRAKTIKUM FACE RECOGNITION")
    print("="*70)
    
    print(f"\n[INFO] face_recognition library: {'Available' if FACE_RECOGNITION_AVAILABLE else 'Not available'}")
    
    while True:
        print("\n" + "-"*50)
        print("MENU DEMONSTRASI:")
        print("-"*50)
        print("1. Konsep Face Recognition")
        print("2. Face Recognition dengan OpenCV LBPH")
        print("3. Face Embedding dan Comparison")
        print("4. Face Database Management")
        print("5. Aplikasi: Sistem Absensi")
        print("6. Jalankan Semua Demo")
        print("0. Keluar")
        
        choice = input("\nPilih menu (0-6): ").strip()
        
        if choice == '1':
            print_face_recognition_concepts()
        elif choice == '2':
            demo_face_recognition_opencv()
        elif choice == '3':
            demo_face_embedding()
        elif choice == '4':
            demo_face_database()
        elif choice == '5':
            demo_attendance_system()
        elif choice == '6':
            print_face_recognition_concepts()
            demo_face_recognition_opencv()
            demo_face_embedding()
            demo_face_database()
            demo_attendance_system()
        elif choice == '0':
            print("\n[INFO] Program selesai.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")


if __name__ == "__main__":
    main()
