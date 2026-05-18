# Distractor Library — Cambridge-Style Distractor Mechanisms (干扰机制库)

> 每个干扰机制必须理解其工作原理、Cambridge 真实用例的实现方式，
> 以及在生成题目时如何正确运用。禁止在同一 Section 中超过 3 次使用同一机制。

---

## 目录

1. [First Answer Rejected](#1-first-answer-rejected)
2. [Correction / Self-Correction](#2-correction--self-correction)
3. [Similar Item, Wrong Condition](#3-similar-item-wrong-condition)
4. [Number Correction](#4-number-correction)
5. [Changed Preference](#5-changed-preference)
6. [Mentioned But Excluded](#6-mentioned-but-excluded)
7. [Past vs Present Contrast](#7-past-vs-present-contrast)
8. [Category vs Specific](#8-category-vs-specific)
9. [Clarification After Ambiguity](#9-clarification-after-ambiguity)
10. [Misleading Early Mention](#10-misleading-early-mention)
11. [Hesitation + Self-Correction](#11-hesitation--self-correction)
12. [Comparative Evaluation](#12-comparative-evaluation)
13. [Conditional Rejection](#13-conditional-rejection)
14. [Agreement with Reservation](#14-agreement-with-reservation)
15. [Indirect Negation](#15-indirect-negation)

---

## 1. First Answer Rejected

### Description | 描述

说话人先提出一个选项（A），然后使用否定词（"No", "But", "Actually"）拒绝该选项，改为另一个选项（B）。B 是正确答案。

这是 Cambridge S1 中最常见的干扰机制。

### Cambridge Examples (paraphrased) | 自写示例

```
Example 1 — Activity Choice:
A: Would you like to join the photography workshop?
B: That sounds interesting but I'm more into painting.
--- 干扰: photography workshop | 答案: painting

Example 2 — Date Selection:
A: Shall we go on the 15th?
B: Actually, the 15th doesn't work for me. What about the 17th?
--- 干扰: 15th | 答案: 17th

Example 3 — Service Type:
A: I'd like the Gold membership plan.
Receptionist: The Gold plan has some great benefits.
A: Actually, on second thought, maybe I'll start with the Basic.
--- 干扰: Gold | 答案: Basic
```

### Implementation Rules | 实现规则

1. Rejection 必须有明确否定信号词（"No", "Actually", "Wait", "On second thought", "Hmm, no"）
2. 拒绝和修正之间可以有短暂的 hesitation 或 pause
3. 两个选项必须有表面合理性（不能有"明显错误"的选项）
4. 拒绝后的正确答案必须被确认（至少一次 backchannel confirmation）
5. 在 S1 中，每个对话至少使用 1 次此机制

### Common Mistakes | 常见错误

- ❌ 拒绝信号太弱（学生听不出"rejected"）
- ❌ 拒绝后立即给出答案，没有间隔（不自然）
- ❌ 两个选项非常类似（易产生真正的歧义）
- ❌ 拒绝后没有确认步骤

---

## 2. Correction / Self-Correction

### Description | 描述

说话人自己或对方立即纠正刚说过的信息。纠正后的内容是正确答案。

### Cambridge Examples (paraphrased)

```
Example 1 — Price Correction:
Agent: The tour costs $250 for adults.
Customer: Um, I thought it was $220.
Agent: Oh, you're right — I was looking at last year's price. It's $220 now.
--- 干扰: $250 | 答案: $220

Example 2 — Self-Correction:
"The course starts in September... no, wait — October actually. Let me confirm...
Yes, the first session is in October."
--- 干扰: September | 答案: October

Example 3 — Address Correction:
A: I live at 25 Oak Street.
B: That's 25 Oak Road, isn't it?
A: Yes, Oak Road — sorry, I always mix those up.
--- 干扰: Oak Street | 答案: Oak Road
```

### Implementation Rules

1. 错误信息必须合理（不是明显错误）
2. 纠正信号必须清晰（"sorry", "actually", "wait", "correction", "my mistake"）
3. 纠正后的信息必须被重复/确认一次
4. 不适合使用在 S4（学术讲座中 speaker 不应有明显错误）

### Common Mistakes

- ❌ 纠正不明显（学生只知道听到了两个信息，不知道哪个是纠正后的）
- ❌ 纠正后的信息没有被重复确认
- ❌ 在 S3/S4 中过度使用（降低学术可信度）

---

## 3. Similar Item, Wrong Condition

### Description | 描述

音频中提到了选项中的一个物品/项目，但用于不同的条件、时间、地点或情境。学生听到熟悉的词，容易选择但实际不对。

### Cambridge Examples (paraphrased)

```
Example 1 — Different Day:
Speaker: The museum is free on Tuesdays, but the special exhibition
which is in the West Wing — that costs extra on any day.
Q: Which area has an additional charge?
Options: A) Main gallery B) West Wing C) East Wing
--- 干扰: Main gallery (free) | 答案: West Wing (但学生可能以为free)

Example 2 — Different Age Group:
"The summer camp is open to ages 10 to 15. There's also a weekend
program for younger children, ages 7 to 9."
Q: Who is the summer camp for?
--- 干扰: 7-9 (mentioned but wrong condition) | 答案: 10-15

Example 3 — Different Activity:
Speaker: The guided tour happens every hour. The audio guide
is available at all times and you can use it independently.
Q: What can visitors use at any time?
--- 干扰: guided tour (only hourly) | 答案: audio guide
```

### Implementation Rules

1. 被提起的项目必须使用原词（所以学生容易被误导）
2. 区分条件必须清晰（时间、地点、对象、方式不同）
3. 可用于 S2 的 matching 和 MCQ 题
4. 此机制通常配合 MCQ 设计

### Common Mistakes

- ❌ 区分条件不够清晰，造成真正的歧义
- ❌ 被提起项目的原词被转述（失去误导效果）
- ❌ 同一题目中多个选项都被"提起过"——太乱

---

## 4. Number Correction

### Description | 描述

先提一个数字（价格、日期、时间、数量、年龄等），然后更正为另一个数字。更正后的数字是答案。

### Cambridge Examples (paraphrased)

```
Example 1 — Price:
"It costs £120 per person... but if you book before Friday,
it's actually £95."
--- 干扰: £120 | 答案: £95

Example 2 — Duration:
"The course runs for six weeks... well, the first five weeks are
taught sessions and the last week is self-study, so I suppose
the formal teaching is five weeks."
--- 干扰: 6 weeks | 答案: 5 weeks

Example 3 — Quantity:
"We need 20 volunteers for the event... actually we've had a few
cancellations, so 18 should be enough."
--- 干扰: 20 | 答案: 18
```

### Implementation Rules

1. 两个数字差距不能太大（差距应该在合理范围内）
2. 原因必须合理（不是随意改数字）
3. 更正后的数字必须被确认
4. 自然使用场景：打折、更新信息、纠正错误
5. 主要用于 S1，偶见于 S2

### Common Mistakes

- ❌ 数字差距太大（如 20 → 5，不合理）
- ❌ 没有给出更改的原因
- ❌ 更正信号不清晰

---

## 5. Changed Preference

### Description | 描述

说话人表示之前喜欢/想要 X，但现在更倾向于 Y。Y 是正确答案。

### Cambridge Examples (paraphrased)

```
Example 1 — Course Preference:
A: I was initially thinking about the intensive course.
B: That's quite demanding though.
A: True... I think I'd prefer the standard course. It's more manageable.
--- 干扰: intensive course | 答案: standard course

Example 2 — Travel Plan:
"I originally wanted to visit the mountains, but after seeing the
photos of the coastal route, I changed my mind. The coast looks
incredible."
--- 干扰: mountains | 答案: coast / coastal route

Example 3 — Accommodation:
"I was going to book a hotel, but my friend recommended a hostel.
I checked reviews and... yeah, the hostel seems way friendlier."
--- 干扰: hotel | 答案: hostel
```

### Implementation Rules

1. 必须有明确的"过去 vs 现在"对比语言
2. 使用信号： "originally/at first/initially... but now"
3. "改主意"的过程需要 2-3 个话轮
4. S1 和 S3 均适用（S3 中可以是学术选择改变）

### Common Mistakes

- ❌ "改主意"太快（1 个话轮就改了，不合理）
- ❌ 没有给出改主意的理由
- ❌ 信号语言不够明显

---

## 6. Mentioned But Excluded

### Description | 描述

某个选项在音频中被明确提及，但同时被排除在外（"not available", "any except that", "not on Mondays"）。学生只听到选项被提及就选了。

### Cambridge Examples (paraphrased)

```
Example 1 — Excluded Day:
"We have guided tours every day except Sunday."
Q: When are guided tours available?
Options: A) Saturday B) Sunday C) Every day
--- 干扰: Sunday (mentioned but excluded)

Example 2 — Excluded Item:
"You can bring a camera, but video recording is not allowed."
Q: What is prohibited during the tour?
--- 干扰: camera (mentioned, but NOT prohibited) | 答案: video recording

Example 3 — Excluded Category:
"The workshop is open to all students except those in the first year."
Q: Who can attend the workshop?
--- 干扰: first-year students (mentioned but excluded)
```

### Implementation Rules

1. 被排除的项目必须在音频中明确提到（不是隐式）
2. 排除信号必须清晰（"except", "not", "cannot", "excluded", "unless"）
3. 排除信息之后通常紧接着正确答案信息
4. 适用于 S2 和 S3

### Common Mistakes

- ❌ 排除信号太弱（学生没听出"excluded"）
- ❌ 排除条件复杂到难以在听力中处理
- ❌ 排除后没有给出"可用的"选项信息

---

## 7. Past vs Present Contrast

### Description | 描述

说话人对比过去和现在的情况。"之前是 X，现在是 Y"。问题问当前情况，答案是 Y。

### Cambridge Examples (paraphrased)

```
Example 1 — Location Change:
"The library used to be on the first floor, but it moved to
the ground floor last year."
Q: Where is the library now?
--- 干扰: first floor | 答案: ground floor

Example 2 — Policy Change:
"Previously, membership was free for students. However, now there's
a small annual fee of £15."
Q: What is the current cost for student membership?
--- 干扰: free | 答案: £15

Example 3 — Opening Hours:
"The park used to close at 5pm, but since September it's open
until 7pm."
Q: What time does the park close now?
--- 干扰: 5pm | 答案: 7pm
```

### Implementation Rules

1. 使用明确的过去/现在信号 (used to / previously / now / currently / these days)
2. 过去的信息是干扰，现在的信息是答案
3. 变化的原因可选提供
4. 适用于 S2 和 S4

### Common Mistakes

- ❌ 没有明确的时间对比信号
- ❌ 问题问的是"过去"还是"现在"不清晰
- ❌ 学生可能依靠常识而非听力作答

---

## 8. Category vs Specific

### Description | 描述

音频提到一个大类（如"fruits"、"sports"），但问题问的是具体子项目（如"apples"、"swimming"）。学生听到大类就选了，但需要更具体的信息。

### Cambridge Examples (paraphrased)

```
Example 1 — Fruit Category:
"They have a great variety of fruits — apples, oranges, and kiwis."
Q: Which fruit is mentioned as being grown locally?
--- 干扰: fruit (too general) | 答案: apples

Example 2 — Sports:
"The centre offers various sports facilities including swimming pools,
tennis courts, and a gym."
Q: What new facility was built last year?
--- 干扰: sports facilities (general category) | 答案: swimming pools (specific)

Example 3 — Tools:
"For the experiment, you'll need some basic lab equipment —
specifically, a microscope and test tubes."
Q: What piece of equipment is essential for the experiment?
--- 干扰: lab equipment (general) | 答案: microscope (specific)
```

### Implementation Rules

1. 大类信息先出现，具体信息后出现
2. 问题需要指向"具体的"那个
3. 适用于 note completion 和 MCQ
4. 干扰项通常是题目中本身的概括词

### Common Mistakes

- ❌ 问题指向不明，学生可以合理选"大类"
- ❌ 问题中没有足够的限定词指向具体项目

---

## 9. Clarification After Ambiguity

### Description | 描述

说话人先给出模糊/不明确的信息，然后通过澄清让信息变得明确。澄清后的信息是正确答案。

### Cambridge Examples (paraphrased)

```
Example 1 — Address Clarification:
A: I live on Green Street.
B: The one near the park or the one near the station?
A: The park — number 42.
Q: What is the address?
--- 初始: Green Street (模糊) | 澄清: 42 Green Street (near park)

Example 2 — Time Clarification:
A: Let's meet on Tuesday.
B: Morning or afternoon?
A: Afternoon. Around 2pm.
Q: What time will they meet?
--- 初始: Tuesday (模糊) | 澄清: Tuesday afternoon, 2pm

Example 3 — Name Clarification:
"My name's Chris — that's C-H-R-I-S, not with a K."
Q: How is the name spelled?
--- 初始: Chris (ambiguity with Kris) | 澄清: C-H-R-I-S
```

### Implementation Rules

1. 初始信息必须具有合理的歧义性
2. 澄清必须是自然的追问或确认
3. 澄清后的信息必须比初始信息更精确
4. S1 中非常常见（地址、名字、时间等）

### Common Mistakes

- ❌ 模糊信息本身没有歧义（学生不会觉得需要澄清）
- ❌ 澄清过程不自然（听起来像为了出题而问）
- ❌ 问题问的是模糊信息而非澄清后的信息

---

## 10. Misleading Early Mention

### Description | 描述

在对话/讲座的早期提到某个信息，看似与后续问题相关但实际上不相关。学生记住了早期信息，在回答问题时会错误使用。

### Cambridge Examples (paraphrased)

```
Example 1 — Early Mention:
Early in the talk:
"This park was established in 1850."
Later:
"The botanical gardens opened in 1920, and the park was renovated."

Q: When was the park established?
--- 干扰: 1850 (early mention — wrong park)
| 答案: (correct year from context)

Example 2 — Course Info:
Early: "The Biology course is on Mondays."
Later: "Chemistry moved to Wednesdays. And Physics is on Fridays."

Q: When is the Physics class?
--- 干扰: Monday (from early course info)
| 答案: Friday
```

### Implementation Rules

1. 早期信息必须和问题有表面关联（同一主题/同一词类）
2. 两个信息之间至少间隔 30 秒以上的音频
3. 干扰不能太牵强（学生应该有可能记住早期信息）
4. 适用于 S2 和 S4 的信息密集段落

### Common Mistakes

- ❌ 早期信息和问题完全无关（不会误导）
- ❌ 两个信息的词/数字一模一样（变成真正的歧义）
- ❌ 两个信息之间的间隔太短

---

## 11. Hesitation + Self-Correction

### Description | 描述

说话人犹豫、改口或重新措辞。这是学术讨论（S3）中的自然特征，常作为干扰信号。

### Cambridge Examples (paraphrased)

```
Example 1 — Research Method:
"I think we should use... well, I was going to say interviews,
but actually questionnaires might work better for our sample size."
--- 干扰: interviews | 答案: questionnaires

Example 2 — Chapter Structure:
"The paper should start with... hmm, the literature review,
no — I mean the introduction, then the literature review."
--- 干扰: literature review (mentioned first) | 答案: introduction

Example 3 — Data Collection:
"We could analyse the... I mean collect the data first,
then analyse it. So data collection comes first."
--- 干扰: analyse | 答案: collect
```

### Implementation Rules

1. 犹豫信号必须自然 ("well...", "I mean...", "actually...", "no...")
2. 初始词和修正词一般相关但不相同
3. 修正后的词是正确答案
4. 主要用于 S3（学术讨论中自然的犹豫和修正）

### Common Mistakes

- ❌ 犹豫信号太频繁（听起来不自然）
- ❌ 修正后的信息没有足够强调
- ❌ 修正的过程不符合 S3 的场景

---

## 12. Comparative Evaluation

### Description | 描述

对两个或以上选项进行比较评估。"X is good but Y is better" 或 "X has this advantage but Y has that advantage"。问题问的是"better/prefer/recommend"这类评价性信息。

### Cambridge Examples (paraphrased)

```
Example 1 — Recommendation:
Speaker A: The online course is flexible.
Speaker B: True, but the in-person class gives you more interaction
and I think that's more valuable for our level.
Q: What do the speakers agree would be better?
--- 干扰: online course (has advantage) | 答案: in-person class

Example 2 — Method Comparison:
"Survey A is quick to administer, but Survey B collects richer data."
Q: Which survey method is more suitable?
--- 干扰: Survey A (quick = easier) | 答案: Survey B (richer data)

Example 3 — Resource Choice:
"Using the library database is reliable, but the internet gives
you more up-to-date information, which is what we need."
Q: What resource do they decide to use?
--- 干扰: library database (reliable) | 答案: internet (more up-to-date)
```

### Implementation Rules

1. 每个选项至少要有一项正面特征
2. 判断标准必须清晰（为什么 Y 更好）
3. 问题必须明确指向评价性判断而非事实
4. 适用于 S3 的 MCQ 题型

### Common Mistakes

- ❌ 其中一个选项没有正面特征（很容易排除）
- ❌ 评价标准太主观（不可测试）
- ❌ 问题写得像事实题而非评价题

---

## 13. Conditional Rejection

### Description | 描述

说话人表示"如果条件满足，我会选 X，但由于条件不满足，我选 Y"。

### Cambridge Examples (paraphrased)

```
Example 1 — Budget Condition:
"I'd love to do the two-week course if I had more time, but since
I can only take a week off, I'll go with the one-week option."
--- 干扰: two-week course | 答案: one-week option

Example 2 — Weather Condition:
"We could have the event outdoors if the weather forecast improves,
but with rain predicted, the indoor hall is safer."
Q: Where will the event be held?
--- 干扰: outdoors | 答案: indoor hall

Example 3 — Experience Condition:
"If I had more experience in programming, I'd take the advanced
class, but given my background, the beginner one makes more sense."
--- 干扰: advanced | 答案: beginner
```

### Implementation Rules

1. 条件句必须有明确的 if-clause
2. 条件满足/不满足的理由必须清楚
3. 最终决定 Y 必须有至少一个支撑理由
4. 可适用于 S1、S3

### Common Mistakes

- ❌ 条件句太复杂（学生听不懂条件）
- ❌ "如果条件满足"和"但实际不满足"之间间隔太长
- ❌ 条件本身不清晰

---

## 14. Agreement with Reservation

### Description | 描述

说话人先表示同意（"Good point", "That's true", "I see what you mean"），然后提出 But/However。后面的内容是正确答案或关键意见。

### Cambridge Examples (paraphrased)

```
Example 1 — Research Approach:
A: I think we should focus on quantitative data.
B: That's a valid point, and the numbers would be useful.
However, I think qualitative data would give us more insight
into people's motivations.
Q: What type of data do they agree to focus on?
--- 干扰: quantitative (first suggestion, agreed valid)
| 答案: qualitative (with reservation)

Example 2 — Timeline:
A: Finishing by Friday seems doable.
B: Ideally yes, but we still have the analysis part which
usually takes at least two days.
--- 干扰: Friday (initially agreed) | 答案: (later date)
```

### Implementation Rules

1. 先要有明确的同意信号（不是直接否定）
2. But/However 后是重要信息
3. 适用于 S3 学术讨论
4. 此机制不适用于 S1（S1 通常不这么复杂）

### Common Mistakes

- ❌ 同意信号太弱，听起来像否定
- ❌ But 后的信息不清晰或和同意部分重叠
- ❌ 在 S1 中使用（不合适的场景）

---

## 15. Indirect Negation

### Description | 描述

说话人不直接说 "No"，而是礼貌/间接地表达否定。例如"It might be better to..."、"Why don't we..."、"Have you considered..." 等建议性语言蕴含了否定之前提议的意思。

### Cambridge Examples (paraphrased)

```
Example 1 — Indirect Rejection:
A: Should we interview the manager?
B: I wonder if it would be more useful to speak to the staff directly.
(含意: 不找经理，找员工)
--- 干扰: manager | 答案: staff

Example 2 — Subtle Change:
A: Let's start with the introduction.
B: Perhaps we should begin with the methodology, given our focus.
(含意: 不介绍，先从方法论开始)
--- 干扰: introduction | 答案: methodology

Example 3 — Alternative Suggestion:
A: I'll prepare the slides.
B: What if I do the slides and you handle the data analysis?
(含意: 我不做数据分析，我做幻灯片)
--- 干扰: slides (for A) | 答案: data analysis (for A)
```

### Implementation Rules

1. 否定不能通过"No"或"But"等直接信号词表达
2. 需要学生理解建议/问题的隐含否定含义
3. 常使用以下句式： "What if...", "Perhaps...", "Maybe we could...", "I wonder if..."
4. 难度较高，适合 6.5+ band
5. 主要用于 S3 的 复杂讨论

### Common Mistakes

- ❌ 间接否定太隐晦（学生完全听不懂）
- ❌ 间接否定太明显（听起来像直接否定）
- ❌ 在低分段题目中使用（不适合 5.5-6.0 水平）

---

## 跨 Section 使用建议 | Cross-Section Usage Guide

| 干扰机制 | S1 | S2 | S3 | S4 | 难度 |
|----------|:--:|:--:|:--:|:--:|:----:|
| 1. First Answer Rejected | ✅✅ | ✅ | ✅ | ❌ | 低 |
| 2. Correction | ✅✅ | ✅ | ✅ | ❌ | 低-中 |
| 3. Similar Item, Wrong Condition | ✅ | ✅✅ | ✅ | ✅ | 中 |
| 4. Number Correction | ✅✅ | ✅ | ❌ | ❌ | 低 |
| 5. Changed Preference | ✅✅ | ❌ | ✅✅ | ❌ | 低-中 |
| 6. Mentioned But Excluded | ✅ | ✅✅ | ✅ | ✅ | 中 |
| 7. Past vs Present Contrast | ❌ | ✅✅ | ❌ | ✅ | 中-高 |
| 8. Category vs Specific | ❌ | ✅ | ❌ | ✅✅ | 中 |
| 9. Clarification After Ambiguity | ✅✅ | ❌ | ✅ | ❌ | 低-中 |
| 10. Misleading Early Mention | ❌ | ✅ | ❌ | ✅✅ | 高 |
| 11. Hesitation + Self-Correction | ❌ | ❌ | ✅✅ | ❌ | 中-高 |
| 12. Comparative Evaluation | ❌ | ❌ | ✅✅ | ❌ | 中-高 |
| 13. Conditional Rejection | ✅ | ✅ | ✅✅ | ❌ | 中-高 |
| 14. Agreement with Reservation | ❌ | ❌ | ✅✅ | ❌ | 高 |
| 15. Indirect Negation | ❌ | ❌ | ✅✅ | ❌ | 高 |

图例: ✅✅ 非常常用 | ✅ 可用 | ❌ 不适用

---

*Document version: 1.0 · Last updated: 2026-05-17*
