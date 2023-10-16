import requests
from bs4 import BeautifulSoup

url = 'https://nyaa.si/?f=0&c=2_0&q='
response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')
tr_elements = soup.find_all('tr')   # Find all <tr> elements with any class

elemet_block_lst = []   # all tr elements
page_dic_lst = []   #each tr element broken down into the following categories:

for tr in tr_elements:
    tr = str(tr)            # Convert from HTMLy text to regular string
    if '<td>' in tr:        # Only include non empty ones
        elemet_block_lst.append(tr) # Add tr elements to page_dic_lst array

for block in elemet_block_lst:   # Process each elelement
    block_lines = block.splitlines()  
    print()
    print()
    #print(block)
    elem_name = ''  # Reseting the values for each element
    elem_link = ''
    elem_magn = ''
    elem_cate = ''
    elem_size = ''
    elem_date = ''
    elem_seeds = ''

    for line in block_lines:

        if 'title="Audio - Lossless"' in line or 'title="Audio - Lossy"' in line:   # Category
            parts = line.split('title="Audio - ')
            second_part = parts[1]
            final_parts = second_part.split('">')
            result = final_parts[0]
            
            print(result)
            elem_cate = result
            continue

        if '<a href="/view/' in line:   # Link
            parts = line.split('<a href="')
            second_part = parts[1]
            final_parts = second_part.split('" title="')
            result = final_parts[0]
            result = 'https://nyaa.si' + result
            
            print(result)
            elem_link = result
            #continue   # Since the link and tittle are in the same line

        if 'title="' in line and not 'comments' in line:   # Title
            line = line.replace("amp;", "") # Remove the amp; thing
            parts = line.split('title="')
            second_part = parts[1]
            final_parts = second_part.split('"')
            result = final_parts[0]
            
            print(result)
            elem_name = result
            continue

        if 'magnet' in line:   # Magnet
            parts = line.split('<a href="')
            second_part = parts[1]
            final_parts = second_part.split('&amp')
            result = final_parts[0]
            
            print(result)
            elem_magn = result
            continue
        
    page_dic_lst.append((elem_name, elem_link, elem_magn, elem_cate, elem_size, elem_date, elem_seeds))


print(f"Total elements found: {len(elemet_block_lst)}")


