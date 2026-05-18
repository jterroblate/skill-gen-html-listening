# Listening Question Quality Gates (题目质量检查清单)

> 所有生成的 IELTS 听力题目在交付前必须通过此质量检查。
> Blocking items 必须全部通过（met），否则题目需要重写。
> Improvement items 建议至少满足 80%。

---

## 使用说明 | How to Use

1. 对每个生成的 Section 逐一检查
2. 每道题都检查，不只是整体
3. Blocking Items: 1 项未通过 → 该 Section 不通过
4. Improvement Items: 记录哪些可优化
5. 最终生成 QC 报告

---

## 一、Blocking Items（必改项 — 任何一项不通过则重写）

> 这些是"一票否决"项。任何一个不通过，整个 Section 必须返工。

### B1 — Unclear Answer (答案歧义)

**检查内容**：每个空/选择是否只有唯一合理的正确答案。

```
✓ PASS: "What type of membership did she choose?"
         Audio clearly says "Silver membership" → Answer: Silver
         (No other membership type could reasonably fit)

✗ FAIL: "What is the meeting time?"
         Audio says "Let's meet at 2... actually 2:30 would be better."
         → 2:00 and 2:30 could both be argued as the answer

         "The course costs around £200."
         → £200 exact or £200 approx? Answer ambigious.
```

**检查方法**：给一个不了解上下文的人读改题，看他是否可能填出 2 个不同答案。

---

### B2 — Question-Audio Mismatch (题目-音频不匹配)

**检查内容**：题目问的问题能不能在音频中找到对应信息。

```
✓ PASS: Stem Q: "How many books can be borrowed at one time?"
         Audio: "The borrowing limit is six books at any time."
         → 信息匹配

✗ FAIL: Stem Q: "What is the library's opening time?"
         Audio: "The library has many books available."
         → 没有回答 opening time

✗ FAIL: Stem Q: "Why did they choose the questionnaire method?"
         Audio: "We used questionnaires for data collection."
         → 说了用了什么，没说为什么

✗ FAIL: Stem Q: "What does the man suggest doing first?"
         Audio: "We need to collect data, then analyse it."
         → 给出了序列但没有"suggest doing first"的评价性信息
```

**检查方法**：Cover stem 只看 audio transcript，找不找得到题目要求的信息类型。

---

### B3 — Stem Copies Transcript (题干照抄原文)

**检查内容**：题干（stem）和 audio transcript 之间是否有意义的转述。

```
✓ PASS:
  Audio: "I'd recommend the morning tour because it's less crowded."
  Stem: "Which tour is suggested due to fewer visitors?"

✗ FAIL:
  Audio: "I'd recommend the morning tour."
  Stem: "Which tour is recommended?"
  → "recommend" 被照抄，差别很小
```

**检查规则**：
- Stem 不能和 audio 共享超过 3 个连续单词
- Stem 至少替换 1 个关键词或改变句式
- See [paraphrase_engine.md](paraphrase_engine.md) for acceptable transformations

---

### B4 — No Locator (无法定位答案位置)

**检查内容**：学生能否在音频中定位到答案出现的位置。

```
✓ PASS:
  Locator signal: "Now, about the fees..."
  → 清晰的段落过渡，学生知道下面要讲费用了

✗ FAIL:
  音频以不同段落顺序排列，或答案信息在全音频中随机出现
  → 学生不知道信息在哪里讲到了
```

**检查方法**：标注每个题的 locator signal，确认它是可定位的（不是 random mention）。

---

### B5 — Broken Distractor (干扰项明显不合理)

**检查内容**：干扰选项是否具有表面合理性。

```
✓ PASS:
  Question: "What time does the workshop start?"
  Options:   A) 9:00  B) 9:30  C) 10:00
  (All three are reasonable start times)

✗ FAIL:
  Question: "What time does the workshop start?"
  Options:   A) 6:00 AM  B) 9:30 AM  C) 11:00 PM
  → C (11PM) is clearly unreasonable as a workshop start time

✗ FAIL:
  Matching where one option is clearly unrelated to the topic
  → 学生很自然会排除该选项
```

---

### B6 — Ambiguous Distractor (干扰可被解读为正确答案)

