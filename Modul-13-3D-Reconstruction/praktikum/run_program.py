#!/usr/bin/env python3
"""
Auto-close wrapper for interactive programs
Runs programs with input simulating non-interactive mode
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_program_non_interactive(program_path, timeout=60):
    """Run a program non-interactively (answer 'n' to interactive prompts)."""
    
    try:
        # Send 'n' + Enter when program asks for input
        result = subprocess.run(
            [sys.executable, str(program_path)],
            input="n\n",  # Answer 'n' to visualization prompt
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(program_path.parent)
        )
        
        return result.returncode == 0, result.stdout + result.stderr, time.time() - time.time()
    
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT (>{timeout}s)", timeout
    except Exception as e:
        return False, str(e), 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_program.py <program.py> [timeout_seconds]")
        sys.exit(1)
    
    program_file = Path(sys.argv[1])
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    if not program_file.exists():
        print(f"Error: {program_file} not found")
        sys.exit(1)
    
    success, output, elapsed = run_program_non_interactive(program_file, timeout)
    
    print(output)
    sys.exit(0 if success else 1)
