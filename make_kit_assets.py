# Builds the REFERENCE TEMPLATE (sample page) + copies the image script, and embeds both into the Kit app.
# Run: python3 /home/user/lander-builder/make_kit_assets.py
import subprocess, json, re, os, shutil
D = '/home/user/lander-builder/'; APP = '/home/user/lander-kit/public/'
subprocess.run(['python3', D + 'build_lander.py', D + 'sample_content.py', '-', D + 'template-raw.html'], check=True)
t = open(D + 'template-raw.html', encoding='utf-8').read()

GUIDE = '''<!--
=====================================================================================
 REFERENCE TEMPLATE – vital-konzept.ch landing page (sample with {{TOKENS}})
=====================================================================================
 HOW TO USE
 1. Copy this file 1:1. Do NOT change the CSS, class names, ids or the <script>.
    Only replace the {{TOKENS}}, the image files and (only if the brief says so) the prices.
 2. {{TOKENS}} = slot IDs of the COPY TEMPLATE (HERO_H1, S1_TITLE, S1_P1 ... FAQ_10_A, REVIEW_11_TEXT).
    **bold** in the copy -> <strong>...</strong>. Every S*_P2 starts with <strong>{{PRODUCT_FULL}}</strong>.
    {{PRODUCT}} = short name with (TM) e.g. "Glavex™" · {{PRODUCT_FULL}} = name + product type
    e.g. "Glavex™ Magnet-Scheibenreiniger" · {{PRODUCT_KEY}} = lowercase slug (countdown storage key).
 3. Images = relative paths images/<file>:
    logo.png · hauptbild.webp (animated main image, GIF copy: hauptbild.gif) · vorher-nachher.jpg ·
    mechanik.jpg · schritte.jpg · experte.jpg · experte-avatar.jpg · testimonial.jpg · abschluss.jpg ·
    paket-1x.jpg paket-2x.jpg paket-3x.jpg paket-5x.jpg · review-01.jpg ... review-11.jpg · sticky.png
    The https:// icons (Swiss flag, Trustpilot, check marks, payment icons, press logos, trust badges,
    insurance and support images) are our shared store assets – keep them unchanged.
 4. Prices (store standard): 1x CHF 35 (statt 70) · 2x CHF 50 (statt 140) · 3x CHF 65 (statt 210) ·
    5x CHF 95 (statt 350) · Versandversicherung CHF 5. They appear in: hero .price-row, the 4 .pack cards,
    the sticky bar.
 5. Shopify: fill CONFIG.variants (+ insuranceVariant) at the top of the <script>. Empty = buttons show
    a notice instead of a broken checkout. Never reuse variant IDs from another product.

 SECTION MAP (top -> bottom) – what each block is and how it behaves
  1  TOPBAR  .topbar      fixed orange bar: offer text + countdown #t-h/#t-m/#t-s (script, evergreen,
                          restarts at 0, stored in localStorage)
  2  HEADER  .header      logo (left) + small "JETZT BESTELLEN" button (all CTAs jump to #pakete)
  3  HERO    .hero-grid   LEFT .hero-img = animated MAIN image (before/after thumbnails, looping circle,
                          product, main character). RIGHT .hero-info = Trustpilot card .tp-card (date is set
                          automatically to "5 days ago") -> H1 -> .price-row -> 5 .bullets with check icons
                          -> .expert box (quote + round avatar) -> pulsing CTA -> guarantee line -> payments
  4  PRESS   .press       "Bekannt aus" = ENDLESS MOVING LOGO STRIP (marquee). How it works:
                          .press-track holds ONE set of logos; the script line
                          track.innerHTML += track.innerHTML duplicates them, and CSS
                          @keyframes marquee slides the track from translateX(0) to translateX(-50%) in 28s,
                          so the row scrolls left forever without a jump. .press has overflow:hidden.
                          .press-label ("★★★★★ Bekannt aus…") sits fixed in the middle on white with a white
                          glow (box-shadow), so logos slide behind it. Keep ALL of that (CSS + JS line).
                          In a static screenshot it simply looks like one row of logos.
  5-8b SECTIONS .sec      2 columns: text (.sec-text: h3 + 3 <p> + CTA + urgency line with .stock)
                          and a SQUARE image (.sec-img). Background alternates: .beige on S1, S3, S5.
                          .sec-grid.reverse = image LEFT (S2, S4). On mobile the image is always above the text.
                          S1 before/after · S2 mechanics · S3 step by step · S4 expert · S5 testimonial
  9  3 REVIEW CARDS #top-reviews .rev (photo + flag, name, "Verifizierter Käufer", stars + text)
                          + "MEHR ANSEHEN" (#more-btn: mobile = expands cards, desktop = scrolls to #bewertungen)
 10  CLOSING  .sec        guarantee section "30 Tage ohne Risiko", last paragraph completely bold
 11  TRUST    .trust      3 badges (fixed)
 12  FAQ      .faq        accordion, 2 columns x 5: .faq-item > button.faq-q + .faq-a (script opens/closes)
 13  PACKS    #pakete     4 cards 5x/3x/2x/1x; .pack.popular = highlighted 3x; .pack-btn[data-qty] builds the
                          Shopify cart link; #insurance checkbox adds the insurance variant
 14  REVIEW GRID #bewertungen  8 cards (4 columns desktop) + big CTA "SICHERN SIE SICH IHREN 50 % - RABATT"
 15  SUPPORT  .support    customer service block (fixed text + support e-mail)
 16  FOOTER   .footer     legal links + {{DISCLAIMER}}
 17  STICKY   #stickybar  fixed bottom bar (product image, name, price, CTA); appears after scrolling past the
                          hero (script toggles class .show)
=====================================================================================
-->
'''
t = t.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n' + GUIDE, 1)
t = t.replace('<!-- ===================== 4. BEKANNT AUS ===================== -->',
 '<!-- ===================== 4. BEKANNT AUS – endless logo marquee: ONE logo set here, the script duplicates it, CSS @keyframes marquee scrolls it; label stays centred ===================== -->')
