# Component Inventory - Shared Packages

**Generated:** 2026-03-18

## @plane/ui Components

### Layout & Navigation

| Component | Props | Description |
|-----------|-------|-------------|
| Breadcrumbs | `children: BreadcrumbItem[]` | Navigation breadcrumb trail with chevron separators |
| BreadcrumbItem | `type: "text"\|"component", label, icon, link, component` | Individual breadcrumb segment |

### Buttons & Controls

| Component | Props | Description |
|-----------|-------|-------------|
| Button | `variant, size (sm\|md\|lg), loading, disabled, prependIcon, appendIcon` | Primary button with variants |
| ToggleSwitch | `value, onChange, label, size` | Boolean toggle switch |

### Dropdowns & Selection

| Component | Props | Description |
|-----------|-------|-------------|
| CustomMenu | `label, placement, width, maxHeight, disabled, ellipsis, customButton, children` | Dropdown menu with MenuItem children |
| CustomSelect | `label, value, onChange, children (Option)` | Select dropdown |
| CustomSearchSelect | `label, value, onChange, options, searchable` | Searchable select with filtering |

### Form Inputs

| Component | Props | Description |
|-----------|-------|-------------|
| Input | `className, ...HTMLInputElement` | Styled text input |
| Textarea | `className, ...HTMLTextAreaElement` | Multi-line text input |
| InputColorPicker | `value, onChange` | Color picker using react-color |

### Display & Feedback

| Component | Props | Description |
|-----------|-------|-------------|
| Avatar | `name, src, size (sm\|md\|base\|lg\|number), shape (circle\|square), fallbackText, fallbackBackgroundColor, showTooltip` | User avatar with initials fallback |
| Tooltip | `tooltipContent, position, children` | Hover tooltip |
| Loader | `children` | Loading placeholder skeleton |
| CircularSpinner | - | Animated spinner |

### Progress Indicators

| Component | Props | Description |
|-----------|-------|-------------|
| ProgressBar | `percentage, color` | Simple linear progress bar |
| LinearProgressIndicator | `data: {name, color, percentage}[], noTooltip` | Multi-segment progress bar |
| CircularProgressIndicator | `percentage, size` | Circular progress ring |
| RadialProgress | `percentage, color, size` | Radial progress indicator |

### Icons (77 total)

#### State Group Icons
BacklogStateIcon, UnstartedStateIcon, StartedStateIcon, CompletedStateIcon, CancelledStateIcon

#### Priority Icons
UrgentPriorityIcon, HighPriorityIcon, MediumPriorityIcon, LowPriorityIcon, NonePriorityIcon

#### Cycle & Module Icons
ContrastIcon, PeopleGroupIcon, DiceIcon, PhotoFilterIcon

#### General UI Icons
ArchiveIcon, AttachmentIcon, BlockedIcon, BlockerIcon, ClipboardIcon, CommentIcon, DiscordIcon, GithubIcon, LayerDiagonalIcon, PencilIcon, StackedLayersIcon, UserGroupIcon, ViewListIcon, and 50+ more

---

## @plane/editor-core Exports

| Export | Type | Description |
|--------|------|-------------|
| useEditor | Hook | Creates editable TipTap editor instance |
| useReadOnlyEditor | Hook | Creates read-only TipTap viewer |
| EditorContainer | Component | Styled editor wrapper with border/padding |
| EditorContentWrapper | Component | Content area wrapper |
| startImageUpload | Function | Handles image upload flow |
| getEditorClassNames | Function | Returns editor CSS class names |
| IMentionHighlight | Type | Mention highlight interface |
| IMentionSuggestion | Type | Mention suggestion interface |

### TipTap Extensions Included
- StarterKit (bold, italic, strike, code, headings, lists, blockquote)
- Color + TextStyle
- Custom Image extension (with resize via react-moveable)
- Link (auto-link, open on click)
- Mention (with suggestion popup)
- Table + TableHeader + TableCell + TableRow
- TaskList + TaskItem
- Underline
- Placeholder

---

## @plane/rich-text-editor Exports

| Export | Type | Description |
|--------|------|-------------|
| RichTextEditor | Component | Full-featured rich text editor |
| RichTextEditorWithRef | Component | Editor with forwarded ref |
| RichReadOnlyEditor | Component | Read-only content viewer |
| RichReadOnlyEditorWithRef | Component | Read-only with forwarded ref |

**Additional Extensions:** CodeBlockLowlight (syntax highlighting), HorizontalRule, Placeholder

---

## @plane/lite-text-editor Exports

| Export | Type | Description |
|--------|------|-------------|
| LiteTextEditor | Component | Lightweight text editor |
| LiteTextEditorWithRef | Component | Editor with forwarded ref |
| LiteReadOnlyEditor | Component | Read-only viewer |
| LiteReadOnlyEditorWithRef | Component | Read-only with forwarded ref |

**Additional Extensions:** ListItem (basic list support)

---

## Configuration Packages

### eslint-config-custom
- Extends: eslint-config-next, eslint-config-turbo
- Plugins: react, prettier
- Shared across all packages and apps

### tailwind-config-custom
- PostCSS + autoprefixer
- Plugins: @tailwindcss/typography, tailwindcss-animate
- Custom color variables: custom-background-*, custom-text-*, custom-border-*
- Shared by web and space apps

### tsconfig
| Config | Used By | Key Settings |
|--------|---------|-------------|
| base.json | All | Base TypeScript settings |
| nextjs.json | web, space | Next.js specific (JSX preserve, module resolution) |
| react-library.json | ui, editors | React library compilation (declaration files) |
