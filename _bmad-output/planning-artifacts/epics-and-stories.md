# Epics and Stories — Jet Rebrand

**Author:** Franc
**Date:** 2026-03-18
**Version:** 1.0
**Status:** Complete
**Source PRD:** prd.md v1.0

---

## Epic Overview

| Epic | Phase | Title | Stories | Effort | Dependencies |
|------|-------|-------|---------|--------|--------------|
| Epic 0 | Phase 0 | Design Assets | 7 | M-L | None |
| Epic 1 | Phase 1 | Backend Rename | 8 | L-XL | E0 (logo for emails) |
| Epic 2 | Phase 2 | Frontend Rename | 9 | L-XL | E0 (all visual assets) |
| Epic 3 | Phase 3 | Infrastructure | 7 | M-L | E1, E2 |
| Epic 4 | Phase 4 | External Integrations | 5 | M | E3 |
| Epic 5 | Phase 5 | Documentation | 4 | S-M | E1, E2, E3, E4 |
| Epic 6 | Phase 6 | Verification & QA | 6 | M-L | All prior epics |
| **Total** | | | **46** | | |

### Dependency Graph

```
E0 (Design Assets)
 ├──> E1 (Backend Rename)
 ├──> E2 (Frontend Rename)
 │     └──> E3 (Infrastructure)
 │           └──> E4 (Integrations)
 │                 └──> E5 (Documentation)
 │                       └──> E6 (Verification)
 └──────────────────────────────> E6 (Verification)
```

### FR Traceability Matrix

| FR ID | Story ID(s) |
|-------|-------------|
| FR-ASSET-1 | E0-S1 |
| FR-ASSET-2 | E0-S2 |
| FR-ASSET-3 | E0-S3 |
| FR-ASSET-4 | E0-S4 |
| FR-ASSET-5 | E0-S5 |
| FR-ASSET-6 | E0-S6 |
| FR-ASSET-7 | E0-S7 |
| FR-BACKEND-1 | E1-S1 |
| FR-BACKEND-2 | E1-S2 |
| FR-BACKEND-3 | E1-S3 |
| FR-BACKEND-4 | E1-S3 |
| FR-BACKEND-5 | E1-S3 |
| FR-BACKEND-6 | E1-S3 |
| FR-BACKEND-7 | E1-S4 |
| FR-BACKEND-8 | E1-S5 |
| FR-BACKEND-9 | E1-S6 |
| FR-BACKEND-10 | E1-S7 |
| FR-BACKEND-11 | E1-S3 |
| FR-BACKEND-12 | E1-S3 |
| FR-FRONTEND-1 | E2-S1 |
| FR-FRONTEND-2 | E2-S2, E2-S3 |
| FR-FRONTEND-3 | E2-S4 |
| FR-FRONTEND-4 | E2-S4 |
| FR-FRONTEND-5 | E2-S5 |
| FR-FRONTEND-6 | E2-S6 |
| FR-FRONTEND-7 | E2-S7 |
| FR-FRONTEND-8 | E2-S5 |
| FR-FRONTEND-9 | E2-S3 |
| FR-FRONTEND-10 | E2-S3 |
| FR-FRONTEND-11 | E2-S8 |
| FR-INFRA-1 | E3-S1 |
| FR-INFRA-2 | E3-S2 |
| FR-INFRA-3 | E3-S3 |
| FR-INFRA-4 | E3-S4 |
| FR-INFRA-5 | E3-S5 |
| FR-INFRA-6 | E3-S3 |
| FR-INFRA-7 | E3-S6 |
| FR-INFRA-8 | E3-S7 |
| FR-INTEGRATE-1 | E4-S1 |
| FR-INTEGRATE-2 | E4-S1 |
| FR-INTEGRATE-3 | E4-S2 |
| FR-INTEGRATE-4 | E4-S3 |
| FR-INTEGRATE-5 | E4-S4 |
| FR-INTEGRATE-6 | E4-S5 |
| FR-INTEGRATE-7 | E4-S5 |
| FR-DOCS-1 | E5-S1 |
| FR-DOCS-2 | E5-S2 |
| FR-DOCS-3 | E5-S3 |
| FR-DOCS-4 | E5-S2 |
| FR-DOCS-5 | E5-S4 |
| FR-VERIFY-1 | E6-S1 |
| FR-VERIFY-2 | E6-S2 |
| FR-VERIFY-3 | E6-S3 |
| FR-VERIFY-4 | E6-S4 |
| FR-VERIFY-5 | E6-S5 |
| FR-VERIFY-6 | E6-S5 |
| FR-VERIFY-7 | E6-S6 |

---

## Epic 0: Design Assets (Phase 0)

**Goal:** Create all visual assets needed before code changes begin. Every downstream epic depends on these assets being ready.
**Dependencies:** None
**Estimated Total Effort:** 5-7 days

---

### E0-S1: Create Chevron "J" Logo Mark SVG

**Description:**
As a designer, I want to create the Chevron "J" logo mark as an SVG vector source, so that the Jet brand has a distinctive, scalable mark that works from 16px favicon to full display.

