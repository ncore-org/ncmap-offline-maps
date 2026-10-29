#!/usr/bin/env python3
import json
import subprocess
import urllib.request
from pathlib import Path

MAPS_ROOT = Path("/home/alex/.nc/workspace/nc-apk/ncmap-offline-maps")


def get_token():
    url = subprocess.check_output(
        ["git", "-C", str(MAPS_ROOT), "remote", "get-url", "origin"],
        text=True,
    ).strip()
    # https://<token>@github.com/...
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


def main():
    token = get_token()

    # 1. Commit & push ncmap-offline-maps + tag v6.0.0-maps
    subprocess.run(["git", "-C", str(MAPS_ROOT), "add", "-A"], check=True)
    status = subprocess.check_output(["git", "-C", str(MAPS_ROOT), "status", "--porcelain"], text=True).strip()
    if status:
        subprocess.run(
            ["git", "-C", str(MAPS_ROOT), "commit", "-m", "feat(v6.0.0-maps): expand OsmAnd & Sygic offline maps catalog to 42 countries with SRTM 3D hills, showers & 3D landmarks"],
            check=True,
        )
    subprocess.run(["git", "-C", str(MAPS_ROOT), "tag", "-f", "v6.0.0-maps"], check=True)
    subprocess.run(["git", "-C", str(MAPS_ROOT), "push", "origin", "main", "v6.0.0-maps"], check=True)

    # 2. Create Release v6.0.0-maps on ncore-org/ncmap-offline-maps (preserving v5.0.0-maps and v4.0.0-maps)
    try:
        rel = gh_api(
            "POST",
            "/repos/ncore-org/ncmap-offline-maps/releases",
            token,
            {
                "tag_name": "v6.0.0-maps",
                "name": "NCMap Offline Maps v6.0.0-maps — 42 Countries (EU-27 + 15 OsmAnd Regions), SRTM 3D Hills, Showers & 3D Landmarks",
                "body": "Public multi-chunk offline map packages for `ncmap-offcial` v6.0.0 across 42 countries (all 27 EU member states + 15 OsmAnd European & North American regions) with 3D buildings, SRTM 3D hill profiles, highway rest areas with showers (`🚿`), speed cameras, and 3D UNESCO landmarks. Previous releases `v5.0.0-maps` and `v4.0.0-maps` remain preserved.",
                "draft": False,
                "prerelease": False,
            },
        )
    except Exception:
        rel = gh_api("GET", "/repos/ncore-org/ncmap-offline-maps/releases/tags/v6.0.0-maps", token)

    upload_url_base = rel["upload_url"].split("{")[0]
    cat_bytes = (MAPS_ROOT / "catalog_v6.json").read_bytes()
    try:
        gh_api(
            "POST",
            f"{upload_url_base}?name=catalog_v6.json",
            token,
            cat_bytes,
            content_type="application/json",
        )
    except Exception as e:
        print("catalog_v6.json upload note:", e)

    # 3. Set GitHub repository topics/tags on both repositories
    topics_app = [
        "navigation",
        "gps",
        "osmand",
        "sygic",
        "flutter",
        "kotlin",
        "cpp17",
        "android-auto",
        "carplay",
        "3d-maps",
        "offline-maps",
        "openstreetmap",
        "dem-terrain",
        "foreground-service",
    ]
    res_app = gh_api("PUT", "/repos/ncore-org/ncmap-offcial/topics", token, {"names": topics_app})
    res_maps = gh_api("PUT", "/repos/ncore-org/ncmap-offline-maps/topics", token, {"names": topics_app})
    print("Topics set on ncmap-offcial:", res_app.get("names"))
    print("Topics set on ncmap-offline-maps:", res_maps.get("names"))


if __name__ == "__main__":
    main()
