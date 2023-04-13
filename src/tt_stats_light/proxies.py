from functools import reduce
from typing import Dict, List, Optional, Tuple
from src.tt_stats_light.utils import open_file, save_file
import requests

PROXY_TYPES: Tuple[str] = ("http", "https", "socks4", "socks5")


def proxy_type_from_url(url: str) -> str:
    file_name = url.split("/")[-1]
    assert ".txt" in file_name
    file_name = file_name.replace(".txt", "")

    if file_name.lower() in PROXY_TYPES:
        return file_name
    else:
        return "undefined"


def prepare_urls() -> Dict:
    raw_urls = open_file("proxies_paths.txt")
    urls = raw_urls.split()
    proxies_template = {proxy_type: dict(urls=[], proxies=[]) for proxy_type in PROXY_TYPES + ("undefined",)}
    for url in urls:
        proxy_type = proxy_type_from_url(url)
        proxies_template[proxy_type]["urls"].append(url)

    return proxies_template


def download_proxies(download_url) -> List[str]:
    responce = requests.get(download_url)
    assert responce.ok
    proxies = responce.text.split()
    clear_proxies = list(map(lambda proxy: proxy.strip(), proxies))
    return clear_proxies


def download_all_proxies(proxy_types: Optional[List[str]] = None):
    proxy_types = PROXY_TYPES + ("undefined",) if proxy_types is None else proxy_types
    all_proxies = prepare_urls()
    for proxy_type in proxy_types:
        for url in all_proxies[proxy_type]["urls"]:
            proxies_by_type = download_proxies(url)
            all_proxies[proxy_type]["proxies"].append(proxies_by_type)
    return all_proxies


def prepare_to_save(all_proxies: Dict) -> Dict:
    for proxy_type in all_proxies.keys():
        # concatenate proxies over urls
        proxies = set(reduce(lambda x, y: x + y, all_proxies[proxy_type]["proxies"]))
        if len(proxies) > 0:
            all_proxies[proxy_type]["proxies"] = list(proxies)
        else:
            all_proxies.pop(proxy_type)
    return all_proxies


def save_proxies(all_proxies: Dict):
    for proxy_type in all_proxies.keys():
        data = "\n".join(all_proxies[proxy_type]["proxies"])
        save_file(data, f"proxies/{proxy_type}.txt")


def main_load_save_flow():
    all_proxies = download_all_proxies()
    prepared_proxies = prepare_to_save(all_proxies)
    save_proxies(prepared_proxies)

# надо делать полноценный объект, потому что в нем должно быть очень много функциональностей
def proxy_iterator(proxy_types: Tuple[str] = PROXY_TYPES):
    pass


if __name__ == "__main__":
    main_load_save_flow()
