# VERIFICATION REPORT — Bab 12: Depth Estimation

Tanggal: 2026-02-05

## Ringkasan Eksekusi

Semua skrip praktikum Bab 12 dijalankan berurutan setelah download data sampel. Window visualisasi telah ditutup otomatis (timeout 2 detik).

## Perintah yang Dijalankan

1. `download_sample_data.py`
2. `01_stereo_calibration.py`
3. `02_stereo_rectification.py`
4. `03_block_matching.py`
5. `04_sgm_matching.py`
6. `05_disparity_to_depth.py`
7. `06_monocular_depth.py`
8. `07_depth_applications.py`

## Hasil & Output Utama

- Data sintetis stereo + checkerboard + street scene dibuat di:
  - praktikum/data/stereo
  - praktikum/data/calibration
  - praktikum/data/images
- Kalibrasi stereo tersimpan di:
  - Bab-12-Depth-Estimation/data/calibration_results/stereo_calibration.yaml
- Rectification outputs:
  - Bab-12-Depth-Estimation/data/rectified/rectified_left.png
  - Bab-12-Depth-Estimation/data/rectified/rectified_right.png
  - Bab-12-Depth-Estimation/data/rectified/rectification_comparison.png
- Disparity outputs:
  - Bab-12-Depth-Estimation/data/disparity/disparity_bm.png
  - Bab-12-Depth-Estimation/data/disparity/disparity_bm_colored.png
  - Bab-12-Depth-Estimation/data/disparity/bm_parameter_comparison.png
  - Bab-12-Depth-Estimation/data/disparity/comparison_bm_vs_sgbm.png
- Depth outputs:
  - Bab-12-Depth-Estimation/praktikum/output/output5/depth/depth_map.png
  - Bab-12-Depth-Estimation/praktikum/output/output5/depth/point_cloud.ply
- Aplikasi depth outputs:
  - Bab-12-Depth-Estimation/praktikum/output/output7/applications/applications_overview.png
  - Bab-12-Depth-Estimation/praktikum/output/output7/applications/point_cloud.ply

## Catatan & Peringatan

- Download Middlebury (tsukuba) gagal (HTTP 404). Data sintetis digunakan sebagai fallback.
- `04_sgm_matching.py`: WLS filter tidak tersedia (opencv-contrib belum terpasang).
- `05_disparity_to_depth.py`: Viewer Open3D gagal membuat window (GL/Wayland). File .ply tetap tersimpan.
- `06_monocular_depth.py`: PyTorch belum terpasang, sehingga MiDaS tidak dijalankan (demo sintetis tampil).

## Status

✅ Semua skrip berjalan sampai selesai dengan fallback yang sesuai.

Jika ingin hasil MiDaS dan WLS:
- Install PyTorch + torchvision + timm
- Install opencv-contrib-python
