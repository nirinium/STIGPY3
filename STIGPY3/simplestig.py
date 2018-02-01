import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start_url = 'https://iase.disa.mil/stigs/Pages/a-z.aspx'
r = requests.get(start_url)
soup = BeautifulSoup(r.text, 'lxml')

# get full url of file
pre = soup.find('pre')
file_urls = pre.select('a[href*="."]')
full_urls = [urljoin(start_url, url['href'])for url in file_urls]
# download file
for full_url in full_urls:
    file_name = full_url.split('/')[-1]
    print("Downloading {} to {}...".format(full_url, file_name))
    with open(file_name, 'wb') as f:
        fr = requests.get(full_url, stream=True)
        for chunk in fr.iter_content(chunk_size=1024):
            f.write(chunk)
    print('Done')