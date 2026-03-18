# Architecture & Technical Decisions Document — Jet Rebrand

**Author:** Franc
**Date:** 2026-03-18
**Version:** 1.0
**Status:** Complete
**Companion Document:** [PRD — Jet Rebrand](./prd.md) | [Brand Identity Specification](./jet-brand-identity.md)

---

## 1. Architecture Overview

### 1.1 System Architecture (Unchanged)

The Jet rebrand operates on the existing Plane v0.13.2 monorepo. No architectural changes are introduced -- the stack, patterns, data flow, and deployment topology remain identical. Only names, identifiers, and visual assets change.

```
                    +----------------+
                    |    Browser     |
                    +-------+--------+
                            |
                    +-------v--------+
                    |     Nginx      |  (port 80)
                    |  Reverse Proxy |
                    +--+----+----+---+
                       |    |    |
          +------------+    |    +------------+
          |                 |                 |
   +------v------+   +-----v------+   +------v------+
   |  Web App    |   | API Server |   |  Space App  |
   |  (Next.js)  |   |  (Django)  |   |  (Next.js)  |
   |  port 3000  |   |  port 8000 |   |  port 4000  |
   +------+------+   +--+--+--+---+   +------+------+
          |              |  |  |              |
          +--- REST -----+  |  +--- REST ----+
                            |
               +------------+------------+
               |            |            |
        +------v------+ +--v----+ +-----v------+
        | PostgreSQL  | | Redis | |   MinIO    |
        |   15.2      | | 6.2.7 | |   (S3)     |
        |  port 5432  | | 6379  | | port 9000  |
        +-------------+ +---+---+ +------------+
                             |
                      +------v-------+
                      |    Celery    |
                      |   Workers   |
                      +--------------+
                      |  Celery Beat |
                      +--------------+
```

### 1.2 Monorepo Structure

| Part | Path | Technology | Port |
|------|------|------------|------|
| Web Dashboard | `web/` | Next.js 12.3.2 / React 18 / TypeScript / MobX / Tailwind | 3000 |
| Space (Public Sharing) | `space/` | Next.js 12.3.2 / React 18 / TypeScript / MobX / Tailwind | 4000 |
| API Server | `apiserver/` | Django 4.2.5 / DRF 3.14.0 / Python 3.11 / Celery 5.3.4 | 8000 |
| Shared Packages | `packages/` | TypeScript / tsup / TipTap | build-time |
| Infrastructure | `deploy/`, `nginx/`, root configs | Docker / Nginx 1.25.0 / GitHub Actions | 80 |

### 1.3 Build Pipeline

```
tsconfig ──────────────────────────┐
eslint-config-custom ──────────────┤
tailwind-config-custom ────────────┤
                                   v
editor-core ──> rich-text-editor ──┤
           └──> lite-text-editor ──┤
                                   v
ui ────────────────────────────────┤
                                   v
                         web, space (apps)
```

Managed by Turbo (`turbo.json`) with Yarn Workspaces (`package.json`). Build order enforced via `dependsOn` in the Turbo pipeline configuration.

### 1.4 Data Flow

```
Web/Space Component
  -> MobX Store (action)
    -> Service Class (axios)
      -> HTTP Request
        -> Nginx proxy (/api/ -> port 8000)
          -> Django REST Framework View
            -> Serializer -> Model -> PostgreSQL
              -> post_save signal -> Celery task
```

### 1.5 Principle: Zero Functional Change

This rebrand changes **identity only**. No features are added, removed, or altered. No dependencies change (except potentially new design asset files). No API contracts change. No database schema changes (only a data migration for `django_content_type`). No runtime behavior changes.

---

## 2. Technical Approach for Rebrand

### 2.1 Philosophy

The rebrand is executed as a combination of automated bulk operations and targeted manual edits. Automation handles the high-volume, pattern-matching work (Python imports, string literals). Manual review catches edge cases, context-sensitive text, and configuration files where blind replacement would cause errors.

### 2.2 Automated Scripting Strategy

Two scripts handle the bulk of the rename work:

#### Script 1: Python Backend Rename (`scripts/rename-backend.sh`)

```bash
#!/bin/bash
# Phase 1: Directory rename
mv apiserver/plane apiserver/jet

# Phase 2: Update Python imports across all .py files
find apiserver/ -name "*.py" -type f -exec sed -i '' \
  -e 's/from plane\./from jet./g' \
  -e 's/from plane /from jet /g' \
  -e 's/import plane\./import jet./g' \
  -e 's/import plane$/import jet/g' \
  -e "s/\"plane\./\"jet./g" \
  -e "s/'plane\./'jet./g" \
  -e 's/plane\.settings/jet.settings/g' \
  -e 's/plane\.wsgi/jet.wsgi/g' \
  -e 's/plane\.asgi/jet.asgi/g' \
  -e 's/plane\.urls/jet.urls/g' \
  -e 's/plane\.celery/jet.celery/g' \
  -e 's/plane\.bgtasks/jet.bgtasks/g' \
  -e 's/plane\.db/jet.db/g' \
  -e 's/plane\.api/jet.api/g' \
  -e 's/plane\.utils/jet.utils/g' \
  -e 's/plane\.web/jet.web/g' \
  -e 's/plane\.middleware/jet.middleware/g' \
  -e 's/plane\.analytics/jet.analytics/g' \
  -e 's/celery -A plane/celery -A jet/g' \
  {} \;
```

#### Script 2: Frontend Rename (`scripts/rename-frontend.sh`)

```bash
#!/bin/bash
# Update @plane/* imports to @jet/* in all TS/TSX/JS/JSON files
find web/ space/ packages/ -type f \( -name "*.ts" -o -name "*.tsx" \
  -o -name "*.js" -o -name "*.jsx" -o -name "*.json" \) -exec sed -i '' \
  -e 's/@plane\/ui/@jet\/ui/g' \
  -e 's/@plane\/editor-core/@jet\/editor-core/g' \
  -e 's/@plane\/rich-text-editor/@jet\/rich-text-editor/g' \
  -e 's/@plane\/lite-text-editor/@jet\/lite-text-editor/g' \
  -e 's/"@plane\//"@jet\//g' \
  {} \;

# Update string literals "Plane" -> "Jet" in user-facing text
# This requires careful, context-aware replacement -- see Section 4.2
```

#### Script 3: Infrastructure Rename (`scripts/rename-infra.sh`)

```bash
#!/bin/bash
# Docker Compose service names and image names
find . -name "docker-compose*.yml" -exec sed -i '' \
  -e 's/plane-db/jet-db/g' \
  -e 's/plane-redis/jet-redis/g' \
  -e 's/plane-minio/jet-minio/g' \
  -e 's/plane-frontend/jet-frontend/g' \
  -e 's/plane-backend/jet-backend/g' \
  -e 's/plane-space/jet-space/g' \
  -e 's/plane-proxy/jet-proxy/g' \
  -e 's/makeplane\/plane/makeplane\/jet/g' \
  {} \;
```

### 2.3 Manual Review Process

After each automation script runs:

1. **`git diff` review** -- Examine every changed line to verify correctness.
2. **Context check** -- Ensure "plane" in non-brand contexts (e.g., `airplane`, `plane geometry`, comments about the original project) is handled appropriately.
3. **Build verification** -- Run builds immediately after each phase to catch import errors.
4. **Grep audit** -- Run `grep -ri "plane" --include="*.py"` (or equivalent per file type) to catch any missed references.

### 2.4 Git Strategy

