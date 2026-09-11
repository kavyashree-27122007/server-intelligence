"""
Single-Command End-to-End Pipeline Execution Script.

Reproduces the entire Support Intelligence pipeline under 15 minutes:
1. Data analysis & brand selection
2. Intent taxonomy validation
3. Conversation reconstruction & train/dev/test splitting (Seed=42)
4. Model training & vector indexing (train-only)
5. Automated evaluation harness execution
6. Results verification

Usage:
    python run_pipeline.py [--sample-size 8000] [--seed 42]
"""
import sys
import os
import argparse
import subprocess
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).parent


def run_step(step_name: str, command: list):
    print("\n" + "=" * 70)
    print(f"  STEP: {step_name}")
    print(f"  CMD:  {' '.join(command)}")
    print("=" * 70)
    start_time = time.time()

    res = subprocess.run(command, cwd=str(PROJECT_ROOT))
    elapsed = time.time() - start_time

    if res.returncode != 0:
        print(f"\n❌ FAILED: {step_name} exited with code {res.returncode}")
        sys.exit(res.returncode)

    print(f"✅ COMPLETED: {step_name} in {elapsed:.1f}s")


def main():
    parser = argparse.ArgumentParser(description="Support Intelligence End-to-End Pipeline")
    parser.add_argument("--sample-size", type=int, default=8000, help="Conversation sample size (default 8,000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default 42)")
    args = parser.parse_args()

    total_start = time.time()
    print("=" * 70)
    print("   SUPPORT INTELLIGENCE — END-TO-END PIPELINE RUNNER")
    print(f"   Target: SpotifyCares | Sample Size: {args.sample_size:,} | Seed: {args.seed}")
    print("=" * 70)

    python_bin = sys.executable

    # Step 1: Generate / Verify Golden Evaluation Benchmark
    run_step(
        "Build Golden Benchmark (200 held-out scenarios)",
        [python_bin, "scripts/build_golden_set.py"]
    )

    # Step 2: Conversation Extraction & Splitting
    run_step(
        "Reconstruct Multi-Turn Conversations & Create Splits",
        [python_bin, "scripts/build_conversations.py"]
    )

    # Step 3: Model Training & Retrieval Indexing (TRAIN ONLY)
    run_step(
        "Train Classifier, Baselines & Vector Index",
        [python_bin, "train.py"]
    )

    # Step 4: Run Automated Evaluation Harness
    run_step(
        "Run Evaluation Harness Against Golden Benchmark",
        [python_bin, "evaluate.py"]
    )

    # Step 5: Run Pytest Suite
    run_step(
        "Run Test Suite (Unit & Integration Tests)",
        [python_bin, "-m", "pytest", "tests/", "-v"]
    )

    total_elapsed = time.time() - total_start
    print("\n" + "=" * 70)
    print(f"🎉 FULL PIPELINE COMPLETED SUCCESSFULLY IN {total_elapsed / 60:.1f} MINUTES!")
    print("   Evaluation results: evaluation/results.csv")
    print("   To start API:       python run.py --backend")
    print("   To start Frontend:  python run.py --frontend")
    print("=" * 70)


if __name__ == "__main__":
    main()
