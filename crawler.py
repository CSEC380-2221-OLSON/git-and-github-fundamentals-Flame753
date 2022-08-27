from lib2to3.pgen2.token import DOUBLESLASH
import sys
from lxml import html
import requests
import re
import enum
from pprint import pprint

#python crawler.py rit.edu https://www.rit.edu/ 1

def get_command_args() -> list[str]:
    if (len(sys.argv)-1) < 3:
        # Stopping the script before breaking something
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]


def get_urls_a_tags(url:str) -> list[str]:
    response = requests.get(url)
    tree = html.fromstring(html=response.text)
    return tree.xpath('//a/@href')


def has_prefix(string: str, prefix: str) -> bool:
     return bool(re.search(f'^{prefix}', string))


def prefix_remover(string: str, prefix: str) -> str:
    return string[len(prefix):]


def remove_duplicates(urls:list[str]) -> list[str]:
    return list(set(urls))


class URL(enum.Enum):
    HTTPS = "https://"
    HTTP = "http://"
    DOUBLESLASH = "//"
    SINGLESLASH = "/"
    EXTENSIONS = ""

def filtering_urls(urls:list[str], prefixs_filter:list[str]) -> dict[str: list[str]]:
    url_dict = {type.name: list() for type in URL}

    for url in urls:
        for prefix in prefixs_filter:
            if has_prefix(url, prefix.value):
                urls_list = url_dict.get(prefix.name)
                urls_list.append(url)
                continue
    return url_dict


def main():
    domain, url, depth= get_command_args()
    orig_urls = get_urls_a_tags(url)
    no_dup_urls = remove_duplicates(orig_urls)
    url_dict = filtering_urls(no_dup_urls, [URL.HTTPS, URL.HTTP, URL.DOUBLESLASH, URL.SINGLESLASH])
    pprint(url_dict)


if __name__ == "__main__":
    main()
