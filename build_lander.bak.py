# Generic vital-konzept lander builder.
# Usage: python3 build_lander.py <content.py> [image-url-map.json|-] [output.html]
# Takes CSS + script from the Erovyn template, rebuilds the body from content.py
import re, html, json, sys, os
T=open('/home/user/erovyn-lander/index.html',encoding='utf-8').read()
def grab(pat):
    m=re.search(pat,T); assert m, pat; return m.group(1)
FLAG=grab(r'<img class="flag" src="([^"]+)"')
TPLOGO=grab(r'class="tp-logo" src="([^"]+)"'); TPSTARS=grab(r'class="tp-stars" src="([^"]+)"')
TPFOOT=grab(r'<div class="tp-foot">\s*<img src="([^"]+)"')
CHECK=grab(r'<ul class="bullets">\s*<li><img src="([^"]+)"')
PAY=grab(r'class="payments" src="([^"]+)"')
PRESSLBL=grab(r'class="press-label"><img src="([^"]+)"')
PRESS=re.search(r'id="press-track">\s*(.*?)\s*</div>',T,re.S).group(1)
TRUST=re.findall(r'class="trust-item"><img src="([^"]+)"',T)
INS=grab(r'id="insurance" checked>\s*<img src="([^"]+)"')
VT=grab(r'class="vt" src="([^"]+)"')
SUPPORT=grab(r'<section class="support">.*?<img src="([^"]+)"'.replace('.*?','[\\s\\S]*?'))
head=T[:T.index('<body')]; body_open=re.search(r'<body[^>]*>',T).group(0)
script=T[T.index('<script>\n/* ===='):]

import importlib.util
spec=importlib.util.spec_from_file_location('C',sys.argv[1]); C=importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
IMG = json.load(open(sys.argv[2])) if len(sys.argv)>2 and sys.argv[2]!='-' else {}
OUT = sys.argv[3] if len(sys.argv)>3 else os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),'index.html')
top3=C.TOP3; grid=C.GRID; faq=C.FAQ; bul=C.BULLETS
def I(name): return IMG.get(name,'images/'+name)

head=head.replace('<title>Erovyn™ Regenerations-Creme für Männer | 50 % Rabatt</title>','<title>'+C.TITLE+'</title>')
head=head.replace('EROVYN™ LANDER – Struktur nach vital-konzept.ch/erovyn/lander',C.NAME.upper()+' LANDER – Struktur nach dem vital-konzept.ch Lander-Template')

URG='<p class="urgency">50 % Rabatt endet um 23:59 Uhr (Nur noch <b class="stock">7</b> Stück auf Lager)</p>'
def section(cls,reverse,title,ps,img,alt,comment,style=''):
    p='\n'.join(f'      <p>{x}</p>' for x in ps)
    return f'''<!-- ===================== {comment} ===================== -->
<section class="sec{(' '+cls) if cls else ''}"{style}>
  <div class="sec-grid{' reverse' if reverse else ''}">
    <div class="sec-text">
      <h3>{title}</h3>
{p}
      <div class="cta-wrap">
        <a href="#pakete" class="btn btn-lg">JETZT BESTELLEN ➞</a>
        {URG}
      </div>
    </div>
    <div class="sec-img"><img src="{I(img)}" alt="{alt}" loading="lazy"></div>
  </div>
</section>
'''
B='<strong>'+C.FULLNAME+'</strong>'
def meta(name):
    return f'<div class="rev-meta"><img class="flag" src="{FLAG}" alt=""><span class="who">{name}</span><span class="verified">Verifizierter<br>Käufer</span><img class="vt" src="{VT}" alt=""></div>'
def fq(q,a): return f'      <div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a"><p>{a}</p></div></div>'
packs=[(5,'Bester Preis',19,95,350,255,'5er-Paket wählen',''),(3,'Beliebteste Wahl',22,65,210,145,'3er-Paket wählen',' popular'),
       (2,'Vorteilspaket',25,50,140,90,'2er-Paket wählen',''),(1,'Einzelpackung',35,35,70,35,'Einzelpackung wählen','')]
