import re
html_path = '/tmp/u03_s2.html'
with open(html_path, encoding='utf-8') as f:
    html = f.read()

pool = {"A":"Cooking sessions","B":"Book sharing","C":"Music memory",
        "D":"Garden projects","E":"Photo albums","F":"Board games",
        "G":"Walking group","H":"Art classes"}
answers = {15:"E",16:"D",17:"G",18:"B",19:"C",20:"H"}

# Convert fill blocks to match blocks
for num, ans in answers.items():
    html = html.replace('data-qtype="fill" data-ans="' + ans + '"', 'data-qtype="match" data-ans="' + ans + '"', 1)
    # Replace input with slot
    inp_pattern = '<input class="fill-input" data-ans="' + ans + '" placeholder="..." autocomplete="off">'
    slot = '<span class="match-slot" data-ans="' + ans + '" data-q="' + str(num) + '" data-letter="" data-pool="match-pool-s2-pool" ondrop="dropMatch(event)" ondragover="allowMatchDrop(event)" ondragleave="this.classList.remove(\'dragover\')" onclick="ddMatchClick(this)"><span class="slot-placeholder">\u62d6\u62fd\u9009\u9879\u81f3\u6b64\u5904</span></span>'
    html = html.replace(inp_pattern, slot, 1)

# Build pool
pool_items = ''
for letter, label in sorted(pool.items()):
    pool_items += '<span class="match-item" draggable="true" data-letter="' + letter + '" ondragstart="dragMatch(event)" ondragend="dragMatchEnd(event)">' + letter + '. ' + label + '</span>'
pool_html = '<div class="match-pool" id="match-pool-s2-pool">' + pool_items + '</div>'

# Insert pool before first match q-block
first_match = html.find('data-qtype="match"')
if first_match > 0:
    qb = html.rfind('<div class="q-block"', 0, first_match)
    if qb > 0:
        html = html[:qb] + pool_html + '\n' + html[qb:]

# Add matching CSS before </style>
match_css = '''
.match-pool{display:flex;flex-wrap:wrap;gap:5px;padding:10px;margin-bottom:14px;background:var(--card);border:2px solid var(--border);border-radius:var(--radius)}
.match-item{padding:5px 12px;border:2px solid var(--accent);border-radius:6px;cursor:grab;font-size:12px;font-weight:600;background:var(--accent-light);color:var(--accent);user-select:none;font-family:var(--ui-font)}
.match-item:hover{border-color:#c0664a;background:#fde4d4}
.match-item.dragging{opacity:.4}
.match-item.used{opacity:.35;cursor:default;border-style:dashed;background:var(--sidebar);color:var(--text2)}
.match-slot{display:inline-flex;align-items:center;justify-content:center;min-width:36px;height:30px;border:2px dashed var(--border);border-radius:5px;background:var(--card);font-size:12px;font-weight:600;color:var(--text);font-family:var(--ui-font);margin:0 4px;padding:0 6px;cursor:default;vertical-align:middle}
.match-slot.dragover{border-color:var(--accent);background:var(--accent-light)}
.match-slot.filled{border-style:solid;border-color:var(--accent);background:var(--accent-light)}
.match-slot.correct{border-color:var(--success);background:#e6f4ea!important}
.match-slot.wrong-only{border-color:var(--error);background:#fef2f2!important}
.match-slot .slot-placeholder{font-size:10px;color:var(--text2);font-weight:400}'''

html = html.replace('</style>', match_css + '\n</style>', 1)

