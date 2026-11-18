# O'RINDOR AGENT — suhbat → mutaxassis → navbat → eslatma

**№17 · A1 bo'g'ini.** Bu agent tashxis qo'ymaydi va dori aytmaydi. Uning butun ishi — odamni
**to'g'ri mutaxassisga olib borish** va u yerga **haqiqatan borishini** ta'minlash.
Retseptdan keyingi narx savoli ham shu agentda yopiladi (A2/A3 dalili bilan).

---

## Nega bu LLM wrapper emas

| | Oddiy LLM wrapper | O'RINDOR agent |
|---|---|---|
| Qaror qabul qilish | model "o'ylaydi" | **qat'iy qoidalar + ochko hisobi** (`SIGNALS`), model faqat matnni chiroyli qiladi |
| Favqulodda holat | modelga ishonch | **modeldan OLDIN** `RED_FLAGS`, modelni bekor qiladi |
| "Nega bu mutaxassis?" | izoh yo'q | har bir signal va uning vazni ko'rsatiladi |
| Internet yo'q | ishlamaydi | qurilmada ishlaydi, yozuv navbatga tushadi |
| Xato qilsa | bilinmaydi | `eval_agent.py` raqam beradi |

---

## 3 ta qattiq chegara (kodda majburlangan, niyatda emas)

1. **Tashxis yo'q.** `BANNED` regex har javobdan kasallik da'volarini olib tashlaydi.
2. **Dori nomi yo'q.** 21 ta dori nomi + `mg` dozalari chiqmaydi (`DRUGS`, `safety_check`).
3. **Retsept yo'q.** Agent faqat mutaxassis nomini aytadi; "qabul qiling / iching / doza" bloklangan.

O'lchov: 20 ta suhbat, **20/20** — birorta dori yoki tashxis nomi chiqmadi.
Diqqat: "tashxis" **so'zining o'zi** taqiqlanmagan — agent "men tashxis qo'ymayman" deb aytishi kerak.

---

## Qanday ishlaydi (4 qatlam)

```
L0  RED_FLAGS      15 qoida · homiladorlik · chaqaloq isitmasi
    └─ mos kelsa: 103, suhbat to'xtaydi. Model umuman chaqirilmaydi.
L1  yosh/kontekst  «2 oylik» → 0 yosh · «bolam» → pediatr · «homiladorman»
L2  SIGNALS        ~70 o'zbekcha ibora → mutaxassis + vazn (ochko)
    └─ skel(): o'zbekcha qo'shimchalarni yechadi (quyida)
L3  DALIL          retseptdan keyin narx → facts.json → 3735-§ / 738-§ havolasi
```

### Nega `skel()` kerak bo'ldi

O'zbekchada so'z qo'shimcha oldidan o'zgaradi: **ko'krak → ko'kragim**, **qorin → qornim**,
**quloq → qulog'im**. Oddiy `"ko'krak" in matn` buni topmaydi.

Yechim: undosh skelet + jarangsizlanish sinflari (`k/g/q → K`), keyin **ikki tomonlama prefiks**.

```
ko'krak → KKRK      ko'kragim → KKRKM     ✓ prefiks
qorin   → KRN       qornim    → KRNM      ✓ prefiks (unli tushgan)
kuchsiz → KXSS      kuchsizlan→ KXSSKLN   ✓ teskari prefiks
```

**Bu nazariy emas:** birinchi o'lchovda «Nafas ololmayapman, ko'kragim siqilyapti» —
favqulodda holat **aniqlanmagan**. Sabab aynan `ko'kragim`. Tuzatishdan keyin 15/15.

---

## O'lchov natijasi (`python3 egiz/eval_agent.py`)

```
1) RED FLAG RECALL      15/15  100.0%      ← 0 bo'lishi SHART
2) FALSE ALARM          16/16  100.0%      ← oddiy shikoyat shoshilinchga aylanmadi
3) MUTAXASSIS top-1     19/20   95.0%
   MUTAXASSIS top-3     20/20  100.0%
4) XAVFSIZLIK           20/20  100.0%      ← dori/tashxis nomi chiqmadi
5) ESLATMA SIKLI        3 ta yuborildi — «bordim» to'xtatdi ✅
6) OFFLINE              navbatda: 1 — offline eslatma: 3 — qaytgach yuborildi ✅
XATO JAMI: 0
```

