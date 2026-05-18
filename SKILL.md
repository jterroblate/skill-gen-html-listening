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

### ⚠️ Cross-Check Rule (Manual Generation)
When generating HTML manually (bypassing the `generate_player.py` script):
1. Read this SKILL.md in full to identify ALL features the skill supports.
2. Do NOT skip a feature because it's extra work (e.g., estimated segment timing).
3. If a feature legitimately can't work without data we don't have, FLAG IT to the user explicitly — don't omit it silently.
4. Generate a complete feature set first, then trim only if user confirms.

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
| `cycleSpeed()` | Click speed display | Cycle through playback speed (0.5x–2.0x) |
| `updateSpeedDisplay()` | Internal | Update speed label text |

## Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Space` | Toggle play/pause |
| `←` (ArrowLeft) | Jump to previous sentence |
| `→` (ArrowRight) | Jump to next sentence |
| `↑` (ArrowUp) | Increase playback speed |
| `↓` (ArrowDown) | Decrease playback speed |

Playback speed cycles through: `0.5x → 0.75x → 1.0x → 1.25x → 1.5x → 2.0x`.
Speed can also be toggled by clicking the speed label in the player bar.

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

**Critical: `answer` field rules**
- fill-in (S1, S4): `render_fill()` reads `q["answer"]` and embeds it as `data-ans` on the `<input>` element. `q["text"]` should use `_____` to mark the blank position; if absent, the input is appended at the end.
- MCQ (S2, S3): `render_mcq_*()` reads `q["answer"]` as the correct letter(s) and `q["stem"]` + `q["options"]` for content. The answer must be a single letter string (`"B"`) or comma-joined string for multi-select (`"B,D"`).
- If `data-ans=""` appears in the HTML output, `generate_player.py` did NOT receive a valid answer — check that the questions.json includes non-empty `answer` fields for fill questions.

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

## ⚠️ Voice Diversity & Quality Rules (CRITICAL)

**Do NOT** reuse the same voice for multiple characters across a unit. Maintain **50/50 male/female** and **50/50 British/American** in the **total pool of character voices** across all 4 sections. A dialogue scene with 2 speakers naturally consumes 2 voices — count those toward the total balance.

ElevenLabs 有数十种 premade voices，以下为经过筛选、适合 IELTS 听力场景的高质量声线。**优先使用 Tier 1 声线**。

### Available Voices (Quality-Tiered)

| Tier | Voice | Gender | Accent | Voice ID | 适合场景 |
|------|-------|--------|--------|----------|----------|
| **T1** | **Juniper** | Female | US | `aMSt68OGf4xUZAnLpTU8` | Podcast/教育/专业角色 (最⾼质量, 8/8 模型训练) |
| **T1** | **Eric** | Male | US | `cjVigY5qzO86Huf0OWal` | S1 接待/客服 (smooth, trustworthy, 7 模型) |
| **T1** | **Will** | Male | US | `bIHbv24MWmeRgasZH58o` | S3 学⽣ (relaxed, conversational, 7 模型) |
| **T1** | **Jessica** | Female | US | `cgSgspJ2msm6clMCkdW9` | S1/S3 年轻⼥角色 (playful, bright, 7 模型) |
| **T1** | **Bella** | Female | US | `hpp4J3VqNfWAUOO0d1Us` | 旁⽩/职业⼥性 (warm, professional, 7 模型) |
| **T1** | **Daniel** | Male | UK | `onwK4e9ZLuTAKqWW03F9` | S2 电台/S4 讲座 (steady broadcaster, 8 模型) |
| **T1** | **Alice** | Female | UK | `Xb7hH8MSUJpSbSDYk0k2` | S4 学术讲座 (clear educator, 7 模型) |
| **T1** | **George** | Male | UK | `JBFqnCBsd6RMkjVDRZzb` | S2 导游/S4 讲师 (warm storyteller, 7 模型) |
| T2 | Michael | Male | US | `flq6f7yk4E4fJM5XTYuZ` | ⽤作 US 男声补充 |
| T2 | Matilda | Female | US | `XrExE9yKIg1WjnnlVkGX` | 专业女性，通⽤场景 |
| T2 | Laura | Female | US | `FGY2WhTYpPnrIDTdsKH5` | 年轻热情角色 |
| T2 | Rachel | Female | UK | `21m00Tcm4TlvDq8ikWAM` | ⽤作 UK ⼥声补充 (warm) |
| T2 | Lily | Female | UK | `pFZP5JQG7iQjIQuC4Bku` | ⽤作 UK ⼥声补充 (velvety) |
| T2 | River | Neutral | US | `SAz9YHcvj6GT2YYXdXww` | 旁白 (neutral, 8 模型) |
| T2 | Roger | Male | US | `CwhRBWXzGAHq8TQ4Fs17` | 通⽤男声 (laid-back) |
| T2 | Brian | Male | US | `nPczCjzI2devNBz1zQrb` | 中年男声 (deep, resonant) |
| T3 | Chris | Male | US | `iP95p4xoKVk53GoZ742B` | 备选男声 |
| T3 | Charlie | Male | AU | `IKne3meq5aSn9XLyUdCD` | 备选澳音（偶用作点缀） |

