#!/usr/bin/env python3
"""
Post-process S2 HTML to add drag-and-drop matching with left-right layout.

Usage: python apply_matching.py <html_path>
"""
import re, sys

POOL_DATA = {"A":"Cooking sessions","B":"Book sharing","C":"Music memory",
             "D":"Garden projects","E":"Photo albums","F":"Board games",
             "G":"Walking group","H":"Art classes"}
ANSWERS = {15:"E",16:"D",17:"G",18:"B",19:"C",20:"H"}

MATCH_CSS = '''
.match-container{display:flex;gap:20px;padding:8px 0}
.match-left{flex:1;min-width:0}
.match-right{width:260px;flex-shrink:0;position:sticky;top:8px;align-self:flex-start}
.match-right .pool-title{font-size:11px;font-weight:600;color:var(--text2);font-family:var(--ui-font);margin-bottom:6px;text-align:center}
.match-pool{display:flex;flex-direction:column;gap:4px;padding:10px;background:var(--card);border:2px solid var(--border);border-radius:var(--radius)}
.match-item{padding:6px 10px;border:2px solid var(--accent);border-radius:6px;cursor:grab;font-size:12px;font-weight:600;background:var(--accent-light);color:var(--accent);user-select:none;font-family:var(--ui-font);text-align:center}
.match-item:hover{border-color:#c0664a;background:#fde4d4}
.match-item.dragging{opacity:.4}
.match-item.used{opacity:.35;cursor:default;border-style:dashed;background:var(--sidebar);color:var(--text2)}
.match-slot{display:block;min-height:38px;border:2px dashed var(--border);border-radius:6px;background:var(--card);font-size:12px;font-weight:600;color:var(--text);font-family:var(--ui-font);padding:6px 10px;cursor:default;text-align:center;line-height:1.6}
.match-slot.dragover{border-color:var(--accent);background:var(--accent-light)}
.match-slot.filled{border-style:solid;border-color:var(--accent);background:var(--accent-light)}
.match-slot.correct{border-color:var(--success);background:#e6f4ea!important}
.match-slot.wrong-only{border-color:var(--error);background:#fef2f2!important}
.match-slot .slot-placeholder{font-size:10px;color:var(--text2);font-weight:400}
@media(max-width:700px){.match-container{flex-direction:column}.match-right{width:100%}}'''

MATCH_JS = '''
<script>
(function(){
var poolData = POOL_PLACEHOLDER;
function ddMatchClick(el) {
  if (el.classList.contains("filled")) { removeMatch(el); return; }
  var p = document.getElementById("match-pool-s2-pool");
  if (!p) return;
  var items = p.querySelectorAll(".match-item:not(.used)");
  if (items.length === 0) return;
  placeMatch(el, items[0].getAttribute("data-letter"), items[0]);
}
function placeMatch(slot, letter, item) {
  slot.innerHTML = "<strong>" + letter + ".</strong> " + (poolData[letter] || letter);
  slot.setAttribute("data-letter", letter);
  slot.classList.add("filled"); slot.classList.remove("wrong-only","correct");
  if (item) { item.classList.add("used"); item.draggable = false; }
}
function removeMatch(slot) {
  var l = slot.getAttribute("data-letter");
  if (!l) return;
  var p = document.getElementById("match-pool-s2-pool");
  if (p) {
    var it = p.querySelector('.match-item[data-letter="' + l + '"]');
    if (it) { it.classList.remove("used"); it.draggable = true; }
  }
  slot.innerHTML = '<span class="slot-placeholder">拖拽选项至此</span>';
  slot.setAttribute("data-letter", "");
  slot.classList.remove("filled","correct","wrong-only");
}
function dragMatch(e) {
  if (e.target.classList.contains("used")) { e.preventDefault(); return; }
  e.dataTransfer.setData("text/plain", e.target.getAttribute("data-letter"));
  e.target.classList.add("dragging");
}
function dragMatchEnd(e) { e.target.classList.remove("dragging"); }
function allowMatchDrop(e) { e.preventDefault(); e.currentTarget.classList.add("dragover"); }
function removeDragOver(e) { e.currentTarget.classList.remove("dragover"); }
function dropMatch(e) {
  e.preventDefault(); e.stopPropagation();
  var slot = e.currentTarget; slot.classList.remove("dragover");
  if (slot.classList.contains("filled")) return;
  var letter = e.dataTransfer.getData("text/plain");
  if (!letter) return;
  var p = document.getElementById("match-pool-s2-pool");
  if (!p) return;
  var item = p.querySelector('.match-item[data-letter="' + letter + '"]');
  if (!item || item.classList.contains("used")) return;
  placeMatch(slot, letter, item);
}
var _ck = window.checkAnswers;
window.checkAnswers = function() {
  document.querySelectorAll('[data-qtype="match"]').forEach(function(b) {
    var s = b.querySelector(".match-slot"); if (!s) return;
    var a = s.getAttribute("data-ans"), v = s.getAttribute("data-letter")||"";
    s.classList.remove("correct","wrong-only","filled");
    s.classList.add(v === a ? "correct" : "wrong-only");
  }); if (_ck) _ck();
};
var _rv = window.revealAnswers;
window.revealAnswers = function() {
  document.querySelectorAll('[data-qtype="match"]').forEach(function(b) {
    var s = b.querySelector(".match-slot"); if (!s) return;
    var a = s.getAttribute("data-ans");
    s.innerHTML = "<strong>" + a + ".</strong> " + (poolData[a] || a);
    s.setAttribute("data-letter", a);
    s.classList.add("correct","filled"); s.classList.remove("wrong-only");
  }); if (_rv) _rv();
};
var _rs = window.resetAnswers;
window.resetAnswers = function() {
  document.querySelectorAll('[data-qtype="match"]').forEach(function(b) {
    var s = b.querySelector(".match-slot"); if (!s) return;
    var l = s.getAttribute("data-letter");
    if (l) {
      var p = document.getElementById("match-pool-s2-pool");
      if (p) {
        var it = p.querySelector('.match-item[data-letter="' + l + '"]');
        if (it) { it.classList.remove("used"); it.draggable = true; }
      }
    }
    s.innerHTML = '<span class="slot-placeholder">拖拽选项至此</span>';
    s.setAttribute("data-letter", "");
    s.classList.remove("filled","correct","wrong-only");
  }); if (_rs) _rs();
};
})();
</script>'''

