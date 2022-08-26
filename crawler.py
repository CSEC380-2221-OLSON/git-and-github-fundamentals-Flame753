import sys
from lxml import html
import requests

#python crawler.py rit.edu https://www.rit.edu/ 1

def get_command_args() -> list:
    if (len(sys.argv)-1) < 3:
        # Stopping the script before breaking something
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]


def get_urls_a_tags(url:str) -> list:
    response = requests.get(url)
    tree = html.fromstring(html=response.text)
    return tree.xpath('//a/@href')


def main():
    domain, url, depth= get_command_args()
    urls = get_urls_a_tags(url)
    print(urls)


if __name__ == "__main__":
    main()