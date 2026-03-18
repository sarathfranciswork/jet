# Jet — Brand Identity Specification

**Status:** Approved
**Date:** 2026-03-18
**Decided by:** AI-recommended, user-approved

---

## Brand Name

**Name:** Jet
**Tagline:** "Ship faster with Jet"
**Full Description:** Jet — Open-source, self-hosted project management at speed

---

## Logo Mark: Chevron "J"

**Concept:** A bold geometric "J" constructed from angular chevron shapes — like a navigation arrow pointing forward and upward. The mark conveys speed, precision, and forward momentum.

**Properties:**
- Angular/geometric construction — no curves
- Works at all sizes from 16px favicon to full display
- Single-color mark (works in mono, primary, and inverted)
- The "J" is immediately recognizable but abstract enough to be distinctive
- Negative space creates an implied forward-pointing arrow

**Variants:**
- **Icon only** — The chevron "J" mark (favicon, app icon, small contexts)
- **Wordmark** — "Jet" in Space Grotesk Bold alongside the mark
- **Lockup** — Icon + wordmark horizontal (header, README, marketing)

---

## Color Palette: Jet Black

**Philosophy:** Dark-first, developer-credible aesthetic inspired by Vercel/Linear. High contrast, minimal, professional. Electric blue accent for energy and interactivity.

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Jet Black | `#09090B` | 9, 9, 11 | Primary background (dark mode) |
| Jet Dark | `#18181B` | 24, 24, 27 | Card/surface background |
| Jet Gray | `#27272A` | 39, 39, 42 | Elevated surfaces, borders |
| Jet Steel | `#3F3F46` | 63, 63, 70 | Secondary borders, dividers |
| Jet Silver | `#A1A1AA` | 161, 161, 170 | Secondary text |
| Jet White | `#FAFAFA` | 250, 250, 250 | Primary text, headings |

### Accent Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Jet Blue | `#3B82F6` | 59, 130, 246 | Primary accent, links, active states |
| Jet Cyan | `#06B6D4` | 6, 182, 212 | Hover states, highlights, gradients |
| Jet Emerald | `#10B981` | 16, 185, 129 | Success states, completed |
| Jet Amber | `#F59E0B` | 245, 158, 11 | Warnings, in-progress |
| Jet Red | `#EF4444` | 239, 68, 68 | Errors, destructive actions, urgent priority |

### Light Mode Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Light Background | `#FFFFFF` | 255, 255, 255 | Primary background |
| Light Surface | `#F4F4F5` | 244, 244, 245 | Card/surface background |
| Light Border | `#E4E4E7` | 228, 228, 231 | Borders, dividers |
| Light Text Primary | `#09090B` | 9, 9, 11 | Primary text |
| Light Text Secondary | `#71717A` | 113, 113, 122 | Secondary text |

### Brand Gradient: "Jet Fuel"

```css
background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
```

Used for: hero sections, CTAs, branded highlights, OG images, loading animations.

---

## Typography

| Role | Font | Weight | Usage |
|------|------|--------|-------|
| Display / Headings | Space Grotesk | 600-700 | Page titles, hero text, branded headings |
| Body / UI | Inter | 400-600 | All body text, labels, inputs, buttons |
| Monospace / Code | JetBrains Mono | 400 | Code blocks, technical references |

**Font Loading:** Google Fonts (Space Grotesk, Inter) or self-hosted for privacy.

---

## Iconography

**Primary Icon Set:** Lucide React (unchanged — not branded)
**Custom Icons:** Replace all 91 Plane custom SVGs with Jet-branded equivalents using the angular/chevron design language of the logo mark.

**Icon Style:**
- Geometric, angular lines (matching logo)
- 1.5px stroke weight
- Rounded line caps only at endpoints
- Consistent 24x24 viewBox

---

## Illustration Style: Technical Blueprint

**Concept:** Illustrations use a "technical blueprint" aesthetic — clean geometric lines on dark backgrounds (or light blueprint blue on white for light mode). Conveys precision, engineering, speed.

