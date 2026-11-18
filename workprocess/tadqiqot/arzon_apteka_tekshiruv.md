# ArzonApteka — ma'lumot tekshiruvi

**Sana:** 2026-11-18 · **Kim tekshirdi:** O'RINDOR · **Xulosa:** ma'lumot bor, lekin **kerakli qismi yopiq**.

---

## 1. Nima ochiq, nima yopiq (tekshirilgan, taxmin emas)

| Qism | Holat | Dalil |
|---|---|---|
| `arzonapteka.uz` bosh sahifa | ✅ ochiq, server-render | 200, 294 KB, **20 unikal mahsulot** |
| Qidiruv (`/uz/search`) | ❌ yopiq | HTML bo'sh — brauzerda chiziladi |
| Katalog (`/uz/catalog`) | ❌ yopiq | 0 ta mahsulot karta |
| Dorixona sahifasi (`/uz/org/1890`) | ❌ yopiq | 0 karta |
| `api.arzonapteka.uz` | 🔒 **auth kerak** | `401 MISSING_SESSION_HEADER` — «X-Session-Id header is required» |
| `robots.txt` | ⚠️ | `Allow: /` · **`Disallow: /api/`** — API'ga robot sifatida kirish taqiqlangan |
| `robots.txt` da `/api/partners/` | 💡 **sheriklik API'si bor** | ya'ni rasmiy yo'l mavjud |

**Muhim:** bosh sahifadagi 20 ta mahsulot **qotib qolgan** — 4 marta ketma-ket yuklab tekshirdim,
ro'yxat o'zgarmadi. Ya'ni takroriy yig'ish bilan katalog to'ldirib bo'lmaydi.

---

## 2. Nima yig'ildi (real, saqlangan)

`orindor/data/arzon_sample.json` — 20 yozuv, har birida:

```
nom · ishlab chiqaruvchi · narx ("X so'mdan") · retsept belgisi · rasm ID · manba URL · olingan vaqt
```

Natija:

```
unikal mahsulot : 20
narxi bor       : 19 / 20
ishlab chiqaruvchi: 20 / 20
retseptli       : 13 / 20
narx oralig'i   : 2 000 – 1 393 500 so'm
mahalliy ishlab chiqaruvchi: 2 / 20   (Merrymed Farm, Nobel-Pharmsanoat)
```

**Bu raqamning o'zi №17 ning ko'rinishi:** vitrinada 20 ta doridan **18 tasi import**.
Mahalliy mahsulot bor, lekin ko'rinmaydi.

---

## 3. Eng muhim topilma — bu mahsulot g'oyasini o'zgartiradi

ArzonApteka'ning o'z qidiruv maydonida yozilgan:

> «Qidiramiz: **nomi · XPN · brend nomi**»

Ya'ni **XPN (INN) bo'yicha qidirish allaqachon ishlaydi** — bozor yetakchisida, bepul.
Men o'tgan safar taklif qilgan "INN kartasi" g'oyasining eng sodda ko'rinishi —
"INN yozasiz, muqobillar chiqadi" — **allaqachon bor**.

Demak O'RINDOR ning qiymati qidiruvda emas. U faqat shu uchta savolga javob berganda
takrorlanmas bo'ladi:

1. **Reyestrda bormi** — davlat ro'yxatidan o'tganmi, raqami va muddati bilan.
2. **Asl belgisi bormi** — qalbaki emasmi (VM 737 / 149).
3. **3735 bo'yicha narx shifti qancha** — referent narx oshib ketganmi.
4. Va eng muhimi: **dalil yo'q bo'lsa «ma'lum emas» deb yozish** — ArzonApteka buni qilmaydi,
   chunki uning ishi sotish, bizning ishimiz — hukm.

Ya'ni raqobat "kim qidiradi" da emas, **"kim hujjat ko'rsatadi"** da.

---

## 4. O'RINDOR ning kerakli maydonlari — bor-yo'qligi

| Kerak | ArzonApteka ochiq sahifasida | Izoh |
|---|---|---|
| Savdo nomi | ✅ | «Кортексин, 5 мг, флак. №10» |
| Ishlab chiqaruvchi | ✅ | 20/20 |
| Narx (eng past) | ✅ 19/20 | «X so'mdan» — aniq dorixona emas |
| Retsept belgisi | ✅ | 13/20 |
| **XPN (INN)** | ❌ | qidiruvda ishlatiladi, lekin ochiq maydon sifatida berilmaydi |
| **Reyestr raqami** | ❌ | yo'q |
| **Asl belgisi / GTIN** | ❌ | yo'q |
| **Referent narx (3735)** | ❌ | yo'q |
| **Dorixona bo'yicha narx tarqalishi** | ❌ | faqat «eng past» ko'rsatiladi |
| **Doza / shakl (alohida maydon)** | ⚠️ | faqat nom ichida, matn sifatida |
| **Bioekvivalentlik** | ❌ | hech qayerda yo'q |

**Xulosa:** O'RINDOR yadrosi uchun kerakli 10 ta maydondan ochiq yo'l bilan **4 tasi** olinadi.
Qolgan 6 tasi — yopiq.

---

## 5. Nima qilish kerak (uch yo'l, tannarxi bilan)

| Yo'l | Nima beradi | Narxi | Tavsiya |
|---|---|---|---|
| **A. Rasmiy sheriklik so'rovi** | `/api/partners/` bor; kontakt: **+998 71 207-08-08**, **info@fom.group** (FOM Group), `@ArzonAptekaSupportBot` | 1 xat + 1 qo'ng'iroq | ✅ **birinchi** — eng arzon, eng qonuniy |
| **B. Boshqa ochiq manba** | `apteka.uz` — alohida mahsulot sahifasi server-render, narx + sotuvchi + manzil bor; lekin katalog va qidiruv ham yopiq | 2–3 soat | ⚠️ zaxira |
| **C. Skript bilan yig'ish (scraping)** | 20 ta mahsulot — tamom. Katalog yopiq, `robots.txt` `/api/` ni taqiqlaydi | arzon, lekin **foydasiz** | ❌ qilmaymiz |

**Qaror:** C rad etildi — hurmat masalasi ham, amaliy ham (20 ta yozuv mahsulot qurmaydi).
A — birinchi qadam. Xat matni keyingi ishda yoziladi.

---

## 6. Nimani o'zgartirish kerak (agent bo'yicha)

Tekshiruvdan keyingi ikkita qat'iy xulosa:

1. **INN qidiruvini "yangilik" deb ko'rsatib bo'lmaydi.** Hakam buni bir daqiqada tekshiradi.
   Taqdimotda ochiq aytish kerak: "INN qidiruvi bor — bizda **hujjat qatlami** bor".
2. **Narx bo'yicha raqobat — yo'q.** Ular «X so'mdan» deydi (sotish uchun). Biz «qonun bo'yicha
   shift shu» deymiz (hukm uchun). Ikki xil gap, ikkisi ham kerak.

---

## 7. Takrorlash

```bash
python3 orindor/tools/arzon.py      # 20 ta mahsulotni qayta yig'adi
```

Skript faqat ochiq sahifalarni o'qiydi, `/api/` ga tegmaydi, har yozuvga manba va vaqt qo'yadi.
