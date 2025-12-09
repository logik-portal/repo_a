#!/usr/bin/env python3
"""
Template for build_python_scripts_json.py in Repo B

This script should be placed in Repo B and will:
1. Scan Repo A's directory structure (if available)
2. Extract metadata from Python scripts
3. Generate python_scripts.json
4. Output the JSON file to the current directory (Repo B root)

The GitHub Actions workflow will handle pushing this file to Repo A.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any

# Repository configuration - easily changeable constants
REPO_A_PATH = os.environ.get('REPO_A_PATH', '../repo_a')  # Path to Repo A when checked out
OUTPUT_FILE = 'python_scripts.json'


def extract_script_metadata(script_path: Path) -> Dict[str, Any]:
    """
    Extract metadata from a Python script file.
    Modify this function to match your actual script metadata format.
    """
    metadata = {
        "Script Name": "",
        "Script Version": "",
        "Flame Version": "",
        "Maximum Flame Version": "",
        "Author": "",
        "Creation Date": "",
        "Update Date": "",
        "Description": ""
    }

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from docstring or comments
        # This is a template - adjust regex patterns to match your script format

        # Example: Extract script name
        name_match = re.search(r'Script Name[:\s]+(.+)', content, re.IGNORECASE)
        if name_match:
            metadata["Script Name"] = name_match.group(1).strip()

        # Example: Extract version
        version_match = re.search(r'Script Version[:\s]+(.+)', content, re.IGNORECASE)
        if version_match:
            metadata["Script Version"] = version_match.group(1).strip()

        # Extract other fields similarly...
        # Add your specific extraction logic here

        # Extract full description (between triple quotes or specific markers)
        desc_match = re.search(r'Description[:\s]+\n(.*?)(?=\n\n|\n[A-Z]|\Z)', content, re.DOTALL | re.IGNORECASE)
        if desc_match:
            metadata["Description"] = desc_match.group(1).strip()

    except Exception as e:
        print(f"Error reading {script_path}: {e}")

    return metadata


def find_python_scripts(repo_path: Path) -> List[Path]:
    """
    Find all Python scripts in Repo A.
    Adjust the search pattern to match your directory structure.
    """
    scripts = []

    # Skip certain directories
    skip_dirs = {'.git', '.github', '__pycache__', 'lib', 'assets', 'fonts', 'templates', 'config'}

    for root, dirs, files in os.walk(repo_path):
        # Filter out skipped directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                script_path = Path(root) / file
                scripts.append(script_path)

    return scripts


def build_python_scripts_json():
    """
    Main function to build the python_scripts.json file.
    """
    repo_a = Path(REPO_A_PATH)

    if not repo_a.exists():
        print(f"Warning: Repo A path {REPO_A_PATH} not found. Using current directory.")
        repo_a = Path('.')

    print(f"Scanning scripts in: {repo_a.absolute()}")

    # Find all Python scripts
    scripts = find_python_scripts(repo_a)
    print(f"Found {len(scripts)} Python scripts")

    # Extract metadata from each script
    scripts_data = []
    for script_path in sorted(scripts):
        metadata = extract_script_metadata(script_path)
        if metadata.get("Script Name"):  # Only include if we found a script name
            scripts_data.append(metadata)
            print(f"  - {script_path.name}")

    # Write JSON file
    output_path = Path(OUTPUT_FILE)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scripts_data, f, indent=2, ensure_ascii=False)

    print(f"\nGenerated {output_path} with {len(scripts_data)} scripts")
    return output_path


if __name__ == "__main__":
    build_python_scripts_json()
