# Project Bab 06: FaceGuard - Smart Attendance System

## Deskripsi Project

### Background Story

**PT. Maju Digital Indonesia** adalah perusahaan teknologi dengan 200+ karyawan. Sistem absensi fingerprint yang ada mengalami masalah:

1. **Antrian Panjang**: Karyawan harus menunggu untuk scan fingerprint
2. **Hygiene Concern**: Touch-based system kurang higienis pasca-pandemi
3. **Buddy Punching**: Tidak bisa mendeteksi jika seseorang absen untuk orang lain
4. **Hardware Mahal**: Fingerprint scanner per lantai costnya tinggi

**Solusi yang diminta**: Sistem absensi contactless berbasis face recognition yang:
- Dapat mengenali karyawan secara real-time
- Mencegah fraud (buddy punching)
- Terintegrasi dengan sistem HR existing
- Cost-effective (menggunakan webcam biasa)

### Project Overview

Anda diminta mengembangkan **FaceGuard** - sistem absensi pintar dengan fitur:

1. **Employee Enrollment**: Registrasi wajah karyawan baru
2. **Face Verification**: Verifikasi identitas saat check-in/check-out
3. **Anti-Spoofing**: Deteksi foto/video untuk mencegah fraud
4. **Attendance Logging**: Pencatatan waktu otomatis
5. **Report Generation**: Laporan kehadiran harian/mingguan

---

## Struktur Project

```
FaceGuard/
├── src/
│   ├── __init__.py
│   ├── face_detector.py       # Face detection module
│   ├── face_recognizer.py     # Face recognition/embedding
│   ├── face_database.py       # Employee database management
│   ├── anti_spoofing.py       # Liveness detection
│   ├── attendance_logger.py   # Attendance logging
│   └── report_generator.py    # Report generation
├── data/
│   ├── employees/             # Employee face images
│   │   ├── EMP001/
│   │   ├── EMP002/
│   │   └── ...
│   ├── embeddings/            # Stored face embeddings
│   └── logs/                  # Attendance logs
├── models/                    # Pre-trained models
├── tests/                     # Unit tests
├── main.py                    # Main application
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

---

## Module Specifications

### Module 1: Employee Enrollment (25%)

#### 1.1 Face Capture System

```python
class FaceCapture:
    """
    Capture multiple face images untuk enrollment
    """
    
    def capture_faces(self, employee_id, num_images=5):
        """
        Capture multiple face images dari webcam
        
        Args:
            employee_id: ID karyawan (format: EMP001)
            num_images: Jumlah gambar yang diambil
            
        Returns:
            List paths gambar yang tersimpan
        """
        pass
    
    def validate_face(self, image):
        """
        Validasi kualitas gambar wajah
        - Cek ada wajah terdeteksi
        - Cek ukuran wajah cukup besar
        - Cek tidak blur
        - Cek pencahayaan cukup
        
        Returns:
            (is_valid, message)
        """
        pass
```

**Requirements**:
- Capture minimal 5 gambar per karyawan
- Validasi kualitas gambar sebelum menyimpan
- Simpan dengan naming convention: `{employee_id}_{timestamp}.jpg`
- Handle lighting conditions berbeda

#### 1.2 Face Embedding Generation

```python
class EmbeddingGenerator:
    """
    Generate face embeddings untuk database
    """
    
    def generate_embedding(self, image_path):
        """
        Generate embedding vector dari gambar wajah
        
        Returns:
            numpy array shape (128,) atau (512,)
        """
        pass
    
    def generate_template(self, image_paths):
        """
        Generate template embedding dari multiple images
        (rata-rata dari beberapa embeddings)
        
        Returns:
            Template embedding untuk identitas
        """
        pass
