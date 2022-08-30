import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import time
import os
import soupsieve
import re


# python spider.py www.rit.edu https://www.rit.edu/ 1
# python spider.py www.w3schools.com/ https://www.w3schools.com/ 1
# python spider.py github.com https://github.com/ 1
# python spider.py www.pythontutorial.net https://www.pythontutorial.net 1
# -------------------------------------------------------------------------------------------
urls = []

# Getting the arguments from the command line
def get_command_args() -> list[str]:
    # Stopping the script before breaking something
    if (len(sys.argv)-1) < 3:
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]

def full_url(scheme, domain, current_path, url):
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

# OLD function
# def parse_css_js_urls(domain, depth, content):
#     # js_urls = re.findall(f'{domain}[^\"]*', content)  # Greedy Version
#     js_urls = re.findall(f'{domain}.*?["`\']', content)  # non Greedy Version
#     for js_url in js_urls:
#         get_resource(domain, f"https//{js_url}", depth - 1)

def get_resource(domain, url, depth=0) -> set[str]:
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
                selectors = ['a[href]', 'link[href]', 'img[src]', 'script[src]', 'iframe[src]', 'object[data]']
                soup = bs(resp.text, 'html.parser')
                matches = soupsieve.select(','.join(selectors), soup)
                for match in matches:
                    match_url = match.get('href', match.get('src', match.get('data')))
                    url = full_url(urldata.scheme, domain, urldata.path, match_url)
                    if url.startswith('http'):
                        get_resource(domain, url, depth - 1)
            elif extension == '.css':
                print('Parse CSS')
                css_urls = re.findall(f'url\((.*?)\)', resp.text)
                for css_url in css_urls:
                    get_resource(domain, full_url(urldata.scheme, domain, urldata.path, css_url), depth - 1)
            elif extension == '.js':
                print('Parse Javascript')
                js_urls = re.findall(f'[\'"]((https?://{domain})?/.*?)[\'"]', resp.text)
                for js_url in js_urls:
                    get_resource(domain, f"{js_url}", depth - 1)
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
    get_resource(domain, url, int(depth)+1)
    write_resources('urls-gathered')
    

if __name__ == "__main__":
    start = time.time()
    main()
    lapsed = time.time() - start
    print(lapsed)