**检查内容**：干扰项是否有合理的理由被误解为正确答案（但不是正确答案本身的歧义）。

```
✗ FAIL:
  Audio: "But the environment here is... not ideal."
  Options: A) Good environment  B) Poor environment  C) Moderate
  → A could be argued because "environment" alone appears

✗ FAIL:
  Audio: "Monday wouldn't work. Let's try Wednesday."
  Options: A) Monday  B) Wednesday  C) Friday
  → Monday is rejected clearly, fine.
  But if Audio said "Monday might be okay, but Wednesday is better."
  → Either could be justified as "the proposed day"
```

---

### B7 — Wrong Difficulty (难度与目标 Band 不匹配)

**检查内容**：题目难度是否符合设定的目标分数段。

```
Band 5.5-6.0 check:
  ✓ 词汇：CEFR A2-B1
  ✓ 转述：简单同义替换
  ✗ 不应该有复杂的推理或多层否定
  
Band 7.5-8.0 check:
  ✓ 需要 inferential comprehension
  ✓ 多层干扰
  ✗ 不应该有简单直接的信息提取
```

**检查方法**：对照难度校准表（cambridge_listening_style_rules.md 1.5 节）。

---

### B8 — Unrealistic Spoken Language (对话不自然)

**检查内容**：对话/独白听起来像真实的人类语言还是书面语朗读。

```
✓ Natural:
  "So, um, what I was thinking is... well, maybe we could try a different approach?"

✗ Unnatural:
  "I have been considering the possibility of adopting a novel methodology."
  → 日常口语不会这么说话（S1 场景）

✗ Unnatural:
  "First we will discuss A. Second we will discuss B. Third..."
  → 太刻板，至少加一些过渡词
```

**常见问题**：
- S1 pronounces exactly like script reading, no hesitation
- S3 sounds like prepared presentation, not real discussion
- Too many full sentences without interruption

---

### B9 — Weak S3 Discussion (S3 缺乏观点碰撞)

**检查内容**：Section 3 是否真正展现了学术讨论的特征。

```
✓ HAS discussion:
  - Students disagree and work out solution
  - Opinion expressed with reasons
  - Hesitation and rephrasing
  - At least one "That's true but..."
  - Natural back-and-forth

✗ NO discussion:
  - Student A reads facts, Student B agrees
  - One student dominates with their plan
  - No disagreement or evaluation
  - Sounds like monologue with occasional "mm-hmm"
```

---

### B10 — Weak S4 Lecture Logic (S4 缺乏讲座结构)

**检查内容**：Section 4 是否有清晰的学术讲座结构和信号词。

```
✓ HAS structure:
  - Clear introduction → background → main topic → sub-topics → conclusion
  - Signal words: "Let's turn to", "Another key aspect", "Crucially"
  - Each section clearly separated

✗ NO structure:
  - Information flows without clear transitions
  - No signal words
  - Sounds like someone reading an article, not giving a lecture
```

---

### B11 — Poor Teacher Explanation (解析没有教学价值)

**检查内容**：答案和解析部分是否具有教学价值。

```
✓ Good explanation:
  "The answer is 'Silver'. The locator is 'As for membership types...'
   The distractor is 'Gold', which was the first suggestion but rejected.
   Paraphrase: 'types of membership' → 'membership type'"

✗ Poor explanation:
  "The answer is Silver." (no explanation)
  "The audio says 'Silver'." (no analysis)
```

---

### B12 — Multiple Valid Answers (填空多解)

**检查内容**：填空题是否有唯一答案。

```
✓ PASS:
  Stem: "The park is located on _____ Street."
  Audio: "...on Elm Street."
  → Answer: Elm (unique, no other street name in context)

✗ FAIL:
  Stem: "The course focuses on ____."  
  Audio: "The course covers language skills and cultural awareness."
  → "language skills" OR "cultural awareness" could both fit

  Stem: "The meeting will be held in the ____ room."
  Audio: "We'll use the conference room or the training room."
  → Both mentioned with no disqualification
```

---

### B13 — Weak Uniqueness (无法唯一确定正确选项)

**检查内容**：在匹配题或选择题中，正确选项是否唯一确定。

