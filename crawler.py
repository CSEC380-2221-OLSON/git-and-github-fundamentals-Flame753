import sys
from lxml import etree, html
import requests




def get_command_args():
    if (len(sys.argv)-1) < 3:
        # Stopping the script before breaking something
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]


def get_a_tags_urls(url) -> list:
    response = requests.get("https://www.rit.edu/")
    tree = html.fromstring(html=response.text)
    return tree.xpath('//a/@href')


class Scraper:
     pass


def main():
    domain, url, depth= get_command_args()
    print(domain, url, depth)

if __name__ == "__main__":
    main()