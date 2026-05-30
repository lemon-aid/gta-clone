# City Tileset And Map Rules

These rules define how the city tileset must behave before generating or composing new chunks.

## Road System

- Roads must be continuously connected. No isolated fragments.
- Every road tile must declare open edges: `N`, `S`, `E`, `W`.
- Adjacent road tiles must have reciprocal edges:
  - `E` must touch `W`
  - `N` must touch `S`
- Roads must support two-way traffic.
- Prefer two-lane roads with one lane per direction.
- Road width must fit at least two cars side by side without overlap.
- Lane centers must be fixed and reusable across all road tiles.
- Intersections, turns, T-junctions, and crosswalks must preserve the same lane centers.
- Crosswalks must span the full road width and connect sidewalk to sidewalk.
- Road tiles must not contain painted direction arrows unless they are a special debug overlay or explicit road marking tile.
- Traffic direction belongs in map metadata/pathing, not baked into the base terrain art.
- Create pavement/city-block tiles with curb or sidewalk borders, so blocks can sit close to roads while preserving a pedestrian edge.

## Cars And Traffic Flow

- Cars must always sit on a valid lane.
- Cars must face the correct travel direction for that lane.
- Cars must not be centered on the whole road if the road has multiple lanes; they must be centered in their lane.
- Parked cars belong only in parking spaces or curb/parking tiles.
- Traffic routes should be represented as a graph or lane path before placing vehicles.

## Sidewalks

- Every road should have sidewalk access on city-block sides.
- Sidewalks must form walkable continuous strips along streets.
- Buildings must never touch roads directly.
- At least one full sidewalk tile must exist between every building footprint and the road.
- Crosswalks must connect two sidewalk areas.
- Pavement/block tiles should have clear curb borders where they meet roads.
- Grass-to-pavement borders need dedicated transition tiles, not hard rectangular color changes.

## Buildings

- Buildings must sit on city blocks, not inside the road graph.
- Building entrances must face a sidewalk, plaza, or pedestrian area.
- Facades should use consistent ground baselines.
- Important buildings should be multi-tile modules, not tiny isolated icons:
  - cafe: 2x1 or 2x2
  - hospital: 2x2 or larger
  - police station: 2x2 or larger
  - parking garage: 2x2 or larger with driveway connection
  - apartment/shop facades: 1x1, 2x1, or 2x2

## Parks And Props

- Parks should occupy defined blocks or plazas.
- Trees, benches, fountains, lamps, semaphores, hydrants, trash bins, and signs should be placed on sidewalks, plazas, park tiles, or parking areas.
- Cones and barriers may be placed on roads only when intended as obstacles or construction events.
- Props must not block car-flow paths unless marked as obstacles.
- Traffic lights/semaphores should usually be overlays or small object sprites placed on corners/curbs. They should not consume a full terrain tile.

## Tile Types To Generate

### Terrain Tiles

Terrain tiles must be seamless edge-to-edge.

- sidewalk
- grass
- park grass
- plaza pavement
- two-lane road straight horizontal
- two-lane road straight vertical
- two-lane corners
- two-lane T-junctions
- two-lane four-way intersection
- crosswalk horizontal
- crosswalk vertical
- parking lot tile
- parking entrance/driveway
- pavement full tile
- pavement with curb top/bottom/left/right
- grass full tile
- grass-to-pavement edge and corner transitions

### Object Sprites

Object sprites may use transparent padding.

- trees
- benches
- semaphores
- lamps
- cones
- barriers
- hydrants
- trash bins
- signs
- planters
- fountains

### Building Modules

Buildings should be larger modules with consistent sidewalk-facing entrances.

- 10 varied building facades
- cafes
- hospital
- police station
- parking garage

## City Chunk Validation

Before accepting a city chunk:

- Confirm all roads belong to one connected graph unless intentionally separated.
- Confirm all road connections match adjacent open edges.
- Confirm every building has at least one sidewalk tile between it and the road.
- Confirm every car is on a valid lane and points in the lane direction.
- Confirm the road width supports two cars side by side.
- Confirm crosswalks connect sidewalk-to-sidewalk across the full road width.
- Confirm props do not block active lanes.
- Confirm parks and plazas are coherent blocks, not random props scattered across roads.
