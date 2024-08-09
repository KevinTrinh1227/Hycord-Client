from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

def center(x, text, font):
    text = str(text)
    try:
        _, _, text_width, _ = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), text, font=font)
        centered_x = x - (text_width / 2)
        return centered_x
    except Exception as e:
        print(f"Error in center function: {e}")
        return x
    

# Function to calculate the width of text
def get_text_width(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)[2]

    
    
def right_align(x, text, font):
    text = str(text)
    try:
        _, _, text_width, _ = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), text, font=font)
        right_aligned_x = x - text_width
        return right_aligned_x
    except Exception as e:
        print(f"Error in right_align function: {e}")
        return x