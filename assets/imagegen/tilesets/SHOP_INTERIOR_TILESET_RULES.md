# Shop Interior Tileset Rules

Each shop interior has its own 256x256 PNG sheet in `assets/imagegen/tilesets/shops/`.

## Grid

- Sheet size: 256x256
- Grid: 4x4
- Cell size: 64x64
- Use `shop_interiors_manifest.json` as the source of truth.

## Required Room Layout

- Recommended room size: 9x7 tiles or larger.
- Back row should use wall tiles: cells 2 and 3.
- Floor should use cells 0 and 1.
- Door/entrance should use cell 12.
- Counter should be near the back wall and at least 3 tiles wide:
  - cell 4 = counter left
  - cell 5 = counter middle
  - cell 6 = counter right
  - cell 7 = front/service counter module
- Attendant NPC stands behind the counter.
- Player interaction tile is directly in front of the counter, usually a walkable floor/rug tile.

## Collision

Solid cells:
2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15

Walkable cells:
0, 1, 12, 13

## Rendering

Draw terrain first: floor, wall, door and rug.
Draw overlay/object tiles next: counter, shelves and props.
Counters are both visible overlays and collision objects.

## Style Themes

- `store`: blue/purple shop with pink/cyan/yellow accents.
- `cafe`: warm brown cafe with neon pink/cyan accents.
- `mechanic`: gray/brown garage with orange/yellow tool accents.
- `flower`: green/pink florist with plant props.
- `hospital`: white, cyan and soft pink clinic interior.
- `arcade`: purple neon arcade with machines.
- `car_dealer`: polished dark showroom with magenta/gold/cyan accents.
