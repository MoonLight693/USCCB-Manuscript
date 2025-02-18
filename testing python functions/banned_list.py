paragraph = ["13 The plan of this catechism is inspired by the great tradition of catechisms which build catechesis on four pillars: the baptismal profession of faith (the Creed), the sacraments of faith, the life of faith (the Commandments), and the prayer of the believer (the Lord's Prayer).", 'Part One: the Profession of Faith', '14 Those who belong to Christ through faith and Baptism must confess their baptismal faith before men.', ' First therefore the Catechism expounds revelation, by which God addresses and gives himself to man, and the faith by which man responds to God (Section One). the profession of faith summarizes the gifts that God gives man: as the Author of all that is good; as Redeemer; and as Sanctifier. It develops these in the three chapters on our baptismal faith in the one God: the almighty Father, the Creator; his Son Jesus Christ, our Lord and Saviour; and the Holy Spirit, the Sanctifier, in the Holy Church (Section Two).', 'Part Two: the Sacraments of Faith', "15 The second part of the Catechism explains how God's salvation, accomplished once for all through Christ Jesus and the Holy Spirit, is made present in the sacred actions of the Church's liturgy (Section One), especially in the seven sacraments (Section Two).", 'Part Three: the Life of Faith', "16 The third part of the Catechism deals with the final end of man created in the image of God: beatitude, and the ways of reaching it - through right conduct freely chosen, with the help of God's law and grace (Section One), and through conduct that fulfils the twofold commandment of charity, specified in God's Ten Commandments (Section Two).", 'Part Four: Prayer in the Life of Faith', "17 The last part of the Catechism deals with the meaning and importance of prayer in the life of believers (Section One). It concludes with a brief commentary on the seven petitions of the Lord's Prayer (Section Two), for indeed we find in these the sum of all the good things which we must hope for, and which our heavenly Father wants to grant us."]

banned = ["Part One: the Profession of Faith", "Part Two: the Sacraments of Faith", "Part Three: the Life of Faith", "Part Four: Prayer in the Life of Faith"]

for i in paragraph:
    if i in banned:
        paragraph.pop(paragraph.index(i))

print(paragraph)