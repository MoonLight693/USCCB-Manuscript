'''
Author: Josh Atkinosn and Christopher Bareras
Last Date Modified: 2/13/25
Description: This script will handle all manuscript quotations 
Vatican Catechism at https://www.vatican.va/archive/ENG0015/_INDEX.HTM. 
Then, parses the Paragraph and its number into a usable table.
Links to additional resources:
'''

import os
import re

def state_machine(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Updated regular expression to ensure quotes are directly followed by a valid reference (CCC with number or Glossary)
    pattern = r'“([^”]+)”\s*\(CCC[.,]?\s*(\d+|Glossary)\s*(?:[^)]+)?\)'
    
    # Find all matches
    matches = [
        (re.sub(r'\s+', ' ', match.group(2) or '').strip(),  # Reference (number or Glossary)
         re.sub(r'\s+', ' ', match.group(1)).strip(),  # Quote
         match.start(1),  # Capture the start position of the quote
         match.end(1))  # Capture the end position of the quote
        for match in re.finditer(pattern, text, re.DOTALL)
    ]
    
    # If no matches, do not create the output file
    if not matches:
        return False  # Indicate no output was created

    # Remove numbers from the quote before writing to the output file
    processed_matches = [
        (reference, re.sub(r'\d+', '', quote))  # Only keep reference and quote
        for reference, quote, _, _ in matches  # Ignore start and end positions
    ]
    
    # Write results to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for reference, quote in processed_matches:
            file.write(f"{reference}${quote}\n")
    
    return True  # Indicate that output was created

def process_directory(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through all .txt files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            
            # Process the file and check if output was created
            output_created = state_machine(input_file, output_file)
            if output_created:
                print(f"Processed: {input_file} -> {output_file}")
            else:
                print(f"Skipped: {input_file} (no valid quotes with quotation marks or invalid references)")

# Example usage:
process_directory("USCCB Test Output Directory", "State Machine Output")
