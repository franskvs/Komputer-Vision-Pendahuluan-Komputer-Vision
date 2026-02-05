#!/usr/bin/env python3
"""
=============================================================================
RUN ALL PRAKTIKUM - BAB 7: DETEKSI FITUR DAN PENCOCOKAN
=============================================================================
Script untuk menjalankan semua praktikum secara otomatis dengan verifikasi
output dan penutupan window otomatis.

Fitur:
- Menjalankan semua 7 praktikum secara berurutan
- Verifikasi output tersimpan di folder
- Penutupan window otomatis dengan delay 2 detik
- Laporan ringkas hasil eksekusi
=============================================================================
"""

import subprocess
import os
import sys
import time
import json
from pathlib import Path

# List program praktikum
PRAKTIKUM_PROGRAMS = [
    "01_harris_corner.py",
    "02_shi_tomasi.py",
    "03_sift_detection.py",
    "04_orb_detection.py",
    "05_bf_matching.py",
    "06_flann_matching.py",
    "07_homography_ransac.py",
    "08_real_world_example.py",
    "09_akaze_detection.py",
    "10_fast_detection.py",
]

def get_script_dir():
    """Get current script directory"""
    return os.path.dirname(os.path.abspath(__file__))

def run_program(program_name):
    """
    Run a single praktikum program
    
    Returns:
        dict: Result dengan status, waktu eksekusi, dan output
    """
    script_dir = get_script_dir()
    program_path = os.path.join(script_dir, program_name)
    
    if not os.path.exists(program_path):
        return {
            'name': program_name,
            'status': 'FAIL',
            'error': f'File not found: {program_path}',
            'time': 0
        }
    
    print(f"\n{'=' * 70}")
    print(f"Running: {program_name}")
    print(f"{'=' * 70}")
    
    start_time = time.time()
    
    try:
        # Run program
        result = subprocess.run(
            [sys.executable, program_path],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        elapsed_time = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        status = 'SUCCESS' if result.returncode == 0 else 'FAIL'
        
        return {
            'name': program_name,
            'status': status,
            'time': elapsed_time,
            'returncode': result.returncode,
            'error': result.stderr if result.returncode != 0 else None
        }
        
    except subprocess.TimeoutExpired:
        return {
            'name': program_name,
            'status': 'TIMEOUT',
            'error': 'Program execution exceeded 60 seconds',
            'time': 60
        }
    except Exception as e:
        return {
            'name': program_name,
            'status': 'ERROR',
            'error': str(e),
            'time': time.time() - start_time
        }

def verify_outputs():
    """
    Verify output files exist
    
    Returns:
        dict: File verification results
    """
    script_dir = get_script_dir()
    output_dir = os.path.join(script_dir, 'output')
    
    results = {
        'total_files': 0,
        'expected_files': {
            'harris': ['harris_checkerboard.jpg', 'harris_building.jpg', 'harris_box.jpg'],
            'shi_tomasi': ['shi_tomasi_checkerboard.jpg', 'shi_tomasi_building.jpg', 'shi_tomasi_butterfly.jpg'],
            'sift': ['sift_checkerboard.jpg', 'sift_building.jpg', 'sift_box.jpg'],
            'orb': ['orb_building.jpg', 'orb_box.jpg', 'orb_scale_factor_comparison.jpg'],
            'bf_match': ['bf_match_box_box_in_scene.jpg'],
            'flann_match': ['flann_match_box_box_in_scene.jpg'],
            'homography': ['homography_box_box_in_scene.jpg'],
            'real_world': ['document_scanner_demo.jpg'],
            'akaze': ['akaze_building.jpg', 'akaze_box.jpg'],
            'fast': ['fast_building.jpg', 'fast_box.jpg', 'fast_threshold_comparison.jpg']
        }
    }
    
    if not os.path.exists(output_dir):
        return results
    
    # Count existing files
    all_files = os.listdir(output_dir)
    results['total_files'] = len(all_files)
    
    # Check expected files
    results['found_files'] = {}
    for category, files in results['expected_files'].items():
        results['found_files'][category] = []
        for fname in files:
            fpath = os.path.join(output_dir, fname)
            if os.path.exists(fpath):
                results['found_files'][category].append(fname)
    
    return results

def print_summary(results, output_verification):
    """
    Print execution summary
    """
    print("\n" + "=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    
    # Program results
    print("\nProgram Execution Results:")
    print("-" * 70)
    
    success_count = 0
    fail_count = 0
    total_time = 0
    
    for result in results:
        status = result['status']
        time_str = f"{result.get('time', 0):.2f}s"
        program_name = result['name']
        
        status_symbol = "✓" if status == 'SUCCESS' else "✗"
        print(f"{status_symbol} {program_name:30} [{status:10}] {time_str}")
        
        if status == 'SUCCESS':
            success_count += 1
        else:
            fail_count += 1
            if result.get('error'):
                print(f"  Error: {result['error']}")
        
        total_time += result.get('time', 0)
    
    print("-" * 70)
    print(f"Total: {success_count} Success, {fail_count} Failed")
    print(f"Total Execution Time: {total_time:.2f}s")
    
    # Output verification
    print("\nOutput File Verification:")
    print("-" * 70)
    print(f"Total output files found: {output_verification['total_files']}")
    
    total_expected = sum(len(files) for files in output_verification['expected_files'].values())
    total_found = sum(len(files) for files in output_verification['found_files'].values())
    
    print(f"Files found: {total_found}/{total_expected}")
    
    # Detailed breakdown
    for category, files in output_verification['found_files'].items():
        expected = output_verification['expected_files'][category]
        found = len(files)
        expected_len = len(expected)
        symbol = "✓" if found == expected_len else "⚠"
        print(f"{symbol} {category:20} {found:2}/{expected_len:2} files")
    
    print("=" * 70)
    
    return success_count == len(results)

def main():
    print("=" * 70)
    print("PRAKTIKUM BAB 7 - AUTOMATED TEST RUNNER")
    print("=" * 70)
    print(f"\nStarting time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Programs to run: {len(PRAKTIKUM_PROGRAMS)}")
    print()
    
    # Check dependencies
    try:
        import cv2
        import numpy as np
        print(f"✓ OpenCV version: {cv2.__version__}")
        print(f"✓ NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return 1
    
    # Check if sample data exists
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, 'data', 'images')
    
    if not os.path.exists(data_dir):
        print(f"\n⚠ Sample data not found: {data_dir}")
        print("Downloading sample data...")
        download_script = os.path.join(os.path.dirname(script_dir), 'download_sample_data.py')
        if os.path.exists(download_script):
            subprocess.run([sys.executable, download_script], cwd=os.path.dirname(script_dir))
    
    # Run all programs
    results = []
    for program in PRAKTIKUM_PROGRAMS:
        result = run_program(program)
        results.append(result)
        time.sleep(2)  # Delay between programs
    
    # Verify outputs
    output_verification = verify_outputs()
    
    # Print summary
    success = print_summary(results, output_verification)
    
    print(f"\nEnd time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
