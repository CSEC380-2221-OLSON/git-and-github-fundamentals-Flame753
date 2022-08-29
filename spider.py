import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import time
import os
import re


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
    urldata = urlparse(url)

    if urldata.scheme not in ['', 'http', 'https']:
        return url

    if url.startswith('/'):
        url = f'{scheme}://{domain}{url}'
    elif not url.startswith('http'):
        if urldata.path == '' and urldata.fragment != '':
            url = f'{scheme}://{domain}{current_path}#{urldata.fragment}'
        else:
            url = f'{scheme}://{domain}{current_path}/{url}'
    return url

def get_resources(domain, url, depth=0) -> set[str]:
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


    # if we have a html, css, or js file, then down the rabbit hole we go
    extension = os.path.splitext(urldata.path)[1]
    if extension in ['', '.html', '.css', '.js']:
        resp = requests.get(url)
        if resp.status_code == 200:
            if extension in ['', '.html']:
                tags = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src', 'iframe': 'src', 'object': 'data' }
                tree = bs(resp.text, 'html.parser')
                for tag, value in tags.items():
                    for link in tree.find_all(tag):
                        url_path = link.get(value)
                        if url_path:  # Preventing None values to be added
                            url = create_url(urldata.scheme, domain, urldata.path, url_path)
                            if url.startswith('http'):
                                get_resources(domain, url, depth - 1)
            elif extension == '.css':
                print('Parse CSS')
                print(resp.text)
            elif extension == '.js':
                print('Parse Javascript')
                pass
            else:
                print('Something went wrong, we shouldnt be here')
        else:
            print(f'Something went wrong getting {url} ({resp.status_code})')
    else:
        print(f'Skipping {url}')
        return False


def write_resources(filepath):
    with open(filepath, 'w') as fh:
        for url in urls:
            fh.write(f'{url}\n')


def main():
    domain, url, depth= get_command_args()
    get_resources(domain, url, int(depth)+1)
    write_resources('urls-gathered')
    

if __name__ == "__main__":
    start = time.time()
    main()
    lapsed = time.time() - start
    print(lapsed)