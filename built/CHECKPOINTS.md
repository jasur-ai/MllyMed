# Checkpointlar — CP0…CP10

Har checkpoint: maqsad → qarorlar (tasdiq/rad) → dalil → keyingi qadam.

| CP | Mavzu | Holat | Dalil |
|---|---|---|---|
| CP0 | Doira, arxitektura, rad etilgan yo'llar | ✅ | `checkpoints/CP0_scope.md` |
| CP1 | Ma'lumot: vendor core + katalog + manifest | ✅ | `checkpoints/CP1_data.md` |
| CP2 | Dorixona konnektori: XPN bog'lash, 80% proxy | ✅ | `checkpoints/CP2_apteka.md` |
| CP3 | Mini DMED: sintetik seed, ruxsatlar, audit | ✅ | `checkpoints/CP3_dmed.md` |
| CP4 | Bridge + veb: bitta oqim, API, UI | ✅ | `checkpoints/CP4_bridge_web.md` |
| CP5 | Virtual tajriba: 12 stsenariy | ✅ | `checkpoints/CP5_virtual_experiment.md` |
| CP6 | Handoff v1 | ✅ | `checkpoints/CP6_handoff.md` |
| CP7 | **Masshtab: 48 → 308 mahsulot, pipeline** | ✅ | `checkpoints/CP7_data_scale.md` |
| CP8 | **SQLite domen: rollar, dispense, audit** | ✅ | `checkpoints/CP8_sqlite_roles.md` |
| CP9 | **Katta mahsulot UI + analitika** | ✅ | `checkpoints/CP9_product_ui.md` |
| CP10 | **Bitta sayqallangan mahsulot + Arzon apteka** | ✅ | `checkpoints/CP10_product_arzon.md` |

## Yagona tekshiruv

```bash
cd orindor && PYTHONIOENCODING=utf-8 python eval_agent.py
cd ../built && PYTHONIOENCODING=utf-8 python build.py --check
PYTHONIOENCODING=utf-8 python -m unittest discover -s tests
PYTHONIOENCODING=utf-8 python sim/run.py
```

Kutilgan: `JAMI XATO: 0` · `CHECK OK` · `17/17 OK` · `12/12 stsenariy`.
