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
SOURCE_EXPANSION = SOURCE_DIR / "arcade_interior_expansion.png"
SOURCE_CINEMA = SOURCE_DIR / "cinema_concessions_expansion.png"
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


def make_floor_tile(source: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """Convert one 32x32 orange floor module into one engine-ready 64x64 tile."""
    pattern = crop(source, box)
    tile = Image.new("RGBA", pattern.size, (104, 38, 27, 255))
    tile.alpha_composite(pattern)
    return tile.resize((CELL, CELL), Image.Resampling.NEAREST)


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


def compose_concession_table(table: Image.Image, items: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    table = fit(table, 56, 60)
    canvas.alpha_composite(table, ((64 - table.width) // 2, 64 - table.height))
    items = fit(items, 32, 25)
    canvas.alpha_composite(items, ((64 - items.width) // 2, 4))
    return canvas


def build_atlas() -> tuple[Image.Image, dict[str, dict]]:
    games = Image.open(SOURCE_GAMES).convert("RGBA")
    party = Image.open(SOURCE_PARTY).convert("RGBA")
    expansion = Image.open(SOURCE_EXPANSION).convert("RGBA")
    cinema = Image.open(SOURCE_CINEMA).convert("RGBA")
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
    orange_boxes = [
        (0, 192, 32, 224), (32, 192, 64, 224), (64, 192, 96, 224),
        (0, 224, 32, 256), (32, 224, 64, 256),
        (0, 288, 32, 320), (32, 288, 64, 320), (64, 288, 96, 320),
    ]
    for i, box in enumerate(orange_boxes):
        paste_full(atlas, i, make_floor_tile(games, box))
    for i, name in enumerate([
        "orange_floor_a", "orange_floor_b", "orange_floor_c", "orange_floor_d",
        "orange_floor_e", "orange_floor_f", "orange_floor_g", "orange_floor_h",
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
        register(13 + i, f"arcade_cabinet_{i + 6}", "arcade", "solid", "bottom-center")

    register_crop = crop(games, (172, 352, 246, 414))
    counter_cells = [
        crop(games, (96, 192, 160, 256)),
        crop(games, (160, 192, 224, 256)),
        crop(games, (96, 256, 160, 320)),
        crop(games, (160, 256, 224, 320)),
    ]
    counter_names = ["u_counter_top_left", "u_counter_top_right", "u_counter_bottom_left", "u_counter_bottom_right"]
    for i, counter in enumerate(counter_cells):
        paste_full(atlas, 16 + i, counter)
        register(16 + i, counter_names[i], "counter", "solid-interaction", "tile")
    put(atlas, 20, crop(base, (128, 64, 192, 128)), max_width=60, max_height=60)
    register(20, "arcade_lounge_seat", "furniture", "solid", "bottom-center")
    put(atlas, 21, register_crop, max_width=58, max_height=48)
    register(21, "prize_terminal", "counter", "solid-interaction", "bottom-center")
    put(atlas, 22, crop(base, (192, 128, 256, 192)), max_width=54, max_height=60)
    register(22, "ticket_machine", "counter", "solid-interaction", "bottom-center")
    put(atlas, 23, crop(base, (0, 128, 64, 192)), max_width=60, max_height=52)
    register(23, "prize_shelf", "counter", "solid", "bottom-center")

    large_table = crop(games, (0, 22, 96, 90))
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

    red_table = crop(cinema, (192, 416, 224, 488))
    yellow_table = crop(cinema, (224, 416, 256, 488))
    popcorn_table = compose_concession_table(red_table, crop(cinema, (0, 128, 64, 224)))
    drinks_table = compose_concession_table(yellow_table, crop(cinema, (64, 128, 128, 224)))
    expansion_items = [
        (45, crop(cinema, (128, 0, 192, 128)), "ticket_booth", "service", "solid-interaction"),
        (46, crop(cinema, (128, 128, 192, 224)), "popcorn_machine", "concessions", "solid-interaction"),
        (47, crop(cinema, (192, 128, 256, 224)), "soda_machine", "concessions", "solid-interaction"),
        (48, popcorn_table, "popcorn_table_red", "concessions", "solid-interaction"),
        (49, drinks_table, "drinks_table_yellow", "concessions", "solid-interaction"),
        (50, crop(cinema, (32, 320, 160, 448)), "cinema_seat_cluster", "furniture", "solid"),
        (51, red_table, "concession_table_red", "furniture", "solid"),
        (52, yellow_table, "concession_table_yellow", "furniture", "solid"),
        (53, crop(cinema, (0, 540, 64, 608)), "lounge_sofa_red", "furniture", "solid"),
        (54, crop(expansion, (196, 2, 252, 60)), "wall_drink_shelf", "concessions", "solid"),
        (55, crop(expansion, (2, 642, 30, 694)), "mini_refrigerator", "concessions", "solid-interaction"),
    ]
    for index, sprite, name, category, collision in expansion_items:
        put(atlas, index, sprite, max_width=60, max_height=60)
        register(index, name, category, collision, "bottom-center")

    # Dark room floors and wall variants remain available separately from the orange floor set.
    for i in range(4):
        paste_full(atlas, 56 + i, base_cells[i])
    paste_full(atlas, 60, base_cells[0].transpose(Image.Transpose.FLIP_LEFT_RIGHT))
    paste_full(atlas, 61, ImageEnhance.Brightness(base_cells[0]).enhance(0.72))
    paste_full(atlas, 62, base_cells[1].transpose(Image.Transpose.FLIP_LEFT_RIGHT))
    paste_full(atlas, 63, ImageEnhance.Brightness(base_cells[2]).enhance(0.82))
    for i, name in enumerate([
        "dark_floor_a", "dark_floor_b", "dark_floor_c", "wall_neon",
        "dark_floor_mirrored", "dark_floor_shadow", "dark_floor_edge", "dark_floor_dim",
    ]):
        register(56 + i, name, "terrain", "walkable" if i != 3 else "solid", "tile")

    return atlas, entries


def build_preview(atlas: Image.Image) -> Image.Image:
    width, height = 14, 10
    room = Image.new("RGBA", (width * CELL, height * CELL), (18, 13, 38, 255))

    def tile(index: int, x: int, y: int) -> None:
        sx, sy = cell_xy(index)
        room.alpha_composite(atlas.crop((sx, sy, sx + CELL, sy + CELL)), (x * CELL, y * CELL))

    for y in range(height):
        for x in range(width):
            tile(56 if y > 0 else 59, x, y)
    for y in range(4, 7):
        for x in range(2, 7):
            tile((x + y) % 8, x, y)
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
    tile(16, 9, 7)
    tile(17, 10, 7)
    tile(18, 9, 8)
    tile(19, 10, 8)
    tile(46, 11, 7)
    tile(47, 12, 7)
    tile(45, 13, 7)
    tile(48, 11, 8)
    tile(49, 12, 8)
    tile(55, 13, 8)
    tile(50, 8, 7)
    return room


def main() -> None:
    for path in (SOURCE_GAMES, SOURCE_PARTY, SOURCE_EXPANSION, SOURCE_CINEMA, SOURCE_BASE):
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
            str(SOURCE_EXPANSION.relative_to(PROJECT)),
            str(SOURCE_CINEMA.relative_to(PROJECT)),
            str(SOURCE_BASE.relative_to(PROJECT)),
        ],
        "rules": [
            "Indices 0 through 7 are orange edge-to-edge walkable floor tiles.",
            "Indices 56 through 63 are the dark room floor and wall variants.",
            "Arcade machines and counters are bottom-center anchored solid objects.",
            "The U-shaped counter is a fixed 2x2 module: 16-17 on top and 18-19 on the bottom.",
            "The source counter opens to the north; do not separate or rotate its quadrants independently.",
            "Birthday garlands, ceiling balloons, and loose balloons are overlays and do not block movement.",
            "The birthday cake table, game tables, cabinets, counters, and gift cluster have colliders.",
            "The popcorn machine, soda machine, ticket booth, concession tables, and refrigerator are solid interaction objects.",
            "Loose popcorn and drinks must never be placed on terrain; use composite table tiles 48 and 49.",
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
