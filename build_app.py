#!/usr/bin/env python3
"""Build script for creating macOS .app bundle."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and print output."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def main():
    root_dir = Path(__file__).parent.absolute()
    spec_file = root_dir / "MedicalSupplementAdvisor.spec"
    dist_dir = root_dir / "dist"

    print("=" * 60)
    print("Building Medical Supplement Advisor .app")
    print("=" * 60)
    print()

    print("Step 1: Cleaning previous build...")
    build_dir = root_dir / "build"
    if build_dir.exists():
        run_command(["rm", "-rf", str(build_dir)])
    if dist_dir.exists():
        run_command(["rm", "-rf", str(dist_dir)])
    print("✓ Clean complete")
    print()

    print("Step 2: Building .app with PyInstaller...")
    run_command(["pyinstaller", "--clean", str(spec_file)], cwd=str(root_dir))
    print("✓ Build complete")
    print()

    app_path = dist_dir / "MedicalSupplementAdvisor.app"

    print("=" * 60)
    print("Build successful!")
    print("=" * 60)
    print(f"App location: {app_path}")
    print()
    print("To run the app:")
    print(f"  open '{app_path}'")
    print()
    print("To move to Applications folder:")
    print(f"  cp -R '{app_path}' /Applications/")
    print()


if __name__ == "__main__":
    main()
