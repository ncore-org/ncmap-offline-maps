#!/usr/bin/env python3
import glob
import json
import os
import subprocess
import urllib.request

REPO = "ncore-org/ncmap-offline-maps"
TAG = "v5.0.0-maps"
ASSETS_DIR = "/home/alex/.nc/workspace/nc-apk/ncmap-offline-maps/release_assets_v5"


def get_token():
    tok = os.environ.get("GITHUB_TOKEN", "")
    if tok:
        return tok
    url = subprocess.check_output(
        ["git", "-C", "/home/alex/.nc/workspace/nc-apk/ncmap-offline-maps", "remote", "get-url", "origin"],
        text=True,
    ).strip()
    if "@" in url and "://" in url:
        creds = url.split("://", 1)[1].split("@", 1)[0]
        if ":" in creds:
            return creds.split(":", 1)[1]
        return creds
    raise RuntimeError("No GitHub token found")


def api_request(url, method="GET", data=None, content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "ncmap-release-publisher/5.0",
    }
    if data is not None:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    release = None
    try:
        release = api_request(f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}")
    except Exception:
        pass

    if not release:
        payload = {
            "tag_name": TAG,
            "target_commitish": "main",
            "name": "NCMap Enterprise Offline Maps v5.0.0-maps (All 27 EU Countries + 3D Landmarks + Showers)",
            "body": (
                "## 🌍 NCMap Enterprise Offline Maps — `v5.0.0-maps` (All 27 EU Countries + Europe)\n\n"
                "- **Kompletná štruktúra pre všetkých 27 členských štátov EÚ + CH, NO, GB, AD, CA (spolu 32 krajín)**.\n"
                "- Každá krajina má vlastnú cestu `countries/<iso>/` s 9 vrstvami:\n"
                "  1. `hlavne_data.json` (Hlavné dáta, hranice, SRTM/DEM výšky, OsmAnd OBF index)\n"
                "  2. `3d_mapa.json` (3D budovy, podlažia a popisné čísla)\n"
                "  3. `cesty.json` (Cesty, diaľnice, štíty ciest, mýtne koridory)\n"
                "  4. `radary.json` (Stacionárne a úsekové radary)\n"
                "  5. `odpocivadla_a_sprchy.json` (Odpočívadlá a čerpacie stanice so **sprchou `sprcha: true` 🚿**, 24/7 hygienou a parkovaním pre kamióny)\n"
                "  6. `pumpy_a_retazce.json` (Všetky pumpy a gastro reťazce)\n"
                "  7. `kompletne_prevadzky_a_firmy.json` (Kompletné prevádzky, firmy, servisy, supermarkety, EV huby)\n"
                "  8. `turisticke_a_rusne_zony.json` (Turistické zóny, UNESCO centrá a rušné zóny)\n"
                "  9. `pamiatky_3d_modely.json` (Pamiatky a ich 3D modely 🏛️)\n"
                "- Predošlé vydanie `v4.0.0-maps` ostáva plne zachované."
            ),
            "draft": False,
            "prerelease": False,
        }
        release = api_request(
            f"https://api.github.com/repos/{REPO}/releases",
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
        )

    upload_base = release["upload_url"].split("{")[0]
    existing_names = {a["name"] for a in release.get("assets", [])}

    files = sorted(glob.glob(os.path.join(ASSETS_DIR, "*")))
    uploaded = 0
    for fpath in files:
        fname = os.path.basename(fpath)
        if fname in existing_names:
            continue
        with open(fpath, "rb") as f:
            raw = f.read()
        url = f"{upload_base}?name={fname}"
        api_request(url, method="POST", data=raw, content_type="application/json")
        uploaded += 1

    print(f"Release {TAG} ready. Uploaded {uploaded} new assets (total {len(files)} files).")


if __name__ == "__main__":
    main()
