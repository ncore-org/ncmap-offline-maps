# 🌍 NCMap Official — Enterprise Offline Maps Repository (`v5.0.0-maps` & `v4.0.0-maps`)

Verejný repozitár offline máp pre aplikáciu **`ncmap-offcial` (Enterprise v5.0)** na úrovni **Sygic Maps / OsmAnd OBF**.
Obsahuje kompletnú stromovú štruktúru pre **všetkých 27 členských štátov Európskej únie (EÚ)** + Švajčiarsko, Nórsko, Veľkú Britániu, Andorru a Kanadu (**spolu 32 krajín**).

---

## 🗂️ Štruktúra každej krajiny (`countries/<iso>/`)

Každá krajina má vlastný adresár `countries/<iso>/` (napr. `countries/sk/`, `countries/de/`, `countries/fr/`, `countries/cz/`, `countries/at/`, `countries/it/`, `countries/pl/`...), ktorý obsahuje **9 špecializovaných vrstiev**:

1. **`hlavne_data.json`** — Hlavné geografické dáta krajiny, hranice, SRTM/DEM výškový model terénu a OsmAnd-kompatibilný index regiónu.
2. **`3d_mapa.json`** — 3D budovy, mestské bloky, výšky v metroch, podlažia, typy striech a presné popisné čísla (`1583/31`, `1586/33`, `1831/2`, `2482/21`...).
3. **`cesty.json`** — Cestná a diaľničná sieť, modré/zelené štíty ciest (`66`, `3096`, `D1`, `A1`), počet jazdných pruhov, mýtne pravidlá a šablóny diaľničných výjazdov.
4. **`radary.json`** — Stacionárne rýchlostné radary, úsekové merania rýchlosti a kamery na križovatkách.
5. **`odpocivadla_a_sprchy.json`** — Diaľničné odpočívadlá a čerpacie stanice **so sprchou (`sprcha: true` / `has_shower: true`)**, počtom sprchovacích kabín, 24/7 hygienickým zázemím, teplou vodou a počtom parkovacích miest pre kamióny.
6. **`pumpy_a_retazce.json`** — Všetky čerpacie stanice (`OMV`, `Shell`, `Slovnaft`, `Orlen`, `Aral`, `MOL`, `TotalEnergies`, `BP`, `Circle K`, `Q8`) a gastro reťazce (`McDonald's`, `KFC`, `Subway`, `Burger King`, `Starbucks`, `Costa Coffee`).
7. **`kompletne_prevadzky_a_firmy.json`** — Kompletné prevádzky, firmy, priemyselné zóny, autorizované servisy (`Bosch Car Service`, `Renault Pro+`, `Mercedes-Benz Truck`), supermarkety (`Kaufland`, `Lidl`, `Tesco`, `IKEA`) a 350 kW EV nabíjacie huby.
8. **`turisticke_a_rusne_zony.json`** — Turistické zóny (`turisticke_zony`), historické centrá UNESCO a rušné dopravné/obchodné zóny (`rusne_zony`) s indexom vyťaženosti.
9. **`pamiatky_3d_modely.json`** — Historické pamiatky a dominanty s 3D procedurálnymi modelmi (`pamiatky_3d_modely`) — napr. *Bratislavský hrad 3D*, *Spišský hrad 3D*, *Kežmarský hrad & Vysoké Tatry 3D*, *Pražský hrad 3D*, *Stephansdom Wien 3D*, *Tour Eiffel 3D*, *Brandenburger Tor 3D*, *Colosseo Roma 3D*.

---

## 🇪🇺 Kompletný zoznam krajín v `v5.0.0-maps` (32 krajín · 27 štátov EÚ)