- **Single feature branch:** `feature/jet-rebrand` (branched from `develop`).
- **Atomic commits per phase:**
  - Commit 1: Design assets added (Phase 0)
  - Commit 2: Backend directory rename + import updates (Phase 1)
  - Commit 3: Content type data migration (Phase 1 -- separate for rollback clarity)
  - Commit 4: Frontend package rename + string literal updates (Phase 2)
  - Commit 5: Visual asset replacement (Phase 2)
  - Commit 6: Infrastructure configuration updates (Phase 3)
  - Commit 7: Documentation updates (Phase 5)
  - Commit 8: Verification fixes and cleanup (Phase 6)
- **Merge strategy:** Squash merge or merge commit to `develop`, depending on team preference. The individual commits provide rollback granularity during development.

### 2.5 Order of Operations

```
Phase 0: Design Assets (prerequisite -- no code changes)
    |
Phase 1: Backend Rename
    |  1a. mv apiserver/plane/ -> apiserver/jet/
    |  1b. Automated sed for Python imports
    |  1c. Manual config file updates (wsgi, asgi, celery, settings, manage.py)
    |  1d. Content type data migration
    |  1e. Email template updates
    |  -> Verify: python manage.py test
    |
Phase 2: Frontend Rename
    |  2a. package.json name updates (@plane/* -> @jet/*)
    |  2b. Import path updates
    |  2c. String literal replacements
    |  2d. Visual asset replacement
    |  2e. CSS variable updates
    |  2f. Turbo/workspace config updates
    |  -> Verify: yarn build
    |
Phase 3: Infrastructure
    |  3a. Docker Compose updates (all 3 files)
    |  3b. Nginx config updates
    |  3c. Dockerfile updates
    |  3d. CI/CD pipeline updates
    |  3e. Environment template updates
    |  -> Verify: docker compose build && docker compose up -d
    |
Phase 4: External Integrations (manual, external services)
    |
Phase 5: Documentation
    |
Phase 6: Verification (grep audit, full test, UI walkthrough)
```

---

## 3. Backend Rename Strategy

### 3.1 Directory Rename

**Action:** Rename the top-level Django project directory.

```bash
cd apiserver
mv plane/ jet/
```

**Affected path:** `apiserver/plane/` -> `apiserver/jet/`

**Subdirectories moved (all under the new `jet/` root):**
- `jet/db/` -- Data layer (models, migrations, management commands)
- `jet/api/` -- API layer (views, serializers, URLs, permissions)
- `jet/bgtasks/` -- Celery background tasks
- `jet/settings/` -- Multi-environment Django configuration
- `jet/utils/` -- Utilities
- `jet/middleware/` -- Custom middleware
- `jet/web/` -- Legacy web views
- `jet/analytics/` -- Analytics module
- `jet/tests/` -- Test suite

### 3.2 Python Import Update Automation

**Scope:** ~225 Python files across the `apiserver/` directory.

**Primary regex patterns for `sed`:**

| Pattern | Replacement | Matches |
|---------|-------------|---------|
| `s/from plane\./from jet./g` | Module-relative imports | `from plane.db.models import Issue` |
| `s/from plane /from jet /g` | Package-level imports | `from plane import celery_app` |
| `s/import plane\./import jet./g` | Direct module imports | `import plane.settings` |
| `s/import plane$/import jet/g` | Package import | `import plane` |
| `s/"plane\./"jet./g` | String references to modules | `"plane.settings.production"` |
| `s/'plane\./'jet./g` | Single-quoted module strings | `'plane.bgtasks.issue_automation_task...'` |

**Command:**

```bash
find apiserver/ -name "*.py" -type f -exec sed -i '' \
  -e 's/from plane\./from jet./g' \
  -e 's/from plane /from jet /g' \
  -e 's/import plane\./import jet./g' \
  -e 's/import plane$/import jet/g' \
  -e "s/\"plane\./\"jet./g" \
  -e "s/'plane\./'jet./g" \
  {} \;
```

**Edge cases requiring manual review after automation:**
- String literals containing "Plane" as a brand name (e.g., in error messages, comments, Slack notifications)
- The `Celery("plane")` call in `celery.py`
- `SCOUT_NAME = "Plane"` in `production.py`
- `EMAIL_FROM` default values containing "plane"
- Comments and docstrings referencing "plane project"

### 3.3 Django Settings Module Path Changes

Every file that sets `DJANGO_SETTINGS_MODULE` must be updated:

| File | Current Value | New Value |
|------|---------------|-----------|
| `apiserver/jet/wsgi.py` | `plane.settings.production` | `jet.settings.production` |
| `apiserver/jet/asgi.py` | `plane.settings.production` | `jet.settings.production` |
| `apiserver/jet/celery.py` | `plane.settings.production` | `jet.settings.production` |
| `apiserver/manage.py` | `plane.settings.production` | `jet.settings.production` |
| `Dockerfile` (root) | `ENV DJANGO_SETTINGS_MODULE plane.settings.production` | `ENV DJANGO_SETTINGS_MODULE jet.settings.production` |
| `deploy/selfhost/docker-compose.yml` | `DJANGO_SETTINGS_MODULE=${...:-plane.settings.selfhosted}` | `DJANGO_SETTINGS_MODULE=${...:-jet.settings.selfhosted}` |

### 3.4 WSGI/ASGI/Celery Configuration Updates

#### `apiserver/jet/wsgi.py`

```python
# Before
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plane.settings.production')

# After
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jet.settings.production')
```

Also update the module docstring: `"""WSGI config for jet project."""`

#### `apiserver/jet/asgi.py`

```python
# Before
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plane.settings.production")

# After
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jet.settings.production")
```

#### `apiserver/jet/celery.py`

```python
# Before
from plane.settings.redis import redis_instance
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plane.settings.production")
app = Celery("plane")
app.conf.beat_schedule = {
    "check-every-day-to-archive-and-close": {
        "task": "plane.bgtasks.issue_automation_task.archive_and_close_old_issues",
        ...
    },
    "check-every-day-to-delete_exporter_history": {
        "task": "plane.bgtasks.exporter_expired_task.delete_old_s3_link",
        ...
    },
}

# After
from jet.settings.redis import redis_instance
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jet.settings.production")
app = Celery("jet")
app.conf.beat_schedule = {
    "check-every-day-to-archive-and-close": {
        "task": "jet.bgtasks.issue_automation_task.archive_and_close_old_issues",
        ...
    },
    "check-every-day-to-delete_exporter_history": {
        "task": "jet.bgtasks.exporter_expired_task.delete_old_s3_link",
        ...
    },
}
```

#### `apiserver/jet/__init__.py`

```python
# No path changes needed -- just verify import works:
from .celery import app as celery_app
__all__ = ('celery_app',)
```

#### `apiserver/jet/settings/common.py`

Key lines to update:

```python
# INSTALLED_APPS
"plane.analytics" -> "jet.analytics"
"plane.api"       -> "jet.api"
"plane.bgtasks"   -> "jet.bgtasks"
"plane.db"        -> "jet.db"
"plane.utils"     -> "jet.utils"
"plane.web"       -> "jet.web"
"plane.middleware" -> "jet.middleware"

# URL config
ROOT_URLCONF = "jet.urls"  # was "plane.urls"

# WSGI/ASGI
WSGI_APPLICATION = "jet.wsgi.application"  # was "plane.wsgi.application"
ASGI_APPLICATION = "jet.asgi.application"  # was "plane.asgi.application"

# Email default
EMAIL_FROM = os.environ.get("EMAIL_FROM", "Team Jet <team@jetpm.app>")
# was: "Team Plane <team@mailer.plane.so>"

# Celery imports
CELERY_IMPORTS = ("jet.bgtasks.issue_automation_task", "jet.bgtasks.exporter_expired_task")
# was plane.bgtasks.*
```

