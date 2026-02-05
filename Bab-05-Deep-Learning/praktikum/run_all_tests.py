#!/usr/bin/env python3
# ============================================================
# COMPREHENSIVE TEST & VERIFICATION - BAB 5 DEEP LEARNING
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
    {"num": 1, "file": "01_opencv_dnn_classification.py", "name": "OpenCV DNN Classification", "concept": "DNN module inference"},
    {"num": 2, "file": "02_model_comparison.py", "name": "Model Comparison", "concept": "Multi-model benchmark"},
    {"num": 3, "file": "03_cnn_pytorch.py", "name": "CNN PyTorch", "concept": "PyTorch CNN training"},
    {"num": 4, "file": "04_cnn_keras.py", "name": "CNN Keras", "concept": "Keras/TensorFlow CNN"},
    {"num": 5, "file": "05_transfer_learning.py", "name": "Transfer Learning", "concept": "Pre-trained fine-tuning"},
    {"num": 6, "file": "06_data_augmentation.py", "name": "Data Augmentation", "concept": "Image augmentation"},
    {"num": 7, "file": "07_yolo_detection.py", "name": "YOLO Detection", "concept": "YOLOv8 inference"},
    {"num": 8, "file": "08_yolo_realtime.py", "name": "YOLO Realtime", "concept": "Realtime detection"},
    {"num": 9, "file": "09_semantic_segmentation.py", "name": "Semantic Segmentation", "concept": "Pixel classification"},
    {"num": 10, "file": "10_instance_segmentation.py", "name": "Instance Segmentation", "concept": "Object instances"},
    {"num": 11, "file": "11_onnx_export.py", "name": "ONNX Export", "concept": "Model conversion"},
    {"num": 12, "file": "12_opencv_deployment.py", "name": "OpenCV Deployment", "concept": "Production inference"},
]

def check_output_exists(program_num):
    """Check if output directory exists and has files."""
    output_dir = os.path.join(DIR_OUTPUT, f"output{program_num}")
    if not os.path.exists(output_dir):
        return False, 0, []
    
    files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.onnx', '.pt', '.pth'))]
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
            timeout=300,  # Timeout lebih lama untuk deep learning
            cwd=DIR_SCRIPT
        )
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            return True, "SUCCESS", elapsed_time
        else:
            error_msg = result.stderr[:150] if result.stderr else "Unknown error"
            return False, f"Error: {error_msg}", elapsed_time
    
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (>300s)", 300.0
    except Exception as e:
        return False, f"Exception: {str(e)[:80]}", 0.0

def main():
    """Main test runner with comprehensive verification."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 80)
    print("COMPREHENSIVE TEST & VERIFICATION - BAB 5: DEEP LEARNING")
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
        f.write(f"VERIFICATION REPORT - BAB 5: DEEP LEARNING\n")
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
