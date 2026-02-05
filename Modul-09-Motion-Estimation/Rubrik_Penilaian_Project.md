# RUBRIK PENILAIAN PROJECT
# BAB 9: SISTEM ANALISIS PERGERAKAN (MotionGuard)

---

## 📊 KOMPONEN PENILAIAN

| No | Komponen | Bobot |
|----|----------|-------|
| 1 | Detection Accuracy | 25% |
| 2 | Tracking Robustness | 25% |
| 3 | Code Quality | 20% |
| 4 | Performance | 15% |
| 5 | Documentation & Demo | 15% |
| **Total** | | **100%** |

---

## 1. DETECTION ACCURACY (25%)

### 1.1 True Positive Rate (12%)

| Skor | Kriteria |
|------|----------|
| 12 | Mendeteksi >95% gerakan nyata |
| 10 | Mendeteksi >85% gerakan nyata |
| 8 | Mendeteksi >75% gerakan nyata |
| 6 | Mendeteksi >60% gerakan nyata |
| 4 | Mendeteksi <60% gerakan nyata |

### 1.2 False Positive Rate (13%)

| Skor | Kriteria |
|------|----------|
| 13 | False alarm <5% |
| 10 | False alarm 5-15% |
| 7 | False alarm 15-25% |
| 4 | False alarm 25-40% |
| 2 | False alarm >40% |

---

## 2. TRACKING ROBUSTNESS (25%)

### 2.1 Track Consistency (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Track ID konsisten sepanjang video |
| 8 | Track ID kadang berubah tapi bisa recover |
| 6 | Track ID sering berubah |
| 4 | Tracking tidak konsisten |
| 0 | Tracking tidak berfungsi |

### 2.2 Multi-Object Handling (8%)

| Skor | Kriteria |
|------|----------|
| 8 | Handle 5+ objek simultan dengan baik |
| 6 | Handle 3-4 objek dengan baik |
| 4 | Handle 2 objek dengan baik |
| 2 | Hanya 1 objek |
| 0 | Tidak bisa track |

### 2.3 Occlusion Handling (7%)

| Skor | Kriteria |
|------|----------|
| 7 | Re-acquire track setelah occlusion |
| 5 | Kadang bisa recover |
| 3 | Track lost setelah occlusion |
| 0 | Tidak handle occlusion |

---

## 3. CODE QUALITY (20%)

### 3.1 Structure & Modularity (8%)

| Skor | Kriteria |
|------|----------|
| 8 | Modular, well-separated concerns |
| 6 | Cukup modular |
| 4 | Kurang modular |
| 2 | Tidak modular |

### 3.2 Readability (6%)

| Skor | Kriteria |
|------|----------|
| 6 | Clean code, good naming, comments |
| 4 | Cukup readable |
| 2 | Sulit dibaca |

### 3.3 Error Handling (6%)

| Skor | Kriteria |
|------|----------|
| 6 | Comprehensive error handling |
| 4 | Basic error handling |
| 2 | Minimal error handling |
| 0 | Tidak ada error handling |

---

## 4. PERFORMANCE (15%)

### 4.1 Frame Rate (10%)

| Skor | Kriteria |
|------|----------|
| 10 | Real-time (>25 FPS) |
| 8 | Near real-time (15-25 FPS) |
| 6 | Usable (10-15 FPS) |
| 4 | Slow (5-10 FPS) |
| 2 | Very slow (<5 FPS) |

### 4.2 Resource Usage (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Efficient, low CPU/memory |
| 3 | Reasonable usage |
| 1 | Resource heavy |

---

## 5. DOCUMENTATION & DEMO (15%)

### 5.1 README (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Complete: install, usage, examples |
| 3 | Basic documentation |
| 1 | Minimal |

### 5.2 Code Documentation (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Docstrings, inline comments |
| 3 | Basic comments |
| 1 | No comments |

### 5.3 Demo Video (5%)

| Skor | Kriteria |
|------|----------|
| 5 | Professional, shows all features |
| 3 | Shows main features |
| 1 | Minimal demo |

---

## 🌟 BONUS

| Fitur | Poin |
|-------|------|
| Person detection integration | +5 |
| Zone-based alerts | +5 |
| Web interface | +5 |
| Statistics dashboard | +5 |

---

## 📝 PENALTI

| Pelanggaran | Penalti |
|-------------|---------|
| Plagiarisme | -100% |
| Terlambat | -10%/hari |
| Tidak berjalan | -50% |
| Crash tanpa handling | -10% |
