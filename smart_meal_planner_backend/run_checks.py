#!/usr/bin/env python
import subprocess
import sys
from typing import List, Tuple

def run_command(command: List[str]) -> Tuple[int, str]:
    """Run a command and return exit code and output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)

def main():
    checks = [
        (["black", ".", "--check"], "Code formatting (black)"),
        (["pylint", "**/*.py"], "Code linting (pylint)"),
        (["mypy", "."], "Type checking (mypy)"),
        (["pytest", "--cov=.", "--cov-report=term-missing"], "Tests and coverage"),
        (["bandit", "-r", ".", "-c", "pyproject.toml"], "Security check (bandit)"),
        (["safety", "check"], "Dependency safety check"),
    ]

    failed = False
    for command, description in checks:
        print(f"\nRunning {description}...")
        exit_code, output = run_command(command)
        if exit_code != 0:
            print(f"❌ {description} failed:")
            print(output)
            failed = True
        else:
            print(f"✅ {description} passed")

    if failed:
        print("\n❌ Some checks failed")
        sys.exit(1)
    else:
        print("\n✅ All checks passed")
        sys.exit(0)

if __name__ == "__main__":
    main() 