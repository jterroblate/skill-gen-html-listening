# Section Blueprint Template (Section 蓝图模板)
# Section Design Planning — Cambridge-Style Structured Outline

> 在生成任何听力内容之前，必须为每个 Section 填写此 Blueprint。
> Blueprint 是整个生成流程的第一步骤，决定题目质量。
> 每个 Section 一个文件，命名为 `blueprint_S1.md`, `blueprint_S2.md` 等。

---

## 模板 Template

```markdown
## Section Blueprint: [S1 / S2 / S3 / S4]

### 场景 | Scenario

| 项目 | 内容 |
|------|------|
| Scenario type | [accommodation / event / course / membership / travel / job / health / library / activity / venue / academic discussion / lecture] |
| Setting | [具体场景描述：地点、时间、背景] |
| Target band | [5.5-6.0 / 6.5-7.0 / 7.5-8.0] |
| Vocabulary level | [everyday / academic / mixed] |

### 对话/讲座设计 | Dialogue / Lecture Design

#### 人物 Speaker(s)

| Name | Role | Description |
|------|------|-------------|
| [姓名] | [角色] | [角色描述，如情绪、态度、口音] |
| [姓名] | [角色] | [角色描述] |

#### 结构 Structure

```
[Phase 1: ...]
[Phase 2: ...]
[Phase 3: ...]
[Phase 4: ...]
```

### 题目设计 | Question Design

| 项目 | 内容 |
|------|------|
| Total questions | [10] |
| Question types | [form completion / note completion / table completion / sentence completion / multiple choice / matching] |
| Answer types | [names / numbers / dates / nouns / opinions] |
| Word limit instruction | [ONE WORD ONLY / ONE WORD AND/OR A NUMBER / NO MORE THAN TWO WORDS] |

### 每题蓝图 | Per-Question Blueprint

#### Question 1

| 项目 | 内容 |
|------|------|
| Stem (题干) | [题目文本] |
| Expected answer | [答案] |
| Answer type | [name / number / date / noun / opinion / ...] |
| Word limit | [instruction] |
| Question type | [completion / MCQ / matching] |
| MCQ options | [A) ... B) ... C) ...] |
| Segment index | [N] |

##### Locator Strategy

| 项目 | 内容 |
|------|------|
| Locator signal | [什么词/短语/过渡触发答案出现] |
| Transcript trigger | [音频中定位答案的原文] |
| Answer support | [答案如何被呈现/确认] |
| Paraphrase relationship | [题干 ↔ 音频原文的转述映射] |

##### Distractor Plan (若适用)

| 项目 | 内容 |
|------|------|
| Distractor type | [correction / rejection / similar item / misleading mention / ...] |
| Mechanism | [具体如何误导] |
| Transcript distractor | [音频中干扰信息的原文] |
| Why it looks plausible | [为什么易错] |
| Why it's wrong | [为什么不是答案] |

##### Difficulty Notes

[题目难度分析，学生可能遇到的困难]

---

#### Question 2
[重复上述结构]
...

### 音频脚本设计 | Transcript Design

| Phase | Script | Duration | Functions |
|-------|--------|----------|-----------|
| Opening | [对话/讲座开场] | ~[X]s | Setup context |
| Body 1 | [信息段落1] | ~[X]s | Questions N-M |
| Body 2 | [信息段落2] | ~[X]s | Questions N-M |
| Body 3 | [信息段落3] | ~[X]s | Questions N-M |
| Closing | [结束语] | ~[X]s | Wrap up |

### 总体验证 | Overall Verification

| Checklist Item | Status |
|----------------|--------|
| 每个题目都有 clear locator | [✅ / ❌] |
| 每个题目都有 natural answer support | [✅ / ❌] |
| 每个题目都有 paraphrase | [✅ / ❌] |
| 每个题目都有 unique answer | [✅ / ❌] |
| 干扰多样化（至少3种机制） | [✅ / ❌] |
| 语速和难度符合 target band | [✅ / ❌] |
| 对话/独白自然流畅 | [✅ / ❌] |
| 所有 quality gates 通过 | [✅ / ❌] |
```

