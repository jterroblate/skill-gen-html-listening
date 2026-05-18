#!/usr/bin/env python3
"""
Generate IELTS listening practice HTML with 刷题/精听 dual-mode player.

Supports 3 question types:
  - fill: text input with answer match (S1, S4)
  - mcq_single: radio buttons, A/B/C (S2, S3)
  - mcq_multi: checkboxes, select TWO from A-E (S2, S3)

Usage:
  python generate_player.py \
    --title "IELTS Listening · U01 Daily Rhythm" \
    --output "/path/to/刷题.html" \
    --mp3 "U01_日常节奏_听力_S1.mp3" \
    --timing timing.json \
    --questions questions.json \
    --sentences sentences.json \
    --q-seg q_to_seg.json
"""

import json, sys, os
import argparse

# ──────────────────────────────────────────────
#  Question type helpers
# ──────────────────────────────────────────────

def render_fill(num, text, seg, answer=""):
    """Fill-in: <input> with data-ans.
    Replaces _____ with an input field, or appends one at the end.
    """
    import re
    blank = '<input class="fill-input" data-ans="%s" placeholder="..." autocomplete="off">' % answer
    if '_____' in text:
        filled = text.replace('_____', blank, 1)
    else:
        filled = text + ' ' + blank
    return f'''<div class="q-block" data-seg="{seg}" data-qtype="fill" data-ans="{answer}">
<div class="q-text"><span class="q-num">{num}.</span> {filled}</div>
<button class="seek-btn-inline" onclick="playSegment({seg})">▶ 跳至音频</button>
</div>'''


def render_notes_layout(layout, questions_by_num):
    """Render S4 notes as structured hierarchical document.
    layout: dict with title + sections[]. Each section has heading + lines[].
    lines have type "label" (no blank) or "blank" (text with {Q} markers).
    questions_by_num: dict mapping qnum -> {answer, seg}
    """
    import re
    html = '<div class="notes-container">'
    
    if layout.get("title"):
        html += f'<div class="notes-title">{layout["title"]}</div>'
    
    for sec in layout.get("sections", []):
        html += f'<div class="notes-heading">{sec.get("heading", "")}</div>'
        for line in sec.get("lines", []):
            lt = line.get("type", "blank")
            text = line.get("text", "")
            
            if lt == "label":
                html += f'<div class="notes-label">{text}</div>'
            elif lt == "blank":
                # Replace {Q} markers with input fields
                def replace_q(m):
                    qnum = int(m.group(1))
                    info = questions_by_num.get(qnum, {})
                    ans = info.get("answer", "")
                    seg = info.get("seg", 0)
                    q_class = "notes-blank"
                    inp = f'<input class="fill-input notes-fill" data-ans="{ans}" data-q="{qnum}" placeholder="..." autocomplete="off">'
                    return f'{inp}'
                
                filled = re.sub(r'\{(\d+)\}', replace_q, text)
                html += f'<div class="notes-line">{filled}</div>'
        
        # Add seek buttons for this section
        html += '<div class="notes-actions">'
        for line in sec.get("lines", []):
            if line.get("type") == "blank":
                for m in re.finditer(r'\{(\d+)\}', line.get("text", "")):
                    qnum = int(m.group(1))
                    seg = questions_by_num.get(qnum, {}).get("seg", 0)
                    html += f'<button class="seek-btn-notes" onclick="playSegment({seg})" title="Q{qnum}">🔊 Q{qnum}</button>'
        html += '</div>'
    
    html += '</div>'
    return html

def render_mcq_single(num, stem, options, answer, seg):
    """Single-select radio buttons (A/B/C)."""
    opts_html = ""
    for letter, option_text in options.items():
        opts_html += f'''<label class="mcq-opt"><input type="radio" name="q{num}" value="{letter}" onchange="optionChanged(this)"><span class="mcq-letter">{letter}.</span> {option_text}</label>\n'''
    return f'''<div class="q-block" data-seg="{seg}" data-qtype="mcq_single" data-ans="{answer}" data-num="{num}">
<div class="q-text"><span class="q-num">{num}.</span> {stem}</div>
<div class="mcq-opts">{opts_html}</div>
<button class="seek-btn-inline" onclick="playSegment({seg})">▶ 跳至音频</button>
</div>'''

