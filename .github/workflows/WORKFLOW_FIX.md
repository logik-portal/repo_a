# Workflow Fix: File Path Issue

## Problem
The `build_python_scripts_json.py` script in Repo B is using a hardcoded local path:
```python
/Users/mike/Desktop/python_scripts.json
```

This causes the script to fail in GitHub Actions because:
- The path doesn't exist on the GitHub Actions runner
- The script should write to the current working directory (Repo B root)

## Error Message
```
FileNotFoundError: [Errno 2] No such file or directory: '/Users/mike/Desktop/python_scripts.json'
```

## Solution

### Fix in Repo B: `build_python_scripts_json.py`

The script should write to the **current working directory** (which is the Repo B root in the GitHub Actions workflow).

**Change this:**
```python
# ❌ WRONG - Hardcoded absolute path
output_file = '/Users/mike/Desktop/python_scripts.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(scripts_data, f, indent=2, ensure_ascii=False)
```

**To this:**
```python
# ✅ CORRECT - Relative path (current directory)
output_file = 'python_scripts.json'  # or Path('python_scripts.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(scripts_data, f, indent=2, ensure_ascii=False)
```

### Recommended Implementation

Use `Path` for better cross-platform compatibility:

```python
from pathlib import Path

# At the top of the function or file
OUTPUT_FILE = 'python_scripts.json'

# When writing the file
output_path = Path(OUTPUT_FILE)  # This creates a relative path
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(scripts_data, f, indent=2, ensure_ascii=False)

print(f"Generated {output_path.absolute()}")  # Shows full path for debugging
```

## Why This Works

1. **In GitHub Actions**: The script runs from Repo B's root directory (`/home/runner/work/repo_b/repo_b/`)
2. **Relative Path**: `python_scripts.json` resolves to the current working directory
3. **Workflow Copy**: The workflow then copies this file to Repo A:
   ```yaml
   - name: Copy JSON file to Repo A
     run: |
       cp python_scripts.json repo_a_push/python_scripts.json
   ```

## Verification

After fixing, the script should:
1. ✅ Write `python_scripts.json` to Repo B root
2. ✅ Workflow can find and copy the file
3. ✅ File gets pushed to Repo A successfully

## Location of Fix

**File to fix**: `build_python_scripts_json.py` in Repo B (root directory)

**Function to check**: Look for `create_readme_json()` or the function that writes the JSON file (around line 500 based on the error)

## Quick Fix Command (if you have access to Repo B)

```bash
cd /path/to/repo_b
# Find and replace the hardcoded path
sed -i "s|'/Users/mike/Desktop/python_scripts.json'|'python_scripts.json'|g" build_python_scripts_json.py
# Or use a more specific replacement based on your actual code
```
