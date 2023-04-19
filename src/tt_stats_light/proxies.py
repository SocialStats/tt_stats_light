from functools import reduce
import random
from time import sleep
from typing import Dict, List, Optional, Tuple
from src.tt_stats_light.utils import open_file, save_file, BASE_DATA_DIR
from loguru import logger
import requests

logger.add("logs/proxies.log", format="{time} {level} {message}", level="INFO")
PROXY_TYPES: Tuple[str] = ("http", "https", "socks4", "socks5")


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


def prepare_to_save(all_proxies: Dict) -> Dict:
    for proxy_type in all_proxies.keys():
        # concatenate proxies over urls
        proxies = set(reduce(lambda x, y: x + y, all_proxies[proxy_type]["proxies"]))
        if len(proxies) > 0:
            all_proxies[proxy_type]["proxies"] = list(proxies)
        else:
            all_proxies.pop(proxy_type)
    return all_proxies


def save_proxies(all_proxies: Dict) -> None:
    for proxy_type in all_proxies.keys():
        data = "\n".join(all_proxies[proxy_type]["proxies"])
        save_file(data, f"proxies/{proxy_type}.txt")


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


def main_load_save_flow():
    all_proxies = download_all_proxies()
    prepared_proxies = prepare_to_save(all_proxies)
    save_proxies(prepared_proxies)


# TODO надо делать полноценный объект, потому что в нем должно быть очень много функциональностей
def proxy_iterator(proxy_types: Tuple[str] = PROXY_TYPES):
    all_proxies = load_proxies(proxy_types)


class ProxyIterator:
    sleep_time = 10

    def __init__(self, proxy_types: Tuple[str] = PROXY_TYPES):
        self.proxy_types = proxy_types
        self.all_proxies = load_proxies(proxy_types)

    def __iter__(self):
        return self

    def _get_proxy_types(self):
        return list(self.all_proxies.keys())

    def _reload_proxies(self):
        self.all_proxies = load_proxies(self.proxy_types)
        logger.info("Reload proxies")

    def _remove_proxy_type(self, proxy_type):
        if len(self.all_proxies[proxy_type]["proxies"]) == 0:
            self.all_proxies.pop(proxy_type)
            logger.info(f"Remove proxy type: {proxy_type}")

    def _get_random_proxy(self) -> Tuple[str, str]:
        """Get random proxy from all_proxies"""
        if len(self._get_proxy_types()):
            proxy_type = random.choice(self._get_proxy_types())
            len_proxies = len(self.all_proxies[proxy_type]["proxies"])
            if len_proxies:
                random_index = random.randint(0, len_proxies - 1)
                random_proxy = self.all_proxies[proxy_type]["proxies"].pop(random_index)

                self._remove_proxy_type(proxy_type)

                return proxy_type, random_proxy
            else:
                self._remove_proxy_type(proxy_type)
                return self._get_random_proxy()
        else:
            raise IndexError("No proxies")

    def __next__(self) -> Tuple[str, str]:
        """one step of iteration with randomize proxy"""
        if len(self.all_proxies) == 0:
            self._reload_proxies()
        try:
            return self._get_random_proxy()
        except IndexError:
            sleep(self.sleep_time)
            self._reload_proxies()
            return self._get_random_proxy()


if __name__ == "__main__":
    main_load_save_flow()
