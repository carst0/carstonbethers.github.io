from PIL import Image, ImageDraw
import os

def create_favicon():
    # Create a new image with a black background
    img = Image.new('RGB', (32, 32), 'black')
    draw = ImageDraw.Draw(img)
    
    # Draw C
    draw.rectangle([8, 10, 10, 22], fill='white')  # Vertical line
    draw.rectangle([8, 10, 14, 12], fill='white')  # Top horizontal
    draw.rectangle([8, 20, 14, 22], fill='white')  # Bottom horizontal
    
    # Draw B
    draw.rectangle([16, 10, 18, 22], fill='white')  # Vertical line
    draw.rectangle([18, 10, 22, 12], fill='white')  # Top horizontal
    draw.rectangle([18, 15, 22, 17], fill='white')  # Middle horizontal
    draw.rectangle([18, 20, 22, 22], fill='white')  # Bottom horizontal
    draw.rectangle([22, 11, 23, 15], fill='white')  # Top curve
    draw.rectangle([22, 17, 23, 21], fill='white')  # Bottom curve
    
    # Save the image
    img.save('favicon.png')
    print("Created favicon.png")

if __name__ == "__main__":
    create_favicon() 