def apply(html_path):
    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    
    # Remove old .match-pool CSS rules
    css_start = html.find('.match-pool{')
    css_end = html.find('.seek-btn-inline:hover{background:var(--accent);color:#fff}', css_start)
    if css_start > 0 and css_end > 0:
        css_end_brace = html.rfind('}', css_start, css_end)
        if css_end_brace > css_start:
            html = html[:css_start] + MATCH_CSS + html[css_end_brace+1:]
    else:
        html = html.replace('</style>', MATCH_CSS + '\n</style>', 1)
    
    # Convert fill q-blocks to match type (div-based drop zones)
    for num in sorted(ANSWERS, reverse=True):
        ans = ANSWERS[num]
        html = html.replace(f'data-qtype="fill" data-ans="{ans}"', f'data-qtype="match" data-ans="{ans}" data-num="{num}"', 1)
        inp = f'<input class="fill-input" data-ans="{ans}" placeholder="..." autocomplete="off">'
        slot = (f'<div class="match-slot" data-ans="{ans}" data-q="{num}" data-letter="" '
                f'data-pool="match-pool-s2-pool" ondragover="allowMatchDrop(event)" '
                f'ondrop="dropMatch(event)" ondragleave="removeDragOver(event)" '
                f'onclick="ddMatchClick(this)"><span class="slot-placeholder">\u62d6\u62fd\u9009\u9879\u81f3\u6b64</span></div>')
        html = html.replace(inp, slot, 1)
    
    # Extract all match q-blocks
    match_blocks = []
    for num in sorted(ANSWERS):
        ans = ANSWERS[num]
        m = re.search(
            r'<div class="q-block" data-qtype="match" data-ans="' + ans + r'" data-num="' + str(num) + r'">.*?</div>\s*</div>',
            html, re.DOTALL
        )
        if m:
            match_blocks.append(m.group(0))
    
    # Build pool items (right panel)
    pool_items = ''.join(
        f'<div class="match-item" draggable="true" data-letter="{l}" ondragstart="dragMatch(event)" ondragend="dragMatchEnd(event)">{l}. {lb}</div>\n'
        for l, lb in sorted(POOL_DATA.items())
    )
    
    # Build left-right layout
    match_html = (
        '<div class="match-container">\n<div class="match-left">\n'
        + '\n'.join(match_blocks)
        + '\n</div>\n<div class="match-right">\n<div class="pool-title">\u9009\u9879\u6c60</div>\n'
        + '<div class="match-pool" id="match-pool-s2-pool">\n' + pool_items + '</div>\n</div>\n</div>\n'
    )
    
    # Replace old match blocks
    first_m = html.find('<div class="q-block" data-qtype="match"')
    last_m = html.rfind('data-qtype="match"')
    if first_m > 0 and last_m > 0:
        last_end = html.find('</div>', html.find('</div>', html.find('</div>', last_m) + 6) + 6) + 6
        html = html[:first_m] + '\n' + match_html + '\n' + html[last_end:]
    
    # Inject matching JS
    js = MATCH_JS.replace('POOL_PLACEHOLDER', json.dumps(POOL_DATA, ensure_ascii=False))
    html = html.replace('</body>', js + '\n</body>', 1)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Applied matching to: {html_path}")

if __name__ == '__main__':
    import json
    if len(sys.argv) > 1:
        apply(sys.argv[1])
    else:
        print("Usage: python apply_matching.py <html_path>")