**Properties:**
- Line-art style, minimal fills
- Primary color: Jet Blue (#3B82F6) lines on dark backgrounds
- Light mode alternative: Dark lines on light blue (#EFF6FF) background
- Motion lines and speed trails for dynamic illustrations
- Grid/dot pattern backgrounds for technical feel

**Applications:**
- Empty state illustrations (no issues, no projects, etc.)
- Onboarding flow visuals
- Auth screen backgrounds
- Error page illustrations
- OG/social sharing images

---

## Favicon & App Icons

**Sizes Required:**
| Size | Format | Usage |
|------|--------|-------|
| 16x16 | PNG/ICO | Browser tab favicon |
| 32x32 | PNG/ICO | Browser tab favicon (retina) |
| 48x48 | PNG | Windows taskbar |
| 72x72 | PNG | PWA icon |
| 96x96 | PNG | PWA icon |
| 128x128 | PNG | Chrome Web Store |
| 144x144 | PNG | PWA icon (MS) |
| 192x192 | PNG | PWA icon (Android) |
| 384x384 | PNG | PWA splash |
| 512x512 | PNG | PWA splash (large) |
| SVG | SVG | Scalable vector source |

**Colors:** Jet Blue (#3B82F6) mark on transparent background. Alternate: white mark on Jet Black (#09090B) background.

---

## Loading Animation

**Concept:** "Jet Trail" — the chevron "J" mark traces a curved arc path, leaving a fading gradient trail (Jet Fuel gradient). Smooth, 1.5s loop.

**Fallback:** CSS-only circular spinner using Jet Blue accent color.

---

## Brand Voice

| Context | Tone | Example |
|---------|------|---------|
| Tagline | Confident, concise | "Ship faster with Jet" |
| Onboarding | Welcoming, clear | "Welcome to Jet. Let's set up your workspace." |
| Empty states | Calm, encouraging | "Clear skies. Create your first issue to get started." |
| Errors | Honest, helpful | "Something went wrong. Please try again or contact support." |
| Loading | Brief | (No text — animation only) |
| Success | Minimal | "Done." / "Saved." / "Created." |

**Voice Rules:**
- No aviation puns in UI (keep it professional)
- Short, direct sentences
- Action-oriented CTAs
- Aviation metaphors reserved for marketing/README only

---

## Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| npm packages | `@jet/` scope | `@jet/ui`, `@jet/editor-core` |
| Python module | `jet` | `jet.settings`, `jet.db.models` |
| Docker images | `jet-` prefix | `jet-frontend`, `jet-backend` |
| Docker services | `jet-` prefix | `jet-db`, `jet-redis`, `jet-minio` |
| Email sender | Jet PM | `Team Jet <team@jetpm.app>` |
| Default admin | - | `admin@jetpm.app` |
| CSS variables | `--color-` (unchanged) | Not brand-prefixed |
| Environment vars | No prefix change | Keep generic names |

---

## Application to Existing Assets

### Files to Replace

| Current Path | New Content |
|-------------|-------------|
| `web/public/logos/` | New Jet logo (SVG + PNG variants) |
| `web/public/favicon/` | New Jet favicon (all sizes) |
| `web/public/empty-state/` | New blueprint-style empty state illustrations |
| `web/public/onboarding/` | New onboarding flow images |
| `web/public/auth/` | New auth screen background/logo |
| `web/public/theme-mode/` | Updated theme preview images |
| `space/public/` | Mirror of web assets for Space app |
| `web/manifest.json` | Updated name, icons, theme_color |

### CSS Variable Mapping

```css
/* Dark mode (default for Jet Black aesthetic) */
:root {
  --color-primary-100: #3B82F6;  /* Jet Blue */
  --color-background-100: #09090B; /* Jet Black */
  --color-background-90: #18181B;  /* Jet Dark */
  --color-background-80: #27272A;  /* Jet Gray */
  --color-text-100: #FAFAFA;      /* Jet White */
  --color-text-200: #A1A1AA;      /* Jet Silver */
  --color-border-100: #27272A;    /* Jet Gray */
  --color-border-200: #3F3F46;    /* Jet Steel */
}

/* Light mode */
[data-theme="light"] {
  --color-background-100: #FFFFFF;
  --color-background-90: #F4F4F5;
  --color-background-80: #E4E4E7;
  --color-text-100: #09090B;
  --color-text-200: #71717A;
  --color-border-100: #E4E4E7;
}
```
