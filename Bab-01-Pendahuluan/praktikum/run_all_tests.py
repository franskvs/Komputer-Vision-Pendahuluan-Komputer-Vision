#!/usr/bin/env python3
# ============================================================
# COMPREHENSIVE TEST & VERIFICATION - BAB 1 PENDAHULUAN
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
    {"num": 1, "file": "01_loading_gambar.py", "name": "Loading Gambar", "concept": "cv2.imread()"},
    {"num": 2, "file": "02_menampilkan_gambar.py", "name": "Menampilkan Gambar", "concept": "cv2.imshow(), matplotlib"},
    {"num": 3, "file": "03_properti_gambar.py", "name": "Properti Gambar", "concept": "Shape, dtype, channels"},
    {"num": 4, "file": "04_konversi_warna.py", "name": "Konversi Warna", "concept": "cv2.cvtColor()"},
    {"num": 5, "file": "05_manipulasi_piksel.py", "name": "Manipulasi Piksel", "concept": "Indexing, slicing"},
    {"num": 6, "file": "06_menggambar_shapes.py", "name": "Menggambar Shapes", "concept": "Drawing functions"},
    {"num": 7, "file": "07_menyimpan_output.py", "name": "Menyimpan Output", "concept": "cv2.imwrite()"},
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
    print("COMPREHENSIVE TEST & VERIFICATION - BAB 1: PENDAHULUAN")
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
        f.write(f"VERIFICATION REPORT - BAB 1: PENDAHULUAN\n")
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
