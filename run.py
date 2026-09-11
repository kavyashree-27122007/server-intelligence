"""
Application Runner for Support Intelligence.

Usage:
    python run.py --backend     # Starts FastAPI backend on http://localhost:8000
    python run.py --frontend    # Starts Vite frontend on http://localhost:5173
    python run.py               # Starts both concurrently
"""
import sys
import os
import argparse
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def run_backend():
    print("[INFO] Starting FastAPI Backend on http://localhost:8000 ...")
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=str(PROJECT_ROOT)
    )


def run_frontend():
    print("[INFO] Starting React/Vite Frontend on http://localhost:5173 ...")
    subprocess.run(
        ["npm", "run", "dev"],
        cwd=str(PROJECT_ROOT / "frontend"),
        shell=True
    )


def main():
    parser = argparse.ArgumentParser(description="Support Intelligence Runner")
    parser.add_argument("--backend", action="store_true", help="Run FastAPI backend")
    parser.add_argument("--frontend", action="store_true", help="Run React/Vite frontend")
    args = parser.parse_args()

    if args.backend:
        run_backend()
    elif args.frontend:
        run_frontend()
    else:
        print("Starting Support Intelligence (Backend + Frontend)...")
        b_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=str(PROJECT_ROOT)
        )
        time.sleep(2)
        f_proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=str(PROJECT_ROOT / "frontend"),
            shell=True
        )
        try:
            b_proc.wait()
            f_proc.wait()
        except KeyboardInterrupt:
            print("\nShutting down servers...")
            b_proc.terminate()
            f_proc.terminate()


if __name__ == "__main__":
    main()