**Tier ⚠ 避免使用（太特色化/卡通化，不适合 IELTS）：** Callum (husky trickster), Harry (fierce warrior), Adam (dominant/firm)。

**Allocation example (using Tier 1 prioritization):**

| Section | Characters | Voices | G | A |
|---------|-----------|--------|---|---|
| S1 | Receptionist + Caller | Eric (US,M) + Alice (UK,F) | M,F | US,UK |
| S2 | Radio host (monologue) | Daniel (UK,M) | M | UK |
| S3 | Tutor + Student (dialogue) | George (UK,M) + Jessica (US,F) | M,F | UK,US |
| S4 | Lecturer (monologue) | Juni​per (US,F) | F | US |
| **Summary** | 5 character slots | 3M, 2F ≈ 60/40 ✅ | | 2UK, 3US ≈ 40/60 ✅ |

### ⚠️ Scenario Gender Awareness（场景性别暗示 — CRITICAL）

IELTS 听⼒的**不同⻆⾊在社会场景中有默认的性别关联**，分配声线时不可为了凑 50/50 男女比例⽽违背现实中的⻆⾊性别暗示。

**基本原则：尊重场景的性别暗示 > 凑 50/50 比例**

#### 常见 IELTS 场景的默认性别关联

| ⻆⾊ | 默认性别 | 理由 |
|------|---------|------|
| Nurse / Healthcare assistant | Female | 现实主流 + IELTS 惯例 |
| Receptionist (hotel/clinic/office) | Female | IELTS 惯例 |
| Librarian | Female | IELTS 惯例 |
| Lecturer / Professor | Male or Female | **均可**，视学科语境灵活分配（理科偏男/文科偏⼥） |
| Tour guide | Male or Female | 均可 |
| Radio host | Male or Female | 均可 |
| Student (undergrad) | Male or Female | 均可 |
| Customer / Caller | Male or Female | 均可 |
| Doctor / GP | Male | C19/C20 惯例偏男 |
| Construction / Manual worker | Male | 现实主流 |
| Police officer | Male | IELTS 惯例 |
| Lab technician / Scientist | Male or Female | 均可，但不宜全篇单⼀性别 |
| Elderly person (retiree) | Male or Female | 均可 |
| Travel agent | Female | C19/C20 惯例 |

> 以上非硬性规则，但**不可为了追求 gender balance ⽽强行将⺟亲/护⼠角色设为男声，或将建筑⼯⼈设为⼥声**。

**操作流程：**
1. 先根据场景**确定各⻆⾊的合理性别**
2. 再根据确定后的性别分布，在**剩余可用声线**中选择对应的男/⼥声线
3. 最后检查整体男女比例是否接近 50/50；若偏差过大（如 6:1），调整**无强性别暗示的角色**（如 lecturer → 换性别）

