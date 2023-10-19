import requests
from bs4 import BeautifulSoup

# A page in this website normally has 75 torrents listed per page

def fetch (link):

    discard_abandoned = True        # Wether to include or not torrents with no seeds
    
    response = requests.get(link)
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
        #print()
        #print(block)
        elem_name = ''  # Reseting the values for each element
        elem_link = ''
        elem_magn = ''
        elem_cate = ''
        
        elem_size = ''
        elem_date = ''
        elem_seeds = ''
        elem_leech = ''
        elem_completions = ''

        number_element = 0

        has_seeders = True

        for line in block_lines:
            line = line.replace("amp;", "") # Remove the amp; thing
            if 'title="Audio - Lossless"' in line or 'title="Audio - Lossy"' in line:   # Category
                parts = line.split('title="Audio - ')
                second_part = parts[1]
                final_parts = second_part.split('">')
                result = final_parts[0]
                elem_cate = result
                continue

            if '<a href="/view/' in line:   # Link
                parts = line.split('<a href="')
                second_part = parts[1]
                final_parts = second_part.split('" title="')
                result = final_parts[0]
                result = 'https://nyaa.si' + result
                
                elem_link = result
                #continue   # Since the link and tittle are in the same line

            if 'title="' in line and not 'comments' in line:   # Title
                
                parts = line.split('title="')
                second_part = parts[1]
                final_parts = second_part.split('"')
                result = final_parts[0]
                
                elem_name = result
                continue

            if 'magnet' in line:   # Magnet
                parts = line.split('<a href="')
                second_part = parts[1]
                final_parts = second_part.split('">')
                result = final_parts[0]
                
                elem_magn = result
                continue
            
            if '<td class="text-center"' in line and '</td>' in line:       # Size,date,seeds,Leeches,Completions
                parts = line.split('<td class="text-center')
                second_part = parts[1]
                third_parts = second_part.split('">')
                fourt_parts = third_parts[1]
                final_parts = fourt_parts.split('<')
                result = str(final_parts[0])
                
                #print('xddd:')
                #print(result)

                if number_element == 0:
                    elem_size = result

                elif number_element == 1:
                    elem_date = result

                elif number_element == 2:
                    elem_seeds = result
                    if discard_abandoned == True and int(result) == 0:
                        has_seeders = False

                elif number_element == 3:
                    elem_leech = result

                elif number_element == 4:
                    elem_completions = result

                #print(num,result)
                number_element = number_element + 1
        
        if has_seeders:     # Only append the torrent if it has any seeders
            page_dic_lst.append([elem_name, elem_link, elem_magn, elem_cate, elem_size, elem_date, elem_seeds, elem_leech, elem_completions])

    return page_dic_lst

def query_setup():
    pages = 1
    sort= 'Seeds'   # Completed/Seeds/Default(Date)
    category = 'Any'    # Any/Lossless/Lossy
    whitelist= []
    blacklist= ['k-pop','halo']

    base_url = 'https://nyaa.si/?f=0&c=2_0&q='  # Category + base + whitelist + blacklist + sort + pagenum

    query_page_lst = []

    if not category == 'Any':
        if category == 'Lossless':
            cat_term = '&c=2_1'
        else:
            cat_term = '&c=2_2'
        base_url = base_url.replace('&c=2_0', cat_term)
    if whitelist:
        for element in whitelist:
            base_url = base_url + '+' + element
    if blacklist:
        for element in blacklist:
            base_url = base_url + '+' + '-' + element
    if sort == 'Completed':
        base_url = base_url + '&s=downloads&o=desc'
    elif sort == 'Seeds':
        base_url = base_url + '&s=seeders&o=desc'
    
    for i in range(pages):
        numered_page = base_url + '&p=' + str(i+1)
        print(numered_page)
        query_page_lst.append(numered_page)
    query_run(query_page_lst)

def query_run(query_page_lst):

    whole_query_songs_lst = []

    for element in query_page_lst:
        single_page_songs_lst = fetch(element)
        if single_page_songs_lst:
            whole_query_songs_lst.extend(single_page_songs_lst)

    for i, song in enumerate(whole_query_songs_lst):
        print()
        print(f"Working on object {i + 1} out of {len(whole_query_songs_lst)}")
        print(song)
        print()
        pass



query_setup()