def render_mcq_multi(num_label, stem, options, answers, seg):
    """Multi-select checkboxes (Choose TWO etc). answers = list of correct letters."""
    ans_str = ",".join(sorted(answers))
    opts_html = ""
    for letter, option_text in options.items():
        opts_html += f'''<label class="mcq-opt"><input type="checkbox" name="multi_{num_label}" value="{letter}"><span class="mcq-letter">{letter}.</span> {option_text}</label>\n'''
    return f'''<div class="q-block" data-seg="{seg}" data-qtype="mcq_multi" data-ans="{ans_str}" data-num="{num_label}">
<div class="q-text"><span class="q-num">{num_label}.</span> {stem}</div>
<div class="mcq-opts">{opts_html}</div>
<button class="seek-btn-inline" onclick="playSegment({seg})">▶ 跳至音频</button>
</div>'''

# ──────────────────────────────────────────────
#  HTML builder
# ──────────────────────────────────────────────

def build_html(title, mp3_path, timing, questions, sentences, q_seg, notes_layout=None):
    segments_json = json.dumps(timing["segments"])
    total_sec = int(timing.get("total_duration", timing["segments"][-1]["end"]))
    total_min = total_sec // 60
    total_s = total_sec % 60
    time_str = f"{total_min}:{total_s:02d}"
    
    s_js = json.dumps(sentences, ensure_ascii=False)
    
    # Build questions lookup for notes
    questions_by_num = {}
    for q in questions:
        qnum = q["num"]
        questions_by_num[qnum] = {
            "answer": q.get("answer", ""),
            "seg": q.get("seg", q_seg.get(str(qnum), 0)),
        }
    
    # Render questions
    layout_notes = ""
    if notes_layout:
        layout_notes = render_notes_layout(notes_layout, questions_by_num)
    
    q_blocks = []
    for q in questions:
        qtype = q.get("type", "fill")
        num = q["num"]
        seg = q.get("seg", q_seg.get(str(num) if not isinstance(num, str) else num, 0))
        
        if notes_layout:
            # In notes mode, still render hidden q-blocks for JS grading
            # but hide them visually; notes layout handles display
            q_blocks.append(render_fill(num, q["text"], seg, q.get("answer", "")))
        elif qtype == "mcq_single":
            q_blocks.append(render_mcq_single(num, q["stem"], q["options"], q["answer"], seg))
        elif qtype == "mcq_multi":
            q_blocks.append(render_mcq_multi(num, q["stem"], q["options"], q["answer"], seg))
        else:
            q_blocks.append(render_fill(num, q["text"], seg, q.get("answer", "")))
    
    q_html = "\n".join(q_blocks)
    
    # ── CSS ──
    mcq_css = '''
.mcq-opts{margin:6px 0 2px 0}.mcq-opt{display:flex;align-items:center;gap:6px;padding:5px 8px;margin:2px 0;border-radius:4px;cursor:pointer;font-size:13px;transition:.15s;font-family:var(--ui-font)}
.mcq-opt:hover{background:var(--sidebar)}
.mcq-opt input[type="radio"],.mcq-opt input[type="checkbox"]{accent-color:var(--accent);cursor:pointer;width:14px;height:14px;flex-shrink:0}
.mcq-letter{font-weight:600;color:var(--accent);min-width:18px}
.mcq-correct{background:#e6f4ea!important;border-left:3px solid var(--success)}
.mcq-correct .mcq-letter{color:var(--success)}
.mcq-wrong{background:#fde8e8!important;border-left:3px solid var(--error)}
.mcq-wrong .mcq-letter{color:var(--error)}'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root{{--bg:#faf8f7;--card:#fffcf9;--sidebar:#f5f0eb;--text:#3a3a3a;--text2:#7a7a7a;--accent:#d97757;--accent-light:#fef0e8;--success:#2d8659;--error:#c0392b;--border:#e8ddd5;--radius:8px;--font:Georgia,'Times New Roman',serif;--ui-font:-apple-system,'Helvetica Neue','PingFang SC',sans-serif}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);line-height:1.7;height:100vh;overflow:hidden}}
.tab-bar{{background:var(--card);border-bottom:1px solid var(--border);display:flex;position:sticky;top:0;z-index:20}}
.tab-btn{{flex:1;padding:14px 6px;border:none;background:none;cursor:pointer;font-size:12px;font-family:var(--ui-font);color:var(--text2);border-bottom:3px solid transparent;transition:.2s;text-align:center}}
.tab-btn:hover{{color:var(--accent)}}.tab-btn.active{{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}}
.player-bar{{background:var(--card);border-bottom:1px solid var(--border);padding:10px 24px;display:flex;align-items:center;gap:12px}}
.player-bar audio{{flex:1;height:40px}}
.player-bar .speed{{font-size:13px;font-weight:600;color:var(--accent);font-family:var(--ui-font);min-width:36px;text-align:center;cursor:pointer;user-select:none}}
.player-bar .time{{font-size:12px;color:var(--text2);font-family:var(--ui-font);min-width:80px}}
.content{{display:flex;height:calc(100vh - 145px);overflow:hidden}}
.panel{{display:none;overflow-y:auto;padding:24px;width:100%}}
.panel.active{{display:block}}
.sentence{{padding:8px 14px;margin:2px 0;border-radius:var(--radius);cursor:pointer;font-size:14px;line-height:1.7;transition:.2s;background:var(--card)}}
.sentence:hover{{background:var(--sidebar)}}
.sentence.active{{background:var(--accent);color:#fff}}
.sentence.played{{opacity:.5}}
.sentence .speaker{{font-weight:600;color:var(--accent);margin-right:6px;font-family:var(--ui-font)}}
.sentence.active .speaker{{color:#fff}}
.q-block{{margin-bottom:14px;padding:14px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);transition:.3s}}
.q-num{{font-weight:600;color:var(--accent);margin-right:6px;font-family:var(--ui-font)}}
.q-text{{font-size:13.5px;font-family:var(--ui-font);margin-bottom:5px}}
.fill-input{{border:none;border-bottom:2px solid var(--border);padding:4px 8px;font-size:13px;font-family:var(--ui-font);background:transparent;margin:0 2px;display:inline}}
.fill-input:focus{{border-bottom-color:var(--accent);outline:none}}
.fill-input.correct{{border-bottom-color:var(--success);color:var(--success)}}
.fill-input.wrong{{border-bottom-color:var(--error);color:var(--error)}}
{mcq_css}
.seek-btn-inline{{display:inline-block;padding:2px 8px;margin-left:6px;border:1px solid var(--accent);border-radius:4px;background:none;cursor:pointer;font-size:10.5px;color:var(--accent);font-family:var(--ui-font);transition:.15s;vertical-align:middle;white-space:nowrap}}
.notes-container .q-block{{display:none!important}}
.notes-container{{padding:8px 0 16px 0}}
.notes-title{{font-size:15px;font-weight:700;color:var(--text);font-family:var(--ui-font);margin-bottom:14px;padding-bottom:6px;border-bottom:2px solid var(--accent)}}
.notes-heading{{font-size:13px;font-weight:600;color:var(--accent);font-family:var(--ui-font);margin:14px 0 6px 0;padding:4px 0}}
.notes-label{{font-size:12px;color:var(--text2);font-family:var(--ui-font);margin:4px 0 2px 8px}}
.notes-line{{font-size:13px;font-family:var(--ui-font);padding:6px 10px;margin:3px 0;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);line-height:1.9}}
.notes-fill{{border-bottom-width:2px!important;padding:2px 6px!important;font-size:13px!important}}
.notes-actions{{display:flex;gap:4px;margin:6px 0 8px 12px;flex-wrap:wrap}}
.seek-btn-notes{{padding:2px 8px;border:1px solid var(--border);border-radius:4px;background:none;cursor:pointer;font-size:10px;color:var(--accent);font-family:var(--ui-font);transition:.15s}}
.seek-btn-notes:hover{{background:var(--accent);color:#fff}}
.seek-btn-inline:hover{{background:var(--accent);color:#fff}}
.action-bar{{background:var(--card);border-top:1px solid var(--border);padding:10px 24px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;position:sticky;bottom:0;z-index:10}}
.btn{{padding:7px 16px;border:none;border-radius:var(--radius);cursor:pointer;font-size:12.5px;font-family:var(--ui-font);font-weight:500;transition:.2s}}
.btn-primary{{background:var(--accent);color:#fff}}.btn-primary:hover{{opacity:.85}}
.btn-secondary{{background:var(--sidebar);color:var(--text);border:1px solid var(--border)}}
.btn:disabled{{opacity:.4;cursor:default}}
.score-badge{{font-size:13px;font-family:var(--ui-font);color:var(--text2);margin-left:auto}}
.score-badge strong{{color:var(--text)}}
@media(max-width:900px){{.content{{flex-direction:column}}}}
</style>
</head>
<body>

<div class="tab-bar">
  <button class="tab-btn active" onclick="switchMode(0)">刷题</button>
  <button class="tab-btn" onclick="switchMode(1)">精听</button>
</div>

<div class="player-bar">
  <audio id="audioPlayer" controls ontimeupdate="onTimeUpdate()">
    <source src="{mp3_path}" type="audio/mpeg">
  </audio>
  <span class="speed" id="speedDisplay" onclick="cycleSpeed()">1.0x</span>
  <span class="time" id="timeDisplay">0:00 / {time_str}</span>
</div>

<div class="content">

<div class="panel active" id="panel_0">
<div style="font-size:15px;font-weight:600;margin-bottom:16px;color:var(--accent);font-family:var(--ui-font)">{title}</div>

{layout_notes}

{q_html}

<div class="action-bar">
  <button class="btn btn-primary" onclick="checkAnswers()">✅ 提交答案</button>
  <button class="btn btn-secondary" onclick="revealAnswers()">💡 显示答案</button>
  <button class="btn btn-secondary" onclick="resetAnswers()">🔄 重置</button>
  <span class="score-badge" id="scoreDisplay"></span>
</div>
</div>

<div class="panel" id="panel_1">
<div style="font-size:15px;font-weight:600;margin-bottom:6px;color:var(--accent);font-family:var(--ui-font)">Close Listening — Sentence by Sentence</div>
<div style="font-size:12px;color:var(--text2);margin-bottom:14px">Click any sentence to play from that point.</div>
<div id="transcriptContainer"></div>
</div>

</div>

<script>
const segments = {segments_json};

const sentences = {s_js};

var audio = document.getElementById("audioPlayer");
var currentSegment = -1;
var speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0];
var speedIdx = 2;

function updateSpeedDisplay() {{
  document.getElementById("speedDisplay").textContent = speeds[speedIdx].toFixed(2).replace(/0$/, "").replace(/\.0$/, ".0") + "x";
}}

function cycleSpeed() {{
  speedIdx = (speedIdx + 1) % speeds.length;
  audio.playbackRate = speeds[speedIdx];
  updateSpeedDisplay();
}}

// Build transcript
var container = document.getElementById("transcriptContainer");
sentences.forEach(function(s, i) {{
  var div = document.createElement("div");
  div.className = "sentence";
  div.setAttribute("data-index", i);
  div.innerHTML = '<span class="speaker">[' + s.speaker + ']</span>' + s.text;
  div.onclick = function() {{ playFrom(i); }};
  container.appendChild(div);
}});

function playFrom(index) {{
  if (index < 0 || index >= segments.length) return;
  audio.currentTime = segments[index].start;
  audio.play();
  highlightSegment(index);
}}

function highlightSegment(index) {{
  var all = document.querySelectorAll(".sentence");
  for (var i = 0; i < all.length; i++) {{
    if (i === index) all[i].classList.add("active");
    else all[i].classList.remove("active");
    if (i < index) all[i].classList.add("played");
    else all[i].classList.remove("played");
  }}
  currentSegment = index;
  var el = document.querySelector('.sentence[data-index="' + index + '"]');
  if (el) el.scrollIntoView({{block:"center",behavior:"smooth"}});
}}

function onTimeUpdate() {{
  var ct = audio.currentTime;
  var m = Math.floor(ct / 60);
  var s = Math.floor(ct % 60);
  document.getElementById("timeDisplay").textContent = m + ":" + (s < 10 ? "0" : "") + s + " / {time_str}";
  for (var i = segments.length - 1; i >= 0; i--) {{
    if (ct >= segments[i].start) {{
      if (i !== currentSegment) highlightSegment(i);
      break;
    }}
  }}
}}

function switchMode(mode) {{
  var tabs = document.querySelectorAll(".tab-btn");
  var panels = document.querySelectorAll(".panel");
  for (var i = 0; i < tabs.length; i++) tabs[i].classList.remove("active");
  for (var j = 0; j < panels.length; j++) panels[j].classList.remove("active");
  tabs[mode].classList.add("active");
  document.getElementById("panel_" + mode).classList.add("active");
}}

function checkAnswers() {{
  var correct = 0, total = 0;
  var blocks = document.querySelectorAll(".q-block");
  for (var i = 0; i < blocks.length; i++) {{
    total++;
    var b = blocks[i];
    var qtype = b.getAttribute("data-qtype");
    var result = false;
    if (qtype === "fill") {{
      var inp = b.querySelector(".fill-input");
      if (!inp) continue;
      var ans = inp.getAttribute("data-ans");
      var val = inp.value.trim().toLowerCase();
      result = (val === ans.toLowerCase());
      if (result) {{
        inp.classList.add("correct"); inp.classList.remove("wrong");
      }} else {{
        inp.classList.add("wrong"); inp.classList.remove("correct");
      }}
    }} else if (qtype === "mcq_single") {{
      var selected = b.querySelector('input[type="radio"]:checked');
      result = selected && selected.value === b.getAttribute("data-ans");
      var opts = b.querySelectorAll(".mcq-opt");
      for (var oi = 0; oi < opts.length; oi++) {{
        opts[oi].classList.remove("mcq-correct","mcq-wrong");
        var inp2 = opts[oi].querySelector("input");
        if (result) {{
          if (inp2.checked) opts[oi].classList.add("mcq-correct");
        }} else {{
          if (inp2.checked) opts[oi].classList.add("mcq-wrong");
        }}
      }}
    }} else if (qtype === "mcq_multi") {{
      var checkedEls = b.querySelectorAll('input[type="checkbox"]:checked');
      var checkedVals = [];
      for (var ci = 0; ci < checkedEls.length; ci++) {{
        checkedVals.push(checkedEls[ci].value);
      }}
      checkedVals.sort();
      var correctAns = b.getAttribute("data-ans").split(",").sort();
      result = (checkedVals.length === correctAns.length && checkedVals.every(function(v,j) {{ return v === correctAns[j]; }}));
      var opts2 = b.querySelectorAll(".mcq-opt");
      for (var oi2 = 0; oi2 < opts2.length; oi2++) {{
        opts2[oi2].classList.remove("mcq-correct","mcq-wrong");
        var inp3 = opts2[oi2].querySelector("input");
        if (inp3.checked) {{
          opts2[oi2].classList.add(result ? "mcq-correct" : "mcq-wrong");
        }}
      }}
    }}
    if (result) {{
      b.style.borderLeft = "4px solid #2d8659";
      correct++;
    }} else {{
      b.style.borderLeft = "4px solid #c0392b";
    }}
  }}
  document.getElementById("scoreDisplay").innerHTML = "<strong>" + correct + "/" + total + "</strong> correct";
}}

function revealAnswers() {{
  var blocks = document.querySelectorAll(".q-block");
  for (var i = 0; i < blocks.length; i++) {{
    var b = blocks[i];
    var qtype = b.getAttribute("data-qtype");
    if (qtype === "fill") {{
      var inp = b.querySelector(".fill-input");
      if (!inp) continue;
      inp.value = inp.getAttribute("data-ans");
      inp.classList.add("correct"); inp.classList.remove("wrong");
      b.style.borderLeft = "4px solid #2d8659";
    }} else if (qtype === "mcq_single") {{
      var ans = b.getAttribute("data-ans");
      var radios = b.querySelectorAll('input[type="radio"]');
      for (var ri = 0; ri < radios.length; ri++) {{
        radios[ri].checked = (radios[ri].value === ans);
      }}
      var opts = b.querySelectorAll(".mcq-opt");
      for (var oi = 0; oi < opts.length; oi++) {{
        opts[oi].classList.remove("mcq-correct","mcq-wrong");
        if (opts[oi].querySelector("input").checked) opts[oi].classList.add("mcq-correct");
      }}
      b.style.borderLeft = "4px solid #2d8659";
    }} else if (qtype === "mcq_multi") {{
      var ansList = b.getAttribute("data-ans").split(",");
      var chks = b.querySelectorAll('input[type="checkbox"]');
      for (var ci = 0; ci < chks.length; ci++) {{
        chks[ci].checked = ansList.indexOf(chks[ci].value) >= 0;
      }}
      var opts2 = b.querySelectorAll(".mcq-opt");
      for (var oi2 = 0; oi2 < opts2.length; oi2++) {{
        opts2[oi2].classList.remove("mcq-correct","mcq-wrong");
        if (opts2[oi2].querySelector("input").checked) opts2[oi2].classList.add("mcq-correct");
      }}
      b.style.borderLeft = "4px solid #2d8659";
    }}
  }}
}}

function resetAnswers() {{
  var blocks = document.querySelectorAll(".q-block");
  for (var i = 0; i < blocks.length; i++) {{
    var b = blocks[i];
    var qtype = b.getAttribute("data-qtype");
    b.style.borderLeft = "";
    if (qtype === "fill") {{
      var inp = b.querySelector(".fill-input");
      if (inp) {{ inp.value = ""; inp.classList.remove("correct","wrong"); }}
    }} else {{
      var inputs = b.querySelectorAll("input");
      for (var ii = 0; ii < inputs.length; ii++) inputs[ii].checked = false;
      var opts = b.querySelectorAll(".mcq-opt");
      for (var oi = 0; oi < opts.length; oi++) opts[oi].classList.remove("mcq-correct","mcq-wrong");
    }}
  }}
  document.getElementById("scoreDisplay").innerHTML = "";
}}

function playSegment(idx) {{
  if (audio) {{
    audio.currentTime = segments[idx].start;
    audio.play();
  }}
}}

function optionChanged(el) {{
  // Clear styling when option changes
  var block = el.closest(".q-block");
  block.style.borderLeft = "";
  var opts = block.querySelectorAll(".mcq-opt");
  for (var i = 0; i < opts.length; i++) opts[i].classList.remove("mcq-correct","mcq-wrong");
}}

audio.addEventListener("play", function() {{ onTimeUpdate(); }});

document.addEventListener("keydown", function(e) {{
  if (e.key === " " || e.code === "Space") {{
    e.preventDefault();
    if (audio.paused) audio.play();
    else audio.pause();
  }} else if (e.key === "ArrowLeft") {{
    e.preventDefault();
    if (currentSegment > 0) playFrom(currentSegment - 1);
  }} else if (e.key === "ArrowRight") {{
    e.preventDefault();
    if (currentSegment < segments.length - 1) playFrom(currentSegment + 1);
  }} else if (e.key === "ArrowUp") {{
    e.preventDefault();
    if (speedIdx < speeds.length - 1) speedIdx++;
    audio.playbackRate = speeds[speedIdx];
    updateSpeedDisplay();
  }} else if (e.key === "ArrowDown") {{
    e.preventDefault();
    if (speedIdx > 0) speedIdx--;
    audio.playbackRate = speeds[speedIdx];
    updateSpeedDisplay();
  }}
}});
</script>
</body>
</html>'''
    return html

