from typing import Dict, List, Optional, Tuple
from tt_stats_light.constants import BASE_DATA_DIR
from tt_stats_light.files.load_save import open_file
from tt_stats_light.proxy.constants import PROXY_TYPES
from tt_stats_light.proxy.process import make_proxies_template, prepare_urls, proxy_type_from_path
import requests


def download_proxies(download_url) -> List[str]:
    responce = requests.get(download_url)
    assert responce.ok
    proxies = responce.text.split()
    clear_proxies = list(map(lambda proxy: proxy.strip(), proxies))
    return clear_proxies


def download_all_proxies(proxy_types: Optional[List[str]] = None) -> Dict:
    proxy_types = PROXY_TYPES + ("undefined",) if proxy_types is None else proxy_types
    all_proxies = prepare_urls()
    for proxy_type in proxy_types:
        for url in all_proxies[proxy_type]["urls"]:
            proxies_by_type = download_proxies(url)
            all_proxies[proxy_type]["proxies"].append(proxies_by_type)
    return all_proxies


def load_proxies(proxy_types: Tuple[str] = PROXY_TYPES) -> Dict:
    proxy_files_names = list(BASE_DATA_DIR.glob("proxies/*.txt"))
    assert len(proxy_files_names), "No downloaded proxies"

    all_proxies = make_proxies_template()
    for proxy_files_name in proxy_files_names:
        proxy_type = proxy_type_from_path(proxy_files_name.name)
        proxies = open_file(proxy_files_name, base=False).split()
        if len(proxies) > 0:
            all_proxies[proxy_type]["proxies"] = proxies
        else:
            all_proxies.pop(proxy_type)

    # delete extra proxy_types (not needful)
    for proxy_type in list(all_proxies.keys()):
        if proxy_type not in proxy_types:
            all_proxies.pop(proxy_type)

    return all_proxies
