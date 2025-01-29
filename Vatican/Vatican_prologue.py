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

# define a parsing method for gathering elements of the html
parser = etree.HTMLParser()

# get the web page html
response = requests.get("https://www.vatican.va/archive/ENG0015/__P1.HTM")
# all html lines can be accessed via the tree by parsing
tree = etree.parse(StringIO(str(response.text)), parser)
# define a specific element in the tree to wish to grab
paragraph = tree.xpath('//p[@class="MsoNormal"]/text()')

# remove the string gargen : \n\r, \n, footnote markers
for i in range(len(paragraph)):
    paragraph[i] = " ".join(paragraph[i].splitlines())

''' stitch the paragraphs together so each element is 1 CCC paragraph '''
# only the last part is need of restitching
i=3
b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip

print(paragraph)

# Write to CSV
import csv
import os

# remove previous output if exists
file_path = "Vatican/new_table.csv"
if os.path.exists(file_path):
    os.remove(file_path)

CCC = 0
a = [0,0,0,]
#with open(file_path, 'w', newline='') as f:
#    writer = csv.writer(f, delimiter=':', quoting=csv.QUOTE_ALL, quotechar='\"')
#    writer.writerows(zip(a,paragraph))
data = [
    ["Value 1", "Value 2", "Value 3"],
    ["Value, 4", "Value 5", "Value 6"],
    ["Value 7", "Value \"8\"", "Value 9"]
]

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter=":", quotechar='\"', quoting=csv.QUOTE_NONE, escapechar='\"')
    for row in data:
        writer.writerow(row)