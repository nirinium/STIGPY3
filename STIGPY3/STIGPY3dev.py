import os
import sys
import time
import logging
from bs4 import BeautifulSoup
# PYTHON 3.X
from urllib.request import urlopen, urlretrieve

URL = 'https://iase.disa.mil/stigs/Pages/a-z.aspx?Paged=TRUE&p_Title=Microsoft%20Windows%202012%20Server%20DNS%20STIG%20-%20Ver%201%2c%20Rel%207%20&p_ID=813&PageFirstRow=301&&View={25A09AF8-178B-447B-B42B-8839EBD71CAD}'
OUTPUT_DIR = 'stigs'

#START
print("Grabbing STIGs...")

#PROGRESS PERCENTAGE
def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("\r" + "...%d%% " % percent)
      sys.stdout.flush()

u = urlopen(URL)
f = open('logging.txt', 'w')
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
    
    print("> %s to %s..." % (href, filename) )
    urlretrieve(href, filename, reporthook = dlProgress)
    print("Done")
