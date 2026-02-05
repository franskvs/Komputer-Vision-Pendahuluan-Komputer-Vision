"""
Praktikum Computer Vision - Bab 06 (Recognition)
Program 03: Face Recognition (Embedding + Matching)

Tujuan:
1) Mengekstrak embedding wajah (face_recognition jika tersedia).
2) Melakukan pencocokan wajah berbasis jarak (Euclidean/Cosine).
3) Menyimpan hasil dengan auto-close 2 detik.
"""

# Import OpenCV untuk operasi citra.
import cv2
# Import NumPy untuk operasi numerik.
import numpy as np
# Import Path untuk penanganan path file.
from pathlib import Path

# Coba import face_recognition (opsional).
try:
    # Import face_recognition jika tersedia.
    import face_recognition
    # Tandai bahwa library tersedia.
    FACE_RECOGNITION_AVAILABLE = True
except Exception:
    # Tandai bahwa library tidak tersedia.
    FACE_RECOGNITION_AVAILABLE = False


def create_output_dir():
    """Buat folder output hasil face recognition."""
    # Tentukan folder output.
    output_dir = Path("output_face_recognition")
    # Buat folder jika belum ada.
    output_dir.mkdir(parents=True, exist_ok=True)
    # Kembalikan path output.
    return output_dir


def load_face_images():
    """Muat dua gambar wajah dari folder data atau buat sintetis."""
    # Cari file pada folder data.
    candidates = list(Path("data").glob("*.jpg")) + list(Path("data").glob("*.png"))
    # Jika ada minimal dua gambar, gunakan dua pertama.
    if len(candidates) >= 2:
        # Baca gambar pertama.
        img1 = cv2.imread(str(candidates[0]))
        # Baca gambar kedua.
        img2 = cv2.imread(str(candidates[1]))
        # Kembalikan pasangan gambar.
        return img1, img2
    # Buat gambar sintetis jika data kurang.
    img1 = np.ones((220, 220, 3), dtype=np.uint8) * 220
    # Gambar wajah sintetis pertama.
    cv2.ellipse(img1, (110, 120), (70, 90), 0, 0, 360, (200, 170, 140), -1)
    # Tambahkan mata pada wajah pertama.
    cv2.circle(img1, (80, 100), 12, (255, 255, 255), -1)
    # Tambahkan mata kedua.
    cv2.circle(img1, (140, 100), 12, (255, 255, 255), -1)
    # Tambahkan pupil.
    cv2.circle(img1, (80, 100), 5, (40, 40, 40), -1)
    # Tambahkan pupil.
    cv2.circle(img1, (140, 100), 5, (40, 40, 40), -1)
    # Tambahkan mulut.
    cv2.ellipse(img1, (110, 155), (35, 15), 0, 0, 180, (120, 80, 80), 2)
    # Salin wajah pertama untuk kedua.
    img2 = img1.copy()
    # Tambahkan variasi kecil pada wajah kedua.
    cv2.rectangle(img2, (70, 70), (150, 85), (60, 40, 30), -1)
    # Kembalikan dua gambar sintetis.
    return img1, img2


def get_embedding_face_recognition(image):
    """Ekstrak embedding menggunakan face_recognition jika tersedia."""
    # Konversi BGR ke RGB untuk face_recognition.
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Deteksi lokasi wajah.
    locations = face_recognition.face_locations(rgb)
    # Jika tidak ada wajah, kembalikan None.
    if not locations:
        return None
    # Hitung embedding wajah.
    encodings = face_recognition.face_encodings(rgb, locations)
    # Kembalikan embedding pertama.
    return encodings[0]


