# MllyMed — Frontend Arxitekturasi

Ushbu katalog loyihaning to'liq modulli frontend qismini o'z ichiga oladi. Avvalgi monolit, tartibsiz kod arxitekturasi professional modulli strukturaga ajratildi.

## Papkalar va Fayllar Tuzilishi

```
frontend/ (yoki built/src/web/static/)
├── index.html            # Asosiy semantik HTML shablon
├── assets/
│   └── logo.svg          # MllyMed rasmiy SVG logotipi (cls-1, cls-2)
├── css/
│   ├── base.css          # Dizayn tokenlari, shriftlar, reset va nishonlar (badges)
│   ├── navbar.css        # MagicHeal uslubidagi suzuvchi nav bar va B2C/B2B switcher
│   ├── catalog.css       # Dori kartochkalari, qadoq rasmlari, qidiruv va filtrlar
│   ├── agent.css         # MllyMed AI suzuvchi tugmasi (FAB) va popup muloqot oynasi
│   ├── b2b.css           # Shifokor (XPN e-retsept), Dorixona (kassa) va Zavod portallari
│   └── modal.css         # Bemor kabineti va dori chuqur tahlili modallari
└── js/
    ├── api.js            # Markazlashgan HTTP API mijozi va rol sarlavhalari (X-Role, X-User)
    ├── catalog.js        # Dori vositalari katalogi, SVG qadoq generatori va tahlil logikasi
    ├── agent.js          # MllyMed AI triaj va klinik xavfsiz skrining muloqoti
    ├── patient.js        # Bemor shaxsiy kabineti, qabullar va retseptlar ko'rinishi
    ├── b2b.js            # Shifokor retsept yozish, dorixona tarqatish va audit tahlili
    └── app.js            # Ilovani ishga tushirish (bootstrap), debounce qidiruv va rejimlar
```

## Afzalliklari
1. **Modullilik**: Har bir komponent (CSS va JS) o'z javobgarlik doirasiga ega.
2. **Qayta ishlatiluvchanlik**: API, dori qadoq SVG rendereri va modallar alohida import qilinadi.
3. **Backend daxlsizligi**: Backend domen logikasi o'zgarishsiz qolgan holda statik marshrutlash ta'minlandi.
