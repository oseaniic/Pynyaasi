import requests
from bs4 import BeautifulSoup

import os
import subprocess
import re
import time

import patoolib
import ctypes

# A page in this website normally has 75 torrents listed per page

def query_setup():      # Get the page list to scrap based on the criteria and begin the query_start function
    pages = 15
    sort= 'Completed'   # Completed/Seeds/Default(Date)
    category = 'Any'    # Any/Lossless/Lossy
    whitelist= []
    blacklist= ['k-pop','english','vtuber','hololive','gawr','fate','IDOLM@STER','bgm', 'dream!', 'nier']

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
    
    print('Page list:')
    for i in range(pages):
        numered_page = base_url + '&p=' + str(i+1)
        print(numered_page)
        query_page_lst.append(numered_page)
    query_run(query_page_lst)

def fetch (link):                   # Fetch all torrents from the URL given

    discard_abandoned = True        # Wether to include or not torrents with no seeds
    
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    tr_elements = soup.find_all('tr')   # Find all <tr> elements with any class

    elemet_block_lst = []   # all tr elements
    page_dic_lst = []   #each tr element broken down into the following categories:
    page_dic_lst_full = []

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
        page_dic_lst_full.append([elem_link])
        

    return page_dic_lst,page_dic_lst_full

def query_run(query_page_lst):      # Run the fetch function for each link

    whole_query_songs_lst = []

    for element in query_page_lst:
        single_page_songs_lst , page_dic_lst_full = fetch(element)
        if single_page_songs_lst:
            whole_query_songs_lst.extend(single_page_songs_lst)

    print(f'Found {len(whole_query_songs_lst)} healthy torrents out of {len(page_dic_lst_full)} torrents.')
    print('Bulk Downloading..')

    success_count = 0
    failed_count = 0

    for i, song in enumerate(whole_query_songs_lst):
        print()
        print(f"Working on object {i + 1} out of {len(whole_query_songs_lst)}")
        print(f"Magnet link: {song[1]}, Size: {song[4]}")
        status = download(song[2])
        if status:
            if status == 'success':
                success_count = success_count + 1
            elif status == 'failed':
                failed_count = failed_count +1
        print(f'Stats so far: succesful: {success_count} failed: {failed_count}')
        #print()
        #pass


def download(magnet):
    max_idle_time = 120 # In seconds
    idle_time_left = 0
    idling = False
    percentage = 0
    percentage_old = -1
    auto_uncompress = True

    download_started = False
    download_failed = False

    #magnet = "magnet:?xt=urn:btih:fd0a65b73d1725a95a385e160f34a6a7ab0198db&dn=%5BTSDM%E8%87%AA%E8%B3%BC%5D%5BHi-Res%5D%5B230412%5DTV%E3%82%A2%E3%83%8B%E3%83%A1%E3%80%8E%E6%8E%A8%E3%81%97%E3%81%AE%E5%AD%90%E3%80%8FOP%E4%B8%BB%E9%A2%98%E6%AD%8C%E3%80%8C%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%80%8D%EF%BC%8FYOASOBI%5B96kHz%2F24bit%5D%5BFLAC%5D&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"

    executable_path = 'aria\\aria2c.exe'
    download_loc = "E:\\Moosic"

    print('DL: Attempting to download')

    # Create a subprocess and capture the output in real-time
    process = subprocess.Popen([executable_path, f'--dir={download_loc}', f'--seed-time=0', f'--file-allocation=none', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

    def extract_archive(archive_path):
        folder = os.path.dirname(archive_path)

        try:
            patoolib.extract_archive(archive_path, outdir=folder, overwrite=True)
            print(f"Extraction successful for {archive_path}")
            os.remove(archive_path)  # Remove the archive file if extraction was successful
        except patoolib.util.PatoolError as e:
            print(f"Error extracting {archive_path}: {str(e)}")
            pass  # Do not delete the archive file if there was an error during extraction
    
    def set_window_title(title):
        ctypes.windll.kernel32.SetConsoleTitleW(title)

    # Read the output line by line and print it in real-time
    for line in process.stdout:
        if len(re.sub(r'\s', '', line)) > 0:            # Only print lines that have any content, rather than empty ones
            #print(f"Standard Output: {line}", end='')

            if '%)' in line:
                if download_started == False:
                    print('DL: Download has started..')
                    download_started = True

                parts = line.split('(')
                second_part = parts[1]
                third_part = second_part.split('%')
                percentage = int(third_part[0])
                #print(f'DL: Progress: {percentage}%')
                
                if percentage == percentage_old:                
                    time_idle_start = time.time()
                    time_idle_total = abs(time_idle_start - time_last_active)
                    time_idle_left = int(max_idle_time - time_idle_total)  

                    set_window_title(f'Download Progress: {percentage}% Idle time remaining: {time_idle_left}')

                    if time_idle_left < 1:
                        print(f"DL: Idlied for too long, exiting process...")
                        download_failed = True
                        process.terminate()
                        break
                    else:
                        #print(f"Idling, time left: {time_idle_left}")
                        pass
                else:
                    time_last_active = time.time()
                percentage_old = percentage 
                #print(f"Python: {percentage}")
            elif ':/' in line and '|' in line and '.rar' in line or '.zip' in line or '.7z' in line:         # TODO we need to build a wall
                #print('a')
                #line = line.replace('.rar','.compp').replace('.zip','.compp').replace('.7z','.compp')
                if '.rar' in line:
                    line = line.replace('.rar','.rarKJLL')
                if '.zip' in line:
                    line = line.replace('.zip','.zipKJLL')
                if '.7z' in line:
                    line = line.replace('.7z','.7zKJLL')
                line_parts = line.split('|')
                lenk_crumbs = line_parts[3]
                other_crumbs = lenk_crumbs.split('KJLL')
                compressed_file = other_crumbs[0]
                print(f"DL: Compressed file: {compressed_file}")

                if auto_uncompress == True:
                    extract_archive(compressed_file)

            else:
                if download_started == False:
                    if idling == False:
                        idling = True
                        timer_idle_start = time.time()
                    timer_current_time = time.time()
                    timer_remaining = int(max_idle_time - abs(timer_idle_start - timer_current_time))

                    set_window_title(f'Download Progress: {percentage}% Idle time remaining: {timer_remaining}')

                    if timer_remaining < 1:
                        print(f"DL: Idlied for too long, exiting process...")
                        download_failed = True
                        process.terminate()
                        break
                    #print(f"Time: {timer_remaining}")

            

    for line in process.stderr:
        if line:
            #print(f"Error Output: {line}", end='')
            download_failed = True

    process.wait()

    return_code = process.returncode

    
    if not download_failed:
        print(f"DL: Download successful, return code: {return_code}, at {percentage}% done")
        return 'success'
    else:
        if download_started:
            print(f"DL: DOWNLOAD FAILED, return code: {return_code}, at {percentage}% done")
        else:
            print(f"DL: Download FAILED, return code: {return_code}")
        return 'failed'

query_setup()