def get_embedding_lbph(image):
    """Ekstrak fitur sederhana menggunakan histogram LBP sebagai fallback."""
    # Konversi ke grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize untuk konsistensi ukuran.
    gray = cv2.resize(gray, (128, 128))
    # Buat LBP sederhana (neighbor 8).
    lbp = np.zeros_like(gray)
    # Loop piksel pusat.
    for y in range(1, gray.shape[0] - 1):
        # Loop piksel pusat horizontal.
        for x in range(1, gray.shape[1] - 1):
            # Ambil nilai pusat.
            center = gray[y, x]
            # Buat nilai biner dari 8 tetangga.
            code = 0
            # Cek tetangga atas-kiri.
            code |= (gray[y - 1, x - 1] >= center) << 7
            # Cek tetangga atas.
            code |= (gray[y - 1, x] >= center) << 6
            # Cek tetangga atas-kanan.
            code |= (gray[y - 1, x + 1] >= center) << 5
            # Cek tetangga kanan.
            code |= (gray[y, x + 1] >= center) << 4
            # Cek tetangga bawah-kanan.
            code |= (gray[y + 1, x + 1] >= center) << 3
            # Cek tetangga bawah.
            code |= (gray[y + 1, x] >= center) << 2
            # Cek tetangga bawah-kiri.
            code |= (gray[y + 1, x - 1] >= center) << 1
            # Cek tetangga kiri.
            code |= (gray[y, x - 1] >= center) << 0
            # Simpan kode LBP.
            lbp[y, x] = code
    # Hitung histogram LBP sebagai embedding.
    hist = cv2.calcHist([lbp], [0], None, [256], [0, 256]).flatten()
    # Normalisasi histogram agar stabil.
    hist = hist / (np.linalg.norm(hist) + 1e-6)
    # Kembalikan embedding histogram.
    return hist


def compute_distances(vec1, vec2):
    """Hitung jarak Euclidean dan Cosine antara dua embedding."""
    # Hitung jarak Euclidean.
    euclidean = float(np.linalg.norm(vec1 - vec2))
    # Hitung cosine similarity.
    cosine = float(np.dot(vec1, vec2) / ((np.linalg.norm(vec1) * np.linalg.norm(vec2)) + 1e-6))
    # Kembalikan kedua metrik.
    return euclidean, cosine


def show_image(title, image, delay_ms=2000):
    """Tampilkan gambar dan auto-close setelah delay tertentu."""
    # Coba tampilkan jendela jika GUI tersedia.
    try:
        # Tampilkan gambar.
        cv2.imshow(title, image)
        # Tunggu beberapa milidetik.
        cv2.waitKey(delay_ms)
        # Tutup semua jendela.
        cv2.destroyAllWindows()
    except Exception:
        # Abaikan jika display tidak tersedia.
        pass


def main():
    """Fungsi utama untuk demo face recognition."""
    # Muat dua gambar wajah.
    img1, img2 = load_face_images()
    # Pilih metode embedding.
    if FACE_RECOGNITION_AVAILABLE:
        # Ambil embedding dengan face_recognition.
        emb1 = get_embedding_face_recognition(img1)
        # Ambil embedding gambar kedua.
        emb2 = get_embedding_face_recognition(img2)
    else:
        # Gunakan embedding LBP fallback.
        emb1 = get_embedding_lbph(img1)
        # Gunakan embedding LBP untuk gambar kedua.
        emb2 = get_embedding_lbph(img2)
    # Pastikan embedding tersedia.
    if emb1 is None or emb2 is None:
        # Informasikan jika embedding gagal.
        print("Embedding wajah tidak ditemukan pada salah satu gambar.")
        # Keluar dari program.
        return
    # Hitung jarak antar embedding.
    euclidean, cosine = compute_distances(emb1, emb2)
    # Buat anotasi pada gambar pertama.
    cv2.putText(img1, "Face A", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 100, 0), 2)
    # Buat anotasi pada gambar kedua.
    cv2.putText(img2, "Face B", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 100, 0), 2)
    # Buat kanvas gabungan.
    combined = np.hstack((cv2.resize(img1, (220, 220)), cv2.resize(img2, (220, 220))))
    # Tambahkan teks hasil jarak.
    cv2.putText(combined, f"Euclidean: {euclidean:.3f}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    # Tambahkan teks cosine similarity.
    cv2.putText(combined, f"Cosine: {cosine:.3f}", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    # Buat folder output.
    output_dir = create_output_dir()
    # Simpan hasil ke file.
    cv2.imwrite(str(output_dir / "03_face_recognition.jpg"), combined)
    # Cetak ringkasan ke terminal.
    print(f"Euclidean distance: {euclidean:.3f}")
    # Cetak cosine similarity.
    print(f"Cosine similarity: {cosine:.3f}")
    # Tampilkan hasil dengan auto-close.
    show_image("Face Recognition Result", combined)


# Jalankan program saat dieksekusi langsung.
if __name__ == "__main__":
    # Panggil fungsi utama.
    main()
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
