#!/usr/bin/env python3
"""
Verification Gate - Runs all quality checks before claiming completion.

Usage:
    python verify.py [--path /project/path] [--language rust|python|node]

Returns:
    Exit 0 if all checks pass
    Exit 1 if any check fails (with JSON report)

Example:
    python verify.py --path /tmp/my-app --language rust
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    auto_fixable: bool = False


@dataclass
class VerificationReport:
    passed: bool = True
    checks: list = field(default_factory=list)
    summary: str = ""

    def add_check(self, result: CheckResult):
        self.checks.append(result)
        if not result.passed:
            self.passed = False

    def to_json(self) -> str:
        return json.dumps({
            "passed": self.passed,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "message": c.message,
                    "auto_fixable": c.auto_fixable
                }
                for c in self.checks
            ],
            "summary": self.summary
        }, indent=2)


def run_command(cmd: list, cwd: str) -> tuple[int, str, str]:
    """Run command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"


def check_rust(path: str) -> list[CheckResult]:
    """Run Rust-specific checks."""
    results = []

    # Check: cargo test
    code, stdout, stderr = run_command(["cargo", "test", "--all"], path)
    results.append(CheckResult(
        name="tests",
        passed=code == 0,
        message="All tests passed" if code == 0 else f"Test failures:\n{stderr or stdout}",
        auto_fixable=False
    ))

    # Check: cargo clippy
    code, stdout, stderr = run_command(
        ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"],
        path
    )
    results.append(CheckResult(
        name="clippy",
        passed=code == 0,
        message="No clippy warnings" if code == 0 else f"Clippy issues:\n{stderr or stdout}",
        auto_fixable=True
    ))

    # Check: cargo fmt
    code, stdout, stderr = run_command(["cargo", "fmt", "--check"], path)
    results.append(CheckResult(
        name="format",
        passed=code == 0,
        message="Code formatted" if code == 0 else "Formatting issues (run cargo fmt)",
        auto_fixable=True
    ))

    # Check: build succeeds
    code, stdout, stderr = run_command(["cargo", "build"], path)
    results.append(CheckResult(
        name="build",
        passed=code == 0,
        message="Build succeeded" if code == 0 else f"Build failed:\n{stderr}",
        auto_fixable=False
    ))

    # Check: app starts and responds to health check
    startup_result = check_rust_startup(path)
    results.append(startup_result)

    return results


