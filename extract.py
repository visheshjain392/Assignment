import fitz  # PyMuPDF
from PIL import Image
import os
import json

# Input PDF path
pdf_path = "Simple.pdf"
output_dir = "output_images"
json_output_path = "extracted_data.json"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the PDF
doc = fitz.open(pdf_path)

# Store extracted data
result = []

for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    text = page.get_text()
    images_info = []

    # Extract images
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"page{page_number + 1}_image{img_index + 1}.{image_ext}"
        image_path = os.path.join(output_dir, image_filename)

        # Save image
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        images_info.append(image_path)

    # Append data for this page
    result.append({
        "page": page_number + 1,
        "Question": text.strip(),
        "images": images_info
    })

# Save as JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n✅ Extraction complete. Images saved to '{output_dir}', structured data saved to '{json_output_path}'")