#!/usr/bin/env python3
"""
Project Validation Script

Validates that a project is correctly initialized:
- Build succeeds
- Health endpoint responds
- Static files served (fullstack)
- Index returns HTML
- All HTMX endpoints exist
- CSS animations are safe

Usage:
    python validate_project.py --path /path/to/project [--port 3000]
"""

import argparse
import subprocess
import time
import sys
import os
import re
from pathlib import Path


def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> tuple[int, str, str]:
    """Run command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def check_build(project_path: str) -> tuple[bool, str]:
    """Check if project builds successfully."""
    code, stdout, stderr = run_cmd("cargo build 2>&1", cwd=project_path, timeout=120)
    output = stdout + stderr
    if "error" in output.lower() and "Compiling" not in output:
        return False, f"Build failed: {output[-500:]}"
    if "Finished" in output or code == 0:
        return True, "Build succeeds"
    return False, f"Build status unclear: {output[-200:]}"


def check_endpoint(url: str) -> tuple[bool, str]:
    """Check if endpoint responds with 200."""
    code, stdout, stderr = run_cmd(f"curl -sf {url}", timeout=10)
    if code == 0:
        return True, f"{url} responds"
    return False, f"{url} failed (code {code})"


def check_static_files(port: int) -> tuple[bool, str]:
    """Check if static files are served."""
    code, stdout, stderr = run_cmd(
        f"curl -sI http://127.0.0.1:{port}/static/styles.css | head -1",
        timeout=10
    )
    if "200" in stdout:
        return True, "Static files served"
    return False, f"Static files not served: {stdout}"


def check_html_response(port: int) -> tuple[bool, str]:
    """Check if index returns HTML."""
    code, stdout, stderr = run_cmd(
        f"curl -s http://127.0.0.1:{port}/ | head -20",
        timeout=10
    )
    if "<html" in stdout.lower() or "<!doctype" in stdout.lower():
        return True, "Index returns HTML"
    return False, f"Index not HTML: {stdout[:100]}"


def find_htmx_endpoints(project_path: str) -> list[str]:
    """Find all hx-* endpoints in templates."""
    templates_dir = Path(project_path) / "templates"
    if not templates_dir.exists():
        return []

    endpoints = set()
    pattern = re.compile(r'hx-(?:get|post|delete)="([^"]+)"')

    for html_file in templates_dir.rglob("*.html"):
        try:
            content = html_file.read_text()
            for match in pattern.findall(content):
                if match.startswith("/"):
                    endpoints.add(match)
        except Exception:
            pass

    return sorted(endpoints)


def check_css_animations(project_path: str) -> tuple[bool, str]:
    """Check for problematic CSS animation patterns."""
    css_file = Path(project_path) / "static" / "styles.css"
    if not css_file.exists():
        return True, "No CSS file (API only?)"

    try:
        content = css_file.read_text()

        # Check for opacity: 0 without animation-fill-mode: both
        has_opacity_0 = "opacity: 0" in content or "opacity:0" in content
        has_fill_both = "animation-fill-mode: both" in content or "fill-mode: both" in content
        has_animation_both = "ease both" in content

        if has_opacity_0 and not (has_fill_both or has_animation_both):
            return False, "CSS has opacity:0 without animation-fill-mode:both (may cause blank page)"

        return True, "CSS animations safe"
    except Exception as e:
        return False, f"CSS check error: {e}"


def check_tower_http(project_path: str) -> tuple[bool, str]:
    """Check if tower-http has fs feature for fullstack."""
    cargo_toml = Path(project_path) / "Cargo.toml"
    if not cargo_toml.exists():
        return True, "Not a Rust project"

    try:
        content = cargo_toml.read_text()
        if "tower-http" in content:
            if '"fs"' in content or "'fs'" in content:
                return True, "tower-http has fs feature"
            return False, "tower-http missing fs feature"
        # Check if it's a fullstack project
        if "askama" in content or "htmx" in content.lower():
            return False, "Fullstack project missing tower-http with fs feature"
        return True, "API only (no tower-http needed)"
    except Exception as e:
        return False, f"Cargo.toml check error: {e}"


def start_app(project_path: str, port: int) -> int | None:
    """Start the app and return PID."""
    # Kill any existing process on port
    run_cmd(f"lsof -ti:{port} | xargs kill -9 2>/dev/null")
    time.sleep(1)

    # Start app in background
    process = subprocess.Popen(
        f"cd {project_path} && cargo run",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for app to start
    time.sleep(5)

    # Check if still running
    if process.poll() is None:
        return process.pid

    return None


def stop_app(port: int):
    """Stop app running on port."""
    run_cmd(f"lsof -ti:{port} | xargs kill -9 2>/dev/null")


def main():
    parser = argparse.ArgumentParser(description="Validate project initialization")
    parser.add_argument("--path", required=True, help="Path to project")
    parser.add_argument("--port", type=int, default=3000, help="Port to use")
    parser.add_argument("--skip-runtime", action="store_true", help="Skip runtime checks")
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)
    port = args.port

    print(f"## Project Validation: {project_path}\n")

    results = []
    warnings = []

    # Static checks (no app running needed)
    print("### Static Checks\n")

    passed, msg = check_build(project_path)
    results.append(("Build", passed, msg))
    print(f"[{'PASS' if passed else 'FAIL'}] {msg}")

    passed, msg = check_tower_http(project_path)
    results.append(("Dependencies", passed, msg))
    print(f"[{'PASS' if passed else 'FAIL'}] {msg}")

    passed, msg = check_css_animations(project_path)
    results.append(("CSS Safety", passed, msg))
    print(f"[{'PASS' if passed else 'WARN'}] {msg}")
    if not passed:
        warnings.append(msg)

    if args.skip_runtime:
        print("\n### Runtime checks skipped\n")
    else:
        print("\n### Runtime Checks\n")

        # Start app for runtime checks
        print("Starting app...")
        pid = start_app(project_path, port)

        if pid:
            try:
                # Health endpoint
                passed, msg = check_endpoint(f"http://127.0.0.1:{port}/health")
                results.append(("Health", passed, msg))
                print(f"[{'PASS' if passed else 'FAIL'}] {msg}")

                # Static files
                passed, msg = check_static_files(port)
                results.append(("Static Files", passed, msg))
                print(f"[{'PASS' if passed else 'FAIL'}] {msg}")

                # Index page
                passed, msg = check_html_response(port)
                results.append(("Index HTML", passed, msg))
                print(f"[{'PASS' if passed else 'FAIL'}] {msg}")

                # HTMX endpoints
                endpoints = find_htmx_endpoints(project_path)
                for endpoint in endpoints:
                    # Remove query params for check
                    clean_endpoint = endpoint.split("?")[0]
                    passed, msg = check_endpoint(f"http://127.0.0.1:{port}{clean_endpoint}")
                    if not passed:
                        warnings.append(f"Endpoint {endpoint} not implemented")
                        print(f"[WARN] {msg}")

            finally:
                stop_app(port)
                print("\nApp stopped.")
        else:
            print("[FAIL] Could not start app")
            results.append(("App Start", False, "Failed to start"))

    # Summary
    print("\n### Summary\n")
    passed_count = sum(1 for _, p, _ in results if p)
    total = len(results)
    print(f"Result: {passed_count}/{total} checks passed")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    failed = [(n, m) for n, p, m in results if not p]
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for name, msg in failed:
            print(f"  - {name}: {msg}")
        sys.exit(1)

    print("\n[OK] Project validation passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
