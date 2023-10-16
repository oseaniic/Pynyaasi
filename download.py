import os
import subprocess

if not os.path.exists('Downloads'):
    os.mkdir('Downloads')

magnet = r'magnet:?xt=urn:btih:41d4a9b38e8336ce5f857b3effb948660bdc78b3&dn=%5BTSDM%E8%87%AA%E8%B3%BC%5D%5B231013%5DTV%E3%82%A2%E3%83%8B%E3%83%A1%E3%80%8E%E3%82%A6%E3%83%9E%E5%A8%98%20%E3%83%97%E3%83%AA%E3%83%86%E3%82%A3%E3%83%BC%E3%83%80%E3%83%BC%E3%83%93%E3%83%BC%20Season%203%E3%80%8FOP%20%26%20ED%E3%80%8C%E3%82%BD%E3%82%B7%E3%83%86%E3%83%9F%E3%83%B3%E3%83%8A%E3%83%8E%E3%80%8D%E3%80%8C%E3%82%A2%E3%82%B3%E3%82%AC%E3%83%ACChallenge%20Dash%21%21%E3%80%8D%5B320K%5D&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce'

executable_path = 'aria\\aria2c.exe'
download_location = 'C:\\Users\\sean\\Documents\\Projs\\Pynyaasi\\Downloads'

completed_process = subprocess.run([executable_path, f'--dir={download_location}', magnet], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Access the standard output and error output
stdout_output = completed_process.stdout
stderr_output = completed_process.stderr

# Print the output
print("Standard Output:")
print(stdout_output)

print("Error Output:")
print(stderr_output)