#### `apiserver/jet/settings/production.py`

```python
# S3 endpoint default
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "http://jet-minio:9000")
# was: "http://plane-minio:9000"

# WEB_URL default
WEB_URL = os.environ.get("WEB_URL", "https://app.jet.pm")
# was: "https://app.plane.so"

# Scout name
SCOUT_NAME = "Jet"
# was: "Plane"
```

#### `apiserver/jet/settings/selfhosted.py`

```python
# S3 endpoint default
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "http://jet-minio:9000")
# was: "http://plane-minio:9000"
```

#### `apiserver/jet/urls.py`

```python
# Docstring update
"""jet URL Configuration"""
# was: """plane URL Configuration"""

# Import paths (handled by sed, but verify):
path("api/", include("jet.api.urls")),
path("", include("jet.web.urls")),
```

### 3.5 Gunicorn Configuration

**File:** `apiserver/gunicorn.config.py`

This file contains only `post_fork` for psycogreen patching -- no `plane` references. No changes needed.

**However**, the Gunicorn command in `apiserver/bin/takeoff` references the WSGI/ASGI module:

```bash
# Before
exec gunicorn -w 8 -k uvicorn.workers.UvicornWorker plane.asgi:application \
  --bind 0.0.0.0:8000 --max-requests 1200 --max-requests-jitter 1000 --access-logfile -

# After
exec gunicorn -w 8 -k uvicorn.workers.UvicornWorker jet.asgi:application \
  --bind 0.0.0.0:8000 --max-requests 1200 --max-requests-jitter 1000 --access-logfile -
```

### 3.6 Bin Scripts

**`apiserver/bin/takeoff`:**

```bash
# Change: plane.asgi:application -> jet.asgi:application
exec gunicorn -w 8 -k uvicorn.workers.UvicornWorker jet.asgi:application ...
```

**`apiserver/bin/worker`:**

```bash
# Change: celery -A plane -> celery -A jet
celery -A jet worker -l info
```

**`apiserver/bin/beat`:**

```bash
# Change: celery -A plane -> celery -A jet
celery -A jet beat -l info
```

### 3.7 Content Type Data Migration

Django's `django_content_type` table stores `app_label` values derived from the Python module path. When `plane.db` becomes `jet.db`, existing content type records must be updated.

**Create a new migration file:** `apiserver/jet/db/migrations/0047_update_content_types_plane_to_jet.py`

```python
from django.db import migrations


def update_content_types_forward(apps, schema_editor):
    """Update django_content_type app_label from 'db' references that
    were registered under the plane module to work with jet module.

    Note: Django content types use the app_label (the last segment of
    INSTALLED_APPS entry), which is 'db' for both 'plane.db' and 'jet.db'.
    Since the app_label itself ('db') does not change, no content type
    migration may actually be needed. This migration is included as a
    safety measure and will be a no-op if labels are already correct.
    """
    ContentType = apps.get_model('contenttypes', 'ContentType')
    # If any content types somehow reference 'plane' as app_label, update them
    ContentType.objects.filter(app_label='plane').update(app_label='jet')


def update_content_types_reverse(apps, schema_editor):
    """Reverse: update app_label back to plane."""
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ContentType.objects.filter(app_label='jet').update(app_label='plane')


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0046_alter_analyticview_created_by_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(
            update_content_types_forward,
            update_content_types_reverse,
        ),
    ]
```

**Important note on app_label:** Django uses the `app_label` attribute, which for `plane.db` and `jet.db` is both `"db"`. The INSTALLED_APPS entries like `"plane.db"` register with app_label `"db"` by default. Since the label itself does not change (it is `"db"`, not `"plane"`), the content type table may not need modification. However, this migration is included as a safety net and will gracefully handle any edge cases where the label was customized.

If any Django app in the project uses a custom `AppConfig` with `label = "plane_something"`, that `AppConfig.label` must also be updated and a corresponding content type data migration created.

### 3.8 Migration File Relocation

All 46+ existing migration files move automatically with the directory rename (`apiserver/plane/db/migrations/` -> `apiserver/jet/db/migrations/`). Since Django resolves migrations by app_label (which is `"db"`), the migration history in `django_migrations` table references `app='db'` and will continue to work without modification.

**No `django_migrations` table updates are needed** -- the `app` column stores the app_label, not the full module path.

### 3.9 Email Template Updates

**Files (7 templates):**

| Template | Path |
|----------|------|
| Email Verification | `apiserver/templates/emails/auth/email_verification.html` |
| Forgot Password | `apiserver/templates/emails/auth/forgot_password.html` |
| Magic Sign-In | `apiserver/templates/emails/auth/magic_signin.html` |
| Analytics Export | `apiserver/templates/emails/exports/analytics.html` |
| Issues Export | `apiserver/templates/emails/exports/issues.html` |
| Project Invitation | `apiserver/templates/emails/invitations/project_invitation.html` |
| Workspace Invitation | `apiserver/templates/emails/invitations/workspace_invitation.html` |

**Changes per template:**
1. Replace all "Plane" text references with "Jet"
2. Replace logo image URLs/paths with Jet Chevron "J" logo
3. Update "Team Plane" sender references to "Team Jet"
4. Update any `plane.so` domain references to `jetpm.app`
5. Update footer text and support links
6. Update color scheme in inline CSS to match Jet palette where applicable

**Approach:** Manual editing (templates contain HTML with inline CSS; automated replacement is too risky for HTML structure).

### 3.10 manage.py Update

```python
# Before
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plane.settings.production')

# After
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jet.settings.production')
```

### 3.11 User Signal (Slack Notification)

The User model's `post_save` signal sends a Slack notification containing "Plane" branding. This text must be updated to reference "Jet" instead.

### 3.12 Default Settings Values

| Setting | Current | New |
|---------|---------|-----|
| `EMAIL_FROM` | `"Team Plane <team@mailer.plane.so>"` | `"Team Jet <team@jetpm.app>"` |
| `DEFAULT_EMAIL` | `"captain@plane.so"` | `"admin@jetpm.app"` |
| `WEB_URL` (production.py) | `"https://app.plane.so"` | `"https://app.jet.pm"` |
| `SCOUT_NAME` | `"Plane"` | `"Jet"` |
| `AWS_S3_ENDPOINT_URL` defaults | `"http://plane-minio:9000"` | `"http://jet-minio:9000"` |

---

## 4. Frontend Rename Strategy

### 4.1 npm Package Scope Change

**7 packages** must have their `package.json` `name` field updated:

| Package | Current Name | New Name | File |
|---------|-------------|----------|------|
| UI Library | `@plane/ui` | `@jet/ui` | `packages/ui/package.json` |
| Editor Core | `@plane/editor-core` | `@jet/editor-core` | `packages/editor/core/package.json` |
| Rich Text Editor | `@plane/rich-text-editor` | `@jet/rich-text-editor` | `packages/editor/rich-text-editor/package.json` |
| Lite Text Editor | `@plane/lite-text-editor` | `@jet/lite-text-editor` | `packages/editor/lite-text-editor/package.json` |
| ESLint Config | `eslint-config-custom` | `eslint-config-custom` | `packages/eslint-config-custom/package.json` (no change) |
| Tailwind Config | `tailwind-config-custom` | `tailwind-config-custom` | `packages/tailwind-config-custom/package.json` (no change) |
| TSConfig | `tsconfig` | `tsconfig` | `packages/tsconfig/package.json` (no change) |

