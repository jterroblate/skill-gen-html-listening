---
name: skill-gen-html-listening
description: >
  Generate interactive IELTS listening practice HTML with dual-mode player (刷题 + 精听).
  Trigger when user requests: listening practice web page, 听力刷题HTML, 精听interactive HTML,
  listening player, or any IELTS listening practice interface. Includes audio segment sync,
  sentence-by-sentence transcript highlighting, fill-in answers with check/reveal/reset,
  and question-to-audio seek buttons. Supports multiple sections (S1-S4) with 40 questions.
---

# IELTS Listening Player Generator

## Critical: Read Before Starting

**Before generating anything for a NEW unit, read the production workflow:**

→ [production-workflow.md](references/production-workflow.md)

This covers the full pipeline: script → questions → review → TTS → HTML → QC.
Follow every step. Skipping a step WILL waste TTS credits (~$15-25/section) and cause bugs.

## Quick Start

Given a completed IELTS listening session (script, questions, audio segments):

```bash
python scripts/generate_player.py \
  --title "IELTS Listening · U01 Daily Rhythm" \
  --output "/path/to/刷题.html" \
  --mp3 "U01_日常节奏_听力_S1.mp3" \
  --timing /tmp/timing.json \
  --questions /tmp/questions.json \
  --sentences /tmp/sentences.json \
  --q-seg /tmp/q_to_seg.json
```

Validate output:

```bash
python scripts/validate_player.py "/path/to/刷题.html"
```

## HTML Architecture

Two-panel design sharing one audio player:

