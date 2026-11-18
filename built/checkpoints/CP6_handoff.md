# CP6 — handoff

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Nima tayyor

| Qism | Holat |
|---|---|
| Yadro (46 079 dori, 2 941 XPN, 12 423 narx) | ✅ vendor + manifest |
| Dorixona katalogi (68 mahsulot, 25 XPN) | ✅ real ma'lumot |
| XPN ↔ reyestr bog'lash | ✅ 9/25, usul ko'rinadi |
| 80% proxy tekshiruv | ✅ 3 holat |
| Mini DMED (27 shifokor, 25 mutaxassis) | ✅ sintetik + ruxsatlar |
| Navbat: request → user confirm | ✅ `PermissionError` bilan himoyalangan |
| Retsept: XPN + doctor_sim imzo | ✅ audit jurnal |
| Bridge + veb UI | ✅ stdlib, 0 bog'liqlik |
| Virtual tajriba | ✅ 12/12 |
| Hujjatlar (BRAIN, CP0–CP6, decisions) | ✅ |

## Tekshiruv dalillari

```bash
cd orindor && python eval_agent.py        # 10/10 suite · JAMI XATO: 0 · exit 0
cd built && python build.py --check       # ✅ CHECK OK · 20 fayl
cd built && python -m unittest discover -s tests   # 12/12 OK
cd built && python sim/run.py             # 12/12 · exit 0
cd built && python -m src.web.server --port 8211
#   /api/health → {"ok": true, "synthetic": true}
#   /api/apteka/inn/ezomeprazol → count 4 · 80% dan qimmat · DV/M 03799/04/21
#   / → HTTP 200 · 12 858 B
```

## Nima hali yo'q (yashirmaymiz)

1. **GMP qatlami** — `uzpharm-gxp.uz` bu muhitda DNS'da yo'q; reja
   `orindor/AGENT.md` 9-bo'limda.
2. **Katalog kichik** — 68 mahsulot; to'liq katalog uchun sheriklik.
3. **Klinik ko'rik yo'q** — 12 stsenariy texnik regression, tibbiy isbot emas.
4. **DMED sintetik** — haqiqiy API yo'q; UI buni ochiq yozadi.
5. **Autentifikatsiya yo'q** — demo uchun.

## Keyingi 3 ish (tartib bilan)

1. `data/gmp.json` yig'ish (HTML jadval parser) + kartada GMP qatori.
2. Katalogni 100–200 mahsulotga kengaytirish, bog'lanish sifatini o'lchash.
3. Simni 40 stsenariyga kengaytirish (inkor, homiladorlik, imlo xatolari).

## Qanday davom ettirish

`BRAIN.md` 8-bo'limidagi runbook. Har o'zgarishdan keyin:
`build.py --check` → `unittest` → `sim/run.py` → yangi CP fayl +
`decisions.jsonl` qatori.
