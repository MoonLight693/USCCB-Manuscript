import os
from PyPDF2 import PdfReader

def convert_pdfs_to_text(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, 'w') as text_file:
            text_file.write(text)
            
#convert_pdfs_to_text("USCCB Test Input Directory", "USCCB Test Output Directory")