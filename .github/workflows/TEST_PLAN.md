# Workflow Test Plan for Repo A

## Overview
This document outlines the testing procedure for the cross-repository workflow that triggers Repo B when code is pushed to Repo A.

## Workflow Flow
1. **Trigger**: Push to `main` branch in Repo A
2. **Action**: Repo A workflow triggers Repo B via `repository-dispatch`
3. **Processing**: Repo B builds `python_scripts.json` from Repo A's scripts
4. **Result**: Repo B pushes updated JSON back to Repo A

## Pre-Test Checklist

### Repo A Configuration
- [x] Workflow file exists: `.github/workflows/trigger-repo-b.yml`
- [ ] Secret `REPO_B_PAT` is configured in Repo A settings
- [ ] Repository names are correct:
  - REPO_B_OWNER: `logik-portal`
  - REPO_B_NAME: `repo_b`
  - REPO_A_OWNER: `logik-portal`
  - REPO_A_NAME: `repo_a`

### Repo B Configuration (Verify in Repo B)
- [ ] Workflow file exists: `.github/workflows/build-and-push-json.yml`
- [ ] Secret `REPO_A_PAT` is configured in Repo B settings (with write access)
- [ ] `build_python_scripts_json.py` script exists and outputs to root

## Test Steps

### Step 1: Validate Workflow Syntax
- [x] Workflow YAML structure is valid
- [x] All required fields are present
- [x] Repository names match expected values

### Step 2: Make Test Commit
1. Make a small change to trigger the workflow
2. Commit and push to `main` branch
3. Expected: Workflow should trigger automatically

### Step 3: Monitor Workflow Execution

#### In Repo A:
1. Go to Actions tab
2. Look for "Trigger Repo B Workflow" run
3. Check that:
   - Workflow starts successfully
   - `repository-dispatch` step completes
   - No errors in logs

#### In Repo B:
1. Go to Actions tab
2. Look for "Build and Push JSON to Repo A" run
3. Check that:
   - Workflow receives the dispatch event
   - Repo A is checked out successfully
   - Python script runs and generates JSON
   - JSON file is copied to Repo A
   - Commit and push to Repo A succeeds

### Step 4: Verify Results
1. Check Repo A for updated `python_scripts.json`
2. Verify the commit message: "Update python_scripts.json from Repo B workflow [skip ci]"
3. Verify the JSON file contains expected script metadata

## Expected Outcomes

### Success Criteria
- ✅ Repo A workflow triggers successfully
- ✅ Repo B workflow receives dispatch event
- ✅ JSON file is generated correctly
- ✅ JSON file is pushed back to Repo A
- ✅ No errors in workflow logs

### Failure Scenarios to Check
- ❌ Workflow not triggering: Check `REPO_B_PAT` secret
- ❌ Repo B not receiving dispatch: Check token permissions
- ❌ JSON generation fails: Check Python script in Repo B
- ❌ Push to Repo A fails: Check `REPO_A_PAT` has write permissions

## Test Execution Log

| Test # | Date | Trigger | Repo A Status | Repo B Status | Result |
|--------|------|---------|---------------|---------------|--------|
| 1      | TBD  | TBD     | TBD           | TBD           | TBD    |

## Notes
- The workflow uses `[skip ci]` in commit message to prevent infinite loops
- Both workflows should complete within a few minutes
- Check GitHub Actions logs for detailed error messages if issues occur
Testing workflow trigger - Tue Dec  9 01:26:02 EST 2025