def pk(n,tag,per,tot,old,save,btn,cls): return f'''    <div class="pack{cls}">
      <div class="pack-tag">{tag}</div>
      <div class="pack-body">
        <div class="pack-img"><img src="{I(f'paket-{n}x.jpg')}" alt="{n}x {C.FULLNAME}" loading="lazy"></div>
        <h3>{n}x {C.NAME}</h3>
        <div class="stars">★★★★★<span>4,8</span></div>
        <div class="per">CHF {per} <small>/ Stück</small></div>
        <div class="total">Gesamt CHF {tot} <s>CHF {old}</s></div>
        <span class="saving">Sie sparen CHF {save}</span>
        <a class="pack-btn" data-qty="{n}" href="#">{btn}</a>
      </div>
    </div>'''

SECS=''.join(section(*x) for x in [
 ('beige',False,C.S[0]['title'],C.S[0]['ps'],C.S[0]['img'],C.S[0]['alt'],'5. SEKTION 1 – Vorher-Nachher (Bild rechts)'),
 ('',True,C.S[1]['title'],C.S[1]['ps'],C.S[1]['img'],C.S[1]['alt'],'6. SEKTION 2 – Mechanik (Bild links)'),
 ('beige',False,C.S[2]['title'],C.S[2]['ps'],C.S[2]['img'],C.S[2]['alt'],'7. SEKTION 3 – Schritt für Schritt (Bild rechts)'),
 ('',True,C.S[3]['title'],C.S[3]['ps'],C.S[3]['img'],C.S[3]['alt'],'8. SEKTION 4 – Experte (Bild links)'),
 ('beige',False,C.S[4]['title'],C.S[4]['ps'],C.S[4]['img'],C.S[4]['alt'],'8b. TESTIMONIAL-SEKTION (Bild rechts)')])
