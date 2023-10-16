import fetch

#lest = fetch.scrap('https://nyaa.si/?f=0&c=2_0&q=')
# Base URL: https://nyaa.si/?f=0&c=2_0&q=

def query():
    pages = 2
    sort= 'Completed'   # Completed/Seeds/Default(Date)
    category = 'Any'    # Any/Lossless/Lossy
    whitelist= ['fate']
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
        #print(numered_page)
        query_page_lst.append(numered_page)

    full_fetch(query_page_lst)

def full_fetch(query_page_lst):

    whole_query_songs_lst = []

    for element in query_page_lst:
        single_page_songs_lst = fetch.scrap(element)
        if single_page_songs_lst:
            whole_query_songs_lst.extend(single_page_songs_lst)

    for i in whole_query_songs_lst:
        print()
        print(i)
        print()



query()