**Acceptance Criteria:**
- [ ] SVG vector source file created with angular/geometric "J" constructed from chevron shapes
- [ ] Mark conveys speed, precision, and forward momentum through negative-space arrow
- [ ] Single-color mark works in mono (black), primary (Jet Blue #3B82F6), and inverted (white on dark) variants
- [ ] Three variants produced: icon only, wordmark ("Jet" in Space Grotesk Bold + mark), and horizontal lockup (icon + wordmark)
- [ ] Mark is visually recognizable and legible at 16x16px
- [ ] No curves — angular/geometric construction only
- [ ] SVG is optimized (no unnecessary paths, minimal file size)

**Effort:** M (1-2 days)
**Dependencies:** None
**Covers:** FR-ASSET-1

---

### E0-S2: Generate Favicon Set (All Sizes)

**Description:**
As a developer, I want a complete favicon set exported in all required sizes, so that the Jet brand appears correctly in browser tabs, PWA installs, and operating system taskbars on every platform.

**Acceptance Criteria:**
- [ ] PNG exports at all required sizes: 16, 32, 48, 72, 96, 128, 144, 192, 384, 512px
- [ ] ICO file created containing 16x16 and 32x32 variants
- [ ] SVG favicon source included for scalable use
- [ ] Chevron "J" in Jet Blue (#3B82F6) on transparent background
- [ ] Alternate set: white mark on Jet Black (#09090B) background
- [ ] All PNGs optimized (compressed, no unnecessary metadata)
- [ ] Files named and organized to match existing `web/public/favicon/` structure

**Effort:** S (< 1 day)
**Dependencies:** E0-S1
**Covers:** FR-ASSET-2

---

### E0-S3: Create OG Social Preview Image

**Description:**
As a marketing stakeholder, I want an OG social preview image with Jet branding, so that links shared on Slack, Twitter, LinkedIn, and other platforms display a professional, branded card.

**Acceptance Criteria:**
- [ ] Image dimensions: 1200x630px
- [ ] Background uses Jet Fuel gradient (linear-gradient 135deg, #3B82F6 to #06B6D4)
- [ ] Chevron "J" logo mark and "Jet" wordmark prominently displayed
- [ ] Tagline "Ship faster with Jet" included
- [ ] Image exported as optimized PNG
- [ ] Separate variants for web app and Space app (if distinct messaging needed)

**Effort:** S (< 1 day)
**Dependencies:** E0-S1
**Covers:** FR-ASSET-3

---

### E0-S4: Create Auth Screen Background Image

**Description:**
As a user, I want to see a distinctive Jet-branded background on the sign-in and sign-up screens, so that my first visual impression establishes the Jet identity.

**Acceptance Criteria:**
- [ ] Dark Jet Black (#09090B) base background
- [ ] Subtle grid/dot pattern overlay for technical feel
- [ ] Optional Jet Fuel gradient accent elements
- [ ] Image works well behind white/light auth form panels
- [ ] Exported as optimized PNG or SVG pattern
- [ ] Responsive: works at common screen widths (1024px to 2560px)

**Effort:** S (< 1 day)
**Dependencies:** E0-S1
**Covers:** FR-ASSET-4

---

### E0-S5: Create Empty State Illustrations (Blueprint Style)

**Description:**
As a user, I want to see visually appealing, on-brand illustrations when pages have no content, so that the product feels polished and encourages me to take action.

**Acceptance Criteria:**
- [ ] Minimum 5 empty state illustrations created in Technical Blueprint style:
  - No issues / empty project
  - No cycles
  - No modules
  - No pages
  - No notifications / empty inbox
- [ ] Line-art style, minimal fills, geometric construction
- [ ] Dark mode variant: Jet Blue (#3B82F6) lines on transparent/dark background
- [ ] Light mode variant: dark lines on light blue (#EFF6FF) background
- [ ] Motion lines and speed trails included for dynamic feel
- [ ] Each illustration works at the existing empty state container sizes
- [ ] Exported as optimized SVG or PNG

**Effort:** L (2-3 days)
**Dependencies:** E0-S1
**Covers:** FR-ASSET-5

---

### E0-S6: Create Onboarding Step Images

**Description:**
As a new user, I want to see clear, branded visuals during the onboarding flow, so that I feel welcomed and guided through workspace setup.

**Acceptance Criteria:**
- [ ] 3-4 onboarding step visuals created matching existing flow steps
- [ ] Technical Blueprint illustration style consistent with E0-S5
- [ ] Images communicate workspace setup, project creation, and team invitation concepts
- [ ] Work at existing onboarding image container dimensions
- [ ] Consistent with Jet Black color palette and brand voice
- [ ] Exported as optimized PNG or SVG

**Effort:** M (1-2 days)
**Dependencies:** E0-S1, E0-S5 (style consistency)
**Covers:** FR-ASSET-6

---

### E0-S7: Create Email Header Logo

**Description:**
As a user receiving emails from Jet, I want to see the Jet logo rendered correctly in the email header, so that the email feels trustworthy and branded.

**Acceptance Criteria:**
- [ ] Email-safe PNG logo created (email clients do not support SVG)
- [ ] Horizontal lockup version (icon + "Jet" wordmark)
- [ ] Max width ~200px for email header context
- [ ] Works on both white and dark email backgrounds
- [ ] Retina-ready (2x resolution export)
- [ ] File size under 50KB for email deliverability

**Effort:** S (< 1 day)
**Dependencies:** E0-S1
**Covers:** FR-ASSET-7

---

## Epic 1: Backend Rename (Phase 1)

**Goal:** Rename all backend Python modules, Django configuration, and server entry points from `plane` to `jet`. After this epic, the API server builds and runs with all `jet.*` module paths.
**Dependencies:** Epic 0 (E0-S7 needed for email template logos)
**Estimated Total Effort:** 7-10 days

---

### E1-S1: Rename `apiserver/plane/` Directory to `apiserver/jet/`

**Description:**
As a developer, I want the Python module directory renamed from `plane/` to `jet/`, so that the codebase's module hierarchy reflects the Jet brand identity.

**Acceptance Criteria:**
- [ ] `apiserver/plane/` directory renamed to `apiserver/jet/` via `git mv`
- [ ] All subdirectories preserved: `db/`, `api/`, `bgtasks/`, `settings/`, `utils/`, `middleware/`, `tests/`
- [ ] All 46+ migration files relocated under `apiserver/jet/db/migrations/`
- [ ] `manage.py` updated: `DJANGO_SETTINGS_MODULE` default changed from `plane.settings.*` to `jet.settings.*`
- [ ] No files left in an `apiserver/plane/` directory
- [ ] Rename is done as a single `git mv` operation for clean blame history (NFR-MAINT-1)

**Effort:** S (< 1 day)
**Dependencies:** None (can start in parallel with E0)
**Covers:** FR-BACKEND-1

---

### E1-S2: Update All Python Imports (`plane.*` to `jet.*`)

**Description:**
As a developer, I want all Python import statements updated from `plane.*` to `jet.*`, so that the application resolves modules correctly after the directory rename.

**Acceptance Criteria:**
- [ ] All `from plane.` imports updated to `from jet.` across ~225 Python files
- [ ] All `import plane.` statements updated to `import jet.`
- [ ] All string references to `plane.` in Python files (e.g., `"plane.db.models"` in settings INSTALLED_APPS) updated to `jet.`
- [ ] Automated `sed` script used for bulk replacement, followed by manual review
- [ ] No remaining `from plane.` or `import plane.` in any `.py` file under `apiserver/`
- [ ] `python manage.py check` passes without import errors

**Effort:** M (1-2 days)
**Dependencies:** E1-S1
**Covers:** FR-BACKEND-2

---

### E1-S3: Update Django Settings, WSGI, ASGI, Celery, and Server Config

**Description:**
As a developer, I want all Django entry points and server configuration files updated to reference `jet.*` module paths, so that the application boots correctly in all environments (dev, production, self-hosted).

**Acceptance Criteria:**
- [ ] All 6 settings files updated: `DJANGO_SETTINGS_MODULE` references `jet.settings.*` where applicable
- [ ] `common.py`: `ROOT_URLCONF` set to `jet.api.urls`; `WSGI_APPLICATION` set to `jet.wsgi.application`; all `INSTALLED_APPS` entries referencing `plane.` updated to `jet.`
- [ ] `wsgi.py`: `DJANGO_SETTINGS_MODULE` default updated; module exposes `jet.wsgi:application`
- [ ] `asgi.py`: `DJANGO_SETTINGS_MODULE` default updated; module exposes `jet.asgi:application`
- [ ] `celery.py`: app name updated to `"jet"`; `autodiscover_tasks` discovers from `jet.*` modules
- [ ] `gunicorn.config.py`: bind, module path, and log references updated
- [ ] `Procfile`: all process commands reference `jet.*` module paths (WSGI, Celery worker, Celery beat)
- [ ] Application starts successfully with `python manage.py runserver`
- [ ] Celery worker starts and discovers all tasks from `jet.bgtasks`

**Effort:** M (1-2 days)
**Dependencies:** E1-S1, E1-S2
**Covers:** FR-BACKEND-3, FR-BACKEND-4, FR-BACKEND-5, FR-BACKEND-6, FR-BACKEND-11, FR-BACKEND-12

---

### E1-S4: Create Django Content Type Data Migration

**Description:**
As a developer, I want a Django data migration that updates all `django_content_type` records from `app_label='plane'` variants to `app_label='jet'` variants, so that existing database records and permissions continue to function after the module rename.

**Acceptance Criteria:**
- [ ] New migration file created in `apiserver/jet/db/migrations/`
- [ ] Migration updates `django_content_type` table: all rows where `app_label` contains `plane` are updated to the `jet` equivalent
- [ ] Migration is reversible (includes a reverse function to restore `plane` app labels)
- [ ] Migration handles potential conflicts (no duplicate content type entries)
- [ ] Migration tested on a copy of the database before applying to development
- [ ] `python manage.py migrate` completes successfully
- [ ] Existing model instances remain accessible through Django ORM after migration

**Effort:** M (1-2 days)
**Dependencies:** E1-S1, E1-S2
**Covers:** FR-BACKEND-7

---

### E1-S5: Rebrand Email Templates

**Description:**
As a user receiving emails from Jet, I want all email communications to display Jet branding (logo, name, contact info), so that the experience is consistent with the in-app brand.

**Acceptance Criteria:**
- [ ] All ~10 email templates in `apiserver/templates/emails/` updated
- [ ] Plane logo replaced with Jet email header logo (from E0-S7)
- [ ] All text references to "Plane" replaced with "Jet"
- [ ] Sender identity updated: display name "Jet" or "Team Jet"
- [ ] Footer links and contact information updated to Jet equivalents
- [ ] Email subject lines reference "Jet" (invitation, export, password reset, magic link)
- [ ] Templates render correctly in Gmail, Outlook, and Apple Mail (manual spot check)

**Effort:** M (1-2 days)
**Dependencies:** E0-S7, E1-S1
**Covers:** FR-BACKEND-8

---

### E1-S6: Update Slack Signal and Notification Text

**Description:**
As a user receiving Slack notifications from the Jet integration, I want the messages to reference "Jet" rather than "Plane", so that the integration feels native to the Jet product.

**Acceptance Criteria:**
- [ ] User model Slack notification signal updated: message text references "Jet"
- [ ] Any hardcoded "Plane" strings in `bgtasks/` notification tasks updated to "Jet"
- [ ] Slack bot message formatting (if any) references Jet branding
- [ ] Log messages in notification tasks reference `jet` module paths

**Effort:** S (< 1 day)
**Dependencies:** E1-S2
**Covers:** FR-BACKEND-9

---

### E1-S7: Update Default Settings Values and Constants

**Description:**
As a developer deploying Jet, I want all default configuration values (email addresses, URLs, app names) to reflect the Jet brand, so that fresh installations are correctly branded out of the box.

**Acceptance Criteria:**
- [ ] `DEFAULT_EMAIL` changed from `captain@plane.so` to `admin@jetpm.app` (or equivalent)
- [ ] `EMAIL_FROM` default updated to Jet domain
- [ ] `WEB_URL` default references updated
- [ ] Django admin site header updated to "Jet Administration"
- [ ] Django admin site title updated to "Jet Admin"
- [ ] Any print statements or logging references to "Plane" updated to "Jet"
- [ ] API token label generation references Jet (if applicable)
- [ ] Management command help text references Jet

**Effort:** S (< 1 day)
**Dependencies:** E1-S2
**Covers:** FR-BACKEND-10

---

### E1-S8: Update Backend Test Suite Imports and Assertions

**Description:**
As a developer, I want the backend test suite to pass after the rename, so that code quality is maintained and regressions are caught.

**Acceptance Criteria:**
- [ ] All test file imports updated from `plane.*` to `jet.*` across ~10 test files
- [ ] Any test assertions comparing string values containing "Plane" updated to "Jet"
- [ ] Test settings file (`test.py`) references `jet.settings.test`
- [ ] `python manage.py test` executes and all existing tests pass
- [ ] No import errors or module-not-found exceptions during test discovery

**Effort:** S (< 1 day)
**Dependencies:** E1-S2, E1-S3
**Covers:** FR-BACKEND-2 (test subset)

---

## Epic 2: Frontend Rename (Phase 2)

**Goal:** Rename all frontend npm packages, update every user-facing string, replace all visual assets, and apply the Jet color palette. After this epic, both web and Space apps build and render with full Jet branding.
**Dependencies:** Epic 0 (all visual assets must be ready)
**Estimated Total Effort:** 8-12 days

---

### E2-S1: Rename npm Packages from `@plane/*` to `@jet/*`

**Description:**
As a developer, I want all npm package names updated from `@plane/*` to `@jet/*`, so that the monorepo's package identity reflects the Jet brand and internal imports resolve correctly.

**Acceptance Criteria:**
- [ ] All 7 `package.json` files updated: `@plane/ui` to `@jet/ui`, `@plane/editor-core` to `@jet/editor-core`, `@plane/rich-text-editor` to `@jet/rich-text-editor`, `@plane/lite-text-editor` to `@jet/lite-text-editor`, `@plane/eslint-config-custom` to `@jet/eslint-config-custom`, `@plane/tailwind-config-custom` to `@jet/tailwind-config-custom`, `@plane/tsconfig` to `@jet/tsconfig`
- [ ] Root `package.json` workspace references updated if applicable
- [ ] All `import ... from "@plane/..."` statements across web, space, and packages updated to `"@jet/..."`
- [ ] `turbo.json` references updated if package names are used
- [ ] `tsconfig.json` path aliases updated in web, space, and package configs
- [ ] `yarn install` completes without errors after rename
- [ ] No remaining `@plane/` references in any `package.json`, `tsconfig.json`, or import statement

**Effort:** L (2-3 days)
**Dependencies:** None (can start in parallel with E1)
**Covers:** FR-FRONTEND-1

---

### E2-S2: Replace "Plane" String Literals in Web App

**Description:**
As a user, I want every visible text in the web dashboard to say "Jet" instead of "Plane", so that the product identity is consistent throughout my experience.

**Acceptance Criteria:**
- [ ] All user-facing string literals containing "Plane" in `web/` updated to "Jet" (~990 TSX/TS files scanned)
- [ ] Toast messages, modal titles, tooltips, and button labels updated
- [ ] Error messages and fallback text updated
- [ ] 404 and error pages reference Jet
- [ ] Django admin references in frontend (if any) updated
- [ ] `grep -rn "Plane\|plane" web/components/ web/pages/ web/layouts/ web/constants/ web/helpers/` returns zero results (excluding node_modules, comments about the migration itself, and variable names unrelated to the brand)
- [ ] Case-sensitive replacements applied correctly: "Plane" to "Jet", "plane" to "jet" (only in brand-name contexts, not in generic English words like "airplane" or "plane" meaning geometric plane)

**Effort:** L (2-3 days)
**Dependencies:** E2-S1
**Covers:** FR-FRONTEND-2

---

### E2-S3: Replace "Plane" String Literals in Space App and Update UI Chrome

**Description:**
As an external viewer on a public board, I want to see Jet branding in the Space app header, footer, and all UI elements, so that the shared board experience is consistently Jet-branded.

**Acceptance Criteria:**
- [ ] All string literals containing "Plane" in `space/` updated to "Jet"
- [ ] Space app header displays Jet logo
- [ ] Footer text updated to "Powered by Jet" (or equivalent)
- [ ] Browser tab title format: "Jet - [Project Name]"
- [ ] Command palette (if present in Space) placeholder text updated
- [ ] Login/auth screens in Space reference Jet
- [ ] `grep -rn "Plane\|plane" space/components/ space/pages/ space/layouts/ space/constants/` returns zero brand-name results

**Effort:** M (1-2 days)
**Dependencies:** E2-S1
**Covers:** FR-FRONTEND-2, FR-FRONTEND-9, FR-FRONTEND-10

---

### E2-S4: Update SEO Metadata, Manifest, and OG Tags

**Description:**
As a user or external visitor, I want browser tabs, PWA installs, and social previews to display Jet branding, so that the product identity is correct in every context outside the app itself.

**Acceptance Criteria:**
- [ ] SEO constants file updated: site title, description, keywords reference "Jet"
- [ ] `web/manifest.json` updated: `name` = "Jet", `short_name` = "Jet", `description` references Jet, `theme_color` = "#09090B" (Jet Black), icon paths point to new favicons
- [ ] `space/manifest.json` (or equivalent) updated with same Jet values
- [ ] `_document.tsx` in web: meta tags (description, author, theme-color) reference Jet; OG tags (`og:title`, `og:description`, `og:image`) reference Jet and point to new OG image
- [ ] `_document.tsx` in space: same OG and meta tag updates
- [ ] Apple touch icon references point to new Jet favicon
- [ ] PWA install prompt shows "Jet" with correct theme color and icon

**Effort:** M (1-2 days)
**Dependencies:** E0-S2, E0-S3
**Covers:** FR-FRONTEND-3, FR-FRONTEND-4

---

### E2-S5: Update Next.js Config and Analytics References

**Description:**
As a developer, I want `next.config.js` and analytics integrations updated to reference Jet domains and identifiers, so that image loading, error tracking, and analytics work correctly under the new brand.

**Acceptance Criteria:**
- [ ] `web/next.config.js`: image domains updated — remove Plane S3/CDN references, add Jet equivalents (or keep generic)
- [ ] `space/next.config.js`: same image domain updates
- [ ] Sentry DSN references updated or parameterized for Jet project
- [ ] Analytics script references (PostHog, Plausible, Clarity, Jitsu) updated with Jet project identifiers (or confirmed as environment-variable-driven and not hardcoded)
- [ ] `_app.tsx` provider wrappers reference Jet where applicable
- [ ] No hardcoded Plane domain names remain in config files

**Effort:** S (< 1 day)
**Dependencies:** E2-S1
**Covers:** FR-FRONTEND-5, FR-FRONTEND-8

---

### E2-S6: Replace All Visual Assets (Logos, Favicons, Images)

**Description:**
As a user, I want to see the new Jet logo, favicon, empty state illustrations, onboarding images, and auth backgrounds throughout the application, so that the visual experience is fully Jet-branded.

**Acceptance Criteria:**
- [ ] `web/public/logos/` — all Plane logo files replaced with Jet logo variants (SVG + PNG, dark + light)
- [ ] `web/public/favicon/` — all favicon files replaced with Jet favicon set from E0-S2
- [ ] `web/public/empty-state/` — all empty state images replaced with Blueprint-style illustrations from E0-S5
- [ ] `web/public/onboarding/` — onboarding images replaced with Jet visuals from E0-S6
- [ ] `web/public/auth/` — auth background image replaced with Jet version from E0-S4
- [ ] `web/public/theme-mode/` — theme preview thumbnails updated if they contain Plane branding
- [ ] `space/public/` — all equivalent Space assets mirrored from web updates
- [ ] All image file references in code (import paths, `src` attributes) verified to match new file names
- [ ] No Plane-branded image files remain in `public/` directories

**Effort:** M (1-2 days)
**Dependencies:** E0-S2, E0-S3, E0-S4, E0-S5, E0-S6
**Covers:** FR-FRONTEND-6

---

### E2-S7: Update CSS Variables and Default Theme to Jet Black Palette

**Description:**
As a user, I want the default color scheme to reflect the Jet Black palette, so that the product's visual identity matches the Jet brand from the first interaction.

**Acceptance Criteria:**
- [ ] `globals.css` (or equivalent) CSS custom properties updated to Jet Black palette defaults:
  - `--color-primary-100: #3B82F6` (Jet Blue)
  - `--color-background-100: #09090B` (Jet Black, dark mode)
  - `--color-background-90: #18181B` (Jet Dark)
  - `--color-text-100: #FAFAFA` (Jet White)
  - etc. per brand identity spec
- [ ] Light mode variables updated per brand identity light mode palette
- [ ] All 5 theme variants render correctly: dark, light, light-contrast, dark-contrast, custom
- [ ] Custom theme option continues to work (Jet colors are defaults, not forced overrides)
- [ ] Tailwind config updated if it contains hardcoded Plane colors
- [ ] No visual regression in existing UI layouts (text remains readable, borders visible, etc.)

**Effort:** M (1-2 days)
**Dependencies:** None
**Covers:** FR-FRONTEND-7

---

### E2-S8: Update Onboarding Tour and Welcome Copy

**Description:**
As a new user, I want the onboarding tour and welcome messages to reference Jet, so that my first experience with the product establishes the correct brand identity.

**Acceptance Criteria:**
- [ ] Onboarding flow welcome text: "Welcome to Jet. Let's set up your workspace."
- [ ] All onboarding step labels and descriptions reference Jet where applicable
- [ ] Workspace creation default text and examples reference Jet
- [ ] Sign-in page heading/subheading references Jet
- [ ] Sign-up page heading/subheading references Jet
- [ ] Magic link email request page references Jet
- [ ] Password reset flow references Jet
- [ ] Any interactive tour tooltips reference Jet product name

**Effort:** S (< 1 day)
**Dependencies:** E2-S2
**Covers:** FR-FRONTEND-11

---

### E2-S9: Update Custom SVG Icon Components (91 Icons)

**Description:**
As a user, I want custom icons throughout the app to follow the Jet angular/chevron design language, so that the icon set feels cohesive with the logo and brand identity.

**Acceptance Criteria:**
- [ ] All 91 custom SVG icon components in `web/components/icons/` audited
- [ ] Icons that contain "Plane" branding (logo marks, branded icons) redesigned in Jet angular/chevron style
- [ ] Generic icons (arrows, status indicators, layout icons) updated to match Jet icon style: geometric, angular lines, 1.5px stroke weight, 24x24 viewBox
- [ ] All icon component file names and export names updated if they reference "Plane"
- [ ] Icons render correctly at standard sizes (16px, 20px, 24px)
- [ ] No Plane-branded iconography remains

**Effort:** XL (3-5 days)
**Dependencies:** E0-S1 (design language reference)
**Covers:** FR-FRONTEND-6 (icon subset)

---

## Epic 3: Infrastructure (Phase 3)

**Goal:** Update all Docker, Nginx, CI/CD, and deployment configurations so that the infrastructure layer uses `jet-*` naming and references the correct `jet.*` module paths. After this epic, `docker compose up` starts all services with Jet identities.
**Dependencies:** Epic 1 (backend module paths), Epic 2 (frontend package names)
**Estimated Total Effort:** 5-7 days

---

### E3-S1: Update Dockerfiles (Root and API Server)

**Description:**
As a DevOps engineer, I want all Dockerfiles updated to reference `jet` module paths, user/group names, and build contexts, so that container images build correctly for the renamed codebase.

**Acceptance Criteria:**
- [ ] Root `Dockerfile` (multi-stage production build): all `plane` references in COPY paths, WORKDIR, RUN commands, and CMD/ENTRYPOINT updated to `jet`
- [ ] `apiserver/Dockerfile` (if separate): module paths, pip install paths, and CMD updated
- [ ] User/group names in Dockerfiles updated from `plane` to `jet` (if applicable)
- [ ] `nginx/Dockerfile`: any Plane references in labels or comments updated
- [ ] All Dockerfiles build successfully: `docker build -t jet-backend ./apiserver`, `docker build -t jet-frontend ./web`, etc.
- [ ] Built images start and respond to health checks

**Effort:** M (1-2 days)
**Dependencies:** E1-S3 (WSGI/ASGI paths finalized)
**Covers:** FR-INFRA-1

---

### E3-S2: Update Docker Compose Files (All 3 Variants)

**Description:**
As a developer or operator, I want all Docker Compose files to use `jet-*` service names, so that running `docker compose up` creates containers with Jet-branded identities.

**Acceptance Criteria:**
- [ ] `docker-compose.yml` (development): all service names changed from `plane-*` to `jet-*` (e.g., `plane-api` to `jet-api`, `plane-worker` to `jet-worker`, `plane-beat-worker` to `jet-beat-worker`, `plane-db` to `jet-db`, `plane-redis` to `jet-redis`, `plane-minio` to `jet-minio`)
- [ ] `docker-compose-local.yml` (local dev): same service name updates
- [ ] `deploy/selfhost/docker-compose.yml` (self-hosted production): same service name updates
- [ ] Image names updated to `jet-*` (e.g., `jet-frontend:latest`, `jet-backend:latest`, `jet-space:latest`, `jet-proxy:latest`)
- [ ] Network names updated from `plane-*` to `jet-*` (if named)
- [ ] Volume names updated from `plane-*` to `jet-*` (if named)
- [ ] Environment variables referencing `plane` module paths updated (e.g., `DJANGO_SETTINGS_MODULE=jet.settings.production`)
- [ ] `docker compose up -d` starts all services; `docker compose ps` shows all healthy

**Effort:** M (1-2 days)
**Dependencies:** E3-S1
**Covers:** FR-INFRA-2

---

### E3-S3: Update Nginx Config and Supervisor Config

**Description:**
As a DevOps engineer, I want the Nginx reverse proxy and process supervisor to reference Jet service names, so that HTTP routing and process management work correctly with the renamed Docker services.

**Acceptance Criteria:**
- [ ] `nginx/nginx.conf.template`: upstream block names updated from `plane-*` to `jet-*` (e.g., `upstream jet-api`, `upstream jet-web`, `upstream jet-space`)
- [ ] Proxy pass targets updated to match new upstream names
- [ ] Any server name or comment references to Plane updated
- [ ] Supervisor configuration (if present): process names updated from `plane-*` to `jet-*`
- [ ] Supervisor command paths reference `jet.*` module paths (Gunicorn, Celery)
- [ ] Nginx starts and correctly routes: `/` to web, `/api/` to API, `/spaces/` to Space, `/uploads/` to MinIO

**Effort:** S (< 1 day)
**Dependencies:** E3-S2
**Covers:** FR-INFRA-3, FR-INFRA-6

---

### E3-S4: Update GitHub Actions CI/CD Workflows

**Description:**
As a developer, I want CI/CD pipelines to build and publish Jet-branded Docker images, so that automated builds produce correctly named artifacts.

**Acceptance Criteria:**
- [ ] `build-test-pull-request.yml`: image names, build contexts, and any "Plane" references updated
- [ ] `create-sync-pr.yml`: repository references and labels updated to Jet
- [ ] `update-docker-images.yml`: Docker Hub image names updated to `jet-*`; repository references updated
- [ ] Any workflow environment variables referencing `plane` updated to `jet`
- [ ] Workflow YAML files pass validation (valid GitHub Actions syntax)
- [ ] No hardcoded `makeplane` or `plane` Docker Hub references remain (unless deliberately pointing to upstream)

**Effort:** M (1-2 days)
**Dependencies:** E3-S1, E3-S2
**Covers:** FR-INFRA-4

---

### E3-S5: Update Setup Script and Start Script

**Description:**
As a developer setting up a local environment, I want `setup.sh` to generate Jet-branded environment files, so that the out-of-box experience reflects the Jet identity.

**Acceptance Criteria:**
- [ ] `setup.sh`: all references to "Plane" in comments, echo statements, and generated defaults updated to "Jet"
- [ ] Generated `.env` files use Jet defaults (e.g., `admin@jetpm.app`, Jet-branded comments)
- [ ] `start.sh`: any Plane references in process start commands or log messages updated
- [ ] Scripts remain executable and function correctly on macOS and Linux
- [ ] Running `./setup.sh` produces `.env` files with zero "Plane" references

**Effort:** S (< 1 day)
**Dependencies:** E1-S7 (default values finalized)
**Covers:** FR-INFRA-5

---

### E3-S6: Update Heroku Configuration

**Description:**
As a developer deploying to Heroku, I want the Heroku app manifest and deployment config to reference Jet, so that Heroku deployments are correctly branded.

**Acceptance Criteria:**
- [ ] `app.json`: app name, description, and any "Plane" references updated to "Jet"
- [ ] `heroku.yml`: Docker image references updated to `jet-*`
- [ ] Environment variable defaults in Heroku config reference `jet.*` module paths
- [ ] Buildpack or addon references updated if they contain "Plane"

**Effort:** S (< 1 day)
**Dependencies:** E3-S1
**Covers:** FR-INFRA-7

---

### E3-S7: Update Environment Variable Templates

**Description:**
As a developer or operator, I want all `.env` template and example files to reference Jet, so that environment setup documentation and defaults are correctly branded.

**Acceptance Criteria:**
- [ ] All `.env.example`, `.env.template`, or equivalent files across the repo updated
- [ ] Comments explaining variables reference "Jet" not "Plane"
- [ ] Default values for URLs, email addresses, and app names use Jet equivalents
- [ ] `deploy/selfhost/variables.env` (or equivalent) updated
- [ ] `ENV_SETUP.md` references checked (covered in E5, but template files updated here)
- [ ] No "Plane" references remain in any environment template file

**Effort:** S (< 1 day)
**Dependencies:** E1-S7
**Covers:** FR-INFRA-8

---

## Epic 4: External Integrations (Phase 4)

**Goal:** Re-register all external service integrations under the Jet identity and update internal code that references these services. After this epic, all OAuth flows, bot integrations, and third-party services operate under the Jet brand.
**Dependencies:** Epic 3 (stable, buildable Jet codebase)
**Estimated Total Effort:** 3-5 days

---

### E4-S1: Register Google and GitHub OAuth Applications

**Description:**
As an admin, I want new OAuth applications registered with Google and GitHub under the Jet identity, so that users can authenticate via "Sign in with Google/GitHub" and see "Jet" as the requesting application.

**Acceptance Criteria:**
- [ ] New Google OAuth app registered at console.cloud.google.com with name "Jet"
- [ ] OAuth consent screen displays "Jet" branding (name, logo, privacy/terms URLs)
- [ ] Redirect URIs configured for Jet deployment domains
- [ ] New GitHub OAuth app registered at github.com/settings/applications with name "Jet"
- [ ] GitHub OAuth app icon set to Jet logo
- [ ] Client ID and Client Secret values documented for environment variable configuration
- [ ] Existing environment variable names (`GOOGLE_CLIENT_ID`, `GITHUB_CLIENT_ID`, etc.) confirmed — values change, keys stay the same
- [ ] OAuth sign-in flow tested end-to-end for both providers

**Effort:** M (1-2 days)
**Dependencies:** E0-S1 (logo for OAuth consent screens)
**Covers:** FR-INTEGRATE-1, FR-INTEGRATE-2

---

### E4-S2: Register GitHub App for Repository Sync

**Description:**
As an admin, I want a new GitHub App registered under the Jet identity, so that repository sync (issue linking, PR tracking) displays "Jet" as the integration partner.

**Acceptance Criteria:**
- [ ] New GitHub App registered with name "Jet" (or "Jet PM")
- [ ] App icon set to Jet logo
- [ ] Webhook URL configured for Jet API server
- [ ] Required permissions set: repository contents, issues, pull requests (matching existing Plane app permissions)
- [ ] Installation flow tested: user installs Jet GitHub App on a repository
- [ ] Webhook events received and processed correctly by `jet.bgtasks` handlers

**Effort:** M (1-2 days)
**Dependencies:** E3-S2 (Jet API server accessible)
**Covers:** FR-INTEGRATE-3

---

### E4-S3: Register Slack App/Bot

**Description:**
As an admin, I want a new Slack app registered as "Jet", so that Slack notifications and the slash command integration display Jet branding.

**Acceptance Criteria:**
- [ ] New Slack app created at api.slack.com with name "Jet"
- [ ] App icon set to Jet logo
- [ ] Bot user display name set to "Jet"
- [ ] Slash command (if present) updated to `/jet`
- [ ] OAuth redirect URIs configured for Jet deployment
- [ ] Event subscriptions pointed to Jet API webhook endpoint
- [ ] Slack bot token and signing secret documented for environment configuration
- [ ] Test: installing app in a Slack workspace shows "Jet" bot sending notifications

**Effort:** M (1-2 days)
**Dependencies:** E1-S6 (Slack notification code updated)
**Covers:** FR-INTEGRATE-4

---

### E4-S4: Update Sentry and Analytics Projects

**Description:**
As a developer, I want error tracking and analytics services to report under the "Jet" project name, so that monitoring dashboards are correctly branded and separated from any Plane telemetry.

**Acceptance Criteria:**
- [ ] Sentry project renamed or new project created with name "Jet"
- [ ] Sentry DSN updated in environment configuration
- [ ] Frontend Sentry SDK initialization references Jet project
- [ ] Backend Sentry SDK initialization references Jet project
- [ ] Analytics services (PostHog, Plausible, Clarity) — project names/IDs updated or confirmed as environment-variable-driven
- [ ] Unsplash API app re-registered under "Jet" name (or confirmed not hardcoded)
- [ ] Error reporting tested: a deliberate error appears in Jet Sentry project

**Effort:** S (< 1 day)
**Dependencies:** E2-S5 (analytics references in frontend)
**Covers:** FR-INTEGRATE-5

---

### E4-S5: Update CORS Origins and OpenAI Prompts

**Description:**
As a developer, I want CORS allowed origins to include Jet domains and OpenAI system prompts to reference Jet, so that API access control and AI features work correctly under the new brand.

**Acceptance Criteria:**
- [ ] CORS allowed origins in Django settings updated: Plane domains removed, Jet domains added
- [ ] Wildcard or environment-variable-driven CORS confirmed (if applicable)
- [ ] OpenAI system prompt text updated: any "Plane" context references changed to "Jet" (e.g., "You are a project management assistant for Jet...")
- [ ] GitHub release notes endpoint repository reference updated (if hardcoded)
- [ ] API responses tested from Jet domains: no CORS errors

**Effort:** S (< 1 day)
**Dependencies:** E1-S2 (backend code updated)
**Covers:** FR-INTEGRATE-6, FR-INTEGRATE-7

---

## Epic 5: Documentation (Phase 5)

**Goal:** Update all documentation files to reflect Jet branding. After this epic, every markdown file, template, and guide in the repository references Jet exclusively.
**Dependencies:** Epics 1-4 (all code changes finalized so docs reflect final state)
**Estimated Total Effort:** 3-5 days

---

### E5-S1: Rewrite README.md

**Description:**
As a developer discovering the project, I want the README to present Jet with its own identity, logo, description, and screenshots, so that the repository landing page establishes Jet as a distinct product.

**Acceptance Criteria:**
- [ ] README header displays Jet logo (horizontal lockup)
- [ ] Project name and description reference Jet throughout
- [ ] Tagline: "Ship faster with Jet" prominently displayed
- [ ] Feature list retained but all Plane references removed
- [ ] Screenshots updated to show Jet-branded UI (or marked as TODO with placeholder text)
- [ ] Quick start instructions reference `jet-*` Docker services and Jet URLs
- [ ] Badge URLs (CI status, license, etc.) updated to Jet repository
- [ ] Contributing, license, and community links updated
- [ ] No remaining references to "Plane" (except legal attribution if required by AGPL-3.0)

**Effort:** M (1-2 days)
**Dependencies:** E2-S6 (visual assets placed for screenshots)
**Covers:** FR-DOCS-1

---

### E5-S2: Update Contributing Guide, Env Setup, Code of Conduct, and License

**Description:**
As a contributor, I want the contributing guide and related documents to reference Jet, so that the development process documentation matches the product identity.

**Acceptance Criteria:**
- [ ] `CONTRIBUTING.md`: all "Plane" references replaced with "Jet"; setup commands reference `jet-*` services; PR guidelines reference Jet repo conventions
- [ ] `ENV_SETUP.md`: all environment variable descriptions reference Jet; example values use Jet defaults (`admin@jetpm.app`, etc.)
- [ ] `CODE_OF_CONDUCT.md`: project name updated to Jet; contact information updated
- [ ] `LICENSE.txt`: verified — AGPL-3.0 attribution checked; original Plane copyright retained if legally required; Jet copyright added for modifications
- [ ] No "Plane" brand references remain in any of these files (legal attribution excepted)

**Effort:** M (1-2 days)
**Dependencies:** E3-S7 (env template values finalized)
**Covers:** FR-DOCS-2, FR-DOCS-4

---

### E5-S3: Update GitHub Issue and PR Templates

**Description:**
As a contributor filing an issue or PR, I want the templates to reference Jet, so that community interactions are consistently branded.

**Acceptance Criteria:**
- [ ] All GitHub issue templates (bug report, feature request, general) in `.github/ISSUE_TEMPLATE/` updated
- [ ] Template headers, labels, and description text reference Jet
- [ ] PR template (if present) references Jet contribution guidelines
- [ ] Template YAML metadata (labels, assignees) verified for accuracy
- [ ] No "Plane" references remain in any template file

**Effort:** S (< 1 day)
**Dependencies:** None
**Covers:** FR-DOCS-3

---

### E5-S4: Regenerate Project Documentation

**Description:**
As a developer using AI-assisted tools, I want the project documentation in `docs/` to accurately reflect the Jet codebase, so that context files are current and useful.

**Acceptance Criteria:**
- [ ] All 16 documentation files in `docs/` regenerated to reflect the post-rebrand codebase state
- [ ] `docs/index.md` references Jet (not Plane) throughout
- [ ] `docs/source-tree-analysis.md` shows `jet/` directory structure
- [ ] Architecture docs reference `jet.*` module paths, `@jet/*` package names, `jet-*` Docker services
- [ ] API contracts and data model docs reference `jet.db.models`, `jet.api.views`, etc.
- [ ] Development and deployment guides reference Jet setup steps
- [ ] No "Plane" references remain in regenerated docs (except historical context if appropriate)

**Effort:** M (1-2 days)
**Dependencies:** E1, E2, E3 (codebase in final state)
**Covers:** FR-DOCS-5

---

## Epic 6: Verification & QA (Phase 6)

**Goal:** Systematically verify that the rebrand is complete, all builds pass, all tests pass, and no "Plane" references remain anywhere in the codebase. This is the gate before merge.
**Dependencies:** All prior epics (E0-E5)
**Estimated Total Effort:** 4-6 days

---

### E6-S1: Automated Grep Audit — Zero "Plane" References

**Description:**
As a developer, I want an automated audit confirming that zero references to "Plane" remain in the codebase, so that the rebrand is provably complete.

**Acceptance Criteria:**
- [ ] Run comprehensive grep: `grep -ri "plane" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.md" --include="*.html" --include="*.css" --include="*.conf" --include="*.env" --include="*.txt" . | grep -v node_modules | grep -v .git | grep -v _bmad`
- [ ] Result: 0 matches (excluding legally required AGPL-3.0 attribution in LICENSE)
- [ ] Case-insensitive search covers: "Plane", "plane", "PLANE"
- [ ] Image file names checked: no files named `*plane*` in `public/` directories
- [ ] Docker image tags checked: no `plane-*` references in any config
- [ ] Environment template files checked: no `plane` in defaults or comments
- [ ] Any remaining references documented with justification (e.g., license attribution) or fixed
- [ ] CI grep check script created for future regression prevention (NFR-MAINT-2)

**Effort:** M (1-2 days)
**Dependencies:** E5 (all changes complete)
**Covers:** FR-VERIFY-1

---

### E6-S2: Backend Test Suite Pass

**Description:**
As a developer, I want the full backend test suite to pass, so that the rename has not introduced any functional regressions.

**Acceptance Criteria:**
- [ ] `cd apiserver && python manage.py test` executes successfully
- [ ] All existing tests pass — zero failures, zero errors
- [ ] No import errors or module-not-found exceptions
- [ ] Django system check passes: `python manage.py check`
- [ ] Django migration check passes: `python manage.py migrate --check` (no unapplied migrations)
- [ ] Celery task discovery succeeds: all tasks in `jet.bgtasks` found

**Effort:** S (< 1 day)
**Dependencies:** E1-S8, E1-S4
**Covers:** FR-VERIFY-2

---

### E6-S3: Frontend Build Verification (Web + Space)

**Description:**
As a developer, I want both frontend applications to build without errors, so that the package rename and string replacements have not broken any imports or type checks.

**Acceptance Criteria:**
- [ ] `yarn build --filter=web` completes successfully with exit code 0
- [ ] `yarn build --filter=space` completes successfully with exit code 0
- [ ] No TypeScript type errors related to renamed imports
- [ ] No missing module errors for `@jet/*` packages
- [ ] Build output size is comparable to pre-rebrand (no unexpected bloat)
- [ ] `yarn lint` passes (if linting is configured)

**Effort:** S (< 1 day)
**Dependencies:** E2-S1, E2-S2, E2-S3
**Covers:** FR-VERIFY-3

---

### E6-S4: Docker Build and Compose Verification

**Description:**
As a DevOps engineer, I want all Docker images to build and all services to start healthily, so that the infrastructure rename is confirmed working.

**Acceptance Criteria:**
- [ ] `docker compose build` completes successfully — all images built
- [ ] `docker compose up -d` starts all services
- [ ] `docker compose ps` shows all services as "healthy" or "running"
- [ ] Services respond on expected ports: web (3000), API (8000), Space (4000)
- [ ] Nginx proxy correctly routes: `/` to web, `/api/` to API, `/spaces/` to Space
- [ ] Inter-service communication verified: web can reach API, worker can reach Redis and DB
- [ ] `docker compose logs` shows `jet.*` module paths (no `plane.*` in startup logs)
- [ ] `docker compose down && docker compose up -d` (clean restart) works

**Effort:** M (1-2 days)
**Dependencies:** E3-S1, E3-S2, E3-S3
**Covers:** FR-VERIFY-4

---

### E6-S5: Manual UI Walkthrough and Email Verification

**Description:**
As a QA tester, I want to manually walk through every major screen in the application and verify email branding, so that no visual "Plane" artifacts remain for end users.

**Acceptance Criteria:**
- [ ] **Auth screens:** Sign-in, sign-up, magic link, password reset — all show Jet logo and branding
- [ ] **Onboarding:** Welcome text says "Jet"; step images are Jet-branded
- [ ] **Dashboard:** Sidebar logo is Jet; browser tab shows "Jet - Dashboard"
- [ ] **Project screens:** Issues, cycles, modules, views, pages, inbox — no "Plane" text visible
- [ ] **Settings:** Workspace and project settings pages reference Jet
- [ ] **Command palette:** Cmd+K shows Jet-branded placeholder text
- [ ] **Empty states:** All empty state illustrations are new Blueprint-style Jet images
- [ ] **Modals and toasts:** Create/edit/delete modals reference Jet where applicable
- [ ] **Profile:** User profile and notification pages reference Jet
- [ ] **Dark/Light themes:** Both themes render Jet color palette correctly
- [ ] **Favicon:** Browser tab shows Chevron "J" favicon
- [ ] **Email test:** Trigger invitation email — confirms Jet logo, "Jet" text, and correct sender name
- [ ] **PWA:** Install as PWA — shows "Jet" name and correct icon/theme color
- [ ] Results documented in a checklist with screenshots for any issues found

**Effort:** L (2-3 days)
**Dependencies:** E6-S3, E6-S4 (app running)
**Covers:** FR-VERIFY-5, FR-VERIFY-6

---

### E6-S6: Space App (Public Board) Verification

**Description:**
As a QA tester, I want to verify that the Space public sharing app displays complete Jet branding to anonymous viewers, so that external stakeholders see a consistent Jet experience.

**Acceptance Criteria:**
- [ ] Space app header shows Jet logo
- [ ] Footer displays "Powered by Jet" (or equivalent)
- [ ] Browser tab shows "Jet - [Project Name]"
- [ ] Favicon is Chevron "J"
- [ ] Issue cards and board views use Jet color scheme
- [ ] OG preview (share link on Slack/social): shows Jet OG image with correct title and description
- [ ] Auth flow in Space (if applicable) shows Jet branding
- [ ] Comment, reaction, and voting UI shows no "Plane" references
- [ ] Mobile responsive view shows Jet branding correctly

**Effort:** S (< 1 day)
**Dependencies:** E6-S4 (Space service running)
**Covers:** FR-VERIFY-7

---

## Appendix A: Effort Summary

| Effort | Count | Description |
|--------|-------|-------------|
| S (< 1 day) | 19 | Quick config changes, single-file updates, spot checks |
| M (1-2 days) | 19 | Multi-file updates, template work, integration registration |
| L (2-3 days) | 5 | Bulk string replacement, illustration creation, UI walkthrough |
| XL (3-5 days) | 3 | Icon redesign, large-scale import updates |
| **Total Stories** | **46** | |

**Estimated Total Duration:** 35-52 person-days (7-10 weeks for 1 developer, 3-5 weeks for 2 developers working in parallel on independent epics)

## Appendix B: Parallel Execution Opportunities

The following work streams can proceed simultaneously:

1. **E0 (Design)** can start immediately — no code dependencies
2. **E1 (Backend)** and **E2-S1, E2-S7, E2-S9 (Frontend package rename, CSS, icons)** can start in parallel once E0-S1 is complete
3. **E5-S3 (GitHub templates)** can start at any time — independent of code changes
4. **E4-S1, E4-S2, E4-S3 (OAuth/App registration)** can start once logos are ready (E0-S1) — does not require code changes
5. **E6-S1 (grep audit)** should be run incrementally throughout, not just at the end

## Appendix C: Risk-Linked Stories

| Risk (from PRD) | Mitigating Story |
|-----------------|-----------------|
| Missed "Plane" references | E6-S1 (grep audit), E6-S5 (UI walkthrough) |
| Django content type migration failure | E1-S4 (reversible migration, tested on DB copy) |
| In-flight Celery tasks fail at deploy | E1-S3 (Celery config), E6-S4 (Docker verification) |
| npm `@jet` scope unavailable | E2-S1 (fallback to `@jetpm` noted in acceptance criteria) |
| Build failures from missed imports | E1-S8 (test suite), E6-S2 (backend tests), E6-S3 (frontend builds) |
| Cookie name change breaks sessions | E1-S7 (acceptable one-time impact, documented) |
