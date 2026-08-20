#!/usr/bin/env python3
"""Import public reg2k WDL catalog gists into normalized JSON.

This only downloads the explicitly listed public text catalogs. It does not
read local game files or package proprietary binaries/assets.
"""
from __future__ import annotations

import argparse, json, re, urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = {
    "wdl_perks.txt": "https://gist.githubusercontent.com/reg2k/8b916a37839d4dbd8a94a78be9bb26d8/raw/wdl_perks.txt",
    "wdl_tags.txt": "https://gist.githubusercontent.com/reg2k/c8f4e5b1518df43a1a72a9f3fad0000b/raw/wdl_tags.txt",
    "wdl_prismactorlist.txt": "https://gist.githubusercontent.com/reg2k/e7065e241df1456dfba9f0bb7a1c6d24/raw/wdl_prismactorlist.txt",
    "wdl_contracts_attendances.txt": "https://gist.githubusercontent.com/reg2k/e753c82c6bc83099040b75cf12a9b552/raw/wdl_contracts_attendances.txt",
    "wdl_clothing_headwear.txt": "https://gist.githubusercontent.com/reg2k/2d5cb3c6867acc39a25ce7410ed3c17e/raw/wdl_clothing_headwear.txt",
    "wdl_clothing_innerwear.txt": "https://gist.githubusercontent.com/reg2k/2d5cb3c6867acc39a25ce7410ed3c17e/raw/wdl_clothing_innerwear.txt",
    "wdl_clothing_legwear.txt": "https://gist.githubusercontent.com/reg2k/2d5cb3c6867acc39a25ce7410ed3c17e/raw/wdl_clothing_legwear.txt",
    "wdl_clothing_outerwear.txt": "https://gist.githubusercontent.com/reg2k/2d5cb3c6867acc39a25ce7410ed3c17e/raw/wdl_clothing_outerwear.txt",
    "wdl_clothing_outfits.txt": "https://gist.githubusercontent.com/reg2k/2d5cb3c6867acc39a25ce7410ed3c17e/raw/wdl_clothing_outfits.txt",
    "wdl_clothing_wolfskin.txt": "https://gist.githubusercontent.com/reg2k/d0641a13fe8125252018e6804a6fda71/raw/wdl_clothing_wolfskin.txt",
    "wdl_character_models.txt": "https://gist.githubusercontent.com/reg2k/de52ef5fd40404598a80cc47c2307619/raw/wdl_character_models.txt",
    "wdl_charactercard.txt": "https://gist.githubusercontent.com/reg2k/d0e3d1b54bdeed25d43fa00c0a1ed8d8/raw/wdl_charactercard.txt",
    "wdl_characterdeck.txt": "https://gist.githubusercontent.com/reg2k/813f1e24cad68a574206fab50be24d9f/raw/wdl_characterdeck.txt",
    "wdl_profiler_metadata.txt": "https://gist.githubusercontent.com/reg2k/e2057f06b1904c9307aa595a200d5b32/raw/wdl_profiler_metadata.txt",
    "wdl_names.txt": "https://gist.githubusercontent.com/reg2k/cd66010c748f0a5a7f7e923d7b25ef5c/raw/wdl_names.txt",
    "wdl_surnames.txt": "https://gist.githubusercontent.com/reg2k/47ff62491b9d3ca0201808a1b8dcb2dc/raw/wdl_surnames.txt",
    "wdl_items_dump.txt": "https://gist.githubusercontent.com/reg2k/51952d262c98c6c9d1b28a1271ffaede/raw/wdl_items_dump.txt",
    "wdl_weapon_ability_ids.txt": "https://gist.githubusercontent.com/reg2k/ac1a6c3ece43c08ca042749bf4597dd9/raw/wdl_weapon_ability_ids.txt",
}

HEX_NAME = re.compile(r"^\s*([0-9A-Fa-f]{8,16})\s*[:|]\s*(.*?)\s*$")
def parse(text: str):
    rows = []
    for line in text.splitlines():
        m = HEX_NAME.match(line)
        if m and m.group(2) and set(m.group(2)) != {"-"}:
            rows.append({"id": m.group(1).upper(), "name": m.group(2).strip()})
    return rows

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("database/reg2k"))
    args = ap.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    retrieved = datetime.now(timezone.utc).isoformat()
    manifest = {"source": "https://gist.github.com/reg2k", "retrievedUtc": retrieved, "files": []}
    for name, url in SOURCES.items():
        with urllib.request.urlopen(url, timeout=30) as response:
            text = response.read().decode("utf-8", "replace")
        rows = parse(text)
        out = {"sourceUrl": url, "retrievedUtc": retrieved, "recordCount": len(rows), "records": rows}
        (args.output / (Path(name).stem + ".json")).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        manifest["files"].append({"file": name, "recordCount": len(rows), "sourceUrl": url})
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(manifest['files'])} catalogs into {args.output}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
