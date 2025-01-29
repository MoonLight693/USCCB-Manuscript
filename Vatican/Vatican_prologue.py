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

''' Request and parse Paragraph from Vatican CCC'''
from lxml import etree
import requests
from io import StringIO
import os

def parsing(URL):
    # define a parsing method for gathering elements of the html
    parser = etree.HTMLParser()

    # get the web page html
    response = requests.get(URL)
    # all html lines can be accessed via the tree by parsing
    tree = etree.parse(StringIO(str(response.text)), parser)
    # define a specific element in the tree to wish to grab
    paragraph = tree.xpath('//p[@class="MsoNormal"]/text()')

    # remove the string gargen : \n\r, \n, footnote markers
    for i in range(len(paragraph)):
        paragraph[i] = " ".join(paragraph[i].splitlines())
    return paragraph

paragraph = parsing("https://www.vatican.va/archive/ENG0015/__P1.HTM")

# copy of last item stitch, used in prologue as prologue CCC has no CCC # associated
i = len(paragraph) - 1
b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip

''' Write to CSV: initialization'''
# remove previous output if exists
file_path = "Vatican/new_table.csv"
if os.path.exists(file_path):
    os.remove(file_path)

# Simple
# Assisted by Dominic Antony
f = open(file_path, "w")
for p in paragraph: f.write(p + "\n")
f.close()