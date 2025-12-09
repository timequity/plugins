#!/usr/bin/env python3
"""
PRD Validator - Ensures PRD.md follows required format.

Usage:
    python validate_prd.py [--path /project/docs/PRD.md]

Required sections:
    - Problem
    - User
    - Core Action / Core Feature
    - Success Metric / Success Criteria

Returns:
    Exit 0 if valid
    Exit 1 if invalid (with details)
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    sections_found: list = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def to_json(self) -> str:
        return json.dumps({
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "sections_found": self.sections_found
        }, indent=2)


# Required sections (at least one variant must exist)
REQUIRED_SECTIONS = [
    ["Problem"],
    ["User", "Users", "Target User"],
    ["Core Action", "Core Feature", "Features", "MVP Scope"],
    ["Success Metric", "Success Criteria", "Success"],
]

# Optional but recommended
RECOMMENDED_SECTIONS = [
    "Non-Goals",
    "Technical Constraints",
    "Timeline",
    "Dependencies",
]


def find_prd(path: str) -> Path | None:
    """Find PRD.md in project."""
    candidates = [
        Path(path),
        Path(path) / "PRD.md",
        Path(path) / "docs" / "PRD.md",
        Path(path) / "docs" / "prd.md",
    ]

    for candidate in candidates:
        if candidate.is_file() and candidate.suffix.lower() == ".md":
            return candidate

    return None


def extract_sections(content: str) -> dict[str, str]:
    """Extract markdown sections from content."""
    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        # Check for heading (## Section Name)
        match = re.match(r'^#{1,3}\s+(.+)$', line)
        if match:
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()

            current_section = match.group(1).strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def validate_prd(filepath: Path) -> ValidationResult:
    """Validate PRD content."""
    result = ValidationResult()

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        result.add_error(f"Cannot read file: {e}")
        return result

    # Check not empty
    if len(content.strip()) < 50:
        result.add_error("PRD is too short (< 50 characters)")
        return result

    # Extract sections
    sections = extract_sections(content)
    result.sections_found = list(sections.keys())

    # Check required sections
    for required_variants in REQUIRED_SECTIONS:
        found = False
        for variant in required_variants:
            if any(variant.lower() in s.lower() for s in sections.keys()):
                found = True
                break

        if not found:
            result.add_error(f"Missing required section: {required_variants[0]}")

    # Check section content is not empty
    for section_name, content in sections.items():
        if not content.strip():
            result.add_warning(f"Section '{section_name}' is empty")

    # Check for recommended sections
    for recommended in RECOMMENDED_SECTIONS:
        if not any(recommended.lower() in s.lower() for s in sections.keys()):
            result.add_warning(f"Consider adding section: {recommended}")

    # Check for features/tasks
    feature_section = None
    for s in sections.keys():
        if any(x in s.lower() for x in ['feature', 'scope', 'mvp']):
            feature_section = sections[s]
            break

    if feature_section:
        # Check for actionable items (checkboxes or numbered list)
        if not re.search(r'(\[[ x]\]|^\d+\.)', feature_section, re.MULTILINE):
            result.add_warning("Features section should have checkboxes [ ] or numbered list")

    return result


def main():
    parser = argparse.ArgumentParser(description="Validate PRD.md")
    parser.add_argument("--path", default=".", help="Project path or PRD.md file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    args = parser.parse_args()

    prd_path = find_prd(args.path)

    if not prd_path:
        if args.json:
            print(json.dumps({"valid": False, "errors": ["PRD.md not found"]}))
        else:
            print("ERROR: PRD.md not found")
            print("Expected locations:")
            print("  - docs/PRD.md")
            print("  - PRD.md")
        sys.exit(1)

    result = validate_prd(prd_path)

    # In strict mode, warnings are errors
    if args.strict and result.warnings:
        for warning in result.warnings:
            result.add_error(f"(strict) {warning}")
        result.warnings = []

    if args.json:
        print(result.to_json())
    else:
        print(f"\n{'=' * 40}")
        print(f"PRD Validation: {prd_path}")
        print(f"{'=' * 40}\n")

        print(f"Sections found: {', '.join(result.sections_found)}\n")

        if result.errors:
            print("ERRORS:")
            for error in result.errors:
                print(f"  ✗ {error}")
            print()

        if result.warnings:
            print("WARNINGS:")
            for warning in result.warnings:
                print(f"  ⚠ {warning}")
            print()

        status = "VALID" if result.valid else "INVALID"
        print(f"Result: {status}")
        print("=" * 40)

    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
