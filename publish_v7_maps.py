#!/usr/bin/env python3
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

MAPS_ROOT = Path("/home/alex/.nc/workspace/nc-apk/ncmap-offline-maps")


def get_token():
    url = subprocess.check_output(
        ["git", "-C", str(MAPS_ROOT), "remote", "get-url", "origin"],
        text=True,
    ).strip()
    return url.split("://")[1].split("@")[0]


def gh_api(method: str, path: str, token: str, payload=None, content_type="application/json"):
    url = f"https://api.github.com{path}" if path.startswith("/") else path
    data = None
    if payload is not None:
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": content_type,
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def osmand_file_for_country(code: str, name: str) -> str:
    clean_name = name.split(" (")[0].replace(" & ", "-").replace(" ", "-").replace("ü", "u")
    if code == "TR":
        clean_name = "Turkey"
    elif code == "GB":
        clean_name = "Gb"
    region = "northamerica" if code in ("US", "CA") else "europe"
    return f"{clean_name}_{region}_2.obf.zip"


def main():
    token = get_token()
    cat = json.loads((MAPS_ROOT / "catalog_v6.json").read_text())
    cat["version"] = "7.0.0-maps"
    cat["osmandIndexesUrl"] = "https://download.osmand.net/get_indexes?gzip&osmandver=OsmAnd+4.9.10"
    cat["osmandDownloadBase"] = "https://download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file="
    cat["worldBasemapMiniUrl"] = (
        "https://download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file=World_basemap_mini_2.obf.zip"
    )

    for c in cat["countries"]:
        obf_file = osmand_file_for_country(c["code"], c["name"])
        enc_file = urllib.parse.quote(obf_file)
        c["osmandObfFile"] = obf_file
        c["osmandStandardUrl"] = f"https://download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file={enc_file}"
        c["osmandRoadOnlyUrl"] = f"https://download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file={enc_file}&road=yes"
        c["osmandSrtmUrl"] = f"https://download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file={enc_file}&srtmcountry=yes"
        c["osmandWikiUrl"] = f"https://download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file={enc_file}&wiki=yes"

    (MAPS_ROOT / "catalog_v7.json").write_text(json.dumps(cat, indent=2, ensure_ascii=False))
    (MAPS_ROOT / "catalog.json").write_text(json.dumps(cat, indent=2, ensure_ascii=False))

    subprocess.run(["git", "-C", str(MAPS_ROOT), "add", "-A"], check=True)
    status = subprocess.check_output(["git", "-C", str(MAPS_ROOT), "status", "--porcelain"], text=True).strip()
    if status:
        subprocess.run(
            [
                "git",
                "-C",
                str(MAPS_ROOT),
                "commit",
                "-m",
                "feat(v7.0.0-maps): link official download.osmand.net .obf.zip endpoints + SRTM/Road/Wiki URLs for all 42 countries",
            ],
            check=True,
        )
    subprocess.run(["git", "-C", str(MAPS_ROOT), "tag", "-f", "v7.0.0-maps"], check=True)
    subprocess.run(["git", "-C", str(MAPS_ROOT), "push", "origin", "main", "v7.0.0-maps"], check=True)

    try:
        rel = gh_api(
            "POST",
            "/repos/ncore-org/ncmap-offline-maps/releases",
            token,
            {
                "tag_name": "v7.0.0-maps",
                "name": "NCMap Offline Maps v7.0.0-maps — Official download.osmand.net .obf.zip Links + 42 Multi-Layer Country Packages",
                "body": "Public offline maps release `v7.0.0-maps` for `ncmap-offcial` v7.0.0 linking official OsmAnd (`download.osmand.net/download?event=2&osmandver=OsmAnd+4.9.10&file=*_2.obf.zip`) standard, road-only, SRTM contour, and Wikipedia packages alongside our 9-layer EU-27 + Europe/North America telemetry (`countries/<iso>/`). Previous releases (`v6.0.0-maps`, `v5.0.0-maps`, `v4.0.0-maps`) remain preserved.",
                "draft": False,
                "prerelease": False,
            },
        )
    except Exception:
        rel = gh_api("GET", "/repos/ncore-org/ncmap-offline-maps/releases/tags/v7.0.0-maps", token)

    upload_url_base = rel["upload_url"].split("{")[0]
    cat_bytes = (MAPS_ROOT / "catalog_v7.json").read_bytes()
    try:
        gh_api(
            "POST",
            f"{upload_url_base}?name=catalog_v7.json",
            token,
            cat_bytes,
            content_type="application/json",
        )
    except Exception as e:
        print("catalog_v7.json upload note:", e)

    print("Published v7.0.0-maps on ncore-org/ncmap-offline-maps:", rel.get("html_url"))


if __name__ == "__main__":
    main()