**示例 — 某一单元的性别分布矫正：**

| Section | 角色 | 场景约束性别 | 初始选声 | 最终调整 |
|---------|------|-------------|---------|---------|
| S1 | Nurse + Patient | F + M/F | Alice(UK,F) + Eric(US,M) | ✅ 合理 |
| S2 | Radio host (monologue) | M/F 均可 | Daniel(UK,M) | 可用 |
| S3 | Librarian + Student | F + M/F | Rachel(UK,F) + Will(US,M) | ⚠ Librarian 偏女，✅ |
| S4 | Construction safety talk | **M** | Eric 已用，改为 Brian(US,M) | ✅ 合理 |
| **性别分布** | | 4F : 3M ≈ 57/43 | | ✅ 可接受 |

### ⚠️ Voice Quality Selection（优先高质量声线）

从 ElevenLabs 数十个 premade voices 中**主动选择更⾼质量的声线**，而非固守原来的 5 个缺省声线。

**质量判断指标：**

| 指标 | ⾼质量标志 |
|------|----------|
| `high_quality_base_model_ids` ⻓度 | ≥7 个模型 (满分 8) |
| `fine_tuning.state` 已训练模型数 | ≥5 个模型为 `fine_tuned` |
| `category` | 优先 `professional` > `premade` (Juniper 独有) |
| 声线描述 | 含 "professional", "clear", "engaging", "warm" 等教育场景关键词 |

**操作规则：**
1. 每次分配声线前，**先查询 ElevenLabs API 确认声线质量**（以上指标）
2. 每个 Section 至少使用 1 个 Tier 1 声线
3. 整单元 Tier 1 声线使用量 ≥ 60%
4. Tier 3 声线每单元最多使用 1 次
5. 避免使用的声线（Callum, Harry, Adam）任何时候都不应出现
6. 如果⼀个 Tier 1 声线在多单元中都适合某类角色，**优先换单元分配** 而非重复使用

**声线池更新流程：**
- 声线表会随 ElevenLabs 新声线发布定期更新
- 新发现的高质量声线 (t≥7, hq≥7, 口音/性别合适) → 加入 Tier 1
- 声线被 ElevenLabs 移除或质量降级 → 降档或移除

### Voice Allocation Summary Rules

