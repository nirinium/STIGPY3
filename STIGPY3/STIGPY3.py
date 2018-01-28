import os
import sys
from bs4 import BeautifulSoup
# PYTHON 3.X
from urllib.request import urlopen, urlretrieve

URL = 'https://iase.disa.mil/stigs/Pages/a-z.aspx'
OUTPUT_DIR = 'stigs'

#PROGRESS BAR
def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("\r" + "...%d%% " % percent)
      sys.stdout.flush()

u = urlopen(URL)
try:
    html = u.read().decode('utf-8')
finally:
    u.close()

soup = BeautifulSoup(html, "html.parser")
for link in soup.select('a[href^="http://"]'):
    href = link.get('href')
    if not any(href.endswith(x) for x in ['.zip', '.xls', '.xlsx', '.csv', '.ppt', '.pptx', '.pdf', '.docx', '.doc', '.txt']):
        continue

    filename = os.path.join(OUTPUT_DIR, href.rsplit('/', 1)[-1])

    # We need a https:// URL for this site
    href = href.replace('http://','https://')

    print("Downloading %s to %s..." % (href, filename) )
    urlretrieve(href, filename, reporthook = dlProgress)
    print("Done.")