CLOSING=section('beige',False,C.CLOSING['title'],C.CLOSING['ps'],C.CLOSING['img'],C.CLOSING['alt'],'10. SEKTION 5 – Abschluss / Garantie (Bild rechts)',' style="margin-top:40px"')
NAME=C.NAME
body=f'''{body_open}

<!-- ===================== 1. TOPBAR ===================== -->
<div class="topbar">
  <div class="msg"><b>👀 Exklusives Angebot auf Facebook!! 👏🏻</b><span>Nur auf dieser Seite verfügbar. Letzte Chance!</span></div>
  <ul class="timer">
    <li><strong id="t-h">01</strong>Stunden</li>
    <li><strong id="t-m">45</strong>Minuten</li>
    <li><strong id="t-s">15</strong>Sekunden</li>
  </ul>
</div>

<!-- ===================== 2. HEADER ===================== -->
<header class="header">
  <div class="container">
    <img class="logo" src="{I(C.LOGO)}" alt="{NAME}" style="width:{C.LOGO_W}px">
    <a href="#pakete" class="btn btn-sm">JETZT BESTELLEN</a>
  </div>
</header>

<!-- ===================== 3. HERO ===================== -->
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-img"><img src="{I('hauptbild.webp')}" alt="{C.HERO_ALT}"></div>

    <div class="hero-info">
      <div class="tp-card">
        <div class="tp-head">
          <img class="flag" src="{FLAG}" alt="CH">
          <span class="name">{C.HERO_REVIEW[0]}</span>
          <span class="date" id="hero-date">22. Oktober 2026</span>
          <img class="tp-logo" src="{TPLOGO}" alt="Trustpilot">
          <img class="tp-stars" src="{TPSTARS}" alt="5 Sterne">
        </div>
        <p>{C.HERO_REVIEW[1]}</p>
        <div class="tp-foot">
          <img src="{TPFOOT}" alt="">
          <span>Ausgezeichnet: <b>4,7</b></span>
          <span><b>13.428</b> Bewertungen</span>
        </div>
      </div>

      <h1>{C.H1}</h1>

      <div class="price-row">
        <span class="price">CHF 35.–</span>
        <span class="price-old">CHF 70</span>
        <span class="save-badge">Sie sparen CHF 35.–</span>
      </div>

      <ul class="bullets">
{chr(10).join(f'        <li><img src="{CHECK}" alt="">{b}</li>' for b in bul)}
      </ul>

      <div class="expert">
        <div>
          <h4>Worte des Experten:</h4>
          <p>{C.EXPERT_QUOTE}</p>
          <small>– {C.EXPERT_NAME}</small>
        </div>
        <img src="{I('experte-avatar.jpg')}" alt="{C.EXPERT_NAME.split(' – ')[0]}">
      </div>

      <div class="cta-wrap">
        <a href="#pakete" class="btn btn-lg btn-pulse">JETZT BESTELLEN ➞</a>
        <p class="guarantee">100 % Zufriedenheit oder Geld zurück</p>
        <img class="payments" src="{PAY}" alt="Klarna, Google Pay, Mastercard, Visa, TWINT">
      </div>
    </div>
  </div>
</section>

<!-- ===================== 4. BEKANNT AUS ===================== -->
<div class="press">
  <div class="press-label"><img src="{PRESSLBL}" alt="">Bekannt aus…</div>
  <div class="press-track" id="press-track">
    {PRESS}
  </div>
</div>

{SECS}
<!-- ===================== 9. BEWERTUNGEN (3 Karten) ===================== -->
<div class="reviews-head">
  <div class="stars">★★★★★</div>
  <h3>Über 60’000 verifizierte Kunden</h3>
  <h4>Werden Sie noch heute Teil von tausenden Erfolgsgeschichten!</h4>
</div>
<div class="rev-grid cols-3" id="top-reviews">
{chr(10).join(f"""  <div class="rev">
    <img src="{I(img)}" alt="{n}" loading="lazy">
    {meta(n)}
    <p>{t}</p>
  </div>""" for n,img,t in top3)}
</div>
<button class="more-btn" id="more-btn">MEHR ANSEHEN</button>

{CLOSING}
<!-- ===================== 11. TRUST BADGES ===================== -->
<div class="trust">
  <h4>Über 60’000 zufriedene Kunden</h4>
  <div class="trust-row">
    <div class="trust-item"><img src="{TRUST[0]}" alt=""><span>Geld-zurück-<br>Garantie</span></div>
    <div class="trust-item"><img src="{TRUST[1]}" alt=""><span>Kostenloser<br>Versand<br>garantiert</span></div>
    <div class="trust-item"><img src="{TRUST[2]}" alt=""><span>Hohe Qualität<br>garantiert</span></div>
  </div>
</div>

<!-- ===================== 12. FAQ ===================== -->
<section class="faq">
  <h4>HÄUFIG GESTELLTE FRAGEN</h4>
  <div class="faq-grid">
    <div>
{chr(10).join(fq(q,a) for q,a in faq[:5])}
    </div>
    <div>
{chr(10).join(fq(q,a) for q,a in faq[5:])}
    </div>
  </div>
</section>

<!-- ===================== 13. PAKETE ===================== -->
<section class="packs" id="pakete">
  <h2>Wählen Sie Ihr {NAME} Paket</h2>
  <p class="sub">Je grösser das Paket, desto mehr sparen Sie pro Stück.</p>
  <div class="pack-grid">
{chr(10).join(pk(*p) for p in packs)}
  </div>
  <div class="pack-perks"><span>Kostenloser Versand</span><span>30 Tage Geld-zurück-Garantie</span><span>Sichere Zahlung</span></div>
  <label class="insurance">
    <input type="checkbox" id="insurance" checked>
    <img src="{INS}" alt="">
    <div><b>Versandversicherung – <em>CHF 5</em></b><p>Falls Ihre Bestellung verloren geht, beschädigt oder gestohlen wird, ersetzen wir sie umgehend oder erstatten Ihnen den vollen Betrag.</p></div>
  </label>
</section>

<!-- ===================== 14. BEWERTUNGEN (Raster 8) ===================== -->
<div class="reviews-head" id="bewertungen">
  <div class="stars">★★★★★</div>
  <h3>Über 60’000 verifizierte Kunden</h3>
  <h4>Werden Sie noch heute Teil von tausenden Erfolgsgeschichten!</h4>
</div>
<div class="rev-grid cols-4">
{chr(10).join(f'  <div class="rev"><img src="{I(img)}" alt="{n}" loading="lazy">{meta(n)}<p>{t}</p></div>' for n,img,t in grid)}
</div>
<div class="cta-wrap" style="margin-top:26px"><a href="#pakete" class="btn btn-lg btn-pulse" style="max-width:540px">SICHERN SIE SICH IHREN 50 % - RABATT</a></div>

<!-- ===================== 15. KUNDENDIENST ===================== -->
<section class="support">
  <h3>Kundendienst-Experten</h3>
  <p>Nicht 100 % zufrieden mit Ihrer Bestellung? Wir werden alles tun, um das Problem zu lösen. Nutzen Sie die 30-Tage-Geld-zurück-Garantie* und testen Sie risikofrei.</p>
  <img src="{SUPPORT}" alt="">
  <p>Unser Kundenservice ist von Montag bis Sonntag von 09:00 bis 22:00 Uhr erreichbar.<br>Durchschnittliche Antwortzeit: 24 Stunden</p>
  <p>Senden Sie uns eine E-Mail:<br><a href="mailto:support@vital-konzept.ch">support@vital-konzept.ch</a></p>
</section>

<!-- ===================== 16. FOOTER ===================== -->
<footer class="footer">
  © vital-konzept.ch
  <a href="https://vital-konzept.ch/pages/terms-of-service">Allgemeine Geschäftsbedingungen</a> |
  <a href="https://vital-konzept.ch/pages/privacy-policy">Datenschutzrichtlinie</a> |
  <a href="https://vital-konzept.ch/pages/refund-policy">Rückgaberichtlinie</a> |
  <a href="https://vital-konzept.ch/pages/disclaimer">*Haftungsausschluss</a>
  <p class="disclaimer">{C.DISCLAIMER}</p>
</footer>

<!-- ===================== 17. STICKY BESTELL-LEISTE ===================== -->
<div class="stickybar" id="stickybar">
  <div class="container">
    <img src="{I(C.STICKY)}" alt="{NAME}">
    <div><h5>{NAME}</h5><div class="p">CHF 35.– <em>50 % RABATT</em></div></div>
    <a href="#pakete" class="btn">JETZT BESTELLEN ➞</a>
  </div>
</div>

'''
# ---- script: product config, no Erovyn variants, safe pack buttons
s=script
s=re.sub(r"/\* =+\n   KONFIGURATION.*?=+ \*/",
"""/* ============================================================
   KONFIGURATION – hier die Shopify-Varianten-IDs DIESES Produkts eintragen
   (leer = Paket-Buttons zeigen einen Hinweis statt in den Warenkorb zu gehen)
   ============================================================ */""",s,flags=re.S)
