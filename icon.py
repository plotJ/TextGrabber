from PIL import Image, ImageDraw

def create_icon():
    # Create a new image with a white background
    image = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple "T" icon
    draw.rectangle([8, 8, 56, 16], fill='black')  # Top bar
    draw.rectangle([28, 16, 36, 56], fill='black')  # Vertical bar
    
    return image

if __name__ == '__main__':
    icon = create_icon()
    icon.save('icon.png')
