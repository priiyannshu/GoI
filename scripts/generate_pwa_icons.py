"""Generates standard and maskable PWA icons in frontend/public/."""
import os
import struct
import zlib

def create_png_square(path: str, size: int, color_rgb: tuple[int, int, int]):
    width = size
    height = size
    raw_data = bytearray()
    r, g, b = color_rgb
    for _ in range(height):
        raw_data.append(0)  # Filter byte 0 (None)
        for _ in range(width):
            raw_data.extend([r, g, b, 255])

    compressed = zlib.compress(bytes(raw_data), 9)
    png = bytearray(b'\x89PNG\r\n\x1a\n')  # Signature

    def add_chunk(chunk_type: bytes, data: bytes):
        length = len(data)
        png.extend(struct.pack('>I', length))
        png.extend(chunk_type)
        png.extend(data)
        crc = zlib.crc32(chunk_type + data)
        png.extend(struct.pack('>I', crc))

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    add_chunk(b'IHDR', ihdr_data)
    add_chunk(b'IDAT', compressed)
    add_chunk(b'IEND', b'')

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(png)

if __name__ == '__main__':
    public_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public')
    os.makedirs(public_dir, exist_ok=True)
    # Emerald green accent (#10B981 -> RGB 16, 185, 129)
    create_png_square(os.path.join(public_dir, 'pwa-192x192.png'), 192, (16, 185, 129))
    create_png_square(os.path.join(public_dir, 'pwa-512x512.png'), 512, (16, 185, 129))
    # Dark slate maskable icon (#0F172A -> RGB 15, 23, 42)
    create_png_square(os.path.join(public_dir, 'maskable-icon.png'), 512, (15, 23, 42))
    # Also create favicon.ico as a tiny 16x16 or 32x32 png / simple icon
    create_png_square(os.path.join(public_dir, 'favicon.ico'), 32, (16, 185, 129))
    print(f"Generated PWA icons in {public_dir}")
