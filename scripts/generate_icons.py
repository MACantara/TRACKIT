"""
Generate placeholder PWA icons for TRACKIT app.
Usage: python scripts/generate_icons.py

This creates simple gradient icons with the TRACKIT logo text.
For production, replace these with professionally designed icons.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("WARNING: Pillow not installed. Run: pip install Pillow")
    print("Continuing with alternative SVG approach...")

import os

ICON_DIR = os.path.join('static', 'icons')
SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def create_icons_with_pil():
    """Create icons using PIL/Pillow library."""
    os.makedirs(ICON_DIR, exist_ok=True)
    
    for size in SIZES:
        # Create image with gradient background
        img = Image.new('RGB', (size, size), color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Draw gradient effect (simplified)
        for y in range(size):
            ratio = y / size
            r = int(102 + (118 - 102) * ratio)
            g = int(126 + (75 - 126) * ratio)
            b = int(234 + (162 - 234) * ratio)
            draw.line([(0, y), (size, y)], fill=(r, g, b))
        
        # Draw circle in center
        circle_margin = size // 4
        draw.ellipse(
            [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
            fill='white',
            outline='white',
            width=2
        )
        
        # Try to add text
        try:
            # Attempt to load a font
            font_size = size // 6
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Draw "T" in the center
            text = "T"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size - text_width) // 2, (size - text_height) // 2 - size // 20)
            draw.text(position, text, fill='#667eea', font=font)
        except:
            pass
        
        # Save icon
        filename = f'icon-{size}x{size}.png'
        filepath = os.path.join(ICON_DIR, filename)
        img.save(filepath, 'PNG')
        print(f'Created {filename}')
    
    print(f'\nAll icons created in {ICON_DIR}/')

def create_placeholder_readme():
    """Create a README for icon replacement."""
    readme_path = os.path.join(ICON_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("""# PWA Icons

These are placeholder icons for the TRACKIT PWA.

## Icon Sizes
- 72x72 - iOS Safari minimal
- 96x96 - Android Chrome minimal
- 128x128 - Standard app icon
- 144x144 - Windows tile
- 152x152 - iOS iPad
- 192x192 - Android primary
- 384x384 - Android splash
- 512x512 - High-resolution devices

## Replacing Icons
For production, replace these with professionally designed icons that:
1. Match your brand identity
2. Have clear, recognizable imagery at small sizes
3. Work well on both light and dark backgrounds
4. Follow platform-specific design guidelines

## Tools for Creating Icons
- Figma, Adobe Illustrator, or Sketch for design
- Online tools like https://www.pwabuilder.com/ or https://realfavicongenerator.net/
""")
    print(f'Created {readme_path}')

def main():
    if PIL_AVAILABLE:
        create_icons_with_pil()
    else:
        # Create minimal placeholder if PIL not available
        os.makedirs(ICON_DIR, exist_ok=True)
        print("\nPillow not available. Creating empty placeholder files...")
        print("Install Pillow to generate actual icon images: pip install Pillow")
        for size in SIZES:
            filename = f'icon-{size}x{size}.png'
            filepath = os.path.join(ICON_DIR, filename)
            # Create a minimal 1x1 PNG as placeholder
            with open(filepath, 'wb') as f:
                # Minimal valid PNG
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
            print(f'Created placeholder {filename}')
    
    create_placeholder_readme()
    print("\n✓ Icon setup complete!")

if __name__ == '__main__':
    main()
