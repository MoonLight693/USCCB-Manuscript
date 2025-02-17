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
    '''Used to grab paragraphs from Vatican catechism website. If the tree returns blank, autocheckes for italicized texted instead.'''
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

def parsingI(URL):
    '''used to grab the italicize paragraph. Hot fix for pages that have normal and italicized text.'''
    # define a parsing method for gathering elements of the html
    parser = etree.HTMLParser()

    # get the web page html
    response = requests.get(URL)
    # all html lines can be accessed via the tree by parsing
    tree = etree.parse(StringIO(str(response.text)), parser)

    # grabs italicize paragraph, then your at a brief page in CCC
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
              'IN BRIEF', 'I. "IN THE NAME OF THE FATHER AND OF THE SON AND OF THE HOLY SPIRIT"', 'II. THE REVELATION OF GOD AS TRINITY',
              'The Father revealed by the Son', 'The Father and the son revealed by the spirit', 'III. THE HOLY TRINITY IN THE TEACHING OF THE FAITH',
              'The formation of the Trinitarian dogma', 'The dogma of the Holy Trinity', 'IV. THE DIVINE WORKS AND THE TRINITARIAN MISSIONS'
              'IN BRIEF', "The mystery of God's apparent powerlessness", 'IN BRIEF', 'I. CATECHESIS ON CREATION', 'II. CREATION - WORK OF THE HOLY TRINITY',
              'III. "THE WORLD WAS CREATED FOR THE GLORY OF GOD"', 'IV. THE MYSTERY OF CREATION', 'God creates by wisdom and love',
              'God creates an ordered and good world', 'God transcends creation and is present to it', 'God upholds and sustains creation', 
              'V. GOD CARRIES OUT HIS PLAN: DIVINE PROVIDENCE', 'Providence and secondary causes', 'Providence and the scandal of evil', 'IN BRIEF',
              'I. THE ANGELS', 'The existence of angels - a truth of faith', 'Who are they?', 'Christ "with all his angels"', 'The angels in the life of the Church',
              'II. THE VISIBLE WORLD', 'IN BRIEF', 'I. "IN THE IMAGE OF GOD"', 'II. "BODY AND SOUL BUT TRULY ONE"', 'III. "MALE AND FEMALE HE CREATED THEM"',
              'Equality and difference willed by God', '"Each for the other" - "A unity in two"', 'IV. MAN IN PARADISE', 'IN BRIEF',
              'I. WHERE SIN ABOUNDED, GRACE ABOUNDED ALL THE MORE', 'The reality of sin', 'Original sin - an essential truth of the faith',
              'How to read the account of the fall', 'II. THE FALL OF THE ANGELS', 'III. ORIGINAL SIN', 'Freedom put to the test', "Man's first sin",
              "The consequences of Adam's sin for humanity", 'A hard battle. . .', 'IV. "YOU DID NOT ABANDON HIM TO THE POWER OF DEATH"', 'IN BRIEF',
              'The Good News: God has sent his Son', 'At the heart of catechesis: Christ', 'I. WHY DID THE WORD BECOME FLESH?', 'II. THE INCARNATION',
              'III. TRUE GOD AND TRUE MAN', 'IV. HOW IS THE SON OF GOD MAN?', "Christ's soul and his human knowledge", "Christ's human will",
              "Christ's true body", 'The heart of the Incarnate Word', 'IN BRIEF', 'I. CONCEIVED BY THE POWER OF THE HOLY SPIRIT. . .',
              'II.... BORN OF THE VIRGIN MARY', "Mary's predestination", 'The Immaculate Conception', "Mary's divine motherhood", 
              "Mary's virginity", 'Mary - "ever-virgin"', "Mary's virginal motherhood in God's plan", 'IN BRIEF', "I. CHRIST'S WHOLE LIFE IS MYSTERY",
              "Characteristics common to Jesus' mysteries", 'Our communion in the mysteries of Jesus', "II. THE MYSTERIES OF JESUS' INFANCY AND HIDDEN LIFE",
              'The preparations', 'The Christmas mystery', "The mysteries of Jesus' infancy", "The mysteries of Jesus' hidden life",
              "III. THE MYSTERIES OF JESUS' PUBLIC LIFE", 'The baptism of Jesus', "Jesus' temptations", '"The kingdom of God is at hand"',
              'The proclamation of the kingdom of God', 'The signs of the kingdom of God', '"The keys of the kingdom"', 'A foretaste of the kingdom: the Transfiguration',
              "Jesus' ascent to Jerusalem", "Jesus' messianic entrance into Jerusalem", 'IN BRIEF', 'I. JESUS AND THE LAW', 'II. JESUS AND THE TEMPLE',
              "III. JESUS AND ISRAEL'S FAITH IN THE ONE GOD AND SAVIOUR", 'IN BRIEF', 'I. THE TRIAL OF JESUS', 'Divisions among the Jewish authorities concerning Jesus',
              "Jews are not collectively responsible for Jesus' death", "All sinners were the authors of Christ's Passion", "II. CHRIST'S REDEMPTIVE DEATH IN GOD'S PLAN OF SALVATION",
              '"Jesus handed over according to the definite plan of God"', '"For our sake God made him to be sin"', 'God takes the initiative of universal redeeming love',
              'III. CHRIST OFFERED HIMSELF TO HIS FATHER FOR OUR SINS', "Christ's whole life is an offering to the Father", '"The Lamb who takes away the sin of the world"',
              "Jesus freely embraced the Father's redeeming love", 'At the Last Supper Jesus anticipated the free offering of his life', 'The agony at Gethsemani',
              "Christ's death is the unique and definitive sacrifice", 'Jesus substitutes his obedience for our disobedience', 'Jesus consummates his sacrifice on the cross',
              "Our participation in Christ's sacrifice", 'IN BRIEF', 'Christ in the tomb in his body', '"You will not let your Holy One see corruption"',
              '"Buried with Christ. . ."', 'IN BRIEF', 'IN BRIEF', 'I. THE HISTORICAL AND TRANSCENDENT EVENT', 'The empty tomb', 'The appearances of the Risen One',
              "The condition of Christ's risen humanity", 'The Resurrection as transcendent event', 'II. THE RESURRECTION - A WORK OF THE HOLY TRINITY',
              'III. THE MEANING AND SAVING SIGNIFICANCE OF THE RESURRECTION', 'IN BRIEF', 'Christ already reigns through the Church. . .'
              '. . . until all things are subjected to him', 'The glorious advent of Christ, the hope of Israel', "The Church's ultimate trial",
              "The proper name of the Holy Spirit", "Titles of the Holy Spirit", "Symbols of the Holy Spirit", "In creation", "The Spirit of the promise",
              "In Theophanies and the Law", "In the Kingdom and the Exile", "Expectation of the Messiah and his Spirit", "John, precursor, prophet, and baptist",
              '"Rejoice, you who are full of grace"', 'In her, the "wonders of God" that the Spirit was to fulfill in Christ and the Church began to be manifested:',
              "Christ Jesus", "Pentecost", "The Holy Spirit - God's gift", "The Holy Spirit and the Church", "I. NAMES AND IMAGES OF THE CHURCH",
              "Symbols of the Church", "II. THE CHURCH'S ORIGIN, FOUNDATION AND MISSION", "A plan born in the Father's heart", "The Church - foreshadowed from the world's beginning",
              "The Church - prepared for in the Old Covenant", "The Church - instituted by Christ Jesus", "The Church - revealed by the Holy Spirit",
              "The Church - perfected in glory", "III. THE MYSTERY OF THE CHURCH", "The Church - both visible and spiritual", "The Church - mystery of men's union with God",
              "The universal Sacrament of Salvation", "IN BRIEF", "I. THE CHURCH - PEOPLE OF GOD", "Characteristics of the People of God", "A priestly, prophetic, and royal people",
              "II. THE CHURCH - BODY OF CHRIST", "The Church is communion with Jesus", '"One Body"', '"Christ is the Head of this Body"',
              "The Church is the Bride of Christ", "III. THE CHURCH IS THE TEMPLE OF THE HOLY SPIRIT", "Charisms", "IN BRIEF", "I. THE CHURCH IS ONE",
              '"The sacred mystery of the Church\'s unity" (UR 2)', "Wounds to unity", "Toward unity", "II THE CHURCH IS HOLY",
              "III. THE CHURCH IS CATHOLIC", 'What does "catholic" mean?', 'Each particular Church is "catholic"', "Who belongs to the Catholic Church?",
              "The Church and non-Christians", '"Outside the Church there is no salvation"', "Mission - a requirement of the Church's catholicity",
              "IV. THE CHURCH IS APOSTOLIC", "The Apostles' mission", "The bishops - successors of the apostles", "The apostolate", "IN BRIEF",
              "I. THE HIERARCHICAL CONSTITUTION OF THE CHURCH", "Why the ecclesial ministry?", "The episcopal college and its head, the Pope", "The teaching office",
              "The sanctifying office", "The governing office", "II. THE LAY FAITHFUL", "The vocation of lay people", "Participation in Christ's prophetic office",
              "Participation in Christ's kingly office", "III. THE CONSECRATED LIFE", "Evangelical counsels, consecrated life", "One great tree, with many branches",
              "The eremitic life", "Consecrated virgins", "Religious life", "Secular institutes", "Societies of apostolic life", "Consecration and mission: proclaiming the King who is corning",
              "IN BRIEF", "I. COMMUNION IN SPIRITUAL GOODS", "II. THE COMMUNION OF THE CHURCH OF HEAVEN AND EARTH", "IN BRIEF"]
    
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
    if paragraph and not paragraph[-1][0].isdigit():
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
    
    '''parses with '''
    paragraph = parsingI("https://www.vatican.va/archive/ENG0015/__" + page + ".HTM")
    if paragraph:
        paragraph = stitching(paragraph)
        appending(paragraph, file_path)
    
    page = page_next(page)