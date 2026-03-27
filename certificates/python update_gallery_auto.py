import os
import fitz  # PyMuPDF
import subprocess

# --- Configuration ---
ROOT_FOLDER = os.getcwd()  # "Gained Certificates"
THUMB_FOLDER = os.path.join(ROOT_FOLDER, "thumbnails")
HTML_FILE = os.path.join(ROOT_FOLDER, "index.html")
AUTO_PUSH = True
COMMIT_MESSAGE = "Auto-update certificates gallery"

# --- Create thumbnails folder if it doesn't exist ---
os.makedirs(THUMB_FOLDER, exist_ok=True)

# --- Function to generate PDF thumbnails ---
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

# --- Generate HTML ---
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

# --- Scan the folder for images and PDFs ---
for f in sorted(os.listdir(ROOT_FOLDER)):
    path = os.path.join(ROOT_FOLDER, f)
    if os.path.isfile(path):
        ext = f.lower().split('.')[-1]
        if ext in ["png", "jpg", "jpeg"]:
            html_content += f"""
    <div class="cert">
        <a href="{f}" target="_blank">
            <img src="{f}" alt="{f}">
            <p>{os.path.splitext(f)[0]}</p>
        </a>
    </div>
"""
        elif ext == "pdf":
            thumb_path = generate_pdf_thumb(path)
            html_content += f"""
    <div class="cert">
        <a href="{f}" target="_blank">
            <img src="thumbnails/{os.path.basename(thumb_path)}" alt="{f}">
            <p>{os.path.splitext(f)[0]}</p>
        </a>
    </div>
"""

html_content += """
</body>
</html>
"""

# --- Write index.html ---
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Gallery updated: {HTML_FILE}")

# --- Optional: auto Git commit & push ---
if AUTO_PUSH:
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print("Git push failed or no changes to commit:", e)