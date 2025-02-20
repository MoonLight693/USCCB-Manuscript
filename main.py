from Vatican.Vatican import *
import os 
''' 
start system
gets the vatican CCC from online and stores them in a db.
'''
paragraph = parsing("https://www.vatican.va/archive/ENG0015/__P1.HTM")

# copy of last item stitch, used in prologue as prologue CCC has no CCC # associated
i = len(paragraph) - 1
b = [''.join(paragraph[i-1:i+1])]  # join the current and last elements
paragraph = paragraph[:i-1] + b + paragraph[i+1:] # reconstruct the list with the stitch and skip

for i in range(len(paragraph)):
    paragraph[i] = "0$" + paragraph[i]

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

page = "P2"
while page != "P20":
    paragraph = parsing("https://www.vatican.va/archive/ENG0015/__" + page + ".HTM")
    #print(paragraph)
    
    '''logic around the page with the Creeds on them.'''
    if page == "P13":
        paragraph = ['The Apostles Creed$I believe in God the Father almighty, creator of heaven and earth. I believe in Jesus Christ, his only Son, our Lord. He was conceived by the power of the Holy Spirit and born of the Virgin Mary Under Pontius Pilate He was crucified, died, and was buried. He descended to the dead. On the third day he rose again. He ascended into heaven and is seated at the right hand of the Father. He will come again to judge the living and the dead. I believe in the Holy Spirit, the holy catholic Church, the communion of saints, the forgiveness of sins, the resurrection of the body, and the life everlasting. Amen.' ,
                     'The Nicene Creed$We believe in one God, the Father, the Almighty, maker of heaven and earth, of all that is, seen and unseen. We believe in one Lord, Jesus Christ, the only Son of God, eternally begotten of the Father, God from God, Light from Light, true God from true God, begotten, not made, of one Being with the Father. Through him all things were made. For us men and for our salvation, he came down from heaven: by the power of the Holy Spirit he was born of the Virgin Mary, and became man. For our sake he was crucified under Pontius Pilate; he suffered died and was buried. On the third day he rose again in fulfillment of the Scriptures; he ascended into heaven and is seated at the right hand of the Father. He will come again in glory to judge the living and the dead, and his kingdom will have no end. We believe in the Holy Spirit, the Lord, the giver of life, who proceeds from the Father and the Son. With the Father and the Son he is worshipped and glorified. He has spoken through the Prophets. We believe in one holy catholic and apostolic Church. We acknowledge one baptism for the forgiveness of sins. We look for the resurrection of the dead, and the life of the world to come. Amen.']
    else: 
        paragraph = stitching(paragraph)
    
    #print(paragraph)
    appending(paragraph, file_path)
    
    '''parses with '''
    paragraph = parsingI("https://www.vatican.va/archive/ENG0015/__" + page + ".HTM")
    if paragraph:
        paragraph = stitching(paragraph)
        appending(paragraph, file_path)
    
    page = page_next(page)

'''Importing this file adds the vatican web CCC to the database'''
from Vatican.Vatican_to_SQL import *

to_table("/home/whitmercraft939/USCCB-Manuscript-3/State Machine Output/Test Text.txt", "Test_Text")




# Experiment