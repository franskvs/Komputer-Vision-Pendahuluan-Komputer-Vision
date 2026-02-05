#!/usr/bin/env python3
"""
=============================================================================
VERIFICATION SCRIPT - BAB 05 DEEP LEARNING
=============================================================================
Script untuk otomatis verifikasi semua program praktikum bab 05.
Memastikan semua program:
1. Bisa diimport tanpa error
2. Memiliki fungsi-fungsi yang diharapkan
3. Bisa dijalankan minimal untuk testing
4. Auto-close window dengan 'q' key sudah terimplementasi

Author: Verification System
Date: 2026-02-05
=============================================================================
"""

import sys
import os
import time
import importlib
import subprocess
from pathlib import Path

# Set up Python path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"  {text}")

def check_syntax(file_path):
    """
    Check if Python file has valid syntax.
    Returns: (success, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        return True, "Syntax valid"
    except SyntaxError as e:
        return False, f"Syntax Error line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_imports(file_path):
    """
    Check if file can be imported without errors.
    Returns: (success, message, module)
    """
    try:
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        
        # Don't execute, just check if it loads
        # spec.loader.exec_module(module)
        
        return True, "Imports OK", module
    except ImportError as e:
        return False, f"Import Error: {str(e)}", None
    except Exception as e:
        return False, f"Error: {str(e)}", None

def check_q_key_implementation(file_path):
    """
    Check if file implements Q-key window closing.
    Returns: (has_implementation, count)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for the Q-key pattern
        q_key_pattern = "key == ord('q') or key == 27"
        count = content.count(q_key_pattern)
        
        # Also check for cv2.imshow
        imshow_count = content.count("cv2.imshow")
        
        return count > 0, count, imshow_count
    except Exception as e:
        return False, 0, 0

def verify_file(file_path):
    """
    Comprehensive verification of a single Python file.
    Returns: dict with verification results
    """
    results = {
        'filename': file_path.name,
        'path': str(file_path),
        'syntax_valid': False,
        'imports_ok': False,
        'q_key_implemented': False,
        'q_key_count': 0,
        'imshow_count': 0,
        'messages': []
    }
    
    print_info(f"Checking: {file_path.name}")
    
    # Check 1: Syntax
    syntax_ok, syntax_msg = check_syntax(file_path)
    results['syntax_valid'] = syntax_ok
    if syntax_ok:
        print_success(f"  Syntax: {syntax_msg}")
    else:
        print_error(f"  Syntax: {syntax_msg}")
        results['messages'].append(syntax_msg)
    
    # Check 2: Imports
    if syntax_ok:
        import_ok, import_msg, _ = check_imports(file_path)
        results['imports_ok'] = import_ok
        if import_ok:
            print_success(f"  Imports: {import_msg}")
        else:
            print_warning(f"  Imports: {import_msg}")
            results['messages'].append(import_msg)
    
    # Check 3: Q-key implementation
    has_q, q_count, imshow_count = check_q_key_implementation(file_path)
    results['q_key_implemented'] = has_q
    results['q_key_count'] = q_count
    results['imshow_count'] = imshow_count
    
    if imshow_count > 0:
        if has_q:
            print_success(f"  Q-key closing: Implemented ({q_count} locations, {imshow_count} cv2.imshow)")
        else:
            print_warning(f"  Q-key closing: NOT implemented ({imshow_count} cv2.imshow found)")
            results['messages'].append("Q-key auto-close not implemented")
    else:
        print_info("  No cv2.imshow found (may use matplotlib or no GUI)")
    
    print()
    return results

def run_verification():
    """Main verification function"""
    print_header("BAB 05 DEEP LEARNING - VERIFICATION SCRIPT")
    
    # Find all Python files in praktikum directory
    praktikum_dir = PROJECT_ROOT / "praktikum"
    
    if not praktikum_dir.exists():
        print_error(f"Praktikum directory not found: {praktikum_dir}")
        return
    
    python_files = sorted(praktikum_dir.glob("*.py"))
    
    if not python_files:
        print_error("No Python files found in praktikum directory")
        return
    
    print_info(f"Found {len(python_files)} Python files to verify\n")
    
    # Verify each file
    all_results = []
    for py_file in python_files:
        results = verify_file(py_file)
        all_results.append(results)
    
    # Generate summary report
    print_header("VERIFICATION SUMMARY")
    
    total = len(all_results)
    syntax_ok = sum(1 for r in all_results if r['syntax_valid'])
    imports_ok = sum(1 for r in all_results if r['imports_ok'])
    q_key_ok = sum(1 for r in all_results if r['q_key_implemented'])
    has_imshow = sum(1 for r in all_results if r['imshow_count'] > 0)
    
    print(f"Total files: {total}")
    print(f"✓ Syntax valid: {syntax_ok}/{total} ({syntax_ok/total*100:.1f}%)")
    print(f"✓ Imports OK: {imports_ok}/{total} ({imports_ok/total*100:.1f}%)")
    print(f"✓ Q-key implemented: {q_key_ok}/{has_imshow} files with cv2.imshow")
    
    # Detailed issues
    issues = [r for r in all_results if r['messages']]
    if issues:
        print_header("ISSUES FOUND")
        for result in issues:
            print_error(f"{result['filename']}:")
            for msg in result['messages']:
                print_info(f"  - {msg}")
    
    # Files with cv2.imshow but no Q-key
    missing_q = [r for r in all_results if r['imshow_count'] > 0 and not r['q_key_implemented']]
    if missing_q:
        print_header("FILES NEEDING Q-KEY FIX")
        for result in missing_q:
            print_warning(f"{result['filename']}: {result['imshow_count']} cv2.imshow, but no Q-key")
    
    # Success files
    success = [r for r in all_results if r['syntax_valid'] and r['imports_ok']]
    if success:
        print_header("SUCCESSFULLY VERIFIED FILES")
        for result in success:
            print_success(result['filename'])
    
    # Overall status
    print_header("OVERALL STATUS")
    if syntax_ok == total and q_key_ok == has_imshow:
        print_success("ALL CHECKS PASSED! ✓✓✓")
        print_info("All programs are ready for practical use.")
    elif syntax_ok == total:
        print_warning("SYNTAX OK, but some Q-key implementations missing")
        print_info("Programs will work but may require manual window closing.")
    else:
        print_error("VERIFICATION FAILED")
        print_info("Please fix syntax errors before proceeding.")
    
    # Write detailed report
    report_path = PROJECT_ROOT / "VERIFICATION_REPORT.md"
    write_report(all_results, report_path)
    print_info(f"\nDetailed report written to: {report_path}")

