# CP2 — dorixona konnektori (arzon_apteka mini + apteka.uz)

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

XPN bo'yicha dorixona takliflarini ko'rsatish va 3735-son F09 ni **proxy**
sifatida tekshirish — sotish emas, hukm chiqarish.

## API

| Funksiya | Nima qaytaradi |
|---|---|
| `search(q)` | nom / XPN / ishlab chiqaruvchi bo'yicha qidiruv |
| `by_inn(inn)` | faqat XPN bog'langan mahsulotlar, narx bo'yicha |
| `price_check(group)` | `mos` · `80% dan qimmat` · `tekshirib bo'lmadi` |
| `registry_view(inn)` | reyestr guruhi, reg raqami, narx qamrovi |
| `summary(inn)` | yuqoridagilar + `link` (usul, ishonch) |
| `coverage()` | nechta XPN reyestrga bog'landi |

## XPN bog'lash — uch bosqich

1. **exact** — katalog kaliti reyestrda aynan bor.
2. **fuzzy** — `difflib` ≥0.90 (`parasetamol` → `paratsetamol`, 0.957).
3. **contains** — tuz qo'shimchasi farqi, qisqa tomon ≥8 belgi va ≥0.75.

Bog'lanmasa — `none`; `by_inn` bo'sh qaytaradi, UI «ma'lum emas» deydi.
Taxmin yashirilmaydi: javobda `link.method` va `link.score` ko'rinadi.

## Natija

```
25 XPN guruhi → 9 tasi reyestrga bog'landi
  parasetamol → paratsetamol (fuzzy 0.957)
  azitromisin → azitromitsin (fuzzy 0.957)
  levofloksasin → levofloksatsin (fuzzy 0.963)
  pirasetam → piratsetam (fuzzy 0.947)
  qolgan 16 guruh — reyestrda topilmadi (ko'pchiligi o'simlik ekstraktlari)
```

## Qarorlar

- **Tasdiq:** imlo farqini avtomatik bog'lash, lekin usul/ishonchni ko'rsatish.
- **Tasdiq:** 80% tekshiruvida faqat `local is True/False` bo'lgan yozuvlar —
  `null` hisobga olinmaydi.
- **Rad:** `local=null` ni import deb hisoblash — noto'g'ri xulosa.
- **Rad:** `price_check` ni "qonun buzilgan" deb atash — bu **proxy**,
  referent narx reyestri yopiq.

## Dalil

```bash
cd built && python -m unittest discover -s tests -v
# TestApteka: 5/5 (counts, arzon, spelling, by_inn, price states)
```

## Keyingi qadam

CP3: mini DMED va ruxsat qoidalari.
