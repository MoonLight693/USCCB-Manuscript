import fitz  # PyMuPDF

def highlight_sentences(pdf_path, output_path, sentences):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Iterate through pages
    for page in pdf_document:
        # Iterate through the list of sentences
        for sentence in sentences:
            # Search for the sentence
            text_instances = page.search_for(sentence)

            # Highlight each instance
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.update()

    # Save the modified PDF
    pdf_document.save(output_path)
    print(f"✅ Highlighted text saved to {output_path}")

# Example usage
sentences_to_highlight = [
    "The desire for God is written on the human heart, because [you have been] created by God and for God” (CCC 27).",
    "I am the way and the truth and the life” (Jn 14:5, 6)",
]
