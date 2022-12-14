# Author: Sergey Gurman 
# Class: CSEC 380

# -------------------------------------------------------------------------------------------

import sys
from lxml import html
import requests
import re
import enum
from pprint import pprint

# -------------------------------------------------------------------------------------------
# Example Script Command:
# python crawler.py rit.edu https://www.rit.edu/ 1

# -------------------------------------------------------------------------------------------
# Getting the arguments from the command line

def get_command_args() -> list[str]:
    # Stopping the script before breaking something
    if (len(sys.argv)-1) < 3:
        sys.exit()
    # Assuming the first 3 inputs was enter correctly. NO sanitaion was done! 
    return sys.argv[1:4]

# -------------------------------------------------------------------------------------------
# Getting the URLs from the Webpage

def get_urls_a_tags(url:str) -> list[str]:
    response = requests.get(url)
    tree = html.fromstring(html=response.text)
    return tree.xpath('//a/@href')

# Removing any duplicates that came from the HTML a-tags.
def remove_duplicates(urls:list[str]) -> list[str]:
    return list(set(urls))

# -------------------------------------------------------------------------------------------
# Organizing the URLs

def has_prefix(string: str, prefix: str) -> bool:
     return bool(re.search(f'^{prefix}', string))


def prefix_remover(string: str, prefix: str) -> str:
    return string[len(prefix):]


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

# -------------------------------------------------------------------------------------------
# Removing any urls that don't match the domain

def remove_non_matching_domain(urls: list[str], domain: str) -> list[str]:
    return [url for url in urls if has_prefix(url, domain)]


# -------------------------------------------------------------------------------------------

def cralwer(domain, url, depth=0):
    orig_urls = get_urls_a_tags(url)
    no_dup_urls = remove_duplicates(orig_urls)
    url_dict = filtering_urls(no_dup_urls)  # Splitting up urls and extesions
    urls_with_desired_domain = remove_non_matching_domain(url_dict.get(UrlPrefix.URL.name), domain)

    extensions = [prefix_remover(x, f"{domain}/") for x in urls_with_desired_domain]  # Converting urls into extension
    extensions.extend(url_dict.get(UrlPrefix.EXTENSIONS.name))  # Combining previous extensions with new extensions
    all_extensions = remove_duplicates(extensions)  # Removing any extension that came from converting urls into extensions

    if depth == 0:
        return all_extensions
    else:
        for extension in all_extensions:
            new_domain = f"{domain}/{extension}"
            new_url = f"{url}/{extension}"
            
            return cralwer(new_domain, new_url, depth-1)

def main():
    domain, url, depth= get_command_args()
    output = cralwer(domain, url, int(depth))
    pprint(len(output))

    # pprint(len(extensions))
    # pprint(all_extensions)


if __name__ == "__main__":
    main()