t = t.replace('<!-- ===================== 3. HERO ===================== -->',
 '<!-- ===================== 3. HERO – left: animated main image · right: review card, H1, price, bullets, expert, CTA ===================== -->')
t = t.replace('<!-- ===================== 13. PAKETE ===================== -->',
 '<!-- ===================== 13. PAKETE – id="pakete" is the target of every CTA; images = product only (no box) ===================== -->')
assert t.count('{{') > 80 and 'ENDLESS MOVING LOGO STRIP' in t
open(D + 'template.html', 'w', encoding='utf-8').write(t)
shutil.copy(D + 'template.html', APP + 'template.html')
shutil.copy(D + 'build_images.py', APP + 'build_images.py')
img = open(D + 'build_images.py', encoding='utf-8').read()

# embed into the app as JS string constants (</ escaped so </script> inside cannot close the tag)
js = lambda s: json.dumps(s, ensure_ascii=False).replace('</', '<\\/')
block = '/*KIT_ASSETS_START*/\nconst TPL_PAGE = ' + js(t) + ';\nconst TPL_IMGSCRIPT = ' + js(img) + ';\n/*KIT_ASSETS_END*/'
a = open(APP + 'index.html', encoding='utf-8').read()
if '/*KIT_ASSETS_START*/' in a:
    a = re.sub(r'/\*KIT_ASSETS_START\*/.*?/\*KIT_ASSETS_END\*/', lambda m: block, a, flags=re.S)
else:
    a = a.replace('/* ---------- MASTER PROMPT ---------- */', block + '\n\n/* ---------- MASTER PROMPT ---------- */', 1)
open(APP + 'index.html', 'w', encoding='utf-8').write(a)
print('template', len(t), 'img script', len(img), 'app', len(a))