| Vlajka | Kód | Krajina | Cesta v repozitári | Balíky v GitHub Release | Diaľnice & Mýto | Sprchy 🚿 & 3D Pamiatky 🏛️ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🇦🇹 | `AT` | **Austria (Rakúsko)** | `countries/at/` | `at.part1..2.ncmap.json` (548,4 MB) | `A1/A2/A10/S1` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇧🇪 | `BE` | **Belgium (Belgicko)** | `countries/be/` | `be.part1.ncmap.json` (342,0 MB) | `A1/A4/E19/E40` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇧🇬 | `BG` | **Bulgaria (Bulharsko)** | `countries/bg/` | `bg.part1.ncmap.json` (318,5 MB) | `A1/A2/A3/A4` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇭🇷 | `HR` | **Croatia (Chorvátsko)** | `countries/hr/` | `hr.part1.ncmap.json` (264,8 MB) | `A1/A3/A6/A7` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇨🇾 | `CY` | **Cyprus (Cyprus)** | `countries/cy/` | `cy.part1.ncmap.json` (78,4 MB) | `A1/A2/A3/A6` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇨🇿 | `CZ` | **Czechia (Česko)** | `countries/cz/` | `cz.part1..2.ncmap.json` (612,6 MB) | `D1/D2/D5/D8/D11` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇩🇰 | `DK` | **Denmark (Dánsko)** | `countries/dk/` | `dk.part1.ncmap.json` (298,2 MB) | `E20/E45/E47` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇪🇪 | `EE` | **Estonia (Estónsko)** | `countries/ee/` | `ee.part1.ncmap.json` (146,0 MB) | `T1/T2/T4/E67` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇫🇮 | `FI` | **Finland (Fínsko)** | `countries/fi/` | `fi.part1..2.ncmap.json` (486,0 MB) | `Vt1/Vt3/Vt4/E75` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇫🇷 | `FR` | **France (Francúzsko)** | `countries/fr/` | `fr.part1..3.ncmap.json` (3,12 GB) | `A1/A4/A6/A7/A9` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇩🇪 | `DE` | **Germany (Nemecko)** | `countries/de/` | `de.part1..4.ncmap.json` (3,84 GB) | `BAB A1-A99` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇬🇷 | `GR` | **Greece (Grécko)** | `countries/gr/` | `gr.part1.ncmap.json` (425,4 MB) | `A1/A2/A6/A8` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇭🇺 | `HU` | **Hungary (Maďarsko)** | `countries/hu/` | `hu.part1.ncmap.json` (348,2 MB) | `M0/M1/M3/M5/M7` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇮🇪 | `IE` | **Ireland (Írsko)** | `countries/ie/` | `ie.part1.ncmap.json` (244,6 MB) | `M1/M4/M7/M50` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇮🇹 | `IT` | **Italy (Taliansko)** | `countries/it/` | `it.part1..3.ncmap.json` (2,18 GB) | `A1/A4/A14/A22` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇱🇻 | `LV` | **Latvia (Lotyšsko)** | `countries/lv/` | `lv.part1.ncmap.json` (162,4 MB) | `A1/A2/A6/A7` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇱🇹 | `LT` | **Lithuania (Litva)** | `countries/lt/` | `lt.part1.ncmap.json` (188,0 MB) | `A1/A2/A5/E67` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇱🇺 | `LU` | **Luxembourg (Luxembursko)** | `countries/lu/` | `lu.part1.ncmap.json` (54,2 MB) | `A1/A3/A4/A6` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇲🇹 | `MT` | **Malta (Malta)** | `countries/mt/` | `mt.part1.ncmap.json` (34,5 MB) | `Route 1/Route 7` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇳🇱 | `NL` | **Netherlands (Holandsko)** | `countries/nl/` | `nl.part1..2.ncmap.json` (592,0 MB) | `A1/A2/A4/A12` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇵🇱 | `PL` | **Poland (Poľsko)** | `countries/pl/` | `pl.part1..2.ncmap.json` (1,34 GB) | `A1/A2/A4/S3/S7` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇵🇹 | `PT` | **Portugal (Portugalsko)** | `countries/pt/` | `pt.part1.ncmap.json` (468,0 MB) | `A1/A2/A3/A22` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇷🇴 | `RO` | **Romania (Rumunsko)** | `countries/ro/` | `ro.part1..2.ncmap.json` (645,2 MB) | `A1/A2/A3/A10` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇸🇰 | `SK` | **Slovakia (Slovensko)** | `countries/sk/` | `sk.part1.ncmap.json` (398,5 MB) | `D1/D2/D3/R1/R2` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇸🇮 | `SI` | **Slovenia (Slovinsko)** | `countries/si/` | `si.part1.ncmap.json` (176,4 MB) | `A1/A2/A4/A5` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇪🇸 | `ES` | **Spain (Španielsko)** | `countries/es/` | `es.part1..3.ncmap.json` (2,24 GB) | `AP-7/A-1/A-2/A-3` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇸🇪 | `SE` | **Sweden (Švédsko)** | `countries/se/` | `se.part1..2.ncmap.json` (740,0 MB) | `E4/E6/E18/E20` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇨🇭 | `CH` | **Switzerland (Švajčiarsko)** | `countries/ch/` | `ch.part1.ncmap.json` (420,0 MB) | `A1/A2/A3/A9` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇳🇴 | `NO` | **Norway (Nórsko)** | `countries/no/` | `no.part1..2.ncmap.json` (580,0 MB) | `E6/E16/E18/E39` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇬🇧 | `GB` | **United Kingdom (Veľká Británia)** | `countries/gb/` | `gb.part1..2.ncmap.json` (1,96 GB) | `M1/M4/M6/M25` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇦🇩 | `AD` | **Andorra** | `countries/ad/` | `ad.part1.ncmap.json` (28,4 MB) | `CG-1/CG-2` | Áno (Sprchy 24/7 + 3D pamiatky) |
| 🇨🇦 | `CA` | **Canada (Kanada)** | `countries/ca/` | `ca.part1..3.ncmap.json` (640,0 MB) | `Hwy 401/407` | Áno (Sprchy 24/7 + 3D pamiatky) |

---

## 📦 Verzie Releases
- **`v5.0.0-maps` (Aktuálna verzia)**: Kompletných 32 krajín (všetkých 27 štátov EÚ + CH, NO, GB, AD, CA), odpočívadlá a pumpy so sprchou (`sprcha: true`), kompletné firmy a prevádzky, turistické a rušné zóny, 3D modely pamiatok.
- **`v4.0.0-maps` (Predošlá verzia — zachovaná)**: Pôvodných 13 krajín.
