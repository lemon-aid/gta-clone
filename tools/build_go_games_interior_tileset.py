from __future__ import annotations

import colorsys
import json
from pathlib import Path

from PIL import Image, ImageEnhance


PROJECT = Path(__file__).resolve().parents[1]
TILESET_DIR = PROJECT / "assets" / "imagegen" / "tilesets"
SOURCE_DIR = TILESET_DIR / "tileset - arcade"
SOURCE_GAMES = SOURCE_DIR / "diftexb-558648e2-1f27-424c-8939-0ffb3dbb6b37.png"
SOURCE_PARTY = SOURCE_DIR / "di592ye-36f28ac7-13a5-461d-b1b5-b7026ee357bb.png"
SOURCE_BASE = TILESET_DIR / "shops" / "shop_arcade_interior_tileset.png"
OUTPUT = TILESET_DIR / "shops" / "go_games_interior_tileset.png"
PREVIEW = TILESET_DIR / "shops" / "go_games_interior_preview.png"
MANIFEST = TILESET_DIR / "shops" / "go_games_interior_tileset.manifest.json"

CELL = 64
COLS = 8
ROWS = 8


def crop(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    return image.crop(box).convert("RGBA")


def fit(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    image = image.crop(bbox)
    scale = min(max_width / image.width, max_height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.NEAREST)


def hue_shift(image: Image.Image, degrees: float) -> Image.Image:
    image = image.convert("RGBA")
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            h = (h + degrees / 360) % 1
            rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
            px[x, y] = (round(rr * 255), round(gg * 255), round(bb * 255), a)
    return image


def cell_xy(index: int) -> tuple[int, int]:
    return (index % COLS) * CELL, (index // COLS) * CELL


def put(
    atlas: Image.Image,
    index: int,
    sprite: Image.Image,
    *,
    max_width: int = 60,
    max_height: int = 60,
    anchor: str = "bottom",
    offset_x: int = 0,
    offset_y: int = 0,
) -> None:
    sprite = fit(sprite, max_width, max_height)
    cell_x, cell_y = cell_xy(index)
    x = cell_x + (CELL - sprite.width) // 2 + offset_x
    if anchor == "center":
        y = cell_y + (CELL - sprite.height) // 2 + offset_y
    elif anchor == "top":
        y = cell_y + 2 + offset_y
    else:
        y = cell_y + CELL - sprite.height - 2 + offset_y
    atlas.alpha_composite(sprite, (x, y))


def paste_full(atlas: Image.Image, index: int, image: Image.Image) -> None:
    x, y = cell_xy(index)
    atlas.alpha_composite(image.resize((CELL, CELL), Image.Resampling.NEAREST), (x, y))


def make_carpet(base_floor: Image.Image, overlay: Image.Image) -> Image.Image:
    tile = base_floor.copy().convert("RGBA")
    overlay = overlay.resize((CELL, CELL), Image.Resampling.NEAREST)
    tile.alpha_composite(overlay)
    return tile


def compose_party_table(table: Image.Image, cake: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    table = fit(table, 116, 92)
    canvas.alpha_composite(table, ((128 - table.width) // 2, 34))
    cake = fit(cake, 38, 34)
    canvas.alpha_composite(cake, ((128 - cake.width) // 2, 20))
    return canvas


def compose_counter(base: Image.Image, register: Image.Image | None = None) -> Image.Image:
    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    canvas.alpha_composite(base.resize((64, 64), Image.Resampling.NEAREST))
    if register is not None:
        register = fit(register, 30, 22)
        canvas.alpha_composite(register, ((64 - register.width) // 2, 8))
    return canvas


def build_atlas() -> tuple[Image.Image, dict[str, dict]]:
    games = Image.open(SOURCE_GAMES).convert("RGBA")
    party = Image.open(SOURCE_PARTY).convert("RGBA")
    base = Image.open(SOURCE_BASE).convert("RGBA")
    atlas = Image.new("RGBA", (COLS * CELL, ROWS * CELL), (0, 0, 0, 0))
    entries: dict[str, dict] = {}

    def register(index: int, name: str, category: str, collision: str, anchor: str) -> None:
        entries[name] = {
            "index": index,
            "row": index // COLS,
            "column": index % COLS,
            "category": category,
            "collision": collision,
            "anchor": anchor,
        }

    base_cells = [crop(base, (x * 64, 0, x * 64 + 64, 64)) for x in range(4)]
    paste_full(atlas, 0, base_cells[0])
    paste_full(atlas, 1, base_cells[1])
    paste_full(atlas, 2, base_cells[2])
    paste_full(atlas, 3, base_cells[3])
    carpet_a = crop(games, (0, 192, 64, 256))
    carpet_b = crop(games, (0, 288, 64, 352))
    paste_full(atlas, 4, make_carpet(base_cells[0], carpet_a))
    paste_full(atlas, 5, make_carpet(base_cells[0], carpet_b))
    paste_full(atlas, 6, crop(base, (0, 0, 64, 64)).transpose(Image.Transpose.FLIP_LEFT_RIGHT))
    paste_full(atlas, 7, ImageEnhance.Brightness(base_cells[0]).enhance(0.72))
    for i, name in enumerate([
        "floor_neon_a", "floor_neon_b", "floor_neon_c", "wall_neon",
        "party_carpet_a", "party_carpet_b", "floor_mirrored", "floor_shadow",
    ]):
        register(i, name, "terrain", "walkable", "tile")

    cabinets = [crop(games, (96 + i * 32, 106, 128 + i * 32, 186)) for i in range(5)]
    for i, cabinet in enumerate(cabinets):
        put(atlas, 8 + i, cabinet, max_width=30, max_height=60)
        register(8 + i, f"arcade_cabinet_{i + 1}", "arcade", "solid", "bottom-center")
    put(atlas, 13, hue_shift(cabinets[0], 55), max_width=30, max_height=60)
    put(atlas, 14, hue_shift(cabinets[1], 165), max_width=30, max_height=60)
    put(atlas, 15, hue_shift(cabinets[2], 260), max_width=30, max_height=60)
    for i in range(3):
        register(13 + i, f"arcade_cabinet_bonus_{i + 1}", "arcade", "solid", "bottom-center")

    register_crop = crop(games, (172, 352, 246, 414))
    counter_cells = [crop(base, (x * 64, 64, x * 64 + 64, 128)) for x in range(4)]
    counter_names = ["counter_left", "counter_middle", "counter_right", "counter_corner"]
    for i, counter in enumerate(counter_cells):
        paste_full(atlas, 16 + i, counter)
        register(16 + i, counter_names[i], "counter", "solid", "tile")
    paste_full(atlas, 20, compose_counter(counter_cells[1], register_crop))
    register(20, "counter_register", "counter", "solid-interaction", "tile")
    put(atlas, 21, register_crop, max_width=58, max_height=48)
    register(21, "prize_terminal", "counter", "solid-interaction", "bottom-center")
    put(atlas, 22, crop(base, (192, 128, 256, 192)), max_width=54, max_height=60)
    register(22, "ticket_machine", "counter", "solid-interaction", "bottom-center")
    put(atlas, 23, crop(base, (0, 128, 64, 192)), max_width=60, max_height=52)
    register(23, "prize_shelf", "counter", "solid", "bottom-center")

    large_table = crop(games, (96, 192, 224, 320))
    cake_large = crop(party, (42, 15, 86, 61))
    cake_small = crop(party, (46, 64, 82, 96))
    party_table = compose_party_table(large_table, cake_large)
    put(atlas, 24, party_table, max_width=62, max_height=62)
    register(24, "birthday_table_with_cake", "party", "solid-interaction", "bottom-center")
    put(atlas, 25, cake_large, max_width=48, max_height=46)
    register(25, "birthday_cake_large", "party", "overlay", "center")
    put(atlas, 26, cake_small, max_width=42, max_height=38)
    register(26, "birthday_cake_small", "party", "overlay", "center")
    put(atlas, 27, crop(party, (128, 194, 224, 254)), max_width=60, max_height=58)
    register(27, "gift_cluster", "party", "solid", "bottom-center")
    put(atlas, 28, crop(party, (6, 164, 58, 254)), max_width=52, max_height=60)
    register(28, "balloon_cluster_a", "party", "overlay", "bottom-center")
    put(atlas, 29, crop(party, (71, 164, 123, 254)), max_width=52, max_height=60)
    register(29, "balloon_cluster_b", "party", "overlay", "bottom-center")
    put(atlas, 30, crop(party, (20, 88, 172, 160)), max_width=62, max_height=38, anchor="top")
    register(30, "birthday_garland", "party", "overlay-no-collision", "top-center")
    put(atlas, 31, crop(party, (128, 0, 224, 64)), max_width=62, max_height=58, anchor="top")
    register(31, "ceiling_balloons", "party", "overlay-no-collision", "top-center")

    games_row = [
        (crop(games, (0, 22, 96, 90)), "pool_table_horizontal"),
        (crop(games, (102, 6, 154, 90)), "pool_table_vertical"),
        (crop(games, (166, 10, 216, 90)), "air_hockey_vertical"),
        (crop(games, (10, 118, 84, 186)), "air_hockey_horizontal"),
        (crop(games, (0, 389, 31, 468)), "arcade_sofa"),
        (register_crop, "multiplayer_console"),
    ]
    for i, (sprite, name) in enumerate(games_row):
        put(atlas, 32 + i, sprite, max_width=60, max_height=60)
        register(32 + i, name, "games", "solid-interaction", "bottom-center")
    put(atlas, 38, crop(party, (1, 8, 31, 64)), max_width=46, max_height=46)
    register(38, "snack_plate", "party", "overlay", "center")
    put(atlas, 39, crop(party, (128, 160, 224, 192)), max_width=60, max_height=34)
    register(39, "birthday_candles", "party", "overlay", "center")

    # Remaining cells are intentionally spare variations and decor overlays.
    decor = [
        (crop(party, (97, 0, 125, 64)), "balloon_blue"),
        (crop(party, (131, 0, 159, 64)), "balloon_red"),
        (crop(party, (161, 0, 189, 64)), "balloon_green"),
        (crop(party, (195, 0, 223, 64)), "balloon_gold"),
        (crop(party, (197, 96, 219, 150)), "party_pinata"),
    ]
    for i, (sprite, name) in enumerate(decor):
        put(atlas, 40 + i, sprite, max_width=46, max_height=60, anchor="top")
        register(40 + i, name, "party", "overlay-no-collision", "top-center")

    # Duplicate useful floor variants in the last row for editor convenience.
    for i in range(8):
        paste_full(atlas, 56 + i, atlas.crop((*cell_xy(i), cell_xy(i)[0] + 64, cell_xy(i)[1] + 64)))
        register(56 + i, f"editor_floor_copy_{i + 1}", "terrain", "walkable", "tile")

    return atlas, entries


def build_preview(atlas: Image.Image) -> Image.Image:
    width, height = 14, 10
    room = Image.new("RGBA", (width * CELL, height * CELL), (18, 13, 38, 255))

    def tile(index: int, x: int, y: int) -> None:
        sx, sy = cell_xy(index)
        room.alpha_composite(atlas.crop((sx, sy, sx + CELL, sy + CELL)), (x * CELL, y * CELL))

    for y in range(height):
        for x in range(width):
            tile(0 if y > 0 else 3, x, y)
    for x in range(2, 7):
        tile(4 if x % 2 == 0 else 5, x, 5)
    for x, index in enumerate([8, 9, 10, 11, 12, 13, 14, 15], start=1):
        tile(index, x, 1)
    for y, index in enumerate([8, 10, 12, 14], start=2):
        tile(index, 12, y)
    tile(30, 4, 2)
    tile(31, 5, 2)
    tile(28, 2, 3)
    tile(24, 4, 4)
    tile(27, 6, 4)
    tile(29, 7, 3)
    tile(32, 2, 7)
    tile(35, 4, 7)
    tile(36, 6, 7)
    for x, index in enumerate([16, 17, 20, 18], start=9):
        tile(index, x, 8)
    tile(23, 9, 7)
    tile(22, 11, 7)
    return room


def main() -> None:
    for path in (SOURCE_GAMES, SOURCE_PARTY, SOURCE_BASE):
        if not path.exists():
            raise FileNotFoundError(path)
    atlas, entries = build_atlas()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(OUTPUT)
    build_preview(atlas).save(PREVIEW)
    manifest = {
        "name": "Go Games Interior",
        "format": "PNG RGBA",
        "tileSize": [64, 64],
        "atlasSize": [atlas.width, atlas.height],
        "columns": COLS,
        "rows": ROWS,
        "sources": [
            str(SOURCE_GAMES.relative_to(PROJECT)),
            str(SOURCE_PARTY.relative_to(PROJECT)),
            str(SOURCE_BASE.relative_to(PROJECT)),
        ],
        "rules": [
            "Terrain cells are edge-to-edge and walkable unless noted otherwise.",
            "Arcade machines and counters are bottom-center anchored solid objects.",
            "Counters form a modular horizontal service line; the register cell is the interaction point.",
            "Birthday garlands, ceiling balloons, and loose balloons are overlays and do not block movement.",
            "The birthday cake table, game tables, cabinets, counters, and gift cluster have colliders.",
            "Place at least one walkable tile in front of every arcade machine and counter interaction point.",
        ],
        "entries": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(OUTPUT)
    print(PREVIEW)
    print(MANIFEST)


if __name__ == "__main__":
    main()
