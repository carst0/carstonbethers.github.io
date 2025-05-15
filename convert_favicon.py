from cairosvg import svg2png

# Read the SVG file
with open('favicon.svg', 'rb') as svg_file:
    svg_content = svg_file.read()

# Convert to PNG
svg2png(bytestring=svg_content,
        write_to='favicon.png',
        output_width=32,
        output_height=32) 