#!/usr/bin/env python3
"""Full CI check: lint + test + audit + build."""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional

SCRIPT_DIR = Path(__file__).parent
STEPS = ["lint", "test", "audit", "build"]


def find_cargo_toml(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find Cargo.toml in current or parent directories."""
    path = start_path or Path.cwd()
    path = path.resolve()

    for parent in [path] + list(path.parents):
        cargo_toml = parent / "Cargo.toml"
        if cargo_toml.exists():
            return parent
    return None


def run_step(step: str, project_dir: Path, release: bool = False) -> tuple[int, float]:
    """Run a single CI step. Returns (exit_code, duration_seconds)."""
    start = time.time()

    if step == "lint":
        result = subprocess.run([
            sys.executable, SCRIPT_DIR / "lint.py",
            "--ci", "--path", str(project_dir),
        ])
    elif step == "test":
        result = subprocess.run([
            sys.executable, SCRIPT_DIR / "test.py",
            "--path", str(project_dir),
        ])
    elif step == "audit":
        result = subprocess.run([
            sys.executable, SCRIPT_DIR / "audit.py",
            "--path", str(project_dir),
        ])
    elif step == "build":
        cmd = [sys.executable, SCRIPT_DIR / "build.py", "--path", str(project_dir)]
        if release:
            cmd.append("--release")
        result = subprocess.run(cmd)
    else:
        print(f"Unknown step: {step}")
        return 1, 0

    duration = time.time() - start
    return result.returncode, duration


def main():
    parser = argparse.ArgumentParser(
        description="Full CI check: lint → test → audit → build",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Full CI check
  %(prog)s --release           # Include release build
  %(prog)s --continue          # Continue on failure
  %(prog)s --skip audit        # Skip specific step
  %(prog)s --only lint test    # Run specific steps only
        """,
    )
    parser.add_argument(
        "--continue",
        dest="continue_on_fail",
        action="store_true",
        help="Continue running steps even if one fails",
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        choices=STEPS,
        default=[],
        help="Steps to skip",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=STEPS,
        help="Run only these steps",
    )
    parser.add_argument(
        "--release", "-r",
        action="store_true",
        help="Build in release mode",
    )
    parser.add_argument(
        "--path", "-p",
        type=Path,
        help="Project path (default: auto-detect)",
    )

    args = parser.parse_args()

    project_dir = find_cargo_toml(args.path)
    if not project_dir:
        print("Error: Cargo.toml not found")
        sys.exit(1)

    # Determine which steps to run
    if args.only:
        steps_to_run = [s for s in STEPS if s in args.only]
    else:
        steps_to_run = [s for s in STEPS if s not in args.skip]

    print(f"Project: {project_dir}")
    print(f"Steps: {' → '.join(steps_to_run)}")
    print("=" * 60)

    results: List[tuple[str, int, float]] = []
    total_start = time.time()

    for i, step in enumerate(steps_to_run, 1):
        print(f"\n[{i}/{len(steps_to_run)}] {step.upper()}")
        print("-" * 60)

        exit_code, duration = run_step(step, project_dir, release=args.release)
        results.append((step, exit_code, duration))

        if exit_code != 0 and not args.continue_on_fail:
            print(f"\n{step} failed. Stopping.")
            break

    total_duration = time.time() - total_start

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("-" * 60)

    passed = 0
    failed = 0
    for step, exit_code, duration in results:
        status = "PASS" if exit_code == 0 else "FAIL"
        symbol = "✓" if exit_code == 0 else "✗"
        print(f"  {symbol} {step:<10} {status:<6} ({duration:.1f}s)")
        if exit_code == 0:
            passed += 1
        else:
            failed += 1

    print("-" * 60)
    print(f"Total: {passed} passed, {failed} failed ({total_duration:.1f}s)")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
