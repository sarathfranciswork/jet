---
name: generate-app-icons
description: Generate production-ready app icons for all platforms (iOS, Android, macOS, Windows, Web/PWA, Electron) from a source image or AI-generated design. Supports both source image resizing and Nano Banana AI generation.
user_invocable: true
---

# Generate App Icons

Generate production-ready app icons for all platforms from a source image or AI prompt.

## Usage

```
/generate-app-icons
```

The skill will ask for:
1. **Source**: A path to a high-res PNG (1024x1024+) OR an AI prompt to generate one
2. **Output directory**: Where to save the generated icons
3. **Platforms**: Which platforms to generate for (default: all)
