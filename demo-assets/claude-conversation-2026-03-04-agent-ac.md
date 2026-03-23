# Claude Conversation Log

Session ID: agent-ac87d6c49a643248d
Date: 2026-03-04 01:08:39

---

## 👤 User

Research TWO topics for me. Be thorough.

## Topic 1: Sound Effects for a Snake Puzzle Game

I need to find or generate these specific sounds for a mobile snake puzzle game:

| Sound | Duration | Character |
|-------|----------|-----------|
| path_step | 50ms | Soft scale-slide tick |
| waypoint_eaten | 150ms | Round "pom" + subtle gulp |
| hint_reveal | 200ms | Soft sparkle/chime |
| completion | 500ms | Triumphant rising chord |
| button_tap | 30ms | Soft tap |
| undo | 60ms | Reverse pop/whoosh |
| invalid_move | 80ms | Dry "tsk" / tongue click |
| snake_hiss | 100ms | Soft hiss (idle tongue flick) |

Research:

1. **Free sound effect libraries** that have high-quality game sounds we can use (MIT/CC0/royalty-free):
   - freesound.org
   - OpenGameArt.org
   - Pixabay sounds
   - Kenney.nl
   - Zapsplat
   - Any others?

2. **AI sound generation tools** that can create these sounds:
   - Google's MusicFX / AudioFX (part of AI Test Kitchen)
   - ElevenLabs Sound Effects
   - Meta's AudioCraft/MusicGen
   - Stability AI's Stable Audio
   - Any CLI tools or APIs we can call programmatically?
   - Can Gemini models generate audio? Can Claude generate audio?

3. **Specifically search for**: snake game sound effects, puzzle game sound effects, satisfying UI sounds, "gulp" sound effect free, "scale slide" sound effect

4. For each source found, note: license, quality, format (mp3/wav/ogg), whether we can download directly

## Topic 2: Simulator Integration Tools / MCPs

Research whether there are MCP (Model Context Protocol) servers or CLI tools that can:

1. **Control iOS Simulator programmatically** — take screenshots, inspect UI, tap elements, get accessibility tree
2. **Control Android Emulator programmatically** — same capabilities
3. **Existing MCP servers** for mobile development:
   - Search for "MCP server iOS simulator"
   - Search for "MCP server Android emulator" 
   - Search for "MCP server mobile testing"
   - Search for "MCP server flutter"
4. **Flutter DevTools** — can it be controlled programmatically or via MCP?
5. **xcrun simctl** capabilities for iOS
6. **adb** capabilities for Android screenshots/UI inspection

List specific tools/MCPs found with installation instructions.

---

## 🤖 Claude



I'll research both topics thoroughly in parallel.

---

## 🤖 Claude

Now let me get a few more specific details to complete the research.

---

## 🤖 Claude

Now let me fetch some key pages for deeper detail.

---

## 🤖 Claude

I now have comprehensive information on both topics. Here is the full research report.

---

# TOPIC 1: Sound Effects for a Snake Puzzle Game

## Part 1: Free Sound Effect Libraries

