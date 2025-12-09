# Setup Instructions for Cross-Repository Workflow

## Overview
This setup creates a workflow where:
1. When code is pushed to Repo A, it triggers a workflow in Repo B
2. Repo B runs `build_python_scripts_json.py` to generate `python_scripts.json`
3. Repo B pushes the updated JSON file back to Repo A

## Setup Steps

### 1. Repo A Setup (Already Done)
The workflow file `.github/workflows/trigger-repo-b.yml` has been created.

**Required Secret:**
- Go to Repo A → Settings → Secrets and variables → Actions
- Add a secret named `REPO_B_PAT` with a Personal Access Token that has access to Repo B

### 2. Repo B Setup

#### A. Create the Workflow File
1. In Repo B, create `.github/workflows/build-and-push-json.yml`
2. Copy the content from `.github/workflows/repo-b-workflow-template.yml` in Repo A

#### B. Required Secrets
- Go to Repo B → Settings → Secrets and variables → Actions
- Add a secret named `REPO_A_PAT` with a Personal Access Token that has **write** access to Repo A

#### C. Modify build_python_scripts_json.py
The script should generate `python_scripts.json` in the root of Repo B. The workflow will handle copying it to Repo A.

Example script structure:
```python
#!/usr/bin/env python3
"""
Script to build python_scripts.json from Repo A's script directories
"""
import json
import os
from pathlib import Path

def build_python_scripts_json():
    # Your existing logic to build the JSON
    # ...

    # Write the JSON file to the current directory (Repo B root)
    output_path = Path("python_scripts.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scripts_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {output_path}")

if __name__ == "__main__":
    build_python_scripts_json()
```

**Note:** The script should output `python_scripts.json` in the root of Repo B. The workflow will handle pushing it to Repo A.

### 3. Testing

1. Make a change in Repo A and push to main
2. Check Repo A's Actions tab - you should see "Trigger Repo B Workflow" running
3. Check Repo B's Actions tab - you should see "Build and Push JSON to Repo A" running
4. After completion, check Repo A - `python_scripts.json` should be updated

## Troubleshooting

- **Workflow not triggering in Repo B:** Check that `REPO_B_PAT` secret in Repo A has correct permissions
- **Push to Repo A failing:** Check that `REPO_A_PAT` secret in Repo B has write permissions to Repo A
- **JSON file not found:** Ensure `build_python_scripts_json.py` outputs to `python_scripts.json` in Repo B root
