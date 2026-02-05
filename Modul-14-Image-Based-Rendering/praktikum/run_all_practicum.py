#!/usr/bin/env python3
"""
Master Test Script untuk Bab 14 - Image-Based Rendering
========================================================

Script ini memverifikasi semua 7 program praktikum:
1. Image Warping & Homography
2. Panorama Stitching
3. Cylindrical & Spherical Projection  
4. View Interpolation
5. Multiplane Images
6. Quality Metrics
7. NeRF Concepts

Features:
- Run dengan timeout untuk safety
- Collect output statistics
- Verify output files exist
- Generate comprehensive report

Run:
    python3 run_all_practicum.py
"""

import subprocess
import sys
from pathlib import Path
import time
import json

# ============================================================
# CONFIGURATION
# ============================================================

PRAKTIKUM_DIR = Path(__file__).parent
OUTPUT_DIR = PRAKTIKUM_DIR / "output"

PROGRAMS = [
    ("01_image_warping.py", 30),
    ("02_panorama_stitching.py", 60),
    ("03_cylindrical_projection.py", 45),
    ("04_view_interpolation.py", 45),
    ("05_multiplane_images.py", 60),
    ("06_quality_metrics.py", 30),
    ("07_nerf_concepts.py", 45),
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def run_program(program_name, timeout_sec):
    """
    Run single program dengan timeout.
    
    Args:
        program_name: Nama file Python
        timeout_sec: Timeout dalam seconds
    
    Returns:
        (success, elapsed_time, error_message)
    """
    program_path = PRAKTIKUM_DIR / program_name
    
    if not program_path.exists():
        return False, 0, f"File not found: {program_path}"
    
    try:
        start_time = time.time()
        
        result = subprocess.run(
            [sys.executable, str(program_path)],
            cwd=PRAKTIKUM_DIR,
            capture_output=True,
            timeout=timeout_sec,
            text=True
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            return True, elapsed, None
        else:
            return False, elapsed, result.stderr[-500:]  # Last 500 chars
    
    except subprocess.TimeoutExpired:
        return False, timeout_sec, f"Timeout after {timeout_sec}s"
    except Exception as e:
        return False, 0, str(e)

def count_output_files(output_num):
    """
    Count output files untuk setiap praktikum.
    
    Args:
        output_num: Nomor praktikum (1-7)
    
    Returns:
        (file_count, total_size_mb)
    """
    output_subdir = OUTPUT_DIR / f"output{output_num}"
    
    if not output_subdir.exists():
        return 0, 0
    
    files = list(output_subdir.glob("*"))
    file_count = len(files)
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    
    return file_count, total_size_mb

def generate_report(results):
    """
    Generate comprehensive report.
    
    Args:
        results: List of (program, success, elapsed, error) tuples
    """
    print("\n" + "="*70)
    print("BAPTER 14: IMAGE-BASED RENDERING - TEST REPORT")
    print("="*70)
    
    print("\n" + "-"*70)
    print(f"{'Program':<35} {'Status':<10} {'Time (s)':<10} {'Files':<10}")
    print("-"*70)
    
    total_success = 0
    total_files = 0
    total_size = 0
    
    for i, (program_name, success, elapsed, error, files, size) in enumerate(results, 1):
        status = "✓ PASS" if success else "✗ FAIL"
        
        print(f"{program_name:<35} {status:<10} {elapsed:<10.2f} {files:<10}")
        
        if success:
            total_success += 1
        total_files += files
        total_size += size
    
    print("-"*70)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    print(f"Programs Executed: {len(results)}")
    print(f"Programs Passed: {total_success}/{len(results)}")
    print(f"Success Rate: {100*total_success/len(results):.1f}%")
    print(f"Total Output Files: {total_files}")
    print(f"Total Output Size: {total_size:.2f} MB")
    
    if total_success == len(results):
        print("\n✓ ALL PRACTICUM PASSED!")
    else:
        print("\n⚠ Some practicum failed - see details above")
    
    print("="*70)

# ============================================================
# MAIN
# ============================================================

def main():
    """Main execution."""
    print("="*70)
    print("STARTING BAB 14 - IMAGE-BASED RENDERING TEST SUITE")
    print("="*70)
    
    results = []
    
    for program_name, timeout in PROGRAMS:
        output_num = int(program_name.split('_')[0])
        
        print(f"\n[{output_num}/7] Testing {program_name}...", end=" ", flush=True)
        
        success, elapsed, error = run_program(program_name, timeout)
        
        # Count output files
        files, size = count_output_files(output_num)
        
        if success:
            print(f"✓ ({elapsed:.2f}s, {files} files, {size:.2f}MB)")
        else:
            print(f"✗ FAILED")
            if error:
                print(f"  Error: {error[:100]}")
        
        results.append((program_name, success, elapsed, error, files, size))
    
    # Generate report
    generate_report(results)
    
    # Return exit code
    return 0 if all(r[1] for r in results) else 1

if __name__ == "__main__":
    sys.exit(main())
