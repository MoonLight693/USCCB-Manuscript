import os
import shutil
import requests
import json
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

def extract_quoted_and_cited(text):
    """
    Extracts text within standard or smart quotes and their immediately following citations in parentheses.
    Removes newline characters from the extracted content, replacing them with spaces.
    """
    extracted_parts = []
    # Regex to find text within standard or smart double quotes
    quote_pattern = r'["“”](.*?)(?:"|”)'
    matches = re.finditer(quote_pattern, text, re.DOTALL)

    for match in matches:
        quote = match.group(1).strip().replace('\n', ' ')  # Replace enters with spaces in the quote
        # Try to find a citation immediately after the quote
        citation_match = re.search(r'\s*\(([^)]*)\)', text[match.end():])
        if citation_match:
            citation = citation_match.group(1).strip().replace('\n', ' ')  # Replace enters with spaces in the citation
            extracted_parts.append(f'"{quote}" ({citation})')
        else:
            extracted_parts.append(f'"{quote}"')

    return "\n".join(extracted_parts)

# Assuming your extract_text_from_pdf function is defined as follows:
def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        extracted_text = ""
        for i, image in enumerate(images):
            print(f"Processing page {i+1}...")
            text = pytesseract.image_to_string(image)
            extracted_text += text
            extracted_text += "\n\n"
        return extracted_text.strip()
    except Exception as e:
        print(f"An error occurred during PDF text extraction: {e}")
        return None

def interact_with_ollama(prompt, model="llama3.2", temperature=None):
    """
    Interacts with the Ollama API to generate text.

    Args:
        prompt (str): The prompt to send to Ollama.
        model (str, optional): The Ollama model to use. Defaults to "llama3.2".
        temperature (float, optional): The temperature parameter for controlling randomness. Defaults to None (Ollama's default).

    Returns:
        str: The generated text from Ollama, or None if an error occurs.
    """
    try:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "prompt": prompt,
            "model": model,
            "stream": False
        }
        if temperature is not None:
            data["temperature"] = temperature

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        full_response = ""
        for line in response.text.splitlines():
            if line.strip():
                try:
                    json_line = json.loads(line)
                    if 'response' in json_line:
                        full_response += json_line['response']
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON line: {e}, line: {line}")
                    continue

        return full_response.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding Ollama response: {e}")
        return None

# 2. Define the main processing function with a return value
def process_pdf_with_ollama(pdf_file_path, output_folder, ollama_model="llama3.2", ollama_temperature=None) -> bool:
    """
    Extracts text from a PDF, prunes it to keep only quotes and citations,
    feeds the pruned text to Ollama with instructions,
    saves the output.
    Returns True if the process completes successfully, False otherwise.

    Args:
        pdf_file_path (str): The path to the PDF file to process.
        output_folder (str): The path to the folder where the output text file will be saved.
        ollama_model (str, optional): The Ollama model to use. Defaults to "llama3.2".
        ollama_temperature (float, optional): The temperature parameter for Ollama. Defaults to None.

    Returns:
        bool: True if the process was successful, False otherwise.
    """
    fixed_instructions = """
    Here are some instructions for the following text:

    Include the $ in between the Reference + Reference Number and the Quote do not use any other symbol. Do not include the quotation marks around the quote. Do NOT have any intoduction give me only the block of text. The output format is very strict and must follow the rules. Extract ALL quotes and their reference in this EXACT format with NO deviation:

    Reference + Reference Number$Quote
    Reference + Reference Number$Quote
    Reference + Reference Number$Quote

    : Here is the text you are supposed to do this on:

    """
    success = False

    try:
        print(f"Processing file: {pdf_file_path}")

        # 1. Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_file_path)

        if extracted_text:
            print("\n--- Extracted Text Before Pruning ---")
            print(extracted_text)
            print("---\n")

            # Prune the extracted text to keep only quotes and citations
            pruned_text = extract_quoted_and_cited(extracted_text)

            print("\n--- Pruned Text After Pruning ---")
            print(pruned_text)
            print("---\n")

            # 2. Create the prompt for Ollama with the pruned text
            ollama_prompt = f"{fixed_instructions}\n\n---\n{pruned_text}\n---"

            # 3. Feed the text into Ollama
            print("Sending pruned text to Ollama...")
            ollama_response = interact_with_ollama(ollama_prompt, model=ollama_model, temperature=ollama_temperature)

            if ollama_response:
                # 4. Save the output to a text file
                base_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
                output_file_name = f"{base_name}.txt"
                output_path = os.path.join(output_folder, output_file_name)

                # Create the output folder if it doesn't exist
                os.makedirs(output_folder, exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(ollama_response)
                print(f"Ollama response saved to: {output_path}")

                success = True  # Set success to True if all steps completed

            else:
                print("Error: No response received from Ollama.")

        else:
            print("Error: Could not extract text from the PDF.")

    except Exception as e:
        print(f"An error occurred during the overall process: {e}")
        success = False  # Set success to False if any exception occurred

    return success

# 3. Example usage (you would call this function with your specific file paths)
if __name__ == "__main__":
    pdf_file = "AI State Machine Input\Jesus Christ The Savior and Redeemer of Humanity V2 GPT.pdf"  # Replace with the actual path to your input PDF file
    output_dir = "AI State Machine Output"
    process_successful = process_pdf_with_ollama(pdf_file, output_dir, ollama_temperature=0.9)

    if process_successful:
        print("PDF processing completed successfully.")
    else:
        print("PDF processing failed.")