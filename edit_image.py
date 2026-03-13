from PIL import Image, ImageDraw, ImageFont
import os

img = Image.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\temp_image.jpg')
w, h = img.size
print(f"Image size: {w}x{h}")

# Create a drawable copy
draw = ImageDraw.Draw(img)

# Try to find a Chinese font
font_paths = [
    r"C:\Windows\Fonts\msyh.ttc",      # Microsoft YaHei
    r"C:\Windows\Fonts\msyhbd.ttc",     # Microsoft YaHei Bold
    r"C:\Windows\Fonts\simhei.ttf",     # SimHei
    r"C:\Windows\Fonts\simsun.ttc",     # SimSun
]

font = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font = ImageFont.truetype(fp, size=48)
            print(f"Using font: {fp}")
            break
        except:
            continue

if not font:
    font = ImageFont.load_default()
    print("Using default font")

text = "我终于知道，为什么总被同一种人吸引！"

# Calculate text position (center-top area)
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
x = (w - tw) // 2
y = h // 4

# Draw a semi-transparent background for readability
padding = 20
bg_box = [x - padding, y - padding, x + tw + padding, y + th + padding]
draw.rectangle(bg_box, fill=(255, 255, 255, 200))

# Draw the text
draw.text((x, y), text, fill=(80, 60, 40), font=font)

# Save
out_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\output_image.jpg'
img.save(out_path, quality=95)
print(f"Saved to: {out_path}")
