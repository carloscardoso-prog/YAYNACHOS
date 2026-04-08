import os
import sys
import re
import subprocess
import pyperclip

url = sys.argv[1]

MAX_BYTES = 100 * 1024 * 1024
OUT = 'video.mp4'
url = sys.argv[1]

for height in (1080, 720, 480, 360, 240, 144):
    if os.path.isfile(OUT):
        os.remove(OUT)
    subprocess.run(
        [
            'yt-dlp',
            '-f',
            f'bv*[height<={height}]+ba/b[height<={height}]',
            '--merge-output-format',
            'mp4',
            '-o',
            OUT,
            url,
        ],
        check=False,
    )
    if os.path.isfile(OUT) and os.path.getsize(OUT) <= MAX_BYTES:
        break
        
subprocess.run(f'yt-dlp -t mp4 -o "{OUT}" {url}', shell=True)
result = subprocess.run(
    f'pyupload "{OUT}" --host=catbox',
    shell=True,
    stdout=subprocess.PIPE,
    text=True,
)
subprocess.run(f'rm "{OUT}"', shell=True)
m = re.search(r'Your link\s*:\s*(\S+)', result.stdout)
pyperclip.copy(m.group(1))
print(m.group(1))