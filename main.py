import requests
import os
from PIL import Image, ImageDraw, ImageFont
import random
import string

GITHUB_API_URL = "https://api.github.com/repos/google/fonts/contents/apache"

def generate_random_text(length=6):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def download_font(url, font_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(font_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded font: {font_path}")
    else:
        print(f"Failed to download font from {url}")

def download_all_fonts():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        fonts = response.json()
        for font in fonts:
            if font['name'].endswith('.ttf'):
                font_url = font['download_url']
                font_path = font['name']
                if not os.path.exists(font_path):
                    print(f"Font {font_path} not found. Downloading...")
                    download_font(font_url, font_path)
    else:
        print(f"Failed to fetch font list from {GITHUB_API_URL}")

def get_random_font(size=55):
    fonts = [f for f in os.listdir() if f.endswith('.ttf')]
    if fonts:
        font_path = random.choice(fonts)
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            print(f"Failed to load font {font_path}. Trying another font.")
            if os.path.exists(font_path):
                os.remove(font_path)
            return get_random_font(size)
    else:
        download_all_fonts()
        return get_random_font(size)

def get_opposite_color(color):
    return tuple(255 - c for c in color)

def create_captcha_image(text, width=200, height=100):
    # Generate a random background color
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    opposite_color = get_opposite_color(background_color)
    
    # Create a background image with the random color
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    # Draw each character individually with random rotation and font
    for i, char in enumerate(text):
        font = get_random_font()
        char_image = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((0, 0), char, font=font, fill=opposite_color)
        
        # Rotate the character
        char_image = char_image.rotate(random.randint(-30, 30), expand=1)
        
        # Paste the character onto the main image
        x = 20 + i * 30
        y = random.randint(10, 40)
        image.paste(char_image, (x, y), char_image)
    
    # Add random lines
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=opposite_color, width=2)
    
    # Add random dots
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        dot_size = random.randint(1, 5)  # Random dot size between 1 and 5
        draw.ellipse((x, y, x + dot_size, y + dot_size), fill=opposite_color)
    
    return image

def save_captcha_image(image, text):
    # Create the "pics" directory if it doesn't exist
    if not os.path.exists("pics"):
        os.makedirs("pics")
    
    file_path = os.path.join("pics", f"{text}.png")
    image.save(file_path)

if __name__ == "__main__":
    i = 0
    l = 10
    while i < l:
        captcha_text = generate_random_text()
        captcha_image = create_captcha_image(captcha_text)
        save_captcha_image(captcha_image, captcha_text)
        print(f"Captcha generated with text: {captcha_text}")
        i += 1