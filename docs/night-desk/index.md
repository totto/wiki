---
title: "The Night Desk: 24 doors, 24 bugs"
description: "A December advent calendar from ExoCortex: 24 short crime and horror stories about real 2026 security bugs, and the night shift that gets the fixes onto the machines."
hide:
  - toc
---

<style>
.md-content__inner > h1:first-of-type{display:none}
.nd-wall{--nd-bg:#14110d;--nd-panel:#1e1a14;--nd-wood:#2a231a;--nd-line:#3d3326;--nd-text:#ede4d3;--nd-muted:#a8987f;--nd-amber:#f2a93b;--nd-amber-dim:#8a6a35;
  background:var(--nd-bg);color:var(--nd-text);border-radius:14px;overflow:hidden;margin:8px 0 28px;border:1px solid var(--nd-line)}
.nd-head{position:relative;min-height:340px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;text-align:center;padding:24px 20px 26px;
  background:linear-gradient(180deg,rgba(20,17,13,0) 30%,rgba(20,17,13,.72) 68%,var(--nd-bg) 100%),url(../assets/images/night-desk/telegraph-wall-hero.webp) center 35%/cover no-repeat}
.nd-kicker{font:600 .72rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--nd-amber);text-shadow:0 1px 6px #000}
.nd-title{font-size:2.1rem;line-height:1.1;margin:.5rem 0 .45rem;color:#fff6e6;font-weight:700;text-shadow:0 2px 14px rgba(0,0,0,.8)}
.nd-sub{color:#d6c8b0;font-size:.95rem;margin:0;max-width:38rem;text-shadow:0 1px 8px #000}
.nd-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;padding:6px 20px 0}
@media (max-width:900px){.nd-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (max-width:560px){.nd-open .nd-top{left:8px;top:8px;gap:5px}.nd-today .nd-top{top:22px}.nd-head{min-height:260px}.nd-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;padding:6px 12px 0}.nd-title{font-size:1.5rem}.nd-door .nd-num{font-size:1.25rem}.nd-open .nd-name{display:none!important}.nd-today .nd-flag{display:none}}
.nd-door{position:relative;aspect-ratio:3/4;border-radius:8px;overflow:hidden;min-width:0;text-decoration:none!important;border:1px solid var(--nd-line);transition:transform .15s ease,border-color .15s ease,box-shadow .15s ease}
.nd-door .nd-num{font:700 1.6rem/1 ui-monospace,SFMono-Regular,Menlo,monospace}
.nd-door .nd-date{font:500 .66rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em;text-transform:uppercase}
.nd-closed{display:flex;flex-direction:column;justify-content:space-between;padding:10px;background:repeating-linear-gradient(90deg,var(--nd-wood) 0 18px,#2f271d 18px 19px);color:var(--nd-amber-dim);cursor:default}
.nd-closed .nd-num{color:#5c4a31}
.nd-closed::after{content:"";position:absolute;right:12px;top:50%;width:7px;height:7px;border-radius:50%;background:#5c4a31;box-shadow:0 0 0 2px #241d15}
.nd-open{display:block;background:#000 center/cover no-repeat;color:var(--nd-text)!important}
.nd-open::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,11,8,.55) 0%,rgba(14,11,8,0) 30%,rgba(14,11,8,.15) 50%,rgba(14,11,8,.92) 82%)}
.nd-open > *{position:relative}
.nd-open .nd-top{position:absolute;top:9px;left:10px;right:10px;display:flex;justify-content:flex-start;align-items:center;gap:7px;white-space:nowrap}
.nd-open .nd-num{color:var(--nd-amber);text-shadow:0 1px 8px #000}
.nd-open .nd-date{color:#e9dcc4;display:flex;align-items:center;gap:6px}
.nd-dot{width:7px;height:7px;border-radius:50%;display:inline-block;box-shadow:0 0 0 1px rgba(0,0,0,.5)}
.nd-dot.cosy{background:#e2b56b}.nd-dot.noir{background:#9fb0c6}.nd-dot.horror{background:#e0705c}.nd-dot.quiet{background:#cfc8bb}
.nd-open .nd-name{position:absolute;left:10px;right:10px;bottom:10px;font-size:.8rem;line-height:1.25;font-weight:600;color:#fff3e0;text-shadow:0 1px 6px #000;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.nd-open:hover{transform:translateY(-2px);border-color:var(--nd-amber)}
.nd-today{border:2px solid var(--nd-amber);box-shadow:0 0 0 1px var(--nd-amber),0 0 28px -2px rgba(242,169,59,.7)}
.nd-flag{position:absolute;top:0;left:50%;transform:translateX(-50%);white-space:nowrap;background:var(--nd-amber);color:#1b140b;font:700 .6rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;padding:4px 8px;border-radius:0 0 6px 6px}
.nd-today .nd-top{top:24px}
.nd-legend{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin:16px 20px 0;color:var(--nd-muted);font:500 .7rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em;text-transform:uppercase}
.nd-legend span{display:inline-flex;align-items:center;gap:6px}
.nd-foot{margin:14px 20px 22px;text-align:center;color:var(--nd-muted);font-size:.78rem}
.nd-foot strong{color:var(--nd-text);font-weight:600}
</style>

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
    <span class="nd-door nd-closed" data-day="13" data-title="The Crime Where Every Check Passed" data-slug="door-13-the-crime-where-every-check-passed" data-tone="cosy" aria-label="Door 13, opens 13 December"><span class="nd-date">13 Dec</span><span class="nd-num">13</span></span>
    <span class="nd-door nd-closed" data-day="14" data-title="The Voice in the File Server" data-slug="door-14-the-voice-in-the-file-server" data-tone="horror" aria-label="Door 14, opens 14 December"><span class="nd-date">14 Dec</span><span class="nd-num">14</span></span>
    <span class="nd-door nd-closed" data-day="15" data-title="The Note Pinned to the Script" data-slug="door-15-the-note-pinned-to-the-script" data-tone="quiet" aria-label="Door 15, opens 15 December"><span class="nd-date">15 Dec</span><span class="nd-num">15</span></span>
    <span class="nd-door nd-closed" data-day="16" data-title="The Voice That Spoke to the Cupboard" data-slug="door-16-the-voice-that-spoke-to-the-cupboard" data-tone="horror" aria-label="Door 16, opens 16 December"><span class="nd-date">16 Dec</span><span class="nd-num">16</span></span>
    <span class="nd-door nd-closed" data-day="17" data-title="The Body Was Already Cold" data-slug="door-17-the-body-was-already-cold" data-tone="quiet" aria-label="Door 17, opens 17 December"><span class="nd-date">17 Dec</span><span class="nd-num">17</span></span>
    <span class="nd-door nd-closed" data-day="18" data-title="The One in the Glass" data-slug="door-18-the-one-in-the-glass" data-tone="quiet" aria-label="Door 18, opens 18 December"><span class="nd-date">18 Dec</span><span class="nd-num">18</span></span>
    <span class="nd-door nd-closed" data-day="19" data-title="The Sleeper" data-slug="door-19-the-sleeper" data-tone="quiet" aria-label="Door 19, opens 19 December"><span class="nd-date">19 Dec</span><span class="nd-num">19</span></span>
    <span class="nd-door nd-closed" data-day="20" data-title="The Dial in the Cellar" data-slug="door-20-the-dial-in-the-cellar" data-tone="horror" aria-label="Door 20, opens 20 December"><span class="nd-date">20 Dec</span><span class="nd-num">20</span></span>
    <span class="nd-door nd-closed" data-day="21" data-title="The Servant and the Forged Order" data-slug="door-21-the-servant-and-the-forged-order" data-tone="noir" aria-label="Door 21, opens 21 December"><span class="nd-date">21 Dec</span><span class="nd-num">21</span></span>
    <span class="nd-door nd-closed" data-day="22" data-title="The Guest Who Was Shown Out Twice" data-slug="door-22-the-guest-who-was-shown-out-twice" data-tone="noir" aria-label="Door 22, opens 22 December"><span class="nd-date">22 Dec</span><span class="nd-num">22</span></span>
    <span class="nd-door nd-closed" data-day="23" data-title="Two Killers, One Alibi" data-slug="door-23-two-killers-one-alibi" data-tone="noir" aria-label="Door 23, opens 23 December"><span class="nd-date">23 Dec</span><span class="nd-num">23</span></span>
    <span class="nd-door nd-closed" data-day="24" data-title="The Last of the Candle" data-slug="door-24-the-last-of-the-candle" data-tone="cosy" aria-label="Door 24, opens 24 December"><span class="nd-date">24 Dec</span><span class="nd-num">24</span></span>
  </div>

  <div class="nd-legend"><span><i class="nd-dot cosy"></i>Cosy</span><span><i class="nd-dot noir"></i>Noir</span><span><i class="nd-dot horror"></i>Horror</span><span><i class="nd-dot quiet"></i>Quiet: real victims</span></div>
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
      var today=(d===openTo&&y===2026&&mo===12);
      a.className='nd-door nd-open'+(today?' nd-today':'');
      a.href='../blog/2026/12/'+String(d).padStart(2,'0')+'/'+slug+'/';
      a.style.backgroundImage='url(../assets/images/night-desk/door-'+String(d).padStart(2,'0')+'-thumb.webp)';
      var tone=el.dataset.tone||'';
      a.setAttribute('aria-label','Door '+d+': '+(el.dataset.title||''));
      a.innerHTML=(today?'<span class="nd-flag">Tonight</span>':'')+'<span class="nd-top"><span class="nd-num">'+d+'</span>'+(tone?'<i class="nd-dot '+tone+'" title="'+tone+'"></i>':'')+'</span><span class="nd-name">'+esc(el.dataset.title||'')+'</span>';
      el.replaceWith(a);
    });
  }catch(e){}
})();
</script>

## What this is

Every night in December the Night Desk in Kaldhavn gets a call. A real 2026 security bug has reached one of the town's machines. The fix already exists; somebody has to get it onto the machine before the morning ferry. Tett A. Hull, who has been patching things at 3 a.m. since before it had a name, does that work with a new colleague she did not ask for: an agent called Morrow, on a 24-day trial.

The stories are fiction. The bugs, the fixes and the people who found them are not, and each door ends with the facts and the sources.

Why we are doing this: [The fix is on the shelf](../blog/2026/11/27/the-fix-is-on-the-shelf/).
