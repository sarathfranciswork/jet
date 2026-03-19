#!/usr/bin/env node

/**
 * Icon Generation Script for Jet Desktop
 *
 * Prerequisites:
 *   npm install -g sharp-cli
 *   # or: brew install librsvg imagemagick
 *
 * This script converts the SVG icons in assets/ into platform-specific formats.
 *
 * Usage:
 *   node scripts/generate-icons.js
 *
 * If sharp is not available, it falls back to creating minimal placeholder PNGs
 * that allow the build to succeed. For production, install sharp and re-run.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const assetsDir = path.join(__dirname, "..", "assets");

function hasCommand(cmd) {
  try {
    execSync(`which ${cmd}`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

/**
 * Create a minimal valid PNG file.
 * This creates the smallest possible valid PNG (1x1 pixel by default,
 * or a specified size with a simple pattern).
 */
function createMinimalPNG(outputPath, width, height) {
  // Create a minimal valid PNG file
  // PNG signature + IHDR + IDAT (minimal) + IEND
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

  // IHDR chunk
  const ihdrData = Buffer.alloc(13);
  ihdrData.writeUInt32BE(width, 0);
  ihdrData.writeUInt32BE(height, 4);
  ihdrData[8] = 8; // bit depth
  ihdrData[9] = 2; // color type: RGB
  ihdrData[10] = 0; // compression method
  ihdrData[11] = 0; // filter method
  ihdrData[12] = 0; // interlace method

  const ihdrChunk = createChunk("IHDR", ihdrData);

  // Create raw pixel data (all pixels = Jet Blue #3B82F6)
  const rawData = [];
  for (let y = 0; y < height; y++) {
    rawData.push(0); // filter byte: None
    for (let x = 0; x < width; x++) {
      rawData.push(0x3b, 0x82, 0xf6); // RGB
    }
  }

  // Compress with zlib (deflate)
  const zlib = require("zlib");
  const compressed = zlib.deflateSync(Buffer.from(rawData));

  const idatChunk = createChunk("IDAT", compressed);

  // IEND chunk
  const iendChunk = createChunk("IEND", Buffer.alloc(0));

  const png = Buffer.concat([signature, ihdrChunk, idatChunk, iendChunk]);
  fs.writeFileSync(outputPath, png);
  console.log(`  Created: ${path.basename(outputPath)} (${width}x${height})`);
}

function createChunk(type, data) {
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);

  const typeBuffer = Buffer.from(type, "ascii");
  const crcData = Buffer.concat([typeBuffer, data]);

  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(crcData), 0);

  return Buffer.concat([length, typeBuffer, data, crc]);
}

