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
    
    if not paragraph:
        # if paragpraph empty, then your at a brief page in CCC
        paragraph = tree.xpath('//p[@class="MsoNormal"]/i/text()')

    # remove the string gargen : \n\r, \n, footnote markers
    for i in range(len(paragraph)):
        paragraph[i] = " ".join(paragraph[i].splitlines())
        
    return paragraph

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
    if not paragraph[-1][0].isdigit():
        b = [''.join(paragraph[-2:])]
        paragraph = paragraph[:-2] + b 
    
    return paragraph

def appending(paragraph, file_path):
    '''Appending to CSV'''
    # Simple
    # Assisted by Dominic Antony
    f = open(file_path, "a")
    for p in paragraph: f.write(p + "\n")
    f.close()

def page_next(page):
    # all possible values for the page keys
    '''Used to iterate through the pages of the Vatican website'''
    iterate = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
               'U', 'V', 'W', 'X', 'Y', 'Z']
    page_list = list(page)      # convert string to list for list comprension replacement
    
    '''
    cases: 
    - increment through the first 36 pages
    - increament to 37th page
    - increment after 37th page
    '''
    if len(page_list) == 2:
        if page_list[-1] != "Z":
            page_list[-1] = iterate[iterate.index(page_list[-1]) + 1]
        else:
            page_list = list("P10")
    else:
        if page_list[-1] != "Z":
            page_list[-1] = iterate[iterate.index(page_list[-1]) + 1]
        else:
            page_list[-2] = iterate[iterate.index(page_list[-2]) + 1]
            page_list[-1] = iterate[0]
    
    res = ''.join(page_list)
    return res

# MAIN #

paragraph = parsing("https://www.vatican.va/archive/ENG0015/__P1.HTM")

# copy of last item stitch, used in prologue as prologue CCC has no CCC # associated
i = len(paragraph) - 1
b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip

for i in range(len(paragraph)):
    paragraph[i] = "PROLOGUE " + paragraph[i]

''' Write to CSV: initialization'''
# remove previous output if exists
file_path = "Vatican/new_table.txt"
if os.path.exists(file_path):
    os.remove(file_path)

# Simple
# Assisted by Dominic Antony
f = open(file_path, "w")
for p in paragraph: f.write(p + "\n")
f.close()

page = "P2"
while page != "PF":
    paragraph = parsing("https://www.vatican.va/archive/ENG0015/__" + page + ".HTM")
    paragraph = stitching(paragraph)
    appending(paragraph, file_path)
    page = page_next(page)