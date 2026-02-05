#!/usr/bin/env python3
# ============================================================
# AUTOMATED TEST RUNNER - BAB 2 PEMBENTUKAN CITRA
# ============================================================
# Menjalankan semua program secara otomatis dan verifikasi output
# ============================================================

import os
import sys
import subprocess
import time
from pathlib import Path

# Setup paths
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIR_SCRIPT, "output")

# Daftar semua program
PROGRAMS = [
    {"file": "01_translasi.py", "name": "Translasi", "interactive": False},
    {"file": "02_rotasi.py", "name": "Rotasi", "interactive": False},
    {"file": "03_scaling.py", "name": "Scaling", "interactive": False},
    {"file": "04_affine_transform.py", "name": "Affine Transform", "interactive": False},
    {"file": "05_perspektif_transform.py", "name": "Perspektif Transform", "interactive": True},
    {"file": "06_document_scanner.py", "name": "Document Scanner", "interactive": True},
    {"file": "07_kalibrasi_kamera.py", "name": "Kalibrasi Kamera", "interactive": False},
    {"file": "08_3d_rotation.py", "name": "3D Rotation", "interactive": False},
    {"file": "09_projection_perspective.py", "name": "Projection", "interactive": False},
    {"file": "10_lens_distortion.py", "name": "Lens Distortion", "interactive": False},
    {"file": "11_sampling_aliasing.py", "name": "Sampling & Aliasing", "interactive": False},
    {"file": "12_color_spaces.py", "name": "Color Spaces", "interactive": False},
    {"file": "13_gamma_correction.py", "name": "Gamma Correction", "interactive": False},
    {"file": "14_photometric_shading.py", "name": "Photometric Shading", "interactive": False},
    {"file": "15_compression_artifacts.py", "name": "Compression Artifacts", "interactive": False},
]

def check_output_exists(program_num):
    """Check if output directory exists and has files."""
    output_dir = os.path.join(DIR_OUTPUT, f"output{program_num}")
    if not os.path.exists(output_dir):
        return False, 0
    
    files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return len(files) > 0, len(files)

def run_program(program_file, interactive=False):
    """Run a single program."""
    program_path = os.path.join(DIR_SCRIPT, program_file)
    
    if not os.path.exists(program_path):
        return False, f"File tidak ditemukan: {program_file}"
    
    try:
        if interactive:
            # For interactive programs, skip them for now
            # They need to be modified to accept automated input
            return True, "SKIPPED (Interactive - requires manual modification)"
        else:
            # Run non-interactive programs
            result = subprocess.run(
                [sys.executable, program_path],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=DIR_SCRIPT
            )
            
            if result.returncode == 0:
                return True, "SUCCESS"
            else:
                error_msg = result.stderr[:200] if result.stderr else "Unknown error"
                return False, f"Error: {error_msg}"
    
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (>30s)"
    except Exception as e:
        return False, f"Exception: {str(e)[:100]}"

def main():
    """Main test runner."""
    print("=" * 80)
    print("AUTOMATED TEST RUNNER - BAB 2: PEMBENTUKAN CITRA")
    print("=" * 80)
    print(f"\nDirectory: {DIR_SCRIPT}")
    print(f"Total Programs: {len(PROGRAMS)}\n")
    
    results = []
    
    for idx, prog in enumerate(PROGRAMS, 1):
        prog_file = prog["file"]
        prog_name = prog["name"]
        
        print(f"\n[{idx:2d}/15] Testing: {prog_name:30} ", end="", flush=True)
        
        # Run program
        success, message = run_program(prog_file, prog["interactive"])
        
        # Check output
        has_output, num_files = check_output_exists(idx)
        
        # Store result
        results.append({
            "num": idx,
            "file": prog_file,
            "name": prog_name,
            "success": success,
            "message": message,
            "has_output": has_output,
            "num_files": num_files,
            "interactive": prog["interactive"]
        })
        
        # Print status
        if success:
            status = "✓ PASS"
            if prog["interactive"]:
                status = "⚠ SKIP"
        else:
            status = "✗ FAIL"
        
        output_status = f"Output: {num_files} files" if has_output else "No output"
        print(f"[{status}] {output_status}")
        
        if not success and not prog["interactive"]:
            print(f"     Error: {message[:100]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r["success"] and not r["interactive"])
    failed = sum(1 for r in results if not r["success"] and not r["interactive"])
    skipped = sum(1 for r in results if r["interactive"])
    total_non_interactive = len(PROGRAMS) - skipped
    
    print(f"\nNon-Interactive Programs:")
    print(f"  ✓ Passed: {passed}/{total_non_interactive}")
    print(f"  ✗ Failed: {failed}/{total_non_interactive}")
    print(f"\nInteractive Programs:")
    print(f"  ⚠ Skipped: {skipped} (requires modification)")
    
    # Detailed output check
    print("\n" + "=" * 80)
    print("OUTPUT VERIFICATION")
    print("=" * 80)
    
    for r in results:
        status = "✓" if r["has_output"] else "✗"
        print(f"{status} {r['num']:2d}. {r['name']:30} → {r['num_files']} output files")
    
    # Failed programs
    if failed > 0:
        print("\n" + "=" * 80)
        print("FAILED PROGRAMS DETAILS")
        print("=" * 80)
        
        for r in results:
            if not r["success"] and not r["interactive"]:
                print(f"\n✗ {r['file']}:")
                print(f"   {r['message']}")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print("""
1. Programs 05 & 06 (Interactive):
   - Need to be modified to accept command-line coordinates
   - Or create non-interactive demo versions
   - Current: Require manual mouse clicking

2. All other programs:
   - Should run automatically and save output
   - Use matplotlib Agg backend (no window display)
   
3. Next Steps:
   - Fix any failed programs
   - Modify interactive programs for automation
   - Verify all output files are generated correctly
    """)

if __name__ == "__main__":
    main()
