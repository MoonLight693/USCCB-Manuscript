import os
import pdfplumber

def convert_pdfs_to_text(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        with pdfplumber.open(filepath) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

convert_pdfs_to_text("USCCB Test Input Directory", "USCCB Test Output Directory")