# IELTS Listening Production Workflow

## Overview
This workflow covers creation of one complete listening practice set (4 sections, 40 questions) for a unit. Follow strictly to avoid wasted TTS credits and broken deliverables.

**Wasted‑credit cost of skipping a step:** ~15–25 USD per section in ElevenLabs API calls, plus hours of debug time.

---

## Phase 0: Pre‑Flight Checklist

Before starting ANY work on a new unit:

- [ ] Read the unit's existing **DOCX files** in the `UXX_听力/` folder (script, student DOCX, teacher DOCX). NEVER assume the content—read it first.
- [ ] If a script DOCX already exists → use it verbatim. Do NOT rewrite.
- [ ] If a student question DOCX exists → questions are already designed. Do NOT redesign.
- [ ] If neither exists → proceed to Phase 1.

**Critical rule:** Always read existing files before creating anything. The session summary may be stale.

---

## Phase 1: Script Generation (if no existing script)

### 1a. Source Material
- Speaking topic pack for this unit (usually in the unit's folder or the original pack).
- Every speaking topic in the pack MUST appear in at least one listening section.

### 1b. Section Structure
| Section | Format | Speakers | Question Type |
|---------|--------|----------|---------------|
| S1 | Conversation (2 speakers) | 1 male + 1 female | ONE WORD AND/OR A NUMBER |
| S2 | Monologue / Talk / Radio | 1 speaker | MCQ (A/B/C) or matching |
| S3 | Discussion / Research talk | 2-3 speakers | Multiple choice or matching |
| S4 | Lecture / Talk | 1 speaker (female academic) | ONE WORD ONLY |

### 1c. Script Requirements
- **~500 words per section** → ~3-4 min spoken.
- Natural, conversational English.
- Each segment = one character's uninterrupted speech (turn in dialogue or paragraph in monologue).
- **Save to DOCX** with speaker labels for TTS.

### 1d. Script Validation (BUILT-IN)
- [ ] Every speaking topic covered
- [ ] ~500 words per section
- [ ] Natural IELTS style (no overly complex vocabulary)
- [ ] Speaker names match gender for TTS voice assignment

### 1e. Script Naturalness Enhancement (MANDATORY)
**Do NOT skip this step.** Direct-first-draft scripts sound mechanical. This phase ensures scripts read like real human speech.

#### Step 1: Prepare C19/C20 Style Reference
Before writing, open **2-3 real Cambridge IELTS Listening transcripts** from C19/C20 as style reference. Pay attention to:
- How topics flow naturally between turns (e.g., "Oh that reminds me...", "Speaking of which...", "Actually that's interesting because...")
- The balance of information vs natural conversation — IELTS speakers don't list facts; they discover them through dialogue
- How monologues use signposting ("Let me turn to...", "Now another thing I'd like to mention...")
- Typical word choices and speech patterns — IELTS English is not overly literary

#### Step 2: Write Content Pass (topic coverage first)
Draft the script covering all required speaking topics. At this stage, focus on content completeness. Allow transitions to be rough.

#### Step 3: Naturalisation Pass (SPEECH QUALITY GATE)
Rewrite the entire script focusing ONLY on naturalness. Check:

**Dialogue transitions:**
- ❌ Q: "Do you exercise?" A: "No, but I do enjoy reading."
- ✅ Q: "So do you exercise at all?" A: "To be honest, not as much as I'd like. But I do make time for reading. I find it's the one thing I can stick to."

**Monologue flow:**
- ❌ "Mornings are important. Energy follows a 90-minute cycle. Lunch breaks matter."
- ✅ "Let's start with mornings, because how you begin your day really does set the tone. Now, once you've started working, you might notice your energy dips after about ninety minutes — that's completely normal."

**Character voice differentiation** — give each speaker a subtle verbal habit:
- One speaker uses "I mean" or "you know" occasionally
- One speaker gives shorter, more direct answers
- One speaker tends to reflect before answering ("Well, that's an interesting question...")
- These should be subtle — genuine IELTS characters, not exaggerated

**Questions and interjections** — real conversations have:
- Echo questions: "You mean...?" / "Wait, so...?"
- Agreement: "Exactly." / "That's a good point."
- Thoughtful pauses before important information

#### Step 4: Topic Coverage Check (POST-NATURALISATION)
After the naturalisation pass, go back and check each speaking topic is still covered. If any topic dropped out, weave it back in naturally — don't force it as an obvious insertion.

#### Step 5: Character Voice Consistency Check
- [ ] Each speaker has a distinct pattern (not just different names)
- [ ] No speaker sounds like a list of facts
- [ ] Transitions between speakers feel natural, not task-driven
- [ ] Read the script aloud — does it sound like something a person would actually say?

---

## Phase 2: Question Design

### 2a. Per-Section Rules (from C19/C20 analysis)

| Section | Instruction | Rules |
|---------|-------------|-------|
| S1 | ONE WORD AND/OR A NUMBER | Numbers spelled as spoken. Fill-in notes. |
| S2 | Choose correct letter A/B/C (or matching) | MCQ only 3 options (A/B/C). Testing comprehension, NOT number recall. |
| S3 | Multiple choice or matching | Can have "Choose TWO" or matching. Focus on paraphrase/comprehension. |
| S4 | ONE WORD ONLY | Verbatim from transcript. Vocabulary content words only. |

### 2b. Answer Quality Checks (Critical!)
- [ ] Every fill-in answer is a **verbatim word from the transcript**
- [ ] NO definition-to-term mapping (e.g., don't ask "device for communication" → "phone")
- [ ] Summary completions must be **coherent** (read the completion aloud)
- [ ] MCQ tests comprehension/paraphrase, NOT number recall
- [ ] Answers are vocabulary content words, not defined terms

### 2c. Question-to-Segment Mapping
Create a mapping dict: `{question_number: segment_index}` where segment_index is 0-based.

Example:
```json
{"1": 3, "2": 3, "3": 5, "4": 14}
```
This links Question 1 to the 4th audio segment (index 3).

### 2d. Multi-Round Review
**Round 1 – Self-review:**
- [ ] All answers verbatim in transcript
- [ ] No answer gaps
- [ ] Section instruction rules followed

**Round 2 – Question quality:**
- [ ] Remove any definition-to-term questions
- [ ] Check summary fill-ins read as complete sentences
- [ ] Verify MCQ options are distinct and one is clearly correct

**Round 3 – Cross-check:**
- [ ] Prepare teacher version with answers + transcript refs
- [ ] Verify teacher version matches student version exactly (only answers added)

---

## Phase 3: Audio Generation

### 3a. Voice Assignment — Quality & Scenario Awareness

#### Quality-Tiered Voice Pool

ElevenLabs 有数十种 premade voices，**主动选择更高质量**的新声线，而非固守原来的 5 个缺省声线。

| Tier | Voice | Gender | Accent | Voice ID | 适合场景 |
|------|-------|--------|--------|----------|----------|
| **T1** | **Juniper** | F | US | `aMSt68OGf4xUZAnLpTU8` | Podcast/教育/专业角色 (最高质量 8/8) |
| **T1** | **Eric** | M | US | `cjVigY5qzO86Huf0OWal` | S1 接待/客服 (smooth trustworthy 7/7) |
| **T1** | **Will** | M | US | `bIHbv24MWmeRgasZH58o` | S3 学生 (relaxed conversational 7/7) |
| **T1** | **Jessica** | F | US | `cgSgspJ2msm6clMCkdW9` | S1/S3 年轻女角色 (playful bright 7/7) |
| **T1** | **Bella** | F | US | `hpp4J3VqNfWAUOO0d1Us` | 旁白/职业女性 (warm professional 7/7) |
| **T1** | **Daniel** | M | UK | `onwK4e9ZLuTAKqWW03F9` | S2 电台/S4 讲座 (steady broadcaster 8/8) |
| **T1** | **Alice** | F | UK | `Xb7hH8MSUJpSbSDYk0k2` | S4 学术讲座 (clear educator 7/7) |
| **T1** | **George** | M | UK | `JBFqnCBsd6RMkjVDRZzb` | S2 导游/S4 讲师 (warm storyteller 7/7) |
| T2 | Michael | M | US | `flq6f7yk4E4fJM5XTYuZ` | 补充 US 男声 |
| T2 | Matilda | F | US | `XrExE9yKIg1WjnnlVkGX` | 通⽤专业女性 |
| T2 | Laura | F | US | `FGY2WhTYpPnrIDTdsKH5` | 年轻热情角色 |
| T2 | Rachel | F | UK | `21m00Tcm4TlvDq8ikWAM` | 补充 UK 女声 (warm professional) |
| T2 | Lily | F | UK | `pFZP5JQG7iQjIQuC4Bku` | 补充 UK 女声 (velvety) |
| T2 | River | N | US | `SAz9YHcvj6GT2YYXdXww` | 旁白 (neutral 8/8) |
| T2 | Roger | M | US | `CwhRBWXzGAHq8TQ4Fs17` | 通⽤男声 (laid-back) |
| T2 | Brian | M | US | `nPczCjzI2devNBz1zQrb` | 中年男声 (deep resonant) |
| T3 | Chris | M | US | `iP95p4xoKVk53GoZ742B` | 备选男声 |
| T3 | Charlie(AU) | M | AU | `IKne3meq5aSn9XLyUdCD` | 备选 澳音点缀 |

**Tier ⚠ 避免使用：** Callum (husky trickster), Harry (fierce warrior), Adam (dominant/firm) — 太特色化/卡通化。

#### ⚠️ Scenario Gender Awareness（角色性别暗示）

IELTS 听力中不同角色有默认的社会性别关联，**不可为了凑 50/50 而违背角色现实性别**。

常见 IELTS 场景默认性别：

| 角色 | 默认性别 | 说明 |
|------|---------|------|
| Nurse / Healthcare assistant | Female | IELTS 惯例 |
| Receptionist (hotel/clinic/office) | Female | IELTS 惯例 |
| Librarian | Female | IELTS 惯例 |
| Doctor / GP | Male | C19/C20 惯例 |
| Construction / Manual worker | Male | 现实主流 |
| Lecturer / Professor | M or F | 均可，视学科语境分配 |
| Tour guide | M or F | 均可 |
| Radio host | M or F | 均可 |
| Student | M or F | 均可 |
| Travel agent | Female | C19/C20 惯例 |

**操作流程：**
1. 先根据场景确定各角色的合理性别
2. 在剩余可用声线中选择匹配的男/女声线
3. 最后检查整体男女比例；若偏差过大，调整无强性别暗示的角色

#### Voice Selection Rules

1. **Tier 1 优先** — 每 Section 至少 1 个 Tier 1，整单元 Tier 1 ≥ 60%
2. **Scenario gender first** — 角色现实性别 > 凑 50/50 比例
3. **Tier 3 最多 1 次** / 单元
4. **避免列表中的声线**禁止使用
5. **跨单元轮换** — 每 2 个单元更换主要声线

### 3b. TTS Generation
- Model: `eleven_turbo_v2_5` (fast, good quality)
- Settings: `stability: 0.35, similarity_boost: 0.75, use_speaker_boost: true`
- One API call per segment (1 segment = 1 character turn, ~10-25 seconds audio)
- **Do NOT** use `[pause]` tags — model v3 doesn't process them, they get spoken as text
- **Do NOT** reuse segments from other units — each section must have fresh TTS

### 3c. Audio Assembly
1. Generate all segment MP3s to `_v5/` directory
2. Concat with **ffmpeg** (NOT `cat` — `cat` produces only header):
   ```bash
   ls *.mp3 | sed 's/^/file /' > segments.txt
   ffmpeg -f concat -safe 0 -i segments.txt -c copy full.mp3
   ```
3. Measure each segment duration with `ffprobe`:
   ```bash
   ffprobe -v quiet -show_entries format=duration -of csv=p=0 segment.mp3
   ```
4. Build timing JSON with accumulated start times

### 3d. Audio Quality Checks
- [ ] Duration: 3-4 min per section (~500 words)
- [ ] No overlapping speech
- [ ] No silence gaps
- [ ] Voice matches character gender
- [ ] Scenario gender: 护士/护理没设为男声, 建筑工人没设为女声
- [ ] Voice quality: Tier 1 ≥ 60%, 无 Tier ⚠ 声线
- [ ] ffprobe duration matches expected

---

## Phase 4: HTML Generation

Use the `skill-gen-html-listening` skill:

```bash
python scripts/generate_player.py \
  --title "IELTS Listening · UXX Section Title" \
  --output "/path/to/UXX_日常节奏_听力_SX_刷题.html" \
  --mp3 "UXX_日常节奏_听力_SX.mp3" \
  --timing timing.json \
  --questions questions.json \
  --sentences sentences.json \
  --q-seg q_to_seg.json
```

Then validate:

```bash
python scripts/validate_player.py "/path/to/UXX_日常节奏_听力_SX_刷题.html"
```

### HTML Validation (8 checks + matching checks)
- [ ] Braces balanced (opening `{` count == closing `}` count)
- [ ] All 8 functions present (playFrom, highlightSegment, onTimeUpdate, switchMode, checkAnswers, revealAnswers, resetAnswers, playSegment)
- [ ] No orphaned code (no `total++`, `inp.`, `blocks[i]` outside functions)
- [ ] Audio source path resolves
- [ ] CSS variables defined (`:root{--bg:...}`)
- [ ] Tab labels: 刷题 / 精听
- [ ] Button classes: btn-primary / btn-secondary
- [ ] Title in English: `IELTS Listening · UXX Name`
- [ ] Matching: uses click-match (not HTML5 Drag API)
- [ ] Matching: post-process script applied (`apply_matching.py`)
- [ ] Matching: 主容器 max-width ≤1280px
- [ ] Matching: 右栏宽度 ≥280px，选项文本 `white-space:nowrap`
- [ ] Matching: drop slot 宽度 180px，flex-shrink:0
- [ ] Matching: Submit/Reveal/Reset 正常
- [ ] Matching: 截图确认视觉比例（无右侧过窄、左侧过宽）
- [ ] Matching: options store letter in data-placed (not charAt(0))

---

## Phase 5: File Management

### 5a. File Naming Convention
```
U01_日常节奏/
└── U01_听力/
    ├── U01_日常节奏_听力_S1.mp3          # Audio per section
    ├── U01_日常节奏_听力_S1_刷题.html      # Practice HTML per section
    ├── U01_日常节奏_听力_刷题.html         # S1 ONLY (backward compat)
    ├── U01_日常节奏_听力_练习_学生版.docx   # Printable student version
    ├── U01_日常节奏_听力_练习_教师版.docx   # Teacher version (answers inline)
    └── U01_日常节奏_听力_文本脚本.docx      # TTS-friendly script
```

### 5b. ⚠️ Chinese Path Critical Warning
Paths containing Chinese characters + spaces **silently fail** with:
- `shutil.copy2()` → FileNotFoundError
- `os.remove()` → FileNotFoundError  
- `open(path, 'w')` → may create wrong file
- `subprocess.run(["cp", ...])` with Chinese paths in Python list → may work

**Always** use shell `cp` with double-quoted variables:
```bash
DEST="/Users/xiaomi/雅思input to output/UXX_日常节奏/UXX_听力/文件名.html"
cp /tmp/source.html "$DEST"
```

Or write to `/tmp/` first, then shell-cp to destination.

### 5c. Browser Cache Prevention
When opening local `.html` files:
- Chrome caches aggressively
- Use `open -a "Google Chrome" --args --disable-cache /path/to/file.html`
- Or rename the file (`_v2.html`) to invalidate cache
- Or clear browser cache for `file://` protocol

---

## Phase 6: QC Gate (Before Delivery)

Run THIS checklist before delivering ANY listening set:

```
[ ] Script matches existing DOCX (didn't rewrite)
[ ] All 40 questions across 4 sections
[ ] Each section's instruction matches IELTS rules (S1: word/number, S4: ONE WORD ONLY)
[ ] All fill-in answers are VERBATIM from transcript
[ ] Teacher DOCX matches student DOCX + answers inline
[ ] Audio: 3-4 min per section, correct voices, no errors
[ ] Scenario gender尊重: 每角色的性别符合现实场景（护士/护工≠男声）
[ ] Matching 布局: 主容器 max-width ≤1280px, 右栏 ≥280px, 选项文本不换行
[ ] Matching 功能: click-to-place + swap + Submit/Reveal/Reset 全部正常
[ ] Matching 无残留: 截图确认无右侧过窄、左侧过宽、选项挤断行等问题
[ ] Voice quality: 整单元 Tier 1 ≥ 60%, 无 Tier ⚠ 声线
[ ] All HTMLs pass 8-point validation
[ ] Files in correct directory (verify with `ls -la`)
[ ] Browser cache test: open at least one HTML to confirm
[ ] NATURALNESS: Script passes Read-Aloud Test (Step 1e)
[ ] 题文同序: Question order verified against transcript for each section
[ ] No person-name matching questions in any section (use box matching instead)
```

---

## Common Mistakes Log (READ BEFORE STARTING)

| # | Mistake | Cost | Prevention |
|---|---------|------|------------|
| 1 | Wrote new scripts instead of using existing DOCX | Wasted TTS credits (~$20) | Read existing files first |
| 2 | `data-seg="3"div` (missing `>`) | Broken HTML layout | Always close attributes properly |
| 3 | Orphaned JS code from partial replacement | All buttons broken | Rebuild entire HTML, don't patch |
| 4 | Files written to wrong path (雅思input to/output vs 雅思input to output) | JT can't see updates | Verify `ls -la` at correct path |
| 5 | `cat *.mp3` instead of ffmpeg concat | 4-second audio | Always use ffmpeg concat |
| 6 | `[pause]` tags in TTS text | Spoken as actual words | Remove, set stability param instead |
| 7 | Male voice assigned to female character | Wrong gender audio | Check character names carefully |
| 8 | Browser showing cached old HTML | User reports "not updated" | Force cache-bust or rename file |
| 9 | Script sounds mechanical / forced transitions | Wasted TTS credits + poor student experience | Always run Naturalisation Pass (1e Step 3) + Read-Aloud Test before generating audio |
| 10 | Person-name matching question in S3 | Unfair question, no real IELTS precedent | Use box matching (A-H) or Choose TWO (A-E) instead |
| 11 | Question order doesn't match transcript order (题文同序) | Confused students, broken question flow | Map every question to transcript paragraph BEFORE writing HTML — verify Q1 info precedes Q2 info etc. |
| 12 | Matching questions use HTML5 Drag API (浏览器不兼容) | Drag silently fails, no console access to debug | Use click-match instead: click option → click dropzone. Inline onclick, not addEventListener. |
| 13 | Matching answer options with identical first-letter prefix (e.g. i/ii, a/ab) | Wrong option restored on remove | Store option letter in `data-placed` attribute, do NOT parse from textContent.charAt(0) |
| 14 | DD zones not reset on page reset | Options stuck in used state, zones not cleared | On reset: clear zone innerHTML + remove filled/correct/wrong + restore options to pool |
| 15 | Hidden select not synced with DD zone | Grade on hidden select not visible to user | On place: set select.value = letter. On remove: clear select.value. After gradePanel: sync classes to DD zone. |
| 16 | Answer reveals placed outside dd-items | Unclear which answer matches which item | Place answer-reveal INSIDE each dd-item, right after the dropzone. |
| 17 | S2/S3 action buttons missing onclick attributes | Buttons do nothing when clicked | Verify all 3 buttons have onclick="checkAnswers();ddCheck()" (etc.) after any HTML edit. |

### 3e. Voice Diversity & Quality Rules (CRITICAL)
**Balance is by total character slots across all 4 sections**, not by section count.
A dialogue scene with 2 characters counts both toward the total.

**Rules (summary — full details at §3a):**
1. **Same voice cannot play two different characters** (even across sections)
2. Total character slots ≈ **50/50 male/female**
3. Total character slots ≈ **50/50 US/UK accents**
4. **Scenario gender first** — 角色现实性别 > 凑 50/50 (⼠/护⼠不设为男声，建筑工人不设为⼥声)
5. **Tier 1 voices first** — 主动选择高质量声线（≥ 60% Tier 1）; 新声线表见 §3a
6. Rotate role assignments between units
7. Narrator: use the least-used voice
8. Tier ⚠ 声线 (Callum, Harry, Adam) 禁止使用

**See §3a above for the complete quality-tiered voice pool (18 voices) and scenario gender table.**
