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


class UrlPrefix(enum.Enum):
    URL = ["https://", "http://", "//"]
    EXTENSIONS = ["/"]

class UrlDict():
    def __init__(self) -> None:
        self.default = UrlPrefix.EXTENSIONS

    def create_url_dict(self) -> dict[str: list]:
        return {type.name: list() for type in UrlPrefix}


def url_prefix_separator_remover(url_dict: dict[str: list], url: str) -> None:
    # Splitting up the urls given into two groups URLs and Extensions. Plus, remove any slashes or http:// in front the url.
    for type in UrlPrefix:
        for prefix in type.value:
            if has_prefix(url, prefix):
                url_list = url_dict.get(type.name)
                url_list.append(prefix_remover(url, prefix))
                return

    default_list = url_dict.get(UrlDict().default.name)
    default_list.append(url)
        

def filtering_urls(urls:list[str]) -> dict[str: list[str]]:
    url_dict = UrlDict().create_url_dict()
    for url in urls:
       url_prefix_separator_remover(url_dict, url)
    return url_dict


def main():
    domain, url, depth= get_command_args()
    orig_urls = get_urls_a_tags(url)
    no_dup_urls = remove_duplicates(orig_urls)
    url_dict = filtering_urls(no_dup_urls)
    pprint(url_dict)


if __name__ == "__main__":
    main()
