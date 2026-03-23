# Claude Conversation Log

Session ID: agent-a1b4f05579b03a736
Date: 2026-03-04 14:00:34

---

## 👤 User

Research the current best practices (as of March 2026) for automated Flutter app deployment to Google Play Store and Apple App Store. The user has:
- Google Play Console account: sarathfrancis90@gmail.com
- Apple Developer account: sarathfrancis90@icloud.com
- GitHub repository for the project
- Flutter app targeting iOS and Android

Research:
1. **GitHub Actions + Fastlane** - Is this still the recommended approach? What are the latest workflows?
2. **Shorebird** (code push) - Is this mature enough for production?
3. **Codemagic** vs **GitHub Actions** - Pros/cons for Flutter deployment
4. **Google Play** - Service account setup, app signing, internal/alpha/beta/production tracks
5. **App Store Connect** - API keys, certificates, provisioning profiles, TestFlight
6. **App signing** - Play App Signing, Apple certificates management
7. **Fastlane** - Latest version, match for iOS signing, supply for Android
8. **Flutter build commands** - Latest flags for release builds (--obfuscate, --split-debug-info, etc.)

Provide a concrete plan with the exact tools, config files, and steps needed. Research this online for the most current information.

---

## 🤖 Claude



I'll research the current best practices for Flutter app deployment as of March 2026 across all the areas you've specified.

---

## 🤖 Claude

Now let me check the existing project structure to understand what's already in place.

---

## 🤖 Claude

Now I have a comprehensive picture. Let me compile the complete research findings.

---

# Flutter App Deployment Research: Comprehensive Plan for ZipPath (March 2026)

## 1. GitHub Actions + Fastlane: Still the Recommended Approach

**Verdict: Yes, this remains the gold standard for Flutter CI/CD in 2026.**

The combination of GitHub Actions (CI orchestration) + Fastlane (build/sign/deploy automation) is the most widely adopted and documented approach for Flutter app deployment. The Flutter team's own [official documentation on Continuous Delivery](https://docs.flutter.dev/deployment/cd) continues to recommend this combination.

**Current Fastlane version:** 2.232.1 (released February 10, 2026), compatible with Ruby 2.5+ through Ruby 3.4.

### Why this stack works best for your project:
- You already have a GitHub repository (no extra CI service needed)
- Fastlane handles the complex signing/uploading logic that would otherwise require hundreds of lines of shell scripts
- Mature ecosystem with thousands of plugins
- Community support is strongest for this combination

---

## 2. Shorebird Code Push: Production Ready, But Use as a Supplement

**Verdict: Yes, production-ready. Use it for hotfixes, not as a replacement for store releases.**

