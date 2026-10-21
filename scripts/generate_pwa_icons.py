"""Generates standard, maskable, and favicon PWA icons with the official emblem."""
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
        
        <!-- Subtle Accent Ring -->
        <rect x="${size*0.06}" y="${size*0.06}" width="${size*0.88}" height="${size*0.88}" rx="${radius*0.9}" fill="none" stroke="#10B981" stroke-opacity=\"0.28\" stroke-width="${Math.max(2, size*0.015)}"/>
        
        <!-- Inner Emerald Container Matching AppHeader -->
        <rect x="${size*0.14}" y="${size*0.14}" width="${size*0.72}" height="${size*0.72}" rx="${radius*0.7}" fill="#10B981" fill-opacity="0.15" stroke="#10B981" stroke-opacity="0.4" stroke-width="${Math.max(2, size*0.018)}"/>
        
        <!-- Classical Government Building Emblem (🏛️) -->
        <g transform="translate(${size*0.22}, ${size*0.24}) scale(${(size*0.56)/240})">
          <!-- Pediment Roof Triangle -->
          <path d="M120 16 L228 78 L12 78 Z" fill="#10B981" stroke="#34D399" stroke-width="6" stroke-linejoin="round"/>
          <circle cx="120" cy="54" r="12" fill="#0F172A" stroke="#34D399" stroke-width="4"/>
          <!-- Architrave / Entablature below triangle -->
          <rect x="14" y="82" width="212" height="20" rx="5" fill="#34D399"/>
          
          <!-- 4 Majestic Columns with fluted details -->
          <rect x="22" y="106" width="40" height="9" rx="2" fill="#34D399"/>
          <rect x="28" y="115" width="28" height="88" rx="4" fill="#10B981"/>
          <line x1="37" y1="118" x2="37" y2="199" stroke="#34D399" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="47" y1="118" x2="47" y2="199" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="22" y="203" width="40" height="9" rx="2" fill="#34D399"/>
          
          <rect x="78" y="106" width="40" height="9" rx="2" fill="#34D399"/>
          <rect x="84" y="115" width="28" height="88" rx="4" fill="#10B981"/>
          <line x1="93" y1="118" x2="93" y2="199" stroke="#34D399" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="103" y1="118" x2="103" y2="199" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="78" y="203" width="40" height="9" rx="2" fill="#34D399"/>
          
          <rect x="134" y="106" width="40" height="9" rx="2" fill="#34D399"/>
          <rect x="140" y="115" width="28" height="88" rx="4" fill="#10B981"/>
          <line x1="149" y1="118" x2="149" y2="199" stroke="#34D399" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="159" y1="118" x2="159" y2="199" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="134" y="203" width="40" height="9" rx="2" fill="#34D399"/>
          
          <rect x="190" y="106" width="40" height="9" rx="2" fill="#34D399"/>
          <rect x="196" y="115" width="28" height="88" rx="4" fill="#10B981"/>
          <line x1="205" y1="118" x2="205" y2="199" stroke="#34D399" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="215" y1="118" x2="215" y2="199" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>
          <rect x="190" y="203" width="40" height="9" rx="2" fill="#34D399"/>
          
          <!-- Stepped Stylobate / Base -->
          <rect x="10" y="214" width="220" height="14" rx="4" fill="#34D399"/>
          <rect x="0" y="230" width="240" height="16" rx="4" fill="#10B981"/>
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
      console.log('Successfully generated icons!');
    }
    run();
    """
    subprocess.run(['node', '-e', node_script], check=True)

if __name__ == '__main__':
    generate_icons()
