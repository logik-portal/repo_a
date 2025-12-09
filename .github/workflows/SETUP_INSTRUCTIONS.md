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

**⚠️ IMPORTANT: Use a relative path, NOT an absolute path!**

Example script structure:
```python
#!/usr/bin/env python3
"""
Script to build python_scripts_json.py from Repo A's script directories
"""
import json
import os
from pathlib import Path

def build_python_scripts_json():
    # Your existing logic to build the JSON
    # ...

    # ✅ CORRECT: Write the JSON file to the current directory (Repo B root)
    # Use a relative path - this will work in GitHub Actions
    output_path = Path("python_scripts.json")  # Relative path
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scripts_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {output_path.absolute()}")  # Shows full path for debugging

if __name__ == "__main__":
    build_python_scripts_json()
```

**Common Error:**
```python
# ❌ WRONG - Don't use hardcoded absolute paths like this:
output_file = '/Users/mike/Desktop/python_scripts.json'  # This will fail in GitHub Actions!
```

**Note:** The script should output `python_scripts.json` in the root of Repo B using a **relative path**. The workflow will handle copying it to Repo A.

### 3. Testing

1. Make a change in Repo A and push to main
2. Check Repo A's Actions tab - you should see "Trigger Repo B Workflow" running
3. Check Repo B's Actions tab - you should see "Build and Push JSON to Repo A" running
4. After completion, check Repo A - `python_scripts.json` should be updated

## Troubleshooting

- **Workflow not triggering in Repo B:** Check that `REPO_B_PAT` secret in Repo A has correct permissions
- **Push to Repo A failing:** Check that `REPO_A_PAT` secret in Repo B has write permissions to Repo A
- **JSON file not found:** Ensure `build_python_scripts_json.py` outputs to `python_scripts.json` in Repo B root
- **FileNotFoundError with absolute path:** The script is using a hardcoded absolute path. Change it to a relative path like `Path("python_scripts.json")`. See `WORKFLOW_FIX.md` for details.