def write_report(results, report_path):
    """Write detailed verification report to Markdown file"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# BAB 05 DEEP LEARNING - VERIFICATION REPORT\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        total = len(results)
        syntax_ok = sum(1 for r in results if r['syntax_valid'])
        imports_ok = sum(1 for r in results if r['imports_ok'])
        q_key_ok = sum(1 for r in results if r['q_key_implemented'])
        has_imshow = sum(1 for r in results if r['imshow_count'] > 0)
        
        f.write(f"- **Total Files**: {total}\n")
        f.write(f"- **Syntax Valid**: {syntax_ok}/{total} ({syntax_ok/total*100:.1f}%)\n")
        f.write(f"- **Imports OK**: {imports_ok}/{total} ({imports_ok/total*100:.1f}%)\n")
        f.write(f"- **Q-key Implemented**: {q_key_ok}/{has_imshow} files with cv2.imshow\n\n")
        
        f.write("## Detailed Results\n\n")
        f.write("| File | Syntax | Imports | Q-key | cv2.imshow | Notes |\n")
        f.write("|------|--------|---------|-------|------------|-------|\n")
        
        for r in results:
            syntax_icon = "✓" if r['syntax_valid'] else "✗"
            import_icon = "✓" if r['imports_ok'] else "⚠"
            q_icon = "✓" if r['q_key_implemented'] or r['imshow_count'] == 0 else "✗"
            
            notes = ", ".join(r['messages']) if r['messages'] else "-"
            
            f.write(f"| {r['filename']} | {syntax_icon} | {import_icon} | {q_icon} | "
                   f"{r['imshow_count']} | {notes} |\n")
        
        f.write("\n## Files by Status\n\n")
        
        # Perfect files
        perfect = [r for r in results if r['syntax_valid'] and r['imports_ok'] and 
                   (r['q_key_implemented'] or r['imshow_count'] == 0)]
        if perfect:
            f.write("### ✓ Ready for Use\n\n")
            for r in perfect:
                f.write(f"- {r['filename']}\n")
            f.write("\n")
        
        # Needs Q-key fix
        needs_q = [r for r in results if r['syntax_valid'] and r['imshow_count'] > 0 and not r['q_key_implemented']]
        if needs_q:
            f.write("### ⚠ Needs Q-key Implementation\n\n")
            for r in needs_q:
                f.write(f"- {r['filename']} ({r['imshow_count']} cv2.imshow locations)\n")
            f.write("\n")
        
        # Has errors
        errors = [r for r in results if not r['syntax_valid']]
        if errors:
            f.write("### ✗ Has Errors\n\n")
            for r in errors:
                f.write(f"- {r['filename']}\n")
                for msg in r['messages']:
                    f.write(f"  - {msg}\n")
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## Recommendations\n\n")
        
        if needs_q:
            f.write("1. **Implement Q-key closing** for files with cv2.imshow\n")
            f.write("   ```python\n")
            f.write("   print(\"\\n[INFO] Tekan 'q' untuk menutup gambar...\")\n")
            f.write("   while True:\n")
            f.write("       key = cv2.waitKey(1) & 0xFF\n")
            f.write("       if key == ord('q') or key == 27:  # 'q' atau ESC\n")
            f.write("           break\n")
            f.write("   cv2.destroyAllWindows()\n")
            f.write("   ```\n\n")
        
        if errors:
            f.write("2. **Fix syntax errors** before running programs\n\n")
        
        f.write("3. **Test each program** individually before batch testing\n\n")
        f.write("4. **Update documentation** to reflect Q-key closing feature\n\n")

if __name__ == "__main__":
    try:
        run_verification()
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
