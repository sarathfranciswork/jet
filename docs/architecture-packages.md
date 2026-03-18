# Architecture - Shared Packages

**Generated:** 2026-03-18
**Part:** packages
**Type:** TypeScript Libraries

## Overview

Shared npm packages consumed by web and space applications, managed via Yarn Workspaces and built with Turbo.

## Package Inventory

| Package | npm Name | Purpose | Consumers |
|---------|----------|---------|-----------|
| `packages/ui` | `@plane/ui` | UI component library | web, space |
| `packages/editor/core` | `@plane/editor-core` | TipTap editor base | rich-text-editor, lite-text-editor |
| `packages/editor/rich-text-editor` | `@plane/rich-text-editor` | Full-featured editor | web |
| `packages/editor/lite-text-editor` | `@plane/lite-text-editor` | Lightweight editor | web |
| `packages/eslint-config-custom` | `eslint-config-custom` | Shared ESLint rules | web, space |
| `packages/tailwind-config-custom` | `tailwind-config-custom` | Shared Tailwind config | web, space |
| `packages/tsconfig` | `tsconfig` | Shared TypeScript configs | all |

## @plane/ui — Component Library

**Build:** tsup (ESM/CJS bundles)
**Dependencies:** React 18, Blueprint.js, Headless UI, react-popper, react-color, lucide-react

### Exported Components

| Component | Props | Description |
|-----------|-------|-------------|
| Avatar | name, src, size, shape, fallbackText, showTooltip | User avatar with initials fallback |
| Breadcrumbs | children (BreadcrumbItem) | Navigation breadcrumbs |
| BreadcrumbItem | type, label, icon, link, component | Breadcrumb item |
| Button | variant, size, loading, disabled, prependIcon, appendIcon | Button with variants |
| ToggleSwitch | value, onChange, label, size | Boolean toggle |
| CustomMenu | label, placement, width, maxHeight, children (MenuItem) | Dropdown menu |
| CustomSelect | label, value, onChange, children (Option) | Select dropdown |
| CustomSearchSelect | label, value, onChange, options, searchable | Searchable select |
| Input | className, ...inputProps | Text input |
| Textarea | className, ...textareaProps | Multi-line text |
| InputColorPicker | value, onChange | Color picker (react-color) |
| Tooltip | tooltipContent, position, children | Hover tooltip |
| Loader | children | Loading placeholder |
| CircularSpinner | - | Spinner animation |
| ProgressBar | percentage, color | Linear progress |
| LinearProgressIndicator | data, noTooltip | Multi-segment progress |
| CircularProgressIndicator | percentage, size | Circular progress |
| RadialProgress | percentage, color, size | Radial progress |

### Icons (77 total)

Categories: State icons (backlog, completed, cancelled, started), Priority icons, Cycle icons, Module icons, General UI icons (archive, discord, github, etc.)

## @plane/editor-core — Editor Foundation

**Build:** tsup
**Base:** TipTap 2.1.7 (headless ProseMirror wrapper)

### TipTap Extensions
- StarterKit (base formatting)
- Color + TextStyle (text coloring)
- Image (with custom resize node view via react-moveable)
- Link (clickable links)
- Mention (@ mentions with suggestion system)
- Table + TableHeader + TableCell + TableRow
- TaskList + TaskItem (checklists)
- Underline
- Placeholder

### Exports
| Export | Purpose |
|--------|---------|
| `useEditor` | Hook for editable editor instance |
| `useReadOnlyEditor` | Hook for read-only viewer |
| `EditorContainer` | Styled wrapper component |
| `EditorContentWrapper` | Content area wrapper |
| `startImageUpload` | Image upload utility |
| Menu item helpers | Toolbar menu construction |

### Architecture
```
ui/hooks/          → useEditor, useReadOnlyEditor (custom TipTap hooks)
ui/extensions/     → Custom TipTap extensions (Image resize, Table)
ui/components/     → EditorContainer, EditorContent wrappers
ui/menus/          → Toolbar items, table context menu
ui/plugins/        → Image upload/delete handlers
ui/mentions/       → Mention list and suggestion system
```

## @plane/rich-text-editor

**Extends:** @plane/editor-core
**Additional Extensions:** Code block lowlight (syntax highlighting), horizontal rule, placeholder

### Exports
| Export | Purpose |
|--------|---------|
| `RichTextEditor` | Full editor component |
| `RichTextEditorWithRef` | Editor with forwarded ref |
| `RichReadOnlyEditor` | Read-only viewer |
| `RichReadOnlyEditorWithRef` | Read-only with ref |

**Use Case:** Issue descriptions, page content — anywhere full formatting is needed.

## @plane/lite-text-editor

**Extends:** @plane/editor-core
**Additional Extensions:** List item support

### Exports
| Export | Purpose |
|--------|---------|
| `LiteTextEditor` | Lightweight editor |
| `LiteTextEditorWithRef` | Editor with ref |
| `LiteReadOnlyEditor` | Read-only viewer |
| `LiteReadOnlyEditorWithRef` | Read-only with ref |

**Use Case:** Comments, quick text input — reduced feature set for performance.

## Configuration Packages

### eslint-config-custom
- Base: eslint-config-next (v13)
- Plugins: react (7.31.8), prettier
- Extends: eslint-config-turbo

### tailwind-config-custom
- PostCSS + autoprefixer
- Plugins: @tailwindcss/typography, tailwindcss-animate
- Custom color scheme: custom-background-*, custom-text-*, custom-border-*

### tsconfig
- `base.json` — Base TypeScript config
- `nextjs.json` — Next.js apps (web, space)
- `react-library.json` — React library packages (ui, editors)

## Build Pipeline

```
tsconfig ──────────────────────────┐
eslint-config-custom ──────────────┤
tailwind-config-custom ────────────┤
                                   ↓
editor-core ───→ rich-text-editor ─┤
           └───→ lite-text-editor ─┤
                                   ↓
ui ────────────────────────────────┤
                                   ↓
                         web, space (apps)
```
