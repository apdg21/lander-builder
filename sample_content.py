# Placeholder content -> produces the REFERENCE TEMPLATE (sample page) used in the master prompt.
# Every {{TOKEN}} matches a slot ID of the copy template.
NAME='{{PRODUCT}}'; FULLNAME='{{PRODUCT_FULL}}'; KEY='{{PRODUCT_KEY}}'
TITLE='{{PRODUCT_FULL}} | 50 % Rabatt'
LOGO='logo.png'; LOGO_W=170; STICKY='sticky.png'
HERO_ALT='{{PRODUCT_FULL}} – {{HERO_IMAGE_ALT}}'
FORBIDDEN=[]
HERO_REVIEW=('{{HERO_REVIEW_NAME}}','{{HERO_REVIEW_TEXT}}')
H1='{{HERO_H1}}'
BULLETS=['{{HERO_BULLET_%d}}'%i for i in range(1,6)]
EXPERT_QUOTE='{{EXPERT_QUOTE}}'
EXPERT_NAME='{{EXPERT_NAME}} – {{EXPERT_TITLE}}'
def sec(k,img,alt): return {'title':'{{%s_TITLE}}'%k,'img':img,'alt':alt,'ps':['{{%s_P1}}'%k,'{{%s_P2}}'%k,'{{%s_P3}}'%k]}
S=[sec('S1','vorher-nachher.jpg','Vorher – Nachher'),
   sec('S2','mechanik.jpg','So funktioniert {{PRODUCT}}'),
   sec('S3','schritte.jpg','In 3 Schritten'),
   sec('S4','experte.jpg','Experte'),
   sec('S5','testimonial.jpg','Zufriedene Kunden')]
CLOSING=sec('CLOSING','abschluss.jpg','{{PRODUCT}} – 30 Tage ohne Risiko')
TOP3=[('{{REVIEW_%d_NAME}}'%i,'review-%02d.jpg'%i,'{{REVIEW_%d_TEXT}}'%i) for i in range(1,4)]
GRID=[('{{REVIEW_%d_NAME}}'%i,'review-%02d.jpg'%i,'{{REVIEW_%d_TEXT}}'%i) for i in range(4,12)]
FAQ=[('{{FAQ_%d_Q}}'%i,'{{FAQ_%d_A}}'%i) for i in range(1,11)]
DISCLAIMER='{{DISCLAIMER}}'
