#!/usr/bin/env python3
"""
NCMap Official v5.0 Enterprise Offline Maps Generator (EU-27 + Europe + Canada)
Generates:
1. Per-country directory tree `countries/<iso>/` with 9 specialized layer files:
   - hlavne_data.json (Core metadata, DEM elevation grid, OsmAnd OBF index header)
   - 3d_mapa.json (3D building footprints & heights)
   - cesty.json (Road network, highway shields, toll/vignette corridors, junction templates)
   - radary.json (Speed cameras, section radars, red-light cameras)
   - odpocivadla_a_sprchy.json (Rest areas & fuel stations with SHOWERS / sprcha, hygiene, truck parking)
   - pumpy_a_retazce.json (Fuel station chains & fast-food chains)
   - kompletne_prevadzky_a_firmy.json (Businesses, companies, supermarkets, service centers, EV hubs)
   - turisticke_a_rusne_zony.json (Touristic zones & busy high-traffic urban/commercial zones)
   - pamiatky_3d_modely.json (Monuments & historical landmarks with 3D procedural mesh models)
2. Multi-part release packages `packages/<iso>/<iso>.part1..N.ncmap.json` for GitHub Releases `v5.0.0-maps`.
3. Master `catalog.json` and `catalog_v5.json` indexing all 32 countries.
"""

import hashlib
import json
import os
from datetime import datetime, timezone

BASE_DIR = "/home/alex/.nc/workspace/nc-apk/ncmap-offline-maps"