**Key rules:**
1. **Same voice cannot play two different characters** (e.g., Eric can't be both the S1 receptionist AND S4 lecturer)
2. Total character slots across all 4 sections should be roughly **50/50 male/female**
3. Total character slots should be roughly **50/50 US/UK accents**
4. Use ≥ Tier 2 声线；⾄少 60% 为 Tier 1
5. 每 2 个单元轮换主要声线 (rotating roster)
6. Narrator lines get the least-used voice
7. **Respect scenario gender暗示** — 角色现实性别 > 凑 50/50
8. **Choose higher-quality voices proactively** — 不固守缺省列表，优先选 Ele​​venLabs 上质量更好的声线

## QC Checklist
Before delivery, confirm:

- [ ] Braces balanced: `python -c "print(open('file.html').read().count('{') == open('file.html').read().count('}'))"`
- [ ] All 10 functions present (see Function Inventory table)
- [ ] No orphaned code (indented `total++`, `inp.` outside functions)
- [ ] All `onclick` targets exist as functions
- [ ] Audio source path resolves relative to HTML location
- [ ] Tab labels: 刷题 / 精听
- [ ] Title in English: `IELTS Listening · UXX Name`
- [ ] CSS variables defined (`:root{--bg:...}`)
- [ ] Buttons use `btn-primary` / `btn-secondary` classes
- [ ] Voice diversity: 50/50 male/female, 50/50 UK/US, no reuse
- [ ] Scenario gender尊重: 护士/护理没设为男声, 建筑工人没设为女声
- [ ] Quality voices: 整单元 Tier 1 ≥ 60%, 无 Tier ⚠ 声线
- [ ] File copied to correct destination (verify with `ls -la`)
- [ ] Cache-bust: if version mismatch, test with `?v=N` or rename file

---

## Content Quality System（内容质量体系）

> ⚠️ **诊断：当前 skill 的不足**
>
> 当前 SKILL.md 主要覆盖 HTML 渲染、JS 逻辑、音频处理和 TTS 工作流——**但缺少听力内容本身的质量指导**。
>
> 已有的生成流程（production-workflow.md）偏重操作流程而非内容设计规范，导致可能出现以下问题：
> - 对话生硬、不自然
> - 题目缺乏真正的干扰机制
> - Section 3 缺乏学术讨论的特点
> - Section 4 没有 lecture 结构
> - 题干和音频之间转述不足
> - 答案歧义或唯一性缺失
>
> 以下新工作流专门解决这些内容质量问题。

### 新工作流：Blueprint-First Approach

**核心原则**：在写任何对话/题目之前，必须先完成 Section Blueprint。

```
Step 1 — Select Section Type & Scenario
    ↓
Step 2 — Complete Section Blueprint
    (使用 references/section_blueprint_template.md)
    ↓
Step 3 — Design Questions with Locator-Distractor-Paraphrase
    (使用 references/cambridge_listening_style_rules.md)
    (使用 references/distractor_library.md)
    (使用 references/paraphrase_engine.md)
    ↓
Step 4 — Write Transcript from Blueprint
    ↓
Step 5 — Apply Quality Gates
    (使用 references/listening_question_quality_gates.md)
    ↓
Step 6 — Only now: Production Pipeline
    (回到 production-workflow.md 做 TTS → HTML → QC)
```

### 新参考文件引用

所有内容质量相关的参考文件位于 `references/` 目录：

| 文件 | 用途 |
|------|------|
| `cambridge_listening_style_rules.md` | 各 Section 的详细场景、结构、答案机制和语言规范 |
| `section_blueprint_template.md` | 每个 Section 的规划模板（必须先填写） |
| `distractor_library.md` | 15 种干扰机制的定义、示例和实现规则 |
| `paraphrase_engine.md` | 14 种转述类型的定义、模式和例子 |
| `listening_question_quality_gates.md` | Quality gates 清单（Blocking + Improvement）|

### 工作流详细步骤

#### Step 1 — 确定 Section 类型与场景

根据 `cambridge_listening_style_rules.md` 中的场景清单选择正确的 Section 场景。

```
S1 选择：accommodation / event / course / membership / travel / job / health / library
S2 选择：activity intro / venue intro / service explanation / event schedule / orientation
S3 选择：project discussion / assignment planning / experiment review / presentation prep
S4 选择：natural science / social science / humanities / engineering / business
```

**不允许**的场景交叉（例如：在 S1 中使用学术讲座，或在 S4 中使用双人对话）。

#### Step 2 — 完成 Section Blueprint

使用 `references/section_blueprint_template.md` 填写完整的 Section 规划，包括：
- Scenario 设定（场景类型、设置、说话人）
- Question Design（题型、答案类型）
- Locator Strategy（每题定位信号 + 转述映射）
- Distractor Plan（每题干扰机制）
- Transcript Function（起承转合）
- Difficulty Calibration（目标分数段）

**约束**：
- 每张 blueprint 必须独立文件到 `blueprints/` 目录
- 未完成 blueprint 不得进入 Step 3
- blueprint 需要通过 self-review（`listening_question_quality_gates.md` Blocking 检查）

#### Step 3 — 题目设计

根据 blueprint 逐题设计，每道题必须明确标注：
- **Locator**：音频中定位答案的关键词或信号
- **Distractor mechanism**：从 `references/distractor_library.md` 选取 1-2 种机制
- **Paraphrase type**：从 `references/paraphrase_engine.md` 选取对应转述类型
- **Answer uniqueness**：确认答案唯一且无歧义

参考 `references/cambridge_listening_style_rules.md` 中各 Section 的详细规则：
- S1：确认/重复/纠正机制必含
- S2：信息密度控制、非 Q-A 结构
- S3：观点碰撞、犹豫、保留式同意
- S4：学术讲座信号词、抽象名词答案

#### Step 4 — 写 Transcript

Blueprint → 对话/独白写作：
1. 场景设定（根据 blueprint 的 scenario）
2. 说话人自然互动（非念稿感）
3. 答案嵌入自然信息流中（不突出、不强调）
4. 干扰信息自然分布
5. 每 2-3 句话包含一次的信息交换（S1/S3）或信号词过渡（S2/S4）

#### Step 5 — Quality Gates

**Blocking Gates**（任何一项 FAIL 则退回 Step 2）：

| 检查项 | 说明 |
|--------|------|
| Unclear Answer | 答案在 transcript 中有歧义 |
| Question-Audio Mismatch | 题干内容在音频中找不到对应 |
| Stem Copies Transcript | 题干直接复制原文超过 3 个单词连续 |
| No Locator | 无法确定答案出现位置 |
| Broken Distractor | 干扰项明显不合理 |
| Wrong Difficulty | 题目难度与目标 band 不匹配 |
| Unrealistic Spoken Language | 对话听起来像书面语 |
| Weak S3 Discussion | 缺乏真正观点碰撞 |
| Weak S4 Lecture Logic | 缺乏学术讲座结构 |

**Improvement Gates**（WARN 不影响交付但需记录）：
- Weak Distractors、Weak Paraphrase、Too Obvious Answers
- Repetitive Answer Pattern、Artificial Dialogue

#### Step 6 — Production Pipeline

通过所有 quality gates 后，回到 `production-workflow.md`：
- 脚本定稿 → TTS 生成 → HTML 组装 → QC 验证 → 交付

---

### 最终 Quality Gates Checklist

使用以下 checklist 进行最终交付前的质量确认（必须逐项通过）：

#### 内容设计
- [ ] 每个 Section 的 Blueprint 已完成并存档
- [ ] 每道题的 locator 清晰可定位
- [ ] 每题均有至少一种干扰机制
- [ ] Stem 无大段复制 transcript 原文
- [ ] 答案唯一且无歧义
- [ ] 填空答案符合指令（ONE WORD ONLY / ONE WORD AND/OR A NUMBER）
- [ ] 干扰项不弱、不合理或可被解为正确答案
- [ ] MCQ 选项不照抄原文

#### Section-Specific
- [ ] S1：包含确认/重复/纠正/干扰
- [ ] S1：对话自然，没有学术词汇
- [ ] S2：单人说明，清晰结构，无 Q-A 形式
- [ ] S2：信息密度适中
- [ ] S3：真实学术讨论，观点碰撞
- [ ] S3：包含犹豫、自我修正、保留式同意等口语特征
- [ ] S3：非一人主导对话
- [ ] S4：学术讲座结构（开头 → 背景 → 主题 → 分论点 → 总结）
- [ ] S4：答案类型为抽象名词/过程/分类术语
- [ ] S4：有 paraphrase，非念答案

#### 转述质量
- [ ] 题干与音频之间至少有 2 种转述变换
- [ ] 不使用模板化转述
- [ ] 转述后仍保持答案唯一性

#### 语言自然度
- [ ] 对话不念稿、不机械
- [ ] 说话人之间有语音差异（习惯用语、语速提示）
- [ ] 过渡自然，不任务驱动

#### 交付标准
- [ ] TTS 生成并验证音频完整性
- [ ] HTML 集成所有 section 的音频
- [ ] 刷题模式 + 精听模式均可用
- [ ] 教师版解析完整
- [ ] Desktop 交付副本已放置

---

*Content Quality System 版本: 1.0 · 最后更新: 2026-05-17*
*基于 Cambridge IELTS 19 & 20 真实出题机制分析*
