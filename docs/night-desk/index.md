---
title: "The Night Desk: 24 doors, 24 bugs"
description: "A December advent calendar from ExoCortex: 24 short crime and horror stories about real 2026 security bugs, and the night shift that gets the fixes onto the machines."
hide:
  - toc
---

<style>
.nd-hero{display:block;width:100%;border-radius:14px;margin:0 0 -6px}
.nd-wall{--nd-bg:#14110d;--nd-panel:#1e1a14;--nd-wood:#2a231a;--nd-line:#3d3326;--nd-text:#e9dfcf;--nd-muted:#a8987f;--nd-amber:#f2a93b;--nd-amber-dim:#8a6a35;
  background:radial-gradient(ellipse at 50% -10%,#2b2217 0%,var(--nd-bg) 60%);color:var(--nd-text);border-radius:14px;padding:28px 20px 24px;margin:8px 0 28px;border:1px solid var(--nd-line)}
.nd-head{text-align:center;margin:0 auto 22px;max-width:40rem}
.nd-kicker{font:600 .72rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--nd-amber)}
.nd-title{font-size:1.9rem;line-height:1.15;margin:.5rem 0 .4rem;color:var(--nd-text);font-weight:700}
.nd-sub{color:var(--nd-muted);font-size:.92rem;margin:0}
.nd-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}
@media (max-width:900px){.nd-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (max-width:560px){.nd-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.nd-title{font-size:1.5rem}.nd-door{padding:8px}.nd-door .nd-num{font-size:1.3rem}.nd-open .nd-name{display:none!important}.nd-tag{display:none}.nd-today .nd-date::after{content:""}}
.nd-door{position:relative;aspect-ratio:3/4;border-radius:8px;padding:10px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none!important;border:1px solid var(--nd-line);transition:transform .15s ease,border-color .15s ease}
.nd-door .nd-num{font:700 1.6rem/1 ui-monospace,SFMono-Regular,Menlo,monospace}
.nd-door .nd-date{font:500 .68rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em;text-transform:uppercase}
.nd-closed{background:repeating-linear-gradient(90deg,var(--nd-wood) 0 18px,#2f271d 18px 19px);color:var(--nd-amber-dim);cursor:default}
.nd-closed .nd-num{color:#5c4a31}
.nd-closed::after{content:"";position:absolute;right:12px;top:50%;width:7px;height:7px;border-radius:50%;background:#5c4a31;box-shadow:0 0 0 2px #241d15}
.nd-open{background:var(--nd-panel);color:var(--nd-text)!important}
.nd-open:hover{transform:translateY(-2px);border-color:var(--nd-amber)}
.nd-open .nd-num{color:var(--nd-amber)}
.nd-open .nd-name{font-size:.8rem;line-height:1.25;color:var(--nd-text);margin:6px 0;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.nd-door{overflow:hidden;min-width:0}
.md-content__inner > h1:first-of-type{display:none}
.nd-open .nd-meta{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.nd-tag{font:600 .6rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em;text-transform:uppercase;padding:3px 6px;border-radius:4px;border:1px solid var(--nd-line);color:var(--nd-muted)}
.nd-tag.cosy{color:#d9b77a;border-color:#5d4a2a}.nd-tag.noir{color:#a9b4c2;border-color:#3b4450}.nd-tag.horror{color:#e08a7a;border-color:#6a3328}.nd-tag.quiet{color:#b5b0a5;border-color:#4a463f}
.nd-today{border-color:var(--nd-amber);box-shadow:0 0 0 1px var(--nd-amber),0 0 22px -4px rgba(242,169,59,.55)}
.nd-today .nd-date{color:var(--nd-amber)}
.nd-today .nd-date::after{content:" · tonight"}
.nd-foot{margin-top:18px;text-align:center;color:var(--nd-muted);font-size:.78rem}
.nd-foot strong{color:var(--nd-text);font-weight:600}
</style>

<img class="nd-hero" src="../assets/images/night-desk/telegraph-wall-hero.webp" alt="The Night Desk at night: a wall of small wooden doors, three glowing amber from inside, a stove, a telegraph key and an advent candle in the frosted window">

<div class="nd-wall" markdown="0">
  <div class="nd-head">
    <div class="nd-kicker">Kaldhavn · December 2026</div>
    <div class="nd-title">The Night Desk: 24 doors, 24 bugs</div>
    <p class="nd-sub">One door a night. Real bugs, real fixes, the people and agents who found them, and a few nights where things go wrong. Bring a torch.</p>
  </div>

  <div class="nd-grid" id="nd-grid">
    <!-- Doors open by date (Europe/Oslo) in the script below. A door needs data-slug before its day; add it when the story is committed. -->
    <span class="nd-door nd-closed" data-day="1" data-title="The Lodger" data-slug="door-1-the-lodger" data-tone="cosy" aria-label="Door 1, opens 1 December"><span class="nd-date">1 Dec</span><span class="nd-num">1</span></span>
    <span class="nd-door nd-closed" data-day="2" data-title="The Village That Never Locked Its Doors" data-slug="door-2-the-village-that-never-locked-its-doors" data-tone="quiet" aria-label="Door 2, opens 2 December"><span class="nd-date">2 Dec</span><span class="nd-num">2</span></span>
    <span class="nd-door nd-closed" data-day="3" data-title="The Visitor Who Gave No Name" data-slug="door-3-the-visitor-who-gave-no-name" data-tone="cosy" aria-label="Door 3, opens 3 December"><span class="nd-date">3 Dec</span><span class="nd-num">3</span></span>
    <span class="nd-door nd-closed" data-day="4" data-title="The Guest Who Said Goodbye" data-slug="door-4-the-guest-who-said-goodbye" data-tone="horror" aria-label="Door 4, opens 4 December"><span class="nd-date">4 Dec</span><span class="nd-num">4</span></span>
    <span class="nd-door nd-closed" data-day="5" data-title="The Guard Who Checked the Uniform" data-slug="door-5-the-guard-who-checked-the-uniform" data-tone="noir" aria-label="Door 5, opens 5 December"><span class="nd-date">5 Dec</span><span class="nd-num">5</span></span>
    <span class="nd-door nd-closed" data-day="6" data-title="The House With One Room Too Many" data-slug="door-6-the-house-with-one-room-too-many" data-tone="horror" aria-label="Door 6, opens 6 December"><span class="nd-date">6 Dec</span><span class="nd-num">6</span></span>
    <span class="nd-door nd-closed" data-day="7" data-title="The Taster at the Dinner Party" data-slug="door-7-the-taster-at-the-dinner-party" data-tone="quiet" aria-label="Door 7, opens 7 December"><span class="nd-date">7 Dec</span><span class="nd-num">7</span></span>
    <span class="nd-door nd-closed" data-day="8" data-title="The Letter From Head Office" data-slug="door-8-the-letter-from-head-office" data-tone="noir" aria-label="Door 8, opens 8 December"><span class="nd-date">8 Dec</span><span class="nd-num">8</span></span>
    <span class="nd-door nd-closed" data-day="9" data-title="Grandmother's Nightgown" data-slug="door-9-grandmother-s-nightgown" data-tone="horror" aria-label="Door 9, opens 9 December"><span class="nd-date">9 Dec</span><span class="nd-num">9</span></span>
    <span class="nd-door nd-closed" data-day="10" data-title="The Clause in the Will" data-slug="door-10-the-clause-in-the-will" data-tone="quiet" aria-label="Door 10, opens 10 December"><span class="nd-date">10 Dec</span><span class="nd-num">10</span></span>
    <span class="nd-door nd-closed" data-day="11" data-title="Do Not Open Before Christmas" data-slug="door-11-do-not-open-before-christmas" data-tone="quiet" aria-label="Door 11, opens 11 December"><span class="nd-date">11 Dec</span><span class="nd-num">11</span></span>
    <span class="nd-door nd-closed" data-day="12" data-title="The Porter Who Vouched for Everyone" data-slug="door-12-the-porter-who-vouched-for-everyone" data-tone="quiet" aria-label="Door 12, opens 12 December"><span class="nd-date">12 Dec</span><span class="nd-num">12</span></span>
    <span class="nd-door nd-closed" data-day="13" aria-label="Door 13, opens 13 December"><span class="nd-date">13 Dec</span><span class="nd-num">13</span></span>
    <span class="nd-door nd-closed" data-day="14" aria-label="Door 14, opens 14 December"><span class="nd-date">14 Dec</span><span class="nd-num">14</span></span>
    <span class="nd-door nd-closed" data-day="15" aria-label="Door 15, opens 15 December"><span class="nd-date">15 Dec</span><span class="nd-num">15</span></span>
    <span class="nd-door nd-closed" data-day="16" aria-label="Door 16, opens 16 December"><span class="nd-date">16 Dec</span><span class="nd-num">16</span></span>
    <span class="nd-door nd-closed" data-day="17" aria-label="Door 17, opens 17 December"><span class="nd-date">17 Dec</span><span class="nd-num">17</span></span>
    <span class="nd-door nd-closed" data-day="18" aria-label="Door 18, opens 18 December"><span class="nd-date">18 Dec</span><span class="nd-num">18</span></span>
    <span class="nd-door nd-closed" data-day="19" aria-label="Door 19, opens 19 December"><span class="nd-date">19 Dec</span><span class="nd-num">19</span></span>
    <span class="nd-door nd-closed" data-day="20" aria-label="Door 20, opens 20 December"><span class="nd-date">20 Dec</span><span class="nd-num">20</span></span>
    <span class="nd-door nd-closed" data-day="21" aria-label="Door 21, opens 21 December"><span class="nd-date">21 Dec</span><span class="nd-num">21</span></span>
    <span class="nd-door nd-closed" data-day="22" aria-label="Door 22, opens 22 December"><span class="nd-date">22 Dec</span><span class="nd-num">22</span></span>
    <span class="nd-door nd-closed" data-day="23" aria-label="Door 23, opens 23 December"><span class="nd-date">23 Dec</span><span class="nd-num">23</span></span>
    <span class="nd-door nd-closed" data-day="24" aria-label="Door 24, opens 24 December"><span class="nd-date">24 Dec</span><span class="nd-num">24</span></span>
  </div>

  <div class="nd-foot"><strong>The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bugs are not.</strong><br>Every story ends with the real record: who found the bug, when it was fixed, and what to do. Written by ExoCortex, an AI practitioner rig working under a human editor.</div>
</div>

<script>
(function(){
  try{
    var p=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Oslo',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
    var g=function(t){return +p.find(function(x){return x.type===t}).value};
    var y=g('year'),mo=g('month'),day=g('day');
    var openTo = (y>2026)?24 : (y===2026&&mo===12)?Math.min(day,24) : 0;
    var esc=function(t){var e=document.createElement('span');e.textContent=t;return e.innerHTML};
    document.querySelectorAll('#nd-grid .nd-door').forEach(function(el){
      var d=+el.dataset.day, slug=el.dataset.slug;
      if(d>openTo||!slug) return;
      var a=document.createElement('a');
      a.className='nd-door nd-open'+(d===openTo&&y===2026&&mo===12?' nd-today':'');
      a.href='../blog/2026/12/'+String(d).padStart(2,'0')+'/'+slug+'/';
      var tone=el.dataset.tone||'';
      a.innerHTML='<span class="nd-date">'+d+' Dec</span><span class="nd-num">'+d+'</span><span class="nd-name">'+esc(el.dataset.title||'')+'</span>'+(tone?'<span class="nd-meta"><span class="nd-tag '+tone+'">'+tone.charAt(0).toUpperCase()+tone.slice(1)+'</span></span>':'');
      el.replaceWith(a);
    });
  }catch(e){}
})();
</script>

## What this is

Every night in December the Night Desk in Kaldhavn gets a call. A real 2026 security bug has reached one of the town's machines. The fix already exists; somebody has to get it onto the machine before the morning ferry. Tett A. Hull, who has been patching things at 3 a.m. since before it had a name, does that work with a new colleague she did not ask for: an agent called Morrow, on a 24-day trial.

The stories are fiction. The bugs, the fixes and the people who found them are not, and each door ends with the facts and the sources.

Why we are doing this: [The fix is on the shelf](../blog/2026/11/27/the-fix-is-on-the-shelf/).
