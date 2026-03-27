import fitz  # PyMuPDF
import os

# Folder containing your PDFs
pdf_folder = r"D:\System Stuff\Gained Certificates"

# Output folder for thumbnails
thumb_folder = pdf_folder  # same folder, your HTML already points to <PDFNAME>_Thumb.png

# Loop through all PDFs
for file in os.listdir(pdf_folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file)
        thumb_name = f"{os.path.splitext(file)[0]}_Thumb.png"
        thumb_path = os.path.join(thumb_folder, thumb_name)

        # Skip if thumbnail already exists
        if os.path.exists(thumb_path):
            print(f"Thumbnail already exists for {file}")
            continue

        print(f"Processing: {file}")
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # first page
        zoom = 2  # better quality
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        pix.save(thumb_path)

print("All PDF thumbnails generated!")