#!/usr/bin/env python3
"""
Workflow Validation Script
Validates the trigger-repo-b.yml workflow configuration
"""

import os
import sys
from pathlib import Path

def validate_workflow():
    """Validate the workflow configuration"""
    errors = []
    warnings = []
    
    workflow_path = Path(__file__).parent / "trigger-repo-b.yml"
    
    if not workflow_path.exists():
        errors.append(f"Workflow file not found: {workflow_path}")
        return errors, warnings
    
    # Read workflow file
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for required elements
    required_elements = {
        "name:": "Workflow name",
        "on:": "Trigger configuration",
        "push:": "Push trigger",
        "branches:": "Branch specification",
        "jobs:": "Jobs section",
        "repository-dispatch@v2": "Repository dispatch action",
        "REPO_B_PAT": "Repo B PAT secret reference",
        "REPO_B_OWNER": "Repo B owner",
        "REPO_B_NAME": "Repo B name",
        "event-type: build-json": "Event type",
    }
    
    for element, description in required_elements.items():
        if element not in content:
            errors.append(f"Missing required element: {description} ({element})")
    
    # Check repository configuration
    if "logik-portal" not in content:
        warnings.append("Repository owner 'logik-portal' found - verify this is correct")
    
    if "repo_b" not in content:
        warnings.append("Repository name 'repo_b' found - verify this is correct")
    
    # Check for proper YAML structure (basic checks)
    if content.count("name:") < 2:  # workflow name + step name
        warnings.append("Workflow may be missing step names")
    
    # Check for secrets
    if "${{ secrets.REPO_B_PAT }}" not in content:
        errors.append("REPO_B_PAT secret reference not found")
    
    return errors, warnings

def main():
    """Main validation function"""
    print("=" * 60)
    print("Workflow Validation for trigger-repo-b.yml")
    print("=" * 60)
    print()
    
    errors, warnings = validate_workflow()
    
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"  • {error}")
        print()
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
        print()
    
    if not errors and not warnings:
        print("✅ Workflow structure looks good!")
        print()
        print("Next steps:")
        print("  1. Ensure REPO_B_PAT secret is configured in GitHub")
        print("  2. Verify Repo B has the corresponding workflow set up")
        print("  3. Make a test commit to trigger the workflow")
        return 0
    elif not errors:
        print("✅ No critical errors found, but review warnings above")
        return 0
    else:
        print("❌ Validation failed - fix errors before testing")
        return 1

if __name__ == "__main__":
    sys.exit(main())