```
✓ PASS:
  Matching items have one-to-one mapping with clear distinctions
  MCQ: only one option muste"符合所有条件

✗ FAIL:
  MCQ where two options both seem plausible after hearing
  Matching where one item's descriptor is generic enough to fit multiple options
```

---

## 二、Improvement Items（优化项 — 建议满足 ≥80%）

> 这些不是必改项，但满足越多 = 题目质量越高。

### I1 — Weak Distractors (干扰太弱)

**改善方法**：让干扰项更有表面合理性，或增加其"真实性"。

```
Weak: 选项 A 明显错误（和时间无关），B 和 C 合理
改善：让 A 也在音频中被提及

Weak: 干扰选项内容不完整
改善：让干扰项引用音频中的部分正确信息
```

---

### I2 — Weak Paraphrase (转述不足)

**改善方法**：增加转述的深度。

```
Weak: 只换了一个同义词
改善：重组句式 + 换核心词 + 换词性
```

---

### I3 — Too Obvious Answers (答案太明显)

**改善方法**：增加干扰，或减少定位信号的直接程度。

```
Too obvious: Audio heavily stresses the answer word
改善：让答案融入正常说话，不加重语气

Too obvious: Answer appears right after a long pause
改善：让答案在信息流中，不单独突出
```

---

### I4 — Repetitive Answer Pattern (答案模式单一化)

**改善方法**：多样化答案类型。

```
Too repetitive:
  全部 Q1-Q10 都是名词填空
改善：
  混合名词、数字、日期、opinions（根据 Section 类型）
```

---

### I5 — Artificial Dialogue (对话生硬)

**改善方法**：使用更自然的口语表达。

```
Too scripted:
  A: What is your name?
  B: My name is John. I am 25 years old.
  
More natural:
  A: And your name is...?
  B: Oh, it's John. John Parker.
  A: Great. And how old are you, John?
  B: 25. Just turned, actually.
```

---

### I6 — Weak Pedagogy (教学价值不足)

**改善方法**：增加题目的教学设计的深度。每个题目应该有"可以学到什么"的价值。

```
Weak pedagogy:
  只是测试能否听到数字
  
Strong pedagogy:
  测试学生能否从"first suggestion → rejection → correction"中
  识别正确答案，训练批判性听力
```

---

## 三、QC 报告模板 | QC Report Template

在完成每个 Section 的检查后，输出以下报告：

```markdown
## QC Report — [Unit Name] Section [S1/S2/S3/S4]

### Blocking Items

| # | Item | Status | Notes |
|---|------|--------|-------|
| B1 | Unclear Answer | ✅ / ❌ | [如果有问题，写具体] |
| B2 | Q-Audio Mismatch | ✅ / ❌ | |
| B3 | Stem Copies Transcript | ✅ / ❌ | |
| B4 | No Locator | ✅ / ❌ | |
| B5 | Broken Distractor | ✅ / ❌ | |
| B6 | Ambiguous Distractor | ✅ / ❌ | |
| B7 | Wrong Difficulty | ✅ / ❌ | |
| B8 | Unrealistic Spoken Language | ✅ / ❌ | |
| B9 | Weak S3 Discussion | ✅ / ❌ | (仅S3) |
| B10 | Weak S4 Lecture Logic | ✅ / ❌ | (仅S4) |
| B11 | Poor Teacher Explanation | ✅ / ❌ | |
| B12 | Multiple Valid Answers | ✅ / ❌ | |
| B13 | Weak Uniqueness | ✅ / ❌ | |

**All blocking items passed:** ✅ / ❌

### Improvement Items

| # | Item | Score (0-10) | Suggested Improvement |
|---|------|-------------|----------------------|
| I1 | Weak Distractors | /10 | |
| I2 | Weak Paraphrase | /10 | |
| I3 | Too Obvious Answers | /10 | |
| I4 | Repetitive Answer Pattern | /10 | |
| I5 | Artificial Dialogue | /10 | |
| I6 | Weak Pedagogy | /10 | |

**Improvement score:** ___/60 (target: ≥48)

### Overall Verdict

✅ **PASS** — Ready for next stage
❌ **FAIL** — Must address blocking items before proceeding
```

---

*Document version: 1.0 · Last updated: 2026-05-17*
