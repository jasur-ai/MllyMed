
Agentni ishga tushirib, kodni o'qib, yangi iboralarda sinab ko'rdim. Endi xulosani yozyapman, avval xotiraga qisqa yozuv qo'shaman.

# Örindor agenti: qattiq tahlil va kuchaytirish

Zipni ochdim, `agent.py` ni o'qidim, `eval_agent.py` va demoni ishga tushirdim, keyin o'zim yangi iboralarda sinadim.

## Umumiy hukm

Agent g'oya jihatidan yaxshi, lekin **hozirgi shaklida jonli demoda sinsa, sizni uzishi mumkin**. Uchta asosiy sabab:

1. Zipda **№17 yadrosi yo'q**.
2. Favqulodda holat qoidalari **yangi iboralarda ishlamaydi**.
3. Demo bir necha joyda **bajarilmagan narsani bajarilgandek** ko'rsatadi.

Pastda har biri dalil bilan.

## 1. Strategik muammo: zipda yadro yo'q

Zipdagi narsalar: agent, uning eval'i, lex.uz yig'uvchi, ma'lumot fayllari. **Ishonch kartasi dvigateli, INN bo'yicha qidiruv, mahsulot jadvali umuman yo'q.**

- `real_products.json` ichida **300 ta AQSh (openFDA) yozuvi** bor (Walmart, Amazon atsetaminofeni). O'zbekiston reyestri `PENDING`. Hakam bu faylni ochsa "bu O'zbekiston emas" deydi.
- `AGENT.md` agentni "№17 · A1 bo'g'ini" deb nomlagan. Bu noto'g'ri: agent haqiqiylikka aloqasiz, u mutaxassisga yo'naltirish va eslatma. Yuqorida kelishganimizdek bu 3-qatlam.
- Hujjatlardagi buyruqlar (`python3 egiz/agent.py`) papka nomi `orindor` bo'lgani uchun ishlamaydi. `facts.json` ichida ham eski "EGIZ" nomi qolgan.

Soat 07:40, checkpoint 15:00. Ustuvorlik teskari: **sayqallangan 3-qatlam bor, 1-qatlam bo'sh.**

## 2. Xavfsizlik: o'lchangan natijalar noto'g'ri tasavvur beradi

Eval'dagi `15/15` va `0 xato` ni men takrorlay oldim, lekin bu **o'sha 15 ta ibora bilan sozlangan to'plam**. Men 24 ta yangi, alohida yozilgan favqulodda ibora bilan sinadim (informal sinov, tadqiqot emas):