**Additionally update `dependencies` / `devDependencies`** in consumer `package.json` files:

| File | Change |
|------|--------|
| `web/package.json` | `@plane/ui` -> `@jet/ui`, `@plane/rich-text-editor` -> `@jet/rich-text-editor`, `@plane/lite-text-editor` -> `@jet/lite-text-editor` |
| `space/package.json` | `@plane/ui` -> `@jet/ui` |
| `packages/editor/rich-text-editor/package.json` | `@plane/editor-core` -> `@jet/editor-core` |
| `packages/editor/lite-text-editor/package.json` | `@plane/editor-core` -> `@jet/editor-core` |

**After updating `package.json` files**, run `yarn install` to regenerate `yarn.lock`.

### 4.2 String Literal Replacement Strategy

**Approach: Two-pass replacement.**

**Pass 1 -- Automated (import paths):**

```bash
# Replace @plane/ package imports in source files
find web/ space/ packages/ -type f \( -name "*.ts" -o -name "*.tsx" \
  -o -name "*.js" -o -name "*.jsx" \) -exec sed -i '' \
  -e 's/@plane\/ui/@jet\/ui/g' \
  -e 's/@plane\/editor-core/@jet\/editor-core/g' \
  -e 's/@plane\/rich-text-editor/@jet\/rich-text-editor/g' \
  -e 's/@plane\/lite-text-editor/@jet\/lite-text-editor/g' \
  {} \;
```

**Pass 2 -- Semi-automated (user-facing strings):**

Identify all user-facing "Plane" references:

```bash
grep -rn "Plane" web/components/ web/constants/ web/pages/ space/components/ \
  --include="*.ts" --include="*.tsx" --include="*.js" | grep -v node_modules
```

Common patterns to replace:

| Pattern | Replacement | Context |
|---------|-------------|---------|
| `"Plane"` | `"Jet"` | Brand name in UI text |
| `"Plane -"` | `"Jet -"` | Browser tab titles |
| `"plane.so"` | `"jetpm.app"` | Domain references |
| `"Plane Pro"` | `"Jet Pro"` | Product tier names |
| `"Search in Plane"` | `"Search in Jet"` | Command palette placeholder |
| `"Welcome to Plane"` | `"Welcome to Jet"` | Onboarding text |
| `"Powered by Plane"` | `"Powered by Jet"` | Space app footer |
| `"captain@plane.so"` | `"admin@jetpm.app"` | Default credentials |
| `"makeplane"` | contextual | GitHub org references |
| `"plane-"` | `"jet-"` | Docker service name references in env |

**Manual review is required** for each match to ensure:
- The word "plane" is used as a brand name (not a generic English word)
- The replacement makes grammatical sense in context
- Dynamic strings (template literals) are correctly handled

### 4.3 Key Frontend Files Requiring Manual Updates

#### SEO Constants

Typically in `web/constants/seo-variables.ts` or similar:

```typescript
// Update all metadata
export const SITE_NAME = "Jet";
export const SITE_TITLE = "Jet - Project Management";
export const SITE_DESCRIPTION = "Open-source project management at jet speed.";
export const SITE_URL = "https://jetpm.app";
```

#### manifest.json (2 files)

**`web/public/manifest.json`:**