```

**Requirements**:
- Gunakan pre-trained model (FaceNet/ArcFace/dlib)
- Template = average dari embeddings multiple images
- Handle face alignment sebelum embedding

#### 1.3 Database Management

```python
class EmployeeDatabase:
    """
    Manage employee face database
    """
    
    def add_employee(self, employee_id, name, department, embedding):
        """Tambah karyawan baru ke database"""
        pass
    
    def remove_employee(self, employee_id):
        """Hapus karyawan dari database"""
        pass
    
    def update_employee(self, employee_id, new_embedding=None, **kwargs):
        """Update data karyawan"""
        pass
    
    def get_employee(self, employee_id):
        """Get employee info"""
        pass
    
    def get_all_embeddings(self):
        """Get semua embeddings untuk matching"""
        pass
    
    def save_database(self, path):
        """Save database ke file"""
        pass
    
    def load_database(self, path):
        """Load database dari file"""
        pass
```

**Database Format** (JSON atau SQLite):
```json
{
    "EMP001": {
        "name": "John Doe",
        "department": "IT",
        "enrolled_date": "2024-01-15",
        "embedding": [...],
        "photos": ["EMP001_001.jpg", "EMP001_002.jpg"]
    }
}
```

---

### Module 2: Face Verification System (35%)

#### 2.1 Face Detection

```python
class FaceDetector:
    """
    Detect faces in images/video frames
    """
    
    def __init__(self, method='mtcnn'):
        """
        method: 'haar', 'hog', 'mtcnn', 'retinaface'
        """
        pass
    
    def detect_faces(self, image):
        """
        Detect all faces in image
        
        Returns:
            List of (bbox, confidence, landmarks)
        """
        pass
    
    def detect_largest_face(self, image):
        """
        Detect the largest face (closest to camera)
        """
        pass
```

**Requirements**:
- Support multiple detection methods
- Return bounding box + confidence
- Optional: return landmarks untuk alignment

#### 2.2 Face Matching

```python
class FaceMatcher:
    """
    Match face against database
    """
    
    def __init__(self, database, threshold=0.6):
        self.database = database
        self.threshold = threshold
    
    def verify(self, image, claimed_id):
        """
        Verify claimed identity (1:1)
        
        Returns:
            (is_verified, confidence, message)
        """
        pass
    
    def identify(self, image, top_k=1):
        """
        Identify person from database (1:N)
        
        Returns:
            List of (employee_id, confidence)
        """
        pass
    
    def compute_similarity(self, embedding1, embedding2, metric='cosine'):
        """
        Compute similarity between two embeddings
        """
        pass
```

**Requirements**:
- Support Euclidean dan Cosine distance
- Configurable threshold
- Return confidence score
- Handle unknown person (tidak ada di database)

#### 2.3 Anti-Spoofing (Liveness Detection)

```python
class LivenessDetector:
    """
    Detect spoofing attempts (photo/video attacks)
    """
    
    def detect_liveness_texture(self, image):
        """
        Texture-based liveness detection
        - LBP (Local Binary Pattern)
        - Blur analysis
        
        Returns:
            (is_live, confidence)
        """
        pass
    
    def detect_liveness_blink(self, frames):
        """
        Blink-based liveness detection
        
        Args:
            frames: Sequence of frames
            
        Returns:
            (is_live, blink_count)
        """
        pass
    
    def detect_liveness_motion(self, frames):
        """
        Motion-based liveness (head movement)
        
        Returns:
            (is_live, motion_score)
        """
        pass
```

**Spoofing Types to Detect**:
1. **Print Attack**: Foto yang dicetak
2. **Replay Attack**: Video playback pada device lain
3. **3D Mask Attack**: (advanced, optional)

**Liveness Methods**:
1. **Passive**: Analisis texture (blur, reflection, moire pattern)
2. **Active**: Minta user melakukan aksi (kedip, gerak kepala)

---

### Module 3: Attendance System (40%)

#### 3.1 Attendance Logger

```python
class AttendanceLogger:
    """
    Log attendance records
    """
    
    def __init__(self, log_path):
        self.log_path = log_path
    
    def check_in(self, employee_id, timestamp=None, method='face'):
        """
        Record check-in
        
        Args:
            employee_id: Employee ID
            timestamp: Waktu check-in (default: now)
            method: 'face', 'manual', 'override'
        """
        pass
    
    def check_out(self, employee_id, timestamp=None):
        """Record check-out"""
        pass
    
    def get_today_attendance(self):
        """Get attendance records for today"""
        pass
    
    def get_employee_attendance(self, employee_id, start_date, end_date):
        """Get attendance history for employee"""
        pass
    
    def export_to_csv(self, output_path, date_range=None):
        """Export attendance to CSV"""
        pass
