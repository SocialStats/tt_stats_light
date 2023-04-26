# tt_stats_light
This is a free TikTok analytics tool on GitHub that provides valuable insights into TikTok accounts. The tool is easy to use and provides detailed analytics that can help users improve their performance on TikTok.


## Features
- [x] **Account analytics** - get detailed analytics for any TikTok account
- [x] **Video analytics** - get detailed analytics for any TikTok video

## Installation
1. Clone the repository
2. Move to the project directory
```cd tt_stats_light```
3. Install the requirements
```pip install -r requirements.txt```

## Usage
1. Download proxies
    
    you can add more proxy sources in the file ```data/proxies_paths.txt```

```python -m tt_stats_light.proxy.run```

2. Run the scripts to crawl user data
```python -m tt_stats_light.crawler.get_user_data <username>```
3. Run the scripts to compute user statictics
```python -m tt_stats_light.data.compute_stats <path_to_row_data>```
4. Enjoy the results in the ```data/results/``` folder


## Examples
### Account analytics
```python -m tt_stats_light.crawler.get_user_data therock```
```python -m tt_stats_light.data.compute_stats data/raw/therock.csv```

***
## License
[MIT](https://choosealicense.com/licenses/mit/)

