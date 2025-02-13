# source: https://www.geeksforgeeks.org/python-replace-to-k-at-ith-index-in-string/#
#z = "abcdefghijklmnopqrstuvwxyz".upper()
#z = "0123456789" + z
#iterate = [i for i in z]
#print(iterate)

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
    #print(f'length: {len(page_list)}')
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

#page = "P9Z"
#print(page)
#page = page_next(page)
#print(page)
page = "P2"
count = 0
while page != "PAE":
    count += 1
    page = page_next(page)
print(f'count: {count}')