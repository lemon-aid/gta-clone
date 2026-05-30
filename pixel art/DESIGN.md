---
name: Retro Urban Carnage
colors:
  surface: '#111125'
  surface-dim: '#111125'
  surface-bright: '#37374d'
  surface-container-lowest: '#0c0c1f'
  surface-container-low: '#1a1a2e'
  surface-container: '#1e1e32'
  surface-container-high: '#28283d'
  surface-container-highest: '#333348'
  on-surface: '#e2e0fc'
  on-surface-variant: '#e5bcc4'
  inverse-surface: '#e2e0fc'
  inverse-on-surface: '#2f2e43'
  outline: '#ac878f'
  outline-variant: '#5c3f45'
  surface-tint: '#ffb1c3'
  primary: '#ffb1c3'
  on-primary: '#66002c'
  primary-container: '#ff4b89'
  on-primary-container: '#590026'
  inverse-primary: '#bb0058'
  secondary: '#d3fbff'
  on-secondary: '#00363a'
  secondary-container: '#00eefc'
  on-secondary-container: '#00686f'
  tertiary: '#ffb94d'
  on-tertiary: '#452b00'
  tertiary-container: '#c48300'
  on-tertiary-container: '#3c2500'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffd9e0'
  primary-fixed-dim: '#ffb1c3'
  on-primary-fixed: '#3f0019'
  on-primary-fixed-variant: '#8f0041'
  secondary-fixed: '#7df4ff'
  secondary-fixed-dim: '#00dbe9'
  on-secondary-fixed: '#002022'
  on-secondary-fixed-variant: '#004f54'
  tertiary-fixed: '#ffddb2'
  tertiary-fixed-dim: '#ffb94d'
  on-tertiary-fixed: '#291800'
  on-tertiary-fixed-variant: '#624000'
  background: '#111125'
  on-background: '#e2e0fc'
  surface-variant: '#333348'
typography:
  headline-lg:
    fontFamily: Space Mono
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.05em
  headline-md:
    fontFamily: Space Mono
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-sm:
    fontFamily: Space Mono
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  body-lg:
    fontFamily: JetBrains Mono
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.5'
  body-md:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-lg:
    fontFamily: Courier Prime
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.0'
  label-sm:
    fontFamily: Courier Prime
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.0'
spacing:
  unit: 4px
  gutter-sm: 8px
  gutter-md: 16px
  margin-edge: 24px
  grid-cols: '12'
---

## Brand & Style

This design system is built on a foundation of **Neo-Retro Brutalism**, merging the raw, structural aggression of 1990s top-down arcade games with modern high-fidelity pixel aesthetics. The visual language is designed to evoke adrenaline, chaos, and urban grit through high-contrast vibrance.

The interface functions as a tactical overlay rather than a traditional HUD. It utilizes heavy strokes, sharp geometric angles, and "low-bit" density to ground the user in a world of high-stakes pixelated action. Every element feels deliberate, industrial, and high-energy, prioritizing immediate readability amidst visual noise.

## Colors

The palette is a high-octane "Midnight Neon" scheme. It uses a deep indigo-black base to allow the vibrant action colors—Neon Pink, Electric Cyan, and Radioactive Orange—to pop with maximum intensity.

- **Primary (Neon Pink):** Used for critical interactive elements, mission targets, and player health.
- **Secondary (Electric Cyan):** Reserved for technical readouts, vehicle stats, and "safe" zones.
- **Tertiary (Radioactive Orange):** Indicates warnings, explosions, and high-priority currency or collectibles.
- **Neutrals:** A spectrum of deep blues and grays that mimic asphalt and city shadows, keeping the UI grounded.

## Typography

This design system utilizes monospaced fonts to reinforce the "technical/hacker" vibe and ensure perfect vertical alignment, which is critical for the pixel-grid aesthetic. 

- **Headlines:** Use **Space Mono** for a futuristic, geometric look. Letter spacing is tight to create a dense, impactful "block" of text.
- **Body:** **JetBrains Mono** provides superior legibility for mission descriptions and dialogue, maintaining the monospaced theme without sacrificing readability.
- **Labels:** **Courier Prime** is used for small technical metadata and "stamped" UI elements, providing a subtle typewriter/dossier feel to the urban crime theme.

## Layout & Spacing

The layout is built on a **Strict Pixel Grid**. All spacing and sizing must be multiples of 4px to prevent "sub-pixel" blurring and maintain the integrity of the pixel art assets.

- **HUD Overlay:** Content is pushed to the corners with a 24px safe margin. 
- **Fixed Grid:** Modals and menus follow a 12-column grid but are often centered with heavy "blackout" backgrounds.
- **Density:** Spacing is tight (8px gutters) to simulate the cramped, bustling nature of a dense city map.

## Elevation & Depth

This design system rejects soft shadows and ambient occlusion. Depth is achieved through **Heavy Stroke Layers** and **Z-axis Color Shifts**.

1.  **Level 0 (Background):** The game world or deep neutral surfaces.
2.  **Level 1 (Panels):** Solid neutral surfaces with a 2px white or cyan border.
3.  **Level 2 (Active Elements):** Elements with an additional 4px "block shadow" (solid color offset, no blur) in a contrasting primary color.
4.  **Level 3 (Overlay):** Full-screen modals with a 50% opacity neutral-dark overlay and high-vibrance borders.

Visual depth is strictly flat; use "stair-step" offsets to simulate 3D instead of gradients.

## Shapes

The shape language is **Strictly Orthogonal**. 

- **Corners:** 0px radius (Sharp). Roundness is forbidden as it conflicts with the pixel-grid nature of the assets.
- **Borders:** Every container must have a visible border. Standard weight is 2px; primary/active weight is 4px.
- **Accents:** Use 45-degree chamfered corners on large panels (cut-off corners) to add a "tactical" industrial feel.

## Components

### Buttons
Buttons are solid blocks of color with a 2px black inner border and a 2px white outer border. On hover, the button shifts its position 2px down and 2px right, while the solid block shadow disappears, simulating a physical press.

### Chips / Tags
Small, high-contrast rectangles with monospaced text. Use secondary (Cyan) for "Weapon Type" and primary (Pink) for "Danger Level."

### Lists
Lists use alternating row backgrounds (Deep Blue / Indigo) with no gaps. Active rows are highlighted with a thick Neon Pink left-edge border (4px).

### Input Fields
Empty black boxes with a 2px white border. The cursor is a solid, blinking Cyan block.

### Cards / Panels
Large containers for stats or mission briefings. They feature a "Header Bar" in a contrasting color (e.g., Pink background with Black text) and a thick 4px border around the entire unit.

### Health & Ammo Bars
Segmented bars rather than smooth fills. Each "pip" represents a discrete unit of health or armor, matching the 4px grid unit.