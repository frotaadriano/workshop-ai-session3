---
name: Consultative Innovation
colors:
  surface: '#fff8f6'
  surface-dim: '#f0d4ca'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1ec'
  surface-container: '#ffe9e2'
  surface-container-high: '#ffe2d8'
  surface-container-highest: '#f9dcd2'
  on-surface: '#271812'
  on-surface-variant: '#5b4137'
  inverse-surface: '#3e2c26'
  inverse-on-surface: '#ffede7'
  outline: '#8f7065'
  outline-variant: '#e4bfb1'
  surface-tint: '#a63b00'
  primary: '#a63b00'
  on-primary: '#ffffff'
  primary-container: '#ff5f00'
  on-primary-container: '#531a00'
  inverse-primary: '#ffb599'
  secondary: '#8f4089'
  on-secondary: '#ffffff'
  secondary-container: '#fea1f3'
  on-secondary-container: '#7c2f79'
  tertiary: '#0061a4'
  on-tertiary: '#ffffff'
  tertiary-container: '#0098fc'
  on-tertiary-container: '#002e52'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbce'
  primary-fixed-dim: '#ffb599'
  on-primary-fixed: '#370e00'
  on-primary-fixed-variant: '#7f2b00'
  secondary-fixed: '#ffd7f5'
  secondary-fixed-dim: '#ffaaf3'
  on-secondary-fixed: '#380038'
  on-secondary-fixed-variant: '#732770'
  tertiary-fixed: '#d1e4ff'
  tertiary-fixed-dim: '#9ecaff'
  on-tertiary-fixed: '#001d36'
  on-tertiary-fixed-variant: '#00497d'
  background: '#fff8f6'
  on-background: '#271812'
  surface-variant: '#f9dcd2'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-page: 40px
  stack-sm: 8px
  stack-md: 24px
  stack-lg: 48px
  section-padding: 80px
---

## Brand & Style

The design system is engineered for a premium, consultative experience that bridges the gap between high-level human expertise and cutting-edge technology. It targets enterprise decision-makers who value reliability, clarity, and forward-thinking digital transformation. 

The visual style is **Corporate Modern**: a disciplined evolution of traditional corporate aesthetics that prioritizes high contrast, rigorous alignment, and generous whitespace. It avoids ephemeral trends like excessive blurring or heavy gradients, instead opting for a crisp, "ink-on-paper" digital precision. The emotional response is one of confidence and clinical efficiency, punctuated by a vibrant orange that signals energy and technological momentum.

## Colors

The palette is anchored by a high-contrast relationship between a clean, off-white canvas and a dual-tone accent system. 

- **Primary Orange (#FF5F00):** Used exclusively for calls to action, active states, and critical data highlights. It represents innovation and progress.
- **Deep Purple (#500050):** Provides a sophisticated "anchor." Use this for secondary structural elements, sidebars, or as a background for high-impact content sections to create a premium, consultative feel.
- **Off-White Surface (#F8F9FA):** Reduces eye strain compared to pure white while maintaining a clinical, high-tech aesthetic.
- **Neutral Grays:** Text is kept at a dark charcoal (#2D2D2D) rather than pure black to soften the reading experience, while borders (#E0E0E0) provide subtle containment without breaking the flow of whitespace.

## Typography

This design system utilizes **Inter** for its utilitarian precision and exceptional legibility at all scales. The typography strategy focuses on a clear hierarchical scale that guides the user through complex information.

- **Headlines:** Use tight letter spacing and heavier weights to project authority. 
- **Body Text:** Generous line heights (1.5–1.6) are mandatory to ensure the "consultative" feel and high readability required for long-form reports or technical specs.
- **Labels:** Small caps or slightly tracked-out uppercase labels should be used for metadata and eyebrow headers to provide visual variety without introducing new typefaces.

## Layout & Spacing

The layout philosophy follows a **Fixed-Fluid Hybrid** model. Content is contained within a 1280px max-width grid to maintain readability, while background elements bleed to the edges. 

- **The 8px Rhythm:** All spacing must be a multiple of 8px. 
- **Generous Whitespace:** Section vertical padding is intentionally large (80px+) to allow the brand's premium nature to breathe. 
- **Grid:** A standard 12-column grid. For consultative dashboards, use a 4-column span for cards. For editorial content, use a centered 8-column span to optimize line length.

## Elevation & Depth

To maintain a "High-Tech" and "Clean" look, this design system eschews traditional heavy shadows in favor of **Tonal Layers** and **Low-Contrast Outlines**.

- **Level 0 (Background):** The off-white (#F8F9FA) base.
- **Level 1 (Cards/Surface):** Pure white (#FFFFFF) surfaces with a 1px border (#E0E0E0). 
- **Interactive Depth:** Only use shadows on "Active" states or floating modals. Shadows should be very diffused: `0px 10px 30px rgba(0, 0, 0, 0.04)`.
- **Primary Depth:** Deep Purple (#500050) sections act as a "basement" layer, providing a high-contrast backdrop for white text and orange accents.

## Shapes

The shape language is "Soft-Professional." By using an **8px to 12px corner radius**, the UI feels modern and approachable without losing its corporate edge.

- **Cards:** 12px radius for large containers.
- **Buttons & Inputs:** 8px radius for a tighter, more functional appearance.
- **Iconography:** Use a consistent 2px stroke weight with slightly rounded joins to match the component geometry.

## Components

- **Buttons:** Primary buttons use a solid Orange (#FF5F00) fill with white text. Secondary buttons use a Deep Purple (#500050) outline or text link. No gradients or inner glows.
- **Cards:** White background, 1px #E0E0E0 border, 12px radius. Internal padding should be a minimum of 32px to maintain the "premium" feel.
- **Input Fields:** 1px #E0E0E0 border that transitions to 2px Orange (#FF5F00) on focus. Labels sit above the field in `label-sm` style.
- **Chips:** Small, 4px radius, using a light gray tint (#F0F0F0) or light purple tint to categorize data without competing with primary actions.
- **Data Visualization:** Use Orange for the primary data point and Deep Purple for comparison sets. Background grids in charts should be #E0E0E0 at 0.5px width.
- **Navigation:** Top-tier navigation uses high-contrast text; active states are marked by a 3px bottom-border in Orange.