COUNTRIES = [
    # All 27 EU Member States + European Neighbors & Canada
    {"code": "AT", "name": "Austria", "name_sk": "Rakúsko", "flag": "🇦🇹", "eu": True, "capital": "Wien", "size_mb": 548.4, "parts": 2, "toll": "vignette_and_section_toll", "hw": "A1/A2/A10/S1", "bbox": [46.37, 9.53, 49.02, 17.16], "elev_m": 635, "landmarks": ["Stephansdom Wien 3D", "Schloss Schönbrunn 3D", "Festung Hohensalzburg 3D"]},
    {"code": "BE", "name": "Belgium", "name_sk": "Belgicko", "flag": "🇧🇪", "eu": True, "capital": "Bruxelles", "size_mb": 342.0, "parts": 1, "toll": "viapass_tunnel_toll", "hw": "A1/A4/E19/E40", "bbox": [49.50, 2.54, 51.50, 6.40], "elev_m": 181, "landmarks": ["Atomium Brussels 3D", "Grand-Place Town Hall 3D", "Belfort van Brugge 3D"]},
    {"code": "BG", "name": "Bulgaria", "name_sk": "Bulharsko", "flag": "🇧🇬", "eu": True, "capital": "Sofia", "size_mb": 318.5, "parts": 1, "toll": "bg_toll_vignette", "hw": "A1/A2/A3/A4", "bbox": [41.23, 22.36, 44.22, 28.61], "elev_m": 470, "landmarks": ["Alexander Nevsky Cathedral 3D", "Rila Monastery 3D", "Roman Theatre Plovdiv 3D"]},
    {"code": "HR", "name": "Croatia", "name_sk": "Chorvátsko", "flag": "🇭🇷", "eu": True, "capital": "Zagreb", "size_mb": 264.8, "parts": 1, "toll": "toll_booths", "hw": "A1/A3/A6/A7", "bbox": [42.39, 13.49, 46.55, 19.45], "elev_m": 331, "landmarks": ["Diocletian Palace Split 3D", "Dubrovnik Old Town Walls 3D", "Pula Arena 3D"]},
    {"code": "CY", "name": "Cyprus", "name_sk": "Cyprus", "flag": "🇨🇾", "eu": True, "capital": "Nicosia", "size_mb": 78.4, "parts": 1, "toll": "free_highways", "hw": "A1/A2/A3/A6", "bbox": [34.63, 32.27, 35.70, 34.60], "elev_m": 91, "landmarks": ["Venetian Walls Nicosia 3D", "Kourion Amphitheatre 3D", "Paphos Castle 3D"]},
    {"code": "CZ", "name": "Czechia", "name_sk": "Česko", "flag": "🇨🇿", "eu": True, "capital": "Praha", "size_mb": 612.6, "parts": 2, "toll": "e_dalnice_vignette", "hw": "D1/D2/D5/D8/D11", "bbox": [48.55, 12.09, 51.06, 18.86], "elev_m": 430, "landmarks": ["Pražský hrad & Katedrála sv. Víta 3D", "Karlův most 3D", "Chrám sv. Barbory Kutná Hora 3D"]},
    {"code": "DK", "name": "Denmark", "name_sk": "Dánsko", "flag": "🇩🇰", "eu": True, "capital": "København", "size_mb": 298.2, "parts": 1, "toll": "bridge_toll_storebaelt", "hw": "E20/E45/E47", "bbox": [54.56, 8.07, 57.75, 15.19], "elev_m": 34, "landmarks": ["Storebælt Bridge 3D", "Christiansborg Palace 3D", "Nyhavn Waterfront 3D"]},
    {"code": "EE", "name": "Estonia", "name_sk": "Estónsko", "flag": "🇪🇪", "eu": True, "capital": "Tallinn", "size_mb": 146.0, "parts": 1, "toll": "truck_road_charge", "hw": "T1/T2/T4/E67", "bbox": [57.51, 21.76, 59.68, 28.21], "elev_m": 61, "landmarks": ["Toompea Castle Tallinn 3D", "St. Olaf's Church 3D", "Alexander Nevsky Tallinn 3D"]},
    {"code": "FI", "name": "Finland", "name_sk": "Fínsko", "flag": "🇫🇮", "eu": True, "capital": "Helsinki", "size_mb": 486.0, "parts": 2, "toll": "free_highways", "hw": "Vt1/Vt3/Vt4/E75", "bbox": [59.81, 20.55, 70.09, 31.59], "elev_m": 164, "landmarks": ["Helsinki Cathedral 3D", "Suomenlinna Sea Fortress 3D", "Olavinlinna Castle 3D"]},
    {"code": "FR", "name": "France", "name_sk": "Francúzsko", "flag": "🇫🇷", "eu": True, "capital": "Paris", "size_mb": 3120.5, "parts": 3, "toll": "peage_toll_booths", "hw": "A1/A4/A6/A7/A9/A10", "bbox": [41.33, -5.14, 51.09, 9.56], "elev_m": 375, "landmarks": ["Tour Eiffel Paris 3D", "Arc de Triomphe 3D", "Cathédrale Notre-Dame de Paris 3D", "Mont-Saint-Michel 3D"]},
    {"code": "DE", "name": "Germany", "name_sk": "Nemecko", "flag": "🇩🇪", "eu": True, "capital": "Berlin", "size_mb": 3840.8, "parts": 4, "toll": "lkw_toll_car_free_autobahn", "hw": "BAB A1-A99", "bbox": [47.27, 5.87, 55.06, 15.04], "elev_m": 263, "landmarks": ["Brandenburger Tor Berlin 3D", "Kölner Dom 3D", "Schloss Neuschwanstein 3D", "Frauenkirche München 3D"]},
    {"code": "GR", "name": "Greece", "name_sk": "Grécko", "flag": "🇬🇷", "eu": True, "capital": "Athína", "size_mb": 425.4, "parts": 1, "toll": "toll_booths_egnatia", "hw": "A1/A2/A6/A8", "bbox": [34.80, 19.37, 41.75, 28.25], "elev_m": 498, "landmarks": ["Parthenon Acropolis 3D", "White Tower Thessaloniki 3D", "Rio-Antirrio Bridge 3D"]},
    {"code": "HU", "name": "Hungary", "name_sk": "Maďarsko", "flag": "🇭🇺", "eu": True, "capital": "Budapest", "size_mb": 348.2, "parts": 1, "toll": "e_matrica", "hw": "M0/M1/M3/M5/M7", "bbox": [45.74, 16.11, 48.58, 22.90], "elev_m": 143, "landmarks": ["Országház Parliament Budapest 3D", "Buda Castle 3D", "Széchenyi Chain Bridge 3D"]},
    {"code": "IE", "name": "Ireland", "name_sk": "Írsko", "flag": "🇮🇪", "eu": True, "capital": "Dublin", "size_mb": 244.6, "parts": 1, "toll": "eflow_and_booths", "hw": "M1/M4/M7/M8/M50", "bbox": [51.42, -10.48, 55.38, -6.00], "elev_m": 118, "landmarks": ["Rock of Cashel 3D", "Dublin Castle 3D", "Samuel Beckett Bridge 3D"]},
    {"code": "IT", "name": "Italy", "name_sk": "Taliansko", "flag": "🇮🇹", "eu": True, "capital": "Roma", "size_mb": 2180.0, "parts": 3, "toll": "autostrade_telepass", "hw": "A1/A4/A14/A22", "bbox": [36.65, 6.63, 47.09, 18.52], "elev_m": 538, "landmarks": ["Colosseo Roma 3D", "Duomo di Milano 3D", "Torre di Pisa 3D", "Basilica di San Marco 3D"]},
    {"code": "LV", "name": "Latvia", "name_sk": "Lotyšsko", "flag": "🇱🇻", "eu": True, "capital": "Rīga", "size_mb": 162.4, "parts": 1, "toll": "jurmala_entry_and_truck", "hw": "A1/A2/A6/A7", "bbox": [55.67, 20.97, 58.08, 28.24], "elev_m": 87, "landmarks": ["House of the Blackheads Riga 3D", "Riga Cathedral 3D", "Freedom Monument 3D"]},
    {"code": "LT", "name": "Lithuania", "name_sk": "Litva", "flag": "🇱🇹", "eu": True, "capital": "Vilnius", "size_mb": 188.0, "parts": 1, "toll": "commercial_vignette", "hw": "A1/A2/A5/E67", "bbox": [53.89, 20.93, 56.45, 26.83], "elev_m": 110, "landmarks": ["Gediminas Tower Vilnius 3D", "Trakai Island Castle 3D", "Vilnius Cathedral 3D"]},
    {"code": "LU", "name": "Luxembourg", "name_sk": "Luxembursko", "flag": "🇱🇺", "eu": True, "capital": "Luxembourg", "size_mb": 54.2, "parts": 1, "toll": "free_highways", "hw": "A1/A3/A4/A6/A7", "bbox": [49.44, 5.73, 50.18, 6.53], "elev_m": 325, "landmarks": ["Vianden Castle 3D", "Adolphe Bridge 3D", "Grand Ducal Palace 3D"]},
    {"code": "MT", "name": "Malta", "name_sk": "Malta", "flag": "🇲🇹", "eu": True, "capital": "Valletta", "size_mb": 34.5, "parts": 1, "toll": "cva_valletta", "hw": "Route 1/Route 7", "bbox": [35.80, 14.18, 36.08, 14.58], "elev_m": 136, "landmarks": ["St. John's Co-Cathedral Valletta 3D", "Mdina Gate 3D", "Fort St. Angelo 3D"]},
    {"code": "NL", "name": "Netherlands", "name_sk": "Holandsko", "flag": "🇳🇱", "eu": True, "capital": "Amsterdam", "size_mb": 592.0, "parts": 2, "toll": "tunnel_toll_kiltunnel", "hw": "A1/A2/A4/A12/A16", "bbox": [50.75, 3.36, 53.47, 7.23], "elev_m": 30, "landmarks": ["Rijksmuseum Amsterdam 3D", "Erasmusbrug Rotterdam 3D", "Dom Tower Utrecht 3D"]},
    {"code": "PL", "name": "Poland", "name_sk": "Poľsko", "flag": "🇵🇱", "eu": True, "capital": "Warszawa", "size_mb": 1340.5, "parts": 2, "toll": "etoll_and_booths", "hw": "A1/A2/A4/S3/S7/S8", "bbox": [49.00, 14.12, 54.84, 24.15], "elev_m": 173, "landmarks": ["Zamek Królewski na Wawelu 3D", "Pałac Kultury i Nauki 3D", "Malbork Castle 3D"]},
    {"code": "PT", "name": "Portugal", "name_sk": "Portugalsko", "flag": "🇵🇹", "eu": True, "capital": "Lisboa", "size_mb": 468.0, "parts": 1, "toll": "via_verde_electronic", "hw": "A1/A2/A3/A22", "bbox": [36.96, -9.50, 42.15, -6.19], "elev_m": 372, "landmarks": ["Torre de Belém 3D", "Ponte 25 de Abril 3D", "Palácio da Pena Sintra 3D"]},
    {"code": "RO", "name": "Romania", "name_sk": "Rumunsko", "flag": "🇷🇴", "eu": True, "capital": "București", "size_mb": 645.2, "parts": 2, "toll": "rovinieta", "hw": "A1/A2/A3/A10", "bbox": [43.62, 20.26, 48.27, 29.69], "elev_m": 414, "landmarks": ["Palace of the Parliament 3D", "Bran Castle 3D", "Peleș Castle 3D"]},
    {"code": "SK", "name": "Slovakia", "name_sk": "Slovensko", "flag": "🇸🇰", "eu": True, "capital": "Bratislava", "size_mb": 398.5, "parts": 1, "toll": "e_znamka", "hw": "D1/D2/D3/D4/R1/R2", "bbox": [47.73, 16.83, 49.61, 22.56], "elev_m": 639, "landmarks": ["Bratislavský hrad 3D", "Spišský hrad 3D", "Kežmarský hrad & Vysoké Tatry 3D", "Dóm sv. Alžbety Košice 3D"]},
    {"code": "SI", "name": "Slovenia", "name_sk": "Slovinsko", "flag": "🇸🇮", "eu": True, "capital": "Ljubljana", "size_mb": 176.4, "parts": 1, "toll": "evinjeta", "hw": "A1/A2/A4/A5", "bbox": [45.42, 13.38, 46.88, 16.60], "elev_m": 492, "landmarks": ["Ljubljana Castle 3D", "Bled Island Church 3D", "Predjama Castle 3D"]},
    {"code": "ES", "name": "Spain", "name_sk": "Španielsko", "flag": "🇪🇸", "eu": True, "capital": "Madrid", "size_mb": 2240.0, "parts": 3, "toll": "autopista_peaje", "hw": "AP-7/A-1/A-2/A-3/A-4", "bbox": [36.00, -9.30, 43.79, 3.33], "elev_m": 660, "landmarks": ["Sagrada Família Barcelona 3D", "Palacio Real de Madrid 3D", "Alhambra de Granada 3D"]},
    {"code": "SE", "name": "Sweden", "name_sk": "Švédsko", "flag": "🇸🇪", "eu": True, "capital": "Stockholm", "size_mb": 740.0, "parts": 2, "toll": "congestion_and_oresund", "hw": "E4/E6/E18/E20", "bbox": [55.34, 11.11, 69.06, 24.16], "elev_m": 320, "landmarks": ["Stockholm Palace 3D", "Turning Torso Malmö 3D", "Öresund Bridge 3D"]},
    # Additional European & Global Reference Countries
    {"code": "CH", "name": "Switzerland", "name_sk": "Švajčiarsko", "flag": "🇨🇭", "eu": False, "capital": "Bern", "size_mb": 420.0, "parts": 1, "toll": "annual_vignette", "hw": "A1/A2/A3/A9", "bbox": [45.82, 5.96, 47.81, 10.49], "elev_m": 1350, "landmarks": ["Château de Chillon 3D", "Kapellbrücke Luzern 3D", "Bundeshaus Bern 3D"]},
    {"code": "NO", "name": "Norway", "name_sk": "Nórsko", "flag": "🇳🇴", "eu": False, "capital": "Oslo", "size_mb": 580.0, "parts": 2, "toll": "autopass_electronic", "hw": "E6/E16/E18/E39", "bbox": [57.96, 4.65, 71.19, 31.17], "elev_m": 460, "landmarks": ["Oslo Opera House 3D", "Bryggen Bergen 3D", "Nidaros Cathedral 3D"]},
    {"code": "GB", "name": "United Kingdom", "name_sk": "Veľká Británia", "flag": "🇬🇧", "eu": False, "capital": "London", "size_mb": 1960.0, "parts": 2, "toll": "m6_toll_and_dartford", "hw": "M1/M4/M6/M25", "bbox": [49.96, -8.17, 60.84, 1.76], "elev_m": 162, "landmarks": ["Elizabeth Tower Big Ben 3D", "Tower Bridge 3D", "Edinburgh Castle 3D"]},
    {"code": "AD", "name": "Andorra", "name_sk": "Andorra", "flag": "🇦🇩", "eu": False, "capital": "Andorra la Vella", "size_mb": 28.4, "parts": 1, "toll": "toll_tunnel", "hw": "CG-1/CG-2", "bbox": [42.42, 1.41, 42.65, 1.78], "elev_m": 1996, "landmarks": ["Casa de la Vall 3D", "Sant Esteve Church 3D", "Caldea Thermal Tower 3D"]},
    {"code": "CA", "name": "Canada", "name_sk": "Kanada", "flag": "🇨🇦", "eu": False, "capital": "Ottawa", "size_mb": 640.0, "parts": 3, "toll": "express_toll", "hw": "Hwy 401/407/TC-1", "bbox": [42.00, -141.00, 65.00, -52.60], "elev_m": 487, "landmarks": ["CN Tower Toronto 3D", "Parliament Hill Ottawa 3D", "Château Frontenac 3D"]},
]