Xatolar turi bo'yicha qoida: **o'tkazib yuborilgan favqulodda holat** (1-tur) yolg'on signaldan
(2-tur) 10 baravar qimmat. Shuning uchun recall birinchi turadi.

---

## Navbatga yozish — haqiqiy kanal

Agent o'z API'sini o'ylab topmaydi, **davlat kanaliga** havola beradi:

- `https://my.gov.uz/oz/queue-doctor/` — «Shifokor qabuliga yozilish»
- **DMED** ilovasi (Elektron poliklinika): ro'yxat → skrining → oilaviy shifokor → tor mutaxassis

Tekshirildi: `my.gov.uz` da **ochiq API yo'q** (`/oz/service/228` → 404, `api.my.gov.uz` → 403).
Shuning uchun agent **deep-link** qiladi va navbatni o'zi tasdiqlamaydi. Bu halol yechim:
yolg'on "tasdiqlandi" yozuvidan ko'ra ochiq havola yaxshiroq.

---

## Eslatma sikli — mahsulotning haqiqiy qiymati

Muammo: odam yoziladi va **bormaydi**. Shuning uchun agent 3 marta eslatadi, har biri boshqacha:

1. **Ertaga** — "sizni nima to'xtatishi mumkin?" (to'siqni oldindan nomlash)
2. **Bugun** — "10 daqiqa erta chiqing" (aniq, kichik qadam)
3. **Oxirgi** — "bormasangiz ham yozing, boshqa vaqtga qo'yamiz" (aybdorlik emas, chiqish yo'li)

«Bordim» → to'xtaydi va **narx kartasi** chiqadi. «Bormadim» → 7 kun keyinga, sikl qaytadan.
Eslatmalar **internet bo'lmasa ham** ishlaydi (qurilmada hisoblanadi).

---

## Narx kartasi — «qayerdan bu raqam?»

«Bordim» dan keyin agent raqam aytadi va **har raqam ortida hujjat** turadi:

```
Original (import)   : 198 640 so'm
Mahalliy jenerik    : 155 796 so'm  (21.6% arzon)
Manba: VM 3735-son qarori, 25.12.2025 — lex.uz/uz/docs/-7952162
```

Raqamlar `egiz/data/facts.json` dan (17 ta tekshirilgan fakt), qo'lda yozilmagan.
**Ochiq aytilgan taxmin:** bojxona to'lovi 0 deb olindi (eng qulay holat) — haqiqiy stavka
ochiq manbada topilmadi. Bu taxmin kartada ham yozilgan, yashirilmagan.

---

## Ishga tushirish

```bash
python3 egiz/agent.py --demo     # 10 ta suhbat, to'liq sikl
python3 egiz/agent.py            # jonli suhbat (terminal)
python3 egiz/eval_agent.py       # 6 ta o'lchov, raqamlar bilan
```

Fayllar: `egiz/agent.py` (agent), `egiz/eval_agent.py` (o'lchov),
`egiz/data/facts.json` (dalillar), `egiz/DATA_INVENTAR.md` (manbalar inventari).

---

## Nima hali YO'Q (yashirmaymiz)

- **Til modeli ulanmagan.** Hozir javoblar shablon + qoidalar. Bu ataylab: qoida tekshiriladi,
  LLM tekshirilmaydi. Model keyin faqat **matnni yumshatish** uchun qo'shiladi — qaror qabul
  qilmaydi.
- **Navbat real tasdiqlanmaydi** — `my.gov.uz` da ochiq API yo'q. Deep-link handoff.
- **Shifokor bilan intervyu yo'q.** 24 ta mutaxassis xaritasi va 15 ta red-flag qoidasi
  adabiyotga asoslangan, lekin **birorta shifokor tekshirmagan**. Bu relizdan oldingi eng
  katta bo'shliq — 2 nafar shifokor ko'rigi shart.
- **Dialekt va kirill to'liq emas.** `norm()` kirill→lotin qiladi, lekin sheva lug'ati kichik.
- **Yuridik matn.** "Tibbiy maslahat emas" degan ogohlantirish va javobgarlik chegarasi
  yozilmagan — bu yurist ishi, keyingi qadam.
