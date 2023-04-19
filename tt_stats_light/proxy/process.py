from functools import reduce
from typing import Dict
from tt_stats_light.files.load_save import open_file
from tt_stats_light.proxy.constants import PROXY_TYPES


def proxy_type_from_path(url: str) -> str:
    file_name = url.split("/")[-1]
    assert ".txt" in file_name
    file_name = file_name.replace(".txt", "")

    if file_name.lower() in PROXY_TYPES:
        return file_name
    else:
        return "undefined"


def make_proxies_template() -> Dict:
    return {proxy_type: dict(urls=[], proxies=[]) for proxy_type in PROXY_TYPES + ("undefined",)}


def prepare_urls() -> Dict:
    raw_urls = open_file("proxies_paths.txt")
    urls = raw_urls.split()
    proxies_template = make_proxies_template()
    for url in urls:
        proxy_type = proxy_type_from_path(url)
        proxies_template[proxy_type]["urls"].append(url)

    return proxies_template


def prepare_to_save(all_proxies: Dict) -> Dict:
    for proxy_type in all_proxies.keys():
        # concatenate proxies over urls
        proxies = set(reduce(lambda x, y: x + y, all_proxies[proxy_type]["proxies"]))
        if len(proxies) > 0:
            all_proxies[proxy_type]["proxies"] = list(proxies)
        else:
            all_proxies.pop(proxy_type)
    return all_proxies