```json
{
  "name": "Jet",
  "short_name": "Jet",
  "description": "Open-source project management at jet speed",
  "theme_color": "#09090B",
  "background_color": "#09090B",
  "icons": [
    { "src": "/favicon/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/favicon/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

**`space/public/manifest.json`:** Same pattern.

#### next.config.js (2 files)

Update `images.domains` to remove any `plane.so` or Plane-specific S3 domains. Add Jet domains as needed.

#### _document.tsx (2 files: web + space)

Update:
- `<title>` fallback
- `<meta>` description, OG tags
- Analytics script references (PostHog, Plausible, Clarity project names)
- Sentry project references
- Favicon link tags

#### _app.tsx (2 files: web + space)

Update:
- Any hardcoded "Plane" strings in providers/wrappers
- Toast/notification default text

### 4.4 Asset Replacement Pipeline

**Source:** Phase 0 design deliverables (Chevron "J" logo, favicon set, illustrations).

**Target directories and files:**

| Directory | Content | Count |
|-----------|---------|-------|
| `web/public/logos/` | Logo SVG/PNG variants (dark, light, mono) | ~6 files |
| `web/public/favicon/` | Favicon PNGs (all sizes) + site.webmanifest | ~12 files |
| `web/public/empty-state/` | Blueprint-style empty state illustrations | ~15 files |
| `web/public/onboarding/` | Onboarding step images | ~4 files |
| `web/public/auth/` | Auth screen backgrounds | ~2 files |
| `web/public/theme-mode/` | Theme preview thumbnails | ~5 files |
| `space/public/` | Mirror of relevant web assets | ~10 files |

**Process:**
1. Export all design assets from design tool (Figma/AI) in required formats and sizes.
2. Name files identically to existing assets (drop-in replacement).
3. Copy to target directories, overwriting existing Plane assets.
4. Verify file sizes are reasonable (SVG < 50KB, PNGs compressed).

### 4.5 CSS Variable Updates

**File:** `web/styles/globals.css` (or wherever theme CSS variables are defined).

Update the default dark mode theme to use the Jet Black palette:

```css
/* Dark mode (Jet Black -- default) */
:root {
  --color-primary-100: #3B82F6;   /* Jet Blue */
  --color-background-100: #09090B; /* Jet Black */
  --color-background-90: #18181B;  /* Jet Dark */
  --color-background-80: #27272A;  /* Jet Gray */
  --color-text-100: #FAFAFA;       /* Jet White */
  --color-text-200: #A1A1AA;       /* Jet Silver */
  --color-border-100: #27272A;     /* Jet Gray */
  --color-border-200: #3F3F46;     /* Jet Steel */
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

The exact CSS variable names depend on the current implementation -- the above follows the Jet Brand Identity Specification color mapping. The theme system (5 variants: light, dark, light-contrast, dark-contrast, custom) must reflect Jet defaults. Custom theme user overrides continue to work unchanged.

### 4.6 Turbo/Workspace Configuration Updates

#### `turbo.json`

Update all `@plane/*` references in pipeline keys:

```json
{
  "web#develop": {
    "dependsOn": [
      "@jet/lite-text-editor#build",
      "@jet/rich-text-editor#build",
      "@jet/ui#build"
    ]
  },
  "space#develop": {
    "dependsOn": [
      "@jet/lite-text-editor#build",
      "@jet/rich-text-editor#build",
      "@jet/ui#build"
    ]
  },
  "web#build": {
    "dependsOn": [
      "@jet/lite-text-editor#build",
      "@jet/rich-text-editor#build",
      "@jet/ui#build"
    ]
  },
  "space#build": {
    "dependsOn": [
      "@jet/lite-text-editor#build",
      "@jet/rich-text-editor#build",
      "@jet/ui#build"
    ]
  },
  "@jet/lite-text-editor#build": {
    "dependsOn": ["@jet/editor-core#build"]
  },
  "@jet/rich-text-editor#build": {
    "dependsOn": ["@jet/editor-core#build"]
  }
}
```

#### Root `package.json`

```json
{
  "repository": "https://github.com/<org>/jet.git",
  "version": "1.0.0"
}
```

The `workspaces` array does not need changes -- it references directory paths (`"web"`, `"space"`, `"packages/editor/*"`, etc.), not package names.

---

## 5. Infrastructure Changes

### 5.1 Docker Image Naming

**Current -> New image names:**

| Current | New |
|---------|-----|
| `makeplane/plane-frontend` | `<registry>/jet-frontend` |
| `makeplane/plane-backend` | `<registry>/jet-backend` |
| `makeplane/plane-space` | `<registry>/jet-space` |
| `makeplane/plane-proxy` | `<registry>/jet-proxy` |

The Docker Hub organization/registry depends on where the Jet project will publish images. For development, local builds are used. The image name pattern changes from `plane-*` to `jet-*`.

### 5.2 Docker Compose Service Naming

**3 Docker Compose files must be updated:**

#### `docker-compose.yml` (Full Development)

| Current Service | New Service | Current Container | New Container |
|----------------|-------------|-------------------|---------------|
| `plane-db` | `jet-db` | `plane-db` | `jet-db` |
| `plane-redis` | `jet-redis` | `plane-redis` | `jet-redis` |
| `plane-minio` | `jet-minio` | `plane-minio` | `jet-minio` |

The `web`, `space`, `api`, `worker`, `beat-worker`, `proxy` services keep their names (they are not `plane-` prefixed currently). But their `depends_on` references to `plane-db`, `plane-redis`, `plane-minio` must be updated.

**The `createbuckets` service** uses MinIO client commands that reference `plane-minio` as a host alias:

```bash
# Before
/usr/bin/mc config host add plane-minio http://plane-minio:9000 ...
/usr/bin/mc mb plane-minio/$AWS_S3_BUCKET_NAME
/usr/bin/mc anonymous set download plane-minio/$AWS_S3_BUCKET_NAME

# After
/usr/bin/mc config host add jet-minio http://jet-minio:9000 ...
/usr/bin/mc mb jet-minio/$AWS_S3_BUCKET_NAME
/usr/bin/mc anonymous set download jet-minio/$AWS_S3_BUCKET_NAME
```

#### `docker-compose-local.yml` (Local Dev)

Same service rename: `plane-db`, `plane-redis`, `plane-minio` -> `jet-db`, `jet-redis`, `jet-minio`. Plus the `createbuckets` MinIO client commands.

Also update the Celery commands in `worker` and `beat-worker` services:

```yaml
# Before
command: /bin/sh -c "celery -A plane worker -l info"
command: /bin/sh -c "celery -A plane beat -l info"

# After
command: /bin/sh -c "celery -A jet worker -l info"
command: /bin/sh -c "celery -A jet beat -l info"
```

And the Django runserver command in the `api` service:

```yaml
# Before
command: ... --settings=plane.settings.local

# After
command: ... --settings=jet.settings.local
```

#### `deploy/selfhost/docker-compose.yml` (Self-Hosted Production)

Same service renames plus:

- Update `x-app-env` environment variable defaults:
  - `DJANGO_SETTINGS_MODULE=${...:-jet.settings.selfhosted}` (was `plane.settings.selfhosted`)
  - `PGHOST=${PGHOST:-jet-db}` (was `plane-db`)
  - `PGDATABASE=${PGDATABASE:-jet}` (was `plane`)
  - `POSTGRES_USER=${POSTGRES_USER:-jet}` (was `plane`)
  - `POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-jet}` (was `plane`)
  - `POSTGRES_DB=${POSTGRES_DB:-jet}` (was `plane`)
  - `REDIS_HOST=${REDIS_HOST:-jet-redis}` (was `plane-redis`)
  - `AWS_S3_ENDPOINT_URL=${...:-http://jet-minio:9000}` (was `plane-minio`)
  - `EMAIL_FROM=${...:-"Team Jet <team@jetpm.app>"}` (was `plane.so`)
  - `DEFAULT_EMAIL=${DEFAULT_EMAIL:-admin@jetpm.app}` (was `captain@plane.so`)
- Update image names: `makeplane/plane-frontend` -> `<registry>/jet-frontend`, etc.

### 5.3 Nginx Upstream Configuration

#### `nginx/nginx.conf.template`

```nginx
# Before
location /${BUCKET_NAME}/ {
    proxy_pass http://plane-minio:9000/uploads/;
}

# After
location /${BUCKET_NAME}/ {
    proxy_pass http://jet-minio:9000/uploads/;
}
```

The `web:3000`, `api:8000`, `space:3000` upstreams do not change (those service names are not `plane-` prefixed).

#### `nginx/nginx-single-docker-image.conf`

```nginx
# Before
upstream plane {
    server localhost:80;
}

# After
upstream jet {
    server localhost:80;
}
```

The upstream name `plane` is used only as an nginx identifier and does not affect routing, but it should be renamed for consistency.

### 5.4 Supervisor Configuration

**File:** `nginx/supervisor.conf`

No `plane` references exist in the supervisor config -- it uses generic names (`node`, `python`, `nginx`, `worker`). No changes needed.

### 5.5 Root Dockerfile

**File:** `Dockerfile` (root)

**Changes:**

```dockerfile
# Before
ENV DJANGO_SETTINGS_MODULE plane.settings.production
COPY apiserver/plane plane/

RUN addgroup --system --gid 1001 plane
RUN adduser --system --uid 1001 captain

COPY --from=installer --chown=captain:plane /app/apps/app/.next/standalone ./

# After
ENV DJANGO_SETTINGS_MODULE jet.settings.production
COPY apiserver/jet jet/

RUN addgroup --system --gid 1001 jet
RUN adduser --system --uid 1001 captain

COPY --from=installer --chown=captain:jet /app/apps/app/.next/standalone ./
```

Note: The `turbo prune --scope=app --scope=plane-deploy` command in Stage 1 may need updating depending on the Turbo workspace names. Verify the `--scope` values match the actual workspace names defined in `package.json`.

### 5.6 API Server Dockerfiles

#### `apiserver/Dockerfile.api`

Update any `DJANGO_SETTINGS_MODULE` or `plane` module path references.

#### `apiserver/Dockerfile.dev`

Same as above.

### 5.7 CI/CD Pipeline Updates

#### `.github/workflows/update-docker-images.yml`

Update all image name references:

```yaml
# Before
images: ${{ secrets.DOCKERHUB_USERNAME }}/plane-frontend
images: ${{ secrets.DOCKERHUB_USERNAME }}/plane-backend
images: ${{ secrets.DOCKERHUB_USERNAME }}/plane-space
images: ${{ secrets.DOCKERHUB_USERNAME }}/plane-proxy

# After
images: ${{ secrets.DOCKERHUB_USERNAME }}/jet-frontend
images: ${{ secrets.DOCKERHUB_USERNAME }}/jet-backend
images: ${{ secrets.DOCKERHUB_USERNAME }}/jet-space
images: ${{ secrets.DOCKERHUB_USERNAME }}/jet-proxy
```

Also update the workflow name:

```yaml
name: Update Docker Images for Jet on Release
```

#### `.github/workflows/create-sync-pr.yml`

Update references to `makeplane/plane` repository name if applicable, or remove this workflow if the Jet project does not sync to an enterprise edition.

#### `.github/workflows/build-test-pull-request.yml`

No `plane` references expected in the workflow logic (it uses generic directory paths). Verify and update any Plane-specific comments.

### 5.8 Environment Variable Template Updates

#### `deploy/selfhost/variables.env`

Replace all Plane defaults:

| Variable | Before | After |
|----------|--------|-------|
| `PGHOST` | `plane-db` | `jet-db` |
| `PGDATABASE` | `plane` | `jet` |
| `PGUSER` | `plane` | `jet` |
| `PGPASSWORD` | `plane` | `jet` |
| `REDIS_HOST` | `plane-redis` | `jet-redis` |
| `AWS_S3_ENDPOINT_URL` | `http://plane-minio:9000` | `http://jet-minio:9000` |
| `EMAIL_FROM` | `Team Plane <team@mailer.plane.so>` | `Team Jet <team@jetpm.app>` |
| `DEFAULT_EMAIL` | `captain@plane.so` | `admin@jetpm.app` |
| `DJANGO_SETTINGS_MODULE` | `plane.settings.selfhosted` | `jet.settings.selfhosted` |

#### `.env.example` files (if they exist in root, web/, space/, apiserver/)

Apply same pattern of updates.

### 5.9 setup.sh Update

Update any comments or echo statements referencing "Plane" to "Jet". Update default email/domain values.

### 5.10 Heroku Configuration

#### `app.json`

```json
{
  "name": "Jet",
  "description": "Open-source project management at jet speed",
  ...
}
```

#### `heroku.yml`

Update if any Plane-specific references exist.

---

## 6. Database Migration Strategy

### 6.1 Django Content Type Table

**Table:** `django_content_type`

This table has columns: `id`, `app_label`, `model`.

**Current state:** All models are registered under app_label `"db"` (from `plane.db`). Since Django derives `app_label` from the app module's last path segment, renaming `plane.db` to `jet.db` does not change the app_label -- it remains `"db"`.

**Conclusion:** No content type migration is strictly necessary for the `db` app. However, the data migration in Section 3.7 is included as a safety net to handle any apps where the `app_label` might be set to `"plane"` via a custom `AppConfig`.

**Other INSTALLED_APPS that change:**

| Current | New | app_label (derived) |
|---------|-----|-------------------|
| `plane.analytics` | `jet.analytics` | `analytics` (unchanged) |
| `plane.api` | `jet.api` | `api` (unchanged) |
| `plane.bgtasks` | `jet.bgtasks` | `bgtasks` (unchanged) |
| `plane.db` | `jet.db` | `db` (unchanged) |
| `plane.utils` | `jet.utils` | `utils` (unchanged) |
| `plane.web` | `jet.web` | `web` (unchanged) |
| `plane.middleware` | `jet.middleware` | `middleware` (unchanged) |

Since Django uses the **last segment** of the dotted path as the `app_label`, and none of these segments change, the `django_content_type` table needs no modifications.

### 6.2 django_migrations Table

**Table:** `django_migrations`

This table has columns: `id`, `app`, `name`, `applied`.

The `app` column stores the app_label (e.g., `"db"`), not the full module path. Since the app_label does not change (see 6.1), **no `django_migrations` updates are needed**.

All existing migration records will continue to be recognized. New migrations created under `apiserver/jet/db/migrations/` will also use app_label `"db"` and be correctly sequenced.

### 6.3 Existing Data Compatibility

**File uploads:** S3/MinIO stored files use configurable `upload_to` paths in Django model fields. These paths use the `AWS_S3_BUCKET_NAME` (typically `"uploads"`) and model-defined sub-paths. As long as `upload_to` paths in model field definitions do not contain `"plane"`, existing files remain accessible. **Verified:** FileAsset and IssueAttachment models use generic upload paths.

**User sessions:** Session cookies may reference "plane" in cookie names (if `SESSION_COOKIE_NAME` was customized). The default Django session cookie name is `"sessionid"` -- no "plane" reference. **Action:** Verify `SESSION_COOKIE_NAME` is not set to a Plane-branded value. If it is, changing it will invalidate all existing sessions (acceptable per PRD NFR-DATA-3).

**JWT tokens:** Tokens are cryptographic and do not contain "plane" in their payload. Existing tokens will continue to work.

### 6.4 Rollback Plan

**If the migration fails:**

1. **Database:** The content type migration (Section 3.7) includes a `reverse` function. Run `python manage.py migrate db 0046` to reverse.
2. **Code:** `git revert` the specific migration commit (Commit 3 in the Git strategy).
3. **Full rollback:** `git checkout develop` to return to pre-rebrand state.
4. **Data:** No destructive changes are made to user data. The only data modification is the content type app_label update, which is reversible.

**Pre-migration safety:**

```bash
# Before running migrations on any database with real data:
docker compose exec jet-db pg_dump -U jet jet > pre-rebrand-backup.sql
```

---

## 7. External Integration Re-registration

These are manual, out-of-code tasks that must be performed on external service dashboards.

### 7.1 Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create new OAuth 2.0 Client ID or update existing
3. Set application name to "Jet"
4. Update authorized redirect URIs to Jet domain(s)
5. Update `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in environment
6. Update consent screen branding (logo, name, links)

### 7.2 GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/applications)
2. Create new OAuth App or update existing
3. Application name: "Jet"
4. Homepage URL: `https://jetpm.app`
5. Authorization callback URL: `https://<jet-domain>/api/v1/auth/github/callback/`
6. Update `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in environment

### 7.3 GitHub App (Repository Sync)

1. Go to [GitHub Developer Settings > GitHub Apps](https://github.com/settings/apps)
2. Create new GitHub App or update existing
3. App name: "Jet"
4. Update webhook URL and permissions
5. Update `NEXT_PUBLIC_GITHUB_APP_NAME` environment variable in `turbo.json` global env

### 7.4 Slack App/Bot

1. Go to [Slack API](https://api.slack.com/apps)
2. Create new Slack App or update existing
3. App name: "Jet"
4. Update bot name, icon, and description
5. Update OAuth redirect URLs
6. Update `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_BOT_TOKEN` in environment

### 7.5 Sentry

1. Go to Sentry dashboard
2. Create new project or rename existing: "Jet" (frontend) and "Jet API" (backend)
3. Update `SENTRY_DSN` environment variable
4. Update `NEXT_PUBLIC_SENTRY_DSN` for frontend
5. Update `sentry_sdk.init()` environment parameter in `production.py`

### 7.6 Analytics Services

| Service | Action |
|---------|--------|
| PostHog | Update project name, update `NEXT_PUBLIC_POSTHOG_KEY` if needed |
| Plausible | Create new site for Jet domain, update `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` |
| Microsoft Clarity | Update project name |
| Crisp (chat) | Update `NEXT_PUBLIC_CRISP_ID` if changing workspace |

### 7.7 Unsplash API

1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Update application name to "Jet"
3. `UNSPLASH_ACCESS_KEY` value does not change

### 7.8 OpenAI

Update the system prompt in any AI-powered features (GPT endpoint) to reference "Jet" instead of "Plane":

```python
# In the view that calls OpenAI:
# Before: "You are a helpful assistant for Plane, a project management tool..."
# After:  "You are a helpful assistant for Jet, a project management tool..."
```

No API key changes needed.

### 7.9 CORS Origins

If `CORS_ALLOWED_ORIGINS` is explicitly set (not `CORS_ALLOW_ALL_ORIGINS = True`), add Jet domains and remove Plane domains:

```python
CORS_ALLOWED_ORIGINS = [
    "https://jetpm.app",
    "https://app.jetpm.app",
    # Remove plane.so entries
]
```

Currently, both `production.py` and `selfhosted.py` use `CORS_ALLOW_ALL_ORIGINS = True`, so no immediate change is needed. Tightening CORS is a post-rebrand hardening task.

---

## 8. Verification Strategy

### 8.1 Automated Grep Audit

The primary completeness check. Run after all phases are complete:

```bash
# Comprehensive grep for any remaining "plane" references
grep -ri "plane" \
  --include="*.py" \
  --include="*.ts" \
  --include="*.tsx" \
  --include="*.js" \
  --include="*.jsx" \
  --include="*.json" \
  --include="*.yml" \
  --include="*.yaml" \
  --include="*.md" \
  --include="*.html" \
  --include="*.css" \
  --include="*.conf" \
  --include="*.env" \
  --include="*.txt" \
  --include="*.sh" \
  --include="*.cfg" \
  . \
  | grep -v node_modules \
  | grep -v .git \
  | grep -v _bmad \
  | grep -v yarn.lock \
  | grep -v .next \
  | grep -v dist/ \
  | grep -v __pycache__
```

**Pass criteria:** Zero results (excluding false positives like the English word "plane" in license text, which should be verified individually).

**Known false positives to exclude:**
- `LICENSE.txt` -- AGPL-3.0 text may reference the original project legitimately
- `yarn.lock` -- Auto-generated, will be regenerated
- Third-party library code in `node_modules/`
- Git history (`.git/`)
- Build artifacts (`.next/`, `dist/`)
- Brainstorming/planning docs (`_bmad*/`)

### 8.2 Build Verification

```bash
# Backend
cd apiserver
python manage.py check                    # Django system check
python manage.py test                     # Full test suite
python manage.py migrate --check          # Verify migrations apply cleanly

# Frontend
yarn install                              # Regenerate lockfile
yarn build                                # Build all packages + apps (via Turbo)
# Or individually:
yarn build --filter=@jet/ui
yarn build --filter=@jet/editor-core
yarn build --filter=@jet/rich-text-editor
yarn build --filter=@jet/lite-text-editor
yarn build --filter=web
yarn build --filter=space

# Infrastructure
docker compose build                      # Build all Docker images
docker compose up -d                      # Start all services
docker compose ps                         # Verify all services running
docker compose logs api | head -50        # Check for startup errors
```

### 8.3 Test Suite Verification

**Backend (Django):**

```bash
cd apiserver
python manage.py test
```

Test files are in `apiserver/jet/tests/` (moved from `plane/tests/`). All imports in test files must also be updated from `plane.*` to `jet.*`.

**Frontend:** No formal test suite exists in v0.13.2. Linting serves as the primary code quality check:

```bash
yarn lint
```

### 8.4 Manual UI Walkthrough

**Checklist:**

| Screen | Check |
|--------|-------|
| Sign-in page | Jet logo, Jet Black colors, "Jet" in title |
| Sign-up page | Jet branding, no "Plane" text |
| Onboarding | "Welcome to Jet" text, step images |
| Dashboard | Sidebar logo, "Jet" in header, favicon |
| Browser tab | "Jet - Dashboard", "Jet - Issues", etc. |
| Command palette (Cmd+K) | "Search in Jet..." placeholder |
| Project settings | No "Plane" references |
| Workspace settings | No "Plane" references |
| Issue detail | No "Plane" references in comments, activity |
| Cycles/Sprints | No "Plane" references |
| Modules | No "Plane" references |
| Pages | No "Plane" references |
| Views | No "Plane" references |
| Analytics | No "Plane" references |
| Profile settings | No "Plane" references |
| Theme switcher | All 5 themes use Jet defaults |
| Empty states | Blueprint-style illustrations, "Jet" copy |
| Error pages (404, 500) | Jet branding |
| Space app (public board) | Jet logo in header, "Powered by Jet" footer |
| Space app login | Jet branding |
| PWA install prompt | "Jet" name and icon |

### 8.5 Email Verification

Trigger each email type and verify Jet branding:

1. Sign up -> email verification email
2. Forgot password -> reset email
3. Magic link login -> magic link email
4. Invite to workspace -> workspace invitation email
5. Invite to project -> project invitation email
6. Export issues -> export ready email
7. Export analytics -> analytics export email

**Check:** Logo, sender name ("Team Jet"), footer text, domain links, no "Plane" text anywhere.

### 8.6 Docker Service Verification

```bash
# Verify all services start with new names
docker compose -f docker-compose-local.yml up -d
docker compose -f docker-compose-local.yml ps

# Expected output:
# jet-db     | running
# jet-redis  | running
# jet-minio  | running
# ...

# Verify inter-service communication
docker compose exec api python manage.py check --database default
docker compose exec api python -c "import redis; r = redis.from_url('redis://jet-redis:6379'); r.ping()"
```

### 8.7 CI Check for Future Prevention

Add a CI step (or pre-commit hook) to prevent "Plane" references from being reintroduced:

```yaml
# .github/workflows/build-test-pull-request.yml (add step)
- name: Check for Plane references
  run: |
    RESULTS=$(grep -ri "plane" --include="*.py" --include="*.ts" --include="*.tsx" \
      --include="*.js" --include="*.json" --include="*.yml" --include="*.html" \
      --include="*.css" --include="*.conf" . \
      | grep -v node_modules | grep -v .git | grep -v _bmad | grep -v yarn.lock \
      | grep -v LICENSE.txt || true)
    if [ -n "$RESULTS" ]; then
      echo "Found 'plane' references that should be 'jet':"
      echo "$RESULTS"
      exit 1
    fi
```

---

## 9. Risk Assessment

### 9.1 Technical Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|-----------|
| R1 | Missed "Plane" references in obscure files | Medium | Low | Automated grep audit (Section 8.1); CI check prevents regression |
| R2 | Python import errors from missed sed patterns | Medium | High | Run `python manage.py check` and full test suite after Phase 1; fix iteratively |
| R3 | Frontend build failures from incorrect package references | Medium | High | Run `yarn build` after each Phase 2 sub-step; fix iteratively |
| R4 | Django content type migration failure on existing databases | Low | High | Test migration on database copy first; migration is reversible; app_labels likely unchanged (Section 6.1) |
| R5 | In-flight Celery tasks fail during deployment | Low | Medium | Deploy during low-traffic window; drain Celery queues before deploy (`celery -A jet control shutdown`); existing tasks using old `plane.*` paths will fail but can be retried |
| R6 | npm `@jet` scope unavailable on public registry | Low | Medium | Scope is only used in the monorepo (private packages); no public npm publishing. If public publishing is needed, fallback to `@jetpm` scope |
| R7 | S3 upload paths break due to hardcoded "plane" in upload_to | Low | High | Audit all `FileField` and `ImageField` definitions for `upload_to` paths; verify none contain "plane" |
| R8 | Cookie/session name change invalidates user sessions | Low | Low | Django uses default cookie names (`sessionid`, `csrftoken`); no "plane" prefix. Verify `SESSION_COOKIE_NAME` is not customized. One-time re-login is acceptable (NFR-DATA-3) |
| R9 | Docker Compose service resolution fails due to stale DNS | Low | Medium | Run `docker compose down -v` to clear old service names before starting with new names; or remove old containers first |
| R10 | Turbo cache invalidation issues after package rename | Low | Low | Clear Turbo cache: `rm -rf node_modules/.cache/turbo`; or run `yarn build --force` |
| R11 | Nginx upstream resolution fails for renamed services | Low | High | Verify all `proxy_pass` directives match Docker Compose service names; test with `docker compose up -d && curl localhost/api/` |
| R12 | Third-party integrations break (Slack, GitHub) | Low | Medium | Re-register integrations before deploying rebrand to production (Phase 4); test in staging environment |
| R13 | Email templates render incorrectly after branding update | Low | Low | Send test emails for each template; visual verification in Gmail, Outlook, Apple Mail |
| R14 | Custom `AppConfig` classes reference "plane" in labels | Low | High | Search for `class *Config(AppConfig)` and verify `label` attributes; update content type migration accordingly |

### 9.2 Process Risks

| # | Risk | Mitigation |
|---|------|-----------|
| P1 | Scope creep -- temptation to add features during rebrand | Strict "identity only" principle; no functional changes |
| P2 | Design asset delivery delays (Phase 0 is critical path) | Can proceed with placeholder assets; swap final assets before merge |
| P3 | Merge conflicts from parallel development on `develop` | Rebase frequently; communicate rebrand timeline to team |

---

## 10. Technology Stack (Unchanged)

The complete technology stack is documented here for reference. No changes are made to any technology choices, versions, or dependencies as part of the rebrand.

### 10.1 Frontend (Web + Space)

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Next.js | 12.3.2 |
| UI Library | React | 18.2.0 |
| Language | TypeScript | 4.7.4 |
| State Management | MobX + mobx-react-lite | 6.10.0 |
| Data Fetching | SWR | 2.1.3 |
| HTTP Client | Axios | 1.1.3 |
| Styling | Tailwind CSS | 3.3.3 |
| Forms | React Hook Form | 7.38.0 |
| UI Components | Headless UI, Blueprint.js, MUI (partial) | Various |
| Rich Text Editor | TipTap (ProseMirror) | 2.1.7 |
| Charts | Nivo (@nivo/bar, line, pie) | 0.80.0 |
| Icons | Lucide React | 0.274.0 |
| Drag & Drop | @hello-pangea/dnd | 16.3.0 |
| Command Menu | cmdk | 0.2.0 |
| Theme | next-themes | 0.2.1 |
| Error Tracking | @sentry/nextjs | 7.36.0 |

### 10.2 Backend (API Server)

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Django | 4.2.5 |
| REST API | Django REST Framework | 3.14.0 |
| Auth (JWT) | djangorestframework-simplejwt | 5.3.0 |
| Database Driver | psycopg | 3.1.10 |
| Background Tasks | Celery | 5.3.4 |
| Scheduled Tasks | django-celery-beat | 2.5.0 |
| WebSocket | Django Channels | 4.0.0 |
| OAuth | django-allauth, dj_rest_auth | 0.55.2, 2.2.5 |
| File Storage | django-s3-storage, boto3 | 0.14.0 |
| CORS | django-cors-headers | 4.2.0 |
| Permissions | django-guardian | 2.4.0 |
| Error Tracking | sentry-sdk | 1.30.0 |
| WSGI Server | Gunicorn | 21.2.0 |
| ASGI Server | Uvicorn | 0.23.2 |
| Audit | django-crum | Current |

### 10.3 Data Layer

| Category | Technology | Version |
|----------|-----------|---------|
| Primary Database | PostgreSQL | 15.2 |
| Cache / Message Broker | Redis | 6.2.7 |
| Object Storage | MinIO (S3-compatible) | Latest |

### 10.4 Infrastructure

| Category | Technology | Version |
|----------|-----------|---------|
| Containerization | Docker | Latest |
| Orchestration | Docker Compose | v3.8 spec |
| Reverse Proxy | Nginx | 1.25.0 |
| Process Manager | Supervisor | Latest (in single-image Dockerfile) |
| Monorepo Build | Turbo | 1.10.16 |
| Package Manager | Yarn | 1.22.19 |
| CI/CD | GitHub Actions | N/A |
| Node.js Runtime | Node.js | 18.x (Alpine) |
| Python Runtime | Python | 3.11.1 (Alpine 3.17) |

### 10.5 External Services (Optional)

| Service | Purpose |
|---------|---------|
| OpenAI API | AI-powered issue assistance |
| GitHub API | OAuth + repository sync |
| Slack API | Bot notifications |
| Google OAuth | Authentication |
| Unsplash API | Cover image search |
| Sentry | Error tracking |
| PostHog | Product analytics |
| Plausible | Website analytics |
| SendGrid/SES/SMTP | Transactional email |
| AWS S3 | Production file storage (alternative to MinIO) |

---

## Appendix A: Complete File Change Inventory

### Backend Files (Estimated)

| Category | File Count | Approach |
|----------|-----------|----------|
| Python imports (`from plane.*`) | ~225 | Automated sed |
| Settings files | 8 | Manual review after sed |
| WSGI/ASGI/Celery config | 3 | Manual |
| Bin scripts (takeoff, worker, beat) | 3 | Manual |
| manage.py | 1 | Manual |
| Email templates | 7 | Manual |
| Migration (new) | 1 | Manual creation |
| User script | 1 | Manual |
| **Total** | **~249** | |

### Frontend Files (Estimated)

| Category | File Count | Approach |
|----------|-----------|----------|
| package.json (name + deps) | ~9 | Manual |
| TypeScript/JSX imports (`@plane/*`) | ~200 | Automated sed |
| String literals ("Plane") | ~100 | Semi-automated + manual |
| manifest.json | 2 | Manual |
| next.config.js | 2 | Manual |
| _document.tsx / _app.tsx | 4 | Manual |
| CSS/style files | ~5 | Manual |
| Visual assets (images) | ~50 | File replacement |
| turbo.json | 1 | Manual |
| **Total** | **~373** | |

### Infrastructure Files

| Category | File Count | Approach |
|----------|-----------|----------|
| Docker Compose files | 3 | Automated sed + manual review |
| Dockerfiles | 8 | Manual |
| Nginx config files | 2 | Manual |
| Supervisor config | 1 | Verify (no changes) |
| GitHub Actions workflows | 3 | Manual |
| Environment templates | 3+ | Manual |
| setup.sh | 1 | Manual |
| Heroku config | 2 | Manual |
| **Total** | **~23** | |

### Documentation

| Category | File Count | Approach |
|----------|-----------|----------|
| README.md | 1 | Full rewrite |
| CONTRIBUTING.md | 1 | Find-replace |
| ENV_SETUP.md | 1 | Find-replace |
| CODE_OF_CONDUCT.md | 1 | Find-replace |
| GitHub templates | 3 | Find-replace |
| LICENSE.txt | 1 | Verify (attribution) |
| docs/ | 16 | Regenerate |
| **Total** | **~24** | |

**Grand total: ~669 files** (including automated + manual changes).

---

## Appendix B: Quick Reference Commands

```bash
# === Phase 1: Backend ===
cd apiserver && mv plane/ jet/
find . -name "*.py" -exec sed -i '' -e 's/from plane\./from jet./g' ... {} \;
python manage.py check
python manage.py test

# === Phase 2: Frontend ===
# Update package.json files manually, then:
yarn install
find web/ space/ packages/ -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -exec sed -i '' -e 's/@plane\//@jet\//g' {} \;
yarn build

# === Phase 3: Infrastructure ===
sed -i '' 's/plane-db/jet-db/g; s/plane-redis/jet-redis/g; s/plane-minio/jet-minio/g' \
  docker-compose*.yml deploy/selfhost/docker-compose.yml
docker compose build
docker compose up -d

# === Phase 6: Verification ===
grep -ri "plane" --include="*.py" --include="*.ts" --include="*.tsx" \
  --include="*.js" --include="*.json" --include="*.yml" --include="*.html" \
  --include="*.css" --include="*.conf" . \
  | grep -v node_modules | grep -v .git | grep -v _bmad | grep -v yarn.lock
```
