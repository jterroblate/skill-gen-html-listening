# Listening Player Architecture Reference

## Dual-Panel Model

The listening player uses a **single audio source** with **two view panels**.
Panel switching is instant (no page load) via CSS class toggling.

### Component Tree

```
Page
├── Tab Bar (.tab-bar)
│   ├── .tab-btn "刷题" → switchMode(0)
│   └── .tab-btn "精听" → switchMode(1)
├── Player Bar (.player-bar)
│   ├── <audio> (shared)
│   └── .time (clock display)
└── Content (.content)
    ├── #panel_0 (刷题)
    │   ├── Section title
    │   ├── .q-block × N
    │   │   ├── .q-text (question + <input>)
    │   │   └── .seek-btn-inline (▶ 跳至音频)
    │   └── .action-bar
    │       ├── .btn-primary (提交答案)
    │       ├── .btn-secondary (显示答案/重置)
    │       └── .score-badge
    └── #panel_1 (精听)
        └── #transcriptContainer
            └── .sentence × M
                ├── .speaker (label)
                └── text content
```

## Question Block Structure

Each `q-block` wraps one question:

```html
<div class="q-block" data-seg="3">        <!-- seg = audio segment index -->
  <div class="q-text">
    <span class="q-num">1.</span>
    Course code:
    <input class="fill-input" data-ans="WTM-2026" style="width:110px">
  </div>
  <button class="seek-btn-inline" onclick="playSegment(3)">▶ 跳至音频</button>
</div>
```

### data-seg Attribute
Links question to the segment where the answer is mentioned.
The playSegment() call reads `segments[data-seg].start` to seek.

## Audio Timing

The `segments` array is the backbone of sync:

```javascript
const segments = [
  {"file": "000.mp3", "start": 0.0,   "end": 4.32,  "duration": 4.32},
  {"file": "001.mp3", "start": 4.32,  "end": 15.8,  "duration": 11.48},
  ...
];
```

### How Sync Works
1. `timeupdate` event fires ~4 times/second
2. `onTimeUpdate()` checks: `currentTime >= segments[i].start`
3. Iterates from end to find the last matching segment
4. Calls `highlightSegment(i)` if different from current
5. Updates `.active` / `.played` classes on all sentence elements

### Performance Note
The O(n) scan is fine for 20-50 segments. Beyond 100 segments, use binary search.

## Answer Marking

### Correct → Green
```javascript
inp.classList.add("correct");           // green underline text
block.style.borderLeft = "4px solid #2d8659";  // green left border
```

### Wrong → Red
```javascript
inp.classList.add("wrong");             // red underline text
block.style.borderLeft = "4px solid #c0392b";  // red left border
```

## Scroll Behavior
When highlighting a segment, the active sentence is scrolled into view:
```javascript
el.scrollIntoView({block: "center", behavior: "smooth"});
```
This ensures the user always sees the current sentence in the middle of the panel.

## browser Caching Issue
Opening local `.html` files in Chrome may show cached versions even after file modification.
Solutions:
1. Rename file (e.g., `_v2.html`) to force reload
2. Copy to Desktop with English name, open with `open -a "Google Chrome" --args --disable-cache`
3. Clear browser cache for `file://` protocol

## Chinese Path Handling
Always use shell commands to move files when paths contain Chinese characters:
```bash
DEST="/path/with/中文 and spaces/刷题.html"
cp /tmp/source.html "$DEST"
```
NEVER use `shutil.copy2`, `os.remove`, or `open(path, 'w')` with Chinese paths from Python.