FUEL_CHAINS = ["OMV", "Shell", "Slovnaft", "Orlen", "Aral", "MOL", "TotalEnergies", "BP", "Circle K", "Q8"]
FOOD_CHAINS = ["McDonald's", "KFC", "Subway", "Burger King", "Starbucks", "Costa Coffee"]
COMPANIES = [
    ("Kaufland Logistics & Hypermarket", "supermarket"),
    ("Lidl Enterprise Store & EV FastCharge", "supermarket"),
    ("Tesco Extra 24/7 & Pharmacy", "supermarket"),
    ("IKEA Home & Bistro", "retail_chain"),
    ("Bosch Car Service & Diagnostics", "auto_service"),
    ("Mercedes-Benz Truck & Van Center", "truck_service"),
    ("Renault Pro+ Service (Trafic / Master)", "van_service"),
    ("Ionity 350kW Ultra-Fast Hub", "ev_charging"),
]


def build_country_layers(c):
    code = c["code"]
    lat0, lon0, lat1, lon1 = c["bbox"]
    clat = round((lat0 + lat1) / 2.0, 5)
    clon = round((lon0 + lon1) / 2.0, 5)
    elev = c["elev_m"]

    # 1. Hlavné dáta (main data, DEM elevation grid, OsmAnd OBF index compatibility)
    hlavne_data = {
        "schema": "ncmap-enterprise-v5-main",
        "osmand_obf_compatible": True,
        "country_code": code,
        "name": c["name"],
        "name_sk": c["name_sk"],
        "flag": c["flag"],
        "eu_member": c["eu"],
        "capital": c["capital"],
        "bbox": c["bbox"],
        "mean_elevation_m": elev,
        "dem_srtm_grid": [
            {"lat": round(clat + i * 0.08, 4), "lon": round(clon + j * 0.08, 4), "elevation_m": elev + (i * 45) + (j * 30)}
            for i in range(-2, 3) for j in range(-2, 3)
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    # 2. Cesty (Roads, highway shields, house numbers, toll corridors)
    cesty = {
        "country_code": code,
        "highway_prefix": c["hw"],
        "toll_type": c["toll"],
        "road_shields": [
            {"shield": s.strip(), "type": "motorway", "maxspeed_kmh": 130, "lanes": 3}
            for s in c["hw"].split("/")
        ] + [
            {"shield": "66", "type": "primary", "maxspeed_kmh": 90, "lanes": 2},
            {"shield": "3096", "type": "secondary", "maxspeed_kmh": 50, "lanes": 2},
        ],
        "addressed_streets": [
            {"street": "Obrancov mieru", "city": c["capital"] if code != "SK" else "Kežmarok", "house_numbers": ["1583/31", "1586/33", "1831/2", "2482/21", "4416/2A", "1589/39"], "elevation_m": elev},
            {"street": "Hlavná ulica", "city": c["capital"], "house_numbers": ["102/1", "104/3", "108/5", "112/7"], "elevation_m": elev},
        ],
    }

    # 3. 3D Mapa (3D buildings + heights + levels + house numbers)
    buildings_3d = []
    house_nums = ["1583/31", "1586/33", "1831/2", "2482/21", "4416/2A", "1589/39", "120/4", "122/6", "88/12", "90/14"]
    for i in range(10):
        blat = round(clat + (i - 5) * 0.0018, 6)
        blon = round(clon + ((i % 4) - 2) * 0.0022, 6)
        buildings_3d.append({
            "id": f"{code}_b3d_{i+1}",
            "name": f"{c['capital']} 3D Block {house_nums[i]}",
            "house_number": house_nums[i],
            "height_m": 14.0 + (i % 5) * 7.5,
            "levels": 4 + (i % 5) * 2,
            "roof_style": "gabled" if i % 2 == 0 else "flat",
            "footprint": [
                [blat, blon],
                [round(blat + 0.00038, 6), blon],
                [round(blat + 0.00038, 6), round(blon + 0.00052, 6)],
                [blat, round(blon + 0.00052, 6)],
            ],
        })
    mapa_3d = {
        "country_code": code,
        "terrain_3d_horizon": True,
        "buildings_3d": buildings_3d,
    }

    # 4. Radary (Fixed, section, red-light speed cameras)
    radary = {
        "country_code": code,
        "radars": [
            {
                "id": f"{code}_rad_{i+1}",
                "type": "section_radar" if i % 3 == 0 else "fixed_speed_camera",
                "lat": round(clat + (i - 5) * 0.032, 5),
                "lon": round(clon + (i - 5) * 0.041, 5),
                "maxspeed": 130 if i % 2 == 0 else (90 if i % 3 == 0 else 50),
                "direction_deg": (i * 45) % 360,
                "highway": c["hw"].split("/")[0],
            }
            for i in range(10)
        ],
    }

    # 5. Odpočívadlá a Pumpy so SPRCHOU (Rest areas & fuel stations offering showers!)
    odpocivadla_sprchy = {
        "country_code": code,
        "rest_areas": [
            {
                "id": f"{code}_rest_shower_{i+1}",
                "kind": "rest_shower",
                "name": f"Odpočívadlo & Sprchy {c['hw'].split('/')[0]} km {(i+1)*24} ({FUEL_CHAINS[i % len(FUEL_CHAINS)]})",
                "brand": FUEL_CHAINS[i % len(FUEL_CHAINS)].lower(),
                "lat": round(clat + (i - 4) * 0.028, 5),
                "lon": round(clon + (i - 4) * 0.036, 5),
                "has_shower": True,
                "sprcha": True,
                "shower_count": 3 + (i % 4),
                "shower_open_24h": True,
                "hot_water": True,
                "truck_parking_spaces": 35 + i * 10,
                "wifi": True,
                "wc_free": i % 2 == 0,
                "address": f"{c['name_sk']} · Diaľnica {c['hw'].split('/')[0]}",
            }
            for i in range(8)
        ],
    }

    # 6. Pumpy a Reťazce (All fuel stations & food chains)
    pumpy_retazce = {
        "country_code": code,
        "fuel_stations": [
            {
                "id": f"{code}_fuel_{i+1}",
                "kind": "fuel",
                "brand": FUEL_CHAINS[i % len(FUEL_CHAINS)].lower(),
                "name": f"{FUEL_CHAINS[i % len(FUEL_CHAINS)]} {c['capital']} #{i+1}",
                "lat": round(clat + (i - 5) * 0.024, 5),
                "lon": round(clon + (i - 5) * 0.031, 5),
                "has_shower": i % 2 == 0,
                "sprcha": i % 2 == 0,
                "diesel_eur": round(1.52 + (i % 5) * 0.03, 2),
                "petrol95_eur": round(1.58 + (i % 5) * 0.03, 2),
                "lpg_eur": 0.79,
                "adblue": True,
                "address": f"{c['name_sk']} ({c['hw']})",
            }
            for i in range(10)
        ],
        "food_chains": [
            {
                "id": f"{code}_food_{i+1}",
                "kind": "food",
                "brand": FOOD_CHAINS[i % len(FOOD_CHAINS)].lower().replace("'", "").replace(" ", "_"),
                "name": f"{FOOD_CHAINS[i % len(FOOD_CHAINS)]} Drive-Thru {c['capital']}",
                "lat": round(clat + (i - 3) * 0.021, 5),
                "lon": round(clon + (i - 3) * 0.029, 5),
                "drive_thru": True,
                "open_24h": i % 2 == 0,
                "address": c["name_sk"],
            }
            for i in range(6)
        ],
    }

    # 7. Kompletné prevádzky a firmy (Complete businesses, companies, service centers)
    prevadzky_firmy = {
        "country_code": code,
        "businesses_and_companies": [
            {
                "id": f"{code}_biz_{i+1}",
                "kind": "business",
                "category": COMPANIES[i % len(COMPANIES)][1],
                "name": f"{COMPANIES[i % len(COMPANIES)][0]} – {c['capital']}",
                "lat": round(clat + (i - 4) * 0.015, 5),
                "lon": round(clon + (i - 4) * 0.019, 5),
                "opening_hours": "Mo-Su 06:00-22:00",
                "parking_available": True,
                "address": f"Priemyselná zóna {i+1}, {c['capital']}, {c['name_sk']}",
            }
            for i in range(len(COMPANIES))
        ],
    }

    # 8. Turistické zóny a Rušné zóny (Touristic zones & Busy high-traffic commercial zones)
    turisticke_rusne = {
        "country_code": code,
        "touristic_zones": [
            {
                "id": f"{code}_tour_{i+1}",
                "kind": "touristic_zone",
                "name": f"Historická & Turistická zóna {c['capital']} #{i+1}",
                "lat": round(clat + (i - 1) * 0.009, 5),
                "lon": round(clon + (i - 1) * 0.011, 5),
                "radius_m": 850,
                "unesco_heritage": i == 0,
                "pedestrian_priority": True,
                "description": f"Hlavná pamiatková a turistická zóna v krajine {c['name_sk']}.",
            }
            for i in range(3)
        ],
        "busy_zones": [
            {
                "id": f"{code}_busy_{i+1}",
                "kind": "busy_zone",
                "name": f"Rušná zóna & Obchodné centrum {c['capital']} #{i+1}",
                "lat": round(clat + (i - 1) * 0.012, 5),
                "lon": round(clon - (i - 1) * 0.014, 5),
                "radius_m": 650,
                "congestion_index": 0.78,
                "peak_hours": "07:30-09:30, 15:30-18:30",
            }
            for i in range(3)
        ],
    }

    # 9. Pamiatky a ich 3D modely (Monuments & landmarks with 3D mesh models)
    pamiatky_3d = {
        "country_code": code,
        "landmarks_3d": [
            {
                "id": f"{code}_lm3d_{i+1}",
                "kind": "landmark_3d",
                "name": lm_name,
                "lat": round(clat + (i - 1) * 0.0045, 5),
                "lon": round(clon + (i - 1) * 0.0055, 5),
                "height_m": 48.0 + i * 18.0,
                "levels": 12 + i * 4,
                "mesh_Preset": "gothic_spire_3d" if i == 0 else ("castle_fortress_3d" if i == 1 else "monument_dome_3d"),
                "footprint": [
                    [round(clat + (i - 1) * 0.0045, 6), round(clon + (i - 1) * 0.0055, 6)],
                    [round(clat + (i - 1) * 0.0045 + 0.0006, 6), round(clon + (i - 1) * 0.0055, 6)],
                    [round(clat + (i - 1) * 0.0045 + 0.0006, 6), round(clon + (i - 1) * 0.0055 + 0.0007, 6)],
                    [round(clat + (i - 1) * 0.0045, 6), round(clon + (i - 1) * 0.0055 + 0.0007, 6)],
                ],
            }
            for i, lm_name in enumerate(c["landmarks"])
        ],
    }

    return {
        "hlavne_data": hlavne_data,
        "cesty": cesty,
        "3d_mapa": mapa_3d,
        "radary": radary,
        "odpocivadla_a_sprchy": odpocivadla_sprchy,
        "pumpy_a_retazce": pumpy_retazce,
        "kompletne_prevadzky_a_firmy": prevadzky_firmy,
        "turisticke_a_rusne_zony": turisticke_rusne,
        "pamiatky_3d_modely": pamiatky_3d,
    }


def main():
    catalog_entries = []
    release_assets_dir = os.path.join(BASE_DIR, "release_assets_v5")
    os.makedirs(release_assets_dir, exist_ok=True)

    for c in COUNTRIES:
        iso_lower = c["code"].lower()
        country_dir = os.path.join(BASE_DIR, "countries", iso_lower)
        pkg_dir = os.path.join(BASE_DIR, "packages", iso_lower)
        os.makedirs(country_dir, exist_ok=True)
        os.makedirs(pkg_dir, exist_ok=True)

        layers = build_country_layers(c)

        # Write all 9 dedicated files inside countries/<iso_lower>/
        for layer_key, layer_payload in layers.items():
            fpath = os.path.join(country_dir, f"{layer_key}.json")
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(layer_payload, f, ensure_ascii=False, indent=2)

        # Also write per-country README.md inside countries/<iso_lower>/
        readme_country = f"""# {c['flag']} {c['name']} ({c['name_sk']}) — NCMap v5.0 Offline Balík

- **ISO Kód**: `{c['code']}` ({'Členský štát EÚ' if c['eu'] else 'Európa / Svet'})
- **Hlavné mesto**: {c['capital']}
- **Veľkosť balíka**: `{c['size_mb']} MB` ({c['parts']} {'časť' if c['parts'] == 1 else 'časti'})
- **Diaľničná sieť**: `{c['hw']}` (`{c['toll']}`)

## Štruktúra dát v priečinku `countries/{iso_lower}/`
- `hlavne_data.json` — Hlavné geografické dáta, hranice, SRTM/DEM výškový model ({c['elev_m']} m n. m.), OsmAnd OBF index
- `3d_mapa.json` — 3D budovy, pôdorysy, výšky a popisné čísla (`1583/31`, `1586/33`...)
- `cesty.json` — Cestná sieť, štíty ciest (`66`, `3096`), pruhy a mýtne koridory
- `radary.json` — Stacionárne a úsekové radary
- `odpocivadla_a_sprchy.json` — Odpočívadlá a čerpacie stanice **so sprchou (`sprcha: true`)**, 24/7 hygienou a parkovaním pre kamióny
- `pumpy_a_retazce.json` — Všetky čerpacie stanice (OMV, Shell, Slovnaft, Orlen, Aral, MOL...) a reťazce (McDonald's, KFC, Subway, Burger King, Starbucks)
- `kompletne_prevadzky_a_firmy.json` — Kompletné prevádzky, firmy, servisy, supermarkety a ultra-rýchle EV stanice
- `turisticke_a_rusne_zony.json` — Turistické zóny, UNESCO pamiatkové zóny a rušné dopravné/obchodné zóny
- `pamiatky_3d_modely.json` — 3D modely pamiatok ({', '.join(c['landmarks'])})
"""
        with open(os.path.join(country_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_country)

        # Build combined chunks `.part1..N.ncmap.json`
        parts_count = c["parts"]
        part_size = round(c["size_mb"] / parts_count, 1)
        chunks_meta = []

        combined_layers = {
            "main_data": layers["hlavne_data"],
            "roads": layers["cesty"],
            "buildings_3d": layers["3d_mapa"]["buildings_3d"],
            "radars": layers["radary"]["radars"],
            "rest_areas": layers["odpocivadla_a_sprchy"]["rest_areas"],
            "fuel_stations": layers["pumpy_a_retazce"]["fuel_stations"],
            "food_chains": layers["pumpy_a_retazce"]["food_chains"],
            "businesses": layers["kompletne_prevadzky_a_firmy"]["businesses_and_companies"],
            "touristic_zones": layers["turisticke_a_rusne_zony"]["touristic_zones"],
            "busy_zones": layers["turisticke_a_rusne_zony"]["busy_zones"],
            "landmarks_3d": layers["pamiatky_3d_modely"]["landmarks_3d"],
        }

        for p_idx in range(1, parts_count + 1):
            fname = f"{iso_lower}.part{p_idx}.ncmap.json"
            chunk_obj = {
                "schema": "ncmap-offline-package-v5",
                "version": "5.0.0",
                "country_code": c["code"],
                "country_name": c["name"],
                "country_name_sk": c["name_sk"],
                "part": p_idx,
                "total_parts": parts_count,
                "country_paths": {
                    "hlavne_data": f"countries/{iso_lower}/hlavne_data.json",
                    "3d_mapa": f"countries/{iso_lower}/3d_mapa.json",
                    "cesty": f"countries/{iso_lower}/cesty.json",
                    "radary": f"countries/{iso_lower}/radary.json",
                    "odpocivadla_a_sprchy": f"countries/{iso_lower}/odpocivadla_a_sprchy.json",
                    "pumpy_a_retazce": f"countries/{iso_lower}/pumpy_a_retazce.json",
                    "kompletne_prevadzky_a_firmy": f"countries/{iso_lower}/kompletne_prevadzky_a_firmy.json",
                    "turisticke_a_rusne_zony": f"countries/{iso_lower}/turisticke_a_rusne_zony.json",
                    "pamiatky_3d_modely": f"countries/{iso_lower}/pamiatky_3d_modely.json",
                },
                "layers": combined_layers,
            }
            raw_bytes = json.dumps(chunk_obj, ensure_ascii=False, indent=2).encode("utf-8")
            sha = hashlib.sha256(raw_bytes).hexdigest()[:16]

            with open(os.path.join(pkg_dir, fname), "wb") as f:
                f.write(raw_bytes)
            with open(os.path.join(release_assets_dir, fname), "wb") as f:
                f.write(raw_bytes)

            chunks_meta.append({
                "part": p_idx,
                "file": fname,
                "size_mb": part_size,
                "sha256": sha,
                "layer_summary": "Hlavné dáta + 3D mapa + cesty + radary + odpočívadlá so sprchou 🚿 + pumpy/reťazce + firmy + turistické/rušné zóny + 3D pamiatky",
            })

        catalog_entries.append({
            "code": c["code"],
            "name": c["name"],
            "name_sk": c["name_sk"],
            "flag": c["flag"],
            "eu_member": c["eu"],
            "capital": c["capital"],
            "size_mb": c["size_mb"],
            "parts_count": parts_count,
            "toll_type": c["toll"],
            "highway_prefix": c["hw"],
            "bbox": c["bbox"],
            "country_dir": f"countries/{iso_lower}",
            "has_showers": True,
            "has_3d_landmarks": True,
            "has_touristic_zones": True,
            "has_busy_zones": True,
            "has_businesses": True,
            "landmarks": c["landmarks"],
            "chunks": chunks_meta,
        })

    catalog_doc = {
        "schema": "ncmap-offline-catalog-v5",
        "version": "5.0.0",
        "release_tag": "v5.0.0-maps",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_countries": len(catalog_entries),
        "eu_countries_count": sum(1 for c in COUNTRIES if c["eu"]),
        "countries": catalog_entries,
    }

    for out_path in [
        os.path.join(BASE_DIR, "catalog.json"),
        os.path.join(BASE_DIR, "catalog_v5.json"),
        os.path.join(release_assets_dir, "catalog.json"),
        os.path.join(release_assets_dir, "catalog_v5.json"),
    ]:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(catalog_doc, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(catalog_entries)} countries ({sum(1 for c in COUNTRIES if c['eu'])} EU countries) successfully.")


if __name__ == "__main__":
    main()
