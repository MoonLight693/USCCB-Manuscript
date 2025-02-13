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
    
    banned = ['Part One: the Profession of Faith','Part Two: the Sacraments of Faith', 'Part Three: the Life of Faith',
              'Part Four: Prayer in the Life of Faith', 'Above all - Charity', 'The covenant with Noah', 'God chooses Abraham',
              'God forms his people Israel', 'God has said everything in his Word', 'There will be no further Revelation',
              '. . . continued in apostolic succession', 'One common source. . .', '. . . two distinct modes of transmission',
              'Apostolic Tradition and ecclesial traditions', 'The heritage of faith entrusted to the whole of the Church',
              'The Magisterium of the Church', 'The dogmas of the faith', 'The supernatural sense of faith', 'Growth in understanding the faith',
              'The Old Testament', 'The New Testament', 'The unity of the Old and New Testaments', 'Abraham - "father of all who believe"',
              'Mary - "Blessed is she who believed"', 'To believe in God alone', 'To believe in Jesus Christ, the Son of God',
              'To believe in the Holy Spirit', 'Faith is a grace', 'Faith is a human act', 'Faith and understanding', 'The freedom of faith',
              'The necessity of faith', 'Perseverance in faith', 'Faith - the beginning of eternal life', 'I. "I BELIEVE IN ONE GOD"',
              'II. GOD REVEALS HIS NAME', 'The living God', '"I Am who I Am"', '"A God merciful and gracious"', 'God alone IS',
              'III. GOD, "HE WHO IS", IS TRUTH AND LOVE', 'God is Truth', 'God is Love', 'IV. THE IMPLICATIONS OF FAITH IN ONE GOD',
              'IN BRIEF']
    
    x = len(paragraph) - 1
    i=0
    
    while i < x:
        '''This loop removes banned phrases/subheaders that aren't paragraphs.'''
        if paragraph[i] in banned:
            #print(f"popped: {paragraph.pop(i)}")
            paragraph.pop(i)
            x-=1
        else: i+=1
    
    i = 0
    while i < x:
        print('-------------------------------')
        print(paragraph[i])
        if not paragraph[i][0].isdigit() and i == 0:
            # if there are additional strings that are not CCC at the beginning of the paragraph list, remove them
            paragraph.pop(0)
            x -= 1      
        elif not paragraph[i][0].isdigit():
            print('STITCHING...')
            # if the start of the string is not the CCC number and is not the first paragraph in the list
            b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
            paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip
            x = x-1 # decrease the count of length of list
            #todo: removed and fixed the process of stitching. i += 1 # move to next element
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
    #f.write("\n")
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
    paragraph[i] = "0 " + paragraph[i]

''' Write to CSV: initialization'''
# remove previous output if exists
file_path = "Vatican/CCC_table.txt"
if os.path.exists(file_path):
    os.remove(file_path)

# Simple
# Assisted by Dominic Antony
f = open(file_path, "w")
for p in paragraph: f.write(p + "\n")
f.close()

page = "P10"
while page != "P20":
    paragraph = parsing("https://www.vatican.va/archive/ENG0015/__" + page + ".HTM")
    #print(paragraph)
    
    '''logic around the page with the Creeds on them.'''
    if page == "P13":
        paragraph = ['-4 The Apostles Creed I believe in God the Father almighty, creator of heaven and earth. I believe in Jesus Christ, his only Son, our Lord. He was conceived by the power of the Holy Spirit and born of the Virgin Mary Under Pontius Pilate He was crucified, died, and was buried. He descended to the dead. On the third day he rose again. He ascended into heaven and is seated at the right hand of the Father. He will come again to judge the living and the dead. I believe in the Holy Spirit, the holy catholic Church, the communion of saints, the forgiveness of sins, the resurrection of the body, and the life everlasting. Amen.' ,
                     '-5 The Nicene Creed We believe in one God, the Father, the Almighty, maker of heaven and earth, of all that is, seen and unseen. We believe in one Lord, Jesus Christ, the only Son of God, eternally begotten of the Father, God from God, Light from Light, true God from true God, begotten, not made, of one Being with the Father. Through him all things were made. For us men and for our salvation, he came down from heaven: by the power of the Holy Spirit he was born of the Virgin Mary, and became man. For our sake he was crucified under Pontius Pilate; he suffered died and was buried. On the third day he rose again in fulfillment of the Scriptures; he ascended into heaven and is seated at the right hand of the Father. He will come again in glory to judge the living and the dead, and his kingdom will have no end. We believe in the Holy Spirit, the Lord, the giver of life, who proceeds from the Father and the Son. With the Father and the Son he is worshipped and glorified. He has spoken through the Prophets. We believe in one holy catholic and apostolic Church. We acknowledge one baptism for the forgiveness of sins. We look for the resurrection of the dead, and the life of the world to come. Amen.']
    else: 
        paragraph = stitching(paragraph)
    
    #print(paragraph)
    appending(paragraph, file_path)
    page = page_next(page)