| Ibora                                                           | Agent javobi                                      |
| --------------------------------------------------------------- | ------------------------------------------------- |
| "Qon qusdim"                                                    | **Oftalmolog**                              |
| "Tushkunman"                                                    | **Stomatolog** (psixiatrdan oldin)          |
| "Kasalman"                                                      | **Oftalmolog**                              |
| "Ko'krak og'riyapti" (yolg'iz)                                  | Kardiolog, **"1 hafta"** (shoshilinch emas) |
| "Yuzimning yarmi qimirlamayapti"                                | Dermatolog                                        |
| "Bolam tutqanoq tutdi"                                          | Terapevt (fallback)                               |
| "Qornimning o'ng tomoni qattiq og'riyapti, qusdim, isitmam bor" | Gastroenterolog, **1 hafta**                |
| "Ko'p kunlardan beri holsizman"                                 | **103 shoshilinch** (yolg'on signal)        |
| "3 kundan beri boshim kuchli og'riyapti"                        | **"To'xtamaydigan qon ketish" signali**     |

24 ta favqulodda iboradan **14 tasi o'tkazib yuborildi** (inme belgisi, qon qusish, tutqanoq, bo'g'ilish, ruscha va kirill iboralar). Yolg'on signal 12 ta oddiy gapdan 7 tasida chiqdi.

**Asosiy sabab:** `skel()` undosh skeleti juda yumshoq. 2 harfli skeletlar ko'p so'zga mos keladi:

- `qon` ≈ **kun**, kunduz
- `gap` ≈ **ko'p**
- `yuz` ≈ **yosh**
- `hush` ≈ **hozir**
- `ko'z` ≈ **kasal**
- `tish` ≈ **tush**kun

Ikkinchi sabab: leksikon bo'shliqlari ("nafasim yetmayapti", "qusdim", "tutqanoq", "terlab") va ruscha qatlam yo'qligi, garchi docstring "UZ + RU" desa ham.

**Eval nega yaroqsiz:**

- Qoidalarni ham, test iboralarini ham bir muallif yozgan.
- `4) XAVFSIZLIK 20/20` bema'ni: agent javoblari shablon, shuning uchun dori yoki tashxis nomi chiqishi mumkin emas edi. Bu LLM qo'shilgandan keyingina ma'noga ega.
- 5 va 6-testlar faqat "baxtli yo'l"ni tekshiradi.

## 3. Demo halolligi

1. **"Navbat tayyor ... 20.11.2026, 09:30"**: vaqt va sana kod tomonidan o'ylab topilgan (bugun + kunlar, soat 09:30). Hech narsa bron qilinmagan. Foydalanuvchi buni haqiqiy navbat deb o'ylaydi.
2. **Eslatmalar vaqt bo'yicha emas.** Ular faqat foydalanuvchi **biror narsa yozganda** chiqadi. Demoda "35" yoki "40" (yosh javobi) eslatmani chaqiradi. Haqiqiy taymer yoki push yo'q.
3. **"Offline ishlaydi"**: `OfflineQueue` xotiradagi ro'yxat, `sync()` uni shunchaki tozalaydi. Hech narsa saqlanmaydi va yuborilmaydi.
4. **"Bordim" dan keyingi narx kartasi** har suhbatda bir xil gipotetik misolni (126 000 so'm) chiqaradi, hatto ko'z shifokoriga borgandan keyin ham. Ekranda "misol" deb yozilmagan.
5. **Yosh ajratish xatosi:** "2 yil" (davomiylik) yosh 2 deb olinadi va pediatrga o'tadi. "Bolam" yozilsa yosh avtomatik 4 qilib qo'yiladi.

## 4. Yaxshi tomonlari (haqiqiy kuch)

- **Qonun matni haqiqiy.** lex.uz dan olingan matnlarda quyidagilar so'zma-so'z topildi: 738-sondagi "2029-yil 1-yanvardan ... ICH ... majburiy" bandi va 3735-sondagi "jenerik ... referent narxlari originalnikining 80 foizidan qimmat bo'lishi mumkin emas" bandi. 15% ulgurji va 20% chakana ustama chegaralari ham matnda bor. Hisob ham to'g'ri: 198 640 va 155 796 so'm, farq 21.6%. Bu mening avvalgi "tekshirilmagan" ogohlantirishimni yopadi va S2/S4 uchun **haqiqiy** kuch.
- Arxitektura g'oyasi to'g'ri: favqulodda qoidalar modeldan oldin, har fakt yonida manba, "nima yo'q" bo'limi halol.
- Undosh skeleti g'oyasi o'zbek morfologiyasi uchun aqlli, faqat qattiqroq qilish kerak.

**Narx haqida bitta aniqlik:** qonun **chegara** belgilaydi ("ortiq bo'lmagan"). 21.6% bu ruxsat etilgan eng yuqori narxlar farqi, dorixonadagi haqiqiy narx farqi emas. Haqiqiy referent narxlar reyestri yopiq.

## 5. Kuchaytirish rejasi (ustuvorlik tartibida)

**P0. Xavfsizlik (agentning ishonchi uchun, ~2 soat)**

1. Skelet moslashuvini qat'iylashtiring: 4 belgidan qisqa asoslarni olib tashlang, to'liq so'z chegarasi bo'yicha moslang. 2–3 harfli signallarni (`qon`, `gap`, `yuz`, `hush`, `ko'z`, `tish`, `hid`, `ayol`, `yara`, `uyqu`) ko'p so'zli iboralarga almashtiring.
2. **Majburiy skrining savollari:** ko'krak, bosh og'rig'i, qorin, ko'rish o'zgarishi, bolada isitma uchun 1–2 ha/yo'q savol (birdan boshlandimi, nafas qisilishi, terlash, qo'l uvishishi) **marshrutlashdan oldin**. Javob yo'q yoki noaniq bo'lsa shoshilinch deb hisoblang.
3. **Xavfsiz default:** yuqori xavfli so'z (ko'krak, nafas, qon, hush, bolada isitma) bor, lekin xavf rad etilmagan bo'lsa, "1 hafta" emas, **"bugun ko'rsating"**.
4. Yosh ajratishdan "yil" ni olib tashlang, "bolam" uchun yosh so'rang.

**P1. Haqiqiy baholash (~1.5 soat)**

- Sozlashda ishlatilmagan **60+ ibora**, boshqa odam (jamoadosh yoki LLM, keyin shifokor tekshirgan) yozsin: inkor, uchinchi shaxs, kirill, ruscha, imlo xatolari.
- Yolg'on signalni **100 ta oddiy gapda** sinang (ichida "kun", "ko'p", "hozir", "yosh").
- Natijani "100%" deb emas, aniq son va chegara bilan ayting.

**P2. Demoni halol qilish (~40 daqiqa)**

- "Navbat tayyor" o'rniga: "my.gov.uz orqali vaqtni o'zingiz tanlaysiz; men eslatma rejalashtiraman". Vaqtni foydalanuvchi kiritsin.
- Eslatmalar: haqiqiy taymer (Telegram bot yoki PWA bildirishnomasi) yoki ochiq belgi: **"simulyatsiya, vaqt tezlashtirilgan"**.
- Offline da'vosini olib tashlang yoki mahalliy saqlashni haqiqatan yozing.
- Narx kartasiga **"MISOL"** yorlig'i qo'ying.

**P3. Agentni №17 ga ulash (eng katta ball manbai)**
Agentni ikki rejimli "Örindor yordamchi" qiling:

1. **Retsept rejimi (yadro):** INN yoki dori nomi → ishonch kartasi. Foydalanuvchi "nega arzon?", "ishonsa bo'ladimi?" desa, agent **faqat `facts.json` dagi faktlardan** va kartadan javob beradi, har javobda fakt raqami (F09 va h.k.) va havola bor. Dalil bo'lmasa "ma'lum emas".
2. **Yo'naltirish rejimi (mavjud triaj):** ikkinchi darajali, "keyingi qadam".

**LLM faqat tilni boshqaradi:** o'zbek, rus, kirill tushunish (strukturali niyat va maydonlarga), va javobni sodda tilga o'tkazish. Chiqishni **validator** tekshirsin: faktlarda yo'q raqam, dori nomi, doza yoki tashxis bo'lsa rad etsin. Shunda 4-test (xavfsizlik) birinchi marta ma'noli bo'ladi. Bu T3/T5 uchun "AI qayerda?" savoliga javob ham.

**P4. Yadro ma'lumoti (~2–3 soat, boshqa jamoadoshlar bilan parallel)**

- O'zbekiston reyestri yopiq bo'lsa, 30 INN ni qo'lda jadvalga yig'ing: har qatorda **manba URL va sana**.
- `openFDA` faylini `reference/` papkasiga olib chiqing yoki repodan olib tashlang.
- Bitta shifokor 15 ta favqulodda qoidani va mutaxassis xaritasini ko'rib chiqsin. `AGENT.md` ning o'zi buni "eng katta bo'shliq" deb yozgan.
- "Tibbiy maslahat emas" ogohlantirishi va chegara matnini qo'shing.

## 6. Ball ta'siri

| Mezon | Hozir    | P0–P3 dan keyin                                    |
| ----- | -------- | --------------------------------------------------- |
| T2/T3 | 6–7 / 7 | 7–8 / 8 (halol eval + qoida+LLM chegarasi)         |
| T5    | 6        | 7 (LLM faqat tilda, validator bilan)                |
| S2/S4 | 8 / 6–7 | 8–9 / 7–8 (qonun iqtiboslari kartada, xavfsizlik) |
| S3    | 6–7     | 7 (yadro oqimi ishlaydi)                            |

**Eng katta xavf:** hakam jonli "Qon qusdim" yoki "Yuzim qiyshaydi" deb yozsa va oftalmolog chiqsa, butun mahsulotga ishonch tushadi. Shuning uchun P0 hamma narsadan oldin.

**Tavsiya:** agentga 3 soatdan ortiq ketkazmang. P0+P2 (xavfsizlik va halollik), keyin P3 (yadroga ulash). Qolgan vaqt yadro kartasi va ma'lumot jadvaliga.

Agentni ishga tushirib, kodni o'qib, yangi iboralarda sinab ko'rdim. Endi xulosani yozyapman, avval xotiraga qisqa yozuv qo'shaman.

# Örindor agenti: qattiq tahlil va kuchaytirish

Zipni ochdim, `agent.py` ni o'qidim, `eval_agent.py` va demoni ishga tushirdim, keyin o'zim yangi iboralarda sinadim.

## Umumiy hukm

Agent g'oya jihatidan yaxshi, lekin **hozirgi shaklida jonli demoda sinsa, sizni uzishi mumkin**. Uchta asosiy sabab:

1. Zipda **№17 yadrosi yo'q**.
2. Favqulodda holat qoidalari **yangi iboralarda ishlamaydi**.
3. Demo bir necha joyda **bajarilmagan narsani bajarilgandek** ko'rsatadi.

Pastda har biri dalil bilan.

## 1. Strategik muammo: zipda yadro yo'q

Zipdagi narsalar: agent, uning eval'i, lex.uz yig'uvchi, ma'lumot fayllari. **Ishonch kartasi dvigateli, INN bo'yicha qidiruv, mahsulot jadvali umuman yo'q.**

- `real_products.json` ichida **300 ta AQSh (openFDA) yozuvi** bor (Walmart, Amazon atsetaminofeni). O'zbekiston reyestri `PENDING`. Hakam bu faylni ochsa "bu O'zbekiston emas" deydi.
- `AGENT.md` agentni "№17 · A1 bo'g'ini" deb nomlagan. Bu noto'g'ri: agent haqiqiylikka aloqasiz, u mutaxassisga yo'naltirish va eslatma. Yuqorida kelishganimizdek bu 3-qatlam.
- Hujjatlardagi buyruqlar (`python3 egiz/agent.py`) papka nomi `orindor` bo'lgani uchun ishlamaydi. `facts.json` ichida ham eski "EGIZ" nomi qolgan.

Soat 07:40, checkpoint 15:00. Ustuvorlik teskari: **sayqallangan 3-qatlam bor, 1-qatlam bo'sh.**

## 2. Xavfsizlik: o'lchangan natijalar noto'g'ri tasavvur beradi

Eval'dagi `15/15` va `0 xato` ni men takrorlay oldim, lekin bu **o'sha 15 ta ibora bilan sozlangan to'plam**. Men 24 ta yangi, alohida yozilgan favqulodda ibora bilan sinadim (informal sinov, tadqiqot emas):

| Ibora                                                           | Agent javobi                                      |
| --------------------------------------------------------------- | ------------------------------------------------- |
| "Qon qusdim"                                                    | **Oftalmolog**                              |
| "Tushkunman"                                                    | **Stomatolog** (psixiatrdan oldin)          |
| "Kasalman"                                                      | **Oftalmolog**                              |
| "Ko'krak og'riyapti" (yolg'iz)                                  | Kardiolog, **"1 hafta"** (shoshilinch emas) |
| "Yuzimning yarmi qimirlamayapti"                                | Dermatolog                                        |
| "Bolam tutqanoq tutdi"                                          | Terapevt (fallback)                               |
| "Qornimning o'ng tomoni qattiq og'riyapti, qusdim, isitmam bor" | Gastroenterolog, **1 hafta**                |
| "Ko'p kunlardan beri holsizman"                                 | **103 shoshilinch** (yolg'on signal)        |
| "3 kundan beri boshim kuchli og'riyapti"                        | **"To'xtamaydigan qon ketish" signali**     |

24 ta favqulodda iboradan **14 tasi o'tkazib yuborildi** (inme belgisi, qon qusish, tutqanoq, bo'g'ilish, ruscha va kirill iboralar). Yolg'on signal 12 ta oddiy gapdan 7 tasida chiqdi.

**Asosiy sabab:** `skel()` undosh skeleti juda yumshoq. 2 harfli skeletlar ko'p so'zga mos keladi:

- `qon` ≈ **kun**, kunduz
- `gap` ≈ **ko'p**
- `yuz` ≈ **yosh**
- `hush` ≈ **hozir**
- `ko'z` ≈ **kasal**
- `tish` ≈ **tush**kun

Ikkinchi sabab: leksikon bo'shliqlari ("nafasim yetmayapti", "qusdim", "tutqanoq", "terlab") va ruscha qatlam yo'qligi, garchi docstring "UZ + RU" desa ham.

**Eval nega yaroqsiz:**

- Qoidalarni ham, test iboralarini ham bir muallif yozgan.
- `4) XAVFSIZLIK 20/20` bema'ni: agent javoblari shablon, shuning uchun dori yoki tashxis nomi chiqishi mumkin emas edi. Bu LLM qo'shilgandan keyingina ma'noga ega.
- 5 va 6-testlar faqat "baxtli yo'l"ni tekshiradi.

## 3. Demo halolligi

1. **"Navbat tayyor ... 20.11.2026, 09:30"**: vaqt va sana kod tomonidan o'ylab topilgan (bugun + kunlar, soat 09:30). Hech narsa bron qilinmagan. Foydalanuvchi buni haqiqiy navbat deb o'ylaydi.
2. **Eslatmalar vaqt bo'yicha emas.** Ular faqat foydalanuvchi **biror narsa yozganda** chiqadi. Demoda "35" yoki "40" (yosh javobi) eslatmani chaqiradi. Haqiqiy taymer yoki push yo'q.
3. **"Offline ishlaydi"**: `OfflineQueue` xotiradagi ro'yxat, `sync()` uni shunchaki tozalaydi. Hech narsa saqlanmaydi va yuborilmaydi.
4. **"Bordim" dan keyingi narx kartasi** har suhbatda bir xil gipotetik misolni (126 000 so'm) chiqaradi, hatto ko'z shifokoriga borgandan keyin ham. Ekranda "misol" deb yozilmagan.
5. **Yosh ajratish xatosi:** "2 yil" (davomiylik) yosh 2 deb olinadi va pediatrga o'tadi. "Bolam" yozilsa yosh avtomatik 4 qilib qo'yiladi.

## 4. Yaxshi tomonlari (haqiqiy kuch)

- **Qonun matni haqiqiy.** lex.uz dan olingan matnlarda quyidagilar so'zma-so'z topildi: 738-sondagi "2029-yil 1-yanvardan ... ICH ... majburiy" bandi va 3735-sondagi "jenerik ... referent narxlari originalnikining 80 foizidan qimmat bo'lishi mumkin emas" bandi. 15% ulgurji va 20% chakana ustama chegaralari ham matnda bor. Hisob ham to'g'ri: 198 640 va 155 796 so'm, farq 21.6%. Bu mening avvalgi "tekshirilmagan" ogohlantirishimni yopadi va S2/S4 uchun **haqiqiy** kuch.
- Arxitektura g'oyasi to'g'ri: favqulodda qoidalar modeldan oldin, har fakt yonida manba, "nima yo'q" bo'limi halol.
- Undosh skeleti g'oyasi o'zbek morfologiyasi uchun aqlli, faqat qattiqroq qilish kerak.

**Narx haqida bitta aniqlik:** qonun **chegara** belgilaydi ("ortiq bo'lmagan"). 21.6% bu ruxsat etilgan eng yuqori narxlar farqi, dorixonadagi haqiqiy narx farqi emas. Haqiqiy referent narxlar reyestri yopiq.

## 5. Kuchaytirish rejasi (ustuvorlik tartibida)

**P0. Xavfsizlik (agentning ishonchi uchun, ~2 soat)**

1. Skelet moslashuvini qat'iylashtiring: 4 belgidan qisqa asoslarni olib tashlang, to'liq so'z chegarasi bo'yicha moslang. 2–3 harfli signallarni (`qon`, `gap`, `yuz`, `hush`, `ko'z`, `tish`, `hid`, `ayol`, `yara`, `uyqu`) ko'p so'zli iboralarga almashtiring.
2. **Majburiy skrining savollari:** ko'krak, bosh og'rig'i, qorin, ko'rish o'zgarishi, bolada isitma uchun 1–2 ha/yo'q savol (birdan boshlandimi, nafas qisilishi, terlash, qo'l uvishishi) **marshrutlashdan oldin**. Javob yo'q yoki noaniq bo'lsa shoshilinch deb hisoblang.
3. **Xavfsiz default:** yuqori xavfli so'z (ko'krak, nafas, qon, hush, bolada isitma) bor, lekin xavf rad etilmagan bo'lsa, "1 hafta" emas, **"bugun ko'rsating"**.
4. Yosh ajratishdan "yil" ni olib tashlang, "bolam" uchun yosh so'rang.

**P1. Haqiqiy baholash (~1.5 soat)**

- Sozlashda ishlatilmagan **60+ ibora**, boshqa odam (jamoadosh yoki LLM, keyin shifokor tekshirgan) yozsin: inkor, uchinchi shaxs, kirill, ruscha, imlo xatolari.
- Yolg'on signalni **100 ta oddiy gapda** sinang (ichida "kun", "ko'p", "hozir", "yosh").
- Natijani "100%" deb emas, aniq son va chegara bilan ayting.

**P2. Demoni halol qilish (~40 daqiqa)**

- "Navbat tayyor" o'rniga: "my.gov.uz orqali vaqtni o'zingiz tanlaysiz; men eslatma rejalashtiraman". Vaqtni foydalanuvchi kiritsin.
- Eslatmalar: haqiqiy taymer (Telegram bot yoki PWA bildirishnomasi) yoki ochiq belgi: **"simulyatsiya, vaqt tezlashtirilgan"**.
- Offline da'vosini olib tashlang yoki mahalliy saqlashni haqiqatan yozing.
- Narx kartasiga **"MISOL"** yorlig'i qo'ying.

**P3. Agentni №17 ga ulash (eng katta ball manbai)**
Agentni ikki rejimli "Örindor yordamchi" qiling:

1. **Retsept rejimi (yadro):** INN yoki dori nomi → ishonch kartasi. Foydalanuvchi "nega arzon?", "ishonsa bo'ladimi?" desa, agent **faqat `facts.json` dagi faktlardan** va kartadan javob beradi, har javobda fakt raqami (F09 va h.k.) va havola bor. Dalil bo'lmasa "ma'lum emas".
2. **Yo'naltirish rejimi (mavjud triaj):** ikkinchi darajali, "keyingi qadam".

**LLM faqat tilni boshqaradi:** o'zbek, rus, kirill tushunish (strukturali niyat va maydonlarga), va javobni sodda tilga o'tkazish. Chiqishni **validator** tekshirsin: faktlarda yo'q raqam, dori nomi, doza yoki tashxis bo'lsa rad etsin. Shunda 4-test (xavfsizlik) birinchi marta ma'noli bo'ladi. Bu T3/T5 uchun "AI qayerda?" savoliga javob ham.

**P4. Yadro ma'lumoti (~2–3 soat, boshqa jamoadoshlar bilan parallel)**

- O'zbekiston reyestri yopiq bo'lsa, 30 INN ni qo'lda jadvalga yig'ing: har qatorda **manba URL va sana**.
- `openFDA` faylini `reference/` papkasiga olib chiqing yoki repodan olib tashlang.
- Bitta shifokor 15 ta favqulodda qoidani va mutaxassis xaritasini ko'rib chiqsin. `AGENT.md` ning o'zi buni "eng katta bo'shliq" deb yozgan.
- "Tibbiy maslahat emas" ogohlantirishi va chegara matnini qo'shing.

## 6. Ball ta'siri

| Mezon | Hozir    | P0–P3 dan keyin                                    |
| ----- | -------- | --------------------------------------------------- |
| T2/T3 | 6–7 / 7 | 7–8 / 8 (halol eval + qoida+LLM chegarasi)         |
| T5    | 6        | 7 (LLM faqat tilda, validator bilan)                |
| S2/S4 | 8 / 6–7 | 8–9 / 7–8 (qonun iqtiboslari kartada, xavfsizlik) |
| S3    | 6–7     | 7 (yadro oqimi ishlaydi)                            |

**Eng katta xavf:** hakam jonli "Qon qusdim" yoki "Yuzim qiyshaydi" deb yozsa va oftalmolog chiqsa, butun mahsulotga ishonch tushadi. Shuning uchun P0 hamma narsadan oldin.

**Tavsiya:** agentga 3 soatdan ortiq ketkazmang. P0+P2 (xavfsizlik va halollik), keyin P3 (yadroga ulash). Qolgan vaqt yadro kartasi va ma'lumot jadvaliga.