### 1. Freesound.org
- **License:** Creative Commons (CC0, CC-BY, CC-BY-NC -- varies per sound; filter for CC0)
- **Quality:** Variable (community-contributed), but many professional-grade uploads
- **Format:** WAV, FLAC, OGG, MP3
- **Direct download:** Yes, after free registration
- **API:** Yes -- official Python client at [github.com/MTG/freesound-python](https://github.com/MTG/freesound-python). You can programmatically search and download sounds with an API key from [freesound.org/apiv2/apply](https://freesound.org/apiv2/apply/)
- **Relevant packs:** "Game Audio - UI SFX" by GameAudio ([freesound.org/people/GameAudio/packs/13940](https://freesound.org/people/GameAudio/packs/13940/))
- **Best for your needs:** Search for "gulp", "tick", "chime", "pop", "whoosh", "hiss" -- massive library with granular filtering by license

### 2. Kenney.nl
- **License:** CC0 (public domain) -- no attribution required, commercial use allowed
- **Quality:** High, consistent, game-ready
- **Format:** OGG and WAV (varies by pack)
- **Direct download:** Yes, free, no registration required
- **Relevant packs:**
  - [UI Audio](https://kenney.nl/assets/ui-audio) -- 50 files (button, switch, click sounds)
  - [Interface Sounds](https://kenney.nl/assets/interface-sounds) -- 100 files (click, button, interface sounds)
  - [Impact Sounds](https://kenney.nl/assets/impact-sounds) -- 130 files
  - [Digital Audio](https://kenney.nl/assets/digital-audio) -- 60 files (space/laser-themed, less relevant)
  - [RPG Audio](https://kenney.nl/assets/rpg-audio) -- 50 files
- **Best for:** `button_tap`, `path_step`, `undo` -- the UI Audio and Interface Sounds packs are excellent starting points

### 3. OpenGameArt.org
- **License:** CC0, CC-BY, GPL (varies per asset; filter for CC0)
- **Quality:** Variable, many good game-ready assets
- **Format:** Primarily WAV, some OGG
- **Direct download:** Yes, free, no registration required
- **Relevant packs:**
  - [51 UI sound effects (buttons, switches, clicks)](https://opengameart.org/content/51-ui-sound-effects-buttons-switches-and-clicks) -- 51 WAV files, all organic sounds, CC0
  - [UI Sound Effects (Button Clicks, User Feedback, Notifications)](https://opengameart.org/content/ui-sound-effects-button-clicks-user-feedback-notifications) -- CC0, public domain
  - [CC0 Sound Effects](https://opengameart.org/content/cc0-sound-effects) -- general CC0 pack
  - [GUI Sound Effects by Lokif](https://opengameart.org/content/gui-sound-effects) -- menu clicks, positive/negative sounds
  - [Interface Sounds](https://opengameart.org/content/interface-sounds) -- button clicks, snaps, confirmations

### 4. Pixabay Sounds
- **License:** Pixabay License -- free for commercial and non-commercial use, no attribution required. Cannot redistribute as standalone files.
- **Quality:** Good, curated
- **Format:** MP3
- **Direct download:** Yes, free, no registration required
- **Relevant searches:** [Snake game sounds](https://pixabay.com/sound-effects/search/snake%20game/), [commercial use sounds](https://pixabay.com/sound-effects/search/commercial%20use/)
- **Limitation:** MP3 only (no WAV), and you cannot redistribute the files as-is

### 5. Zapsplat
- **License:** Standard License (free tier) requires attribution. Premium membership removes attribution requirement.
- **Quality:** High, professional-grade, 150,000+ sounds
- **Format:** Free tier = MP3 only. Premium = WAV + MP3
- **Direct download:** Yes, after free registration
- **Relevant:** [Games and Puzzles category](https://www.zapsplat.com/sound-effect-category/games-and-puzzles/)
- **Limitation:** Attribution required on free tier; MP3 only on free tier

### 6. SONNISS GameAudioGDC
- **License:** Royalty-free, commercially usable, no attribution required
- **Quality:** Professional (contributed by AAA sound designers for GDC)
- **Format:** WAV (high quality)
- **Direct download:** Yes, but bundles are massive (27-44 GB per year)
- **Available at:** [sonniss.com/gameaudiogdc](https://sonniss.com/gameaudiogdc/)
- **Limitation:** Huge download size (~200GB total across all years). Best to download and search locally.

### 7. Mixkit
- **License:** Mixkit License -- free for commercial and personal use, no attribution required
- **Quality:** Good, curated
- **Format:** WAV and MP3
- **Direct download:** Yes, free, no registration
- **Relevant:** [Game sound effects](https://mixkit.co/free-sound-effects/game/)

### 8. Additional Sources
- **Uppbeat** ([uppbeat.io/sfx](https://uppbeat.io/sfx/category/gaming/game/puzzle-game)) -- Puzzle game SFX, free tier with attribution
- **SFX Engine** ([sfxengine.com](https://sfxengine.com/sound-effects/puzzle)) -- Royalty-free puzzle sounds, no credit card required
- **itch.io** ([itch.io CC0 SFX collection](https://itch.io/c/4003879/cc0-sfx-and-voices)) -- 4,000+ CC0 sound effects across various packs, including "Ultimate UI SFX Pack" by JDSherbert (67 unique sounds)
- **gamesounds.xyz** -- Mirrors of Kenney's Sound Pack and other game audio

---

## Part 2: AI Sound Generation Tools

### 1. ElevenLabs Sound Effects
- **URL:** [elevenlabs.io/sound-effects](https://elevenlabs.io/sound-effects)
- **API:** Yes -- [elevenlabs.io/developers](https://elevenlabs.io/developers). The Sound Effect V2 API (launched September 2025) supports 20+ second clips, seamless looping, and 48 kHz audio.
- **How it works:** Text-to-sound-effect. Describe the sound in natural language, get audio back.
- **Free tier:** 10,000 credits/month (~20 minutes of audio). Free tier is for non-commercial experimentation only.
- **Commercial use:** Requires paid plan (Starter at ~$5/month). Generated sounds are royalty-free on paid plans.
- **Format:** MP3/WAV output
- **Programmatic:** Full REST API. Python SDK available. Example: `POST /v1/sound-generation` with a text prompt.
- **Verdict:** Best option for programmatically generating custom sounds. You could generate all 8 of your sounds with precise text prompts like "short 50ms soft tick sound, scale sliding" or "150ms round pom gulp sound effect for eating".

### 2. Meta AudioCraft / AudioGen
- **URL:** [github.com/facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft)
- **API:** Python library, no hosted API (self-hosted only)
- **How it works:** AudioGen is the text-to-sound-effect model; MusicGen is the text-to-music model. Both run locally.
- **License:** MIT license for code; model weights have separate research licenses
- **Requirements:** Python 3.9+, PyTorch 2.1.0+, ffmpeg, GPU recommended (CUDA)
- **Installation:**
  ```bash
  pip install -U audiocraft
  ```
- **Usage:**
  ```python
  from audiocraft.models import AudioGen
  model = AudioGen.get_pretrained('facebook/audiogen-medium')
  model.set_generation_params(duration=0.5)
  wav = model.generate(['soft tick sound, scale sliding on a surface'])
  ```
- **Verdict:** Free and open-source, runs locally, but requires a GPU for reasonable speed. Good for batch-generating many variations.

### 3. Stability AI / Stable Audio
- **URL:** [stableaudio.com](https://www.stableaudio.com/) and [stability.ai/stable-audio](https://stability.ai/stable-audio)
- **API:** Available via [Replicate](https://replicate.com/stability-ai/stable-audio-2.5) and the Stability AI platform
- **Open-source option:** Stable Audio Open ([stabilityai/stable-audio-open-1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0)) is optimized for short audio samples and sound effects
- **Free tier:** Limited free generations on stableaudio.com
- **Installation (open-source):**
  ```bash
  pip install stable-audio-tools
  ```
- **Verdict:** Good for sound effects. The open-source model is specifically designed for short audio and production elements.

### 4. Google MusicFX / Lyria
- **URL:** [labs.google/fx/tools/music-fx-dj](https://labs.google/fx/tools/music-fx-dj)
- **API:** No public API. Web-based only through Google Labs.
- **How it works:** Text-to-music, powered by Lyria and Lyria RealTime (Google DeepMind). Generates up to 70-second clips.
- **Availability:** US, New Zealand, Kenya, Australia only
- **Limitation:** Primarily designed for music, not short sound effects. No programmatic access.
- **Verdict:** Not suitable for your use case -- no API, music-focused, geographic restrictions.

### 5. Gemini Audio Generation
- **Can Gemini generate audio?** Yes. Gemini 2.5 Pro Preview has native text-to-speech capabilities. Lyria 3 is Gemini's music generator that creates 30-second tracks from text prompts. Gemini can generate spoken audio but is not designed for short SFX generation.
- **API:** Available via Firebase AI Logic / Google AI Studio
- **Verdict:** Better for speech and music than for short game sound effects.

### 6. Can Claude Generate Audio?
- **No.** Claude cannot directly generate audio files. Claude can:
  - Write Python code that uses libraries like `scipy`, `numpy`, or `pydub` to synthesize sounds programmatically (sine waves, noise, etc.)
  - Generate MIDI files via code
  - Write Lilypond notation for sheet music
  - Help craft prompts for other AI audio tools
- **Verdict:** Claude can help you write a Python script to synthesize simple sounds (clicks, pops, tones), but cannot produce audio files natively.

### 7. Other AI/Programmatic Sound Tools
- **Suno** ([suno.com](https://suno.com)) -- API available, but focused on full songs, not short SFX
- **Soundverse** ([soundverse.ai](https://www.soundverse.ai)) -- Enterprise-grade music generation API
- **sfxr / jsfxr** ([sfxr.me](https://sfxr.me/)) -- Classic retro sound effect generator. Open source. Generates 8-bit/retro sounds. Has a web version and CLI. Great for "button_tap", "undo", "invalid_move" type sounds.

---

## Part 3: Specific Sound Mapping Recommendations

Here is where I would source each of your 8 sounds:

| Sound | Recommended Source | Search Terms / Approach |
|-------|-------------------|------------------------|
| `path_step` (50ms) | Kenney UI Audio or ElevenLabs API | "soft click", "light tap", "slide tick" |
| `waypoint_eaten` (150ms) | ElevenLabs API or Freesound | "bubble pop gulp", "soft pom eating sound" |
| `hint_reveal` (200ms) | Kenney Interface Sounds or Freesound | "sparkle chime", "magic reveal", "twinkle" |
| `completion` (500ms) | Freesound or ElevenLabs API | "triumphant chord", "level complete fanfare", "victory rising chord" |
| `button_tap` (30ms) | Kenney UI Audio (CC0, ready to use) | Already has perfect button click sounds |
| `undo` (60ms) | Freesound or ElevenLabs API | "reverse pop", "short whoosh back", "rewind pop" |
| `invalid_move` (80ms) | OpenGameArt or Freesound | "error buzz", "tongue click tsk", "deny sound" |
| `snake_hiss` (100ms) | Freesound or Pixabay | "short snake hiss", "tongue flick", "soft serpent" |

---

# TOPIC 2: Simulator Integration Tools / MCPs

## 1. iOS Simulator MCP Servers

### A. mobile-mcp (mobile-next) -- RECOMMENDED, Cross-Platform
- **URL:** [github.com/mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)
- **Platforms:** iOS Simulator + Android Emulator + Real Devices (both platforms)
- **Installation for Claude Code:**
  ```bash
  claude mcp add mobile -- npx -y @mobilenext/mobile-mcp@latest
  ```
- **Prerequisites:** Node.js v22+, Xcode command line tools (iOS), Android Platform Tools (Android)
- **Tools provided:**
  - `mobile_list_available_devices` -- enumerate simulators/emulators/devices
  - `mobile_take_screenshot` -- capture current screen
  - `mobile_save_screenshot` -- save screenshot to disk
  - `mobile_list_elements_on_screen` -- extract UI elements with coordinates (accessibility tree)
  - `mobile_click_on_screen_at_coordinates` -- tap at x,y
  - `mobile_double_tap_on_screen` -- double-tap gesture
  - `mobile_long_press_on_screen_at_coordinates` -- long press
  - `mobile_swipe_on_screen` -- directional swipes
  - `mobile_type_keys` -- text input
  - `mobile_press_button` -- HOME, BACK, VOLUME, ENTER
  - `mobile_open_url` -- launch URLs
  - `mobile_launch_app` / `mobile_terminate_app` / `mobile_install_app` / `mobile_uninstall_app` -- app lifecycle
  - `mobile_get_screen_size` / `mobile_get_orientation` / `mobile_set_orientation` -- display management
- **Verdict:** Best all-in-one option. Works with both iOS and Android. Active development. Official Claude Code integration guide available.

### B. ios-simulator-mcp (Joshua Yoes)
- **URL:** [github.com/joshuayoes/ios-simulator-mcp](https://github.com/joshuayoes/ios-simulator-mcp)
- **Platform:** iOS Simulator only
- **Installation:**
  ```json
  {
    "mcpServers": {
      "ios-simulator": {
        "command": "npx",
        "args": ["-y", "ios-simulator-mcp"]
      }
    }
  }
  ```
- **Prerequisites:** Node.js, macOS, Xcode with iOS simulators, Facebook IDB (iOS Development Bridge)
- **Tools provided:**
  - `get_booted_sim_id` -- get ID of booted simulator
  - `open_simulator` -- open the Simulator app
  - `ui_describe_all` -- describe accessibility info for entire screen
  - `ui_describe_point` -- accessibility element at coordinates
  - `ui_tap` / `ui_swipe` / `ui_type` -- UI interaction
  - `ui_view` -- compressed screenshot
  - `screenshot` -- full screenshot
  - `record_video` / `stop_recording` -- video capture
  - `install_app` / `launch_app` -- app management
- **Verdict:** iOS-specific, good accessibility tree support via `ui_describe_all`.

### C. iosef (riwsky) -- Swift-native, High Performance
- **URL:** [github.com/riwsky/iosef](https://github.com/riwsky/iosef)
- **Platform:** iOS Simulator only
- **Installation:**
  ```bash
  uv tool install iosef
  # or
  pip install iosef
  # or
  uvx iosef --help
  ```
- **MCP Configuration:**
  ```json
  {
    "mcpServers": {
      "iosef": {
        "command": "iosef",
        "args": ["mcp"]
      }
    }
  }
  ```
- **Prerequisites:** macOS 13+, Xcode with iOS simulator runtime, Swift 6.1+ (only if building from source)
- **Tools provided:**
  - Session management (start/stop simulators, connect to devices)
  - UI inspection (accessibility trees, screenshots, element queries by depth)
  - Interaction (tap, type, swipe, long-press)
  - Queries (find elements, check existence, count matches, extract text, wait for elements)
  - App control (install, launch, terminate)
  - Logging (recent logs, live streaming with filters)
- **Verdict:** Written in Swift for performance. Consistent coordinate space. Every CLI subcommand is also an MCP tool. Good for agents that need to "see and tap."

### D. mcp-server-simulator-ios-idb (InditexTech)
- **URL:** [github.com/InditexTech/mcp-server-simulator-ios-idb](https://github.com/InditexTech/mcp-server-simulator-ios-idb)
- **Platform:** iOS Simulator only
- **Installation:** Clone repo, create Python venv, `npm install`, `npm run build`, `npm start`. Auto-installs `idb-companion` via Homebrew and `fb-idb` via pip.
- **Prerequisites:** macOS, Xcode, Node.js v14+
- **Features:** Natural language parsing, session management, app install/launch, UI interactions, accessibility queries, screenshots, location simulation, media injection, URL handling, keychain operations
- **Verdict:** Rich feature set (location simulation, keychain operations) but more complex setup.

## 2. Android Emulator MCP Servers

### A. mobile-mcp (same as above -- cross-platform)
See section 1A above. Covers Android emulators and real devices.

### B. Android-Ui-MCP (infiniV)
- **URL:** [github.com/infiniV/Android-Ui-MCP](https://github.com/infiniV/Android-Ui-MCP)
- **Platform:** Android (supports Flutter, React Native, native Android)
- **Installation:** Docker-based. `docker build` and `docker run` with device mounting.
- **Features:** Real-time UI analysis via screenshots, device management, AI-powered UI feedback
- **Verdict:** Good for Flutter developers specifically. Provides AI-powered UI improvement suggestions.

### C. android-mcp-server (minhalvp)
- **URL:** [github.com/minhalvp/android-mcp-server](https://github.com/minhalvp/android-mcp-server)
- **Platform:** Android via ADB
- **Features:** Control over Android devices via adb

### D. adb-mcp (srmorete)
- **URL:** [github.com/srmorete/adb-mcp](https://github.com/srmorete/adb-mcp)
- **Platform:** Android via ADB (TypeScript)
- **Features:** MCP server for interacting with Android devices through ADB

### E. mcp-android-emulator (Anjos2)
- **URL:** [github.com/Anjos2/mcp-android-emulator](https://github.com/Anjos2/mcp-android-emulator)
- **Platform:** Android Emulator
- **Features:** AI assistants can control Android emulator devices

## 3. Flutter-Specific MCP Servers

### A. Official Dart and Flutter MCP Server -- RECOMMENDED
- **URL:** [docs.flutter.dev/ai/mcp-server](https://docs.flutter.dev/ai/mcp-server)
- **Blog post:** [Flutter blog announcement](https://blog.flutter.dev/supercharge-your-dart-flutter-development-experience-with-the-dart-mcp-server-2edcc8107b49)
- **Requirements:** Dart 3.9+ / Flutter 3.35+ (beta channel as of early 2026)
- **Installation for Claude Code:**
  ```bash
  claude mcp add --transport stdio dart -- dart mcp-server
  ```
- **Capabilities:**
  - Analyze and fix errors in project code
  - Resolve symbols and fetch documentation
  - Introspect and interact with running Flutter app (hot reload, get selected widget, fetch runtime errors)
  - Search pub.dev for packages
  - Manage pubspec.yaml dependencies
  - Run tests and analyze results
  - Format code
  - Inspect widget tree for layout debugging
- **Verdict:** The official solution from the Flutter team. Best for code-level interaction with your Flutter project. Experimental but rapidly evolving.

### B. mcp_flutter (Arenukvern) -- Flutter Inspector
- **URL:** [github.com/Arenukvern/mcp_flutter](https://github.com/Arenukvern/mcp_flutter)
- **Features:** Widget tree inspection, debugging, performance monitoring, error analysis, dynamic tooling
- **Verdict:** Good complement to the official server for runtime inspection.

### C. DCM MCP Server
- **URL:** [dcm.dev/docs/ide-integrations/mcp-server](https://dcm.dev/docs/ide-integrations/mcp-server)
- **Installation:**
  ```bash
  claude mcp add --transport stdio dcm -- dcm start-mcp-server --client=claude-code
  ```
- **Features:** Code quality tooling for Flutter -- lint rules, metrics, anti-pattern detection
- **Verdict:** Complementary tool for code quality, not UI inspection.

## 4. Raw CLI Tools (No MCP Required)

### xcrun simctl (iOS)
- **Screenshot:** `xcrun simctl io booted screenshot output.png`
- **Video recording:** `xcrun simctl io booted recordVideo output.mp4`
- **List devices:** `xcrun simctl list devices`
- **Boot simulator:** `xcrun simctl boot <device-id>`
- **Install app:** `xcrun simctl install booted /path/to/app.app`
- **Launch app:** `xcrun simctl openurl booted "myapp://"`
- **Screenshot formats:** PNG (default), TIFF, BMP, GIF, JPEG
- **Options:** `--type=jpeg`, `--mask=black`
- **Accessibility:** Modify `com.apple.Accessibility.plist` to enable/disable VoiceOver. Use Xcode's Accessibility Inspector for tree inspection.

### adb (Android)
- **Screenshot:** `adb exec-out screencap -p > screenshot.png`
- **UI hierarchy dump:** `adb shell uiautomator dump` (outputs to `/sdcard/window_dump.xml`)
- **Direct stdout dump:** `adb exec-out uiautomator dump /dev/tty`
- **Pull dump file:** `adb pull /sdcard/window_dump.xml .`
- **Tap:** `adb shell input tap <x> <y>`
- **Swipe:** `adb shell input swipe <x1> <y1> <x2> <y2>`
- **Type text:** `adb shell input text "hello"`
- **List devices:** `adb devices`
- **Install app:** `adb install app.apk`
- **Accessibility settings:** `adb shell settings put secure enabled_accessibility_services <service>`

## 5. Recommended Setup for Your ZipPath Project

For a Flutter project targeting both iOS and Android, I recommend this MCP configuration:

```bash
# 1. Cross-platform simulator/emulator control
claude mcp add mobile -- npx -y @mobilenext/mobile-mcp@latest

# 2. Official Flutter development tools (requires Dart 3.9+)
claude mcp add --transport stdio dart -- dart mcp-server

# 3. (Optional) iOS-specific with better accessibility tree
# Choose ONE of these if you need deeper iOS inspection:
# Option A: Swift-native, fast
# uv tool install iosef
# claude mcp add iosef -- iosef mcp
# Option B: Node.js-based
# claude mcp add ios-sim -- npx -y ios-simulator-mcp
```

This gives you:
- Screenshot capture on both platforms
- UI element inspection / accessibility tree reading
- Tap, swipe, type interactions
- App install and launch
- Flutter code analysis, hot reload, widget tree inspection, test running

---

Sources:
- [Freesound](https://freesound.org/)
- [Freesound Python Client](https://github.com/MTG/freesound-python)
- [Kenney Audio Assets](https://kenney.nl/assets/category:Audio)
- [OpenGameArt CC0 Sound Effects](https://opengameart.org/content/cc0-sound-effects)
- [OpenGameArt 51 UI Sound Effects](https://opengameart.org/content/51-ui-sound-effects-buttons-switches-and-clicks)
- [Pixabay Sound Effects](https://pixabay.com/sound-effects/)
- [Pixabay License](https://pixabay.com/service/license-summary/)
- [Zapsplat](https://www.zapsplat.com/)
- [SONNISS GameAudioGDC](https://sonniss.com/gameaudiogdc/)
- [Mixkit Sound Effects](https://mixkit.co/free-sound-effects/game/)
- [Uppbeat Puzzle Game SFX](https://uppbeat.io/sfx/category/gaming/game/puzzle-game)
- [itch.io CC0 SFX](https://itch.io/c/4003879/cc0-sfx-and-voices)
- [ElevenLabs Sound Effects](https://elevenlabs.io/sound-effects)
- [ElevenLabs API](https://elevenlabs.io/developers)
- [ElevenLabs Pricing](https://elevenlabs.io/pricing)
- [Meta AudioCraft (GitHub)](https://github.com/facebookresearch/audiocraft)
- [AudioCraft Homepage](https://audiocraft.metademolab.com/)
- [Stable Audio](https://www.stableaudio.com/)
- [Stable Audio Open (Hugging Face)](https://huggingface.co/stabilityai/stable-audio-open-1.0)
- [Google MusicFX](https://labs.google/fx/tools/music-fx-dj)
- [Gemini Audio Generation](https://firebase.google.com/docs/ai-logic/generate-audio)
- [mobile-mcp (GitHub)](https://github.com/mobile-next/mobile-mcp)
- [mobile-mcp Claude Code Setup](https://github.com/mobile-next/mobile-mcp/wiki/Getting-Started-with-Claude-Code)
- [ios-simulator-mcp (GitHub)](https://github.com/joshuayoes/ios-simulator-mcp)
- [iosef (GitHub)](https://github.com/riwsky/iosef)
- [InditexTech iOS IDB MCP](https://github.com/InditexTech/mcp-server-simulator-ios-idb)
- [Android-Ui-MCP (GitHub)](https://github.com/infiniV/Android-Ui-MCP)
- [android-mcp-server (GitHub)](https://github.com/minhalvp/android-mcp-server)
- [adb-mcp (GitHub)](https://github.com/srmorete/adb-mcp)
- [Official Dart/Flutter MCP Server Docs](https://docs.flutter.dev/ai/mcp-server)
- [Flutter Blog: Dart MCP Server](https://blog.flutter.dev/supercharge-your-dart-flutter-development-experience-with-the-dart-mcp-server-2edcc8107b49)
- [mcp_flutter Inspector (GitHub)](https://github.com/Arenukvern/mcp_flutter)
- [DCM MCP Server](https://dcm.dev/docs/ide-integrations/mcp-server)
- [MCP Servers for Dart/Flutter 2026 Guide](https://voxturrlabs.com/blog/mcp-servers-for-dart-and-flutter-developers-2026/)
- [xcrun simctl Guide (NSHipster)](https://nshipster.com/simctl/)
- [ADB Accessibility Commands](https://alexzh.com/adb-commands-accessibility/)
- [Top 10 AI SFX Generators 2025](https://www.devopsschool.com/blog/top-10-ai-sound-effects-generators-tools-in-2025-features-pros-cons-comparison/)

---

