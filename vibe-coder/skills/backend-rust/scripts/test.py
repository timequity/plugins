#!/usr/bin/env python3
"""Rust test runner with coverage support."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_cargo_toml(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find Cargo.toml in current or parent directories."""
    path = start_path or Path.cwd()
    path = path.resolve()

    for parent in [path] + list(path.parents):
        cargo_toml = parent / "Cargo.toml"
        if cargo_toml.exists():
            return parent
    return None


def check_coverage_tool() -> Optional[str]:
    """Check which coverage tool is available."""
    # Prefer cargo-llvm-cov (faster, more accurate)
    if shutil.which("cargo-llvm-cov") or subprocess.run(
        ["cargo", "llvm-cov", "--version"],
        capture_output=True,
    ).returncode == 0:
        return "llvm-cov"

    # Fallback to tarpaulin
    if subprocess.run(
        ["cargo", "tarpaulin", "--version"],
        capture_output=True,
    ).returncode == 0:
        return "tarpaulin"

    return None


def run_tests(
    project_dir: Path,
    filter_pattern: Optional[str] = None,
    threads: Optional[int] = None,
    integration_only: bool = False,
    nocapture: bool = False,
    verbose: bool = False,
) -> int:
    """Execute cargo test."""
    cmd = ["cargo", "test"]

    if integration_only:
        cmd.append("--test")
        cmd.append("*")

    if verbose:
        cmd.append("-v")

    if filter_pattern or threads or nocapture:
        cmd.append("--")
        if filter_pattern:
            cmd.append(filter_pattern)
        if threads:
            cmd.extend(["--test-threads", str(threads)])
        if nocapture:
            cmd.append("--nocapture")

    print(f"Running: {' '.join(cmd)}")
    print(f"Directory: {project_dir}")
    print("-" * 40)

    return subprocess.run(cmd, cwd=project_dir).returncode


def run_coverage(
    project_dir: Path,
    tool: str,
    html: bool = False,
    json: bool = False,
) -> int:
    """Run tests with coverage."""
    if tool == "llvm-cov":
        cmd = ["cargo", "llvm-cov"]
        if html:
            cmd.append("--html")
        elif json:
            cmd.append("--json")
    else:  # tarpaulin
        cmd = ["cargo", "tarpaulin"]
        if html:
            cmd.extend(["--out", "Html"])
        elif json:
            cmd.extend(["--out", "Json"])

    print(f"Running: {' '.join(cmd)}")
    print(f"Directory: {project_dir}")
    print("-" * 40)

    result = subprocess.run(cmd, cwd=project_dir)

    if result.returncode == 0 and html:
        if tool == "llvm-cov":
            report_path = project_dir / "target" / "llvm-cov" / "html" / "index.html"
        else:
            report_path = project_dir / "tarpaulin-report.html"
        if report_path.exists():
            print(f"\nCoverage report: {report_path}")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run Rust tests with optional coverage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         # Run all tests
  %(prog)s --coverage              # With coverage report
  %(prog)s --filter test_user      # Filter by name
  %(prog)s --integration           # Integration tests only
  %(prog)s --threads 1             # Single-threaded (for DB tests)
  %(prog)s --coverage --html       # HTML coverage report
        """,
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Run with coverage (requires cargo-llvm-cov or cargo-tarpaulin)",
    )
    parser.add_argument(
        "--filter", "-f",
        dest="filter_pattern",
        help="Test name filter pattern",
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run integration tests only",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML coverage report",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate JSON coverage report",
    )
    parser.add_argument(
        "--threads", "-t",
        type=int,
        help="Number of test threads (use 1 for DB tests)",
    )
    parser.add_argument(
        "--nocapture",
        action="store_true",
        help="Show test output (println!, etc.)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
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

    print(f"Project: {project_dir}")
    print("=" * 40)

    if args.coverage:
        tool = check_coverage_tool()
        if not tool:
            print("Error: No coverage tool found")
            print("Install with: cargo install cargo-llvm-cov")
            print("Or: cargo install cargo-tarpaulin")
            sys.exit(1)

        print(f"Using coverage tool: {tool}")
        exit_code = run_coverage(
            project_dir,
            tool=tool,
            html=args.html,
            json=args.json,
        )
    else:
        exit_code = run_tests(
            project_dir,
            filter_pattern=args.filter_pattern,
            threads=args.threads,
            integration_only=args.integration,
            nocapture=args.nocapture,
            verbose=args.verbose,
        )

    print("\n" + "=" * 40)
    if exit_code == 0:
        print("All tests passed!")
    else:
        print("Some tests failed")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
