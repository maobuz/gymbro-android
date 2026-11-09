#!/usr/bin/env python3
"""Crea la versione GymBro Lite dell'app Android a partire da www/ (la Pro).

Lite = senza Garmin/Home Assistant, timer di recupero a cerchio al centro, nome e id diversi
(si installa accanto alla Pro). Uso: python3 ci/make_lite.py  -> crea www-lite/ e capacitor.config.json lite.
"""
import json, os, shutil

SRC, DST = "www", "www-lite"
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
p = os.path.join(DST, "index.html")
s = open(p, encoding="utf-8").read()

CSS = r'''#timer.full{inset:0;bottom:0;padding:0;display:flex;align-items:center;justify-content:center;background:rgba(10,12,14,.72);pointer-events:auto;z-index:30}
#timer .tcard{background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:24px;padding:20px 20px 12px;width:min(340px,calc(100% - 32px));display:flex;flex-direction:column;align-items:center;gap:14px;box-shadow:0 18px 50px rgba(0,0,0,.35)}
#timer .tname{font-size:15px;color:var(--muted);text-align:center;max-width:100%;overflow-wrap:anywhere}
#timer .tname b{display:block;color:var(--ink);font-size:17px;margin-top:2px}
#timer .ring{position:relative;width:min(240px,62vw);aspect-ratio:1}
#timer .ring svg{width:100%;height:100%;transform:rotate(-90deg);display:block}
#timer .rbg{fill:none;stroke:var(--line);stroke-width:14}
#timer .rfg{fill:none;stroke:var(--accent);stroke-width:14;stroke-linecap:round;transition:stroke-dashoffset .25s linear}
#timer .rin{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}
#timer .rtime{font-family:var(--f-display);font-weight:700;font-size:58px;line-height:1;font-variant-numeric:tabular-nums}
#timer .rskip{background:var(--accent);color:var(--accent-ink);border:0;border-radius:999px;padding:10px 28px;font-weight:700;font-size:17px;min-height:46px}
#timer .rbtns{display:flex;gap:10px;width:100%}
#timer .rb{flex:1;min-height:48px;border-radius:12px;border:1px solid var(--line);background:var(--surface-2);color:var(--ink);font-weight:600;font-size:16px}
#timer .rmin{background:none;border:0;color:var(--muted);font-weight:600;font-size:14px;padding:6px 10px;min-height:36px}
#timer.full.over .rtime{color:var(--accent-text)}
@media (prefers-reduced-motion:reduce){#timer .rfg{transition:none}}
'''
TICK = r'''let tMini=false;
const RC=2*Math.PI*104;
function tick(){
  const el=document.getElementById("timer"); const left=(tPause!=null?tPause:tEnd-Date.now())/1000;
  if(left<=0&&!tBeeped){tBeeped=true;beep();}
  if(left<-20){stopTimer();return;}
  el.hidden=false; el.classList.toggle("over",left<=0);
  const stato=tPause!=null?"In pausa":left>0?"Recupero":"Prossima serie";
  if(tMini){
    el.classList.remove("full");
    el.innerHTML=`<div class="tb"><div class="tt">${left>0?fmtTime(left):"Via!"}</div><div class="tl">${stato} · ${esc(tName)}</div>
    <button data-act="tmax">Ingrandisci</button><button data-act="tskip">${left>0?"Salta":"Ok"}</button>
    <div class="bar" style="width:${Math.max(0,Math.min(100,left/tTotal*100))}%"></div></div>`;
    return;
  }
  if(!el.classList.contains("full")||!el.querySelector(".ring")){
    el.classList.add("full");
    el.innerHTML=`<div class="tcard" role="dialog" aria-label="Recupero"><div class="tname"></div>
      <div class="ring"><svg viewBox="0 0 240 240" aria-hidden="true"><circle class="rbg" cx="120" cy="120" r="104"/><circle class="rfg" cx="120" cy="120" r="104" stroke-dasharray="${RC.toFixed(2)}"/></svg>
      <div class="rin"><div class="rtime" aria-live="off"></div><button class="rskip" data-act="tskip">Salta</button></div></div>
      <div class="rbtns"><button class="rb" data-act="tpause">Pausa</button><button class="rb" data-act="tadd">+15 s</button></div>
      <button class="rmin" data-act="tmini">Riduci e continua a segnare</button></div>`;
  }
  const frac=left>0?Math.max(0,Math.min(1,left/tTotal)):0;
  el.querySelector(".tname").innerHTML=`${stato}<b>${esc(tName)}</b>`;
  el.querySelector(".rtime").textContent=left>0?fmtTime(left):"Via!";
  el.querySelector(".rfg").style.strokeDashoffset=(RC*frac).toFixed(2);
  el.querySelector(".rskip").textContent=left>0?"Salta":"Ok";
  const pb=el.querySelector('[data-act="tpause"]'); pb.hidden=!(left>0); pb.textContent=tPause!=null?"Riprendi":"Pausa";
}
document.addEventListener("click",e=>{const b=e.target.closest("[data-act]"); if(!b) return;
  if(b.dataset.act==="tmini"){tMini=true;tick();} else if(b.dataset.act==="tmax"){tMini=false;tick();}});'''

def sostituisci(vecchio, nuovo):
    global s
    n = s.count(vecchio)
    assert n == 1, f"atteso 1, trovato {n}: {vecchio[:60]!r}"
    s = s.replace(vecchio, nuovo)

# Nome
sostituisci("<title>GymBro Pro</title>", "<title>GymBro Lite</title>")
sostituisci('<div class="brand"><i></i>Palestra da GymBro Pro</div>', '<div class="brand"><i></i>GymBro Lite</div>')
sostituisci('x.fillText("PALESTRA DA GYMBRO PRO",112,118);', 'x.fillText("GYMBRO LITE",112,118);')
# Niente Garmin / Home Assistant
sostituisci('window.claude={use:async n=>n==="mcp"?mcp:null};', 'window.claude={use:async n=>null};')
sostituisci("${vTema()}${vZoom()}${vHA()}${vBackup()}", "${vTema()}${vZoom()}${vBackup()}")
sostituisci("Colore, testo, collegamento a Home Assistant e backup dei dati.", "Colore, dimensione del testo e backup dei dati.")
# Timer di recupero: cerchio al centro (se la Pro non lo ha già)
if "const RC=2*Math.PI*104" not in s:
    i = s.index("function tick(){")
    j = s.index("\nasync function keepAwake", i)
    s = s[:i] + TICK + s[j:]
    sostituisci("function startTimer(sec,name,from){tFrom=from||null;", "function startTimer(sec,name,from){tMini=false;tFrom=from||null;")
    sostituisci("#timer.over .tb{", CSS + "#timer.over .tb{")

open(p, "w", encoding="utf-8").write(s)

cfg = json.load(open("capacitor.config.json"))
cfg.update({"appId": "it.maobuz.gymbro.lite", "appName": "GymBro Lite", "webDir": DST})
json.dump(cfg, open("capacitor.config.json", "w"), indent=2)
print("www-lite pronto")