def check_rust_startup(path: str) -> CheckResult:
    """Verify Rust app can start and respond to /health endpoint."""
    import time
    import signal

    # Start the app in background
    try:
        proc = subprocess.Popen(
            ["cargo", "run"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        return CheckResult(
            name="startup",
            passed=False,
            message=f"Failed to start app: {e}",
            auto_fixable=False
        )

    # Wait for app to start (max 10 seconds)
    port = 3000  # Default port
    started = False
    for _ in range(20):
        time.sleep(0.5)
        try:
            import urllib.request
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1)
            if response.status == 200:
                started = True
                break
        except Exception:
            # App not ready yet, keep waiting
            if proc.poll() is not None:
                # Process exited early
                _, stderr = proc.communicate()
                return CheckResult(
                    name="startup",
                    passed=False,
                    message=f"App exited before starting:\n{stderr[:500]}",
                    auto_fixable=False
                )
            continue

    # Kill the app
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()

    if started:
        return CheckResult(
            name="startup",
            passed=True,
            message="App starts and /health responds OK"
        )
    else:
        return CheckResult(
            name="startup",
            passed=False,
            message=f"App did not respond to /health within 10 seconds",
            auto_fixable=False
        )


def check_python(path: str) -> list[CheckResult]:
    """Run Python-specific checks."""
    results = []

    # Check: pytest
    code, stdout, stderr = run_command(["pytest", "-v"], path)
    results.append(CheckResult(
        name="tests",
        passed=code == 0,
        message="All tests passed" if code == 0 else f"Test failures:\n{stdout}",
        auto_fixable=False
    ))

    # Check: ruff (linting)
    code, stdout, stderr = run_command(["ruff", "check", "."], path)
    results.append(CheckResult(
        name="lint",
        passed=code == 0,
        message="No lint issues" if code == 0 else f"Lint issues:\n{stdout}",
        auto_fixable=True
    ))

    # Check: ruff format
    code, stdout, stderr = run_command(["ruff", "format", "--check", "."], path)
    results.append(CheckResult(
        name="format",
        passed=code == 0,
        message="Code formatted" if code == 0 else "Formatting issues (run ruff format)",
        auto_fixable=True
    ))

    return results


def check_node(path: str) -> list[CheckResult]:
    """Run Node.js-specific checks."""
    results = []

    # Check: npm test
    code, stdout, stderr = run_command(["npm", "test"], path)
    results.append(CheckResult(
        name="tests",
        passed=code == 0,
        message="All tests passed" if code == 0 else f"Test failures:\n{stdout}",
        auto_fixable=False
    ))

    # Check: npm run lint (if exists)
    code, stdout, stderr = run_command(["npm", "run", "lint"], path)
    results.append(CheckResult(
        name="lint",
        passed=code == 0,
        message="No lint issues" if code == 0 else f"Lint issues:\n{stdout}",
        auto_fixable=True
    ))

    # Check: npm run build
    code, stdout, stderr = run_command(["npm", "run", "build"], path)
    results.append(CheckResult(
        name="build",
        passed=code == 0,
        message="Build succeeded" if code == 0 else f"Build failed:\n{stderr}",
        auto_fixable=False
    ))

    return results


def check_secrets(path: str) -> CheckResult:
    """Check for exposed secrets."""
    # Try gitleaks
    code, stdout, stderr = run_command(["gitleaks", "detect", "--no-git", "-v"], path)
    if code == 0:
        return CheckResult(
            name="secrets",
            passed=True,
            message="No secrets detected"
        )

    # Check if gitleaks found secrets or just errored
    if "leaks found" in stderr.lower() or "leaks found" in stdout.lower():
        return CheckResult(
            name="secrets",
            passed=False,
            message="Potential secrets detected! Review before committing.",
            auto_fixable=False
        )

    # gitleaks not installed, try basic grep
    patterns = [".env", "API_KEY=", "SECRET=", "PASSWORD=", "aws_secret"]
    for pattern in patterns:
        code, stdout, _ = run_command(
            ["grep", "-r", "--include=*.rs", "--include=*.py", "--include=*.js", pattern],
            path
        )
        if code == 0 and stdout.strip():
            return CheckResult(
                name="secrets",
                passed=False,
                message=f"Potential secret pattern found: {pattern}",
                auto_fixable=False
            )

    return CheckResult(
        name="secrets",
        passed=True,
        message="No obvious secrets detected"
    )


def detect_language(path: str) -> Optional[str]:
    """Auto-detect project language."""
    if os.path.exists(os.path.join(path, "Cargo.toml")):
        return "rust"
    elif os.path.exists(os.path.join(path, "pyproject.toml")) or \
         os.path.exists(os.path.join(path, "setup.py")):
        return "python"
    elif os.path.exists(os.path.join(path, "package.json")):
        return "node"
    return None


def main():
    parser = argparse.ArgumentParser(description="Run verification checks")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--language", choices=["rust", "python", "node"],
                        help="Project language (auto-detected if not specified)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    path = os.path.abspath(args.path)
    language = args.language or detect_language(path)

    if not language:
        print("Could not detect project language. Use --language flag.", file=sys.stderr)
        sys.exit(1)

    report = VerificationReport()

    # Language-specific checks
    if language == "rust":
        for result in check_rust(path):
            report.add_check(result)
    elif language == "python":
        for result in check_python(path):
            report.add_check(result)
    elif language == "node":
        for result in check_node(path):
            report.add_check(result)

    # Universal checks
    report.add_check(check_secrets(path))

    # Summary
    passed = sum(1 for c in report.checks if c.passed)
    total = len(report.checks)
    report.summary = f"{passed}/{total} checks passed"

    if args.json:
        print(report.to_json())
    else:
        print(f"\n{'=' * 40}")
        print(f"Verification Report: {path}")
        print(f"Language: {language}")
        print(f"{'=' * 40}\n")

        for check in report.checks:
            status = "PASS" if check.passed else "FAIL"
            icon = "✓" if check.passed else "✗"
            print(f"[{icon}] {check.name}: {status}")
            if not check.passed:
                print(f"    {check.message[:200]}")
                if check.auto_fixable:
                    print(f"    (auto-fixable)")

        print(f"\n{report.summary}")
        print("=" * 40)

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
