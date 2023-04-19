from tt_stats_light.data.save import save_proxies
from tt_stats_light.proxy.load import download_all_proxies
from tt_stats_light.proxy.process import prepare_to_save


def load_and_save_flow() -> None:
    all_proxies = download_all_proxies()
    prepared_proxies = prepare_to_save(all_proxies)
    save_proxies(prepared_proxies)


if __name__ == "__main__":
    load_and_save_flow()
