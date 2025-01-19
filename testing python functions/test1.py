# problem: need strings in a list to combine with the previous element if
# the current element doesn't start with an integer
# sources for thinking: https://www.geeksforgeeks.org/python-merge-list-elements/#,
# https://stackoverflow.com/questions/5577501/how-to-tell-if-string-starts-with-a-number-with-python

a = ['1a','b',"2c","d","3e","f"]
print(a)

x = len(a)
i=0
while i < x:
    if not a[i][0].isdigit() and i != 0:
        b = [''.join(a[i-1:i+1])]  # store 'for' in a variable 
        print(b)
        a = a[:i-1] + b + a[i+1:]
        x = x-1
        i += 1
    else: i += 1
print(a)