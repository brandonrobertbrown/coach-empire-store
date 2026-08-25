#!/usr/bin/env python3
"""Coach Empire — packager. Builds shippable zips for all products under Empire/products/.

Usage:
    python package_products.py            # build/refresh all product zips
    python package_products.py --verify   # list zips + contents summary
"""
from __future__ import annotations

import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

EMPIRE = Path(__file__).resolve().parent
PRODUCTS = EMPIRE / "products"
RELEASES = EMPIRE / "releases"


def build_zip(product_dir: Path) -> Path | None:
    """Zip everything in a product dir except prior zips and packaging script."""
    if not product_dir.is_dir():
        return None
    name = product_dir.name
    RELEASES.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out = RELEASES / f"{name}_v{stamp}.zip"
    if out.exists():
        print(f"  [skip] {out.name} already exists")
        return out
    files = [
        p for p in sorted(product_dir.rglob("*"))
        if p.is_file() and p.suffix != ".zip" and p.name != "package_products.py"
    ]
    if not files:
        print(f"  [warn] {name}: no files to zip")
        return None
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=str(f.relative_to(product_dir)))
    print(f"  [ok] {out} ({out.stat().st_size:,} bytes, {len(files)} files)")
    return out


def main() -> int:
    args = sys.argv[1:]
    if "--verify" in args:
        for z in sorted(RELEASES.glob("*.zip")) if RELEASES.exists() else []:
            with zipfile.ZipFile(z) as zf:
                names = zf.namelist()
            print(f"{z.name}: {len(names)} files, {z.stat().st_size:,} bytes")
            for n in names[:8]:
                print(f"   - {n}")
        return 0

    manifest = {"built_utc": datetime.now(timezone.utc).isoformat(), "products": {}}
    print("Packaging empire products...")
    for d in sorted(PRODUCTS.iterdir()) if PRODUCTS.exists() else []:
        if not d.is_dir():
            continue
        print(f" {d.name}:")
        z = build_zip(d)
        if z:
            manifest["products"][d.name] = {
                "zip": str(z), "size_bytes": z.stat().st_size,
                "files": len([p for p in d.rglob('*') if p.is_file()]),
            }
    (EMPIRE / "releases" / "_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest: {EMPIRE / 'releases' / '_manifest.json'}")
    print(f"Products packaged: {len(manifest['products'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