```
┌─────────────────────────────────────┐
│  Tab Bar: [刷题] [精听]              │
├─────────────────────────────────────┤
│  Audio Player (shared)              │
├─────────────────────────────────────┤
│                                     │
│  ┌─ Panel 0 (刷题) ─────────────┐  │
│  │ Q1  Course code: _____ ▶跳音 │  │
│  │ Q2  Fee: _____ ▶跳音         │  │
│  │ ...                          │  │
│  │ [提交答案] [显示答案] [重置]  │  │
│  └─────────────────────────────┘  │
│                                     │
│  ┌─ Panel 1 (精听) ─────────────┐  │
│  │ [Narrator] You will hear...  │  │
│  │ [Bella] Good morning...      │  │
│  │ ← active sentence highlighted │  │
│  │ ← played sentences grayed    │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Panel 0 — 刷题 (Practice)
- `q-block` wrapper per question with `data-seg="N"` attribute
- `fill-input` with `data-ans` attribute for answer matching
- `seek-btn-inline` at end of each block: `▶ 跳至音频`
- Action bar: submit/reveal/reset buttons with score badge

### Panel 1 — 精听 (Close Listening)
- `sentence` divs with `data-index` attribute matching segment index
- `speaker` span for character label in brackets
- `onclick` calls `playFrom(index)` to seek to that segment
- `active` class = currently playing (orange bg, white text)
- `played` class = already passed (grayed out, 50% opacity)

## JavaScript Critical Rules

### DO NOT LEAVE ORPHANED CODE
Every `}`, `function`, `var`, `const` must be inside a function or valid top-level declaration. The most common bug: remnants of previous `function checkAnswers()` body lines left outside any function after replacement.

### Self-Check Before Delivery
After generating the HTML, always run:

```bash
python scripts/validate_player.py <html_path>
```

This checks:
- Opening `{` count == closing `}` count
- Every `onclick="NAME("` has a matching `function NAME(`
- No orphaned `total++`, `inp.getAttribute`, or similar assignment lines outside functions
- Audio source path resolves relative to HTML location

### Function Inventory
Every generated page must have exactly these functions:
| Function | Trigger | Purpose |
|----------|---------|---------|
| `playFrom(index)` | Sentence click in 精听 | Seek audio + highlight |
| `highlightSegment(index)` | Audio time update | Update active/played classes, scroll |
| `onTimeUpdate()` | audio `timeupdate` event | Update clock, find current segment |
| `switchMode(mode)` | Tab click (0/1) | Toggle panels |
| `checkAnswers()` | 提交答案 button | Mark correct green, wrong red |
| `revealAnswers()` | 显示答案 button | Fill all answers, mark green |
| `resetAnswers()` | 重置 button | Clear inputs, remove marks |
| `playSegment(idx)` | 跳至音频 button | Seek audio, DON'T switch tabs |

### Variable Scope
- Use `var` (not `const`/`let`) for function-scoped variables to avoid block scoping issues
- Segment timing data: global scope (top of `<script>`)
- Sentences array: global scope
- Audio element: after DOM ready

## Audio Workflow

### From TTS to Player
1. Generate per-segment MP3 files via TTS API (ElevenLabs)
   - Each segment = 1 character utterance, ~10-25 seconds
2. Combine into full MP3 with ffmpeg concat:
   ```bash
   ls *.mp3 | sed 's/^/file /' > segments.txt
   ffmpeg -f concat -safe 0 -i segments.txt -c copy full.mp3
   ```
3. Generate timing JSON by measuring each segment's duration:
   ```bash
   ffprobe -v quiet -show_entries format=duration 000.mp3 ...
   ```
   Accumulate start times: seg[0].start=0, seg[N].start=seg[N-1].end
4. Embed timing JSON in HTML as `const segments = [...]`

### Timing JSON Format
```json
{
  "total_duration": 184.0,
  "segments": [
    {"file": "000.mp3", "start": 0.0, "end": 4.32, "duration": 4.32},
    {"file": "001.mp3", "start": 4.32, "end": 15.8, "duration": 11.48},
    ...
  ]
}
```

## Question-to-Segment Mapping
Each `q-block` has a `data-seg` attribute linking to the segment index where the answer appears:

```json
// Question index → segment index (0-based)
{ "1": 3, "2": 3, "3": 5, "4": 14, ... }
```

The `playSegment(idx)` function uses `segments[idx].start` to seek.

## Input File Formats

### questions.json
```json
[
  {"num": 1, "text": "Course code: ___", "answer": "WTM-2026", "seg": 3},
  {"num": 2, "text": "Fee: ___ yuan per person", "answer": "150", "seg": 3},
  ...
]
```

### sentences.json
```json
[
  {"speaker": "Narrator", "text": "You will hear..."},
  {"speaker": "Bella", "text": "Good morning..."},
  ...
]
```

### q_to_seg.json
```json
{"1": 3, "2": 3, "3": 5, ...}
```

## ⚠️ Critical: Chinese Path Handling
Paths containing Chinese characters + spaces **silently fail** with:
- `shutil.copy2()` — fails with FileNotFoundError
- `os.remove()` — raises FileNotFoundError
- `open(path, 'w')` — raises FileNotFoundError

**Workaround**: Always use shell commands with quoted variables:
```bash
DEST="/path/with/中文 and spaces/index.html"
cp /tmp/source.html "$DEST"
```

Or use Python `subprocess.run`:
```python
import subprocess
subprocess.run(["cp", "/tmp/source.html", dest_path])
```

Prefer short English filenames on Desktop (`~/Desktop/`) and use `cp` to move them to the Chinese-named folder.

## ⚠️ Voice Diversity Rules (CRITICAL)

**Do NOT** reuse the same voice for multiple characters across a unit. Maintain **50/50 male/female** and **50/50 British/American** in the **total pool of character voices** across all 4 sections. A dialogue scene with 2 speakers naturally consumes 2 voices — count those toward the total balance.

| Voice | Gender | Accent | Voice ID |
|-------|--------|--------|----------|
| Michael | Male | US | `flq6f7yk4E4fJM5XTYuZ` |
| Bella | Female | US | `hpp4J3VqNfWAUOO0d1Us` |
| Matilda | Female | US | `XrExE9yKIg1WjnnlVkGX` |
| Rachel | Female | UK | `21m00Tcm4TlvDq8ikWAM` |
| Lily | Female | UK | `pFZP5JQG7iQjIQuC4Bku` |

**Allocation example (correct):**

| Section | Characters | Voices | G | A |
|---------|-----------|--------|---|---|
| S1 | Receptionist + Caller | Bella (US,F) + Lily (UK,F) | F,F | US,UK |
| S2 | Radio host (monologue) | Michael (US,M) | M | US |
| S3 | Tom + Sarah (dialogue) | Michael (US,M) + Rachel (UK,F) | M,F | US,UK |
| S4 | Lecturer (monologue) | Matilda (US,F) | F | US |
| **Summary** | 5 character slots | 3F, 2M ≈ 60/40 ✅ | | 4US, 2UK ≈ 66/33 ✅ |

**Key rules:**
1. **Same voice cannot play two different characters** (e.g., Michael can't be both the S2 host AND S3 Tom)
2. Total character slots across all 4 sections should be roughly **50/50 male/female**
3. Total character slots should be roughly **50/50 US/UK accents**
4. Use all 5 available voices across the unit; minimize repeats
5. Rotate voice-to-character assignments between units (don't always use Michael for male leads)
6. Narrator lines get the least-used voice

## QC Checklist
Before delivery, confirm:

- [ ] Braces balanced: `python -c "print(open('file.html').read().count('{') == open('file.html').read().count('}'))"`
- [ ] All 8 functions present (see Function Inventory table)
- [ ] No orphaned code (indented `total++`, `inp.` outside functions)
- [ ] All `onclick` targets exist as functions
- [ ] Audio source path resolves relative to HTML location
- [ ] Tab labels: 刷题 / 精听
- [ ] Title in English: `IELTS Listening · UXX Name`
- [ ] CSS variables defined (`:root{--bg:...}`)
- [ ] Buttons use `btn-primary` / `btn-secondary` classes
- [ ] Voice diversity: 50/50 male/female, 50/50 UK/US, no reuse
- [ ] File copied to correct destination (verify with `ls -la`)
- [ ] Cache-bust: if version mismatch, test with `?v=N` or rename file
