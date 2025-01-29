'''
Author: Evan Whitmer
Last Date Modified: January 17, 2025
Description: This script uses wget command to bulk download the 
Vatican Catechism at https://www.vatican.va/archive/ENG0015/_INDEX.HTM. 
Then, parses the Paragraph and its number into a usable table.
Links to additional resources:
- https://www.youtube.com/watch?v=mRuK_zSw1oI - How to scrape websites using python and lxml
- https://www.geeksforgeeks.org/python-removing-newline-character-from-string/#using-strsplitlines-and-strjoin - split line tutorial
'''

from Vatican_prologue import *

def appending(paragraph, file_path):
    '''Appending to CSV'''
    # Simple
    # Assisted by Dominic Antony
    f = open(file_path, "a")
    for p in paragraph: f.write(p + "\n")
    f.close()

def stitching(paragraph):
    ''' stitch the paragraphs together so each element is one CCC paragraph '''
    x = len(paragraph) - 1
    i=0
    while i < x:
        if not paragraph[i][0].isdigit() and i == 0:
            # if there are additional strings that are not CCC at the beginning of the paragraph list, remove them
            paragraph.pop(0)
            x -= 1
        elif not paragraph[i][0].isdigit():
            # if the start of the string is not the CCC number and is not the first paragraph in the list
            b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
            paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip
            x = x-1 # decrease the count of length of list
            i += 1 # move to next element
        else: i += 1 # element contains CCC number, so do nothing

    # fail safe check for if the last item in the paragraph list was skipped in stitching
    if paragraph[-1][0] == " ":
        b = [''.join(paragraph[i-1:i+1])]
        paragraph = paragraph[:i-1] + b + paragraph[i+1:]
    
    return paragraph

paragraph = parsing("https://www.vatican.va/archive/ENG0015/__P2.HTM")
paragraph = stitching(paragraph)
appending(paragraph, file_path)