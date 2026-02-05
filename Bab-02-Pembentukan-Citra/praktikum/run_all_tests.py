#!/usr/bin/env python3
# ============================================================
# COMPREHENSIVE TEST & VERIFICATION - BAB 2 PEMBENTUKAN CITRA
# ============================================================

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# Daftar semua program (termasuk versi auto untuk yang interactive)
PROGRAMS = [
    {"num": 1, "file": "01_translasi.py", "name": "Translasi (Translation)", "concept": "Pergeseran geometri 2D"},
    {"num": 2, "file": "02_rotasi.py", "name": "Rotasi (Rotation)", "concept": "Rotasi dengan matrix 2D"},
    {"num": 3, "file": "03_scaling.py", "name": "Scaling (Resize)", "concept": "Interpolasi & resampling"},
    {"num": 4, "file": "04_affine_transform.py", "name": "Affine Transform", "concept": "Transformasi affine umum"},
    {"num": 5, "file": "05_perspektif_transform_auto.py", "name": "Perspektif Transform", "concept": "Koreksi perspektif dokumen"},
    {"num": 6, "file": "06_document_scanner_auto.py", "name": "Document Scanner", "concept": "Auto-detect & scan dokumen"},
    {"num": 7, "file": "07_kalibrasi_kamera.py", "name": "Kalibrasi Kamera", "concept": "Camera intrinsics & distortion"},
    {"num": 8, "file": "08_3d_rotation.py", "name": "3D Rotation", "concept": "Rodrigues formula"},
    {"num": 9, "file": "09_projection_perspective.py", "name": "Projection", "concept": "Ortografik vs perspektif"},
    {"num": 10, "file": "10_lens_distortion.py", "name": "Lens Distortion", "concept": "Radial distortion correction"},
    {"num": 11, "file": "11_sampling_aliasing.py", "name": "Sampling & Aliasing", "concept": "Nyquist theorem & anti-aliasing"},
    {"num": 12, "file": "12_color_spaces.py", "name": "Color Spaces", "concept": "RGB, HSV, LAB konversi"},
    {"num": 13, "file": "13_gamma_correction.py", "name": "Gamma Correction", "concept": "Gamma encode/decode"},
    {"num": 14, "file": "14_photometric_shading.py", "name": "Photometric Shading", "concept": "Lambertian + Phong model"},
    {"num": 15, "file": "15_compression_artifacts.py", "name": "Compression Artifacts", "concept": "JPEG compression quality"},
]

def check_output_exists(program_num):
    """Check if output directory exists and has files."""
    output_dir = os.path.join(DIR_OUTPUT, f"output{program_num}")
    if not os.path.exists(output_dir):
        return False, 0, []
    
    files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return len(files) > 0, len(files), files

def run_program(program_file):
    """Run a single program."""
    program_path = os.path.join(DIR_SCRIPT, program_file)
    
    if not os.path.exists(program_path):
        return False, f"File tidak ditemukan", 0.0
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, program_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=DIR_SCRIPT
        )
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            return True, "SUCCESS", elapsed_time
        else:
            error_msg = result.stderr[:150] if result.stderr else "Unknown error"
            return False, f"Error: {error_msg}", elapsed_time
    
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (>60s)", 60.0
    except Exception as e:
        return False, f"Exception: {str(e)[:80]}", 0.0

