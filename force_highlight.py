import fitz  # PyMuPDF

def highlight_multiline_quotes(pdf_path, output_path, quotes):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Normalize each quote: remove line breaks and extra spaces
    normalized_quotes = [" ".join(q.strip().split()) for q in quotes]

    # Iterate over each page in the PDF
    for page in doc:
        # Extract all words along with their positions
        words = page.get_text("words")  # Each word: (x0, y0, x1, y1, "word", block, line, word)
        
        # Sort words top-to-bottom, then left-to-right for proper reading order
        words.sort(key=lambda w: (w[1], w[0]))

        # Reconstruct the page text as a single string while tracking word positions
        full_text = ""
        word_positions = []
        for w in words:
            full_text += w[4] + " "  # Append word and a space
            word_positions.append(w)  # Save the word position for later use

        full_text = full_text.strip()  # Clean trailing space

        # Go through each quote and try to find it in the reconstructed page text
        for quote in normalized_quotes:
            # Locate the starting index of the quote in the full page text
            start_idx = full_text.find(quote)
            if start_idx == -1:
                continue  # Quote not found on this page, move on to the next

            # Calculate the ending index of the quote
            end_idx = start_idx + len(quote)

            # Initialize variables to keep track of which words match the quote
            current_idx = 0
            start_word_i = None
            end_word_i = None

            # Walk through the list of words to determine the word range for the quote
            for i, w in enumerate(word_positions):
                word = w[4]
                word_len = len(word) + 1  # +1 because we added a space during text construction

                # Find the first word that overlaps the quote's start index
                if current_idx <= start_idx < current_idx + word_len:
                    start_word_i = i
                # Find the first word that overlaps the quote's end index
                if current_idx < end_idx <= current_idx + word_len:
                    end_word_i = i
                    break  # We found the full span of the quote

                current_idx += word_len  # Move the index forward

            # If both start and end words are found, highlight them
            if start_word_i is not None and end_word_i is not None:
                # Create rectangles for each word in the matched range
                rects = [fitz.Rect(*word_positions[i][:4]) for i in range(start_word_i, end_word_i + 1)]

                # Add a highlight annotation over the matching text
                highlight = page.add_highlight_annot(rects)
                highlight.update()

    # Save the updated PDF to a new file
    doc.save(output_path)
    print(f"Highlights saved to {output_path}")
