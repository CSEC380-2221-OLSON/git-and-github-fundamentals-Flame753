import sys
from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import requests


# python spider.py www.rit.edu https://www.rit.edu/ 1
# python spider.py www.w3schools.com/ https://www.w3schools.com/ 1
# python spider.py github.com https://github.com/ 1
# -------------------------------------------------------------------------------------------
urls = []

# Getting the arguments from the command line
def get_command_args() -> list[str]:
    # Stopping the script before breaking something
    if (len(sys.argv)-1) < 3:
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]

def create_url(scheme, domain, current_path, url):
    # print(f"current_path: {current_path}", f"url: {url}", "Are both the same:",current_path == url)
    if url.startswith('/'):
        url = f'{scheme}://{domain}{url}'
    elif not url.startswith('http'):
        url = f'{scheme}://{domain}{current_path}/{url}'
    return url

def get_resources(content: str) -> set[str]:
    tags = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src', 'iframe': 'src', 'object': 'data' }
    links = []
    tree = bs(content, 'html.parser')
    for tag, value in tags.items():
        for link in tree.find_all(tag):
            url_path = link.get(value)
            if url_path:  # Preventing None values to be added 
                links.append(url_path)
    return set(links)

def spider(domain, url, depth=0):
    urldata = urlparse(url)

    # if domain doesnt match then skip
    if urldata.netloc and urldata.netloc != domain:
        return False

    # if path not already in our list, append it
    if url not in urls:
        urls.append(url)
    else:
        # if we got here then escape early, we've already hit this url
        return False

    # if depth has reached 0 then go no further
    if depth == 0:
        return False
    
    print(url)
    resp = requests.get(url)
    if resp.status_code == 200:
        print(resp)
        # if resp.status_code:

        links = get_resources(resp.text)
        for link in links:
            spider(domain, create_url(urldata.scheme, domain, urldata.path, link), depth - 1)


def main():
    domain, url, depth= get_command_args()
    spider(domain, url, int(depth))
    pprint(urls)
    

if __name__ == "__main__":
    main()