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

# get the web page html
response = requests.get("https://www.vatican.va/archive/ENG0015/__P2.HTM")
# define a parsing method for gathering elements of the html
parser = etree.HTMLParser()
# all html lines can be accessed via the tree by parsing
tree = etree.parse(StringIO(str(response.text)), parser)
# define a specific element in the tree to wish to grab
paragraph = tree.xpath('//p[@class="MsoNormal"]/text()')

for i in range(len(paragraph)):
    paragraph[i] = " ".join(paragraph[i].splitlines())
    print(paragraph[i])