```

**Log Format** (CSV):
```csv
timestamp,employee_id,employee_name,event_type,method,confidence
2024-01-15 08:30:25,EMP001,John Doe,check_in,face,0.95
2024-01-15 17:35:10,EMP001,John Doe,check_out,face,0.92
```

#### 3.2 Report Generator

```python
class ReportGenerator:
    """
    Generate attendance reports
    """
    
    def daily_report(self, date):
        """
        Generate daily attendance report
        
        Returns:
            - Total hadir
            - Total tidak hadir
            - Terlambat
            - Pulang awal
            - Overtime
        """
        pass
    
    def weekly_report(self, week_start):
        """Generate weekly summary"""
        pass
    
    def employee_report(self, employee_id, month):
        """Generate individual employee report"""
        pass
    
    def export_pdf(self, report_data, output_path):
        """Export report to PDF (bonus)"""
        pass
```

**Report Metrics**:
- Total working days
- Present/Absent count
- Late arrivals (>09:00)
- Early departures (<17:00)
- Average working hours
- Overtime hours

#### 3.3 Real-time System

```python
class FaceGuardSystem:
    """
    Main application - integrates all modules
    """
    
    def __init__(self, config):
        self.detector = FaceDetector(config.detection_method)
        self.recognizer = FaceRecognizer()
        self.database = EmployeeDatabase(config.db_path)
        self.liveness = LivenessDetector()
        self.logger = AttendanceLogger(config.log_path)
    
    def run_enrollment_mode(self):
        """Interactive enrollment mode"""
        pass
    
    def run_attendance_mode(self):
        """Real-time attendance mode"""
        pass
    
    def run_admin_mode(self):
        """Admin mode untuk reporting"""
        pass
