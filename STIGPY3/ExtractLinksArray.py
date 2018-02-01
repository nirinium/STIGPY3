#Link Extraction Function to be implemented into STIGs

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import lxml
import re

URL1 = 'https://iase.disa.mil/stigs/Pages/a-z.aspx'
URL2 = 'https://iase.disa.mil/stigs/Pages/a-z.aspx?Paged=TRUE&p_Title=Microsoft%20Windows%202012%20Server%20DNS%20STIG%20-%20Ver%201%2c%20Rel%207%20&p_ID=813&PageFirstRow=301&&View={25A09AF8-178B-447B-B42B-8839EBD71CAD}'

html_page = urlopen(URL1)
soup = BeautifulSoup(html_page, 'lxml')
links = []
 
for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
     links.append(link.get('href'))
     

print(links, 'Total:', len(links) )