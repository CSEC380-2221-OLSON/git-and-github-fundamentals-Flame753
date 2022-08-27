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


def filtering_out_bad_urls(urls:list[str], good_urls_features:list[str]) -> list[str]:
    # Filtering out from the start of the URL string any bad urls
    new_urls_list = list()
    for url in urls:
        for feature in good_urls_features:
            # Searching from the start for a matching string
            if re.search(f'^{feature}', url):
                new_urls_list.append(url)
                continue
    return new_urls_list


def remove_duplicates(urls:list[str]) -> list[str]:
    return list(set(urls))


def url_extension_spliter(urls:list[str]) -> dict[str:list[str]]:
    urls_with_domain = filtering_out_bad_urls(urls, good_urls_features=["http", "//"])
    extensions = [url for url in urls if url not in urls_with_domain]
    return {"urls": urls_with_domain, "extensions": extensions}


def main():
    domain, url, depth= get_command_args()
    orig_urls = get_urls_a_tags(url)
    no_dup_urls = remove_duplicates(orig_urls)
    print(no_dup_urls)
    url_dict = url_extension_spliter(no_dup_urls)
    pprint(url_dict)


if __name__ == "__main__":
    main()