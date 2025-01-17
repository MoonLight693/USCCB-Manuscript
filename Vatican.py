'''
Author: Evan Whitmer
Last Date Modified: January 17, 2025
Description: This script uses wget command to bulk download the 
Vatican Catechism at https://www.vatican.va/archive/ENG0015/_INDEX.HTM. 
Then, parses the Paragraph and its number into a usable table.
Links to additional resources:
'''

from lxml import etree
import requests
from io import StringIO