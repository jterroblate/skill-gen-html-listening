#!/usr/bin/env python3
"""
Post-process S2 HTML: convert fill-type matching questions into click-to-place matching
with proper left-right layout (table-based, proven reliable).

Usage: python apply_matching.py <html_path> [--answers_json answers.json]
"""

import re, sys, json

POOL_DATA = {"A":"Cooking sessions","B":"Book sharing","C":"Music memory",
             "D":"Garden projects","E":"Photo albums","F":"Board games",
             "G":"Walking group","H":"Art classes"}
ANSWERS = {15:"E",16:"D",17:"G",18:"B",19:"C",20:"H"}
STEMS = {
    15:"involves looking at old photographs together",16:"helps with learning about plants and nature",
    17:"described as the easiest activity to start with",18:"participants bring something they have read recently",
    19:"particularly recommended for those who enjoy playing instruments",20:"requires the volunteer to have a specific skill",
}
SEGS = {15:"6",16:"7",17:"8",18:"9",19:"10",20:"11"}

MATCH_CSS = '''
.match-area{max-width:1280px;margin:0 auto;padding:0 8px}
.match-wrap{width:100%;border-collapse:collapse}
.match-wrap td{vertical-align:top}
.match-wrap td.left{padding-right:24px}
.match-wrap td.right{width:300px;min-width:280px}
.match-row{display:flex;align-items:center;gap:10px;padding:8px 12px;margin-bottom:8px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);font-size:13px;font-family:var(--ui-font)}
.match-row .ql{font-weight:700;color:var(--accent);min-width:24px;flex-shrink:0}
.match-row .qs{flex:1;line-height:1.5;min-width:0}
.match-slot{width:180px;min-height:34px;border:2px dashed var(--border);border-radius:6px;background:var(--bg);font-size:12px;font-weight:500;color:var(--text2);padding:4px 8px;cursor:pointer;text-align:center;line-height:1.5;flex-shrink:0;transition:all .15s}
.match-slot:hover{border-color:var(--accent);background:var(--accent-light)}
.match-slot.filled{border-style:solid;border-color:var(--accent);background:var(--accent-light);color:var(--text);font-weight:600}
.match-slot.correct{border-color:var(--success);background:#e6f4ea!important;color:var(--success)}
.match-slot.wrong{border-color:var(--error);background:#fef2f2!important;color:var(--error)}
.pool-title{font-size:12px;font-weight:600;color:var(--text2);font-family:var(--ui-font);margin-bottom:8px;text-align:center;letter-spacing:1px}
.match-pool{display:flex;flex-direction:column;gap:5px;padding:12px;background:var(--card);border:2px solid var(--border);border-radius:var(--radius)}
.match-opt{padding:7px 10px;border:2px solid var(--accent);border-radius:6px;cursor:pointer;font-size:12.5px;font-weight:600;background:var(--accent-light);color:var(--accent);user-select:none;font-family:var(--ui-font);text-align:center;transition:all .15s;white-space:nowrap}
.match-opt:hover{border-color:#c0664a;background:#fde4d4}
.match-opt.selected{border-color:var(--success);background:#e6f4ea;color:var(--success)}
.match-opt.used{opacity:.3;cursor:default;border-style:dashed;background:var(--sidebar);color:var(--text2)}
@media(max-width:750px){.match-wrap,.match-wrap tbody,.match-wrap tr,.match-wrap td{display:block}.match-wrap td.right{width:100%}}'''