```

**Real-time Pipeline**:
```
Frame → Face Detection → Liveness Check → Face Recognition → Attendance Log
```

---

## Deliverables

### 1. Source Code (40%)

**Kriteria Penilaian**:
- [ ] Semua module terimplementasi
- [ ] Code clean dan well-documented
- [ ] Error handling yang proper
- [ ] Unit tests untuk critical functions

### 2. Demo Video (30%)

**Durasi**: 10-15 menit

**Konten**:
1. **Introduction** (1 menit)
   - Overview sistem
   - Architecture diagram

2. **Enrollment Demo** (3 menit)
   - Register karyawan baru
   - Multi-image capture
   - Database management

3. **Attendance Demo** (4 menit)
   - Check-in process
   - Check-out process
   - Unknown person handling
   - Anti-spoofing demo

4. **Reporting Demo** (2 menit)
   - Daily report
   - Employee history

5. **Technical Explanation** (3 menit)
   - Face detection method
   - Recognition approach
   - Performance metrics

### 3. Documentation (30%)

**README.md** harus mencakup:
- Installation instructions
- Configuration guide
- Usage instructions
- Architecture diagram
- API reference
- Troubleshooting guide

---

## Grading Rubric

### Module 1: Enrollment (25%)

| Aspek | Excellent (90-100) | Good (70-89) | Adequate (50-69) | Poor (<50) |
|-------|-------------------|--------------|------------------|------------|
| Face Capture | Multi-pose, quality validation | Single pose, basic validation | Capture works, no validation | Not working |
| Embedding | Template averaging, alignment | Single embedding, no alignment | Basic extraction | Not working |
| Database | CRUD complete, persistence | Basic CRUD, persistence | Add/Get only | Not working |

### Module 2: Verification (35%)

| Aspek | Excellent (90-100) | Good (70-89) | Adequate (50-69) | Poor (<50) |
|-------|-------------------|--------------|------------------|------------|
| Detection | Multiple methods, landmarks | Single deep method | Haar only | Not working |
| Matching | Verify + Identify, tuned threshold | One method, fixed threshold | Basic matching | Not working |
| Anti-Spoofing | 2+ methods implemented | 1 method working | Basic attempt | Not implemented |

### Module 3: Attendance (40%)

| Aspek | Excellent (90-100) | Good (70-89) | Adequate (50-69) | Poor (<50) |
|-------|-------------------|--------------|------------------|------------|
| Logging | Complete CRUD, export | Check-in/out, basic query | Check-in only | Not working |
| Reporting | Multiple reports, visualization | Basic report generation | Simple listing | Not implemented |
| Real-time | Smooth (≥15 FPS), all features | Works but slow | Batch mode only | Not working |

---

## Bonus Points

1. **UI/UX** (+10%):
   - GUI application (Tkinter/PyQt/Web)
   - Clean interface design

2. **Advanced Anti-Spoofing** (+5%):
   - Deep learning based liveness
   - 3D depth estimation

3. **Multi-camera Support** (+5%):
   - Handle multiple camera inputs
   - Location-based logging

4. **Integration** (+5%):
   - REST API untuk HR system
   - Email notification

5. **Performance Optimization** (+5%):
   - GPU acceleration
   - Efficient face tracking

---

## Timeline

| Minggu | Deliverable |
|--------|-------------|
| 1-2 | Module 1: Enrollment System |
| 3-4 | Module 2: Verification System |
| 5 | Module 3: Attendance & Reporting |
| 6 | Integration, Testing, Demo |

---

## Technical Requirements

### Minimum Requirements

```
Python >= 3.8
OpenCV >= 4.5.0
face_recognition >= 1.3.0 atau dlib >= 19.22
numpy >= 1.20.0
```

### Recommended Libraries

```
# Face Detection
mtcnn
retinaface

# Face Recognition
facenet-pytorch
insightface

# OCR (optional untuk ID card)
easyocr
pytesseract

# GUI (bonus)
tkinter
streamlit

# Reporting
pandas
matplotlib
reportlab (PDF)
```

---

## Sample Test Scenarios

### Scenario 1: Normal Check-in
```
1. Karyawan EMP001 datang pukul 08:30
2. Sistem detect wajah
3. Liveness check passed
4. Recognition: EMP001 (confidence: 0.95)
5. Check-in logged
6. Display: "Selamat Pagi, John Doe!"
```

### Scenario 2: Unknown Person
```
1. Orang tidak dikenal datang
2. Sistem detect wajah
3. Recognition: No match found
4. Display: "Wajah tidak terdaftar. Silakan hubungi HR."
```

### Scenario 3: Spoofing Attempt
```
1. Seseorang mencoba menggunakan foto
2. Sistem detect wajah
3. Liveness check: FAILED
4. Display: "Deteksi spoofing! Gunakan wajah asli."
5. Log suspicious activity
```

### Scenario 4: Late Arrival
```
1. Karyawan EMP002 datang pukul 09:30 (terlambat)
2. Normal check-in process
3. System marks as "LATE"
4. Display: "Check-in berhasil. Anda terlambat 30 menit."
```

---

## Evaluation Checklist

### Enrollment Module
- [ ] Capture multiple face images
- [ ] Validate image quality
- [ ] Generate face embeddings
- [ ] Store in database
- [ ] CRUD operations

### Verification Module
- [ ] Face detection working
- [ ] Face recognition accurate
- [ ] Threshold configurable
- [ ] Handle unknown faces
- [ ] Anti-spoofing implemented

### Attendance Module
- [ ] Check-in logging
- [ ] Check-out logging
- [ ] Daily report generation
- [ ] CSV export
- [ ] Real-time operation

### Documentation
- [ ] README complete
- [ ] Code documented
- [ ] Demo video recorded
- [ ] Installation tested

---

*Project ini mensimulasikan development real-world attendance system menggunakan teknologi face recognition*
