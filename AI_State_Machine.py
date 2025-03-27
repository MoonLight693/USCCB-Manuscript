import google.generativeai as genai
from PIL import Image  # Added import for Pillow Image
from io import BytesIO
from pdf2image import convert_from_path
import pytesseract
import config
import os  # Import the os module for file path operations

# Initialize the client (Corrected client initialization)
genai.configure(api_key=config.API_KEY)


def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    return images

def extract_text_from_image(image):
    # Use pytesseract to extract text from image
    text = pytesseract.image_to_string(image)
    return text

def extract_images_and_text_from_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    text_data = [] # Changed variable name to text_data to avoid confusion
    image_data = []

    for i, img in enumerate(images): # Added enumerate to track page number (index i)
        # Convert image to byte array
        img_byte_array = BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)  # Rewind the byte stream

        # Extract text from image (Uncommented to enable text extraction)
        extracted_text = extract_text_from_image(img)
        text_data.append(extracted_text) # Append extracted text
        image_data.append(img_byte_array.getvalue()) # Append image data

        print(f"Extracted data from page {i+1} of {pdf_path}") # Debug print: Page processing confirmation

    return image_data, text_data # Return both image_data and text_data

def ai_state_machine(pdf_path, instructions):
    image_data, extracted_text_data = extract_images_and_text_from_pdf(pdf_path) # Get both image_data and extracted_text

    contents = [] # List to hold content for each page

    for i, img_bytes in enumerate(image_data): # Enumerate to track page number (index i)
        pil_image = Image.open(BytesIO(img_bytes)) # Open image bytes with Pillow
        page_text = extracted_text_data[i] # Get corresponding text for the page

        # Construct content using dictionaries - Corrected structure
        content_dict = {
            "parts": [
                { # Image Part
                    "inline_data": { # "inline_data" for image blob
                        "mime_type": "image/png",
                        "data": img_bytes  # Pass image byte data directly
                    }
                },
                { # Text Part - Include extracted text for each page
                    "text": f"Page {i+1} OCR Text:\n{page_text}\n\nInstructions: {instructions}" # Combine page text and instructions
                }
            ],
            "role": "user" # Role of the content
        }
        contents.append(content_dict) # Append the dictionary to contents
        print(f"Prepared content for page {i+1} of {pdf_path}") # Debug print: Content preparation confirmation

    print(f"Sending {len(contents)} pages from {pdf_path} to Gemini API...") # Debug print: Total pages being sent

    # Instantiate the GenerativeModel (ensure you use a model that supports images - vision models)
    model = genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp")

    # Use generate_content with the list of content dictionaries
    response = model.generate_content(
        contents=contents, # Now passing a list of content dictionaries (one per page)
        generation_config=genai.GenerationConfig(temperature=0.7, candidate_count=1),
        request_options={"timeout": 300}  # Increase timeout (e.g., 5 minutes)
    )

    return response

# --- File Output Section ---
output_directory = "State Machine Output"  # **Hardcoded output directory - CHANGE THIS TO YOUR DESIRED PATH**
input_directory = "USCCB Test Input Directory" # **Hardcoded input directory - CHANGE THIS TO YOUR INPUT DIRECTORY**

instructions = """
Extract all quotes from the Catechism of the Catholic Church (CCC) and any other references in the format:

Reference$Quote

Example output:

123$This is a quote.  
353$This is an example.  
Glossary$Example. This is an example. Words.  
Matthew 22:37-39$You shall love the Lord your God with all your heart, with all your soul, and with all your mind. This is the greatest and first commandment. And a second is like it: You shall love your neighbor as yourself.  
John 20:28$My Lord and my God!

Follow these strict rules:
Extract only direct quotes with their reference numbers.
Format must always be Reference$Quote without quotation marks.
If a reference or quote is missing, exclude it.
Include both footnotes and direct quotes.
Your task is to extract and return only the formatted list, with no additional text.
CCC references and quotes should look like
CCC 123$This is a quote.
NOT
123$This is a quote.

a quote could look like:
The  Bible  explicitly  declares  Jesus  as  the  Son  of  God,  affirming  His  divine  nature.  In  John  1:1,  it 
 is  written,  "In  the  beginning  was  the  Word,  and  the  Word  was  with  God,  and  the  Word  was  God." 
the output should be:
John 1:1$In the beginning was the Word, and the Word was with God, and the Word was God.
"""

# --- Process all PDF files in input directory ---
pdf_files_in_directory = [f for f in os.listdir(input_directory) if f.lower().endswith('.pdf')] # List PDF files

print(f"Found {len(pdf_files_in_directory)} PDF files in {input_directory}") # Debug print: Number of PDFs found

for pdf_filename in pdf_files_in_directory:
    pdf_path = os.path.join(input_directory, pdf_filename)
    print(f"\nProcessing PDF: {pdf_path}") # Debug print: Processing start for each PDF
    response = ai_state_machine(pdf_path, instructions)

    # --- Construct output filename based on input PDF ---
    pdf_filename_base = os.path.splitext(os.path.basename(pdf_path))[0] # Get filename without extension
    output_filename = f"{pdf_filename_base}_gemini_output.txt" # Create output filename
    output_filepath = os.path.join(output_directory, output_filename)

    # --- Accumulate AI responses (text only) ---
    all_responses_text = ""
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content.parts:
                ai_response_text = candidate.content.parts[0].text # Extract only AI response text
                all_responses_text += ai_response_text + "\n\n"

    # --- File Writing (CONDITIONAL - only if response contains '$') ---
    if '$' in all_responses_text: # Check if all_responses_text contains '$'
        try:
            os.makedirs(output_directory, exist_ok=True) # Create directory if it doesn't exist
            with open(output_filepath, "w", encoding="utf-8") as outfile:
                outfile.write(all_responses_text.strip()) # Write to file, strip whitespace
            print(f"Gemini responses saved to: {output_filepath}")
        except Exception as e:
            print(f"Error writing responses to file for {pdf_filename}: {e}")
    else:
        print(f"No quotes found (no '$' in response) in {pdf_filename}. Output file NOT created.") # Message for empty response


print("\n--- PDF Processing Complete ---") # Final completion message