MATCH_JS = '''
<script>
var poolData = POOL_PLACEHOLDER;
var selectedLetter = null;

function optClick(el) {
  if (el.classList.contains("used")) return;
  document.querySelectorAll(".match-opt.selected").forEach(function(o){o.classList.remove("selected");});
  if (selectedLetter === el.getAttribute("data-letter")) {
    selectedLetter = null; return;
  }
  el.classList.add("selected");
  selectedLetter = el.getAttribute("data-letter");
}

function slotClick(el) {
  var isFilled = el.classList.contains("filled");
  var slotL = el.getAttribute("data-letter");
  if (isFilled && selectedLetter && selectedLetter !== slotL) {
    var newOpt = document.querySelector('.match-opt[data-letter="' + selectedLetter + '"]');
    if (newOpt && !newOpt.classList.contains("used")) {
      var oldOpt = document.querySelector('.match-opt[data-letter="' + slotL + '"]');
      if (oldOpt) { oldOpt.classList.remove("used","selected"); }
      placeMatch(el, selectedLetter, newOpt);
      if (oldOpt) { oldOpt.classList.add("selected"); selectedLetter = slotL; }
      return;
    }
  }
  if (isFilled) {
    var oldL = slotL; var oldOpt = document.querySelector('.match-opt[data-letter="' + oldL + '"]');
    el.innerHTML = "\u2713 \u62d6\u62fd/\u70b9\u51fb";
    el.setAttribute("data-letter", ""); el.classList.remove("filled","correct","wrong");
    selectedLetter = null;
    if (oldOpt) { oldOpt.classList.remove("used","selected"); oldOpt.classList.add("selected"); selectedLetter = oldL; }
    return;
  }
  if (!selectedLetter) return;
  var opt = document.querySelector('.match-opt[data-letter="' + selectedLetter + '"]');
  if (!opt || opt.classList.contains("used")) return;
  placeMatch(el, selectedLetter, opt);
}

function placeMatch(el, letter, opt) {
  el.innerHTML = "<b>" + letter + ".</b> " + (poolData[letter] || letter);
  el.setAttribute("data-letter", letter); el.classList.add("filled"); el.classList.remove("correct","wrong");
  if (opt) { opt.classList.remove("selected"); opt.classList.add("used"); }
  selectedLetter = null;
}

var _ck = window.checkAnswers;
window.checkAnswers = function() {
  document.querySelectorAll(".match-slot").forEach(function(s) {
    var a = s.getAttribute("data-ans"), v = s.getAttribute("data-letter") || "";
    s.classList.remove("correct","wrong","filled");
    s.classList.add(v === a ? "correct" : "wrong");
  });
  if (_ck) _ck();
};
var _rv = window.revealAnswers;
window.revealAnswers = function() {
  document.querySelectorAll(".match-slot").forEach(function(s) {
    var a = s.getAttribute("data-ans");
    s.innerHTML = "<b>" + a + ".</b> " + (poolData[a] || a);
    s.setAttribute("data-letter", a); s.classList.add("correct","filled"); s.classList.remove("wrong");
  });
  if (_rv) _rv();
};
var _rs = window.resetAnswers;
window.resetAnswers = function() {
  document.querySelectorAll(".match-slot").forEach(function(s) {
    var l = s.getAttribute("data-letter");
    if (l) {
      var o = document.querySelector('.match-opt[data-letter="' + l + '"]');
      if (o) { o.classList.remove("used","selected"); }
    }
    s.innerHTML = "\u2713 \u62d6\u62fd/\u70b9\u51fb";
    s.setAttribute("data-letter", ""); s.classList.remove("filled","correct","wrong");
  });
  if (_rs) _rs();
};
</script>'''


