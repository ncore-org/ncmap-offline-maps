# NCMap Official — Public Offline Maps & 3D Data Repository (`v4.0.0-maps`)

Verejný distribučný repozitár a **GitHub Releases** CDN pre navigačnú platformu **NCMap Official v4.0.0** (`ncore-org/ncmap-offcial`).

## Obsah offline balíkov (Sygic-Grade Multi-Layer Format)
Každá krajina obsahuje kompletné navigačné vrstvy pre 100 % offline prevádzku:
1. **3D Budovy (`buildings_3d`)**: Pôdorysy a výšky budov pre 3D perspektívne vykresľovanie miest.
2. **Rýchlostné radary (`speed_cameras`)**: Stacionárne radary, úsekové merania a rýchlostné limity.
3. **Čerpacie stanice (`fuel_stations`)**: OMV, Slovnaft, Shell, Aral, TotalEnergies, Orlen, MOL, BP.
4. **Odpočívadlá a reťazce (`rest_areas_and_food`)**: Diaľničné odpočívadlá, parkoviská, McDonald's, KFC, Subway, Burger King, Starbucks.
5. **Chodníky a pešie trasy (`sidewalks_and_pedestrian`)**: Dáta chodníkov, priechodov a peších zón.
6. **Mýtne a diaľničné pravidlá (`toll_metadata`)**: Rozlíšenie spoplatnených (známky / mýtne brány) a nezpoplatnených úsekov pre výpočet trasy podľa jednotlivých krajín.

## Podpora Multi-Part archívov pre veľké krajiny
Krajiny, ktorých kompletné dáta presahujú limit jedného súboru na GitHub Releases (napr. **Nemecko**, **Francúzsko**, **Taliansko**, **Kanada**, **Poľsko**, **Španielsko**, **Veľká Británia**), sú automaticky rozdelené do viacerých častí (`.part1.ncmap.json`, `.part2.ncmap.json`, `.part3.ncmap.json`, `.part4.ncmap.json`). Aplikácia **NCMap Official v4.0.0** aj jej backend tieto časti pri sťahovaní automaticky stiahnu a spoja do jedného celku.
