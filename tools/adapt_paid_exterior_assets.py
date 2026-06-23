from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


PROJECT = Path(__file__).resolve().parents[1]
SRC_ROOT = (
    PROJECT
    / "assets"
    / "paid"
    / "Exterior"
    / "modernexteriors-win"
    / "Modern_Exteriors_48x48"
    / "ME_Theme_Sorter_48x48"
)
OUT_ROOT = PROJECT / "assets" / "paid_adapted" / "modern_exteriors_64"


TERRAIN = {
    "asphalt_clean": "2_City_Terrains_Singles_48x48/ME_Singles_City_Terrains_48x48_Asphalt_1_Variation_24.png",
    "asphalt_detail": "2_City_Terrains_Singles_48x48/ME_Singles_City_Terrains_48x48_Asphalt_1_Variation_25.png",
    "sidewalk": "2_City_Terrains_Singles_48x48/ME_Singles_City_Terrains_48x48_Sidewalk_1_1.png",
    "grass": "1_Terrains_and_Fences_Singles_48x48/ME_Singles_Terrains_and_Fences_48x48_Grass_1_10.png",
    "grass_edge": "1_Terrains_and_Fences_Singles_48x48/ME_Singles_Terrains_and_Fences_48x48_Grass_1_13.png",
}

PROPS = {
    "bench": "3_City_Props_Singles_48x48/ME_Singles_City_Props_48x48_Bench_1.png",
    "cone": "3_City_Props_Singles_48x48/ME_Singles_City_Props_48x48_Cone_3.png",
    "hydrant": "3_City_Props_Singles_48x48/ME_Singles_City_Props_48x48_Hydrant_1.png",
    "trash": "3_City_Props_Singles_48x48/ME_Singles_City_Props_48x48_Black_Closed_Trash_Can.png",
    "statue": "17_Garden_Singles_48x48/ME_Singles_Garden_48x48_Angel_Statue_1.png",
    "garden_bench": "17_Garden_Singles_48x48/ME_Singles_Garden_48x48_Big_Bench_Horizontal.png",
}

BUILDINGS = {
    "market_small": (
        "9_Shopping_Center_and_Markets_Singles_48x48/ME_Singles_Shopping_Center_and_Markets_48x48_Market_Small_1.png",
        192,
    ),
    "market_medium": (
        "9_Shopping_Center_and_Markets_Singles_48x48/ME_Singles_Shopping_Center_and_Markets_48x48_Market_Medium_1.png",
        256,
    ),
    "mall": (
        "9_Shopping_Center_and_Markets_Singles_48x48/ME_Singles_Shopping_Center_and_Markets_48x48_Mall_1.png",
        384,
    ),
    "hospital": (
        "12_Hotel_and_Hospital_Singles_48x48/ME_Singles_Hotel_and_Hospital_48x48_Hospital_1.png",
        384,
    ),
    "hotel": (
        "12_Hotel_and_Hospital_Singles_48x48/ME_Singles_Hotel_and_Hospital_48x48_Hotel_1.png",
        256,
    ),
    "police": (
        "15_Police_Station_Singles_48x48/ME_Singles_Police_Station_48x48_Police_Station_1.png",
        320,
    ),
    "police_small": (
        "15_Police_Station_Singles_48x48/ME_Singles_Police_Station_48x48_Police_Station_Small_1.png",
        192,
    ),
}


def load(rel: str) -> Image.Image:
    path = SRC_ROOT / rel
    if not path.exists():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGBA")


def save_tile(name: str, rel: str, manifest: dict) -> None:
    img = load(rel)
    out = OUT_ROOT / "terrain" / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.resize((64, 64), Image.Resampling.NEAREST).save(out)
    manifest["terrain"][name] = {
        "file": out.relative_to(PROJECT).as_posix(),
        "source": str((SRC_ROOT / rel).relative_to(PROJECT)),
        "size": [64, 64],
        "rule": "edge-to-edge terrain tile, no transparency padding",
    }


def save_prop(name: str, rel: str, manifest: dict) -> None:
    img = load(rel)
    scale = min(1.0, 60 / img.width, 60 / img.height)
    if img.width <= 48 and img.height <= 48:
        scale = min(60 / img.width, 60 / img.height)
    resized = img.resize(
        (max(1, round(img.width * scale)), max(1, round(img.height * scale))),
        Image.Resampling.NEAREST,
    )
    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((64 - resized.width) // 2, 64 - resized.height))
    out = OUT_ROOT / "props" / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    manifest["props"][name] = {
        "file": out.relative_to(PROJECT).as_posix(),
        "source": str((SRC_ROOT / rel).relative_to(PROJECT)),
        "size": [64, 64],
        "rule": "overlay prop, anchor at bottom center, transparent padding preserved",
    }


def save_building(name: str, rel: str, target_width: int, manifest: dict) -> None:
    img = load(rel)
    scale = target_width / img.width
    resized = img.resize(
        (target_width, max(1, round(img.height * scale))),
        Image.Resampling.NEAREST,
    )
    out = OUT_ROOT / "buildings" / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    resized.save(out)
    manifest["buildings"][name] = {
        "file": out.relative_to(PROJECT).as_posix(),
        "source": str((SRC_ROOT / rel).relative_to(PROJECT)),
        "sourceSize": [img.width, img.height],
        "size": [resized.width, resized.height],
        "rule": "uniformly resized facade copy; original paid asset is unchanged",
    }


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "sourceRoot": str(SRC_ROOT),
        "outputRoot": str(OUT_ROOT.relative_to(PROJECT)),
        "tileSize": 64,
        "terrain": {},
        "props": {},
        "buildings": {},
        "notes": [
            "Original paid assets are never overwritten.",
            "Terrain is normalized to 64x64 for the current Nolan City grid.",
            "Props are isolated 64x64 overlays with transparent RGBA background.",
            "Buildings are uniformly resized derivatives for preview map validation.",
        ],
    }
    for name, rel in TERRAIN.items():
        save_tile(name, rel, manifest)
    for name, rel in PROPS.items():
        save_prop(name, rel, manifest)
    for name, (rel, target_width) in BUILDINGS.items():
        save_building(name, rel, target_width, manifest)
    (OUT_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(OUT_ROOT)


if __name__ == "__main__":
    main()
