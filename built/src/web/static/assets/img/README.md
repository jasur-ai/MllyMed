# Mahsulot fotolari (ixtiyoriy)

MllyMed kartalarida **generativ «pack shot»** ko'rsatiladi (nomdan deterministik SVG ko'rinish).
Agar ma'lum bir mahsulotning haqiqiy fotosurati bo'lsa, shu papkaga joylang:

- `frontend/assets/img/<product-id>.jpg` (yoki `.png`, `.webp`)
- `frontend/assets/img/manifest.json` ichida `{ "<product-id>": "assets/img/<product-id>.jpg" }` yozuvi bo'lsin

`manifest.json` o'zgarsa sahifani yangilang — karta avtomatik haqiqiy fotoya o'tadi.
