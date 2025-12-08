#!/usr/bin/env python3
"""Security audit with cargo-audit."""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def find_cargo_toml(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find Cargo.toml in current or parent directories."""
    path = start_path or Path.cwd()
    path = path.resolve()

    for parent in [path] + list(path.parents):
        cargo_toml = parent / "Cargo.toml"
        if cargo_toml.exists():
            return parent
    return None


def check_cargo_audit_installed() -> bool:
    """Check if cargo-audit is installed."""
    result = subprocess.run(
        ["cargo", "audit", "--version"],
        capture_output=True,
    )
    return result.returncode == 0


def install_cargo_audit() -> bool:
    """Install cargo-audit."""
    print("Installing cargo-audit...")
    result = subprocess.run(["cargo", "install", "cargo-audit"])
    return result.returncode == 0


def check_cargo_lock(project_dir: Path) -> bool:
    """Check if Cargo.lock exists."""
    return (project_dir / "Cargo.lock").exists()


def run_audit(
    project_dir: Path,
    json_output: bool = False,
    ignore: Optional[List[str]] = None,
    fix: bool = False,
    deny: Optional[str] = None,
) -> int:
    """Execute cargo audit."""
    cmd = ["cargo", "audit"]

    if json_output:
        cmd.append("--json")

    if ignore:
        for advisory in ignore:
            cmd.extend(["--ignore", advisory])

    if fix:
        cmd.append("--fix")

    if deny:
        cmd.extend(["--deny", deny])

    print(f"Running: {' '.join(cmd)}")
    print(f"Directory: {project_dir}")
    print("-" * 40)

    return subprocess.run(cmd, cwd=project_dir).returncode


def main():
    parser = argparse.ArgumentParser(
        description="Security audit for Rust dependencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Run audit
  %(prog)s --json                       # JSON output (for CI)
  %(prog)s --ignore RUSTSEC-2022-0001   # Ignore specific advisory
  %(prog)s --fix                        # Auto-update vulnerable deps
  %(prog)s --deny warnings              # Fail on warnings
        """,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output in JSON format (for CI integration)",
    )
    parser.add_argument(
        "--ignore",
        nargs="+",
        help="Advisory IDs to ignore (e.g., RUSTSEC-2022-0001)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically update vulnerable dependencies",
    )
    parser.add_argument(
        "--deny",
        choices=["warnings", "unmaintained", "yanked"],
        help="Treat category as error",
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

    # Check Cargo.lock
    if not check_cargo_lock(project_dir):
        print("Warning: Cargo.lock not found")
        print("Run 'cargo generate-lockfile' to create it")
        print("Attempting to generate...")
        subprocess.run(["cargo", "generate-lockfile"], cwd=project_dir)

    # Check/install cargo-audit
    if not check_cargo_audit_installed():
        if not install_cargo_audit():
            print("Error: Failed to install cargo-audit")
            sys.exit(1)

    exit_code = run_audit(
        project_dir,
        json_output=args.json_output,
        ignore=args.ignore,
        fix=args.fix,
        deny=args.deny,
    )

    print("\n" + "=" * 40)
    if exit_code == 0:
        print("No vulnerabilities found!")
    else:
        print("Security issues detected")
        if not args.fix:
            print("Run with --fix to auto-update vulnerable dependencies")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
