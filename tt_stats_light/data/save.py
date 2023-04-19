from typing import Dict

from tt_stats_light.files.load_save import save_file


def save_proxies(all_proxies: Dict) -> None:
    for proxy_type in all_proxies.keys():
        data = "\n".join(all_proxies[proxy_type]["proxies"])
        save_file(data, f"proxies/{proxy_type}.txt")
