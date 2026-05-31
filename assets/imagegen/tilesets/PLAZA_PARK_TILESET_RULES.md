# Plaza Park Tileset Rules

Use `plaza_park_tileset.png` as a 512x512 sheet with 64x64 cells.

## Draw Order

1. Terrain cells: grass, path, corners, transitions.
2. Prop cells: benches, trees, fountain, statue, lamps, flowerbeds.
3. Overlay cells: sparkles, flowers, sitting marker, border details.
4. Characters/NPCs.

## Collision

Use `solidCells` from `plaza_park_tileset.manifest.json`.

Benches are solid props, but each bench has `sitAnchorPx`. When the player/NPC sits, place the character visually at that anchor and lock movement until standing.

## Plaza Layout

- Paths must connect using cells 40-47.
- Fountains/statues should be focal points with at least one walkable ring around them.
- Benches should face paths or statues/fountains.
- Trees and flowerbeds should decorate edges, never block every route.
- Use grass variation cells 0-3 and 48-51 to avoid repeating flat green blocks.

## Recommended Composition

- 2-4 benches per plaza.
- 1 focal point: fountain or statue.
- 2-6 trees or bushes at the edges.
- Use lamps near path intersections.
- Use flower overlays sparingly so paths remain readable.
