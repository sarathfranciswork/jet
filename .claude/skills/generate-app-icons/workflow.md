# App Icon Generator Workflow

**Goal:** Generate production-ready app icons for all platforms from a source image or AI-generated design.

## Instructions

When this skill is invoked:

1. **Determine the source** — Ask the user (or use arguments) for one of:
   - `--source <path>` — A high-resolution PNG image (1024x1024 or larger)
   - `--prompt "<description>"` — Text prompt for AI generation via Nano Banana
   - `--reference <path> --prompt "<description>"` — Reference image + prompt for AI refinement
   - If no arguments, ask the user which approach they prefer

2. **Determine output directory** — Default: `./app-icons/` in the project root. Can be overridden with `--output <dir>`.

3. **Determine platforms** — Default: all. Can be filtered with `--platforms ios,android,macos,windows,web,electron`.

4. **Run the generator script** — Execute `node <skill-dir>/generate-icons.js` with the appropriate arguments. The script handles:
   - Source image validation and preparation (crop to square, scale to 1024x1024)
   - For AI mode: calls Gemini API with Nano Banana 2 Pro to generate a 1024x1024 icon
   - Resizing to all required sizes per platform
   - Generating platform-specific formats (ICNS, ICO, favicon.ico)
   - Creating metadata files (Contents.json for iOS, mipmap structure for Android, webmanifest for PWA)

5. **Report results** — Show the user what was generated, organized by platform.

## Dependencies

The script requires these npm packages (installed automatically if missing):
- `sharp` — Image processing and resizing
- `sharp-ico` — ICO file generation
- `png2icons` — ICNS file generation

For AI generation mode:
- `GOOGLE_AI_API_KEY` environment variable must be set
- Uses `gemini-2.5-flash-preview-image` model (Nano Banana 2)

## Platform Output Structure

```
<output-dir>/
├── ios/
│   └── AppIcon.appiconset/
│       ├── Contents.json
│       └── icon-*.png (all required sizes)
├── android/
│   ├── mipmap-mdpi/ic_launcher.png
│   ├── mipmap-hdpi/ic_launcher.png
│   ├── mipmap-xhdpi/ic_launcher.png
│   ├── mipmap-xxhdpi/ic_launcher.png
│   ├── mipmap-xxxhdpi/ic_launcher.png
│   └── playstore-icon.png (512x512)
├── macos/
│   ├── icon.icns
│   └── icon.iconset/ (all sizes)
├── windows/
│   └── icon.ico (multi-size)
├── web/
│   ├── favicon.ico
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── apple-touch-icon.png (180x180)
│   ├── icon-192x192.png
│   ├── icon-512x512.png
│   ├── site.webmanifest
│   └── browserconfig.xml
├── electron/
│   ├── icon.icns
│   ├── icon.ico
│   ├── icon.png (512x512)
│   ├── tray-icon.png (22x22)
│   ├── tray-icon@2x.png (44x44)
│   ├── tray-iconTemplate.png (22x22)
│   └── tray-iconTemplate@2x.png (44x44)
└── source.png (1024x1024 master)
```
