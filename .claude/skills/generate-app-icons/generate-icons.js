#!/usr/bin/env node
/**
 * App Icon Generator — Production-ready icons for all platforms
 *
 * Usage:
 *   node generate-icons.js --source ./icon.png --output ./app-icons
 *   node generate-icons.js --source ./icon.png --output ./app-icons --platforms ios,android,web
 *   node generate-icons.js --prompt "3D isometric J letter" --output ./app-icons
 *   node generate-icons.js --reference ./ref.png --prompt "clean app icon" --output ./app-icons
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// ─── Platform Icon Specifications ──────────────────────────────────────────

const SPECS = {
  ios: {
    dir: "ios/AppIcon.appiconset",
    sizes: [
      { size: 1024, name: "icon-1024.png", idiom: "universal", scale: "1x", platform: "ios" },
      { size: 180, name: "icon-180.png", idiom: "iphone", scale: "3x" },
      { size: 120, name: "icon-120.png", idiom: "iphone", scale: "2x" },
      { size: 167, name: "icon-167.png", idiom: "ipad", scale: "2x" },
      { size: 152, name: "icon-152.png", idiom: "ipad", scale: "2x" },
      { size: 87, name: "icon-87.png", idiom: "iphone", scale: "3x", role: "spotlight" },
      { size: 80, name: "icon-80.png", idiom: "ipad", scale: "2x", role: "spotlight" },
      { size: 76, name: "icon-76.png", idiom: "ipad", scale: "1x" },
      { size: 60, name: "icon-60.png", idiom: "iphone", scale: "1x" },
      { size: 58, name: "icon-58.png", idiom: "iphone", scale: "2x", role: "settings" },
      { size: 40, name: "icon-40.png", idiom: "universal", scale: "2x", role: "spotlight" },
      { size: 29, name: "icon-29.png", idiom: "iphone", scale: "1x", role: "settings" },
      { size: 20, name: "icon-20.png", idiom: "universal", scale: "1x", role: "notification" },
    ],
  },
  android: {
    dir: "android",
    sizes: [
      { size: 512, name: "playstore-icon.png", density: "playstore" },
      { size: 192, name: "mipmap-xxxhdpi/ic_launcher.png", density: "xxxhdpi" },
      { size: 144, name: "mipmap-xxhdpi/ic_launcher.png", density: "xxhdpi" },
      { size: 96, name: "mipmap-xhdpi/ic_launcher.png", density: "xhdpi" },
      { size: 72, name: "mipmap-hdpi/ic_launcher.png", density: "hdpi" },
      { size: 48, name: "mipmap-mdpi/ic_launcher.png", density: "mdpi" },
      // Round icons
      { size: 192, name: "mipmap-xxxhdpi/ic_launcher_round.png", density: "xxxhdpi" },
      { size: 144, name: "mipmap-xxhdpi/ic_launcher_round.png", density: "xxhdpi" },
      { size: 96, name: "mipmap-xhdpi/ic_launcher_round.png", density: "xhdpi" },
      { size: 72, name: "mipmap-hdpi/ic_launcher_round.png", density: "hdpi" },
      { size: 48, name: "mipmap-mdpi/ic_launcher_round.png", density: "mdpi" },
    ],
  },
  macos: {
    dir: "macos",
    sizes: [
      { size: 1024, name: "icon_512x512@2x.png" },
      { size: 512, name: "icon_512x512.png" },
      { size: 512, name: "icon_256x256@2x.png" },
      { size: 256, name: "icon_256x256.png" },
      { size: 256, name: "icon_128x128@2x.png" },
      { size: 128, name: "icon_128x128.png" },
      { size: 64, name: "icon_32x32@2x.png" },
      { size: 32, name: "icon_32x32.png" },
      { size: 32, name: "icon_16x16@2x.png" },
      { size: 16, name: "icon_16x16.png" },
    ],
  },
  windows: {
    dir: "windows",
    sizes: [
      { size: 256, name: "icon-256.png" },
      { size: 128, name: "icon-128.png" },
      { size: 64, name: "icon-64.png" },
      { size: 48, name: "icon-48.png" },
      { size: 32, name: "icon-32.png" },
      { size: 16, name: "icon-16.png" },
    ],
  },
  web: {
    dir: "web",
    sizes: [
      { size: 512, name: "icon-512x512.png" },
      { size: 192, name: "icon-192x192.png" },
      { size: 180, name: "apple-touch-icon.png" },
      { size: 152, name: "icon-152x152.png" },
      { size: 144, name: "icon-144x144.png" },
      { size: 128, name: "icon-128x128.png" },
      { size: 96, name: "icon-96x96.png" },
      { size: 72, name: "icon-72x72.png" },
      { size: 48, name: "icon-48x48.png" },
      { size: 32, name: "favicon-32x32.png" },
      { size: 16, name: "favicon-16x16.png" },
    ],
  },
  electron: {
    dir: "electron",
    sizes: [
      { size: 1024, name: "icon-1024.png" },
      { size: 512, name: "icon.png" },
      { size: 256, name: "icon-256.png" },
      { size: 128, name: "icon-128.png" },
      { size: 64, name: "icon-64.png" },
      { size: 32, name: "icon-32.png" },
      { size: 16, name: "icon-16.png" },
      { size: 44, name: "tray-icon@2x.png" },
      { size: 22, name: "tray-icon.png" },
      { size: 44, name: "tray-iconTemplate@2x.png" },
      { size: 22, name: "tray-iconTemplate.png" },
    ],
  },
};

// ─── Helper Functions ──────────────────────────────────────────────────────

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    source: null,
    prompt: null,
    reference: null,
    output: "./app-icons",
    platforms: Object.keys(SPECS),
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--source":
        opts.source = args[++i];
        break;
      case "--prompt":
        opts.prompt = args[++i];
        break;
      case "--reference":
        opts.reference = args[++i];
        break;
      case "--output":
        opts.output = args[++i];
        break;
      case "--platforms":
        opts.platforms = args[++i].split(",");
        break;
    }
  }
  return opts;
}

// ─── Ensure Dependencies ───────────────────────────────────────────────────

function ensureDeps() {
  const skillDir = __dirname;
  const nodeModules = path.join(skillDir, "node_modules");

  if (!fs.existsSync(path.join(nodeModules, "sharp"))) {
    console.log("Installing dependencies (first run)...");
    execSync("npm install --no-save sharp sharp-ico png2icons", {
      cwd: skillDir,
      stdio: "pipe",
    });

    // Create a minimal package.json if it doesn't exist
    const pkgPath = path.join(skillDir, "package.json");
    if (!fs.existsSync(pkgPath)) {
      fs.writeFileSync(
        pkgPath,
        JSON.stringify({ name: "generate-app-icons", version: "1.0.0", private: true }, null, 2)
      );
    }
  }
}

// ─── AI Generation via Gemini (Nano Banana) ────────────────────────────────

async function generateWithAI(prompt, referencePath, outputPath) {
  const apiKey = process.env.GOOGLE_AI_API_KEY || process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.error(
      "Error: GOOGLE_AI_API_KEY or GEMINI_API_KEY env var required for AI generation"
    );
    process.exit(1);
  }

  const model = process.env.ICON_GEN_MODEL || "gemini-2.5-flash-image";
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

  const parts = [];

  // Add reference image if provided
  if (referencePath && fs.existsSync(referencePath)) {
    const imageData = fs.readFileSync(referencePath).toString("base64");
    const mimeType = referencePath.endsWith(".png") ? "image/png" : "image/jpeg";
    parts.push({
      inline_data: { mime_type: mimeType, data: imageData },
    });
  }

  // Add the prompt
  const fullPrompt = `Generate a clean, professional app icon (1024x1024 pixels, square, no rounded corners — the OS will apply rounding). ${prompt}. The icon should be centered, have good contrast, and look crisp at small sizes. Output a single PNG image.`;
  parts.push({ text: fullPrompt });

  const body = {
    contents: [{ parts }],
    generationConfig: {
      responseModalities: ["TEXT", "IMAGE"],
    },
  };

  console.log("Generating icon with AI (Nano Banana)...");

  const https = require("https");
  const response = await new Promise((resolve, reject) => {
    const req = https.request(url, { method: "POST", headers: { "Content-Type": "application/json" } }, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve({ status: res.statusCode, data }));
    });
    req.on("error", reject);
    req.write(JSON.stringify(body));
    req.end();
  });

  if (response.status !== 200) {
    console.error(`AI API error (${response.status}):`, response.data.substring(0, 500));
    process.exit(1);
  }

  const result = JSON.parse(response.data);
  const candidates = result.candidates || [];

  for (const candidate of candidates) {
    for (const part of candidate.content?.parts || []) {
      const imgData = part.inline_data || part.inlineData;
      if (imgData) {
        const imageBuffer = Buffer.from(imgData.data, "base64");
        fs.writeFileSync(outputPath, imageBuffer);
        console.log(`AI-generated icon saved: ${outputPath}`);
        return outputPath;
      }
    }
  }

  console.error("AI did not return an image. Response:", JSON.stringify(result).substring(0, 500));
  process.exit(1);
}

// ─── Icon Generation ───────────────────────────────────────────────────────

async function generateIcons(sourcePath, outputDir, platforms) {
  const sharp = require("sharp");

  // Validate source
  if (!fs.existsSync(sourcePath)) {
    console.error(`Source file not found: ${sourcePath}`);
    process.exit(1);
  }

  // Read and prepare source image
  const sourceImage = sharp(sourcePath);
  const metadata = await sourceImage.metadata();
  console.log(`Source: ${sourcePath} (${metadata.width}x${metadata.height})`);

  // Ensure square and at least 1024x1024
  let masterImage;
  const minDim = Math.min(metadata.width, metadata.height);
  if (metadata.width !== metadata.height) {
    // Crop to square (center)
    masterImage = sharp(sourcePath).resize(minDim, minDim, { fit: "cover", position: "center" });
    console.log(`Cropped to square: ${minDim}x${minDim}`);
  } else {
    masterImage = sharp(sourcePath);
  }

  // Scale to 1024 if needed
  const masterBuffer = await masterImage.resize(1024, 1024, { fit: "fill" }).png().toBuffer();
  const masterPath = path.join(outputDir, "source-1024.png");
  ensureDir(outputDir);
  fs.writeFileSync(masterPath, masterBuffer);
  console.log(`Master icon: ${masterPath}`);

  let totalFiles = 0;

  for (const platform of platforms) {
    const spec = SPECS[platform];
    if (!spec) {
      console.warn(`Unknown platform: ${platform}, skipping`);
      continue;
    }

    console.log(`\nGenerating ${platform} icons...`);
    const platformDir = path.join(outputDir, spec.dir);
    ensureDir(platformDir);

    for (const icon of spec.sizes) {
      const filePath = path.join(platformDir, icon.name);
      ensureDir(path.dirname(filePath));

      await sharp(masterBuffer)
        .resize(icon.size, icon.size, { fit: "fill", kernel: "lanczos3" })
        .png({ quality: 100, compressionLevel: 9 })
        .toFile(filePath);

      totalFiles++;
      process.stdout.write(`  ✓ ${icon.name} (${icon.size}x${icon.size})\n`);
    }

    // Generate platform-specific files
    if (platform === "ios") {
      generateIOSContentsJson(platformDir, spec.sizes);
    } else if (platform === "web") {
      await generateFaviconICO(masterBuffer, platformDir);
      generateWebManifest(platformDir);
      generateBrowserConfig(platformDir);
    } else if (platform === "macos") {
      await generateICNS(masterBuffer, platformDir);
    } else if (platform === "windows") {
      await generateWindowsICO(masterBuffer, platformDir);
    } else if (platform === "electron") {
      await generateICNS(masterBuffer, platformDir);
      await generateWindowsICO(masterBuffer, platformDir);
    }
  }

  console.log(`\n✅ Generated ${totalFiles} icon files across ${platforms.length} platforms`);
  console.log(`   Output: ${outputDir}`);
}

// ─── iOS Contents.json ─────────────────────────────────────────────────────

function generateIOSContentsJson(dir, sizes) {
  const images = sizes.map((s) => {
    const entry = {
      filename: s.name,
      idiom: s.idiom || "universal",
      scale: s.scale || "1x",
      size: `${Math.round(s.size / parseInt(s.scale || "1"))}x${Math.round(s.size / parseInt(s.scale || "1"))}`,
    };
    if (s.platform) entry.platform = s.platform;
    return entry;
  });

  const contents = {
    images,
    info: { author: "generate-app-icons", version: 1 },
  };

  fs.writeFileSync(path.join(dir, "Contents.json"), JSON.stringify(contents, null, 2));
  console.log("  ✓ Contents.json (Xcode asset catalog)");
}

// ─── Web Manifest & Favicon ───────────────────────────────────────────────

async function generateFaviconICO(masterBuffer, dir) {
  try {
    const sharpIco = require("sharp-ico");
    const sharp = require("sharp");

    const sizes = [16, 32, 48];
    const images = await Promise.all(
      sizes.map((size) =>
        sharp(masterBuffer).resize(size, size, { fit: "fill", kernel: "lanczos3" }).png().toBuffer()
      )
    );

    const icoBuffer = await sharpIco.encode(images);
    fs.writeFileSync(path.join(dir, "favicon.ico"), icoBuffer);
    console.log("  ✓ favicon.ico (multi-size)");
  } catch (e) {
    console.warn("  ⚠ favicon.ico generation failed (sharp-ico not available), using 32px PNG fallback");
    const sharp = require("sharp");
    await sharp(masterBuffer).resize(32, 32).png().toFile(path.join(dir, "favicon.ico"));
  }
}

function generateWebManifest(dir) {
  const manifest = {
    name: "Jet",
    short_name: "Jet",
    description: "Open-source project management tool",
    start_url: "/",
    display: "standalone",
    background_color: "#09090B",
    theme_color: "#3B82F6",
    icons: [
      { src: "/icon-192x192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512x512.png", sizes: "512x512", type: "image/png" },
      { src: "/icon-512x512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
  fs.writeFileSync(path.join(dir, "site.webmanifest"), JSON.stringify(manifest, null, 2));
  console.log("  ✓ site.webmanifest");
}

function generateBrowserConfig(dir) {
  const xml = `<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square150x150logo src="/icon-144x144.png"/>
      <TileColor>#09090B</TileColor>
    </tile>
  </msapplication>
</browserconfig>`;
  fs.writeFileSync(path.join(dir, "browserconfig.xml"), xml);
  console.log("  ✓ browserconfig.xml");
}

// ─── ICNS Generation ───────────────────────────────────────────────────────

async function generateICNS(masterBuffer, dir) {
  try {
    const png2icons = require("png2icons");
    const icnsBuffer = png2icons.createICNS(masterBuffer, png2icons.BICUBIC, 0);
    if (icnsBuffer) {
      fs.writeFileSync(path.join(dir, "icon.icns"), icnsBuffer);
      console.log("  ✓ icon.icns (macOS)");
    }
  } catch (e) {
    console.warn("  ⚠ ICNS generation failed:", e.message);
    // Fallback: create iconset folder (macOS can convert)
    console.log("  → iconset folder created, run `iconutil -c icns icon.iconset` to generate .icns");
  }
}

// ─── Windows ICO Generation ────────────────────────────────────────────────

async function generateWindowsICO(masterBuffer, dir) {
  try {
    const png2icons = require("png2icons");
    const icoBuffer = png2icons.createICO(masterBuffer, png2icons.BICUBIC, 0, true);
    if (icoBuffer) {
      fs.writeFileSync(path.join(dir, "icon.ico"), icoBuffer);
      console.log("  ✓ icon.ico (Windows)");
    }
  } catch (e) {
    try {
      const sharpIco = require("sharp-ico");
      const sharp = require("sharp");
      const sizes = [256, 128, 64, 48, 32, 16];
      const images = await Promise.all(
        sizes.map((size) => sharp(masterBuffer).resize(size, size).png().toBuffer())
      );
      const icoBuffer = await sharpIco.encode(images);
      fs.writeFileSync(path.join(dir, "icon.ico"), icoBuffer);
      console.log("  ✓ icon.ico (Windows, via sharp-ico)");
    } catch (e2) {
      console.warn("  ⚠ ICO generation failed:", e2.message);
    }
  }
}

// ─── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const opts = parseArgs();

  console.log("🎨 App Icon Generator");
  console.log("─".repeat(50));

  // Ensure dependencies
  ensureDeps();

  let sourcePath;

  if (opts.source) {
    sourcePath = path.resolve(opts.source);
  } else if (opts.prompt) {
    // AI generation mode
    const tempPath = path.join(opts.output, "ai-generated-source.png");
    ensureDir(opts.output);
    sourcePath = await generateWithAI(opts.prompt, opts.reference ? path.resolve(opts.reference) : null, tempPath);
  } else {
    console.error("Error: Provide --source <path> or --prompt <description>");
    console.error("");
    console.error("Usage:");
    console.error("  node generate-icons.js --source ./icon.png --output ./app-icons");
    console.error('  node generate-icons.js --prompt "3D letter J, cyan" --output ./app-icons');
    console.error('  node generate-icons.js --reference ./ref.png --prompt "clean icon" --output ./app-icons');
    process.exit(1);
  }

  await generateIcons(sourcePath, path.resolve(opts.output), opts.platforms);
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
