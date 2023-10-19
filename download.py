import os
import subprocess
import re

max_idle_time = 60 # In seconds
idling = False
percentage = 0


if not os.path.exists('Downloads'):
    os.mkdir('Downloads')

magnet = r"magnet:?xt=urn:btih:a32e902c94764558ccaf8e92f3820f6daed1303b&dn=%5BTSDM%E8%87%AA%E8%B3%BC%5D%5B231005%5DTV%E3%82%A2%E3%83%8B%E3%83%A1%E3%80%8ESPY%C3%97FAMILY%20Season2%E3%80%8FOP%E4%B8%BB%E9%A1%8C%E6%AD%8C%E3%80%8C%E3%82%AF%E3%83%A9%E3%82%AF%E3%80%8D%EF%BC%8FAdo%5BFLAC%5D&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"

executable_path = 'aria\\aria2c.exe'
download_location = 'C:\\Users\\sean\\Documents\\Projs\\Pynyaasi\\Downloads'

# Create a subprocess and capture the output in real-time
process = subprocess.Popen([executable_path, f'--dir={download_location}', f'--seed-time=0', f'--file-allocation=none', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

# Read the output line by line and print it in real-time
for line in process.stdout:
    if len(re.sub(r'\s', '', line)) > 0:            # Only print lines that have any content, rather than empty ones
        if '%)' in line:
            parts = line.split('(')
            second_part = parts[1]
            third_part = second_part.split('%')
            percentage = third_part[0]
            print(f"Python: {percentage}")
        print(f"Standard Output: {line}", end='')

for line in process.stderr:
    if line:
        print(f"Error Output: {line}", end='')

# Wait for the process to finish
process.wait()

# Optionally, get the return code
return_code = process.returncode
print(f"Return Code: {return_code}")
