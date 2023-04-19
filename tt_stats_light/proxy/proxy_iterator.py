import random
from time import sleep
from typing import Tuple
from loguru import logger

from tt_stats_light.proxy.constants import PROXY_TYPES
from tt_stats_light.proxy.load import load_proxies


logger.add("logs/loadproxies.log", format="{time} {level} {message}", level="INFO")


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
