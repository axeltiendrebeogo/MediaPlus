#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FasoHorizon - Sanity Verification Script
Checks generated files for link integrity, DOM stability, and tracking placeholders.
"""

import os
import re

def verify():
    errors = 0
    warnings = 0
    checked_files = 0
    
    # 1. Check folder presence
    print("Checking directories...")
    for folder in ['.', 'articles', 'assets/css', 'assets/js']:
        path = os.path.join(folder)
        if not os.path.exists(path):
            print(f"[ERROR] Directory missing: {path}")
            errors += 1
        else:
            print(f"[OK] Directory found: {path}")
            
    # 2. Check main assets
    print("\nChecking assets...")
    css_file = "assets/css/styles.css"
    js_file = "assets/js/main.js"
    for f in [css_file, js_file]:
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            print(f"[ERROR] Asset missing or empty: {f}")
            errors += 1
        else:
            print(f"[OK] Asset check passed: {f} ({os.path.getsize(f)} bytes)")

    # 3. Gather generated HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden folders or assets
        if 'assets' in root or '.git' in root or '.gemini' in root or '.agents' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"\nFound {len(html_files)} HTML pages to check.")
    
    # Simple regexes to parse tags
    placeholder_pattern = re.compile(r'<!-- EXTRA_TRACKING_SCRIPTS_PLACEHOLDER -->')
    video_pattern = re.compile(r'<video[^>]*>')
    form_pattern = re.compile(r'<form[^>]*>')
    link_pattern = re.compile(r'href="([^"]+)"')
    
    internal_links_to_check = []
    
    # 4. Parse pages
    for filepath in html_files:
        checked_files += 1
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"Analyzing {filepath}...")
        
        # A. Check placeholder
        if not placeholder_pattern.search(content):
            print(f"  [ERROR] Missing tracker placeholder in {filepath}")
            errors += 1
        else:
            # Ok
            pass
            
        # B. Check video tags
        video_tags = video_pattern.findall(content)
        if video_tags:
            print(f"  [INFO] Found {len(video_tags)} native video tag(s) in {filepath}")
            for v_tag in video_tags:
                if 'id="' not in v_tag:
                    print(f"  [ERROR] Video tag missing id: {v_tag}")
                    errors += 1
                if 'class="faso-video-player"' not in v_tag:
                    print(f"  [WARNING] Video tag missing stable class: {v_tag}")
                    warnings += 1
                if 'controls' not in v_tag:
                    print(f"  [WARNING] Video player controls omitted: {v_tag}")
                    warnings += 1
                    
        # C. Check forms
        forms = form_pattern.findall(content)
        if forms:
            for form in forms:
                if 'id="' not in form:
                    print(f"  [ERROR] Form missing ID: {form} in {filepath}")
                    errors += 1
                    
        # D. Collect links
        links = link_pattern.findall(content)
        for link in links:
            # Normalize anchor / external link
            if link.startswith('#') or link.startswith('http') or link.startswith('mailto:'):
                continue
            
            # Resolve link relative path relative to file location
            file_dir = os.path.dirname(filepath)
            resolved_link = os.path.normpath(os.path.join(file_dir, link))
            
            internal_links_to_check.append((filepath, link, resolved_link))

    # 5. Check Link Integrity
    print("\nVerifying link integrity...")
    link_errors = 0
    for source_file, original_link, resolved_link in internal_links_to_check:
        # Check if file exists
        if not os.path.exists(resolved_link):
            # Try splitting anchor if any
            clean_resolved = resolved_link.split('#')[0]
            if not os.path.exists(clean_resolved):
                print(f"[ERROR] Broken link in {source_file}: '{original_link}' -> resolved as '{resolved_link}' does not exist.")
                link_errors += 1
                errors += 1

    if link_errors == 0:
        print("[OK] All internal links are valid!")

    print(f"\n--- Verification Report ---")
    print(f"Files checked: {checked_files}")
    print(f"Errors found: {errors}")
    print(f"Warnings found: {warnings}")
    
    if errors > 0:
        print("[FAIL] Sanity check failed. Please resolve the errors above.")
        return False
    else:
        print("[SUCCESS] All checks passed successfully! FasoHorizon is stable.")
        return True

if __name__ == '__main__':
    verify()