# Add matching JS before </body>
match_js = '''
<script>
(function(){
function ddMatchClick(el) {
  if (el.classList.contains("filled")) { removeMatch(el); return; }
  var pool = document.getElementById(el.getAttribute("data-pool"));
  if (!pool) return;
  var items = pool.querySelectorAll(".match-item:not(.used)");
  if (items.length === 0) return;
  placeMatch(el, items[0].getAttribute("data-letter"), items[0]);
}
function placeMatch(slot, letter, item) {
  slot.innerHTML = "<strong>" + letter + "</strong>";
  slot.setAttribute("data-letter", letter);
  slot.classList.add("filled"); slot.classList.remove("wrong-only","correct");
  item.classList.add("used"); item.draggable = false;
}
function removeMatch(slot) {
  var l = slot.getAttribute("data-letter");
  if (!l) return;
  var p = document.getElementById(slot.getAttribute("data-pool"));
  if (p) {
    var it = p.querySelector(\'.match-item[data-letter="\' + l + \'"]\');
    if (it) { it.classList.remove("used"); it.draggable = true; }
  }
  slot.innerHTML = \'<span class="slot-placeholder">\u62d6\u62fd\u9009\u9879\u81f3\u6b64\u5904</span>\';
  slot.setAttribute("data-letter", "");
  slot.classList.remove("filled","correct","wrong-only");
}
function dragMatch(e) {
  if (e.target.classList.contains("used")) { e.preventDefault(); return; }
  e.dataTransfer.setData("text", e.target.getAttribute("data-letter"));
  e.target.classList.add("dragging");
}
function dragMatchEnd(e) { e.target.classList.remove("dragging"); }
function allowMatchDrop(e) { e.preventDefault(); e.currentTarget.classList.add("dragover"); }
function dropMatch(e) {
  e.preventDefault();
  var slot = e.currentTarget; slot.classList.remove("dragover");
  if (slot.classList.contains("filled")) return;
  var letter = e.dataTransfer.getData("text");
  var pool = document.getElementById(slot.getAttribute("data-pool"));
  if (!pool) return;
  var item = pool.querySelector(\'.match-item[data-letter="\' + letter + \'"]\');
  if (!item || item.classList.contains("used")) return;
  placeMatch(slot, letter, item);
}
// Patch grading
var _ck = window.checkAnswers;
window.checkAnswers = function() {
  document.querySelectorAll(\'[data-qtype="match"]\').forEach(function(b) {
    var s = b.querySelector(".match-slot"); if (!s) return;
    var a = s.getAttribute("data-ans"), v = s.getAttribute("data-letter")||"";
    s.classList.remove("correct","wrong-only","filled");
    s.classList.add(v === a ? "correct" : "wrong-only");
  });
  if (_ck) _ck();
};
var _rv = window.revealAnswers;
window.revealAnswers = function() {
  document.querySelectorAll(\'[data-qtype="match"]\').forEach(function(b) {
    var s = b.querySelector(".match-slot"); if (!s) return;
    var a = s.getAttribute("data-ans");
    s.innerHTML = "<strong>" + a + "</strong>";
    s.setAttribute("data-letter", a);
    s.classList.add("correct","filled"); s.classList.remove("wrong-only");
  });
  if (_rv) _rv();
};
var _rs = window.resetAnswers;
window.resetAnswers = function() {
  document.querySelectorAll(\'[data-qtype="match"]\').forEach(function(b) {
    var s = b.querySelector(".match-slot"); if (!s) return;
    var l = s.getAttribute("data-letter");
    if (l) {
      var p = document.getElementById(s.getAttribute("data-pool"));
      if (p) {
        var it = p.querySelector(\'.match-item[data-letter="\' + l + \'"]\');
        if (it) { it.classList.remove("used"); it.draggable = true; }
      }
    }
    s.innerHTML = \'<span class="slot-placeholder">\u62d6\u62fd\u9009\u9879\u81f3\u6b64\u5904</span>\';
    s.setAttribute("data-letter", "");
    s.classList.remove("filled","correct","wrong-only");
  });
  if (_rs) _rs();
};
})();
</script>'''
html = html.replace('</body>', match_js + '\n</body>', 1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

stats = {
    'match-pool': html.count('match-pool'),
    'match-slot': html.count('match-slot'),
    'match-item': html.count('match-item'),
    'dragMatch': html.count('function dragMatch'),
    'dropMatch': html.count('function dropMatch'),
    'fill-input': html.count('fill-input'),
}
for k, v in stats.items():
    print(f"{k}: {v}")
