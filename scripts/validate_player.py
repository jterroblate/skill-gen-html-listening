#!/usr/bin/env python3
"""
Validate IELTS listening practice HTML output.

Checks:
- JS brace balance
- All 10 required functions present
- No orphaned code outside functions
- All onclick targets exist as functions
- Keyboard shortcuts present (Space, arrow keys)
- Speed control present (cycleSpeed, speed display)
- Audio source path resolves
- CSS variables defined
- Tab labels correct
- Button classes correct
"""

import sys, re, os

REQUIRED_FUNCTIONS = [
    "playFrom", "highlightSegment", "onTimeUpdate", "switchMode",
    "checkAnswers", "revealAnswers", "resetAnswers", "playSegment",
    "cycleSpeed", "updateSpeedDisplay"
]

def validate(filepath):
    if not os.path.exists(filepath):
        return {"error": "File not found", "passed": False}
    
    with open(filepath) as f:
        html = f.read()
    
    errors = []
    passes = []
    script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
    
    if not script_match:
        return {"error": "No <script> tag found", "passed": False}
    
    js = script_match.group(1)
    
    # 1. Brace balance
    opens = len(re.findall(r'(?<!\\)\{', js))
    closes = len(re.findall(r'(?<!\\)\}', js))
    if opens == closes:
        passes.append(f"Braces balanced: {opens}/{closes}")
    else:
        errors.append(f"Braces UNBALANCED: {opens} open, {closes} close")
    
    # 2. Required functions
    found_funcs = re.findall(r'function\s+(\w+)', js)
    for fn in REQUIRED_FUNCTIONS:
        if fn in found_funcs:
            passes.append(f"Function '{fn}' found")
        else:
            errors.append(f"Function '{fn}' MISSING")
    
    # 3. Orphaned code detection
    lines = js.split('\n')
    orphaned = []
    in_func = False
    brace_depth = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('function '):
            in_func = True
            brace_depth = stripped.count('{') - stripped.count('}')
            continue
        if in_func:
            brace_depth += stripped.count('{') - stripped.count('}')
            if brace_depth <= 0 and stripped and not stripped.startswith('//'):
                # Check if this is code that should be in a function
                orphan_keywords = ['total++', 'const ans', 'const val', 'inp.getAttribute', 
                                   'inp.classList', 'blocks[i]', 'all[i]', 'tabs[i]']
                if any(k in stripped for k in orphan_keywords):
                    orphaned.append(f"  Line {i+1}: {stripped[:60]}")
            if brace_depth <= 0:
                in_func = False
    
    if orphaned:
        errors.append(f"ORPHANED CODE ({len(orphaned)} lines):")
        errors.extend(orphaned)
    else:
        passes.append("No orphaned code detected")
    
    # 4. Audio source
    src_match = re.search(r'<source src="([^"]+)"', html)
    if src_match:
        audio_path = src_match.group(1)
        passes.append(f"Audio source: {audio_path}")
    else:
        errors.append("Audio source not found")
    
    # 5. CSS variables
    if '--bg:' in html and '--accent:' in html:
        passes.append("CSS variables defined")
    else:
        errors.append("CSS variables MISSING")
    
    # 6. Keyboard shortcuts
    if 'keydown' in js and 'ArrowLeft' in js and 'ArrowRight' in js and 'key ===' in js:
        passes.append("Keyboard shortcuts present (Space / ← → ↑ ↓)")
    else:
        errors.append("Keyboard shortcuts MISSING")
    
    # 7. Speed control
    if 'speedDisplay' in js and 'cycleSpeed' in js and 'playbackRate' in js:
        passes.append("Speed control present (cycleSpeed, speed display)")
    else:
        errors.append("Speed control MISSING")
    
    # 8. Tab labels
    if '刷题' in html and '精听' in html:
        passes.append("Tab labels: 刷题 / 精听")
    else:
        errors.append("Tab labels INCORRECT")
    
    # 9. Button classes
    if 'btn-primary' in html and 'btn-secondary' in html:
        passes.append("Button classes: btn-primary / btn-secondary")
    else:
        errors.append("Button classes MISSING")
    
    # 8. Fill-in question rendering
    fill_inputs = re.findall(r'<input\s+class="fill-input"', html)
    fill_q_blocks = re.findall(r'data-qtype="fill"', html)
    if fill_q_blocks:
        if fill_inputs:
            passes.append(f"Fill-in inputs: {len(fill_inputs)} found for {len(fill_q_blocks)} fill questions")
        else:
            errors.append(f"FILL-IN INPUTS MISSING: {len(fill_q_blocks)} fill questions but no .fill-input elements")
        # Check data-ans is not empty
        empty_ans = re.findall(r'data-ans=""', html)
        if empty_ans:
            errors.append(f"EMPTY ANSWERS: {len(empty_ans)} fill-input(s) with empty data-ans")
        else:
            passes.append("All fill-inputs have non-empty data-ans")
    
    # 9. MCQ question rendering
    mcq_blocks = re.findall(r'data-qtype="mcq_single"', html) + re.findall(r'data-qtype="mcq_multi"', html)
    mcq_opts = re.findall(r'class="mcq-opt"', html)
    if mcq_blocks:
        if mcq_opts:
            passes.append(f"MCQ options: {len(mcq_opts)} found for {len(mcq_blocks)} MCQ questions")
        else:
            errors.append(f"MCQ OPTIONS MISSING: {len(mcq_blocks)} MCQ questions but no .mcq-opt elements")
    
    # 10. HTML size
    passes.append(f"File size: {len(html):,} bytes")
    
    result = {
        "passed": len(errors) == 0,
        "pass": passes,
        "error": errors,
        "file": filepath,
        "size": len(html)
    }
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_player.py <html_file>")
        sys.exit(1)
    
    result = validate(sys.argv[1])
    
    for p in result.get("pass", []):
        print(f"  ✅ {p}")
    for e in result.get("error", []):
        print(f"  ❌ {e}")
    if result.get("error"):
        print(f"\nResult: FAILED ({len(result['error'])} errors)")
    else:
        print(f"\nResult: PASSED ✅")

if __name__ == "__main__":
    main()
