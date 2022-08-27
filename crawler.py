import sys
from lxml import html
import requests
import re
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


def filtering_out_urls(urls:list[str], prefixs_filter:str) -> list[str]:
    new_urls_list = list()
    for url in urls:
        if has_prefix(url, prefixs_filter):
            new_urls_list.append(url)
    return new_urls_list


def url_extension_spliter(urls:list[str]) -> dict[str:list[str]]:

    https_urls = filtering_out_urls(urls, prefixs_filter="https://")
    urls_without_https = [url for url in urls if url not in https_urls]

    http_urls = (filtering_out_urls(urls_without_https, prefixs_filter="http://"))
    urls_without_http = [url for url in urls_without_https if url not in http_urls]

    double_slash_urls = (filtering_out_urls(urls_without_http, prefixs_filter="//"))
    urls_without_double_slashes = [url for url in urls_without_http if url not in double_slash_urls]

    single_slash_extensions = (filtering_out_urls(urls_without_double_slashes, prefixs_filter="/"))
    extensions_without_single_slashes = [url for url in urls_without_double_slashes if url not in single_slash_extensions]
    
    return {"https_urls": https_urls, 
            "http_urls": http_urls,
            "double_slash_urls": double_slash_urls,
            "single_slash_extensions": single_slash_extensions,
            "extensions": extensions_without_single_slashes}



def main():
    domain, url, depth= get_command_args()
    orig_urls = get_urls_a_tags(url)
    no_dup_urls = remove_duplicates(orig_urls)
    url_dict = url_extension_spliter(no_dup_urls)
    pprint(url_dict)


if __name__ == "__main__":
    main()
