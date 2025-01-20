'''
Sources:
https://www.youtube.com/watch?v=q5uM4VKywbA - Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files
https://www.google.com/search?q=csv+2+lists+pytohn&sca_esv=a4c5c968ead58a07&rlz=1CAMFAZ_enUS978US978&sxsrf=ADLYWIKKymC_-lRxg1wgXkz5A9kkhFp2HQ%3A1737311380519&ei=lESNZ6W5H5-x0PEP_Z7dkQE&ved=0ahUKEwil08ydtYKLAxWfGDQIHX1PNxIQ4dUDCBA&uact=5&oq=csv+2+lists+pytohn&gs_lp=Egxnd3Mtd2l6LXNlcnAiEmNzdiAyIGxpc3RzIHB5dG9objIHECEYoAEYCjIHECEYoAEYCjIHECEYoAEYCjIHECEYoAEYCjIHECEYoAEYCjIFECEYqwIyBRAhGJ8FMgUQIRifBTIFECEYnwUyBRAhGJ8FSJM5UIoGWPQ2cAN4AZABAZgBgQGgAfodqgEFMTMuMjO4AQPIAQD4AQGYAhegAv8RqAIUwgIKEAAYsAMY1gQYR8ICBRAAGIAEwgIGEAAYFhgewgILEAAYgAQYhgMYigXCAggQABiABBiiBMICBxAjGCcY6gLCAhQQABiABBiRAhi0AhiKBRjqAtgBAcICFBAAGOMEGLQCGIkFGOkEGOoC2AEBwgIUEAAYgAQY4wQYtAIY6QQY6gLYAQHCAgQQIxgnwgIKECMYgAQYJxiKBcICCxAAGIAEGJECGIoFwgINEAAYgAQYsQMYQxiKBcICDhAuGIAEGLEDGNEDGMcBwgIOEAAYgAQYsQMYgwEYigXCAg4QLhiABBjHARiOBRivAcICCxAuGIAEGLEDGIMBwgIKEAAYgAQYQxiKBcICChAuGIAEGEMYigXCAgcQABiABBgKwgIQEC4YgAQYFBiHAhjHARivAcICChAAGIAEGBQYhwLCAgUQABjvBcICCBAAGKIEGIkFwgIFECEYoAGYAxTxBdy8GMG7XU9EiAYBkAYIugYGCAEQARgBkgcENy4xNqAH0oQC&sclient=gws-wiz-serp
https://www.google.com/search?q=if+file+exists+python+delete&rlz=1CAMFAZ_enUS978US978&oq=if+file+exists+python&gs_lcrp=EgZjaHJvbWUqBwgBEAAYgAQyDwgAEEUYORiRAhiABBiKBTIHCAEQABiABDIHCAIQABiABDIICAMQABgWGB4yCAgEEAAYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yDQgHEAAYhgMYgAQYigUyBwgIEAAY7wUyBwgJEAAY7wXSAQg1MjU0ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
'''

import csv

import os

file_path = "testing python functions/new_table.csv"
if os.path.exists(file_path):
    os.remove(file_path)

a = [1,2,3,4,5,6]
b = ["a","b","c","d","e","f",]

with open(file_path, "w", newline='') as new_file:
    cvs_writer = csv.writer(new_file, delimiter=":")
    cvs_writer.writerows(zip(a,b))