s=re.sub(r"variants: \{[^}]*\},","variants: { 1:'', 2:'', 3:'', 5:'' },   // TODO: Varianten-IDs dieses Produkts eintragen",s)
s=s.replace("""document.querySelectorAll('.pack-btn').forEach(a=>{
  const set=()=>a.href=cartUrl(a.dataset.qty); set();""","""document.querySelectorAll('.pack-btn').forEach(a=>{
  const set=()=>{ if(CONFIG.variants[a.dataset.qty]) a.href=cartUrl(a.dataset.qty); else a.href='#pakete'; }; set();
  a.addEventListener('click',e=>{ if(!CONFIG.variants[a.dataset.qty]){ e.preventDefault(); alert('Hinweis für den Shop-Betreiber: Für dieses Paket ist noch keine Shopify-Varianten-ID hinterlegt (CONFIG.variants im Skript).'); } });""")
s=s.replace("'erovyn_deadline'","'"+C.KEY+"_deadline'")
assert C.KEY+"_deadline" in s and "variants: { 1:''" in s and "Hinweis für den Shop-Betreiber" in s
out=head+body+s
bad=[w for w in ['Erovyn','erovyn','Urolog','Potenz','Schlafzimmer','Elvory','Elviro','Orvantis']+getattr(C,'FORBIDDEN',[]) if w in out]
print('leftovers:',bad)
dst=OUT
open(dst,'w',encoding='utf-8').write(out); print('written',dst,len(out))
