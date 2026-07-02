---
name: Aetheric Terminal
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#c7c4d8'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#918fa1'
  outline-variant: '#464555'
  surface-tint: '#c4c0ff'
  primary: '#c4c0ff'
  on-primary: '#2000a4'
  primary-container: '#8781ff'
  on-primary-container: '#1b0091'
  inverse-primary: '#4f44e2'
  secondary: '#bdf4ff'
  on-secondary: '#00363d'
  secondary-container: '#00e3fd'
  on-secondary-container: '#00616d'
  tertiary: '#bdc6e5'
  on-tertiary: '#273049'
  tertiary-container: '#8790ae'
  on-tertiary-container: '#202942'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e3dfff'
  primary-fixed-dim: '#c4c0ff'
  on-primary-fixed: '#100069'
  on-primary-fixed-variant: '#3622ca'
  secondary-fixed: '#9cf0ff'
  secondary-fixed-dim: '#00daf3'
  on-secondary-fixed: '#001f24'
  on-secondary-fixed-variant: '#004f58'
  tertiary-fixed: '#dae1ff'
  tertiary-fixed-dim: '#bdc6e5'
  on-tertiary-fixed: '#121b33'
  on-tertiary-fixed-variant: '#3d4660'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  container-max: 1440px
---

## Brand & Style

This design system embodies a high-fidelity, futuristic interface that bridges the gap between deep-space exploration and technical mastery. The aesthetic is a sophisticated fusion of **Glassmorphism** and **Corporate Modernism**, utilizing layered translucency to create a sense of vast digital space.

The brand personality is authoritative yet gamified—evoking the feeling of operating a high-end starship console while learning to code. It balances the cleanliness of a productivity tool with the immersive atmospheric depth of a sci-fi epic. Visuals should prioritize clarity of information (the "GitHub" influence) while utilizing vibrant neon accents and "orbital" motion patterns to maintain high engagement levels.

## Colors

The palette is anchored in a monochromatic "Deep Space" foundation, using varied depths of navy and obsidian to create architectural hierarchy. 

- **Primary Accent (Purple Neon):** Reserved for primary actions, milestones, and high-level progression. Use for "glow" effects to signify energy.
- **Secondary Accent (Cyan Neon):** Used for technical details, code syntax highlights, and HUD-style decorations.
- **Glass Surfaces:** Card backgrounds (#121B33) must always be applied with a 15-25% opacity and a 12px to 20px backdrop-blur to maintain legibility over background cosmic textures.
- **Borders:** Use a consistent `rgba(255, 255, 255, 0.08)` for inactive states, transitioning to primary or secondary gradients on interaction.

## Typography

The typographic system utilizes a three-tier hierarchy to balance technical precision with cinematic impact.

1.  **Headlines (Space Grotesk):** Geometric and futuristic. Use for page titles and major module headers.
2.  **Body (Inter):** High-readability sans-serif for instructional content, descriptions, and UI labels.
3.  **Technical (JetBrains Mono):** Used for all code blocks, HUD data readouts, and small metadata labels to reinforce the "programming" nature of the platform.

Text should primarily be White (#FFFFFF) for high contrast, with secondary information in Slate (#94A3B8). Neon colors should be used sparingly for text (e.g., status indicators) to prevent eye strain.

## Layout & Spacing

This design system employs a **Fluid Grid** with a strictly enforced 4px base-unit scale. 

- **Desktop:** 12-column grid with 24px gutters. Use wide margins (40px+) to allow the "Deep Space" background to breathe, creating a sense of isolation and focus.
- **Mobile:** 4-column grid with 16px margins.
- **HUD Layout:** Critical data should be anchored to the corners or perimeter of the screen (similar to a cockpit view), while the "Work Area" (Code Editor/Lessons) remains centered. 

Spacing between unrelated modules should be generous (64px+) to prevent the UI from feeling cluttered, maintaining the "Notion-like" cleanliness within a sci-fi context.

## Elevation & Depth

Depth is achieved through **Tonal Translucency** rather than traditional drop shadows.

- **Level 0 (Background):** Deep space (#060816) with subtle, non-distracting cosmic dust or blurred orbital paths.
- **Level 1 (Sub-surface):** #0D1326 for sidebar and navigation containers.
- **Level 2 (Cards/Modules):** Glassmorphic panels (#121B33 at 0.6 opacity) with a `1px` inner stroke of `white/0.08`.
- **Level 3 (Interactive):** When hovered, elements should emit a soft, localized outer glow (15px-30px blur) matching the primary or secondary accent color, simulating a powered-up state.

## Shapes

The shape language is "Soft-Tech"—modern and approachable but structurally sound. 

- **Standard Radius:** 8px (0.5rem) for most small components like inputs and chips.
- **Container Radius:** 16px (1rem) for cards and main UI panels to create a premium, friendly feel.
- **Interactive Elements:** Buttons and progress fills should use a 12px-16px radius.
- **HUD Accents:** Use 45-degree chamfered edges on small decorative corner pieces to reinforce the futuristic theme without making the overall UI feel sharp or hostile.

## Components

### Buttons
- **Primary:** Gradient fill (Primary to Secondary), 16px radius, white text. Hover: 1.05x scale transform and a 20px primary-color outer glow.
- **Secondary:** Ghost style with a 1.5px border. Hover: Fill with `rgba(255,255,255,0.05)`.

### Cards & Modules
- Semi-transparent background (#121B33 at 60%). 
- On hover, the border opacity should increase from 0.08 to 0.4, and the card should lift slightly (-4px Y-axis).

### HUD Progress Bars
- Background track: Dark navy (#0D1326).
- Fill: Linear gradient (Secondary to Primary) with a 4px "pulse" glow at the leading edge.

### Code Editor (The "Aether" Editor)
- Background: Solid #060816 to maximize focus.
- Syntax Highlighting: Use the Secondary Accent (Cyan) for variables and Primary (Purple) for keywords. 
- Line highlighting: A subtle horizontal band of `rgba(108, 99, 255, 0.1)`.

### Chips & Badges
- Pill-shaped (rounded-full).
- Low-opacity background fills with high-opacity text. Example: Success badge is `#22C55E` at 15% fill with solid `#22C55E` text.