---

## Blueprint 示例 (Example: S1)

```markdown
## Section Blueprint: S1

### 场景 | Scenario

| 项目 | 内容 |
|------|------|
| Scenario type | Event registration |
| Setting | 某社区中心报名参加夏季音乐节 |
| Target band | 5.5-6.0 |
| Vocabulary level | everyday |

### 对话设计

#### 人物

| Name | Role | Description |
|------|------|-------------|
| Anna | Festival coordinator | 友善、有条理、英式英语 |
| Tom | Applicant | 有些犹豫、不确定细节 |

#### 结构

```
Opening: Anna 接电话问候 → Tom 说明来意
Body:
  Q1-Q2: 活动选择和日期（first suggestion rejected）
  Q3-Q4: 个人信息和联系方式（spelling clarification）
  Q5-Q6: 费用和支付方式（number correction）
  Q7-Q8: 额外服务选择（changed preference）
  Q9-Q10: 确认和时间安排（clarification）
Closing: 总结信息 → 道别
```

### 题目设计

| 项目 | 内容 |
|------|------|
| Total questions | 10 |
| Question types | Form completion |
| Answer types | names, numbers, dates, simple nouns |
| Word limit instruction | ONE WORD AND/OR A NUMBER |

### 每题蓝图

#### Question 1

| 项目 | 内容 |
|------|------|
| Stem | Name of event: \_\_\_\_\_\_\_\_ |
| Expected answer | Summer Festival |
| Answer type | noun phrase |
| Word limit | ONE WORD AND/OR A NUMBER |

##### Locator Strategy

| 项目 | 内容 |
|------|------|
| Locator signal | "I'm interested in joining your summer..." |
| Transcript trigger | "Let me check... we have the Summer Festival in August." |
| Answer support | 首次提及后，Tom确认"Yes, that one" |
| Paraphrase | Stem: "Name of event" ↔ Transcript: "Summer Festival" |

##### Distractor Plan

| 项目 | 内容 |
|------|------|
| Distractor type | First Suggested Rejected |
| Transcript distractor | Tom 先问 "Is it the Music Day event?" → Anna: "No, that was last month" |
| Why it looks plausible | 这是合理的活动名称 |
| Why it's wrong | 被明确否定了 "That was last month" |

### 音频脚本设计

| Phase | Script | Duration | Functions |
|-------|--------|----------|-----------|
| Opening | Anna: Hello, City Community Centre... | ~15s | Setup |
| Body | Anna 介绍活动 → Tom 选择 → ... | ~120s | Q1-Q10 |
| Closing | Anna 确认所有信息 → 道别 | ~15s | Wrap up |
```

---

## Blueprint For Each Section Type

### S2 Blueprint Focus

```
重点：
- 总-分结构：介绍 1-2句 → Part A → Part B → Part C → 简要总结
- 信息密度：每10秒1个信息点
- 题型偏好：matching (6题) + completion (4题) 或 全completion
- 无明显Q-A格式，信息自然嵌入说明中
```

### S3 Blueprint Focus

```
重点：
- 观点碰撞：至少2次 disagreement/reformulation
- 讨论类型：至少2种（比较、评估、分析、建议等）
- 语言特征：hesitation, self-correction, reservation
- 题型偏好：MCQ + Choose TWO + matching
- 每题需要听懂 opinions/reasons/evaluations，非factual lookup
```

### S4 Blueprint Focus

```
重点：
- Lecture structure: intro → background → main topic → subtopics → conclusion
- 信号词规划：每段开头用topic signal
- 答案类型：abstract nouns, processes, causes/effects
- 不能有专有名词答案
- 每题需要 paraphrase（答案不会在stem中用原词出现）
```

---

## 使用方法 | How to Use

1. 复制此模板到 `blueprints/` 目录，命名为 `blueprint_S1.md` 等
2. 填写所有内容
3. 在每个 section 生成前，必须先完成此 blueprint
4. 使用 `listening_question_quality_gates.md` 验证
5. 通过后才能进入脚本写作阶段

---

*Document version: 1.0 · Last updated: 2026-05-17*
