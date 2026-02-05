#!/usr/bin/env python3
# ============================================================
# COMPREHENSIVE TEST & VERIFICATION - BAB 13: 3D RECONSTRUCTION
# ============================================================

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json

DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# List all programs with per-program timeouts
PROGRAMS = [
    {
        "num": 1, 
        "file": "01_point_cloud_basics.py", 
        "name": "Point Cloud Basics",
        "category": "Fundamentals",
        "timeout": 60
    },
    {
        "num": 2, 
        "file": "02_point_cloud_filtering.py", 
        "name": "Point Cloud Filtering",
        "category": "Preprocessing",
        "timeout": 60
    },
    {
        "num": 3, 
        "file": "03_normal_estimation.py", 
        "name": "Normal Estimation",
        "category": "Preprocessing",
        "timeout": 60
    },
    {
        "num": 4, 
        "file": "04_point_cloud_registration.py", 
        "name": "Point Cloud Registration",
        "category": "Registration",
        "timeout": 60
    },
    {
        "num": 5, 
        "file": "05_poisson_reconstruction.py", 
        "name": "Poisson Surface Reconstruction",
        "category": "Reconstruction",
        "timeout": 180  # Longer timeout for heavy computation
    },
    {
        "num": 6, 
        "file": "06_ball_pivoting.py", 
        "name": "Ball Pivoting Algorithm",
        "category": "Reconstruction",
        "timeout": 180  # Longer timeout for heavy computation
    },
    {
        "num": 7, 
        "file": "07_mesh_processing.py", 
        "name": "Mesh Processing",
        "category": "Post-processing",
        "timeout": 90
    },
]

def check_dependencies():
    """Check if required packages are installed."""
    required = ['open3d', 'numpy', 'matplotlib', 'scipy']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        return False
    return True

def check_output_exists(program_num):
    """Check if output directory has generated files."""
    output_dir = os.path.join(DIR_OUTPUT, f"output{program_num}")
    if not os.path.exists(output_dir):
        return False, 0, []
    
    files = []
    for ext in ['.ply', '.pcd', '.obj', '.stl', '.xyz', '.png', '.json']:
        files.extend([f for f in os.listdir(output_dir) if f.endswith(ext)])
    
    return len(files) > 0, len(files), files

def run_program(program_file, timeout=90):
    """Run program non-interactively with specified timeout."""
    program_path = os.path.join(DIR_SCRIPT, program_file)
    
    if not os.path.exists(program_path):
        return False, f"File tidak ditemukan", 0.0
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, program_path],
            input="n\n",  # Answer 'n' to visualization prompt
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=DIR_SCRIPT
        )
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            return True, "SUCCESS", elapsed_time
        else:
            error_msg = result.stderr[:150] if result.stderr else "Unknown error"
            return False, error_msg, elapsed_time
    
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT (>{timeout}s)", timeout
    except Exception as e:
        return False, f"Exception: {str(e)[:80]}", 0.0

def main():
    """Main test runner."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("COMPREHENSIVE TEST & VERIFICATION - BAB 13: 3D RECONSTRUCTION")
    print("=" * 80)
    print(f"Timestamp: {timestamp}")
    print(f"Total Programs: {len(PROGRAMS)}\n")
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("⚠️  Some dependencies missing\n")
    
    results = []
    total_time = 0.0
    passed = 0
    
    # Run each program
    for prog in PROGRAMS:
        num = prog["num"]
        prog_file = prog["file"]
        prog_name = prog["name"]
        category = prog.get("category", "Unknown")
        timeout = prog.get("timeout", 90)
        
        print(f"\n[{num:2d}/{len(PROGRAMS):2d}] {prog_name:35} ", end="", flush=True)
        
        success, message, exec_time = run_program(prog_file, timeout)
        total_time += exec_time
        
        has_output, num_files, files = check_output_exists(num)
        
        if success:
            passed += 1
            print(f"✓ PASS ({exec_time:.2f}s)")
        else:
            print(f"✗ FAIL - {message}")
        
        results.append({
            'num': num,
            'name': prog_name,
            'category': category,
            'success': success,
            'message': message,
            'time': exec_time,
            'output_files': num_files,
            'timeout_limit': timeout
        })
        
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total: {len(PROGRAMS)} | Passed: {passed} ✓ | Failed: {len(PROGRAMS) - passed} ✗")
    print(f"Total Time: {total_time:.2f}s")
    
    if len(PROGRAMS) > 0:
        pass_rate = (passed / len(PROGRAMS)) * 100
        print(f"Pass Rate: {pass_rate:.1f}%")
    
    # Save report
    report = {
        'timestamp': timestamp,
        'total': len(PROGRAMS),
        'passed': passed,
        'failed': len(PROGRAMS) - passed,
        'pass_rate': (passed / len(PROGRAMS) * 100) if PROGRAMS else 0,
        'total_time': total_time,
        'results': results
    }
    
    os.makedirs(DIR_OUTPUT, exist_ok=True)
    with open(os.path.join(DIR_OUTPUT, "test_report.json"), 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Report saved to output/test_report.json")
    print("=" * 80)
    
    return passed == len(PROGRAMS)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
