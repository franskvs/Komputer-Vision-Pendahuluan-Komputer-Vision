# Verification Report - Bab 4 (Model Fitting)

Tanggal: 2026-02-05

## Ringkasan
Semua program praktikum Bab 4 telah dijalankan tanpa error runtime. Output log tersimpan pada file [Bab-04-Model-Fitting/verification_run.log](Bab-04-Model-Fitting/verification_run.log).

## Lingkungan
- OS: Linux
- Python: python3

## Hasil Uji
| Program | Status | Catatan |
|---|---|---|
| 01_feature_detection.py | ✅ OK | Output keypoints & visualisasi tampil, auto-close aktif |
| 02_feature_matching.py | ✅ OK | Matching BF/FLANN + demo ratio, auto-close aktif |
| 03_ransac.py | ✅ OK | RANSAC vs LS + demo threshold, auto-close aktif |
| 04_hough_lines.py | ✅ OK | HoughLines & HoughLinesP, auto-close aktif |
| 05_hough_circles.py | ✅ OK | HoughCircles + demo parameter, auto-close aktif |
| 06_homography.py | ✅ OK | Homography + RANSAC, auto-close aktif |
| 07_perspective_correction.py | ✅ OK | Document scan pipeline, auto-close aktif |
| 08_optical_flow.py | ✅ OK | Sparse & dense flow, auto-close aktif |

## Catatan
- Semua visualisasi Matplotlib kini auto-close dalam 2 detik agar eksekusi batch dapat berjalan berurutan.
- Tidak ditemukan exception pada log eksekusi.
