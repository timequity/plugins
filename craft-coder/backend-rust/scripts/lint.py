#!/usr/bin/env python3
"""Rust linting with rustfmt and clippy."""

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


def run_rustfmt(project_dir: Path, fix: bool = False, check_only: bool = False) -> int:
    """Run rustfmt on the project."""
    cmd = ["cargo", "fmt"]

    if check_only or not fix:
        cmd.append("--check")

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_dir)

    if result.returncode != 0 and not fix:
        print("\nFormat issues found. Run with --fix to auto-fix.")

    return result.returncode


def run_clippy(
    project_dir: Path,
    fix: bool = False,
    deny_level: Optional[str] = None,
    allow_dirty: bool = True,
) -> int:
    """Run clippy on the project."""
    cmd = ["cargo", "clippy"]

    if fix:
        cmd.extend(["--fix"])
        if allow_dirty:
            cmd.extend(["--allow-dirty", "--allow-staged"])

    cmd.append("--")

    if deny_level:
        cmd.extend(["-D", deny_level])

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_dir)

    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Lint Rust project with rustfmt and clippy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Check only (no changes)
  %(prog)s --fix               # Auto-fix issues
  %(prog)s --ci                # CI mode (strict, deny warnings)
  %(prog)s --clippy-only       # Only run clippy
  %(prog)s --fmt-only          # Only run rustfmt
        """,
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix formatting and clippy issues",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: strict checking, deny all warnings",
    )
    parser.add_argument(
        "--clippy-only",
        action="store_true",
        help="Only run clippy, skip rustfmt",
    )
    parser.add_argument(
        "--fmt-only",
        action="store_true",
        help="Only run rustfmt, skip clippy",
    )
    parser.add_argument(
        "--deny",
        default=None,
        help="Deny lint level (e.g., warnings, clippy::all)",
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

    exit_code = 0
    deny_level = args.deny or ("warnings" if args.ci else None)

    # Run rustfmt
    if not args.clippy_only:
        print("\n[1/2] rustfmt")
        print("-" * 40)
        fmt_result = run_rustfmt(project_dir, fix=args.fix, check_only=args.ci)
        if fmt_result != 0:
            exit_code = 1
            if args.ci:
                print("Formatting check failed")
                sys.exit(1)

    # Run clippy
    if not args.fmt_only:
        print("\n[2/2] clippy")
        print("-" * 40)
        clippy_result = run_clippy(
            project_dir,
            fix=args.fix and not args.ci,
            deny_level=deny_level,
        )
        if clippy_result != 0:
            exit_code = 1

    # Summary
    print("\n" + "=" * 40)
    if exit_code == 0:
        print("All checks passed!")
    else:
        print("Some checks failed")
        if not args.fix:
            print("Run with --fix to auto-fix issues")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
