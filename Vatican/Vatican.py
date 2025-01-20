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

from lxml import etree
import requests
from io import StringIO

# define a parsing method for gathering elements of the html
parser = etree.HTMLParser()

# get the web page html
response = requests.get("https://www.vatican.va/archive/ENG0015/__P3.HTM")
# all html lines can be accessed via the tree by parsing
tree = etree.parse(StringIO(str(response.text)), parser)
# define a specific element in the tree to wish to grab
paragraph = tree.xpath('//p[@class="MsoNormal"]/text()')

# remove the string gargen : \n\r, \n, footnote markers
for i in range(len(paragraph)):
    paragraph[i] = " ".join(paragraph[i].splitlines())

# stitch the paragraphs together so each element is 1 CCC paragraph
x = len(paragraph)
i=0
while i < x:
    if not paragraph[i][0].isdigit() and i != 0:
        # if the start of the string is not the CCC number and is not the first paragraph in the list
        b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
        paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip
        x = x-1 # decrease the count of length of list
        i += 1 # move to next element
    else: i += 1 # element contains CCC number, so do nothing

import csv
import os

# remove previous output if exists
file_path = "Vatican/new_table.csv"
if os.path.exists(file_path):
    os.remove(file_path)

CCC = 4
with open(file_path, "w", newline='') as new_file:
    cvs_writer = csv.writer(new_file, delimiter=":")
    a = []
    for i in range(len(paragraph)):
        paragraph[i] = paragraph[i].replace(str(CCC) + " ", "")
        a.append(str(CCC))
        CCC += 1
    cvs_writer.writerows(zip(a,paragraph))