function crc32(buf) {
  let crc = 0xffffffff;
  for (let i = 0; i < buf.length; i++) {
    crc ^= buf[i];
    for (let j = 0; j < 8; j++) {
      if (crc & 1) {
        crc = (crc >>> 1) ^ 0xedb88320;
      } else {
        crc = crc >>> 1;
      }
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

/**
 * Create a minimal ICO file from a PNG buffer
 */
function createICO(outputPath, pngPath) {
  const pngData = fs.readFileSync(pngPath);
  const size = 256;

  // ICO header
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0); // reserved
  header.writeUInt16LE(1, 2); // type: ICO
  header.writeUInt16LE(1, 4); // count: 1 image

  // ICO directory entry
  const entry = Buffer.alloc(16);
  entry[0] = 0; // width (0 = 256)
  entry[1] = 0; // height (0 = 256)
  entry[2] = 0; // color palette
  entry[3] = 0; // reserved
  entry.writeUInt16LE(1, 4); // color planes
  entry.writeUInt16LE(32, 6); // bits per pixel
  entry.writeUInt32LE(pngData.length, 8); // size of image data
  entry.writeUInt32LE(22, 12); // offset to image data (6 + 16 = 22)

  const ico = Buffer.concat([header, entry, pngData]);
  fs.writeFileSync(outputPath, ico);
  console.log(`  Created: ${path.basename(outputPath)}`);
}

/**
 * Create a minimal ICNS file from PNG data
 */
function createICNS(outputPath, pngPath) {
  const pngData = fs.readFileSync(pngPath);

  // ICNS header
  const magic = Buffer.from("icns");
  const fileSize = Buffer.alloc(4);
  // ic10 = 1024x1024 retina, but we'll use ic09 (512x512)
  const iconType = Buffer.from("ic09");
  const iconSize = Buffer.alloc(4);

  const dataLength = 8 + pngData.length; // type(4) + size(4) + data
  iconSize.writeUInt32BE(dataLength, 0);

  const totalSize = 8 + dataLength; // magic(4) + fileSize(4) + icon entry
  fileSize.writeUInt32BE(totalSize, 0);

  const icns = Buffer.concat([magic, fileSize, iconType, iconSize, pngData]);
  fs.writeFileSync(outputPath, icns);
  console.log(`  Created: ${path.basename(outputPath)}`);
}

// Main
console.log("Generating Jet Desktop icons...\n");

// Check if we can use rsvg-convert or sips for SVG->PNG
const hasRsvg = hasCommand("rsvg-convert");
const hasSips = process.platform === "darwin";

if (hasRsvg) {
  console.log("Using rsvg-convert for SVG to PNG conversion\n");

  // Generate main icon at various sizes
  const sizes = [16, 32, 64, 128, 256, 512, 1024];
  for (const size of sizes) {
    const out = path.join(assetsDir, `icon-${size}.png`);
    execSync(
      `rsvg-convert -w ${size} -h ${size} "${path.join(assetsDir, "icon.svg")}" -o "${out}"`
    );
    console.log(`  Generated: icon-${size}.png`);
  }

  // Copy 512 as the main icon.png
  fs.copyFileSync(
    path.join(assetsDir, "icon-512.png"),
    path.join(assetsDir, "icon.png")
  );

  // Generate tray icons
  const traySizes = [16, 22, 32, 44];
  for (const size of traySizes) {
    const suffix = size > 22 ? "@2x" : "";
    const out = path.join(
      assetsDir,
      size <= 22 ? `tray-icon.png` : `tray-icon${suffix}.png`
    );
    execSync(
      `rsvg-convert -w ${size} -h ${size} "${path.join(assetsDir, "tray-icon.svg")}" -o "${out}"`
    );
    console.log(`  Generated: tray-icon${suffix}.png (${size}x${size})`);
  }

  // macOS template tray icon
  fs.copyFileSync(
    path.join(assetsDir, "tray-icon.png"),
    path.join(assetsDir, "tray-iconTemplate.png")
  );
  fs.copyFileSync(
    path.join(assetsDir, "tray-icon@2x.png"),
    path.join(assetsDir, "tray-iconTemplate@2x.png")
  );
} else {
  console.log(
    "rsvg-convert not found. Creating placeholder PNG icons.\n" +
      "For production icons, install librsvg: brew install librsvg\n"
  );

  // Create placeholder PNGs
  createMinimalPNG(path.join(assetsDir, "icon.png"), 512, 512);
  createMinimalPNG(path.join(assetsDir, "icon-16.png"), 16, 16);
  createMinimalPNG(path.join(assetsDir, "icon-32.png"), 32, 32);
  createMinimalPNG(path.join(assetsDir, "icon-64.png"), 64, 64);
  createMinimalPNG(path.join(assetsDir, "icon-128.png"), 128, 128);
  createMinimalPNG(path.join(assetsDir, "icon-256.png"), 256, 256);
  createMinimalPNG(path.join(assetsDir, "icon-512.png"), 512, 512);
  createMinimalPNG(path.join(assetsDir, "icon-1024.png"), 1024, 1024);
  createMinimalPNG(path.join(assetsDir, "tray-icon.png"), 22, 22);
  createMinimalPNG(path.join(assetsDir, "tray-icon@2x.png"), 44, 44);
  createMinimalPNG(path.join(assetsDir, "tray-iconTemplate.png"), 22, 22);
  createMinimalPNG(path.join(assetsDir, "tray-iconTemplate@2x.png"), 44, 44);
}

// Generate ICO (Windows)
console.log("\nGenerating platform-specific formats...");
const icon256Path = path.join(assetsDir, "icon-256.png");
if (!fs.existsSync(icon256Path)) {
  createMinimalPNG(icon256Path, 256, 256);
}
createICO(path.join(assetsDir, "icon.ico"), icon256Path);

// Generate ICNS (macOS)
const icon512Path = path.join(assetsDir, "icon-512.png");
if (!fs.existsSync(icon512Path)) {
  createMinimalPNG(icon512Path, 512, 512);
}
createICNS(path.join(assetsDir, "icon.icns"), icon512Path);

console.log("\nIcon generation complete!");