Shorebird had a strong 2025 -- over 16,000 new signups, doubled paid subscribers, and hundreds of millions of patches deployed globally across Android, iOS, Mac, Windows, and Linux ([Shorebird 2025 Year in Review](https://shorebird.dev/blog/2025-year-in-review)).

### How it works:
- Apps built with Shorebird include a modified Flutter engine
- On startup, the engine checks for Dart code patches
- If available, downloads the patch; user sees it on next restart
- Only patches Dart code (runs in Dart VM), NOT native code

### App Store compliance:
- **Apple**: Compliant because Dart runs in a VM. Apple's policy permits interpreted code updates as long as you don't "change the primary purpose of the Application"
- **Google**: Compliant. Google permits OTA updates for interpreted/VM-based code

### Recommendation for ZipPath:
- **Do NOT use Shorebird as your primary deployment mechanism**
- **DO integrate it** for emergency bugfixes (e.g., a broken puzzle engine after a release)
- Continue full store releases as your standard pipeline
- Shorebird pricing has a free Hobby tier; paid plans scale with patch installs

### Integration point:
Add Shorebird later (post-launch) as a Story in Sprint 3+. It requires wrapping your build with `shorebird release` instead of `flutter build`, and adding the `shorebird_code_push` package.

---

## 3. Codemagic vs GitHub Actions: Comparison

| Factor | GitHub Actions | Codemagic |
|--------|---------------|-----------|
| **Setup complexity** | Higher (YAML config, manual signing setup) | Lower (visual UI, auto-signing) |
| **Flutter focus** | General-purpose CI | Purpose-built for Flutter |
| **iOS code signing** | Manual (Fastlane match or manual certs) | Automatic (connects to ASC API directly) |
| **Cost (free tier)** | 2,000 min/mo Linux, 300 min/mo macOS (10x multiplier) | ~500 build min/mo free |
| **macOS runner cost** | $0.08/min ($4.80/hr) | Included in plans |
| **Self-hosted runners** | Supported (new $0.002/min charge from March 2026) | Not applicable |
| **Ecosystem** | 20,000+ marketplace actions | Flutter-specific integrations |
| **Vendor lock-in** | Low (standard YAML) | Medium (Codemagic-specific config) |

**Recommendation for ZipPath: GitHub Actions + Fastlane.**

Reasons:
1. Your code is already on GitHub -- zero friction
2. Fastlane gives you portable automation that works locally and in CI
3. You learn transferable skills (Fastlane is industry standard)
4. The macOS minute cost is manageable for a single-app project (a Flutter iOS build typically takes 10-15 minutes, so ~$0.80-$1.20 per build)
5. Codemagic's advantage is mainly for teams that want zero-config signing, but Fastlane match handles this well

---

## 4. Google Play Store: Setup Plan

### Step 4A: Create a Service Account (for automated uploads)

1. Go to [Google Cloud Console](https://console.cloud.google.com) > IAM & Admin > Service Accounts
2. Create a new service account named `zippath-ci-deploy`
3. Click Actions > Manage keys > Add Key > Create new key > JSON format
4. Download the JSON file (this is your `play-store-credentials.json`)
5. Go to [Google Play Console](https://play.google.com/console) > Settings > API access
6. Link the Google Cloud project
7. Grant the service account "Release manager" permissions
8. **IMPORTANT**: Wait 24 hours for credentials to propagate

### Step 4B: App Signing Setup

1. **Generate upload keystore:**
```bash
keytool -genkey -v \
  -keystore ~/upload-keystore.jks \
  -keyalg RSA -keysize 2048 \
  -validity 10000 \
  -alias upload
```

2. **Create `android/key.properties`** (do NOT commit this):
```properties
storePassword=<password>
keyPassword=<password>
keyAlias=upload
storeFile=/path/to/upload-keystore.jks
```

3. **Configure `android/app/build.gradle.kts`** to use the signing config:
```kotlin
// Add before android { block
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    // ... existing config ...
    
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

4. **Enroll in Play App Signing** when you upload the first AAB to Play Console
5. **2026 requirement**: `targetSdk = 35` (Android 15) -- mandatory since August 2025

### Step 4C: Release Tracks

| Track | Purpose | Review time |
|-------|---------|-------------|
| Internal testing | Team testing, up to 100 testers | Instant |
| Closed testing (Alpha) | Limited external testers | ~Hours |
| Open testing (Beta) | Public beta | ~Hours |
| Production | Full release | 1-7 days |

**Recommended flow**: Internal testing -> Closed testing -> Production (skip open testing for a puzzle game)

---

## 5. Apple App Store Connect: Setup Plan

### Step 5A: App Store Connect API Key

1. Go to [App Store Connect](https://appstoreconnect.apple.com) > Users and Access > Integrations > App Store Connect API
2. Click "+" to generate a new key
3. Name: `zippath-ci`
4. Access: "App Manager"
5. Download the `.p8` file (you can only download it ONCE)
6. Note the **Key ID** and **Issuer ID** displayed on the page

### Step 5B: Certificates & Provisioning Profiles (Fastlane Match)

Fastlane Match stores certificates and profiles in a **private Git repository**, encrypted with a passphrase.

1. **Create a private GitHub repo**: `zippath-certificates` (under your account)
2. **Initialize match**:
```bash
cd ios
fastlane match init
# Choose option 1: git
# Enter repo URL: git@github.com:sarathfrancis/zippath-certificates.git
```

3. **Generate certificates**:
```bash
fastlane match appstore    # Distribution certificate + App Store profile
fastlane match development # Development certificate + Dev profile
```

4. **For CI**, set these environment variables:
   - `MATCH_PASSWORD` -- passphrase to decrypt the certificates repo
   - `MATCH_GIT_BASIC_AUTHORIZATION` -- base64-encoded `username:token` for Git auth

### Step 5C: TestFlight

TestFlight is integrated into App Store Connect. Your CI pipeline uploads to TestFlight automatically via `fastlane deliver` or `fastlane pilot`.

- Internal testers: Up to 100, instant access
- External testers: Up to 10,000, requires beta review (usually < 24 hours)

---

## 6. App Signing Details

### Android: Play App Signing
- Google holds the **app signing key** (the one that signs the final APK delivered to users)
- You hold the **upload key** (signs the AAB you upload to Play Console)
- If you lose your upload key, you can request a reset through Play Console
- All new apps are automatically enrolled in Play App Signing

### iOS: Apple Certificates (managed via Fastlane Match)
- **Distribution certificate**: Signs the app binary (limited to 3 per account)
- **Provisioning profile**: Links certificate + app ID + entitlements
- Match stores both in your private Git repo, encrypted with OpenSSL
- Match automatically creates/renews certificates and profiles
- **Note (May 2025)**: Fastlane deprecated `managed_capabilities` in match; use Xcode for custom entitlements

---

## 7. Fastlane Configuration: Complete Setup

### Directory Structure
```
project_root/
├── android/
│   └── fastlane/
│       ├── Appfile
│       ├── Fastfile
│       └── .env.default
├── ios/
│   └── fastlane/
│       ├── Appfile
│       ├── Fastfile
│       ├── Matchfile
│       └── .env.default
├── Gemfile
└── Gemfile.lock
```

### Root `Gemfile`
```ruby
source "https://rubygems.org"

gem "fastlane", "~> 2.232"
gem "cocoapods", "~> 1.16"
```

### `android/fastlane/Appfile`
```ruby
json_key_file("../play-store-credentials.json")
package_name("com.zlynkr.zlynkr")
```

### `android/fastlane/Fastfile`
```ruby
default_platform(:android)

platform :android do
  desc "Deploy to Google Play Internal Testing"
  lane :internal do
    upload_to_play_store(
      track: "internal",
      aab: "../build/app/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Promote Internal to Production"
  lane :promote_to_production do
    upload_to_play_store(
      track: "internal",
      track_promote_to: "production",
      skip_upload_changelogs: false
    )
  end
end
```

### `ios/fastlane/Appfile`
```ruby
app_identifier("com.zlynkr.zlynkr")
apple_id("sarathfrancis90@icloud.com")
itc_team_id("YOUR_ITC_TEAM_ID")  # From App Store Connect
team_id("YOUR_TEAM_ID")           # From Apple Developer Portal
```

### `ios/fastlane/Matchfile`
```ruby
git_url("git@github.com:sarathfrancis/zippath-certificates.git")
storage_mode("git")
type("appstore")
app_identifier(["com.zlynkr.zlynkr"])
```

### `ios/fastlane/Fastfile`
```ruby
default_platform(:ios)

platform :ios do
  desc "Sync certificates and profiles"
  lane :sync_certs do
    match(type: "appstore", readonly: is_ci)
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    sync_certs

    api_key = app_store_connect_api_key(
      key_id: ENV["ASC_KEY_ID"],
      issuer_id: ENV["ASC_ISSUER_ID"],
      key_filepath: ENV["ASC_KEY_PATH"],
      duration: 1200,
      in_house: false
    )

    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store",
      output_directory: "../build/ios",
      output_name: "Runner.ipa"
    )

    upload_to_testflight(
      api_key: api_key,
      skip_waiting_for_build_processing: true
    )
  end

  desc "Promote to App Store"
  lane :release do
    api_key = app_store_connect_api_key(
      key_id: ENV["ASC_KEY_ID"],
      issuer_id: ENV["ASC_ISSUER_ID"],
      key_filepath: ENV["ASC_KEY_PATH"],
      duration: 1200,
      in_house: false
    )

    deliver(
      api_key: api_key,
      submit_for_review: true,
      automatic_release: true,
      force: true,
      skip_binary_upload: true,
      precheck_include_in_app_purchases: false
    )
  end
end
```

---

## 8. Flutter Build Commands: Current Best Practices

### Android Release Build
```bash
flutter build appbundle \
  --release \
  --obfuscate \
  --split-debug-info=build/app/outputs/symbols \
  --dart-define=FLUTTER_BUILD_MODE=release
```

### iOS Release Build
```bash
flutter build ipa \
  --release \
  --obfuscate \
  --split-debug-info=build/ios/symbols \
  --export-options-plist=ios/ExportOptions.plist
```

### Key flags explained:
| Flag | Purpose |
|------|---------|
| `--release` | Optimized build with AOT compilation |
| `--obfuscate` | Renames Dart symbols to make reverse engineering harder |
| `--split-debug-info=<dir>` | Required with `--obfuscate`; outputs symbol maps for crash reporting |
| `--dart-define=KEY=VALUE` | Compile-time constants (env config) |
| `--export-options-plist` | iOS signing/export configuration |

### Symbol maps for crash reporting:
Upload the `build/app/outputs/symbols/` directory to Firebase Crashlytics or your crash reporting service to get readable stack traces from obfuscated builds.

---

## 9. Complete GitHub Actions Workflows

### `.github/workflows/ci.yml` -- Pull Request CI
```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.x'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter analyze --fatal-infos
      - run: flutter test --coverage
```

### `.github/workflows/deploy-android.yml` -- Android Deployment
```yaml
name: Deploy Android

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.x'
          channel: 'stable'
          cache: true

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: Decode keystore
        run: echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 --decode > android/app/upload-keystore.jks

      - name: Create key.properties
        run: |
          cat > android/key.properties << EOF
          storePassword=${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          keyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}
          keyAlias=upload
          storeFile=upload-keystore.jks
          EOF

      - name: Decode Play Store credentials
        run: echo "${{ secrets.PLAY_STORE_CREDENTIALS }}" | base64 --decode > android/play-store-credentials.json

      - name: Build AAB
        run: |
          flutter build appbundle \
            --release \
            --obfuscate \
            --split-debug-info=build/app/outputs/symbols

      - name: Deploy to Play Store (Internal)
        run: |
          cd android
          bundle exec fastlane internal
```

### `.github/workflows/deploy-ios.yml` -- iOS Deployment
```yaml
name: Deploy iOS

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.x'
          channel: 'stable'
          cache: true

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: Install CocoaPods
        run: cd ios && pod install

      - name: Decode App Store Connect API Key
        run: |
          echo "${{ secrets.ASC_KEY_P8_BASE64 }}" | base64 --decode > ios/AuthKey.p8

      - name: Build IPA
        run: |
          flutter build ipa \
            --release \
            --obfuscate \
            --split-debug-info=build/ios/symbols

      - name: Deploy to TestFlight
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTHORIZATION }}
          ASC_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          ASC_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          ASC_KEY_PATH: "../ios/AuthKey.p8"
        run: |
          cd ios
          bundle exec fastlane beta
```

---

## 10. GitHub Secrets Required

You will need to configure these secrets in your GitHub repository (Settings > Secrets and variables > Actions):

| Secret Name | Source | Description |
|------------|--------|-------------|
| `ANDROID_KEYSTORE_BASE64` | `base64 upload-keystore.jks` | Base64-encoded upload keystore |
| `ANDROID_KEYSTORE_PASSWORD` | Your password | Keystore password |
| `ANDROID_KEY_PASSWORD` | Your password | Key password |
| `PLAY_STORE_CREDENTIALS` | `base64 play-store-credentials.json` | Base64-encoded Google service account JSON |
| `ASC_KEY_P8_BASE64` | `base64 AuthKey_XXXXXX.p8` | Base64-encoded App Store Connect API key |
| `ASC_KEY_ID` | App Store Connect | API Key ID |
| `ASC_ISSUER_ID` | App Store Connect | Issuer ID |
| `MATCH_PASSWORD` | Your passphrase | Passphrase to decrypt match certificates repo |
| `MATCH_GIT_BASIC_AUTHORIZATION` | `echo -n "user:token" \| base64` | Auth for match Git repo |

---

## 11. Step-by-Step Implementation Order

Here is the concrete sequence to set everything up:

### Phase 1: Local Setup (Do First)
1. Generate Android upload keystore
2. Create `android/key.properties` (add to `.gitignore`)
3. Update `android/app/build.gradle.kts` with signing config
4. Create Google Play Console app entry and upload the first AAB manually
5. Create Google Cloud service account and download JSON key
6. Grant service account API access in Play Console (wait 24 hours)
7. Create App Store Connect app entry
8. Generate App Store Connect API key (download `.p8`)
9. Install Fastlane locally: `gem install fastlane` or `brew install fastlane`
10. Create root `Gemfile` with Fastlane dependency
11. Run `fastlane init` in both `android/` and `ios/` directories
12. Create private GitHub repo for iOS certificates
13. Run `fastlane match init` and `fastlane match appstore` in `ios/`
14. Test both lanes locally: `cd android && fastlane internal` and `cd ios && fastlane beta`

### Phase 2: CI/CD Setup
15. Add all secrets to GitHub repository
16. Create `.github/workflows/ci.yml` (PR checks)
17. Create `.github/workflows/deploy-android.yml`
18. Create `.github/workflows/deploy-ios.yml`
19. Tag a release (`git tag v1.0.0 && git push --tags`) to trigger deployments
20. Verify builds succeed, apps appear in Play Console Internal and TestFlight

### Phase 3: Post-Launch Enhancements (Optional)
21. Add Shorebird for emergency OTA patches
22. Add Firebase App Distribution for pre-release testing
23. Consider self-hosted macOS runner if build costs exceed $50/month

---

## 12. Cost Estimate (Monthly)

| Item | Cost |
|------|------|
| GitHub Actions - Linux runners (CI) | Free (2,000 min/mo) |
| GitHub Actions - macOS runners (iOS builds) | ~$5-15/mo (60-200 min at $0.08/min) |
| Google Play Console | $25 one-time |
| Apple Developer Program | $99/year |
| Shorebird (if added) | Free tier to start |
| **Total ongoing** | **~$15-25/month** |

---

## Key Files Referenced in This Research

- `/Users/sarathfrancis/work/git/Personal/Zip/pubspec.yaml` -- Current app configuration showing package name `zlynkr` and version `1.0.0+1`
- `/Users/sarathfrancis/work/git/Personal/Zip/android/app/build.gradle.kts` -- Current Android build config with `applicationId = "com.zlynkr.zlynkr"`, currently using debug signing for release (needs to be updated)
- `/Users/sarathfrancis/work/git/Personal/Zip/CLAUDE.md` -- Project context specifying GitHub Actions + Fastlane as the CI/CD stack

## Sources

- [Flutter Official: Continuous Delivery](https://docs.flutter.dev/deployment/cd)
- [Flutter Official: Build and Release Android](https://docs.flutter.dev/deployment/android)
- [Flutter Official: Build and Release iOS](https://docs.flutter.dev/deployment/ios)
- [Flutter Official: Obfuscate Dart Code](https://docs.flutter.dev/deployment/obfuscate)
- [Shorebird Official: Code Push Overview](https://docs.shorebird.dev/code-push/)
- [Shorebird FAQ: App Store Compliance](https://docs.shorebird.dev/code-push/faq/)
- [Shorebird 2025 Year in Review](https://shorebird.dev/blog/2025-year-in-review)
- [Shorebird Pricing](https://shorebird.dev/pricing)
- [Fastlane: Match Documentation](https://docs.fastlane.tools/actions/match/)
- [Fastlane: Upload to Play Store](https://docs.fastlane.tools/actions/upload_to_play_store/)
- [Fastlane: Flutter Getting Started](https://docs.fastlane.tools/getting-started/cross-platform/flutter/)
- [Fastlane Releases (v2.232.1)](https://github.com/fastlane/fastlane/releases)
- [GitHub Actions Runner Pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)
- [Codemagic vs GitHub Actions Comparison](https://blog.codemagic.io/codemagic-vs-github-actions-comparison/)
- [Bright Inventions: iOS TestFlight with GitHub Actions & Fastlane Match (2025)](https://brightinventions.pl/blog/ios-testflight-github-actions-fastlane-match/)
- [NTT DATA: Flutter CI/CD with Fastlane and GitHub Actions](https://nttdata-dach.github.io/posts/dd-fluttercicd-01-basics/)
- [Flutter Play Store Deployment 2026 Checklist](https://flutterfever.com/how-to-deploy-flutter-app-on-google-play-store/)
- [Deploy Flutter Android App to Play Store 2026](https://dev.to/dharanidharan_d_tech/deploy-your-flutter-android-app-to-play-store-in-2026-step-by-step-guide-with-code-gotchas-n2k)
- [Google Play Developer API: Getting Started](https://developers.google.com/android-publisher/getting_started)
- [Codemagic: iOS Code Signing](https://docs.codemagic.io/flutter-code-signing/ios-code-signing/)
- [FreeCodeCamp: Automate Flutter Testing with GitHub Actions](https://www.freecodecamp.org/news/how-to-automate-flutter-testing-and-builds-with-github-actions-for-android-and-ios/)

---

