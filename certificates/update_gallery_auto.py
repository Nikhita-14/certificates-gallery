import os
import fitz  # PyMuPDF
import subprocess

# --- Config ---
CERT_FOLDER = "certificates"            # folder with your PDFs/images
THUMB_FOLDER = os.path.join(CERT_FOLDER, "thumbnails")
HTML_FILE = os.path.join(CERT_FOLDER, "index.html")
AUTO_PUSH = True                        # True = push to GitHub automatically
COMMIT_MESSAGE = "Auto-update certificates gallery"

# --- Ensure thumbnails folder exists ---
os.makedirs(THUMB_FOLDER, exist_ok=True)

# --- Function to generate PDF thumbnail ---
def generate_pdf_thumb(pdf_path):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    thumb_path = os.path.join(THUMB_FOLDER, f"{base_name}_Thumb.png")
    if not os.path.exists(thumb_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(thumb_path)
        doc.close()
        print(f"Generated thumbnail for {pdf_path}")
    return thumb_path

# --- Generate dynamic HTML ---
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>My Certificates</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        .cert { display: inline-block; margin: 15px; text-align: center; vertical-align: top; }
        .cert img { width: 200px; height: auto; border: 1px solid #ccc; box-shadow: 2px 2px 5px #aaa; }
        .cert p { margin-top: 5px; font-size: 14px; max-width: 200px; word-wrap: break-word; }
        a { text-decoration: none; color: #000; }
        h1 { margin-bottom: 40px; }
    </style>
</head>
<body>
<h1>My Certificates</h1>
"""

# --- Scan folder ---
files = os.listdir(CERT_FOLDER)
files.sort()

for f in files:
    path = os.path.join(CERT_FOLDER, f)
    if os.path.isfile(path):
        ext = f.lower().split('.')[-1]
        if ext in ["png", "jpg", "jpeg"]:
            # Image certificate
            html_content += f"""
    <div class="cert">
        <a href="{CERT_FOLDER}/{f}" target="_blank">
            <img src="{CERT_FOLDER}/{f}" alt="{f}">
            <p>{os.path.splitext(f)[0]}</p>
        </a>
    </div>
"""
        elif ext == "pdf":
            thumb_path = generate_pdf_thumb(path)
            html_content += f"""
    <div class="cert">
        <a href="{CERT_FOLDER}/{f}" target="_blank">
            <img src="{THUMB_FOLDER}/{os.path.basename(thumb_path)}" alt="{f}">
            <p>{os.path.splitext(f)[0]}</p>
        </a>
    </div>
"""

# --- HTML footer ---
html_content += """
</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Gallery updated: {HTML_FILE}")

# --- Git automatic commit & push ---
if AUTO_PUSH:
    try:
        # Stage all changes including deletions
        subprocess.run(["git", "add", "-A"], cwd=CERT_FOLDER, check=True)
        # Commit with preset message
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], cwd=CERT_FOLDER, check=True)
        # Push to remote
        subprocess.run(["git", "push"], cwd=CERT_FOLDER, check=True)
        print("Changes pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print("Git push failed or no changes to commit:", e)