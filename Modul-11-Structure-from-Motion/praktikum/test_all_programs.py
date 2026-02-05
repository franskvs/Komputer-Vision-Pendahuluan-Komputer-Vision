#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk testing semua program Bab 11 secara otomatis
Memastikan semua program berjalan dan menghasilkan output
"""

import subprocess
import sys
from pathlib import Path
import time

# Daftar program yang akan ditest
PROGRAMS = [
    "01_feature_matching_multiview.py",
    "02_fundamental_matrix.py",
    "03_essential_matrix.py",
    "04_triangulasi_3d.py",
    "05_visual_odometry.py",
    "06_bundle_adjustment.py",
    "07_simple_slam.py",
    "08_vanishing_points_calibration.py",
    "09_pnp_pose_estimation.py",
    "10_radial_distortion_plumbline.py",
    "11_tomasi_kanade_factorization.py",
]

def run_program(program_name, timeout=30):
    """
    Menjalankan satu program dengan timeout
    
    Returns:
        (success, output, error)
    """
    print(f"\n{'='*70}")
    print(f"Testing: {program_name}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, program_name],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent
        )
        
        success = result.returncode == 0
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"⚠ TIMEOUT: Program melebihi {timeout} detik")
        return False, "", "Timeout"
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False, "", str(e)

def main():
    """Testing semua program"""
    print("="*70)
    print("AUTOMATED TESTING - BAB 11: STRUCTURE FROM MOTION")
    print("="*70)
    print(f"Total programs to test: {len(PROGRAMS)}")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    for i, program in enumerate(PROGRAMS, 1):
        print(f"\n[{i}/{len(PROGRAMS)}] Testing {program}...")
        
        success, stdout, stderr = run_program(program, timeout=30)
        
        results.append({
            'program': program,
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        })
        
        if success:
            print(f"✓ SUCCESS")
            # Print last 10 lines of output
            lines = stdout.split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"  {line}")
        else:
            print(f"✗ FAILED")
            if stderr:
                print(f"  Error: {stderr[:200]}")
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results if r['success'])
    failed = len(results) - passed
    
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {passed/len(results)*100:.1f}%")
    
    print("\nDetailed Results:")
    for r in results:
        status = "✓" if r['success'] else "✗"
        print(f"  {status} {r['program']}")
    
    # Save report
    report_path = Path(__file__).parent / "output" / "test_report.txt"
    with open(report_path, 'w') as f:
        f.write("="*70 + "\n")
        f.write("TEST REPORT - BAB 11: STRUCTURE FROM MOTION\n")
        f.write("="*70 + "\n\n")
        f.write(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Programs: {len(results)}\n")
        f.write(f"Passed: {passed}\n")
        f.write(f"Failed: {failed}\n\n")
        
        for r in results:
            f.write(f"\n{'='*70}\n")
            f.write(f"Program: {r['program']}\n")
            f.write(f"Status: {'PASSED' if r['success'] else 'FAILED'}\n")
            f.write(f"{'='*70}\n")
            if r['stdout']:
                f.write("STDOUT:\n")
                f.write(r['stdout'][-1000:])  # Last 1000 chars
                f.write("\n")
            if r['stderr']:
                f.write("STDERR:\n")
                f.write(r['stderr'][:500])
                f.write("\n")
    
    print(f"\nTest report saved to: {report_path}")
    print(f"\nFinished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