def main():
    """Main test runner with comprehensive verification."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("COMPREHENSIVE TEST & VERIFICATION - BAB 2: PEMBENTUKAN CITRA")
    print("=" * 80)
    print(f"Timestamp: {timestamp}")
    print(f"Directory: {DIR_SCRIPT}")
    print(f"Total Programs: {len(PROGRAMS)}\n")
    
    results = []
    total_time = 0.0
    
    for prog in PROGRAMS:
        num = prog["num"]
        prog_file = prog["file"]
        prog_name = prog["name"]
        
        print(f"\n[{num:2d}/15] {prog_name:35} ", end="", flush=True)
        
        # Run program
        success, message, exec_time = run_program(prog_file)
        total_time += exec_time
        
        # Check output
        has_output, num_files, files = check_output_exists(num)
        
        # Store result
        results.append({
            "num": num,
            "file": prog_file,
            "name": prog_name,
            "concept": prog["concept"],
            "success": success,
            "message": message,
            "exec_time": exec_time,
            "has_output": has_output,
            "num_files": num_files,
            "output_files": files
        })
        
        # Print status
        status = "✓ PASS" if success else "✗ FAIL"
        output_status = f"{num_files} files" if has_output else "No output"
        time_str = f"{exec_time:.2f}s"
        
        print(f"[{status}] {output_status:12} ({time_str})")
        
        if not success:
            print(f"     {message[:70]}")
    
    # ========================================
    # SUMMARY STATISTICS
    # ========================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    with_output = sum(1 for r in results if r["has_output"])
    total_files = sum(r["num_files"] for r in results)
    
    print(f"\nExecution Results:")
    print(f"  ✓ Passed:  {passed}/{len(PROGRAMS)} programs")
    print(f"  ✗ Failed:  {failed}/{len(PROGRAMS)} programs")
    print(f"\nOutput Verification:")
    print(f"  ✓ With Output: {with_output}/{len(PROGRAMS)} programs")
    print(f"  📁 Total Files: {total_files} output files generated")
    print(f"\nExecution Time:")
    print(f"  ⏱ Total: {total_time:.2f}s")
    print(f"  ⏱ Average: {total_time/len(PROGRAMS):.2f}s per program")
    
    # ========================================
    # DETAILED OUTPUT TABLE
    # ========================================
    print("\n" + "=" * 80)
    print("DETAILED OUTPUT VERIFICATION")
    print("=" * 80)
    print(f"\n{'No':>3} {'Program Name':35} {'Files':>6} {'Status':>8}")
    print("-" * 80)
    
    for r in results:
        status = "✓ OK" if r["has_output"] else "✗ NONE"
        print(f"{r['num']:3d}. {r['name']:35} {r['num_files']:6d} {status:>8}")
    
    # ========================================
    # CONCEPT COVERAGE
    # ========================================
    print("\n" + "=" * 80)
    print("KONSEP YANG TERCAKUP")
    print("=" * 80)
    
    categories = {
        "Transformasi Geometri": [1, 2, 3, 4, 5, 6],
        "Kalibrasi & Proyeksi": [7, 8, 9, 10],
        "Sampling & Color": [11, 12],
        "Fotometri": [13, 14, 15]
    }
    
    for category, nums in categories.items():
        print(f"\n{category}:")
        for num in nums:
            prog = next(r for r in results if r["num"] == num)
            status = "✓" if prog["has_output"] else "✗"
            print(f"  {status} {num:2d}. {prog['name']:30} → {prog['concept']}")
    
    # ========================================
    # FAILED PROGRAMS DETAILS
    # ========================================
    if failed > 0:
        print("\n" + "=" * 80)
        print("FAILED PROGRAMS DETAILS")
        print("=" * 80)
        
        for r in results:
            if not r["success"]:
                print(f"\n✗ {r['num']:2d}. {r['file']}:")
                print(f"   {r['message']}")
    
    # ========================================
    # REAL-WORLD APPLICATIONS
    # ========================================
    print("\n" + "=" * 80)
    print("PENERAPAN NYATA (REAL-WORLD APPLICATIONS)")
    print("=" * 80)
    print("""
TRANSFORMASI GEOMETRI:
✓ Mobile Scanner Apps (CamScanner, Adobe Scan)
✓ Photo Editing (Instagram, Snapseed filters)
✓ Augmented Reality (AR face filters)
✓ Document Digitization

KALIBRASI & PROYEKSI:
✓ Self-Driving Cars (camera calibration)
✓ 3D Reconstruction (photogrammetry)
✓ Robot Vision (depth estimation)
✓ Surveillance Systems

COLOR & SAMPLING:
✓ Image Compression (JPEG, WebP)
✓ Color Grading (film/video production)
✓ Medical Imaging (CT scan, MRI)

FOTOMETRI:
✓ HDR Photography
✓ Game Engines (realistic lighting)
✓ Computer Graphics Rendering
    """)
    
    # ========================================
    # RECOMMENDATIONS
    # ========================================
    print("\n" + "=" * 80)
    print("NEXT STEPS & RECOMMENDATIONS")
    print("=" * 80)
    
    if passed == len(PROGRAMS):
        print("""
🎉 SEMUA PROGRAM BERHASIL!

✓ Semua 15 program telah berjalan dengan sukses
✓ Output images telah di-generate dengan benar
✓ Praktikum siap untuk digunakan

Langkah selanjutnya:
1. Review output images di folder output/
2. Pelajari kode untuk memahami implementasi
3. Eksperimen dengan parameter berbeda
4. Coba dengan gambar sendiri
        """)
    else:
        print(f"""
⚠ Ada {failed} program yang gagal

Tindakan yang diperlukan:
1. Review error messages di atas
2. Fix programs yang gagal
3. Re-run test setelah perbaikan
        """)
    
    # Save verification report
    report_path = os.path.join(DIR_SCRIPT, "VERIFICATION_REPORT.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"VERIFICATION REPORT - BAB 2 PEMBENTUKAN CITRA\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"=" * 80 + "\n\n")
        f.write(f"Total Programs: {len(PROGRAMS)}\n")
        f.write(f"Passed: {passed}/{len(PROGRAMS)}\n")
        f.write(f"Failed: {failed}/{len(PROGRAMS)}\n")
        f.write(f"Output Files: {total_files}\n")
        f.write(f"Total Execution Time: {total_time:.2f}s\n\n")
        
        for r in results:
            f.write(f"{r['num']:2d}. {r['name']:35} | ")
            f.write(f"Status: {'PASS' if r['success'] else 'FAIL':4} | ")
            f.write(f"Files: {r['num_files']:3d} | ")
            f.write(f"Time: {r['exec_time']:.2f}s\n")
    
    print(f"\n📄 Verification report saved: {report_path}")
    print("\n✓ Testing complete!\n")

if __name__ == "__main__":
    main()
