# CP8 — SQLite domen: rollar, dispense, audit

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

v1 da DMED holati JSON faylda edi: parallel so'rovlarda poyga, audit yo'q,
"kim berdi" savoliga javob yo'q. Katta mahsulotga tranzaksiyali domen kerak.

## Sxema (`data/runtime/dmed.db`)

```sql
appointments(id, patient, doctor_id, specialist, slot, status,
             created_at, confirmed_at, confirmed_by)
  UNIQUE(doctor_id, slot) WHERE status IN ('requested','confirmed')
prescriptions(id, patient, doctor_id, doctor, inn, inn_key,
              status, created_at, signed_at, signed_by)
orders(id, rx_id, patient, pharmacy, offer_id, name, price,
       status, created_at, dispensed_at)
audit(id, at, actor, role, action, entity, entity_id, payload)
```

Statuslar: `requested → confirmed | cancelled`; `draft → signed → dispensed`.

## Ruxsat matritsasi

| Amal | Rol | Qo'shimcha shart | Rad etilganda |
|---|---|---|---|
| navbat ochish | patient | slot bo'sh | 403 / 400 |
| tasdiqlash | patient (`actor="user"`) | status `requested` | 403 |
| retsept yozish | doctor | XPN reyestrda | 403 / 400 |
| imzolash | doctor (`actor="doctor_sim"`) | status `draft` | 403 |
| berish | pharmacist | status `signed` + XPN mos | 403 / 400 |

Har mutatsiya `audit` ga yoziladi: `at, actor, role, action, entity, payload`.

## Natija

E2E (rol sarlavhalari bilan):

```
draft 200 → sign 200 → dispense (bemor) 403 → dispense (farmatsevt) 200
order.status=dispensed · price=56 000 · audit 3 qator · queue (bemor) 403
```

Testlar: `17/17 OK` — jumladan `test_dispense_requires_signed_and_role`,
`test_dispense_wrong_inn_rejected`, `test_only_patient_books`.

## Qarorlar

- **Tasdiq:** SQLite (stdlib) — tashqi servis yo'q, fayl ko'chiriladi.
- **Tasdiq:** har amalda `_conn()` context manager (lock muammosi yo'q).
- **Tasdiq:** XPN mosligi `canon_inn` bo'yicha (`parasetamol` ≈ `paratsetamol`).
- **Rad:** imzolangan retseptni o'zgartirish — statuslar orqali taqiqlangan.
- **Rad:** dorini bemor tasdiqlashi — bu farmatsevt amali.
- **Rad:** haqiqiy qoldiqni da'vo qilish — `pharmacies` soni bor, `stock` yo'q.

## Keyingi qadam

CP9: 4 portalli UI va analitika paneli.
