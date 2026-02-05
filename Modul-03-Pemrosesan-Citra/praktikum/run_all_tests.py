#!/usr/bin/env python3
# ============================================================
# COMPREHENSIVE TEST & VERIFICATION - BAB 3 PEMROSESAN CITRA
# ============================================================

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# Daftar semua program
PROGRAMS = [
    {"num": 1, "file": "01_brightness_contrast.py", "name": "Brightness & Contrast", "concept": "Point operations"},
    {"num": 2, "file": "02_gamma_correction.py", "name": "Gamma Correction", "concept": "Gamma encoding/decoding"},
    {"num": 3, "file": "03_thresholding.py", "name": "Thresholding", "concept": "Binary, Otsu, adaptive"},
    {"num": 4, "file": "04_histogram_equalization.py", "name": "Histogram Equalization", "concept": "Contrast enhancement"},
    {"num": 5, "file": "05_spatial_filtering.py", "name": "Spatial Filtering", "concept": "Convolution, blur, sharpen"},
    {"num": 6, "file": "06_edge_detection.py", "name": "Edge Detection", "concept": "Sobel, Canny"},
    {"num": 7, "file": "07_morphological_operations.py", "name": "Morphological Operations", "concept": "Erosion, dilation"},
    {"num": 8, "file": "08_image_enhancement_pipeline.py", "name": "Enhancement Pipeline", "concept": "Multi-stage processing"},
    {"num": 9, "file": "09_compositing_matting.py", "name": "Compositing & Matting", "concept": "Alpha blending"},
    {"num": 10, "file": "10_fourier_transform.py", "name": "Fourier Transform", "concept": "FFT, frequency filtering"},
    {"num": 11, "file": "11_pyramids_wavelets.py", "name": "Pyramids & Wavelets", "concept": "Multi-resolution"},
    {"num": 12, "file": "12_geometric_transformations.py", "name": "Geometric Transformations", "concept": "Warp, affine"},
    {"num": 13, "file": "13_steerable_filters_advanced.py", "name": "Steerable Filters", "concept": "Oriented filters"},
    {"num": 14, "file": "14_interpolation_decimation_advanced.py", "name": "Interpolation & Decimation", "concept": "Resampling"},
    {"num": 15, "file": "15_advanced_blending_techniques.py", "name": "Advanced Blending", "concept": "Seamless cloning"},
    {"num": 16, "file": "16_mesh_warping_morphing.py", "name": "Mesh Warping & Morphing", "concept": "Face morphing"},
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
            timeout=120,  # Timeout lebih lama untuk program kompleks
            cwd=DIR_SCRIPT
        )
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            return True, "SUCCESS", elapsed_time
        else:
            error_msg = result.stderr[:150] if result.stderr else "Unknown error"
            return False, f"Error: {error_msg}", elapsed_time
    
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (>120s)", 120.0
    except Exception as e:
        return False, f"Exception: {str(e)[:80]}", 0.0

def main():
    """Main test runner with comprehensive verification."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("COMPREHENSIVE TEST & VERIFICATION - BAB 3: PEMROSESAN CITRA")
    print("=" * 80)
    print(f"Timestamp: {timestamp}")
    print(f"Directory: {DIR_SCRIPT}")
    print(f"Total Programs: {len(PROGRAMS)}\n")
    
    # Pastikan folder output ada
    os.makedirs(DIR_OUTPUT, exist_ok=True)
    
    results = []
    total_time = 0.0
    
    for prog in PROGRAMS:
        num = prog["num"]
        prog_file = prog["file"]
        prog_name = prog["name"]
        
        print(f"\n[{num:2d}/{len(PROGRAMS)}] {prog_name:35} ", end="", flush=True)
        
        # Run program
        success, message, exec_time = run_program(prog_file)
        total_time += exec_time
        
        # Check output
        has_output, num_files, files = check_output_exists(num)
        
        if success:
            status = "✅ PASS"
            if has_output:
                status += f" ({num_files} files)"
        else:
            status = f"❌ FAIL: {message}"
        
        print(f"{status} [{exec_time:.1f}s]")
        
        results.append({
            "num": num,
            "name": prog_name,
            "concept": prog["concept"],
            "success": success,
            "message": message,
            "time": exec_time,
            "has_output": has_output,
            "num_files": num_files
        })
    
    # Summary
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed
    total_files = sum(r["num_files"] for r in results)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Programs : {len(PROGRAMS)}")
    print(f"Passed         : {passed} ✅")
    print(f"Failed         : {failed} ❌")
    print(f"Total Files    : {total_files}")
    print(f"Total Time     : {total_time:.1f}s")
    print("=" * 80)
    
    # Write report to file
    report_path = os.path.join(DIR_SCRIPT, "VERIFICATION_REPORT.txt")
    with open(report_path, "w") as f:
        f.write(f"VERIFICATION REPORT - BAB 3: PEMROSESAN CITRA\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        
        for r in results:
            status = "PASS" if r["success"] else "FAIL"
            f.write(f"[{r['num']:02d}] {r['name']}\n")
            f.write(f"     Status: {status}\n")
            f.write(f"     Concept: {r['concept']}\n")
            f.write(f"     Time: {r['time']:.2f}s\n")
            f.write(f"     Output files: {r['num_files']}\n")
            if not r["success"]:
                f.write(f"     Error: {r['message']}\n")
            f.write("\n")
        
        f.write("=" * 60 + "\n")
        f.write(f"SUMMARY: {passed}/{len(PROGRAMS)} programs passed\n")
        f.write(f"Total execution time: {total_time:.1f}s\n")
    
    print(f"\n📄 Report saved to: {report_path}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
