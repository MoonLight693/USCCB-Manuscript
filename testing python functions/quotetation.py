'''
Author: Evan Whitmer
Last Date Modified: January 23, 2025
Description: replace "" with " as error fixing in grep ing paragraphs.
Links to additional resources:
- https://stackoverflow.com/questions/70463905/replace-method-not-working-over-single-quote
- https://www.geeksforgeeks.org/python-remove-substring-list-from-string/
'''
my_list = ["a\"\"ppl\"\"e", "banana", "cherry", '"We begin our profession of faith by saying: ""I believe"" or ""We believe""']

# Replace "a" with "o" in each string
new_list = [item.replace("\"\"", "o") for item in my_list]

print(new_list)
