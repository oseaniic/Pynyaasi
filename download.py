import os
import subprocess
import re
import time

import patoolib


def download(magnet):
    max_idle_time = 120 # In seconds
    idle_time_left = 0
    idling = False
    percentage = 0
    percentage_old = -1
    auto_uncompress = True

    download_started = False
    download_failed = False

    magnet = "magnet:?xt=urn:btih:fd0a65b73d1725a95a385e160f34a6a7ab0198db&dn=%5BTSDM%E8%87%AA%E8%B3%BC%5D%5BHi-Res%5D%5B230412%5DTV%E3%82%A2%E3%83%8B%E3%83%A1%E3%80%8E%E6%8E%A8%E3%81%97%E3%81%AE%E5%AD%90%E3%80%8FOP%E4%B8%BB%E9%A2%98%E6%AD%8C%E3%80%8C%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%80%8D%EF%BC%8FYOASOBI%5B96kHz%2F24bit%5D%5BFLAC%5D&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"

    executable_path = 'aria\\aria2c.exe'
    download_loc = "C:\\Users\\sean\\Documents\\Projs\\Pynyaasi\\Downloads"

    print('DL: Attempting to download')

    # Create a subprocess and capture the output in real-time
    process = subprocess.Popen([executable_path, f'--dir={download_loc}', f'--seed-time=0', f'--file-allocation=none', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

    def extract_archive(archive_path):
        folder = os.path.dirname(archive_path)

        try:
            patoolib.extract_archive(archive_path, outdir=folder)
            print(f"Extraction successful for {archive_path}")
            os.remove(archive_path)  # Remove the archive file if extraction was successful
        except patoolib.util.PatoolError as e:
            print(f"Error extracting {archive_path}: {str(e)}")
            pass  # Do not delete the archive file if there was an error during extraction

    # Read the output line by line and print it in real-time
    for line in process.stdout:
        if len(re.sub(r'\s', '', line)) > 0:            # Only print lines that have any content, rather than empty ones
            print(f"Standard Output: {line}", end='')
            if '%)' in line:
                if download_started == False:
                    print('DL: Download has started..')
                    download_started = True

                parts = line.split('(')
                second_part = parts[1]
                third_part = second_part.split('%')
                percentage = int(third_part[0])
                print(f'DL: Progress: {percentage}%')
                if percentage == percentage_old:                
                    time_idle_start = time.time()
                    time_idle_total = abs(time_idle_start - time_last_active)
                    time_idle_left = int(max_idle_time - time_idle_total)  
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
                print('a')
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
        print(f"DL: Download successful, return code: {return_code}")
    else:
        print(f"DL: Download FAILED, return code: {return_code}")