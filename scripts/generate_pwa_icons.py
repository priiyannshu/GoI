"""Generates standard, maskable, and favicon PWA icons with the official sky blue emblem."""
import os
import subprocess

def generate_icons():
    node_script = """
    const sharp = require('./worker/node_modules/sharp');
    const fs = require('fs');

    const svgIcon = (size, isMaskable = false) => {
      const radius = isMaskable ? 0 : Math.round(size * 0.22);
      
      return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="${size}" height="${size}" rx="${radius}" fill="#0F172A"/>
        
        <!-- Subtle Sky Blue Accent Ring -->
        <rect x="${size*0.06}" y="${size*0.06}" width="${size*0.88}" height="${size*0.88}" rx="${radius*0.9}" fill="none" stroke="#38BDF8" stroke-opacity="0.35" stroke-width="${Math.max(2, size*0.015)}"/>
        
        <!-- Inner Sky Blue Container Matching AppHeader -->
        <rect x="${size*0.14}" y="${size*0.14}" width="${size*0.72}" height="${size*0.72}" rx="${radius*0.7}" fill="#0284C7" fill-opacity="0.15" stroke="#38BDF8" stroke-opacity="0.45" stroke-width="${Math.max(2, size*0.018)}"/>
        
        <!-- Perfectly Symmetrical Classical Emblem in Sky Blue (🏛️) -->
        <g transform="translate(${size*0.22}, ${size*0.24}) scale(${(size*0.56)/240})">
          <!-- Pediment Roof Triangle -->
          <path d="M120 16 L228 78 L12 78 Z" fill="#0284C7" stroke="#38BDF8" stroke-width="6" stroke-linejoin="round"/>
          <circle cx="120" cy="54" r="12" fill="#0F172A" stroke="#38BDF8" stroke-width="4"/>
          <circle cx="120" cy="54" r="4.5" fill="#38BDF8"/>
          <!-- Architrave / Entablature below triangle -->
          <rect x="12" y="82" width="216" height="18" rx="4" fill="#38BDF8"/>
          
          <!-- 4 Symmetrical Columns -->
          <!-- Column 1 (Center: 39) -->
          <rect x="21" y="104" width="36" height="9" rx="2" fill="#38BDF8"/>
          <rect x="26" y="113" width="26" height="90" rx="3" fill="#0284C7"/>
          <line x1="34" y1="116" x2="34" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="44" y1="116" x2="44" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="21" y="203" width="36" height="9" rx="2" fill="#38BDF8"/>
          
          <!-- Column 2 (Center: 93) -->
          <rect x="75" y="104" width="36" height="9" rx="2" fill="#38BDF8"/>
          <rect x="80" y="113" width="26" height="90" rx="3" fill="#0284C7"/>
          <line x1="88" y1="116" x2="88" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="98" y1="116" x2="98" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="75" y="203" width="36" height="9" rx="2" fill="#38BDF8"/>
          
          <!-- Column 3 (Center: 147) -->
          <rect x="129" y="104" width="36" height="9" rx="2" fill="#38BDF8"/>
          <rect x="134" y="113" width="26" height="90" rx="3" fill="#0284C7"/>
          <line x1="142" y1="116" x2="142" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="152" y1="116" x2="152" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="129" y="203" width="36" height="9" rx="2" fill="#38BDF8"/>
          
          <!-- Column 4 (Center: 201) -->
          <rect x="183" y="104" width="36" height="9" rx="2" fill="#38BDF8"/>
          <rect x="188" y="113" width="26" height="90" rx="3" fill="#0284C7"/>
          <line x1="196" y1="116" x2="196" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="206" y1="116" x2="206" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="183" y="203" width="36" height="9" rx="2" fill="#38BDF8"/>
          
          <!-- Stepped Stylobate / Base -->
          <rect x="10" y="214" width="220" height="14" rx="4" fill="#38BDF8"/>
          <rect x="0" y="230" width="240" height="16" rx="4" fill="#0284C7"/>
        </g>
      </svg>`;
    };

    async function run() {
      const targets = [
        { file: 'frontend/public/pwa-512x512.png', size: 512, maskable: false },
        { file: 'frontend/public/pwa-192x192.png', size: 192, maskable: false },
        { file: 'frontend/public/maskable-icon.png', size: 512, maskable: true },
        { file: 'frontend/public/favicon.ico', size: 64, maskable: false }
      ];
      for (const t of targets) {
        await sharp(Buffer.from(svgIcon(t.size, t.maskable))).resize(t.size, t.size).png().toFile(t.file);
      }
      fs.writeFileSync('frontend/public/logo.svg', svgIcon(512, false));
      console.log('Successfully generated symmetrical sky-blue icons!');
    }
    run();
    """
    subprocess.run(['node', '-e', node_script], check=True)

if __name__ == '__main__':
    generate_icons()
