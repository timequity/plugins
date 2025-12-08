#!/usr/bin/env python3
"""Rust build automation with release and cross-compilation support."""

import argparse
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


def run_build(
    project_dir: Path,
    release: bool = False,
    target: Optional[str] = None,
    all_targets: bool = False,
    features: Optional[str] = None,
    verbose: bool = False,
) -> int:
    """Execute cargo build with specified options."""
    cmd = ["cargo", "build"]

    if release:
        cmd.append("--release")

    if target:
        cmd.extend(["--target", target])

    if all_targets:
        cmd.append("--all")

    if features:
        cmd.extend(["--features", features])

    if verbose:
        cmd.append("-v")

    print(f"Running: {' '.join(cmd)}")
    print(f"Directory: {project_dir}")
    print("-" * 40)

    result = subprocess.run(cmd, cwd=project_dir)

    if result.returncode == 0:
        mode = "release" if release else "debug"
        target_dir = project_dir / "target"
        if target:
            target_dir = target_dir / target / mode
        else:
            target_dir = target_dir / mode
        print("-" * 40)
        print(f"Build successful. Artifacts in: {target_dir}")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Build Rust project with release and cross-compilation support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Debug build
  %(prog)s --release                 # Release build
  %(prog)s --target x86_64-unknown-linux-musl  # Cross-compile
  %(prog)s --release --all           # All workspace members
        """,
    )
    parser.add_argument(
        "--release", "-r",
        action="store_true",
        help="Build in release mode with optimizations",
    )
    parser.add_argument(
        "--target", "-t",
        help="Cross-compilation target (e.g., x86_64-unknown-linux-musl)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_targets",
        help="Build all workspace members",
    )
    parser.add_argument(
        "--features", "-f",
        help="Comma-separated list of features to enable",
    )
    parser.add_argument(
        "--path", "-p",
        type=Path,
        help="Project path (default: auto-detect from current directory)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    project_dir = find_cargo_toml(args.path)
    if not project_dir:
        print("Error: Cargo.toml not found in current or parent directories")
        print("Use --path to specify project location")
        sys.exit(1)

    sys.exit(run_build(
        project_dir=project_dir,
        release=args.release,
        target=args.target,
        all_targets=args.all_targets,
        features=args.features,
        verbose=args.verbose,
    ))


if __name__ == "__main__":
    main()