def apply(html_path, pool=None, answers=None, stems=None, segs=None):
    if pool is None: pool = POOL_DATA
    if answers is None: answers = ANSWERS
    if stems is None: stems = STEMS
    if segs is None: segs = SEGS
    
    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    
    # 1. Remove old match CSS
    for target in ['.match-area','.match-wrap','.match-row','.match-slot','.match-opt','.pool-title','.match-pool','.match-item','.match-container',
                   '.match-left','.match-right','.match-wrapper','.match-pool{']:
        idx = html.find(target)
        if idx >= 0:
            # Find the full CSS rule (from { to matching })
            rule_start = html.find('{', idx) if '{' in html[idx:idx+50] else -1
            if rule_start >= 0:
                depth = 1
                pos = rule_start + 1
                while depth > 0 and pos < len(html):
                    if html[pos] == '{': depth += 1
                    elif html[pos] == '}': depth -= 1
                    pos += 1
                html = html[:idx] + html[pos:]
    
    # 2. Add new CSS
    html = html.replace('</style>', MATCH_CSS + '\n</style>', 1)
    
    # 3. Convert fill q-blocks to match type and extract segs
    match_blocks_removed = False
    for num in sorted(answers.keys(), reverse=True):
        ans = answers[num]
        seg_str = segs.get(str(num), str(num))
        old_attr = f'data-qtype="fill" data-ans="{ans}"'
        new_attr = f'data-qtype="match" data-ans="{ans}" data-num="{num}"'
        html = html.replace(old_attr, new_attr, 1)
        inp = f'<input class="fill-input" data-ans="{ans}" placeholder="..." autocomplete="off">'
        html = html.replace(inp, '', 1)
    
    # 4. Remove old q-blocks for match questions
    num_list = sorted(answers.keys())
    first = html.find(f'data-qtype="match" data-ans="{answers[num_list[0]]}"')
    last = html.rfind('data-qtype="match"')
    if first > 0 and last > 0:
        first_block = html.rfind('<div class="q-block"', 0, first)
        last_block_start = html.rfind('<div class="q-block"', 0, last)
        last_block_end = html.find('</div>', html.find('</div>', html.find('</div>', last_block_start) + 6) + 6) + 6
        old_blocks = html[first_block:last_block_end]
        
        # 5. Build new table layout
        left_rows = ''
        for num in num_list:
            ans = str(answers[num])
            seg = str(segs.get(str(num), str(num)))
            stem = stems[num]
            left_rows += (
                f'<div class="match-row"><div class="ql">Q{num}</div>'
                f'<div class="qs">{stem}</div>'
                f'<div class="match-slot" data-ans="{ans}" data-q="{num}" data-letter="" '
                f'onclick="slotClick(this)">\u2713 \u62d6\u62fd/\u70b9\u51fb</div>'
                f'<button class="seek-btn-inline" onclick="playSegment({seg})">\u25b6</button></div>\n'
            )
        
        pool_items = ''
        for letter, label in sorted(pool.items()):
            pool_items += f'<div class="match-opt" data-letter="{letter}" onclick="optClick(this)">{letter}. {label}</div>\n'
        
        match_html = (
            '<div class="match-area">\n'
            '<table class="match-wrap"><tr>'
            '<td class="left">\n' + left_rows + '</td>'
            '<td class="right">\n'
            '<div class="pool-title">\u9009\u9879\u6c60</div>\n'
            '<div class="match-pool" id="match-pool">\n' + pool_items + '</div>\n</td>'
            '</tr></table>\n</div>\n'
        )
        
        html = html[:first_block] + '\n' + match_html + '\n' + html[last_block_end:]
    
    # 6. Inject matching JS
    js = MATCH_JS.replace('POOL_PLACEHOLDER', json.dumps(pool, ensure_ascii=False))
    
    # Remove old matching JS if any
    for marker in ['(function(){','var poolData']:
        js_start = html.find(marker)
        if js_start >= 0 and 'optClick' in html[js_start:js_start+200]:
            # Find the closing </script>
            script_end = html.find('</script>', js_start)
            if script_end >= 0:
                script_end += 9
                html = html[:js_start] + html[script_end:]
    
    # Inject new JS
    html = html.replace('</body>', js + '\n</body>', 1)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 7. Verify
    checks = [
        ('match-area', 'match-area' in html),
        ('match-slot count', html.count('class="match-slot"') == len(answers) * 1),  # CSS + HTML
        ('match-opt count', html.count('class="match-opt"') == len(pool) * 1),  # CSS + HTML
        ('table layout', '<table' in html),
        ('optClick function', 'function optClick' in html),
        ('slotClick function', 'function slotClick' in html),
        ('checkAnswers patch', 'var _ck' in html),
        ('revealAnswers patch', 'var _rv' in html),
        ('resetAnswers patch', 'var _rs' in html),
    ]
    print(f"Applied matching to: {html_path}")
    for name, ok in checks:
        print(f"  {'✅' if ok else '❌'} {name}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        html_path = sys.argv[1]
        pool = POOL_DATA
        answers = ANSWERS
        
        if '--answers-json' in sys.argv:
            idx = sys.argv.index('--answers-json')
            data = json.load(open(sys.argv[idx + 1]))
            pool = data.get('pool', pool)
            answers = {int(k): v for k, v in data.get('answers', answers).items()}
        
        apply(html_path, pool, answers)
    else:
        print("Usage: python apply_matching.py <html_path> [--answers-json answers.json]")