def main():
    parser = argparse.ArgumentParser(description="Generate IELTS listening practice HTML")
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--mp3", required=True)
    parser.add_argument("--timing", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--sentences", required=True)
    parser.add_argument("--q-seg", required=True)
    parser.add_argument("--notes-layout", default=None)
    
    args = parser.parse_args()
    
    with open(args.timing) as f: timing = json.load(f)
    with open(args.questions) as f: questions = json.load(f)
    with open(args.sentences) as f: sentences = json.load(f)
    with open(args.q_seg) as f: q_seg = json.load(f)
    
    notes_layout = None
    if args.notes_layout and os.path.exists(args.notes_layout):
        with open(args.notes_layout) as f:
            notes_layout = json.load(f)
    
    html = build_html(args.title, args.mp3, timing, questions, sentences, q_seg, notes_layout)
    
    tmp_path = "/tmp/ielts_player_output.html"
    with open(tmp_path, "w") as f:
        f.write(html)
    
    import subprocess
    subprocess.run(["cp", tmp_path, args.output])
    
    size = len(html)
    fn_count = sum(1 for fn in ["playFrom","highlightSegment","onTimeUpdate","switchMode","checkAnswers","revealAnswers","resetAnswers","playSegment","cycleSpeed","updateSpeedDisplay"] if fn in html)
    print(f"Generated: {args.output}\nSize: {size:,} bytes\nFunctions: {fn_count}/10")

if __name__ == "__main__":
    main()
