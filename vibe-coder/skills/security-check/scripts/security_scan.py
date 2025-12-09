#!/usr/bin/env python3
"""
Security Scanner - OWASP-based code security checks.

Usage:
    python security_scan.py [--path /project/path] [--fix]

Checks:
    - SQL injection vulnerabilities
    - Hardcoded secrets
    - Unsafe eval/exec usage
    - Missing input validation
    - Insecure HTTP usage

Returns:
    Exit 0 if no critical issues
    Exit 1 if critical issues found (with JSON report)
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SecurityIssue:
    severity: str  # critical, high, medium, low
    category: str
    file: str
    line: int
    message: str
    code_snippet: str
    fix_suggestion: str
    auto_fixable: bool = False


@dataclass
class SecurityReport:
    issues: list = field(default_factory=list)
    files_scanned: int = 0

    def add_issue(self, issue: SecurityIssue):
        self.issues.append(issue)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "critical")

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "high")

    def to_json(self) -> str:
        return json.dumps({
            "files_scanned": self.files_scanned,
            "total_issues": len(self.issues),
            "critical": self.critical_count,
            "high": self.high_count,
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "file": i.file,
                    "line": i.line,
                    "message": i.message,
                    "code_snippet": i.code_snippet,
                    "fix_suggestion": i.fix_suggestion,
                    "auto_fixable": i.auto_fixable
                }
                for i in self.issues
            ]
        }, indent=2)


# Security patterns to check
PATTERNS = {
    "sql_injection": {
        "patterns": [
            (r'execute\([^)]*\+[^)]*\)', "String concatenation in SQL execute"),
            (r'query\([^)]*\+[^)]*\)', "String concatenation in SQL query"),
            (r'f"SELECT.*{', "F-string in SQL query"),
            (r'f"INSERT.*{', "F-string in SQL INSERT"),
            (r'f"UPDATE.*{', "F-string in SQL UPDATE"),
            (r'f"DELETE.*{', "F-string in SQL DELETE"),
            (r'format!\("SELECT', "Format macro in SQL (Rust)"),
        ],
        "severity": "critical",
        "fix": "Use parameterized queries instead of string formatting"
    },
    "hardcoded_secrets": {
        "patterns": [
            (r'api_key\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded API key"),
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
            (r'AWS_SECRET_ACCESS_KEY\s*=\s*["\']', "Hardcoded AWS secret"),
            (r'PRIVATE_KEY\s*=\s*["\']', "Hardcoded private key"),
        ],
        "severity": "critical",
        "fix": "Move secrets to environment variables"
    },
    "unsafe_eval": {
        "patterns": [
            (r'\beval\s*\(', "Use of eval()"),
            (r'\bexec\s*\(', "Use of exec()"),
            (r'__import__\s*\(', "Dynamic import"),
        ],
        "severity": "high",
        "fix": "Avoid dynamic code execution; use safer alternatives"
    },
    "unsafe_deserialization": {
        "patterns": [
            (r'pickle\.loads?\s*\(', "Unsafe pickle deserialization"),
            (r'yaml\.load\s*\([^)]*\)', "Unsafe YAML load (use safe_load)"),
            (r'marshal\.loads?\s*\(', "Unsafe marshal deserialization"),
        ],
        "severity": "high",
        "fix": "Use safe deserialization methods"
    },
    "command_injection": {
        "patterns": [
            (r'os\.system\s*\([^)]*\+', "Command injection via os.system"),
            (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', "Shell=True in subprocess"),
            (r'subprocess\.run\s*\([^)]*shell\s*=\s*True', "Shell=True in subprocess"),
        ],
        "severity": "high",
        "fix": "Use subprocess with shell=False and list arguments"
    },
    "insecure_http": {
        "patterns": [
            (r'http://(?!localhost|127\.0\.0\.1)', "Insecure HTTP URL"),
        ],
        "severity": "medium",
        "fix": "Use HTTPS for external URLs"
    },
    "missing_input_validation": {
        "patterns": [
            (r'request\.(args|form|json)\[', "Direct access to request data without validation"),
            (r'\.unwrap\(\)', "Unwrap without error handling (Rust)"),
        ],
        "severity": "medium",
        "fix": "Add input validation before using user data"
    },
    "debug_enabled": {
        "patterns": [
            (r'DEBUG\s*=\s*True', "Debug mode enabled"),
            (r'app\.run\([^)]*debug\s*=\s*True', "Flask debug mode in production"),
        ],
        "severity": "medium",
        "fix": "Disable debug mode in production"
    }
}


def scan_file(filepath: Path, report: SecurityReport):
    """Scan a single file for security issues."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
    except Exception:
        return

    for category, config in PATTERNS.items():
        for pattern, description in config["patterns"]:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    report.add_issue(SecurityIssue(
                        severity=config["severity"],
                        category=category,
                        file=str(filepath),
                        line=i,
                        message=description,
                        code_snippet=line.strip()[:100],
                        fix_suggestion=config["fix"]
                    ))


def scan_directory(path: str, report: SecurityReport):
    """Scan directory for security issues."""
    extensions = {'.py', '.js', '.ts', '.rs', '.go', '.rb', '.php', '.java'}
    exclude_dirs = {'node_modules', 'target', 'venv', '.venv', '__pycache__', '.git'}

    root = Path(path)
    for filepath in root.rglob('*'):
        if filepath.is_file() and filepath.suffix in extensions:
            # Skip excluded directories
            if any(excluded in filepath.parts for excluded in exclude_dirs):
                continue
            report.files_scanned += 1
            scan_file(filepath, report)


def main():
    parser = argparse.ArgumentParser(description="Security scanner")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fail-on", choices=["critical", "high", "medium", "low"],
                        default="critical", help="Exit 1 if issues at this level or above")
    args = parser.parse_args()

    path = os.path.abspath(args.path)
    report = SecurityReport()

    scan_directory(path, report)

    if args.json:
        print(report.to_json())
    else:
        print(f"\n{'=' * 50}")
        print(f"Security Scan: {path}")
        print(f"Files scanned: {report.files_scanned}")
        print(f"{'=' * 50}\n")

        if not report.issues:
            print("No security issues found!")
        else:
            # Group by severity
            for severity in ["critical", "high", "medium", "low"]:
                issues = [i for i in report.issues if i.severity == severity]
                if issues:
                    print(f"\n[{severity.upper()}] ({len(issues)} issues)")
                    print("-" * 40)
                    for issue in issues:
                        print(f"  {issue.file}:{issue.line}")
                        print(f"    {issue.message}")
                        print(f"    Code: {issue.code_snippet}")
                        print(f"    Fix: {issue.fix_suggestion}")
                        print()

        print(f"\nSummary: {report.critical_count} critical, {report.high_count} high")
        print("=" * 50)

    # Determine exit code
    fail_levels = {
        "critical": ["critical"],
        "high": ["critical", "high"],
        "medium": ["critical", "high", "medium"],
        "low": ["critical", "high", "medium", "low"]
    }

    should_fail = any(
        i.severity in fail_levels[args.fail_on]
        for i in report.issues
    )

    sys.exit(1 if should_fail else 0)


if __name__ == "__main__":
    main()
