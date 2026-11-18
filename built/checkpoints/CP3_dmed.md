# CP3 — mini DMED (simulyatsiya, qat'iy ruxsatlar)

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

Retsept va navbat oqimini ko'rsatish — lekin **haqiqiy bron va haqiqiy
imzo** taassurotini bermasdan. `arxiv/` xulosasi: DMED — platforma egasi,
biz uning ustidagi modulmiz.

## Seed (sintetik)

- 3 klinika (Chilonzor, Yunusobod, Mirzo Ulug'bek)
- 27 shifokor, 25 mutaxassis (reyestrdagi `SPECIALISTS` kalitlari bilan mos)
- Slotlar: bugundan 7 kun, 09:00–17:00, 30 daqiqa, tushlik 13:00;
  band slot deterministik (`sha256(doctor|slot) % 7`).

Hammasi `meta.synthetic = true` va `SYNTHETIC_NOTE` bilan belgilangan.

## Ruxsat matritsasi (kodda)

| Amal | Kim | Rad etilganda |
|---|---|---|
| `create_appointment` | foydalanuvchi tanlovi | bo'sh bo'lmagan slot → `ValueError` |
| `confirm_appointment` | **faqat `actor="user"`** | `PermissionError` |
| `cancel_appointment` | faqat `actor="user"` | `PermissionError` |
| `create_prescription` | shifokor; XPN reyestrda bo'lishi shart | `ValueError` |
| `sign_prescription` | **faqat `actor="doctor_sim"`** | `PermissionError` |

Har amal `data/runtime/dmed_audit.jsonl` ga yoziladi:
`appointment.requested / confirmed / cancelled`, `prescription.draft / signed`.

## Qarorlar

- **Tasdiq:** ikki bosqichli navbat (`requested` → `confirmed`) — "agent
  band qildi" degan yolg'ondan qochadi.
- **Tasdiq:** retsept faqat **XPN** bo'yicha; erkin matn rad etiladi.
- **Tasdiq:** imzo funksiyasi alohida nom bilan (`prescription_sign`) —
  chaqiruvchi nima qilayotganini ko'radi.
- **Rad:** haqiqiy DMED API'siga so'rov — ochiq API yo'q.
- **Rad:** "navbat tayyor 09:30" degan avtomatik javob — critic P2.

## Dalil

```bash
cd built && python -m unittest discover -s tests -v
# TestDMed: 4/4 (unknown doctor, agent cannot confirm, INN required, only doctor signs)
```

## Keyingi qadam

CP4: bridge va veb-qatlam.
