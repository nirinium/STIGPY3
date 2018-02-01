# PYTHON 3.6 | STIGPY3 | 2018
# For Support >>> email: wills.colton@gmail.com
# Version 0.0.4[dev]
# NOT FOR USE IN PRODUCTION ENVIRONMENT YET

import os, sys, lxml, re, ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve

#HANDLES SSL REQUESTS
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
#END SSL REQUEST HANDLING

URL = 'https://iase.disa.mil/stigs/Pages/a-z.aspx'
URL2 = 'https://iase.disa.mil/stigs/Pages/a-z.aspx?Paged=TRUE&p_Title=Microsoft%20Windows%202012%20Server%20DNS%20STIG%20-%20Ver%201%2c%20Rel%207%20&p_ID=813&PageFirstRow=301&&View={25A09AF8-178B-447B-B42B-8839EBD71CAD}'
OUTPUT_DIR = 'stigs'

#START
print("Grabbing STIGs...")

#PROGRESS PERCENTAGE
def progressDL(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize) #FORMULA TO CALCULATE DOWNLOAD PROGRESS
      sys.stdout.write("\r" + "...%d%% " % percent) #PRINTS PROGRESS TO CONSOLE
      sys.stdout.flush() #WRITES EVERYTHING TO TERMINAL

#PARSE LINKS -- EXPORT FUNCTION COMING SOON 
html_page = urlopen(URL)
soup = BeautifulSoup(html_page, 'lxml')
linksList = []
log = 'logfile.txt'
 
for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
     linksList.append(link.get('href'))    

if not os.path.exists('logs'):
  outfile = open(log, "w")
  outfile.write(linksList)
  outfile.close()

print(linksList, 'Total:', len(linksList) )
#END PARSE FUNCTION

u = urlopen(URL)
u2 = urlopen(URL2)

try: #PAGE 1 of STIG site
    html = u.read().decode('utf-8')
finally:
    u.close()
try: #PAGE 2 of STIG site
    html = u2.read().decode('utf-8')
finally:
    u2.close()
#BEGIN FILTERING

soup = BeautifulSoup(html, 'lxml')
for link in soup.select('a[href^="http://"]'):
    href = link.get('href')
    if not any(href.endswith(x) for x in linksList): #pulls links from [LIST] linksList
        continue

    filename = os.path.join(OUTPUT_DIR, href.rsplit('/', 1)[-1])

    href = href.replace('http://','https://') #forces HTTPS 

    print("> %s to \%s..." % (href, OUTPUT_DIR) ) #handles only printing of URL and Local URL Destination | minus 1st 48 char of str
    urlretrieve(href, filename, reporthook = progressDL)
    #urlretrieve(href, filename, reporthook = progressDL) # href | pulls 'href' out of actual html | that is what beautifulsoup is scraping
    print("DONE!") 

