import os
from PIL import Image
import fitz  # PyMuPDF

BASE_DIR = r"D:\System Stuff\Gained Certificates"
CERT_DIR = os.path.join(BASE_DIR, "certificates")
THUMB_DIR = os.path.join(BASE_DIR, "thumbnails")

os.makedirs(THUMB_DIR, exist_ok=True)

SUPPORTED_IMAGES = (".png", ".jpg", ".jpeg", ".webp")
SUPPORTED_PDFS = (".pdf",)

# Clear old thumbnails (important for rename/delete updates)
for f in os.listdir(THUMB_DIR):
    os.remove(os.path.join(THUMB_DIR, f))

gallery_items = []

def create_pdf_thumbnail(pdf_path, thumb_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap()
    pix.save(thumb_path)

def create_image_thumbnail(img_path, thumb_path):
    img = Image.open(img_path)
    img.thumbnail((400, 400))
    img.save(thumb_path)

for file in os.listdir(CERT_DIR):
    file_path = os.path.join(CERT_DIR, file)
    name, ext = os.path.splitext(file)
    ext = ext.lower()

    thumb_path = os.path.join(THUMB_DIR, name + ".png")

    if ext in SUPPORTED_PDFS:
        create_pdf_thumbnail(file_path, thumb_path)

    elif ext in SUPPORTED_IMAGES:
        create_image_thumbnail(file_path, thumb_path)

    else:
        continue

    clean_name = name.replace("_", " ").replace("-", " ").title()

    gallery_items.append((file, "thumbnails/" + name + ".png", clean_name))

# Generate HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Certificates Gallery</title>

<style>
body {{
    background: #0f0f0f;
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    text-align: center;
}}

h1 {{
    margin-top: 30px;
    font-weight: 300;
}}

.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 25px;
    padding: 40px;
}}

.card {{
    background: #1a1a1a;
    padding: 12px;
    border-radius: 12px;
    transition: 0.25s;
}}

.card:hover {{
    transform: scale(1.05);
}}

img {{
    width: 100%;
    border-radius: 8px;
}}

p {{
    margin-top: 10px;
    font-size: 14px;
    opacity: 0.8;
}}

a {{
    text-decoration: none;
    color: white;
}}

footer {{
    margin: 30px;
    opacity: 0.5;
    font-size: 13px;
}}
</style>

</head>

<body>

<h1>My Certificates</h1>

<div class="gallery">
"""

for file, thumb, clean_name in gallery_items:
    html_content += f"""
    <div class="card">
        <a href="certificates/{file}" target="_blank">
            <img src="{thumb}">
            <p>{clean_name}</p>
        </a>
    </div>
    """

html_content += """
</div>

<footer>© Dittakavi Nikhita</footer>

</body>
</html>
"""

with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Gallery updated successfully.")